import pywikibot
import RevisionPuller as RP
import SearchEngine as SE
import PageProcessor as PP

engine = SE.SearchEngine()
processor = PP.PageProcessor()



def get_readable_text_of_old_revision(page_title:str, rev_id:int):
    """
    Returns a string containing a "readable" version of a revision
    :param page_title: A string of the page title
    :param rev_id: The revision number of the desired revision
    :return: A string of the revision's readable text
    """
    page = engine.search(page_title, 1, "nearmatch")[0]
    return processor.getReadableText(RP.get_text_of_old_revision(page, rev_id))

def get_revisions(page_title:str, recent_to_oldest:bool=True, num_revisions=None, start_time:pywikibot.Timestamp=None, end_time:pywikibot.Timestamp=None):
    """
    Returns the last (num_revisions) revisions from a given Wikipedia page
    If all revisions are desired use: get_latest_revisions(page)
    :param page_title: A string containing the title of the desired page
    :param recent_to_oldest: Set to false if we want the revisions in order of oldest to most recent
    :param num_revisions: The number of revisions to be grabbed (set to an integer to set limit to number of revisions grabbed)
    :param start_time: A timestamp corresponding to the oldest revision we want to grab
    :param end_time: A timestamp corresponding to the most recent revision we want to grab
    :return: A list of pywikibot.page.Revision objects (dictionaries that store revisions by revid, text changed, timestamp, user, and comment)
             Note that revisions starting earlier will be towards the end of the list
    """
    page = engine.search(page_title, 1, "nearmatch")[0]
    return RP.get_latest_revisions(page, recent_to_oldest=recent_to_oldest, num_revisions=num_revisions, start_time=start_time, end_time=end_time)

def get_rev_id(rev:pywikibot.page.Revision):
    """
    Gets the revision id of a revision
    :param rev: The revision object
    :return: An integer corresponding to the revision id
    """
    return RP.getRevisionMetadata(rev, "revid")
