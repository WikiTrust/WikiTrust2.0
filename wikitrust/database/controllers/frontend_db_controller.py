from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date
from wikitrust.database.controllers.create_entry import create_entry  as create
import wikitrust.database.db_schema as db_schema
from wikitrust.database.controllers.db_wrappers import autocommit
import logging

class frontend_db_controller:
    def __init__(self, uri = 'sqlite://storage.sqlite'):
        self.db = db_schema.connect_to_db(uri)

    #parameters: rev_id
    #return previous revision id
    def get_prev_rev(self, rev_id):
        rev = self.db(self.db.revision.rev_id == rev_id).select().first()
        return rev.prev_rev

    #parameters: rev_id
    #return next revision id
    def get_next_rev(self, rev_id):
        rev = self.db(self.db.revision.rev_id == rev_id).select().first()
        print(rev)
        return rev.next_rev


    #parameters: page_id
    #return all revision ids
    def get_all_revisions(self, page_id):
        x = self.db.revision.page_id == page_id
        all_revs = list(self.db(x).iterselect(orderby=self.db.revision.rev_id))
        all_revs_list = []
        for row in all_revs:
            all_revs_list.append(row.rev_id)
        return all_revs_list

    #parameters: revision_id
    #return boolean corresponding to text_retrieved
    def check_text_retrieved(self, rev_id):
        x = self.db.revision.rev_id == rev_id
        ret = self.db(x).select(self.db.revision.text_retrieved).first().text_retrieved
        return ret

    #parameters: page_id
    #return: environment
    def get_environment_by_page_id(self, page_id):
        x = self.db.page.page_id == page_id
        return self.db(x).select(self.db.page.environment_id).first().environment_id

    #parameters: rev_id
    #return: page_id
    def get_page_from_rev(self, rev_id):
        x = self.db.revision.rev_id == rev_id
        return self.db(x).select(self.db.revision.page_id).first().page_id

    #parameters: rev_id
    #return: user_id
    def get_user_from_rev(self, rev_id):
        x = self.db.revision.rev_id == rev_id
        return self.db(x).select(self.db.revision.user_id).first().user_id

    #parameters: version, user_id, environment
    #exceptions: crash if get_reputation finds more than 1
    #return reputation of user
    def get_reputation(self, version, user_id, env):
        x = self.db.user_reputation.version == version
        y = self.db.user_reputation.user_id == user_id
        z = self.db.user_reputation.environment == env
        user_rep = self.db(x & y & z).select(self.db.user_reputation.reputation_value)
        if(len(user_rep) > 1):
            logging.error("MORE THAN ONE USER FOUND WHEN USING get_reputation")
        if(user_rep.first()==None):
            self.create.create_user_reputation(version, user_id, env)
            return 0
        user_rep = user_rep.first().reputation_value
        return user_rep