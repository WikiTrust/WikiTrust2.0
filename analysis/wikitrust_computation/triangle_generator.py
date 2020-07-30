import math
import json
import datetime

from pydal.migrator import InDBMigrator
from pydal import DAL, Field

#Algorithm Constants
__ALGORITHM_VER__ = "TRIANGLE_GENERATOR_DEV"
__MAX_JUDGE_DIST__ = 10
__SCALING_CONST__ = 1
__SCALING_FUNC__ = lambda x : math.log(x)

#Temporarily bootstrapping off old OOP Code, pending non OOP rewrite
from wikitrust_algorithms.author_reputation.article import Article
from wikitrust_algorithms.author_reputation.version import Version
EDIT_DISTANCE_CALCULATOR = Article(__MAX_JUDGE_DIST__, __SCALING_CONST__, __SCALING_FUNC__)

def compute_triangles_batch(page_id, db_uri):
    db = DAL(db_uri)
    page_revs = db(db.revision.page_id == page_id).iterselect(orderby=db.revision.page_id)

    # Rolls over current revision into reference revision, initialized to none
    reference_revision_text = None
    reference_revision_author = None

    for rev_num in range(len(page_revs)):
        # If this is the first revision, there is no reference revision so we cannot judge it.
        # We will however, populate reference_revision_text
        if rev_num == 0:
            #Checks that we have access to the reference text, add advanced error handling later
            assert(page_revs[rev_num-1].text_retrieved == True)
            #Populates reference_revision_text with current text for use in next iteration
            reference_revision_id = page_revs[rev_num].revision_id
            reference_revision_blob = page_revs[rev_num].revision_blob
            reference_revision_text = None #TBD Revision storage engine
            reference_revision_author = page_revs[rev_num].user_id

        #Checks that we have access to the reference judged text, add advanced error handling later
        assert(page_revs[rev_num].text_retrieved == True)

        #Get revision text for current (judged) revision
        judged_revision_id = page_revs[rev_num].revision_id
        judged_revision_blob = page_revs[rev_num].revision_blob
        judged_revision_text = None #TBD Revision storage engine
        judged_revision_author = page_revs[rev_num].user_id

        #Computes edit distance between reference and current once
        reference_current_distance = compute_edit_distance(reference_revision_text, judged_revision_text)

        for new_rev_num in range(rev_num + 1, rev_num + __MAX_JUDGE_DIST__):
            #Get revision text for new revision
            new_revision_id = page_revs[new_rev_num].revision_id
            new_revision_blob = page_revs[new_rev_num].revision_blob
            new_revision_text = None #TBD Revision storage engine
            new_revision_author = page_revs[new_rev_num].user_id

            reference_new_distance = compute_edit_distance(reference_revision_text, new_revision_text)
            current_new_distance = compute_edit_distance(judged_revision_text, new_revision_text)

            triangle_dict = {"revisions": [reference_revision_id, judged_revision_id, new_revision_id], \
                             "distances": [reference_current_distance, reference_new_distance, current_new_distance], \
                             "authors":   [reference_revision_author, judged_revision_author, new_revision_author]}

            triangle_json = json.dumps(triangle_dict)

            db.triangles.update_or_insert((db.triangles.page == page_id) & 
                                          (db.triangles.algorithm == __ALGORITHM_VER__) &
                                          (db.triangles.judged_revision == judged_revision_id) &
                                          (db.triangles.new_revision == new_revision_id),
                                         page = page_id,
                                         algorithm = __ALGORITHM_VER__,
                                         info = str(triangle_json),
                                         judged_revision= judged_revision_id,
                                         new_revision= new_revision_id,
                                         reputation_inc = None)

        db.revision_log.update_or_insert((db.revision_log.page == page_id) &
                                         (db.revision_log.algorithm == __ALGORITHM_VER__),
                                          page = page_id,
                                          algorithm = __ALGORITHM_VER__,
                                          last_revision = judged_revision_id,
                                          lock_date = datetime.date.today()
                                          )

        #Rolls over current revision variables into reference revision variables
        reference_revision_id = judged_revision_id
        reference_revision_text = judged_revision_text
        reference_revision_author = judged_revision_author


def compute_triangles_keepup():
    pass

def compute_edit_distance(rev_1_text, rev_2_text):
    #Temporarily bootstrapping off old OOP Code, pending non OOP rewrite
    version_1 = Version("author1", rev_1_text)
    version_2 = Version("author2", rev_2_text)
    return EDIT_DISTANCE_CALCULATOR.compute_edit_distance(version_1, version_2)
