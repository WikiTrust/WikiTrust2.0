import wikitrust.test.db_test as db_test
import wikitrust.test.computation_engine_debug as ce_test
import wikitrust.test.text_trust_vizualizer.text_trust_vis_server as trust_viz
import wikitrust.test.storage_engine_debug as storage_test
import wikitrust.test.fill_storage_engine as storage_fill

import wikitrust.database.db_schema as db_schema
import os

def db_population_test():
    db_test.drop_and_populate()

if __name__ == '__main__':
    ce_test.test_computation_engine()


    #os.system("del storage.sqlite")
    #os.system("rm storage.sqlite")

    #db_population_test()
    #storage_fill.fill_storage_engine()
    # storage_test.test_storage_engine()
    # db = db_schema.connect_to_db()
    # print(db)
    # print(db.text_storage)
    #trust_viz.text_trust_visualization_server().run()

