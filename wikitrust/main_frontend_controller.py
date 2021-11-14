# for extension & debugging viz server
from wikitrust.database.controllers.frontend_db_controller import frontend_db_controller
import wikitrust.text_trust_vizualizer.text_trust_vis_server as trust_viz


class main_frontend_controller:
    def __init__(self, db, backend_ctrl):
        self.frontend_db_ctrl = frontend_db_controller(db)
        self.backend_ctrl = backend_ctrl

        # get references to the storage engines
        self.revStore = backend_ctrl.revStore
        self.textTrustStore = backend_ctrl.textTrustStore

    def __enter__(self):
        """
        Used for returning self for "with" statement
        """
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        """
        Used for cleaning up on "with" statement exit
        """
        #TODO: probably should shut down the visualization server component gracefully here

    def start_viz_server(self):
        trust_viz.text_trust_visualization_server(
            self.frontend_db_ctrl, self.revStore, self.textTrustStore
        ).run()

    def print_page_details(self, page_id):
        latest_rev_id = self.frontend_db_ctrl.get_most_recent_rev_id(page_id)
        print("Page ID: ", page_id, " Latest revision ID: ", latest_rev_id)

    def print_processed_pages(self):
        print("========= Wikipedia Pages in our DB: =========")
        for page in self.frontend_db_ctrl.get_all_pages():
            latest_rev_id = self.frontend_db_ctrl.get_most_recent_rev_id(
                page.page_id
            )
            latest_rev_index = self.frontend_db_ctrl.get_most_recent_rev_index(
                page.page_id
            )
            environment_name = self.frontend_db_ctrl.get_environment(
                page.environment_id
            )
            print(
                page.page_title, "(Enviro:", environment_name, ") PageID:",
                page.page_id, "| Last Update:", page.last_check_time,
                "| Last pulled revision:", latest_rev_id, "(rev_idx",
                latest_rev_index, ")"
            )
        print(
            "Note: These pages may not be fully processed if the program was halted before processing finished"
        )
        print("==============================================")
