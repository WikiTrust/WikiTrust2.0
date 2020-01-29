from author_reputation.article import Article
from author_reputation.version import Version
from author_reputation.author import Author
from author_reputation.edit import Edit

import math

def simple_test():
    test_strings = []
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("foo the quick brown fox jumps over the lazy dog bar")
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("the lazy fox jumps over the quick brown dog")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff")
    test_strings.append("i am a vandal")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff cats and dogs")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff cats and dogs with zebras or lions")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff cats and dogs with zebras or lions but not artichokes")

    test_authors = []
    test_authors.append(Author(1, 0))
    test_authors.append(Author(2, 0))
    test_authors.append(Author(3, 0))
    test_authors.append(Author(4, 0))
    test_authors.append(Author(5, 0))
    test_authors.append(Author(6, 0))
    test_authors.append(Author(7, 0))
    test_authors.append(Author(8, 0))
    test_authors.append(Author(9, 0))
    test_authors.append(Author(10, 0))

    test_versions = []

    for version_iter in range(len(test_authors)):
        test_versions.append(Version(test_authors[version_iter], test_strings[version_iter]))

    max_judgement_dist = 4
    scaling_constant = 1
    scaling_function = lambda x: math.log(1.1 + x)

    test_article = Article(max_judgement_dist, scaling_constant, scaling_function)

    for x in range(1):
        for version_iter, version in enumerate(test_versions):
            print("Loop %d:\n" % version_iter)

            print("Author Status:")
            for author in test_authors:
                print(str(author))
            print()

            print("Adding Version...")
            print(str(version))
            test_article.add_new_version(version)

def medium_test():
    test_strings = []
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("foo the quick brown fox jumps over the lazy dog bar")
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("the lazy fox jumps over the quick brown dog")
    test_strings.append("the lazy fox jumps over the quick and also other stuff")
    test_strings.append("i am a vandal")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff cats and dogs")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff cats and dogs with zebras or lions")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff cats and dogs with zebras or lions but not artichokes")

    authors_list = []

    author_1 = Author(1, 0)
    author_2 = Author(2, 0)
    author_3 = Author(3, 0)

    authors_list.append(author_1)
    authors_list.append(author_2)
    authors_list.append(author_3)

    test_authors = []
    test_authors.append(author_1)
    test_authors.append(author_2)
    test_authors.append(author_3)
    test_authors.append(author_1)
    test_authors.append(author_3)
    test_authors.append(author_2)
    test_authors.append(author_1)
    test_authors.append(author_3)
    test_authors.append(author_1)
    test_authors.append(author_3)

    test_versions = []

    for version_iter in range(len(test_authors)):
        test_versions.append(Version(test_authors[version_iter], test_strings[version_iter]))

    max_judgement_dist = 4
    scaling_constant = 1
    scaling_function = lambda x: math.log(1.1 + x)

    test_article = Article(max_judgement_dist, scaling_constant, scaling_function)

    for x in range(1):
        for version_iter, version in enumerate(test_versions):
            print("Loop %d:\n" % version_iter)

            print("Author Status:")
            for author in authors_list:
                print(str(author))
            print()

            print("Adding Version...")
            print(str(version))
            test_article.add_new_version(version)

if __name__ == '__main__':
    from sys import path
    from os.path import dirname as dir

    print(path)

    path.append(dir(path[0]))

    medium_test()