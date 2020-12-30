import wikitrust.test.db_test as db_test
import wikitrust.test.computation_engine_debug as ce_test
import wikitrust.test.storage_engine_debug as storage_test

import wikitrust.database.db_schema as db_schema

def db_population_test():
    db_test.drop_and_populate()

if __name__ == '__main__':
    # ce_test.test_computation_engine()
    storage_test.test_storage_engine()
    # db = db_schema.connect_to_db()
    # print(db)
    # print(db.text_storage)
