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
    
    #parameters: parameters rev_id
    #return previous revision id
    def get_prev_rev(self, rev_id):
        return 0

    #parameters: version, user_id, environment
    #return reputation of user
    def get_reputation(self, version, user_id, env):
        return 0.0

    #parameters: version, page_id
    #return all triangles in chronological order
    def get_all_triangles_chronological(self, version, page_id):
        return 0

    #paramters: id, reputation
    #return nothing
    def update_triangle(self, id, reputation):
        return 0
    
    #parameters: page_id
    #return all revisions and if the text has been retrieved
    def get_all_revisions(self, page_id):
        return 0
    
    #parameters: version, stage, page_id, revision
    #return 
    def update_revision_log(self, version, stage, page_id, revision):
        return 0
