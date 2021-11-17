from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from logging import warning, error
import traceback, json, threading

import wikitrust_py.database.controllers.frontend_db_controller as database_controller
from wikitrust_py.database.controllers.storage_engine_db_controller import storage_engine_db_controller
from wikitrust_py.storage_engine.storage_engine import TextTrustStorageEngine
from wikitrust_py.storage_engine.storage_engine import RevisionStorageEngine


# a very insecure generic get request handler factory function
def MakeHandlerClassWithParameters(
    staticWebContentDirectory='./wikitrust_py/test/text_trust_vizualizer',
    apiHandlerClass=None
):
    class _get_request_handler(SimpleHTTPRequestHandler):
        api_handler_class = apiHandlerClass

        # Initialize the SimpleHTTPRequestHandler (in this case the super class)
        # with the directory specified and all other passed arguements
        def __init__(self, *args, **kwargs):
            super().__init__(
                *args, directory=staticWebContentDirectory, **kwargs
            )

        def reply_with_error(self, err, errorCode=400):
            errMsg = str(err)
            error("Error Handling HTTP request: " + errMsg)
            error(traceback.format_exc())

            errJsonStr = json.dumps({"error": errMsg})
            self.send_response(errorCode)
            self.send_header('Content-type', "application/json")
            self.send_header(
                "Access-Control-Allow-Origin", "*"
            )  # TODO: CHange to wikipedia only
            self.end_headers()
            self.wfile.write(bytes(errJsonStr, 'utf-8'))

        def reply_with_success(self, bodyStr, contentType="application/json"):
            self.send_response(200)
            self.send_header('Content-type', contentType)
            self.send_header(
                "Access-Control-Allow-Origin", "*"
            )  # TODO: CHange to wikipedia only
            self.end_headers()
            self.wfile.write(bytes(bodyStr, 'utf-8'))

        # Handle GET Requests from WebApp
        def do_GET(self):
            try:
                pathParts = urlparse(self.path)
                if (pathParts.path == "/api"):
                    query = pathParts.query
                    try:
                        query_components = dict(
                            qc.split("=") for qc in query.split("&")
                        )
                    except:
                        raise Exception(
                            "/api rest endpoint: got malformed or empty query string:"
                            + query
                        )

                    reply = json.dumps(
                        apiHandlerClass.handle_api_request(
                            queryParams=query_components
                        )
                    )
                    return self.reply_with_success(bodyStr=reply)
            except Exception as e:
                return self.reply_with_error(err=e)

            return super().do_GET()

    return _get_request_handler


class text_trust_visualization_server:
    def __init__(self, frontend_db_ctrl, revStore, textTrustStore) -> None:
        self.current_revision_id = None
        self.frontend_db_ctrl = frontend_db_ctrl

        # get references to the storage engines
        self.revStore = revStore
        self.textTrustStore = textTrustStore

    def get_latest_page_text_trust(self, pageId) -> str:
        if (pageId == None or pageId == ""):
            raise Exception(
                "get_latest_page_text_trust() - Got Passed Null Page ID!"
            )
        rev_id = self.frontend_db_ctrl.get_most_recent_rev_id(page_id=pageId)
        return {
            "rev_id": rev_id,
            "values": self.get_revision_text_trust(rev_id)
        }

    def get_revision_text_trust(self, revisionId) -> str:
        if (revisionId == None or revisionId == ""):
            raise Exception(
                "get_revision_text_trust() - Got Passed Null Revision ID!"
            )
        page_id = self.frontend_db_ctrl.get_page_from_rev(rev_id=revisionId)
        revisionIdx = self.frontend_db_ctrl.get_most_recent_rev_index(
            page_id=page_id
        )
        text_trust = self.textTrustStore.read(
            page_id=page_id, rev_id=revisionId
        )
        text_words = self.revStore.read(page_id=page_id, rev_id=revisionId)
        return {
            "words": json.loads(text_words),
            "trust_values": json.loads(text_trust),
            "revision_index": revisionIdx
        }

    def get_page_from_revision_id(self, revisionId) -> str:
        if (revisionId == None or revisionId == ""):
            raise Exception(
                "get_page_from_revision_id() - Got Passed Null Revision ID!"
            )
        page_id = self.frontend_db_ctrl.get_page_from_rev(rev_id=revisionId)
        return {"page_id": page_id}

    def get_previous_revision_id(self, revisionId) -> str:
        if (revisionId == None or revisionId == ""):
            raise Exception(
                "get_previous_revision_id() - Got Passed Null Revision ID!"
            )
        prev_rev_id = self.frontend_db_ctrl.get_prev_rev(rev_id=revisionId)
        return {"rev_id": prev_rev_id}

    def get_next_revision_id(self, revisionId) -> str:
        if (revisionId == None or revisionId == ""):
            raise Exception(
                "get_next_revision_id() - Got Passed Null Revision ID!"
            )
        prev_rev_id = self.frontend_db_ctrl.get_next_rev(rev_id=revisionId)
        return {"rev_id": prev_rev_id}

    def get_query_parameter(self, params, key):
        try:
            return params[key]
        except:
            raise Exception("Required query parameter '" + key + "' missing!")

    # Handle GET Requests from WebApp
    def handle_api_request(self, queryParams):
        print(queryParams)

        action = self.get_query_parameter(queryParams, 'action')

        if (action == 'get_latest_page_text_trust'):
            page_id = self.get_query_parameter(queryParams, 'page_id')
            return self.get_latest_page_text_trust(page_id)

        elif (action == 'get_revision_text_trust'):
            revision_id = self.get_query_parameter(queryParams, 'revision_id')
            return self.get_revision_text_trust(revision_id)

        elif (action == 'get_next_revision_id'):
            revision_id = self.get_query_parameter(queryParams, 'revision_id')
            return self.get_next_revision_id(revision_id)

        elif (action == 'get_previous_revision_id'):
            revision_id = self.get_query_parameter(queryParams, 'revision_id')
            return self.get_previous_revision_id(revision_id)

        elif (action == 'get_page_from_revision_id'):
            revision_id = self.get_query_parameter(queryParams, 'revision_id')
            return self.get_page_from_revision_id(revision_id)

        else:
            raise Exception(
                "What the heck is this action request? action=" + action
            )

    def run(self, port=8000):
        # Server settings
        # By default we use the localhost address (127.0.0.1) and the port 8000
        server_address = ('', port)

        requestHandler = MakeHandlerClassWithParameters(
            staticWebContentDirectory='./wikitrust_py/text_trust_vizualizer',
            apiHandlerClass=self
        )

        print('\nStarting server...')
        httpd = HTTPServer(server_address, requestHandler)

        print(
            'Running server - open your browser to: http://localhost:' +
            str(port)
        )
        print(
            'Or run the extension/bookmarklet on a wikipedia page - the extension assumes port=8000\n'
        )

        # Start the server in a new thread
        server_thread = threading.Thread(
            name='wikitrust_web_server_thread', target=httpd.serve_forever
        )  # can also pass args with args=() param
        server_thread.setDaemon(
            True
        )  # Set as a daemon so it will be killed once the main thread is dead.
        server_thread.start()