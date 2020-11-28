import wikitrust.test.db_test as db_test
import wikitrust.test.computation_engine_debug as ce_test

import wikitrust.database.db_schema as db_schema

def db_population_test():
    db = db_schema.connect_to_db('sqlite://storage.sqlite')
    db_test.populate(db)

if __name__ == '__main__':
    ce_test.test_computation_engine()
