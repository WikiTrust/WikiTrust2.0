from http.server import SimpleHTTPRequestHandler, HTTPServer
import json, os

from text_trust.version import Version
from text_trust.block import Block
from text_trust.edit import Edit
from text_trust.word import Word

from chdiff import test_tichy, test_greedy, print_edit_diff


class HTTP_RequestHandler(SimpleHTTPRequestHandler):
  # Initialize the SimpleHTTPRequestHandler (in this case the super class)
  # with the directory specified and all other passed arguements
#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, directory="./", **kwargs)

  # Handle GET Requests from WebApp
  def do_GET(self):

      # Set response status code
      self.send_response(200)

      # Send headers
      self.send_header('Content-type','text/html') #self.send_header('Content-type','application/json')
      self.send_header('Access-Control-Allow-Origin','*')
      self.end_headers()

      # Write content as utf-8 data
      self.wfile.write(bytes(getFilledHTMLString(self.jsonDatas), "utf8"))
      return

def getFilledHTMLString(datas):
    print(os.getcwd())
    f = open("./analysis/demo.html", "r")
    HTMLPageStr = f.read()
    jsonDataStr = json.dumps(datas)
    return HTMLPageStr.replace("{/* THIS WILL BE REPLACED BY THE PYTHON OUTPUT */ }",jsonDataStr)


def getTrustExample():
    """
    An example of using text_trust.py. The test strings are the different
    texts of different versions. The test_trusts list is the different
    author_reputations of each version.
    """
    initial_trust = 1

    test_strings = []
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("foo the quick brown fox jumps over the lazy dog bar")
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("the lazy fox jumps over the quick brown dog")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff")

    test_trusts = [10, 7, 10, 20]

    trust_inheritance_const = 0.5
    revision_const = 0.1
    edge_effect_const = 2

    constants = (trust_inheritance_const, revision_const, edge_effect_const)

    print("Initial String: " + str(test_strings[0]))

    for string_iter, string in enumerate(test_strings):
        print("String %d: %s" %(string_iter, string))
    print()

    print("Version 1:\n")
    print("Initial Trust: " + str(initial_trust) + "\n")

    text_list = test_strings[0].split()

    version_list = []

    #ver = Version(word_list, edit_list, author_reputation, initial_trust, trust_inheritance_const, revision_const, edge_effect_const)
    ver = Version.create_initial_version(text_list, initial_trust, constants)

    version_list.append(ver)

    print("".join([str(word) for word in ver.word_list]) + "\n")

    print("Block List:")
    print("".join([str(block) + "\n" for block in ver.block_list]))

    print("\n")

    for string_iter in range(len(test_strings)-1):
        print("Version %d:\n" % (string_iter + 2))
        print("Author Reputation: %d\n" % (test_trusts[string_iter]))

        diff_list = test_tichy(test_strings[string_iter], test_strings[string_iter + 1])
        edit_list = [Edit.edit_tuple_constructor(edit) for edit in diff_list]
        text_list = test_strings[string_iter+1].split()

        ver = Version.create_next_version(ver, text_list, edit_list, test_trusts[string_iter])

        version_list.append(ver)

        print("".join([str(word) for word in ver.word_list]) + "\n")

        print("Block List:\n")
        print("".join([str(block) + "\n" for block in ver.block_list]))
        print("\n")

    return  version_list

def run(port=8080):

    print('starting server...')

    datas = []
    outputVersions = getTrustExample()
    for version in outputVersions:
        words = []
        for word in version.word_list:
            words.append(word.__dict__)
        datas.append(words)

    # Server settings
    # By default we use the localhost address (127.0.0.1) and the port 8080
    server_address = ('127.0.0.1', port)

    HTTP_RequestHandler.jsonDatas = datas # hacky but works
    httpd = HTTPServer(server_address,HTTP_RequestHandler)


    print('running server... - open your browser to: http://localhost:'+ str(port))
    httpd.serve_forever()

run()