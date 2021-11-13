__ALGORITHM_VER__ = 1
__DBURI__ = "sqlite://storage.sqlite"
__STORAGE_BUCKET_NAME__ = "wikitrust-testing"

from datetime import datetime

# for database
from wikitrust.database import db_schema

# for testing?
# import wikitrust.test.db_test as db_test
# import wikitrust.test.computation_engine_debug as ce_test
# import wikitrust.test.storage_engine_debug as storage_test
# import wikitrust.test.fill_storage_engine as storage_fill

# For storage engine
from wikitrust.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust.storage_engine.storage_engine import RevisionStorageEngine
from wikitrust.storage_engine.storage_engine import TextTrustStorageEngine

# controllers
from wikitrust.main_backend_controller import main_backend_controller
from wikitrust.main_frontend_controller import main_frontend_controller

if __name__ == '__main__':

    # Connect to database:
    db = db_schema.connect_to_db(__DBURI__)

    #initialize storage engines
    storage_db_ctrl = storage_engine_db_controller(db)
    # storage_db_ctrl.print_storage_table() # < for debugging
    revStore = RevisionStorageEngine(
        bucket_name=__STORAGE_BUCKET_NAME__,
        storage_db_ctrl=storage_db_ctrl,
        version=__ALGORITHM_VER__
    )
    textTrustStore = TextTrustStorageEngine(
        bucket_name=__STORAGE_BUCKET_NAME__,
        storage_db_ctrl=storage_db_ctrl,
        version=__ALGORITHM_VER__
    )

    # initialize backend:
    with main_backend_controller(db, revStore, textTrustStore) as backend_ctrl:
        with main_frontend_controller(db, backend_ctrl) as frontend_ctrl:
            frontend_ctrl.print_processed_pages()
            frontend_ctrl.start_viz_server()
            while True:
                pass
