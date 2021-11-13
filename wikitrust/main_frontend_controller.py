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

    def __exit__(
        self, exec_type, exec_value, traceback
    ):  # other params available: exec_type, exec_value, traceback
        """
        Used for cleaning up on "with" statement exit
        """

    def start_viz_server(self):
        trust_viz.text_trust_visualization_server(
            self.frontend_db_ctrl, self.revStore, self.textTrustStore
        ).run()

    def print_page_details(self, page_id):
        latest_rev_id = self.frontend_db_ctrl.get_most_recent_rev_id(page_id)
        print("Page ID: ", page_id, " Latest revision ID: ", latest_rev_id)

    def print_processed_pages(self):
        print("========= Currently Processed Pages: =========")
        for page in self.frontend_db_ctrl.get_all_pages():
            latest_rev_id = self.frontend_db_ctrl.get_most_recent_rev_id(
                page.page_id
            )
            environment_name = self.frontend_db_ctrl.get_environment(
                page.environment_id
            )
            print(
                page.page_title,
                "(Environment:",
                environment_name,
                ") | Last update date:",
                page.last_check_time,
                "| Latest processed revision id:",
                latest_rev_id,
            )
        print("==============================================")
