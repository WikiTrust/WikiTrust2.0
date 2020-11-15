import db_schema
import local_storage_engine

import wikitrust_computation.triangle_generator as triangle_generator
import wikitrust_lib.text_diff.chdiff as chdiff

import json


__DBURI__ = "sqlite://Test.db"
__PAGEID__ = 31774937
__PAGEJSON__ = "LadyGagaMeatDressRevisions/all_revision.json"

if __name__ == '__main__':
    db = db_schema.connect_to_db(__DBURI__)
    text_storage_engine = local_storage_engine.LocalStorageEngine(db = None)

    with open(__PAGEJSON__) as json_file:
        json_object = json.load(json_file)
        local_storage_engine.load_page_json_into_storage(text_storage_engine, json_object)

    tg = triangle_generator.TriangleGenerator(db, text_storage_engine, "TRIANGLE_TEST", 10, chdiff.edit_diff_greedy, chdiff.make_index2)
    tg.compute_triangles_batch(__PAGEID__)
