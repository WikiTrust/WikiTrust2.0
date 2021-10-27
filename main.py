from datetime import datetime
import os
import json
import math
import datetime
from datetime import datetime

# for database
from wikitrust.database import db_schema
import wikitrust.test.db_test as db_test
# for testing?
import wikitrust.test.computation_engine_debug as ce_test
import wikitrust.test.storage_engine_debug as storage_test
import wikitrust.test.fill_storage_engine as storage_fill
# For revision puller
from wikitrust.database.controllers.revision_puller_db_controller import revsion_puller_db_controller
from wikitrust.revision_puller.RevisionsWrapper import convert_rev_to_table_row, get_rev_id, tranform_pywikibot_revision_list_into_rev_table_schema_dicts
import wikitrust.revision_puller.SearchEngine as WikiSearchEngine
import wikitrust.revision_puller.RevisionPuller as WikiRevPuller
import wikitrust.revision_puller.PageProcessor as WikiPageProcessor
# For storage engine
from wikitrust.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust.storage_engine.storage_engine import RevisionStorageEngine
from wikitrust.storage_engine.storage_engine import TextTrustStorageEngine
# for computation engine
from wikitrust.database.controllers.computation_engine_db_controller import computation_engine_db_controller
from wikitrust.computation_engine.triangle_generator import TriangleGenerator
from wikitrust.computation_engine.reputation_generator import ReputationGenerator
from wikitrust.computation_engine.text_annotation import TextAnnotation
import wikitrust.computation_engine.wikitrust_algorithms.text_diff.chdiff as chdiff

# for viz server
from wikitrust.database.controllers.frontend_db_controller import frontend_db_controller
import wikitrust.test.text_trust_vizualizer.text_trust_vis_server as trust_viz

__DBURI__ = "sqlite://storage.sqlite"
__ALGORITHM_VER__ = 1

if __name__ == '__main__':
    print(
        "Starting..........................................................................................................."
    )
    # Connect to database and initilize controllers:
    db = db_schema.connect_to_db(__DBURI__)
    storage_db_ctrl = storage_engine_db_controller(db)
    compute_db_ctrl = computation_engine_db_controller(db)
    rev_puller_db_ctrl = revsion_puller_db_controller(db)
    frontend_db_ctrl = frontend_db_controller(db)

    # Initilize revision pulller tools:
    wikiSearchEngine = WikiSearchEngine.SearchEngine()
    wikiPageProcessor = WikiPageProcessor.PageProcessor()

    # find a page:
    current_PyWiki_Page = wikiSearchEngine.search(
        "Walter Goad", max_pages_grabbed=1, search_by="nearmatch"
    )[0]
    #  #wikiSearchEngine.getByPageID()
    current_page_id = current_PyWiki_Page.pageid
    print("current_page_id:", current_page_id)

    # get all revisions for that page
    all_revisions = WikiRevPuller.get_all_revisions(
        current_PyWiki_Page, recent_to_oldest=False
    )

    # convert revisions to the revision table db schema and load them into the db:
    rev_table_row_dicts = tranform_pywikibot_revision_list_into_rev_table_schema_dicts(
        all_revisions, current_page_id
    )
    rev_puller_db_ctrl.insert_revisions(rev_table_row_dicts)
    # rev_puller_db_ctrl.print_revision_table()

    all_revisions_text = []

    # Populate the tables neccesary for the compute engine to process this page
    create = compute_db_ctrl.create
    compute_db_env = create.create_environment('kyle_test_category')
    create.create_page(
        page_id=current_page_id,
        environment_id=compute_db_env,
        page_title=current_PyWiki_Page.title,
        last_check_time=None
    )
    create.create_revision_log(__ALGORITHM_VER__, None, page_id=current_page_id)

    # page_id = dogPage.pageid
    with RevisionStorageEngine(
        bucket_name='wikitrust-testing',
        storage_db_ctrl=storage_db_ctrl,
        version=1
    ) as revStore:
        with TextTrustStorageEngine(
            bucket_name='wikitrust-testing',
            storage_db_ctrl=storage_db_ctrl,
            version=1
        ) as textTrustStore:
            for revision in all_revisions:
                rev_id = WikiRevPuller.getRevisionMetadata(revision, "revid")
                rev_user_id = WikiRevPuller.getRevisionMetadata(
                    revision, "userid"
                )
                rev_text = wikiPageProcessor.getReadableText(
                    WikiRevPuller.get_text_of_old_revision(
                        current_PyWiki_Page, rev_id
                    )
                )

                #convert text to a json encoded array of words (by splitting revison text on whitespace)
                rev_text = json.dumps(rev_text.split())

                # store the cleaned word array in all_revisions_text array and in the storage engine (meaning: google clound sstorage in bundles)
                all_revisions_text.append(rev_text)
                revStore.store(
                    page_id=current_page_id,
                    rev_id=rev_id,
                    text=rev_text,
                    timestamp=datetime.now()
                )

                # now append revision metadata to the computation relevant tables?
                create.create_revision(rev_id, current_page_id, rev_user_id)
                create.create_user(rev_user_id)
                create.create_user_reputation(
                    __ALGORITHM_VER__, rev_user_id, compute_db_env
                )

                # fake text trusts array and store in texttrusts var and in the storage engine (meaning: google clound sstorage in bundles)
                # texttrusts = []
                # for word in rev_text.split():
                #     texttrusts.append(len(word))
                # textTrustStore.store(page_id=current_page_id, rev_id=rev_id, text=json.dumps(texttrusts),timestamp=datetime.now())
                #Run Triangle generator

            print("Starting Triangle Generator...")
            tg = TriangleGenerator(
                compute_db_ctrl, revStore, __ALGORITHM_VER__,
                (3, chdiff.edit_diff_greedy, chdiff.make_index2)
            )
            tg.compute_triangles_batch(current_page_id)
            print("Triangle Generator done\n")

            #Run Reputation generator
            print("Starting Reputation Generator...")
            rg = ReputationGenerator(
                compute_db_ctrl, __ALGORITHM_VER__,
                (0.5, (lambda x: math.log(1.1 + x)))
            )
            rg.update_author_reputation()
            print("Reputation Generator done\n")

            #Run Text Annotation on each revision
            print("Running Text Annotation...")
            ta = TextAnnotation(
                compute_db_ctrl, revStore, textTrustStore, __ALGORITHM_VER__,
                (0.5, 0.5, 5, chdiff.edit_diff_greedy, chdiff.make_index2)
            )
            for revision in all_revisions:  # this all_revisions list must be sorted. (from oldest to newest.?)
                ta.compute_revision_trust(revision.revid)

            print("Text Annotation done \n")

            print("flushing storage engines....")
            textTrustStore.flush()
            revStore.flush()

    storage_db_ctrl.print_storage_table()

    revision_list = frontend_db_ctrl.get_all_revisions(current_page_id)
    print("Revision Engine and Text Reputation Engine Populated")

    print("Page Id: ", current_page_id, "rev", revision_list[0])

    trust_viz.text_trust_visualization_server(storage_db_ctrl,frontend_db_ctrl).run()
