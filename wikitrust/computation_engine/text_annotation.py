import json
from datetime import datetime

from wikitrust_algorithms.text_trust.version import Version
from wikitrust_algorithms.text_trust.version import Block
from wikitrust_algorithms.text_trust.version import Word

__ALGORITHM_VER__ = "TEXT_ANNOTATION_DEV"

__INITIAL_TRUST__ = 0

__TRUST_INHERITANCE_CONST__ = 0.5
__REVISION_CONST__ = 0.1
__EDGE_EFFECT_CONST__ = 2

__CONSTANTS__ = (__TRUST_INHERITANCE_CONST__, __REVISION_CONST__, __EDGE_EFFECT_CONST__)

def compute_revision_trust(rev_id, db, revision_storage_engine, trust_storage_engine):
    """
    Calculates the text trust of the passed revision_id.
    Assumesthe previous revision's trust has already been calculated.
    """

    # Asserts that all the triangles with this revision in the
    # most recent position have a reputation_inc not None.
    target_triangles = db(db.triangles.revid_3 == rev_id).iterselect()

    for target_triangle in target_triangles:
        assert target_triangle.reputation_inc is not None #Consider changing to empty return?

    # Get previous revision and it's annotated text trust
    target_revision = db(db.revision.rev_id == rev_id).select()

    assert len(target_revision) == 1

    page_id = target_revision[0].page_id
    prev_revision_id = target_revision[0].prev_revision

    # Assume JSON has the structure [word_list: [], trust_list: []]
    previous_annotated_text = json.loads(trust_storage_engine.read(prev_revision_id, __ALGORITHM_VER__, page_id))

    previous_text = previous_annotated_text["word_list"]
    previus_trust = previous_annotated_text["trust_list"]

    #Gets new text from storage engine
    new_text = revision_storage_engine.read(page_id, __ALGORITHM_VER__, rev_id).split()

    #Gets author reputation
    user_reputation = db(db.user_reputation.user_id == target_revision.user_id).select()

    assert len(user_reputation) == 1

    author_reputation = user_reputation[0]

    new_version = Version.create_version(previous_text, previus_trust, author_reputation, __CONSTANTS__)

    new_trust = [word.trust for word in new_version.word_list]

    new_json = {"word_list": new_text, "trust_list": new_trust}

    trust_storage_engine.store(page_id, __ALGORITHM_VER__, rev_id, new_json, datetime.now())

    trust_storage_engine.flush()