import dbtest

import wikitrust.database.controllers.computation_engine_db_controller as db_controller
import wikitrust.storage_engine.local_storage_engine as local_storage_engine

from wikitrust.computation_engine.triangle_generator import TriangleGenerator
from wikitrust.computation_engine.reputation_generator import ReputationGenerator
from wikitrust.computation_engine.text_annotation import TextAnnotation
import wikitrust.computation_engine.wikitrust_algorithms.text_diff.chdiff as chdiff

import json


__DBURI__ = "sqlite://Test.db"
__PAGEID__ = 31774937
__PAGEJSON__ = "../../LadyGagaMeatDressRevisions/all_revision.json"
__ALGORITHM_VER__ = "0.1"

def test_computation_engine():
    # Initialize DB controller
    dbcontroller = dbtest.drop_and_populate(__DBURI__)

    # Initialize local text storage engine
    text_storage_engine = local_storage_engine.LocalStorageEngine(db = None)

    with open(__PAGEJSON__) as json_file:
        json_object = json.load(json_file)
        local_storage_engine.load_page_json_into_storage(text_storage_engine, json_object)

    # Initialize local trust storage engine
    trust_storage_engine = local_storage_engine.LocalStorageEngine(db = None)

    #Run Triangle generator
    tg = TriangleGenerator(dbcontroller, text_storage_engine, __ALGORITHM_VER__, (10, chdiff.edit_diff_greedy, chdiff.make_index2))
    tg.compute_triangles_batch(__PAGEID__)

    #Run Reputation generator
    rg = ReputationGenerator(dbcontroller, __ALGORITHM_VER__, (1, (lambda x: x)))
    rg.update_author_reputation()

    #Run Text Annotation on each revision
    ta = TextAnnotation(dbcontroller, text_storage_engine, trust_storage_engine, __ALGORITHM_VER__, (0.5, 0.5, 5, chdiff.edit_diff_greedy, chdiff.make_index2))
