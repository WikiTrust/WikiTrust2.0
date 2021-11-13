from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date
from wikitrust.database.controllers.create_entry import create_entry
import wikitrust.database.db_schema as db_schema
from wikitrust.database.controllers.db_wrappers import autocommit
import logging


class computation_engine_db_controller:
    def __init__(self,  db):
        self.db = db
        self.create_entry = create_entry(self.db)

    def populate_prev_rev(self, page_id):
        all_revs = self.db(self.db.revision.page_id == page_id).iterselect(orderby=self.db.revision.rev_id)
        prev2 = None
        for i,rev in enumerate(all_revs):
            prev = rev
            rev.rev_idx = i
            if(prev2):
                rev.prev_rev = prev2.rev_id
                prev2.next_rev = rev.rev_id
                prev2.update_record()
            rev.update_record()
            self.db.commit()
            prev2 = prev

        print("Previous Revision Field Populated")

    #parameters: rev_id
    #return previous revision id
    def get_prev_rev(self, rev_id):
        rev = self.db(self.db.revision.rev_id == rev_id).select().first()
        return rev.prev_rev

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
            self.create_page_entry.create_user_reputation(version, user_id, env)
            return 0
        user_rep = user_rep.first().reputation_value
        return user_rep

    #parameters: version, user_id, env, reputation
    #return user id
    def set_reputation(self, version, user_id, env, rep):
        x = self.db.user_reputation.version == version
        y = self.db.user_reputation.user_id == user_id
        z = self.db.user_reputation.environment == env
        user_rep = self.db(x & y & z).select().first()
        user_rep.reputation_value = rep
        user_rep.update_record()
        self.db.commit()
        return user_rep.user_id

    #return unique id
    #update text Distances 1 - 2, 2 - 3, 1 - 3
    def create_triangle(self, version, page_id, revs, distances, rep = None):
        v = self.db.triangles.version == version
        w = self.db.triangles.page_id == page_id
        x = self.db.triangles.rev_id_1 == revs[0]
        y = self.db.triangles.rev_id_2 == revs[1]
        z = self.db.triangles.rev_id_3 == revs[2]
        ret = triangle = self.db(v & w & x & y & z).select().first()
        if(triangle == None):
            ret = self.create_page_entry.create_triangles(
                version, page_id, revs[0], revs[1], revs[2], rep
            ).id
        else:
            ret = ret.id
            triangle.reputation_inc = rep
            triangle.update_record()
            self.db.commit()
        #rev 1 to rev 2 distance
        self.create_page_entry.create_text_distance(
            version, revs[0], revs[1], distances[0]
        )
        #rev 2 to rev 3 distance
        self.create_page_entry.create_text_distance(
            version, revs[1], revs[2], distances[1]
        )
        #rev 1 to rev 3 distance
        self.create_page_entry.create_text_distance(
            version, revs[0], revs[2], distances[2]
        )
        return ret

    #parameters: triangle.id, reputation
    #return: triangle.id
    def update_triangle_rep(self, id, rep):
        triangle = self.db(self.db.triangles.id == id).select().first()
        triangle.reputation_inc = rep
        triangle.update_record()
        self.db.commit()
        return id

    #parameters: version, page_id
    #return all triangle id's (in chronological order by rev_id_2)
    def get_all_triangles_chronological(self, version, page_id):
        x = self.db.triangles.page_id == page_id
        y = self.db.triangles.version == version
        all_triangles = self.db(x & y).iterselect(orderby=self.db.triangles.rev_id_2)
        all_triangle_ids = []
        for row in all_triangles:
            all_triangle_ids.append(row.id)
        return all_triangle_ids

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

    #parameters: version, stage, page_id, revision
    #return
    def update_revision_log(self, version, stage, page_id, rev):
        x = self.db.revision_log.version == version
        y = self.db.revision_log.page_id == page_id
        rev_log = self.db(x & y).select().first()
        if(rev_log == None):
            rev_log = self.create_page_entry.create_revision_log(
                version, stage, page_id, rev, date.today()
            )
        else:
            rev_log.stage = stage
            rev_log.last_rev = rev
            rev_log.lock_date = date.today()
            rev_log.update_record()
            self.db.commit()
        return rev_log.id

    #parameters: version, page_id
    #return: all unprocessed triangles, in chronological order, by third revision, for a given page
    #return only triangle unique ids
    def get_all_unprocessed_triangles(self, version):
        x = self.db.triangles.version == version
        y = self.db.triangles.reputation_inc == None
        unprocessed_triangles = self.db(x & y).iterselect(orderby=self.db.triangles.rev_id_2)
        rows = list(unprocessed_triangles)
        unprocessed_triangle_ids = []
        for row in rows:
            unprocessed_triangle_ids.append(row.id)
        return unprocessed_triangle_ids

    #parameters: page_id
    #return: environment
    def get_environment_by_page_id(self, page_id):
        x = self.db.page.page_id == page_id
        return self.db(x).select(self.db.page.environment_id).first().environment_id

    #parameters: eviroment_name
    #return: environment
    def get_environment_by_name(self, eviroment_name):
        x = self.db.environments.page_id == page_id
        return self.db(x).select(self.db.page.environment_id).first().environment_id

    #parameters: triangle.id
    #return: 3 tuples with three tuples inside
    # (rev1,rev2,rev3),(user_id1,...,...),(distance 1-2, distance 2-3, distance 1-3)
    def get_triangle_info(self, id):
        triangle = self.db(self.db.triangles.id == id).select().first()
        rev_tuple = (triangle.rev_id_1,triangle.rev_id_2,triangle.rev_id_3)

        user_1 = self.db(self.db.revision.rev_id == rev_tuple[0]).select(self.db.revision.user_id).first().user_id
        user_2 = self.db(self.db.revision.rev_id == rev_tuple[1]).select(self.db.revision.user_id).first().user_id
        user_3 = self.db(self.db.revision.rev_id == rev_tuple[2]).select(self.db.revision.user_id).first().user_id
        user_tuple = (user_1,user_2,user_3)

        distance_1_q_1 = self.db.text_distance.rev_id_1 == rev_tuple[0]
        distance_1_q_2 = self.db.text_distance.rev_id_2 == rev_tuple[1]

        distance_2_q_1 = self.db.text_distance.rev_id_1 == rev_tuple[1]
        distance_2_q_2 = self.db.text_distance.rev_id_2 == rev_tuple[2]

        distance_3_q_1 = self.db.text_distance.rev_id_1 == rev_tuple[0]
        distance_3_q_2 = self.db.text_distance.rev_id_2 == rev_tuple[2]

        distance_1 = self.db(distance_1_q_1 & distance_1_q_2).select(self.db.text_distance.distance).first().distance
        distance_2 = self.db(distance_2_q_1 & distance_2_q_2).select(self.db.text_distance.distance).first().distance
        distance_3 = self.db(distance_3_q_1 & distance_3_q_2).select(self.db.text_distance.distance).first().distance
        distance_tuple = (distance_1, distance_2, distance_3)

        info = (rev_tuple, user_tuple, distance_tuple)
        return info

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