import json
from datetime import datetime

from wikitrust_algorithms.text_trust.version import Version
from wikitrust_algorithms.text_trust.version import Block
from wikitrust_algorithms.text_trust.version import Word

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

    def compute_revision_trust(self, rev_id):
        """
        Calculates the text trust of the passed revision_id.
        Assumesthe previous revision's trust has already been calculated.
        """

        # Get previous revision and it's annotated text trust
        target_revision = self.dbcontroller.get_prev_rev(rev_id)

        page_id = target_revision[0].page_id
        prev_revision_id = target_revision[0].prev_revision

        # Assume JSON has the structure [word_list: [], trust_list: []]
        previous_annotated_text = json.loads(self.trust_storage_engine.read(prev_revision_id, self.algorithm_ver, page_id))

        previous_text = previous_annotated_text["word_list"]
        previus_trust = previous_annotated_text["trust_list"]

        #Gets new text from storage engine
        new_text = self.text_storage_engine.read(page_id, self.algorithm_ver, rev_id).split()

        #Gets author reputation
        user_reputation = self.dbcontroller.get_reputation()

        assert len(user_reputation) == 1

        author_reputation = user_reputation[0]

        new_version = Version.create_version(previous_text, previus_trust, author_reputation, __CONSTANTS__)

        new_trust = [word.trust for word in new_version.word_list]

        new_json = {"word_list": new_text, "trust_list": new_trust}

        self.trust_storage_engine.store(page_id, self.algorithm_ver, rev_id, new_json, datetime.now())

        self.trust_storage_engine.flush()