from datetime import datetime
import sys

# constants used in the program
import wikitrust_py.consts as consts

# for database
from wikitrust_py.database import db_schema

# for testing?
# import wikitrust_py.test.db_test as db_test
# import wikitrust_py.test.computation_engine_debug as ce_test
# import wikitrust_py.test.storage_engine_debug as storage_test
# import wikitrust_py.test.fill_storage_engine as storage_fill

# For storage engine
from wikitrust_py.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust_py.storage_engine.storage_engine import RevisionStorageEngine
from wikitrust_py.storage_engine.storage_engine import TextTrustStorageEngine

# controllers
from wikitrust_py.main_backend_controller import main_backend_controller
from wikitrust_py.main_frontend_controller import main_frontend_controller

if __name__ == '__main__':

    # Connect to database:
    db = db_schema.connect_to_db(consts.__DBURI__)

    #initialize db controller for storage engines
    storage_db_ctrl = storage_engine_db_controller(db)
    # storage_db_ctrl.print_storage_table() # < for debugging

    # initialize storage engines
    # NOTE: I last set __USE_GCS__ in consts.py to False, so the storage engines will save to local files instead of using Google Cloud Storage, you can change this to True to use GCS
    revStore = RevisionStorageEngine(
        bucket_name=consts.__GCS_BUCKET_NAME__,
        storage_db_ctrl=storage_db_ctrl,
        version=consts.__ALGORITHM_VER__
    )
    textTrustStore = TextTrustStorageEngine(
        bucket_name=consts.__GCS_BUCKET_NAME__,
        storage_db_ctrl=storage_db_ctrl,
        version=consts.__ALGORITHM_VER__
    )

    # initialize backend:
    with main_backend_controller(db, revStore, textTrustStore) as backend_ctrl:
        with main_frontend_controller(db, backend_ctrl) as frontend_ctrl:
            frontend_ctrl.print_processed_pages()
            frontend_ctrl.start_viz_server()
            # NOTE: you'll need some kind of infinite loop after starting the viz server, as it runs in a seperate thread
            # that will get killed if this thread exits (like if the program finishes the last line).

            environment = backend_ctrl.get_or_create_wiki_environment(
                consts.__WIKI_ENVIRONMENT_NAME__
            )

            commandLineMessage = "Enter the name/search keyword of a wikipedia page to process it. Or type STOP to quit"
            print(commandLineMessage)
            for search_term in sys.stdin:

                search_term = search_term.rstrip()
                if search_term == 'STOP':
                    break

                page = backend_ctrl.find_page(search_term)
                if page is None:
                    print("No wikipedia page found for that search.")
                else:
                    print("Processing page: " + page.title())
                    backend_ctrl.process_page(page, environment)
                    print("Done processing page: " + page.title())
                print(commandLineMessage)

    print("Program has exited. Server thread should have stopped too.")
