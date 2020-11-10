from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date

class computation_engine_db_controller: 
    def __init__(self, db):
        self.db = db

    def populate_prev_rev(self, page_id):
        all_revs = self.db(self.db.revision.page_id == page_id).iterselect(orderby=self.db.revision.rev_id)
        x=0
        prev2 = None
        for rev in all_revs:
            prev = rev
            rev.prev_rev = prev2
            rev.update_record()
            self.db.commit()
            prev2 = prev.rev_id
            print(str(rev.rev_id) + " : " + str(prev2))
            x+=1
        print(x)
        