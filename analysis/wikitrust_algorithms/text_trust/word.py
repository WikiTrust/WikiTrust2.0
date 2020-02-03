"""
Module containing Word class. Part of the text_trust package.

Eric Vin, 2019-2020
"""

#Standard library imports
from typing import List

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
        trust_list. Essentially zips together the two lists into a list of Words.
        """

        #Checks that text_list and trust_list are the same length. Otherwise raises
        #ValueError.
        if len(text_list) != len(trust_list):
            raise ValueError("Length of text_list does not equal length of trust_list: %d != %d" \
                             % (len(text_list), len(trust_list)))

        #Declares list to hold created words and fills it with created words
        words_list: List["Word"] = [Word(text_list[list_iter], trust_list[list_iter]) \
                                    for list_iter in range(len(text_list))]

        return words_list

    def clone(self) -> "Word":
        """
        Returns a deep copy of the word object.
        """
        return Word(self.text, self.trust)
