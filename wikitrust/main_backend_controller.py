import json, math
from datetime import datetime

import pywikibot

# For revision puller
from wikitrust.database.controllers.revision_puller_db_controller import revsion_puller_db_controller
from wikitrust.revision_puller.RevisionsWrapper import convert_rev_to_table_row, get_rev_id, tranform_pywikibot_revision_list_into_rev_table_schema_dicts
import wikitrust.revision_puller.SearchEngine as WikiSearchEngine
import wikitrust.revision_puller.RevisionPuller as WikiRevPuller
import wikitrust.revision_puller.PageProcessor as WikiPageProcessor
# for computation engine
from wikitrust.database.controllers.computation_engine_db_controller import computation_engine_db_controller
from wikitrust.computation_engine.triangle_generator import TriangleGenerator
from wikitrust.computation_engine.reputation_generator import ReputationGenerator
from wikitrust.computation_engine.text_annotation import TextAnnotation
import wikitrust.computation_engine.wikitrust_algorithms.text_diff.chdiff as chdiff


class main_backend_controller:
    def __init__(self, db, revStore, textTrustStore):

        # get references to the storage engines
        self.revStore = revStore
        self.textTrustStore = textTrustStore

        # initialize the db controllers
        self.compute_db_ctrl = computation_engine_db_controller(db)
        self.rev_puller_db_ctrl = revsion_puller_db_controller(db)

        # Initilize page / revision pulller tools:
        self.wikiSearchEngine = WikiSearchEngine.SearchEngine()
        self.wikiPageProcessor = WikiPageProcessor.PageProcessor()

        # initilize compoutation engine tools:
        self.compute_db_filler = self.compute_db_ctrl.create_entry

    def __enter__(self):
        """
        Used for returning self for "with" statement
        """
        return self

    def __exit__(
        self, exec_type, exec_value, traceback
    ):  # other params available: exec_type, exec_value, traceback
        """
        Used for cleaning up on "with" statement exit
        """
        self.revStore.__exit__()
        self.textTrustStore.__exit__()

    def find_page(self, search_term) -> pywikibot.page:
        """ Returns a pywikibot page reference for a given search term string or None? """
        return self.wikiSearchEngine.search(
            search_term, max_pages_grabbed=1, search_by="nearmatch"
        )[0]

    def find_page_by_id(self, page_id) -> pywikibot.page:
        """ Returns the pywikibot page reference with a given id or None? """
        return self.WikiSearchEngine.getByPageID(page_id)

    def get_or_create_wiki_environment(self, environment_name: str):
        """
        Finds an existing or Creates a new environment (aka a category like physiscs or biology that can be used to
        group wiki authors with expertiese in one category, so their user reputations can be computed per category)
        """
        environment = self.compute_db_ctrl.get_environment_by_name(
            environment_name
        )
        if environment is None:
            return self.compute_db_filler.create_environment(environment_name)
        else:
            return environment

    def pull_page_into_db(self, pyWiki_Page, page_environment):
        """
        Pulls the given pywikibot page details and adds the revisions of said page to revisions table in db
        ***** Does NOT ****  add page text to the storage engine
        returns the list of pywikibot revisions from the page
        """
        ## TODO: only pull revisions that are not already in the db

        current_page_id = pyWiki_Page.pageid
        print("Pulling page ", pyWiki_Page.title, " with ID:", current_page_id)

        # get all revisions for that page
        all_revisions = WikiRevPuller.get_all_revisions(
            pyWiki_Page, recent_to_oldest=False
        )

        # convert revisions to the revision table db schema and load them into the db:
        rev_table_row_dicts = tranform_pywikibot_revision_list_into_rev_table_schema_dicts(
            all_revisions, current_page_id
        )
        self.rev_puller_db_ctrl.insert_revisions(rev_table_row_dicts)

        # Populate the tables neccesary for the compute engine to process this page

        self.compute_db_filler.create_page(
            page_id=current_page_id,
            environment_id=page_environment,
            page_title=pyWiki_Page.title,
            last_check_time=None
        )
        self.compute_db_filler.create_revision_log(
            __ALGORITHM_VER__, None, page_id=current_page_id
        )

    def process_page(
        self, pyWiki_Page: pywikibot.page, page_environment, page_revisions
    ):
        """
        Processes the given page by pulling all of the wikitext for all revisions, striping each revision to a list of words, running the algos and adding the trust results & revision words to the cloud storage.
        param page_revisions: list(pywikibot page revision)
        param page_environment: str?? - or evnironment table db row?
        """
        #TODO: only process pages & revisions that are new to us / haven't been processed before.

        current_page_id = pyWiki_Page.pageid

        all_revisions_text = []
        for revision in page_revisions:
            rev_id = WikiRevPuller.getRevisionMetadata(revision, "revid")
            rev_user_id = WikiRevPuller.getRevisionMetadata(revision, "userid")
            rev_text = self.wikiPageProcessor.getReadableText(
                WikiRevPuller.get_text_of_old_revision(pyWiki_Page, rev_id)
            )

            #convert text to a json encoded array of words (by splitting revison text on whitespace)
            rev_text = json.dumps(rev_text.split())

            # store the cleaned word array in all_revisions_text array and in the storage engine (meaning: google clound sstorage in bundles)
            all_revisions_text.append(rev_text)
            self.revStore.store(
                page_id=current_page_id,
                rev_id=rev_id,
                text=rev_text,
                timestamp=datetime.now()
            )

            # now append revision metadata to the computation relevant tables?
            self.compute_db_filler.create_revision(
                rev_id, current_page_id, rev_user_id
            )
            self.compute_db_filler.create_user(rev_user_id)
            self.compute_db_filler.create_user_reputation(
                __ALGORITHM_VER__, rev_user_id, page_environment
            )

            # fake text trusts array and store in texttrusts var and in the storage engine (meaning: google clound sstorage in bundles)
            # texttrusts = []
            # for word in rev_text.split():
            #     texttrusts.append(len(word))
            # textTrustStore.store(page_id=current_page_id, rev_id=rev_id, text=json.dumps(texttrusts),timestamp=datetime.now())
            #Run Triangle generator

            print("Starting Triangle Generator...")
            tg = TriangleGenerator(
                self.compute_db_ctrl, self.revStore, __ALGORITHM_VER__,
                (3, chdiff.edit_diff_greedy, chdiff.make_index2)
            )
            tg.compute_triangles_batch(current_page_id)
            print("Triangle Generator done\n")

            #Run Reputation generator
            print("Starting Reputation Generator...")
            rg = ReputationGenerator(
                self.compute_db_ctrl, __ALGORITHM_VER__,
                (0.5, (lambda x: math.log(1.1 + x)))
            )
            rg.update_author_reputation()
            print("Reputation Generator done\n")

            #Run Text Annotation on each revision
            print("Running Text Annotation...")
            ta = TextAnnotation(
                self.compute_db_ctrl, self.revStore, self.textTrustStore,
                __ALGORITHM_VER__,
                (0.5, 0.5, 5, chdiff.edit_diff_greedy, chdiff.make_index2)
            )

            all_rev_ids = self.compute_db_ctrl.get_all_revisions(
                current_page_id
            )
            for revision_id in all_rev_ids:  # this all_revisions list must be sorted. (from oldest to newest. which I think it is already?)
                ta.compute_revision_trust(revision_id)

            print("Text Annotation done \n")

        print("flush writing to storage engines....")
        self.textTrustStore.flush()
        self.revStore.flush()

        print("Done. Revision and Text Reputation are saved to storage & db")
