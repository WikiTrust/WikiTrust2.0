import storage_engine.storage_engine as StorageEngine
import database.db_schema as schema
import datetime
from datetime import datetime
from pydal.migrator import InDBMigrator
from pydal import DAL, Field

import random

db = schema.connect_to_db()
se = StorageEngine.StorageEngine(bucket_name='wikitrust-testing', num_revs_per_file=2, db=db, database_table=db.text_storage, default_version=1)

randomInteger = random.randint(1, 50)
print("storing revision with random page_id number = ",randomInteger * 2)
print("and rev_id number = ",randomInteger)

se.store(page_id=randomInteger * 2, version_id="100", rev_id=randomInteger, text="asdf", timestamp=datetime.now(), kind="stuff")
se.store(page_id=3, version_id="2", rev_id=8, text="asdf", timestamp=datetime.now(), kind="stuff")
print(se.read(page_id=3, version_id="2", rev_id=8))