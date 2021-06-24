import json
import wikitrust.test.db_test as db_test
import wikitrust.test.computation_engine_debug as ce_test
import wikitrust.test.text_trust_vizualizer.text_trust_vis_server as trust_viz
import wikitrust.test.storage_engine_debug as storage_test
import wikitrust.test.fill_storage_engine as storage_fill
# For revision puller
import wikitrust.revision_puller.SearchEngine as SE
import wikitrust.revision_puller.RevisionPuller as RP
import wikitrust.revision_puller.PageProcessor as PP
from pywikibot import Timestamp
# For storage engine
from pydal import DAL, Field
from wikitrust.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust.storage_engine.storage_engine import StorageEngine
from wikitrust.storage_engine.storage_engine import RevisionEngine
from wikitrust.storage_engine.storage_engine import TextReputationEngine
import wikitrust.database.db_schema as schema
import datetime
from datetime import datetime
from pydal.migrator import InDBMigrator

import wikitrust.database.db_schema as db_schema
import os

__DBURI__ = "sqlite://storage.sqlite"

def db_population_test():
    db_test.drop_and_populate()

if __name__ == '__main__':
    # engine = SE.SearchEngine()
    # processor = PP.PageProcessor()
    # dogPage = engine.search("Dog", max_pages_grabbed=1, search_by="nearmatch")[0]
    # all_revisions = RP.get_latest_revisions(dogPage, recent_to_oldest=False, num_revisions=1)
    # all_revisions_text = []
    # db_ctrl = storage_engine_db_controller(uri=__DBURI__)
    # page_id = dogPage.pageid
    # with RevisionEngine(bucket_name='wikitrust-testing', db_ctrl=db_ctrl, version=1) as re:
    #         with TextReputationEngine(bucket_name='wikitrust-testing', db_ctrl=db_ctrl, version=1) as tte:
    #             for revision in all_revisions:
    #                 rev_id = RP.getRevisionMetadata(revision, "revid")
    #                 rev_text = processor.getReadableText(RP.get_text_of_old_revision(dogPage, rev_id))
    #                 all_revisions_text.append(rev_text)
    #                 re.store(page_id=page_id, rev_id=rev_id, text=rev_text,timestamp=datetime.now())
    #                 texttrusts = []
    #                 for word in rev_text.split():
    #                     texttrusts.append(len(word))
    #                 tte.store(page_id=page_id, rev_id=rev_id, text=json.dumps(texttrusts),timestamp=datetime.now())

    # db_ctrl.print_storage_table()


    #ce_test.test_computation_engine()


    db_population_test()
    storage_fill.fill_storage_engine()
    # storage_test.test_storage_engine()
    db = db_schema.connect_to_db()
    print(db)
    print(db.text_storage)
    trust_viz.text_trust_visualization_server().run()

