"""
This file contains an example of how one would use the text_trust package.

Eric Vin, 2019
"""

from text_trust.version import Version
from text_trust.block import Block
from text_trust.edit import Edit
from text_trust.word import Word

from chdiff import test_tichy, test_greedy, print_edit_diff

if __name__ == '__main__':
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

    ver = Version.create_initial_version(text_list, initial_trust, constants)

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

        print("".join([str(word) for word in ver.word_list]) + "\n")

        print("Block List:\n")
        print("".join([str(block) + "\n" for block in ver.block_list]))
        print("\n")
