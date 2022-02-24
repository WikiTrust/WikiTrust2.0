import wikitrust_algorithms

from wikitrust_algorithms.author_reputation.author import Author
from wikitrust_algorithms.author_reputation.article import Article
from wikitrust_algorithms.author_reputation.version import Version as AuthorRepVersion

from wikitrust_algorithms.text_diff.chdiff import test_tichy
from wikitrust_algorithms.text_diff.edit import Edit

from wikitrust_algorithms.text_trust.version import Version as TextTrustVersion


import math
import sys
import time

__MAXREP__ = 100000

__TRUSTCONST__ = 1
__REVISIONCONST_ = 0.1
__EDGECONST__ = 2

__VERSIONCONST__ = (__TRUSTCONST__, __REVISIONCONST_, __EDGECONST__)

__MAXJUDGEDIST__ = 4
__SCALINGCONST__ = 0.01
__SCALINGFUNC__ = lambda x: math.log(1.1 + x)

def compute_demo(file_name):
    revision_list = create_revision_list(file_name)[::-1]

    author_table = create_author_table(revision_list)

    version_list = []

    initial_text = revision_list[0][2]

    initial_version = TextTrustVersion.create_initial_version(initial_text.split(), 0, __VERSIONCONST__)

    version_list.append(initial_version)

    initial_version_author_id = revision_list[0][1]
    initial_version_author = author_table[initial_version_author_id]

    print("Rev#" + str(0))
    print(revision_list[0][0])
    print(revision_list[0][1])
    print()


    article = Article(__MAXJUDGEDIST__, __SCALINGCONST__, __SCALINGFUNC__)

    article.add_new_version(AuthorRepVersion(initial_version_author, revision_list[0][2]))

    for version_iter in range(1, len(revision_list)):
        print("Rev #" + str(version_iter))
        print("Revision ID: " + str(revision_list[version_iter][0]))
        print("User ID: " + str(revision_list[version_iter][1]))
        print()

        old_text = revision_list[version_iter-1][2]
        new_text = revision_list[version_iter][2]

        version_author_id = revision_list[version_iter][1]
        version_author = author_table[version_author_id]
        version_author_rep = version_author.reputation

        diff_list = test_tichy(old_text, new_text)
        edit_list = [Edit.edit_tuple_constructor(edit) for edit in diff_list]
        text_list = new_text.split()

        prev_version = version_list[-1:][0]

        article.add_new_version(AuthorRepVersion(version_author, new_text))

        new_version = TextTrustVersion.create_next_version(prev_version, text_list, edit_list, version_author_rep)

        version_list.append(new_version)

    for author_id in author_table.keys():
        print(author_table[author_id])

    return version_list


def create_author_table(revision_list):
    author_id_list = [revision[1] for revision in revision_list]

    author_id_list = sorted(list(dict.fromkeys(author_id_list)))

    author_table = {}

    for author_id in author_id_list:
        author_table[author_id] = Author(author_id, 0, __MAXREP__)

    author_table[0].maximum_reputation = 0

    return author_table

def create_revision_list(json_data):

    #List of tuples (revision_id, user_id, text)
    revision_list = []

    for rev_num in range(json_data["size"]):
        revision_id = revision_text = json_data["revisions"][rev_num]["revisionId"]
        user_id = revision_text = json_data["revisions"][rev_num]["userId"]
        text = json_data["revisions"][rev_num]["text"]

        revision_list.append((revision_id, user_id, text))

    return revision_list

