#!/usr/bin/python

"""
This file contains functions that deal with the evaluation of
text trust.

Eric Vin, 2019
"""

import math

from typing import List, Tuple

from chdiff import test_tichy, test_greedy, print_edit_diff

class Word:
    """
    Class representing a word and its associated trust value
    """

    def __init__(self, text: str, trust: float) -> None:
        """
        Word Constructor:
            -text: The text present in the word
            -trust: The trust value associated with this word. Set to
                1 if trust for word does not exist in previous version.
                Otherwise starts as trust of word in previous version
                and is modified to trust of current version by parent
                Version class.
        """
        self.text: str = text
        self.trust: float = trust

    def __str__(self) -> str:
        """
        Returns a string interpretation of this Word
        """
        return "(%s,%.2f)" % (self.text, self.trust)

    @classmethod
    def create_list_words(cls, text_list: List[str], trust_list: List[float]) -> List["Word"]:
        """
        Returns a list of Word objects containing text from text_list and trust from
        trust_list. Essentially zips together the two lists.
        """

        #Checks that text_list and trust_list are the same length. Otherwise raises
        #ValueError.
        if len(text_list) != len(trust_list):
            raise ValueError("Length of text_list does not equal length of trust_list: %d != %d" % (len(text_list), len(trust_list)))

        #Declares list to hold created words
        words_list: List["Word"] = []

        #Creates all words and adds them to list
        for list_iter in range(len(text_list)):
            words_list.append(Word(text_list[list_iter], trust_list[list_iter]))

        return words_list

    def clone(self) -> "Word":
        """
        Returns a deep copy of the word object.
        """
        return Word(self.text, self.trust)

class Edit:
    """
    Class representing an edit in a version's edit list
    """

    #Constants describing edit type
    MOVE: int = 0
    INSERT: int = 1
    DELETE: int = 2

    def __init__(self, edit_type: int, origin: int, destination: int, length: int) -> None:
        """
        Edit Constructor:
            -edit_type: The type of this edit. Should conform to constants declared above
            -origin: The origin of this edit. In moves origin is the location of the moved
                text in the previous version. In deletes, origin is the location at
                which the removed text was. In insertions, origin is -1.
            -destination: The destination of this edit. In moves, destination is the
                location at which the text is being moved to. In insertions, destination is
                the location at which text is inserted. In deletes destination is -1.
            -Length: The length of the edit, i.e. the number of whitespace separated words
                present in this edit.
        """

        #Standard edit variables describing the edit itself
        self.edit_type: int = edit_type
        self.origin: int = origin
        self.destination: int = destination
        self.length: int = length

    def __str__(self) -> str:
        """
        Returns a string interpretation of this Edit
        """
        if self.edit_type == self.MOVE:
            return "MOVE   : %d -> %d, L= %d" % (self.origin, self.destination, self.length)
        if self.edit_type == self.DELETE:
            return "DELETE : %d, L: %d" % (self.origin, self.length)
        if self.edit_type == self.INSERT:
            return "INSERT : %d, L: %d" % (self.destination, self.length)

        raise RuntimeError("Invalid Edit type: \"%s\"" % (self.edit_type))

    @classmethod
    def edit_tuple_constructor(cls, edit_info: Tuple[int, int, int, int]) -> "Edit":
        """
        Converts a tuple of the form (edit_type, origin, destination, length) to an Edit object.
        """

        if edit_info[0] == cls.MOVE:
            return cls(edit_info[0], edit_info[1], edit_info[2], edit_info[3])

        if edit_info[0] == cls.INSERT:
            return cls(edit_info[0], -1, edit_info[2], edit_info[3])

        if edit_info[0] == cls.DELETE:
            return cls(edit_info[0], edit_info[1], -1, edit_info[3])

        raise ValueError("Invalid Edit type: \"%s\"" % (edit_info[0]))

class Block:
    """
    Class representing a group of words that are all part of one edit.
    """

    def __init__(self, words: List[Word], edit: Edit) -> None:
        """
        Block Constructor:
            -words: A list of Words present in this Block
            -edit: The Edit that corresponds to this Block
        """

        #The Words present in this edit
        self.words: List[Word] = words

        #The Edit that corresponds to this block
        self.edit: Edit = edit

        #Variables indicating whether the left or right bound have changed context.
        #These default to False until the edits are crawled to verify bound context.
        self.left_bound_change: bool = False
        self.right_bound_change: bool = False

    def __str__(self) -> str:
        """
        Returns a string interpretation of this Block
        """
        edit_print: str = str(self.edit)
        words_print: str = "".join([str(word) for word in self.words])

        return "Edit Type: %s\nWords: %s\nLeft Bound Change: %s  Right Bound Change: %s"\
        % (edit_print, words_print, self.left_bound_change, self.right_bound_change)

