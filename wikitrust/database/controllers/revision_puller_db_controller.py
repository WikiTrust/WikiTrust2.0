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
        for i, rev_object in enumerate(rev_formated_dict_arry):
            # x = self.db.revision.page_id == page_id
            # y = self.db.revision.rev_id == rev_id
            # revision_row = self.db(x & y).select().first()
            # revision_row.index = rep
            # revision_row.update_record()
            # rev_formated_dict_arry
            self.db.revison.insert()
