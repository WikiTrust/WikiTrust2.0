from models import User, Cache, Revision, Block

"""
    Both creates new Authors and updates Rep of Author.
    :param authorID: Required, Int, ID of author to be created or updated
    :param rep: Not Required, Float, Default = 0, Updates Rep of Author
"""
def updateAuthor(authorID, rep=0):
    try:
        user = User.objects.get(authorID=authorID)
        user.rep = rep
        user.save()
        return user
    except User.DoesNotExist:
        newUser = User(authorID=authorID, rep=rep)
        newUser.save()
        return newUser

"""
    Creates and Updates Cache
    :param revID1: Required, Int, first Revision ID
    :param revID2: Required, Int, second Revision ID
    :param distance: Required, Float, Distance between rev_1 and rev_2
"""
def updateCache(revID1, revID2, distance):
    rev_1 = Revision.objects.get(revisionID=revID1).to_dbref()
    rev_2 = Revision.objects.get(revisionID=revID2).to_dbref()
    try:
        cache = Cache.objects.get(rev_1 = rev_1, rev_2 = rev_2)
        cache.distance = distance
        cache.save()
    except Cache.DoesNotExist:
        cache = Cache(rev_1=rev_1, rev_2=rev_2, distance=distance)
        cache.save()

"""
    Creates a new Revision. If the Revision exists does nothing.
    :param revID: Required, Int, Revision ID
    :param pageID: Required, Int, Page ID
    :param authorID: Required, Int, Author ID
"""
def createRevision(revID, pageID, authorID):
    user = getAuthor(authorID)
    try:
        Revision.objects.get(revisionID=revID)
    except Revision.DoesNotExist:
        rev = Revision(author=user, revisionID=revID, pageID=pageID)
        rev.save()

"""
    Given 2 Revision ID's finds the cache
    :param revID1: Required, Int, First Revision ID
    :param revID2: Required, Int, Second Revision ID
    :return cache: Cache Object
    :return None: None
"""
def getCache(revID1, revID2):
    rev_1 = getRevision(revID1).to_dbref()
    rev_2 = getRevision(revID2).to_dbref()
    try: 
        cache = Cache.objects.get(rev_1=rev_1, rev_2=rev_2)
        return cache
    except Cache.DoesNotExist:
        return None

"""
    Returns Author or creates an Author with rep 0 if not found
    :param authorID: Required, Int, Author ID
    :return: User Object
"""
def getAuthor(authorID):
    try:
        return User.objects.get(authorID=authorID)
    except User.DoesNotExist:
        newUser = User(authorID=authorID, rep=0)
        newUser.save()
        return newUser

"""
    Given a Revision ID returns Revision
    :param revID: Required, Int, Revision ID
    :return revision: Revision Object
    :return None: None
"""
def getRevision(revID):
    try: 
        rev = Revision.objects.get(revisionID=revID)
        return rev
    except Revision.DoesNotExist:
        return None

"""
    Given a Revision ID returns next Revision in ascending order
    :param revID: Required, Int, Revision ID
    :return revision: Next Revision
    :return None: None
"""
def getNextRevision(revID):
    rev = Revision.objects(revisionID__gt=revID).order_by('+revisionID')[:1]
    if(rev.count() != 0):
        return rev[0]
    else:
        return None