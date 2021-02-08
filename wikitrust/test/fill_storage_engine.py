from wikitrust.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust.storage_engine.storage_engine import TextReputationEngine
from wikitrust.storage_engine.storage_engine import RevisionEngine
import wikitrust.database.db_schema as schema
import datetime
from datetime import datetime
from pydal.migrator import InDBMigrator
from pydal import DAL, Field
import json

import random
__DBURI__ = "sqlite://storage.sqlite"
__PAGEID__ = 31774937
__PAGEJSON__ = "resources/LadyGagaMeatDressRevisions/all_revision.json"
__ALGORITHM_VER__ = "0.1"

def fill_storage_engine():
    db_ctrl = storage_engine_db_controller(uri=__DBURI__)

    with open("./resources/LadyGagaMeatDressRevisions/all_revision.json") as json_file:
        json_object = json.load(json_file)

    page_id = int(json_object["pageId"])
    with RevisionEngine(bucket_name='wikitrust-testing', db_ctrl=db_ctrl, version=1) as re:
        with TextReputationEngine(bucket_name='wikitrust-testing', db_ctrl=db_ctrl, version=1) as tte:
            for rev_iter in range(10): # int(json_object["size"])
                rev_id = json_object["revisions"][rev_iter]["revisionId"]
                rev_text = json_object["revisions"][rev_iter]["text"]
                re.store(page_id=page_id, rev_id=rev_id, text=rev_text,timestamp=datetime.now())
                texttrusts = []
                for word in rev_text.split():
                    texttrusts.append(len(word))
                tte.store(page_id=page_id, rev_id=rev_id, text=json.dumps(texttrusts),timestamp=datetime.now())

    db_ctrl.print_storage_table()

    for rev_iter in range(10): # int(json_object["size"])
        rev_id = json_object["revisions"][rev_iter]["revisionId"]
        print("reading: "+str(rev_id))
        print(tte.read(page_id=page_id, rev_id=rev_id))
        # ^ON Second thought How is this working at all? tte is out of scope.
