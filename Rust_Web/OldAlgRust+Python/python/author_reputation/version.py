"""
Module containing Version class. Part of the author_reputation package.

Eric Vin, 2019
"""

from .author import Author

class Version:
    """
    Class representing a version of an article, i.e. it's state at one point,
    past or present.
    """

    def __init__(self, author: Author, text) -> None:
        """
        Version Constructor:
            -author: An author object representing the author of this version.
            -text: The text in this version.
        """
        self.author: Author = author
        self.text = text

    def __str__(self) -> str:
        """
        Returns a string interpretation of this Version
        """
        return "Version " + str(self.author.author_id) +"\n Text: " + self.text
