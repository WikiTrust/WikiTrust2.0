from datetime import datetime
import pywikibot
import wikitrust_py.revision_puller.RevisionPuller as WikiRevPuller
import wikitrust_py.revision_puller.SearchEngine as WikiSearchEngine
import wikitrust_py.revision_puller.PageProcessor as WikiPageProcessor

engine = WikiSearchEngine.SearchEngine()
processor = WikiPageProcessor.PageProcessor()


def get_readable_text_of_old_revision(page_title: str, rev_id: int):
    """
    Returns a string containing a "readable" version of a revision
    :param page_title: A string of the page title
    :param rev_id: The revision number of the desired revision
    :return: A string of the revision's readable text
    """
    page = engine.search(page_title, 1, "nearmatch")[0]
    return processor.getReadableText(
        WikiRevPuller.get_text_of_old_revision(page, rev_id)
    )


def get_revisions(
    page_title: str,
    recent_to_oldest: bool = True,
    num_revisions=None,
    start_time: pywikibot.Timestamp = None,
    end_time: pywikibot.Timestamp = None
):
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
    return WikiRevPuller.get_latest_revisions(
        page,
        recent_to_oldest=recent_to_oldest,
        num_revisions=num_revisions,
        start_time=start_time,
        end_time=end_time
    )


def get_rev_id(rev: pywikibot.page.Revision):
    """
    Gets the revision id of a revision
    :param rev: The revision object
    :return: An integer corresponding to the revision id
    """
    return WikiRevPuller.getRevisionMetadata(rev, "revid")


#TODO: Update this to be better about  ignoring already inerted revisions
def tranform_pywikibot_revision_list_into_rev_table_schema_dicts(
    revision_list: list[pywikibot.page.Revision], page_id
):
    """
    Outputs a list of revision dicts matching the revision table db schema columns
    :param rev: The pywikibot revisions to process
    :param page: The pywikibot page corresponding to these
    :return: the page revision objects outputed as a list of dicts matching the revision table db schema columns
    """
    rev_count = len(revision_list)
    rev_table_rows = []
    # convert revisions into table format

    for i, rev_object in enumerate(revision_list):
        prev_id = get_rev_id(revision_list[i - 1]) if i > 0 else None
        next_id = get_rev_id(
            revision_list[i + 1]
        ) if i < rev_count - 1 else None
        rev_table_row = convert_rev_to_table_row(
            rev_object, page_id, i, prev_id, next_id
        )
        rev_table_rows.append(rev_table_row)
    return rev_table_rows


#TODO: UPdate this to be better about keeping track of attempts
def convert_rev_to_table_row(
    rev: pywikibot.page.Revision, page_id: int, rev_idx: int, prev_rev_id: int,
    next_rev_id: int
):
    """
    Outputs the revision dict matching the revision table db schema columns
    :param rev: The pywikibot revision to process
    :param page: The pywikibot page corresponding to this revision
    :return: the page revision object outputed as a dict matching the revision table db schema columns
    """
    return {
        "page_id":
            page_id,
        "rev_id":
            WikiRevPuller.getRevisionMetadata(rev, "revid"),
        "user_id":
            WikiRevPuller.getRevisionMetadata(rev, "userid"),
        "rev_date":
            datetime.fromtimestamp(
                WikiRevPuller.getRevisionMetadata(rev, "timestamp").timestamp()
            ),
        'next_rev':
            next_rev_id,
        'prev_rev':
            prev_rev_id,
        'rev_idx':
            rev_idx,
        'text_retrieved':
            True,  #######!!!!!!!!!!!!!! this is wrong at this stage, this should be updated when the wikipedia page's text is actually retrived
        'last_attempt_date':
            datetime.now(),
        'num_attempts':
            0.
    }
