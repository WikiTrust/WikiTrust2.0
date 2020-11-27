from pydal import DAL, Field

from datetime import date
from wikitrust.database.controllers.db_wrappers import autocommit
"""
All functions in this file follow the same format.
Each function creates a new entry in the database
@param db: The Database pointer
@param param#: All variables to be put into the created object in the database
@return: returns the object that was inserted into the database
"""
class create_entry:
    def __init__(self, db):
        self.db = db

    @autocommit
    def create_environment(
        self, 
        environment_name = ''
    ):
        try:
            env = self.db.environment.insert(environment_name = environment_name)
            return env
        except:
            self.db.rollback()
            return self.db(self.db.environment.environment_name == environment_name).select(self.db.environment.id).first()

    @autocommit
    def create_page(
        self, 
        page_id=-1, 
        environment_id = None, 
        page_title = "", 
        last_check_time = None
    ):
        try:
            ret = self.db.page.insert(page_id = page_id, environment_id = environment_id, page_title = page_title, last_check_time = last_check_time)
            return ret
        except:
            self.db.rollback()
            return self.db(self.db.page.page_id == page_id).select(self.db.page.id).first()
    @autocommit
    def create_user(
        self, 
        user_id=-1, 
        user_name=''
    ):
        try:
            ret = self.db.user.insert(user_id = user_id, user_name = user_name)
            return ret
        except:
            self.db.rollback()
            return self.db(self.db.user.user_id == user_id).select(self.db.user.id).first()


    @autocommit
    def create_revision(
        self, 
        rev_id = -1, 
        page_id = -1, 
        user_id = -1, 
        rev_date = None, 
        prev_rev = -1, 
        text_retrieved = 'F', 
        last_attempt_date = None, 
        num_attempts = -1,
    ):
        try:
            ret = self.db.revision.insert(rev_id = rev_id, page_id = page_id, user_id = user_id, rev_date = rev_date, prev_rev = prev_rev, text_retrieved = text_retrieved, last_attempt_date = last_attempt_date, num_attempts = num_attempts)
            return ret
        except:
            self.db.rollback()
            return self.db(self.db.revision.rev_id == rev_id).select(self.db.revision.id).first()

    @autocommit
    def create_revision_log(
        self, 
        version = '', 
        stage = '', 
        page_id = -1, 
        last_rev = None, 
        lock_date = None
    ):
        x = self.db.revision_log.version == version
        y = self.db.revision_log.page_id == page_id
        q = self.db(x & y).select().first()
        if(q == None):
            ret = self.db.revision_log.insert(version = version, stage = stage, page_id = page_id, last_rev = last_rev, lock_date = lock_date)
            return ret
        return q

    @autocommit
    def create_user_reputation(
        self, 
        version = '', 
        user_id = -1, 
        environment = None, 
        reputation_value = 0
    ):
        x = self.db.user_reputation.version == version
        y = self.db.user_reputation.user_id == user_id
        z = self.db.user_reputation.environment == environment
        q = self.db(x & y & z).select().first()
        if(q == None):
            ret = self.db.user_reputation.insert(version = version, user_id = user_id, environment = environment, reputation_value = reputation_value)
            return ret
        return q

    @autocommit
    def create_text_storage(
        self, 
        version = '', 
        page_id = -1,
        rev_id = -1,
        text_type = '',
        blob = ''
    ):
        ret = self.db.text_storage.insert(version = version, page_id = page_id, rev_id = rev_id, text_type = text_type, blob = blob)
        return ret

    @autocommit
    def create_triangles(
        self,
        version = '',
        page_id = -1,
        rev_id_1 = -1,
        rev_id_2 = -1,
        rev_id_3 = -1,
        reputation_inc = None
    ):
        ret = self.db.triangles.insert(version = version, page_id = page_id, rev_id_1 = rev_id_1, rev_id_2 = rev_id_2, rev_id_3 = rev_id_3, reputation_inc = reputation_inc)
        return ret

    @autocommit
    def create_text_diff(
        self,
        version = '',
        rev_id_1 = -1,
        rev_id_2 = -1,
        info = ''
    ):
        ret = self.db.text_diff.insert(version = version, rev_id_1 = rev_id_1, rev_id_2 = rev_id_2, info=info)
        return ret

    @autocommit
    def create_text_distance(
        self, 
        version = '',
        rev_id_1 = -1,
        rev_id_2 = -1,
        distance = 0.0
    ):
        x = self.db.text_distance.version == version
        y = self.db.text_distance.rev_id_1 == rev_id_1
        z = self.db.text_distance.rev_id_2 == rev_id_2
        q = self.db(x & y & z).select().first()
        if(q == None):
            ret = self.db.text_distance.insert(version = version, rev_id_1 = rev_id_1, rev_id_2 = rev_id_2, distance = distance)
            return ret
        return q
        
