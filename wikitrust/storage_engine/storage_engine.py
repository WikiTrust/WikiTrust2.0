import datetime
from datetime import datetime
from logging import error
import os
import json
import traceback
from typing import Dict
import zlib
import collections
from google.cloud import storage
from threading import Lock

from wikitrust.computation_engine.wikitrust_algorithms.author_reputation import version

__all__ = ['StorageEngine']
__num_revs_per_slot__ = 10  # DO NOT CHANGE THIS VALUE LIGHTLY, if the slot num changes, all previously saved pages/revisions will have the wrong slot calculated and will not load.
__gcs_access_key_json_file__ = "./private/wikitrust-prod-643472bb33d3.json"


class StorageEngine(object):
    def __init__(
        self,
        bucket_name=None,
        storage_db_ctrl=None,
        version=0,
        text_type="revision"
    ):
        """
        :param storage_db_ctrl: handle to the databse controller instance.
        :param num_objects_per_blob: CAUTION CHanging this will break existing storage! (Number of items to compress together in each GCS file)
        :param str database_table: the name of the database table for the storage engine
        :param default_version: Blob version

        Builds an GCS access controller.
        Another way is to provide the path to the json via:
        export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
        """
        self.storage_db_ctrl = storage_db_ctrl  # database controller for storage engine
        self.bucket_name = bucket_name  # the name of the GCS bucket to store the data in (e.g. testing or production buckets)
        self.lock = Lock()  # Lock for thread safety
        self.cache = collections.OrderedDict(
        )  # a cache of the compressed slots that have been downloaded in the current session.
        self.cache_size = 1000  # number of revisions to keep in memory cache
        self.page_dict = {
        }  # a temporary store to hold (for each page) an array containing any slots that are being filled / aren't yet full. -  (each slot is an array of revisions' text or trust)
        self.version = version  # a version number used to isolate storage engine data, so the engine will not see blobs created with a different version number.
        # NOTE: the above verson number has not been tested for being changed, it will probably break with the db records and sutch so test first before you change it.
        self.text_type = text_type  # the type of data to store in the storage engine (e.g. revision, text_trust, etc.) - Used by the extended classes. - sorts the data into folders on gcs

        self.GCS = storage.Client.from_service_account_json(
            __gcs_access_key_json_file__
        )

    def __enter__(self):
        """
        Used for returning self for "with" statement
        """
        return self

    def __exit__(self):
        """
        Used for performing flash storage on "with" statement exit
        """
        self.flush()
        pass

    def store(self, page_id: int, rev_id: int, text: str, timestamp: datetime):
        """Writes to the store.
        :param page_id: id of page
        :param rev_id: id of revision
        :param text: text or data to be written (a python string)
        :param timestamp: timestamp originally of revision in wikipedia.
        :return: a boolean indicating whether all has been written (True) or whether some
            changes are pending (False) for the given page_id and version_id.
        """
        with self.lock:  # Thread safety
            if rev_id is None:
                raise Exception(
                    "Could not write revision: No rev_id provided. PageId:" +
                    str(page_id) + " " + " Text:" + text
                )

            # Storage table DB query
            rev_blob_name = self.storage_db_ctrl.get_storage_blob_name(
                page_id=page_id,
                version_id=self.version,
                rev_id=rev_id,
                text_type=self.text_type
            )
            if (rev_blob_name != None):
                # we're using the existance of a blob name in the db to indicate that the revision has already been stored.
                print(
                    f'TYPE:{self.text_type} Page: {page_id} Rev: {rev_id} is already stored in engine. Skipping...'
                )
                # Do not overwrite if a revision text with the givien version_id,page_id,rev_id exists
                return False

            # Make sure the page_dict is ready to accept any slots for this page
            if page_id not in self.page_dict:
                self.page_dict[page_id] = {}

            # calculate the slot num and blob name for this revision given the revision id and page id
            slot_num = self._calculate_slot_num(page_id=page_id, rev_id=rev_id)
            blob_name = self._generate_blob_name(
                page_id=page_id, slot_num=slot_num
            )

            if slot_num not in self.page_dict[page_id]:
                # if the slot is not in the page_dict temporary storage, create the page_dict >page >slot to be filled.
                self.page_dict[page_id][slot_num] = {}

                # check if any revisions were previously stored in this slot, on a previous run of the program.
                exisitng_revisions_in_blob_count = self.storage_db_ctrl.count_revisions_in_blob(
                    blob_name, self.text_type
                )
                if exisitng_revisions_in_blob_count > 0:
                    # if there are any revisions in the (partially filled) slot, then we need to load them into the page_dict for this page > slot.
                    found_revs = self.pull_all_revisions_in_slot(
                        page_id, rev_id, do_cache=False
                    )
                    self.page_dict[page_id][slot_num] = found_revs

            # add the revision we want to store to the right slot in the right page in page_dict temporary storage
            self.page_dict[page_id][slot_num][str(rev_id)] = text

            # LONG message for debugging the whole contents of a slot:
            print(
                f'Type:{self.text_type} RevId: {rev_id} is now in PageId: {page_id} slotNum: {slot_num} in storage engine... :'
            )

            # find out how full this slot is
            num_revisions_in_this_slot = len(self.page_dict[page_id][slot_num])
            print(
                "This slot has " + str(num_revisions_in_this_slot) +
                " spots full"
            )

            # if the slot is full, write the whole slot in the page_dict temporary storage to GCS as a blob
            if num_revisions_in_this_slot >= __num_revs_per_slot__:
                print("writing to storage engine because slot is full...")
                self._write_revisions(page_id, slot_num)
                return True

            # return false to indicate that the slot is not full yet.
            return False

    def read(self, page_id: int, rev_id: int, do_cache=False) -> str:
        slot_num = self._calculate_slot_num(page_id=page_id, rev_id=rev_id)
        if (
            page_id in self.page_dict and
            slot_num in self.page_dict[page_id] and
            str(rev_id) in self.page_dict[page_id][slot_num]
        ):
            return self.page_dict[page_id][slot_num][str(rev_id)]

        db_data = self.pull_all_revisions_in_slot(page_id, rev_id, do_cache)
        if db_data == {}:
            return ""
        else:
            return db_data[str(rev_id)]

    def pull_all_revisions_in_slot(
        self, page_id: int, rev_id: int, do_cache=True
    ) -> Dict:
        """
        Reads all the revisions in the slot that should contain this revision's text.
        :param page_id:
        :param rev_id:
        :return: The array of all revisions in the pulled slot.
        """


        # see _calculate_slot_num for an explanation of what slots are
        slot_num = self._calculate_slot_num(page_id, rev_id)

        # Storage db table query, try to get the name of the blob (aka a "slot") in GCS that contains the revision
        rev_blob_name = self.storage_db_ctrl.get_storage_blob_name(
            rev_id=rev_id,
            page_id=page_id,
            version_id=self.version,
            text_type=self.text_type
        )
        if rev_blob_name == None:
            # we could potentially recover here by re-creating the slot name from the rev_id and trying to read from the slot
            print(
                "Trying to read " + self.text_type + " page_id: " +
                str(page_id) + " rev_id:" + str(rev_id) +
                " without blob name in storage db. Attempting to _generate_blob_name() from revision index instead"
            )
            rev_blob_name = self._generate_blob_name(page_id, slot_num)

        s = None
        # Try to read the blob from the cache
        if do_cache and rev_blob_name in self.cache:
            s = self.cache[rev_blob_name]

        # If not in cache, read from GCS
        if s is None:
            s = self._gcs_read(self.bucket_name, rev_blob_name)
            # and add it to the cache:
            if s and do_cache:
                self.__make_cache_space()
                self.cache[rev_blob_name] = s

        # If the blob was found, either in cache or GCS, decompress it, parse the stored json and return the result:
        if s is not None:
            json_text = zlib.decompress(s).decode('utf-8')
            result = json.loads(json_text)
            return result

        # If the blob was not found, Raise an error
        else:
            raise Exception(
                "STORAGE ENGINE (" + str(self.text_type) +
                "): Could not load blob for page_id: " + str(page_id) +
                " rev_id:" + str(rev_id) +
                ", was that revision stored before?: "
            )

    def flush(self):
        """Writes any remaining revisions to the GCS bucket immediately."""
        with self.lock:
            print(
                "Flushing " + self.text_type +
                " storage engine... Current page_dict:"
            )
            for page_id in list(self.page_dict.keys()):
                print(page_id)
                for slot_num in list(self.page_dict[page_id].keys()):
                    print("   " + str(slot_num))
                    if (
                        page_id in self.page_dict and
                        slot_num in self.page_dict[page_id]
                    ):
                        print(
                            "      " +
                            str(list(self.page_dict[page_id][slot_num].keys()))
                        )
                        self._write_revisions(page_id, slot_num)

    def _write_revisions(self, page_id, slot_num):
        """write the whole slot in the page_dict temporary storage for the given page_id > slot_num to GCS as a compressed blob"""
        blob_name = self._generate_blob_name(page_id, slot_num)

        print(
            "writing blob " + blob_name + "  to " + self.text_type +
            " folder in gcs bucket "
        )

        if self.page_dict[page_id][slot_num] != None and len(
            self.page_dict[page_id][slot_num]
        ) > 0:
            revisions_json = json.dumps(self.page_dict[page_id][slot_num])
            compressed_contents = zlib.compress(bytes(revisions_json, 'utf-8'))
            self._gcs_write(
                self.bucket_name,
                blob_name,
                compressed_contents,
                type='application/zlib'
            )

            # for all of the revisions in the slot we just wrote, note the blob name in the storage db corresponding to each revision
            for revision in self.page_dict[page_id][slot_num]:
                self.storage_db_ctrl.insert_blob_name(
                    rev_id=revision,
                    version_id=self.version,
                    page_id=page_id,
                    blob_name=blob_name,
                    text_type=self.text_type
                )

            # remove the slot_num in this page from the page_dict temporary storage
            print("Before popping:" + str(self.page_dict[page_id].keys()))
            self.page_dict[page_id].pop(slot_num)
            print(
                "After popping " + str(slot_num) + ":" +
                str(self.page_dict[page_id].keys())
            )

    def __make_cache_space(self):
        """
        Checks the length of the cache and if over self.cache_size, removes the first n revisions
        in the cache so the cache length is back to self.cache_size.
        """
        keys = self.cache.keys()
        full = len(keys) - self.cache_size
        if full >= 0:
            for key in keys[0:full + 1]:
                del self.cache[key]

    def _calculate_slot_num(self, page_id, rev_id):
        """The slot number is the blob in gcs that the revision goes in - like a page (a revision) in a book of consecutive revisions (the slot/blob) on a shelf (a wiki page) in a library (the gcs bucket folder)"""
        # Revision db table query, try to get the revision index from the revision ID
        rev_idx = self.storage_db_ctrl.get_rev_idx(
            rev_id=rev_id, page_id=page_id
        )
        if rev_idx == None:
            raise Exception(
                "STORAGE ENGINE (" + str(self.text_type) +
                "): Could not find revision index of page_id: " + str(page_id) +
                " rev_id:" + str(rev_id)
            )

        # Calculate the slot number by performing integer division by the number of revisions in each slot
        slot_num = rev_idx // __num_revs_per_slot__
        return slot_num

    def _generate_blob_name(self, page_id, slot_num):
        """Returns the naming scheme used to name the GCS blob for the given slot number"""
        return str(self.version) + "-" + str(page_id) + "-" + str(slot_num)

    def _gcs_write(self, bucketname, filename, content, type='text/plain'):
        """
        Writes content to GCS from a string
        :param bucketname: Bucket name.
        :param filename: File name in GCS.
        :param content: Content to be written.
        :param type: Type (default: text/plain).
        :return: Nothing.
        """
        bucket = self.GCS.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.upload_from_string(content, content_type=type)

    def _gcs_read(self, bucketname, filename):
        """
        Reads content from GCS.
        :param bucketname: Bucket name.
        :param filename: File name.
        :return: The content read.
        """
        bucket = self.GCS.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        return blob.download_as_string()  # returns None if not present

    # More unused GCS related functions from Luca

    # def _gcs_upload(self, bucketname, filename, local_file, type='text/plain'):
    #     """
    #     Writes content to GCS from a local file, presumed open.
    #     :param bucketname: Bucket name.
    #     :param filename: desination filename in GCS.
    #     :param local_file: file-like object.
    #     :param type: Type of file.  Consider 'application/octet-stream' if you don't know.
    #     :return: Nothing.
    #     """
    #     bucket = self.GCS.get_bucket(bucketname)
    #     blob = storage.Blob(filename, bucket)
    #     blob.upload_from_file(local_file, content_type=type)

    # def _gcs_download(self, bucketname, filename, local_file):
    #     """
    #     Download blob to a local file.
    #     :param bucketname: Bucket name in GCS.
    #     :param filename: File name in GCS.
    #     :param local_file: Local file (open for writing).
    #     :return: Nothing.
    #     """
    #     bucket = self.GCS.get_bucket(bucketname)
    #     blob = storage.Blob(filename, bucket)
    #     blob.download_to_file(local_file)

    # def _gcs_delete(self, bucketname, filename):
    #     """
    #     Deletes a file.
    #     :param bucketname: Bucket name.
    #     :param filename: File name.
    #     :return: Nothing.  Raises error if not present.
    #     """
    #     bucket = self.GCS.get_bucket(bucketname)
    #     blob = storage.Blob(filename, bucket)
    #     blob.delete()  # raises error if not present

    # def _gcs_listfiles(self, bucketname, maximum=None):
    #     """
    #     Lists files in a given bucket.
    #     :param bucketname: Name of the bucket.
    #     :param maximum: Maximum number of files to list.
    #     :return: A list of file names.
    #     """
    #     bucket = self.GCS.get_bucket(bucketname)
    #     return [
    #         blob.name for k, blob in enumerate(bucket.list_blobs())
    #         if maximum is None or k < maximum
    #     ]


class RevisionStorageEngine(StorageEngine):
    def __init__(self, bucket_name=None, storage_db_ctrl=None, version=0):
        return super().__init__(
            bucket_name=bucket_name,
            storage_db_ctrl=storage_db_ctrl,
            version=version,
            text_type="revision"
        )

    def _gcs_write(self, bucketname, filename, content, type='text/plain'):
        return super()._gcs_write(
            bucketname, "revisions/" + filename, content, type
        )

    def _gcs_read(self, bucketname, filename):
        return super()._gcs_read(bucketname, "revisions/" + filename)


class TextTrustStorageEngine(StorageEngine):
    def __init__(self, bucket_name=None, storage_db_ctrl=None, version=0):
        return super().__init__(
            bucket_name=bucket_name,
            storage_db_ctrl=storage_db_ctrl,
            version=version,
            text_type="trust"
        )

    def _gcs_write(self, bucketname, filename, content, type='text/plain'):
        return super()._gcs_write(
            bucketname, "text_reputation/" + filename, content, type
        )

    def _gcs_read(self, bucketname, filename):
        return super()._gcs_read(bucketname, "text_reputation/" + filename)