class Version:
    """
    Class representing one version of an article at a certain point in time.
    """

    def __init__(self, word_list: List[Word], edit_list: List[Edit], author_rep: float,\
        trust_inheritance_const: float, revision_const: float, edge_effect_const: float) -> None:
        """
        Version Constructor:
            -words: A list of Words present in this Version
            -edit_list: A list of Edits that map the previous Version
                to this Version.
            -author_rep: The reputation of the author who made the
                edits in edit_list
            -trust_inheritance_const: Trust inheritance constant
            -revision_const: Revision constant
            -edge_effect_const: Edge effect constant

            **NOTE**
            This constructor should only be used by the factory methods create_initial_version
            and create_next_version.
        """

        #A list of words present in this Version
        self.word_list: List[Word] = word_list #Word.create_list_words(word_list, [initial_trust for x in range(len(word_list))])

        #A list of edits that brought the previous version to the current version
        self.edit_list: List[Edit] = edit_list

        #The reputation of the author who made the edits in edit_list
        self.author_rep: float = author_rep

        #The constants used in trust calculations
        self.trust_inheritance_const: float = trust_inheritance_const
        self.revision_const: float = revision_const
        self.edge_effect_const: float = edge_effect_const

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
    def create_initial_version(cls, text_list: List[str], initial_trust: float,\
        trust_inheritance_const: float, revision_const: float, edge_effect_const: float) -> "Version":
        """
        This is a factory method to create an initial Version of a page
        given a starting list of words. This is structured as an insertion
        containing all words in a word_list with the author reputation
        being the initial_trust passed.

        create_initial_version Parameters:
            -text_list: A list of strings representing all words in this Version.
            -initial_trust: A float representing the initial trust for all words
                in this Version.
            -trust_inheritance_const: Trust inheritance constant
            -revision_const: Revision constant
            -edge_effect_const: Edge effect constant
        """

        #Creates list of Word objects all with trust equal to initial_trust.
        word_list: List[Word] = Word.create_list_words(text_list,\
                                [initial_trust for x in range(len(text_list))])

        #Creates edit_list with one edit: A move of all text in text_list from
        #zero to zero
        edit_list = [Edit(Edit.MOVE, 0, 0, len(word_list))]

        return cls(word_list, edit_list, initial_trust,\
                trust_inheritance_const, revision_const, edge_effect_const)

    @classmethod
    def create_next_version(cls, prev_version: "Version", new_text: List[str], new_edits: List[Edit], author_rep: float) -> "Version":
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
        new_word_list: List[Word] = Word.create_list_words(new_text,\
                                    [-1 for x in range(len(new_text))])

        #Copies trust from words involved in moves.
        #They assume the same trust they had in the previous version
        for edit in edit_list:
            #Only applies copy if edit is a move
            if edit.edit_type == Edit.MOVE:
                #Copies over a clone of all words in move from edit origin
                #in prev_word_list to edit destination in new_word_list,
                #scaled by word_iter
                for word_iter in range(edit.length):
                    new_word_list[edit.destination+word_iter] = prev_word_list[edit.origin+word_iter].clone()


        #Creates and returns the next version
        return cls(new_word_list, new_edits, author_rep,\
                    prev_version.trust_inheritance_const, prev_version.revision_const, prev_version.edge_effect_const)



    def compute_blocks(self) -> List[Block]:
        """
        Computes a list of Blocks from this Version's words and edit_list
        """

        #Gets all edits with a destination in the current version, i.e. they
        #are present in this version (e.g. Moves and Inserts)
        present_edits: List[Edit] = [edit for edit in self.edit_list if edit.destination >= 0]

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
            version_blocks.append(Block(self.word_list[start_words:end_words], edit))

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
                    word.trust = (self.author_rep * self.trust_inheritance_const)


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
                if (block.edit.origin == block.edit.destination) and (block.edit.destination == 0):
                    block.left_bound_change = False
                else:
                    block.left_bound_change = True

                #Checks if right bound has changed context
                if (block.edit.origin == block.edit.destination) and (block.edit.destination == len(self.word_list)-block.edit.length):
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
                    k_bar: int = len(block.words) - word_iter -1

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
                word.trust = word.trust + ((self.author_rep - word.trust) * self.revision_const)

if __name__ == '__main__':
    initial_trust = 1

    test_strings = []
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("foo the quick brown fox jumps over the lazy dog bar")
    test_strings.append("the quick brown fox jumps over the lazy dog")
    test_strings.append("the lazy fox jumps over the quick brown dog")
    test_strings.append("the lazy fox jumps over the quick brown dog and also other stuff")

    test_trusts = [10, 7, 10, 20]

    trust_inheritance_const = 0.5
    revision_const = 0.1
    edge_effect_const = 2

    print("Initial String: " + str(test_strings[0]))

    for string_iter, string in enumerate(test_strings):
        print("String %d: %s" %(string_iter, string))
    print()

    print("Version 1:\n")
    print("Initial Trust: " + str(initial_trust) + "\n")

    text_list = test_strings[0].split()

    #ver = Version(word_list, edit_list, author_reputation, initial_trust, trust_inheritance_const, revision_const, edge_effect_const)
    ver = Version.create_initial_version(text_list, initial_trust, trust_inheritance_const, revision_const, edge_effect_const)

    print("".join([str(word) for word in ver.word_list]) + "\n")

    print("Block List:")
    print("".join([str(block) + "\n" for block in ver.block_list]))

    print("\n")

    for string_iter in range(len(test_strings)-1):
        print("Version %d:\n" % (string_iter + 2))
        print("Author Reputation: %d\n" % (test_trusts[string_iter]))

        diff_list = test_tichy(test_strings[string_iter], test_strings[string_iter + 1])
        edit_list = [Edit.edit_tuple_constructor(edit) for edit in diff_list]
        text_list = test_strings[string_iter+1].split()

        ver = Version.create_next_version(ver, text_list, edit_list, test_trusts[string_iter])

        print("".join([str(word) for word in ver.word_list]) + "\n")

        print("Block List:\n")
        print("".join([str(block) + "\n" for block in ver.block_list]))
        print("\n")
