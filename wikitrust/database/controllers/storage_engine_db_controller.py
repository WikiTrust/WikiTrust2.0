from pydal import DAL, Field
from pydal.migrator import InDBMigrator
from datetime import date
import wikitrust.database.db_schema as db_schema
from wikitrust.database.controllers.db_wrappers import autocommit
import logging 


class storage_engine_db_controller: 
    def __init__(self, uri = 'sqlite://storage.sqlite'):
        self.db = db_schema.connect_to_db(uri)

    