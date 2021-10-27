from wikitrust.test.db_test import drop_and_populate
from wikitrust.test.fill_storage_engine import fill_storage_engine

from wikitrust.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust.storage_engine.storage_engine import StorageEngine
from wikitrust.storage_engine.storage_engine import RevisionStorageEngine
from wikitrust.storage_engine.storage_engine import TextTrustStorageEngine
from wikitrust.database.controllers.frontend_db_controller import frontend_db_controller

import wikitrust.storage_engine.local_storage_engine as local_storage_engine
import wikitrust.storage_engine.storage_engine as storage_engine

from wikitrust.computation_engine.triangle_generator import TriangleGenerator
from wikitrust.computation_engine.reputation_generator import ReputationGenerator
from wikitrust.computation_engine.text_annotation import TextAnnotation
import wikitrust.computation_engine.wikitrust_algorithms.text_diff.chdiff as chdiff
import datetime
from datetime import datetime

import json
import math

__PAGEID__ = 31774937
__PAGEJSON__ = "resources/LadyGagaMeatDressRevisions/all_revision.json"
__ALGORITHM_VER__ = "0.1"


def test_computation_engine(compute_db_ctrl, storage_db_ctrl, frontend_db_ctrl):
    # Initialize DB controller
    print("Populating DBController Database")

    dbcontroller = drop_and_populate(compute_db_ctrl)

    # Initialize local text storage engine
    #text_storage_engine = local_storage_engine.LocalStorageEngine(db = None)
    with RevisionStorageEngine(
        bucket_name='wikitrust-testing',
        storage_db_ctrl=storage_db_ctrl,
        version=1
    ) as rse:
        with TextTrustStorageEngine(
            bucket_name='wikitrust-testing',
            storage_db_ctrl=storage_db_ctrl,
            version=1
        ) as tre:
            print("Populating Revision Engine and Text Reputation Engine")
            with open(__PAGEJSON__, encoding="utf-8") as json_file:
                json_object = json.load(json_file)
                #local_storage_engine.load_page_json_into_storage(text_storage_engine, json_object)

            page_id = int(json_object["pageId"])

            for rev_iter in range(10):  # int(json_object["size"])
                rev_id = json_object["revisions"][rev_iter]["revisionId"]
                rev_text = json_object["revisions"][rev_iter]["text"]
                rse.store(
                    page_id=page_id,
                    rev_id=rev_id,
                    text=rev_text,
                    timestamp=datetime.now()
                )
                texttrusts = []
                for word in rev_text.split():
                    texttrusts.append(len(word))
                tre.store(
                    page_id=page_id,
                    rev_id=rev_id,
                    text=json.dumps(texttrusts),
                    timestamp=datetime.now()
                )

            revision_list = frontend_db_ctrl.get_all_revisions(__PAGEID__)
            print("Revision Engine and Text Reputation Engine Populated")

            #Run Triangle generator
            print("Starting Triangle Generator...")
            tg = TriangleGenerator(
                dbcontroller, rse, __ALGORITHM_VER__,
                (3, chdiff.edit_diff_greedy, chdiff.make_index2)
            )
            tg.compute_triangles_batch(__PAGEID__)
            print("Triangle Generator done\n")

            #Run Reputation generator
            print("Starting Reputation Generator...")
            rg = ReputationGenerator(
                dbcontroller, __ALGORITHM_VER__,
                (0.5, (lambda x: math.log(1.1 + x)))
            )
            rg.update_author_reputation()
            print("Reputation Generator done\n")

            #Run Text Annotation on each revision
            print("Running Text Annotation...")
            ta = TextAnnotation(
                dbcontroller, rse, tre, __ALGORITHM_VER__,
                (0.5, 0.5, 5, chdiff.edit_diff_greedy, chdiff.make_index2)
            )
            for revision in sorted(revision_list):
                ta.compute_revision_trust(revision)
            print("Text Annotation done \n")
