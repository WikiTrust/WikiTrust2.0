from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date
from wikitrust.database.controllers.create_entry import create_entry  as create
from wikitrust.database.controllers.db_wrappers import autocommit

class computation_engine_db_controller: 
    def __init__(self, db_, create_ = None):
        self.db = db_
        if(create == None):
            self.create = create_.create_entry(db_)
        else:
            self.create = create_

    def populate_prev_rev(self, page_id):
        all_revs = self.db(self.db.revision.page_id == page_id).iterselect(orderby=self.db.revision.rev_id)
        prev2 = None
        for rev in all_revs:
            prev = rev
            rev.prev_rev = prev2
            rev.update_record()
            self.db.commit()
            prev2 = prev.rev_id
        print("Previous Revision Field Populated")
    
    #parameters: rev_id
    #return previous revision id
    def get_prev_rev(self, rev_id):
        rev = self.db(self.db.revision.rev_id == rev_id).select().first()
        return rev.prev_rev

    #parameters: version, user_id, environment
    #return reputation of user
    def get_reputation(self, version, user_id, env):
        x = self.db.user_reputation.version == version
        y = self.db.user_reputation.user_id == user_id
        z = self.db.user_reputation.environment == env
        user_rep = self.db(x & y & z).select().first()
        return user_rep.reputation_value

    def update_or_insert_triangle(self, version, page_id, rev_1, rev_2, rev_3, rep = 0):
        v = self.db.triangles.version == version
        w = self.db.triangles.page_id == page_id
        x = self.db.triangles.rev_id_1 == rev_1
        y = self.db.triangles.rev_id_2 == rev_2
        z = self.db.triangles.rev_id_3 == rev_3
        triangle = self.db(v & w & x & y & z).select().first()
        if(triangle == None):
            self.create.create_triangles(version, page_id, rev_1, rev_2, rev_3, rep)
        else:
            triangle.reputation_inc = rep
            triangle.update_record()
            self.db.commit()

    #parameters: version, page_id
    #return all triangles in chronological order
    def get_all_triangles_chronological(self, version, page_id):
        x = self.db.triangles.page_id == page_id
        y = self.db.triangles.version == version
        all_triangles = self.db(x & y).iterselect(orderby=self.db.triangles.rev_id_2)
        return all_triangles
    
    #parameters: page_id
    #return all revisions and if the text has been retrieved
    def get_all_revisions(self, page_id):
        x = self.db.revision.page_id == page_id
        all_revs = self.db(x).select(self.db.revision.rev_id, self.db.revision.text_retrieved).iterselect(orderby=self.db.revision.self.db.revision.rev_id)
        return all_revs
    
    #parameters: version, stage, page_id, revision
    #return 
    def update_revision_log(self, version, stage, page_id, rev):
        x = self.db.revision_log.version == version
        y = self.db.revision_log.page_id == page_id
        rev_log = self.db(x & y).select().first()
        if(rev_log == None):
            rev_log = self.create.create_revision_log(version, stage, page_id, rev, date.today())
        else: 
            rev_log.stage = stage
            rev_log.last_rev = rev
            rev_log.lock_date = date.today()
            rev_log.update_record()
            self.db.commit()
        return rev_log

    #parameters: version, page_id
    #return: all unprocessed triangles, in chronological order, by third revision, for a given page
    def get_all_unprocessed_triangles(self, version):
        x = self.db.triangles.version == version
        y = self.db.triangles.reputation_inc == None
        unprocessed_triangles = self.db(x & y).iterselect(orderby=self.db.triangles.rev_id_2)
        return unprocessed_triangles