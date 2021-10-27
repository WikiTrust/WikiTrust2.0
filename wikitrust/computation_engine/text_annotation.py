import json
from datetime import datetime

from wikitrust.computation_engine.wikitrust_algorithms.text_trust.version import Version
from wikitrust.computation_engine.wikitrust_algorithms.text_trust.block import Block
from wikitrust.computation_engine.wikitrust_algorithms.text_trust.word import Word

from wikitrust.computation_engine.wikitrust_algorithms.text_diff.edit import Edit

__INITIAL_TRUST__ = 0

__TRUST_INHERITANCE_CONST__ = 0.5
__REVISION_CONST__ = 0.1
__EDGE_EFFECT_CONST__ = 2

__CONSTANTS__ = (
    __TRUST_INHERITANCE_CONST__, __REVISION_CONST__, __EDGE_EFFECT_CONST__
)


class TextAnnotation:
    def __init__(
        self, dbcontroller, text_storage_engine, trust_storage_engine,
        algorithm_ver, params
    ):
        self.dbcontroller = dbcontroller
        self.text_storage_engine = text_storage_engine
        self.trust_storage_engine = trust_storage_engine
        self.algorithm_ver = algorithm_ver
        self.trust_inheritance_const = params[0]
        self.revision_const = params[1]
        self.edge_effect_const = params[2]
        self.constants = (params[0], params[1], params[2])
        self.text_diff_function = params[3]
        self.index_function = params[4]

    def compute_revision_trust(self, rev_id):
        """
        Calculates the text trust of the passed revision_id.
        Assumesthe previous revision's trust has already been calculated.
        """

        page_id = self.dbcontroller.get_page_from_rev(rev_id)
        env_id = self.dbcontroller.get_environment_by_page_id(page_id)

        # Get previous revision and it's annotated text trust
        prev_rev_id = self.dbcontroller.get_prev_rev(rev_id)

        if prev_rev_id == None:
            #First revision, so previous text and trust lists are empty
            prev_text_vals = []
            prev_trust_vals = []
        else:
            # Get previous text and trust values from storage engine
            prev_text_vals = json.loads(
                self.text_storage_engine.read(page_id, prev_rev_id)
            )

            prev_trust_vals = json.loads(
                self.trust_storage_engine.read(page_id, prev_rev_id)
            )

        #Gets new text from storage engine
        new_text_vals = json.loads(
            self.text_storage_engine.read(page_id, rev_id)
        )

        #Gets author reputation
        new_rev_author_id = self.dbcontroller.get_user_from_rev(rev_id)
        author_rep = self.dbcontroller.get_reputation(
            self.algorithm_ver, new_rev_author_id, env_id
        )

        #Get Edits from previous to new revision
        edit_index = self.index_function(new_text_vals)
        edit_list_tuples = self.text_diff_function(
            prev_text_vals, new_text_vals, edit_index
        )

        #Converts list of tuples to list of Edits
        edit_list = [
            Edit.edit_tuple_constructor(edit_tuple)
            for edit_tuple in edit_list_tuples
        ]

        prev_version = Version.create_version(
            prev_text_vals, prev_trust_vals, author_rep, self.constants
        )

        new_version = Version.create_next_version(
            prev_version, new_text_vals, edit_list, author_rep
        )

        new_trust = [word.trust for word in new_version.word_list]

        new_json = json.dumps(new_trust)

        #Store new json in trust storage engine
        print("Storing Trust Values in GCS:", page_id, rev_id)
        self.trust_storage_engine.store(
            page_id, rev_id, new_json, datetime.now()
        )

        self.trust_storage_engine.flush()
