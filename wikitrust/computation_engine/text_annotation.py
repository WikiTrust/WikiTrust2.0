import json
from datetime import datetime

from wikitrust_algorithms.text_trust.version import Version
from wikitrust_algorithms.text_trust.version import Block
from wikitrust_algorithms.text_trust.version import Word

from wikitrust_lib.text_diff.edit import Edit

__INITIAL_TRUST__ = 0

__TRUST_INHERITANCE_CONST__ = 0.5
__REVISION_CONST__ = 0.1
__EDGE_EFFECT_CONST__ = 2

__CONSTANTS__ = (__TRUST_INHERITANCE_CONST__, __REVISION_CONST__, __EDGE_EFFECT_CONST__)

class ReputationGenerator:
    def __init__(self, dbcontroller, text_storage_engine, trust_storage_engine, algorithm_ver, params):
        self.dbcontroller               = dbcontroller
        self.text_storage_engine        = text_storage_engine
        self.trust_storage_engine       = trust_storage_engine
        self.algorithm_ver              = algorithm_ver
        self.trust_inheritance_const    = params[0]
        self.revision_const             = params[1]
        self.edge_effect_const          = params[2]
        self.constants                  = (params[0], params[1], params[2])
        self.text_diff_function         = params[4]
        self.index_function             = params[5]


    def compute_revision_trust(self, rev_id):
        """
        Calculates the text trust of the passed revision_id.
        Assumesthe previous revision's trust has already been calculated.
        """

        page_id = self.dbcontroller.get_page_from_rev(rev_id)

        # Get previous revision and it's annotated text trust
        prev_rev_id = self.dbcontroller.get_prev_rev(rev_id)

        # Get previous text and trust values
        prev_text_json = json.loads(self.text_storage_engine.read(self.algorithm_ver, page_id, prev_rev_id))
        prev_text_vals = prev_text_json["text_list"]

        prev_trust_json = json.loads(self.trust_storage_engine.read(prev_rev_id, self.algorithm_ver))
        previus_trust_vals = prev_trust_json["trust_list"]

        #Gets new text from storage engine
        new_text_json = self.text_storage_engine.read(self.algorithm_ver, page_id, rev_id).split()
        new_text_vals = new_text_json["text_list"]

        #Gets author reputation
        new_rev_author_id = self.dbcontroller.get_user_from_rev(rev_id)
        author_rep = self.dbcontroller.get_reputation(self.algorithm_ver, new_rev_author_id)

        #Get Edits from previous to new revision
        edit_index= self.index_function(new_text_vals)
        edit_list_tuples = self.text_diff_function(prev_text_vals, new_text_vals, edit_index)

        #Converts list of tuples to list of Edits
        edit_list = [Edit.edit_tuple_constructor(edit_tuple) for edit_tuple in edit_list_tuples]

        prev_version = Version.create_version(prev_text_vals, previus_trust_vals, author_rep, self.constants)

        new_version = Version.create_next_version(prev_version, new_text_vals, edit_list, author_rep)

        new_trust = [word.trust for word in new_version.word_list]

        new_json = {"trust_list": new_trust}

        #Store new json in trust storage engine
        self.trust_storage_engine.store(self.algorithm_ver, page_id, rev_id, new_json, datetime.now())

        self.trust_storage_engine.flush(page_id)
