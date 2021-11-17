from wikitrust_py.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust_py.storage_engine.storage_engine import StorageEngine
from wikitrust_py.storage_engine.storage_engine import RevisionStorageEngine
import wikitrust_py.database.db_schema as schema
import datetime
from datetime import datetime
from pydal.migrator import InDBMigrator
from pydal import DAL, Field

import random

__PAGEID__ = 31774937
__PAGEJSON__ = "resources/LadyGagaMeatDressRevisions/all_revision.json"


def test_storage_engine(storage_db_ctrl):

    randomInteger = random.randint(1, 50)
    print("storing revision with random page_id number = ", 3)
    print("and rev_id number = ", randomInteger)

    # with open("/home/ericvin/Projects/WikiTrust2.0/LadyGagaMeatDressRevisions/all_revision.json") as json_file:
    #     json_object = json.load(json_file)
    #     load_page_json_into_storage(dummy_storage_engine, json_object)

    #     page_id = int(input_json["pageId"])

    #     for rev_iter in range(int(input_json["size"])):
    #         rev_id = input_json["revisions"][rev_iter]["revisionId"]
    #         rev_text = input_json["revisions"][rev_iter]["text"]
    #         storage_engine.store("DUMMY_VERSION", page_id, rev_id, json.dumps(rev_text.split()), datetime.datetime.now())
    # se.store(page_id=31774937, version_id="2", rev_id=941941295, text="First One", timestamp=datetime.now(), kind="stuff")
    # se.store(page_id=31774937, version_id="2", rev_id=941817554, text="Second One", timestamp=datetime.now(), kind="stuff")
    # se.store(page_id=31774937, version_id="2", rev_id=933170168, text="Third 1ne", timestamp=datetime.now(), kind="stuff")
    # print(se.read(page_id=31774937, version_id="2", rev_id=933170168))

    with RevisionStorageEngine(
        bucket_name='wikitrust-testing', db_ctrl=storage_db_ctrl, version=1
    ) as se:
        se.store(
            page_id=31774937,
            rev_id=429099416,
            text="2nd",
            timestamp=datetime.now()
        )
        se.store(
            page_id=31774937,
            rev_id=429097598,
            text="0th",
            timestamp=datetime.now()
        )
        se.store(
            page_id=31774937,
            rev_id=442457383,
            text="51th",
            timestamp=datetime.now()
        )
        se.store(
            page_id=31774937,
            rev_id=429097648,
            text="1st",
            timestamp=datetime.now()
        )
        se.store(
            page_id=31774937,
            rev_id=442400879,
            text="50th",
            timestamp=datetime.now()
        )

        print(se.read(page_id=31774937, rev_id=442400879))

    with RevisionStorageEngine(
        bucket_name='wikitrust-testing', db_ctrl=storage_db_ctrl, version=1
    ) as se:
        se.store(
            page_id=31774937,
            rev_id=429102121,
            text="3rd",
            timestamp=datetime.now()
        )
        print("------------------------------")
        print("second is: %s" % se.read(page_id=31774937, rev_id=429099416))
        print("third is: %s" % se.read(page_id=31774937, rev_id=429102121))