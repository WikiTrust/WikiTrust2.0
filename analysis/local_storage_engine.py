import datetime
import json

class LocalStorageEngine(object):
    """
    A dummy implementation of the StorageEngine that is purely local. 
    Can be initialized with a JSON using the functions below.
    """
    def __init__(self, db, num_objects_per_blob=10, database_table=None,
                 default_version=None):
        """
        :param db: handle to the pydal database to be used.
        :param num_objects_per_blob:
        :param database_table:
        :param default_version:
        """

        #Initialize a dictionary mapping page_id to a page_dictionary
        self.pages = {}

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
        if page_id not in self.pages:
            self.pages[page_id] = {}

        self.pages[page_id][rev_id] = text


    def read(self, page_id: int, version_id: str, rev_id: int) -> str:
        """
        Reads from the text storage.
        :param page_id: id of page (or in general, of compression space)
        :param version_id: id of the version we are writing.
        :param rev_id: id of revision (or in general, of object in space)
        :return: The string that was written.
        """
        assert page_id in self.pages
        assert rev_id in self.pages[page_id]

        return self.pages[page_id][rev_id]


    def flush(self, page_id: int, version_id: str):
        """Writes all remaining changes to the given page_id and version_id."""
        pass

def load_page_json_into_storage(storage_engine, json):
    """
    Takes a JSON object containing information about a Wikipedia page and loads it into the storage engine.
    """
    page_id = int(json["pageId"])

    for rev_iter in range(int(json["size"])):
        rev_id = json["revisions"][rev_iter]["revisionId"]
        rev_text = json["revisions"][rev_iter]["text"]
        storage_engine.store(page_id, "DUMMY_VERSION", rev_id, rev_text, datetime.datetime.now())

    print(dummy_storage_engine.read(page_id, "DUMMY_VERSION", 429097598))
if __name__ == '__main__':
    dummy_storage_engine = LocalStorageEngine(db = None)

    with open("/home/ericvin/Projects/WikiTrust2.0/LadyGagaMeatDressRevisions/all_revision.json") as json_file:
        json_object = json.load(json_file)
        load_page_json_into_storage(dummy_storage_engine, json_object)
