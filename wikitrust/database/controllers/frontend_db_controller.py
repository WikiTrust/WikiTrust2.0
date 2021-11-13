from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date
from wikitrust.database.controllers.create_entry import create_entry as create
import wikitrust.database.db_schema as db_schema
from wikitrust.database.controllers.db_wrappers import autocommit
import logging


class frontend_db_controller:
    def __init__(self, db):
        self.db = db

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
    #return the revision id of the most recent revision of the page
    def get_most_recent_rev_id(self, page_id):
        x = self.db.revision.page_id == page_id
        return self.db(x).select(self.db.revision.rev_id).last().rev_id

    # returns an iterator for going through all pages currently in the database
    def get_all_pages(self):
        return self.db(self.db.page).iterselect(self.db.page.ALL)

    def get_environment(self, environment_id):
        return self.db(environment_id).select(
            self.db.environment.environment_name
        ).first().environment_name

    #parameters: revision_id
    #return boolean corresponding to if the text was retirieved (column text_retrieved)
    # Note: The revision puller sets text_retrieved before the text is downloaded, this is incorrect behavior!!
    def check_text_retrieved(self, rev_id):
        x = self.db.revision.rev_id == rev_id
        ret = self.db(x).select(self.db.revision.text_retrieved
                               ).first().text_retrieved
        return ret

    #parameters: page_id
    #return: environment
    def get_environment_by_page_id(self, page_id):
        x = self.db.page.page_id == page_id
        return self.db(x).select(self.db.page.environment_id
                                ).first().environment_id

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
        user_rep = self.db(x & y & z).select(
            self.db.user_reputation.reputation_value
        )
        if (len(user_rep) > 1):
            logging.error(
                "MORE THAN ONE USER FOUND WHEN USING get_reputation in frontend_db_controller"
            )
        if (user_rep.first() == None):
            self.create.create_user_reputation(version, user_id, env)
            return 0
        user_rep = user_rep.first().reputation_value
        return user_rep