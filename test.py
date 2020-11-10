import wikitrust.test.db_test as db_test
import wikitrust.database.db_schema as db_schema

def db_population_test():
    db = db_schema.connect_to_db('sqlite://storage.sqlite')
    db_test.populate(db)
