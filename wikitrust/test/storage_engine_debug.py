from wikitrust.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust.storage_engine.storage_engine import StorageEngine
import wikitrust.database.db_schema as schema
import datetime
from datetime import datetime
from pydal.migrator import InDBMigrator
from pydal import DAL, Field

import random

__DBURI__ = "sqlite://Test.db"
__PAGEID__ = 31774937
__PAGEJSON__ = "resources/LadyGagaMeatDressRevisions/all_revision.json"
__ALGORITHM_VER__ = "0.1"

def test_storage_engine():
    db_ctrl = storage_engine_db_controller(uri=__DBURI__)
    se = StorageEngine(bucket_name='wikitrust-testing', num_revs_per_slot=2, db_ctrl=db_ctrl, default_version=1)

    randomInteger = random.randint(1, 50)
    print("storing revision with random page_id number = ",3)
    print("and rev_id number = ",randomInteger)

    se.store(page_id=3, version_id="2", rev_id=9, text="asdf", timestamp=datetime.now(), kind="stuff")
    se.store(page_id=3, version_id="2", rev_id=8, text="asdf", timestamp=datetime.now(), kind="stuff")
    print(se.read(page_id=3, version_id="2", rev_id=8))