"""
Module containing Block class. Part of the text_trust package.

Eric Vin, 2019
"""

from typing import List

from .word import Word

from wikitrust_algorithms.text_diff.edit import Edit

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

        return "Edit Type: %s\nWords: %s\nLeft Bound Change: %s  Right Bound Change: %s" \
                % (edit_print, words_print, self.left_bound_change, self.right_bound_change)
