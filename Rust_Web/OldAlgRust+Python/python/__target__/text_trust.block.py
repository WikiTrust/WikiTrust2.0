"""
Module containing Block class. Part of the text_trust package.

Eric Vin, 2019
"""



from text_trust.edit import Edit
from text_trust.word import Word

class Block:
    """
    Class representing a group of words that are all part of one edit.
    """

    def __init__(self, words, edit) -> None:
        """
        Block Constructor:
            -words: A list of Words present in this Block
            -edit: The Edit that corresponds to this Block
        """

        #The Words present in this edit
        self.words = words

        #The Edit that corresponds to this block
        self.edit = edit

        #Variables indicating whether the left or right bound have changed context.
        #These default to False until the edits are crawled to verify bound context.
        self.left_bound_change: bool = False
        self.right_bound_change: bool = False

    def __str__(self) -> str:
        """
        Returns a string interpretation of this Block
        """
        edit_print = str(self.edit)
        words_print = "".join([str(word) for word in self.words])

        return "Edit Type: "+edit_print+"\nWords: "+words_print+"\nLeft Bound Change: "+ self.left_bound_change+"  Right Bound Change: "+self.right_bound_change
