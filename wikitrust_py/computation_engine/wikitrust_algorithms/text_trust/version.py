"""
Module containing Version class. Part of the text_trust package.

Eric Vin, 2019-2020
"""

#Standard library imports
import math
from typing import List, Tuple

#text_trust package imports
from .block import Block
from .word import Word

#text_diff package imports
from wikitrust_py.computation_engine.wikitrust_algorithms.text_diff.edit import Edit


class Version:
    """
    Class representing one version of an article at a certain point in time.
    """
    def __init__(self, word_list: List[Word], edit_list: List[Edit], author_rep: float, \
                 constants: Tuple[float, float, float]) \
                 -> None:
        """
        Version Constructor:
            -words: A list of Words present in this Version
            -edit_list: A list of Edits that map the previous Version
                to this Version.
            -author_rep: The reputation of the author who made the
                edits in edit_list
            -constants: A tuple containing, in order, the trust inheritance
                constant, the revision constant, and the edge effect constant.

            **NOTE**
            This constructor should only be used by the factory methods create_initial_version
            and create_next_version.
        """

        #A list of words present in this Version
        self.word_list: List[Word] = word_list

        #A list of edits that brought the previous version to the current version
        self.edit_list: List[Edit] = edit_list

        #The reputation of the author who made the edits in edit_list
        self.author_rep: float = author_rep

        #The constants used in trust calculations
        self.constants = constants

        #Unpacks constants into their own variables for more intuitive access
        self.trust_inheritance_const: float = constants[0]
        self.revision_const: float = constants[1]
        self.edge_effect_const: float = constants[2]

        #A list of blocks contained in this version
        self.block_list: List[Block] = self.compute_blocks()

        #Calculates the trust of all inserted blocks
        self.apply_insertion_trust()

        #Checks if bounds of any blocks have changed contexts
        self.check_block_bound_changes()

        #Applies the edge effect to all block bounds that have changed context
        self.apply_edge_effect()

        #Applies the revision effect to all words
        self.apply_revision_effect()

    @classmethod
    def create_initial_version(cls, text_list: List[str], initial_trust: float, \
                               constants: Tuple[float, float, float]) -> "Version":
        """
        This is a factory method to create an initial Version of a page
        given a starting list of words. This is structured as an insertion
        containing all words in a word_list with the author reputation
        being the initial_trust passed.

        create_initial_version Parameters:
            -text_list: A list of strings representing all words in this Version.
            -initial_trust: A float representing the initial trust for all words
                in this Version.
            -constants: A tuple containing, in order, the trust inheritance
                constant, the revision constant, and the edge effect constant.
        """

        #Creates list of Word objects all with trust equal to initial_trust.
        word_list: List[Word] = Word.create_list_words(text_list,\
                                [initial_trust for x in range(len(text_list))])

        #Creates edit_list with one edit: A move of all text in text_list from
        #zero to zero
        edit_list = [Edit(Edit.MOVE, 0, 0, len(word_list))]

        return cls(word_list, edit_list, initial_trust, constants)

    @classmethod
    def create_version(cls, text_list: List[str], trust_list: List[float], \
                       author_rep: float, constants: Tuple[float, float, float]) -> "Version":

        new_version = cls.create_initial_version(text_list, 0.0, constants)

        #Creates list of Word objects all with trust equal to initial_trust.
        word_list: List[Word] = Word.create_list_words(text_list, trust_list)

        new_version.word_list = word_list

        return new_version

    @classmethod
    def create_next_version(cls, prev_version: "Version", new_text: List[str], \
        new_edits: List[Edit], author_rep: float) -> "Version":
        """
        This is a factory method to create and return the next Version, given a previous
        Version, a list of edits applied to that previous Version and the words present in
        the next version.

        create_next_version Parameters:
            -prev_version: The version immediately before the new version being generated
                by this method.
            -new_text: A list of strings representing all words in the the new version.
            -new_edits: A list of edits mapping the old version to the new version.
            -author_rep: The reputation of the author making the edits in this new version.
        """

        #Creates reference to Word list of previous version.
        prev_word_list: List[Word] = prev_version.word_list

        #Creates new Word list based off new_text. All trusts are set
        #to -1 initially to help detect if a word's trust is not properly
        #set later. (Trust should never be negative after object construction
        #is finished)
        new_word_list: List[Word] = Word.create_list_words(new_text, \
                                    [-1 for x in range(len(new_text))])

        #Copies trust from words involved in moves.
        #They assume the same trust they had in the previous version
        for edit in new_edits:
            #Only applies copy if edit is a move
            if edit.edit_type == Edit.MOVE:
                #Copies over a clone of all words in move from edit origin
                #in prev_word_list to edit destination in new_word_list,
                #scaled by word_iter
                for word_iter in range(edit.length):
                    new_word_list[edit.destination+word_iter] = \
                        prev_word_list[edit.origin+word_iter].clone()

        #Creates and returns the next version
        return cls(new_word_list, new_edits, author_rep, prev_version.constants)

    def compute_blocks(self) -> List[Block]:
        """
        Computes a list of Blocks from this Version's words and edit_list
        """

        #Gets all edits with a destination in the current version, i.e. they
        #are present in this version (e.g. Moves and Inserts)
        present_edits: List[Edit] = [
            edit for edit in self.edit_list if edit.destination >= 0
        ]

        #Sorts edits by destination in ascending order
        present_edits = sorted(present_edits, key=lambda edit: edit.destination)

        #Creates a list of blocks in order from the present_edits
        version_blocks: List[Block] = []

        #Each block is made of an edit and its associated text. The associated
        #text comes from the Version words list. The start is the edit's destination
        #and the end is the destination+length
        for edit in present_edits:
            start_words: int = edit.destination
            end_words: int = start_words + edit.length
            version_blocks.append(
                Block(self.word_list[start_words:end_words], edit)
            )

        return version_blocks

    def apply_insertion_trust(self) -> None:
        """
        Applies the trust calculations for an insertion to all insertion blocks
        in this version.
        """
        #Iterates through every block in this version
        for block in self.block_list:
            #Checks if this block is an insertion
            if block.edit.edit_type == Edit.INSERT:
                #This block is an insertion, so we apply the insertion trust formula
                #to each word in it
                for word in block.words:
                    word.trust = (
                        self.author_rep * self.trust_inheritance_const
                    )

    def check_block_bound_changes(self) -> None:
        """
        Iterates through every block in the block_list to check if their bounds
        have changed context.

        Current implementation conforms to "Assigning Trust to Wikipedia Content"
        model. ALL Moves have the edge effect applied to them with two exceptions:

            -If the Move starts at the beginning of the article both before and after
             the edit, then the left bound does not change context.
            -If the Move ends at the end of the article both before and after the edit,
             then the right bound does not change context.
        """
        for block in self.block_list:
            #Checks if block edit type is move
            if block.edit.edit_type == Edit.MOVE:
                #Checks if left bound has changed context
                if (block.edit.origin == block.edit.destination
                   ) and (block.edit.destination == 0):
                    block.left_bound_change = False
                else:
                    block.left_bound_change = True

                #Checks if right bound has changed context
                if (block.edit.origin == block.edit.destination) and \
                   (block.edit.destination == len(self.word_list)-block.edit.length):
                    block.right_bound_change = False
                else:
                    block.right_bound_change = True

    def apply_edge_effect(self) -> None:
        """
        Applies the edge effect to all block bounds marked as changed by the
        check_block_bound_changes function
        """
        for block in self.block_list:
            #Applies left edge effect if appropriate
            if block.left_bound_change:
                for word_iter, word in enumerate(block.words):
                    #Use k to remain consistent with paper's formula
                    k: int = word_iter

                    #Compute new trust for Word
                    new_word_trust_left: float = word.trust + \
                    ((self.trust_inheritance_const * self.author_rep - word.trust) * \
                    math.exp((-self.edge_effect_const) * k))

                    #Replace old Word trust with new Word trust
                    word.trust = new_word_trust_left
            if block.right_bound_change:
                for word_iter, word in enumerate(block.words):
                    #Use k_bar to remain consistent with paper's formula
                    k_bar: int = len(block.words) - word_iter - 1

                    #Compute new trust for Word
                    new_word_trust_right: float = word.trust + \
                    ((self.trust_inheritance_const * self.author_rep - word.trust) * \
                    math.exp((-self.edge_effect_const) * k_bar))

                    #Replace old Word trust with new Word trust
                    word.trust = new_word_trust_right

    def apply_revision_effect(self) -> None:
        """
        Applies the revision effect to all words in this version
        """
        for word in self.word_list:
            if word.trust < self.author_rep:
                word.trust = word.trust + (
                    (self.author_rep - word.trust) * self.revision_const
                )
