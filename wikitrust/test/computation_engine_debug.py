import wikitrust.database.controllers.computation_engine_db_controller as db_controller
import wikitrust.storage_engine.local_storage_engine as local_storage_engine

import wikitrust.computation_engine.triangle_generator as triangle_generator
import wikitrust.computation_engine.reputation_generator as reputation_generator
import wikitrust.computation_engine.text_annotation as text_annotation
import wikitrust.computation_engine.wikitrust_algorithms.text_diff.chdiff as chdiff

import json


__DBURI__ = "sqlite://Test.db"
__PAGEID__ = 31774937
__PAGEJSON__ = "../../LadyGagaMeatDressRevisions/all_revision.json"
__ALGORITHM_VER__ = 0.1

if __name__ == '__main__':
    # Initialize DB controller
    

    # Initialize local text storage engine
    text_storage_engine = local_storage_engine.LocalStorageEngine(db = None)

    with open(__PAGEJSON__) as json_file:
        json_object = json.load(json_file)
        local_storage_engine.load_page_json_into_storage(text_storage_engine, json_object)

    # Initialize local trust storage engine
    trust_storage_engine = local_storage_engine.LocalStorageEngine(db = None)

    #Run Triangle generator
    tg = triangle_generator.TriangleGenerator(db, text_storage_engine, "0.1", 10, chdiff.edit_diff_greedy, chdiff.make_index2)
    tg.compute_triangles_batch(__PAGEID__)

    #Run Reputation generator

    #Run Text Annotation on each revision

