import datetime
import pywikibot
import SearchEngine as SE


def get_latest_revisions(page:pywikibot.page.Page, recent_to_oldest:bool=True, num_revisions=None, start_time:pywikibot.Timestamp=None, end_time:pywikibot.Timestamp=None):
    """
    Returns the last (num_revisions) revisions from a given Wikipedia page
    If all revisions are desired use: get_latest_revisions(page)
    :param page: A pywikibot.Page object that we want to grab the the revisions for
    :param recent_to_oldest: Set to false if we want the revisions in order of oldest to most recent
    :param num_revisions: The number of revisions to be grabbed (set to an integer to set limit to number of revisions grabbed)
    :param start_time: A timestamp corresponding to the oldest revision we want to grab
    :param end_time: A timestamp corresponding to the most recent revision we want to grab
    :return: A list of pywikibot.page.Revision objects (dictionaries that store revisions by revid, text changed, timestamp, user, and comment)
             Note that revisions starting earlier will be towards the end of the list
    """
    return list(page.revisions(reverse=not recent_to_oldest, total=num_revisions, starttime=start_time, endtime=end_time))

def get_revisions_between(page:pywikibot.page.Page, revision1:pywikibot.page.Revision, revision2:pywikibot.page.Revision, recent_to_oldest=True):
    """
    Returns all of the revisions between two revisions from a given Wikipedia page
    :param page: A pywikibot.Page object that we want to grab the the revisions for
    :param recent_to_oldest: Set to false if we want the revisions in order of oldest to most recent
    :param revision1: The first revision of the page
    :param revision2: The second revision of the page
    :return: A list of pywikibot.page.Revision objects (dictionaries that store revisions by revid, text changed, timestamp, user, and comment)
             Note that revisions starting earlier will be towards the end of the list
    """
    firstRevTime = getRevisionMetadata(revision1, "timestamp")
    secondRevTime = getRevisionMetadata(revision2, "timestamp")
    if(recent_to_oldest and firstRevTime <= secondRevTime):
        raise ValueError("Second revision must occur before first revision if sorting by recent to oldest")
    elif(not recent_to_oldest and firstRevTime >= secondRevTime):
        raise ValueError("First revision must occur before second revision if sorting by oldest to recent")
    return get_latest_revisions(page, recent_to_oldest, start_time=firstRevTime, end_time=secondRevTime)


def get_text_of_old_revision(page:pywikibot.page.Page, rev_id:int):
    """
    Returns the WikiText of a page from a specific revision
    :param page: A pywikibot.Page object that we want to return the text for
    :param rev_id: The revision id corresponding to the revision of the page that we want to extract the text based on
    :return: A string of WikiText containing the text of a page after the revision
    """
    return page.getOldVersion(rev_id)


def getRevisionMetadata(revision:pywikibot.page.Revision, key:str):
    """
    Returns a piece of metadata associated with a revision
    :param key: A string that corresponds to a valid piece of metadata associated with a revision
                Valid inputs: comment, revid, timestamp, user, rollbacktoken
    :return: The desired metadata as a string
    """
    return revision[key]