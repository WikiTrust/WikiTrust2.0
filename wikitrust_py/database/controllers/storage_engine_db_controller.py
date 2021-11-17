from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date
import wikitrust_py.database.db_schema as db_schema
from wikitrust_py.database.controllers.db_wrappers import autocommit
import logging


class storage_engine_db_controller:
    def __init__(self, db):
        self.db = db
        self.storage_table = self.db.text_storage
        self.revision_table = self.db.revision

    """Writes to the store.
    :param page_id: id of page (or in general, of compression space)
    :param version_id: id of the version we are writing.
    :param rev_id: id of revision (or in general, of object in space)
    :return: Whether the given page/revision/version combo exists in the Storage table
                (meaning it is in a blob in a gcsbucket)
    """

    def get_storage_blob_name(
        self, page_id: int, version_id: int, rev_id: int, text_type: str
    ):
        # Returns
        query = (self.storage_table.version == version_id) & (page_id == self.storage_table.page_id) \
            & (rev_id == self.storage_table.rev_id) & (text_type == self.storage_table.text_type)
        blob_list = self.db(query).select(self.storage_table.blob)
        if blob_list != None and len(blob_list) > 0:
            return blob_list[0].blob
        return None

    def count_revisions_in_blob(self, blob_name: str, text_type: str):
        query = (self.storage_table.blob
                 == blob_name) & (self.storage_table.text_type == text_type)
        x = self.db(query).count()
        return x

    """Writes to the store.
    :param page_id: id of page (or in general, of compression space)
    :param version_id: id of the version we are writing.
    :param rev_id: id of revision (or in general, of object in space)
    :return: Whether the given page/revision/version combo exists in the Storage table
                (meaning it is in a blob in a gcsbucket)
    """

    def get_rev_idx(self, page_id: int, rev_id: int):
        query = (self.db.revision.rev_id
                 == rev_id) & (page_id == self.db.revision.page_id)
        revision_list = self.db(query).select(self.db.revision.rev_idx)
        if revision_list == None or len(revision_list) == 0:
            return None
        return revision_list[0]["rev_idx"]

    """Writes to the store.
    :param page_id: id of page (or in general, of compression space)
    :param version_id: id of the version we are writing.
    :param rev_id: id of revision (or in general, of object in space)
    :return: Whether the given page/revision/version combo exists in the Storage table
                (meaning it is in a blob in a gcsbucket)
    """

    @autocommit
    def insert_blob_name(
        self, rev_id: int, page_id: int, version_id: int, blob_name: str,
        text_type: str
    ):
        self.storage_table.update_or_insert(
            rev_id=rev_id,
            version=version_id,
            page_id=page_id,
            blob=blob_name,
            text_type=text_type
        )

    @autocommit
    def set_rev_idx(self, page_id: int, rev_formated_dict_arry):
        print("TODO: Implement set_rev_idx")
        # I don't think this function was ever used

    """
    DEBUG Function to print the whole storage table
    """

    def print_storage_table(self):
        # Returns
        blob_list = self.db().select(self.storage_table.ALL)
        if blob_list == None or len(blob_list) == 0:
            return print("storage table empty")
        print(blob_list)