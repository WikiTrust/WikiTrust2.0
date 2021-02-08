from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from logging import warning,error
import traceback
import json, os

import wikitrust.database.controllers.frontend_db_controller as database_controller
import wikitrust.storage_engine.local_storage_engine as local_storage_engine

# a very insecure generic get request handler factory fucntion
def MakeHandlerClassWithParameters(staticWebContentDirectory='./wikitrust/test/text_trust_vizualizer',apiHandlerClass=None):
    class _get_request_handler(SimpleHTTPRequestHandler):
        api_handler_class = apiHandlerClass
        # Initialize the SimpleHTTPRequestHandler (in this case the super class)
        # with the directory specified and all other passed arguements
        def __init__(self, *args,  **kwargs):
            super().__init__( *args, directory=staticWebContentDirectory,**kwargs)

        def reply_with_error(self,err,errorCode=400):
            errMsg = str(err)
            error("Error Handling HTTP request: " + errMsg)
            error(traceback.format_exc())

            errJsonStr = json.dumps({"error":errMsg})
            self.send_response(errorCode)
            self.send_header('Content-type', "application/json")
            self.end_headers()
            self.wfile.write(bytes(errJsonStr, 'utf-8'))

        def reply_with_success(self,bodyStr,contentType="application/json"):
            self.send_response(200)
            self.send_header('Content-type', contentType)
            self.end_headers()
            self.wfile.write(bytes(bodyStr, 'utf-8'))

        # Handle GET Requests from WebApp
        def do_GET(self):
            try:
                pathParts = urlparse(self.path)
                if(pathParts.path == "/api"):
                    query = pathParts.query
                    try:
                        query_components = dict(qc.split("=") for qc in query.split("&"))
                    except:
                        raise Exception("/api rest endpoint: got malformed or empty query string:" + query)

                    reply = apiHandlerClass.handle_api_request(queryParams=query_components)
                    self.reply_with_success(bodyStr=reply)
            except Exception as e:
                self.reply_with_error(err=e)

            else:
                return super().do_GET()
    return _get_request_handler


class text_trust_visualization_server:
    db_controller = database_controller.frontend_db_controller()
    def __init__(self) -> None:
        pass

    def get_latest_text_trust (self,pageId) -> str:
        return json.dumps({"this just in":pageId})

    def get_revision_text_trust (self,revisionId) -> str:
        return json.dumps({"no! Yohoodslkjf":revisionId})

    def get_page_from_revision_id (self,revisionId) -> str:
        page_id = self.db_controller.get_page_from_rev(rev_id=revisionId)
        return json.dumps({"page_id":page_id})

    def get_previous_revision_id (self,revisionId) -> str:
        prev_rev_id = self.db_controller.get_prev_rev(rev_id=revisionId)
        return json.dumps({"revision_id":prev_rev_id})

    def get_query_parameter(self,params,key):
        try:
            return params[key]
        except:
            raise Exception("Required query parameter '" + key + "' missing!")

    # Handle GET Requests from WebApp
    def handle_api_request(self,queryParams):
        print(queryParams)

        action = self.get_query_parameter(queryParams,'action')

        if (action == 'get_latest_text_trust'):
            page_id = self.get_query_parameter(queryParams,'page_id')
            return self.get_latest_text_trust(page_id)

        elif (action == 'get_revision_text_trust'):
            revision_id = self.get_query_parameter(queryParams,'revision_id')
            return self.get_revision_text_trust(revision_id)

        elif (action == 'get_previous_revision_id'):
            revision_id = self.get_query_parameter(queryParams,'revision_id')
            return self.get_previous_revision_id(revision_id)

        elif (action == 'get_page_from_revision_id'):
            revision_id = self.get_query_parameter(queryParams,'revision_id')
            return self.get_page_from_revision_id(revision_id)

        else:
            raise Exception("What the heck is this action request? action="+action)



    def run(self,port=8000):
        # Server settings
        # By default we use the localhost address (127.0.0.1) and the port 8080
        server_address = ('', port)

        requestHandler = MakeHandlerClassWithParameters(staticWebContentDirectory='./wikitrust/test/text_trust_vizualizer',apiHandlerClass=self)

        print('Starting server...')
        httpd = HTTPServer(server_address, requestHandler)

        print('Running server - open your browser to: http://localhost:'+ str(port))
        httpd.serve_forever()


# def getFilledHTMLString(datas):
#     print(os.getcwd())
#     f = open("./analysis/demo.html", "r")
#     HTMLPageStr = f.read()
#     jsonDataStr = json.dumps(datas)
#     return HTMLPageStr.replace("{/* THIS WILL BE REPLACED BY THE PYTHON OUTPUT */ }",jsonDataStr)


# def getTrustExample():
#     """
#     An example of using text_trust.py. The test strings are the different
#     texts of different versions. The test_trusts list is the different
#     author_reputations of each version.
#     """
#     initial_trust = 1

#     test_strings = []
#     test_strings.append("the quick brown fox jumps over the lazy dog")
#     test_strings.append("foo the quick brown fox jumps over the lazy dog bar")
#     test_strings.append("the quick brown fox jumps over the lazy dog")
#     test_strings.append("the lazy fox jumps over the quick brown dog")
#     test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff")

#     test_trusts = [10, 7, 10, 20]

#     trust_inheritance_const = 0.5
#     revision_const = 0.1
#     edge_effect_const = 2

#     constants = (trust_inheritance_const, revision_const, edge_effect_const)

#     print("Initial String: " + str(test_strings[0]))

#     for string_iter, string in enumerate(test_strings):
#         print("String %d: %s" %(string_iter, string))
#     print()

#     print("Version 1:\n")
#     print("Initial Trust: " + str(initial_trust) + "\n")

#     text_list = test_strings[0].split()

#     version_list = []

#     #ver = Version(word_list, edit_list, author_reputation, initial_trust, trust_inheritance_const, revision_const, edge_effect_const)
#     ver = Version.create_initial_version(text_list, initial_trust, constants)

#     version_list.append(ver)

#     print("".join([str(word) for word in ver.word_list]) + "\n")

#     print("Block List:")
#     print("".join([str(block) + "\n" for block in ver.block_list]))

#     print("\n")

#     for string_iter in range(len(test_strings)-1):
#         print("Version %d:\n" % (string_iter + 2))
#         print("Author Reputation: %d\n" % (test_trusts[string_iter]))

#         diff_list = test_tichy(test_strings[string_iter], test_strings[string_iter + 1])
#         edit_list = [Edit.edit_tuple_constructor(edit) for edit in diff_list]
#         text_list = test_strings[string_iter+1].split()

#         ver = Version.create_next_version(ver, text_list, edit_list, test_trusts[string_iter])

#         version_list.append(ver)

#         print("".join([str(word) for word in ver.word_list]) + "\n")

#         print("Block List:\n")
#         print("".join([str(block) + "\n" for block in ver.block_list]))
#         print("\n")

#     return  version_list

# def run(port=8080):

#     print('starting server...')

#     datas = []
#     outputVersions = getTrustExample()
#     for version in outputVersions:
#         words = []
#         for word in version.word_list:
#             words.append(word.__dict__)
#         datas.append(words)

#     # Server settings
#     # By default we use the localhost address (127.0.0.1) and the port 8080
#     server_address = ('127.0.0.1', port)

#     HTTP_RequestHandler.jsonDatas = datas # hacky but works
#     httpd = HTTPServer(server_address,HTTP_RequestHandler)


#     print('running server... - open your browser to: http://localhost:'+ str(port))
#     httpd.serve_forever()

# run()

server = text_trust_visualization_server()
server.run()