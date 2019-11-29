"""
Module containing Edit class. Part of the author_reputation package.

Eric Vin, 2019
"""

from typing import Tuple

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
