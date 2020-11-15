# Luca de Alfaro, Massimo Di Pierro 2019
# BSD License
import os
import datetime
import json
import traceback
import zlib
import collections

from google.cloud import storage
from threading import Lock


__all__ = ['StorageEngine']


class StorageEngine(object):

    def __init__(self, bucket_name=None, num_revs_per_file=None):
        """
        Builds an GCS access controller.
        Another way is to provide the path to the json via:
        export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
        """
        json_key = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        self.client = storage.Client.from_service_account_json(json_key)
        self.bucket_name = bucket_name
        self.num_revs_per_file = num_revs_per_file
        self.lock = Lock()
        self.cache = collections.OrderedDict()
        self.cache_size = 1000
        self.revision_dict = {}
        self.current_blob_name = None

    def store(self, revision):
        """Stores a revision if it is new.
        :returns: True unless an error happens: whether the revision is new or not.
        If di is not None, then stores in the table the location of the revision.
        :param revision: A dict containing the a key value pair where the key is the revision ID & the value is the revision text """
        revision_id = list(revision.keys())[0]
        with self.lock:
            if revision_id is None:
                print("Could not write revision: No revision_id")
                return False

            if self.current_blob_name is None:
                self.current_blob_name = revision_id
                # Todo (if passing db): Writes revision path to revision table if new.
            # Maybe useful: path = self.bucket_name + '/' + self.current_blob_name

            self.revision_dict[str(revision_id)] = revision[revision_id]
            if len(self.revision_dict) >= self.num_revs_per_file:
                self.__write_revisions()
            return True

    def __write_revisions(self):
        """Compresses and stores the revisions in self.revision_dict in gcs"""
        if len(self.revision_dict) > 0:
            revisions_json = bytes(json.dumps(self.revision_dict), 'utf-8')
            s = zlib.compress(revisions_json)
            name = self.current_blob_name
            self.__write(self.bucket_name, name, s, type='application/zlib')
            # Empties the memory list.
        self.revision_dict = {}
        self.current_blob_name = None
                

    def flush(self):
        """
        Writes any remaining revisions to the GSC bucket immediately.
        """
        with self.lock:
            self.__write_revisions()

    def read_revision(self, revision_id=None, path=None, do_cache=True):
        """
        Returns a revision with a given revision_id, or None if there is no such revision.
        :param str revision_id: (Default = None) the revision_id to retrieve
        :param str path: (Default = None) the path to the GCS blob containing this revision. ie: bucket_name/blob_name
        :param bool do_cache: (Default = True) Use the cache. Attempts to returns revision text from the cache with a GCS fallback. If the requested revision was not in the cache, save that revision to the cache.
        """
        #    Luca Tweet Data Interface comment:
        #    One can either specify a data interface (di) and a tweet_id
        #    or a datastore path and the index within that path

        # only read from database if we do not already know
                # if di and tweet_id and not path and not idx:
                #     path, idx = di.read_tweet_location(tweet_id)
                # if path is None:
                #     return None
        path_parts = path.split('/')
        bucket_name = path_parts[0]
        blob_name = path_parts[1]
        s = None
        if do_cache and path in self.cache:
            s = self.cache[path]
        if s is None:
            s = self.__read(bucket_name, blob_name)
            if s and do_cache:
                self.__make_cache_space()
                self.cache[blob_name] = s
        if s is not None:
            revision_dict = json.loads(zlib.decompress(s).decode('utf-8'))
            print(revision_dict)
            try:
                return revision_dict[revision_id]
            except:
                return None
        else:
            return None

    def __make_cache_space(self):
        """
        Checks the length of the cache and if over self.cache_size, removes the first n revisions
        in the cache so the cache length is back to self.cache_size.
        """
        keys = self.cache.keys()
        full = len(keys) - self.cache_size
        if full >= 0:
            for key in keys[0: full+1]:
                del self.cache[key]

    def __enter__(self):
        """
        Used for returning self for "with" statement
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Used for performing flash storage on "with" statement exit
        """
        self.flush()
        pass
    
    def __write(self, bucketname, filename, content, type='text/plain'):
        """
        Writes content to GCS from a string
        :param bucketname: Bucket name.
        :param filename: File name in GCS.
        :param content: Content to be written.
        :param type: Type (default: text/plain).
        :return: Nothing.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.upload_from_string(content, content_type=type)

    def __upload(self, bucketname, filename, local_file, type='text/plain'):
        """
        Writes content to GCS from a local file, presumed open.
        :param bucketname: Bucket name.
        :param filename: desination filename in GCS.
        :param local_file: file-like object.
        :param type: Type of file.  Consider 'application/octet-stream' if you don't know.
        :return: Nothing.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.upload_from_file(local_file, content_type=type)

    def __read(self, bucketname, filename):
        """
        Reads content from GCS.
        :param bucketname: Bucket name.
        :param filename: File name.
        :return: The content read.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        return blob.download_as_string() # returns None if not present

    def __download(self, bucketname, filename, local_file):
        """
        Download blob to a local file.
        :param bucketname: Bucket name in GCS.
        :param filename: File name in GCS.
        :param local_file: Local file (open for writing).
        :return: Nothing.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.download_to_file(local_file)

    def __delete(self, bucketname, filename):
        """
        Deletes a file.
        :param bucketname: Bucket name.
        :param filename: File name.
        :return: Nothing.  Raises error if not present.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.delete() # raises error if not present

    def __listfiles(self, bucketname, maximum=None):
        """
        Lists files in a given bucket.
        :param bucketname: Name of the bucket.
        :param maximum: Maximum number of files to list.
        :return: A list of file names.
        """
        bucket = self.client.get_bucket(bucketname)
        return [blob.name for k, blob in enumerate(bucket.list_blobs())
                if maximum is None or k < maximum]



if __name__ == '__main__':
    se = StorageEngine(bucket_name='wikitrust-testing', num_revs_per_file=2)

    for i in range(4):
        print("Writing revision " + str(i))
        rev = {str(i)+"asdf": "stuff" + str(i)}
        se.store(rev)

    print(se.read_revision("1asdf", "wikitrust-testing/0asdf"))