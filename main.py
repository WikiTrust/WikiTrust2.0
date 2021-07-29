from datetime import datetime
import os
import json

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
# for viz server
from wikitrust.database.controllers.frontend_db_controller import frontend_db_controller
import wikitrust.test.text_trust_vizualizer.text_trust_vis_server as trust_viz

__DBURI__ = "sqlite://storage.sqlite"

if __name__ == '__main__':

    # Connect to database and initilize controllers:
    db = db_schema.connect_to_db(__DBURI__)
    storage_db_ctrl = storage_engine_db_controller(db)
    compute_db_ctrl = computation_engine_db_controller(db)
    rev_puller_db_ctrl = revsion_puller_db_controller(db)
    frontend_db_ctrl = frontend_db_controller(
        db)







    # Initilize revision pulller tools:
    wikiSearchEngine = WikiSearchEngine.SearchEngine()
    wikiPageProcessor = WikiPageProcessor.PageProcessor()

    # find a page:
    current_PyWiki_Page = wikiSearchEngine.search(
        "Dog", max_pages_grabbed=1, search_by="nearmatch"
    )[0]
    current_page_id = current_PyWiki_Page.pageid

    # get all revisions for that page
    all_revisions = WikiRevPuller.get_all_revisions(
        current_PyWiki_Page, recent_to_oldest=False
    )

    # convert revisions to the revision table db schema and load them into the db:
    rev_table_row_dicts = tranform_pywikibot_revision_list_into_rev_table_schema_dicts(all_revisions,current_page_id)
    rev_puller_db_ctrl.insert_revisions(rev_table_row_dicts)
    # rev_puller_db_ctrl.print_revision_table()

    all_revisions_text = []

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
                rev_text = wikiPageProcessor.getReadableText(WikiRevPuller.get_text_of_old_revision(current_PyWiki_Page, rev_id))
                all_revisions_text.append(rev_text)
                revStore.store(page_id=current_page_id, rev_id=rev_id, text=rev_text,timestamp=datetime.now())
                texttrusts = []
                for word in rev_text.split():
                    texttrusts.append(len(word))
                textTrustStore.store(page_id=current_page_id, rev_id=rev_id, text=json.dumps(texttrusts),timestamp=datetime.now())
    storage_db_ctrl.print_storage_table()

    db_test.drop_and_populate(compute_db_ctrl)
    ce_test.test_computation_engine(
        compute_db_ctrl, storage_db_ctrl, frontend_db_ctrl
    )

    storage_fill.fill_storage_engine(storage_db_ctrl)
    storage_test.test_storage_engine(storage_db_ctrl)

    print(db)
    print(db.text_storage)

    trust_viz.text_trust_visualization_server(storage_db_ctrl).run()
