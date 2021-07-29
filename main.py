import os
import json
from wikitrust.revision_puller.RevisionsWrapper import convert_rev_to_table_row, get_rev_id

# for database
from wikitrust.database import db_schema
import wikitrust.test.db_test as db_test

import wikitrust.test.computation_engine_debug as ce_test
import wikitrust.test.storage_engine_debug as storage_test
import wikitrust.test.fill_storage_engine as storage_fill
# For revision puller
from wikitrust.database.controllers.revision_puller_db_controller import revsion_puller_db_controller
import wikitrust.revision_puller.SearchEngine as SE
import wikitrust.revision_puller.RevisionPuller as RP
import wikitrust.revision_puller.PageProcessor as PP
# For storage engine
from wikitrust.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust.storage_engine.storage_engine import StorageEngine
from wikitrust.storage_engine.storage_engine import RevisionEngine
from wikitrust.storage_engine.storage_engine import TextReputationEngine
# for computation engine
from wikitrust.database.controllers.computation_engine_db_controller import computation_engine_db_controller
# for viz server
from wikitrust.database.controllers.frontend_db_controller import frontend_db_controller
import wikitrust.test.text_trust_vizualizer.text_trust_vis_server as trust_viz

__DBURI__ = "sqlite://storage.sqlite"

if __name__ == '__main__':
    db = db_schema.connect_to_db(__DBURI__)
    storage_db_ctrl = storage_engine_db_controller(db)
    compute_db_ctrl = computation_engine_db_controller(db)
    rev_puller_db_ctrl = revsion_puller_db_controller(db)
    frontend_db_ctrl = frontend_db_controller(db)

    # revision puller stuff
    engine = SE.SearchEngine()
    processor = PP.PageProcessor()

    # find a page
    dogPage = engine.search("Dog", max_pages_grabbed=1,
                            search_by="nearmatch")[0]
    print(dogPage)

    #get all revisions for that page
    all_revisions = RP.get_all_revisions(dogPage, recent_to_oldest=False)
    rev_count = len(all_revisions)
    rev_table_rows = []
    for i, rev_object in enumerate(all_revisions):
        prev_id = get_rev_id(all_revisions[i - 1]) if i > 0 else None
        next_id = get_rev_id(
            all_revisions[i + 1]
        ) if i < rev_count - 1 else None
        rev_table_row = convert_rev_to_table_row(
            rev_object, dogPage, i, prev_id, next_id
        )
        rev_table_rows.append(rev_table_row)

    rev_puller_db_ctrl.insert_revisions(rev_table_rows)
    rev_puller_db_ctrl.print_revision_table()

    all_revisions_text = []

    # page_id = dogPage.pageid
    with RevisionEngine(
        bucket_name='wikitrust-testing',
        storage_db_ctrl=storage_db_ctrl,
        version=1
    ) as re:
        with TextReputationEngine(
            bucket_name='wikitrust-testing',
            storage_db_ctrl=storage_db_ctrl,
            version=1
        ) as tte:
            pass
    #             for revision in all_revisions:
    #                 rev_id = RP.getRevisionMetadata(revision, "revid")
    #                 rev_text = processor.getReadableText(RP.get_text_of_old_revision(dogPage, rev_id))
    #                 all_revisions_text.append(rev_text)
    #                 re.store(page_id=page_id, rev_id=rev_id, text=rev_text,timestamp=datetime.now())
    #                 texttrusts = []
    #                 for word in rev_text.split():
    #                     texttrusts.append(len(word))
    #                 tte.store(page_id=page_id, rev_id=rev_id, text=json.dumps(texttrusts),timestamp=datetime.now())

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
