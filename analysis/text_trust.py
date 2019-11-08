#!/usr/bin/python

"""
This file contains functions that deal with the evaluation of
text trust.

Eric Vin, 2019
"""

from typing import List, Tuple

from chdiff import test_tichy, test_greedy, print_edit_diff

class Word:
    """
    Class representing a word and its associated trust value
    """

    def __init__(self, text: str, trust: int) -> None:
        """
        Word Constructor:
            -text: The text present in the word
            -trust: The trust value associated with this word
        """
        self.text: str = text
        self.trust: int = trust

    def __str__(self) -> str:
        """
        Returns a string interpretation of this Word
        """
        return "(%s,%d)" % (self.text, self.trust)

    @classmethod
    def create_list_words(cls, text_list: List[str], trust_list: List[int]) -> List["Word"]:
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

        return "Edit Type: %s\nWords: %s" % (edit_print, words_print)

class Version:
    """
    Class representing one version of an article at a certain point in time.
    """

    def __init__(self, word_list: List[Word], edit_list: List[Edit]) -> None:
        """
        Version Constructor:
            -words: A list of Words present in this Version
            -edit_list: A list of Edits that map the previous Version
                to this Version.
        """

        #A list of words present in this Version
        self.word_list: List[Word] = word_list

        #A list of edits that brought the previous version to the current version
        self.edit_list: List[Edit] = edit_list

        #A list of blocks contained in this version
        self.block_list: List[Block] = self.compute_blocks()

        #Checks if bounds of blocks have changed contexts
        self.check_block_bound_changes()

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

    def check_block_bound_changes(self) -> None:
        """
        Iterates through every block in the block_list to check if their bounds
        have changed context
        """
        for block in self.block_list:


            #Checks to see if left bound is at start of word_list, or right bound
            #is at end of word_list. In either case, that respective bound does
            #NOT change context.
            if block.edit.destination == 0:
                #Left bound is at the start of the word_list, therefore
                #no change of context at left bound.
                block.left_bound_change = False
            if block.edit.destination + block.edit.length == len(self.word_list):
                #Right bound is at the end of the word_list, therefore
                #no change of context at right bound.
                block.right_bound_change = False

if __name__ == '__main__':
    s1 = "the quick brown fox jumps over the lazy dog"
    s2 = "the lazy fox jumps over the quick brown dog"

    print("String 1: %s" % (s1))
    print("String 2: %s" % (s2))

    print()

    diff_list = test_tichy("the quick brown fox jumps over the lazy dog", "the lazy fox jumps over the quick brown dog")

    print("Differences:")

    print(diff_list)
    print_edit_diff(diff_list)

    print()

    word_list = Word.create_list_words(s2.split(), [1 for x in range(len(s2.split()))])
    edit_list = [Edit.edit_tuple_constructor(edit) for edit in diff_list]

    print("Word List:")
    for word in word_list:
        print(str(word))

    print()

    print("Edit List:")
    for edit in edit_list:
        print(str(edit))

    print()

    ver = Version(word_list, edit_list)

    print("Block List:")
    print("".join([str(block) + "\n" for block in ver.block_list]))