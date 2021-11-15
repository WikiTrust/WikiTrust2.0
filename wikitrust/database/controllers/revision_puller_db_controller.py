from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date
import wikitrust.database.db_schema as db_schema
from wikitrust.database.controllers.db_wrappers import autocommit
import logging


class revsion_puller_db_controller:
    def __init__(self, db):
        self.db = db
        self.revision_table = self.db.revision

    @autocommit
    def insert_revisions(self, rev_formated_dict_arry):
        # this says unique contstraint failed if it's run twice because the rows are already in the table (delete table and re-try to fix)
        # self.revision_table.bulk_insert(rev_formated_dict_arry)
        for rev_object in rev_formated_dict_arry:
            print(rev_object)
            x = self.db.revision.page_id == rev_object["page_id"]
            y = self.db.revision.rev_id == rev_object["rev_id"]
            self.db.revision.update_or_insert(x & y, **rev_object)
            # revision_row = self.db(x & y).select().first()
            # revision_row.index = rep
            # revision_row.update_record()
            # rev_formated_dict_arry
            # self.db.revision.insert()

    """
    DEBUG Function to print the whole revision table
    """
    def print_revision_table(self):
        # Returns
        blob_list = self.db().select(self.revision_table.ALL)
        if blob_list == None or len(blob_list) == 0:
            return print("rev table empty")
        print(blob_list)