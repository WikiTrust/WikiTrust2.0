from wikitrust.test.db_test import drop_and_populate

import wikitrust.database.controllers.computation_engine_db_controller as db_controller
import wikitrust.storage_engine.local_storage_engine as local_storage_engine

from wikitrust.computation_engine.triangle_generator import TriangleGenerator
from wikitrust.computation_engine.reputation_generator import ReputationGenerator
from wikitrust.computation_engine.text_annotation import TextAnnotation
import wikitrust.computation_engine.wikitrust_algorithms.text_diff.chdiff as chdiff

import json


__DBURI__ = "sqlite://Test.db"
__PAGEID__ = 31774937
__PAGEJSON__ = "resources/LadyGagaMeatDressRevisions/all_revision.json"
__ALGORITHM_VER__ = "0.1"

def test_computation_engine():
    # Initialize DB controller
    dbcontroller = drop_and_populate(__DBURI__)

    # Initialize local text storage engine
    text_storage_engine = local_storage_engine.LocalStorageEngine(db = None)

    with open(__PAGEJSON__) as json_file:
        json_object = json.load(json_file)
        local_storage_engine.load_page_json_into_storage(text_storage_engine, json_object)

    revision_list = text_storage_engine.pages[__PAGEID__].keys()

    print("Local Text Storage Engine initialized...")

    # Initialize local trust storage engine
    trust_storage_engine = local_storage_engine.LocalStorageEngine(db = None)

    print("Local Trust Storage Engine initialized...")

    print()

    #Run Triangle generator
    print("Starting Triangle Generator...")
    tg = TriangleGenerator(dbcontroller, text_storage_engine, __ALGORITHM_VER__, (3, chdiff.edit_diff_greedy, chdiff.make_index2))
    tg.compute_triangles_batch(__PAGEID__)
    print("Triangle Generator done\n")

    #Run Reputation generator
    print("Starting Reputation Generator...")
    rg = ReputationGenerator(dbcontroller, __ALGORITHM_VER__, (1, (lambda x: x)))
    rg.update_author_reputation()
    print("Reputation Generator done\n")

    #Run Text Annotation on each revision
    print("Running Text Annotation...")
    ta = TextAnnotation(dbcontroller, text_storage_engine, trust_storage_engine, __ALGORITHM_VER__, (0.5, 0.5, 5, chdiff.edit_diff_greedy, chdiff.make_index2))
    for revision in revision_list:
        ta.compute_revision_trust(revision)
    print("Text Annotation done \n")
