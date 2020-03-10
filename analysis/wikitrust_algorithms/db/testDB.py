from controller import *

def main():
    updateAuthor(12345, 9)
    updateAuthor(12345, 10)
    updateAuthor(123, 1)
    createRevision(999, 1, 12345)
    createRevision(555, 1, 123)
    createRevision(444, 1, 123)
    createRevision(333, 1, 123)
    createRevision(222, 1, 123)
    createRevision(111, 1, 123)
    updateCache(999, 888, 10)
    print(getCache(999,888).distance)
    print(getAuthor(12345).rep)
    print(getAuthor(123).rep)

    x = getRevision(111)
    while x != None:
        print(x.revisionID)
        x = getNextRevision(x.revisionID)

if __name__ == "__main__":
    main()