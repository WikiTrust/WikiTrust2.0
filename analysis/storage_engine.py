
import datetime

class StorageEngine(object):

    def __init__(self, db, num_objects_per_blob=10, database_table=None,
                 default_version=None):
        """
        :param db: handle to the pydal database to be used.
        :param num_objects_per_blob:
        :param database_table:
        :param default_version:
        """
        pass


    def store(self, page_id: int, version_id: str, rev_id: int, text: str, timestamp: datetime.datetime):
        """Writes to the store.
        :param page_id: id of page (or in general, of compression space)
        :param version_id: id of the version we are writing.
        :param rev_id: id of revision (or in general, of object in space)
        :param text: text to be written (a python string)
        :param timestamp: timestamp originally of revision in wikipedia.
        :return: a boolean indicating whether all has been written (True) or whether some
            changes are pending (False) for the given page_id and version_id.
        """
        pass


    def read(self, page_id: int, version_id: str, rev_id: int) -> str:
        """
        Reads from the text storage.
        :param page_id:
        :param version_id:
        :param rev_id:
        :return: The string that was written.
        """
        pass


    def flush(self, page_id: int, version_id: str):
        """Writes all remaining changes to the given page_id and version_id."""
        pass


class RevisionEngine(StorageEngine):
    pass

class TextReputationEngine(StorageEngine):
    pass
