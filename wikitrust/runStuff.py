import storage_engine.storage_engine as StorageEngine
import database.db_schema as schema
import datetime
from datetime import datetime
from pydal.migrator import InDBMigrator
from pydal import DAL, Field

db = schema.connect_to_db()

se = StorageEngine.StorageEngine(bucket_name='wikitrust-testing', num_revs_per_file=2, database_table=db.text_storage, default_version=1)

se.store(page_id=0, version_id=1, rev_id=1, text="asdf", timestamp=datetime.now(), kind="stuff")