import datetime
from datetime import datetime
import os
import json
import traceback
import zlib
import collections

from google.cloud import storage
from threading import Lock


__all__ = ['StorageEngine']

class StorageEngine(object):

    def __init__(self, num_revs_per_file=10, bucket_name=None, database_table=None,
                 default_version=0):
        """
        :param db: handle to the pydal database to be used.
        :param num_objects_per_blob:
        :param str database_table: the name of the database table for the storage engine
        :param default_version: Default blob version

        Builds an GCS access controller.
        Another way is to provide the path to the json via:
        export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
        """
        self.db_table = db.database_table
        json_key = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        self.client = storage.Client.from_service_account_json(json_key)
        self.bucket_name = bucket_name
        self.num_revs_per_file = num_revs_per_file
        self.lock = Lock()
        self.cache = collections.OrderedDict()
        self.cache_size = 1000
        self.revision_dict = {}
        self.current_blob_name = None
        self.default_version = default_version

        pass


    def store(self, page_id: int, version_id: str, rev_id: int, text: str, timestamp: datetime.datetime, kind: str):
        """Writes to the store.
        :param page_id: id of page (or in general, of compression space)
        :param version_id: id of the version we are writing.
        :param rev_id: id of revision (or in general, of object in space)
        :param text: text to be written (a python string)
        :param timestamp: timestamp originally of revision in wikipedia.
        :return: a boolean indicating whether all has been written (True) or whether some
            changes are pending (False) for the given page_id and version_id.
        """
        
        with self.lock:
            if rev_id is None:
                print("Could not write revision: No rev_id")
                return False

            if self.current_blob_name is None:
                self.current_blob_name = rev_id + "-" + version_id
                
            self.db_table.insert(revision_id=rev_id, version=version_id, blob=self.current_blob_name,
                revision_date = timestamp, kind=kind)
            
            self.revision_dict[str(rev_id)] = text
            if len(self.revision_dict) >= self.num_revs_per_file:
                self.__write_revisions()
                return True
            return False

        return False


    def read(self, page_id: int, version_id: str, rev_id: int, do_cache=True) -> str:
        """
        Reads from the text storage.
        :param page_id:
        :param version_id:
        :param rev_id:
        :return: The string that was written.
        """
        query = (self.db_table.version == version_id) and (page_id == self.db_table.page_id) and (rev_id == self.db_table.revision_id)
        blob_list = self.db_table(query).select(self.db_table.blob)
        if len(blob_list) <= 0:
            return None
        blob_name = blob_list[0] + "-" + version_id

        s = None
        if do_cache and blob_name in self.cache:
            s = self.cache[blob_name]
        if s is None:
            s = self.__read(self.bucket_name, blob_name)
            if s and do_cache:
                self.__make_cache_space()
                self.cache[blob_name] = s
        if s is not None:
            revision_dict = json.loads(zlib.decompress(s).decode('utf-8'))
            try:
                return revision_dict[rev_id]
            except:
                return None
        else:
            return None


    def flush(self):
        """Writes any remaining revisions to the GCS bucket immediately."""
        with self.lock:
            self.__write_revisions()

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

class RevisionEngine(StorageEngine):
    pass

class TextReputationEngine(StorageEngine):
    pass