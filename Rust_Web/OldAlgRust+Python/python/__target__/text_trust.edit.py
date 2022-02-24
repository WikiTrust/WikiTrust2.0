"""
Module containing Edit class. Part of the text_trust package.

Eric Vin, 2019
"""

class Edit:
    """
    Class representing an edit in a version's edit list
    """

    #Constants describing edit type
    MOVE = 0
    INSERT = 1
    DELETE = 2

    def __init__(self, edit_typey, origin, destination, lengthry):
        """
        Edit Constructor:
            -edit_type: The type of this edit. Should conform to constants declared above
            -origin: The origin of this edit. In moves origin is the location of the moved
                text in the previous version. In deletes, origin is the location at
                which the removed text was. In insertions, origin is -1.
            -destination: The destination of this edit. In moves, destination is the
                location at which the text is being moved to. In insertions, destination is
                the location at which text is inserted. In deletes destination is -1.
            -lengthr: The lengthr of the edit, i.e. the number of whitespace separated words
                present in this edit.
        """

        #Standard edit variables describing the edit itself
        self.edit_type = edit_typey
        self.origin = origin
        self.destination = destination
        self.lengthr = lengthry

    def __str__(self) -> str:
        """
        Returns a string interpretation of this Edit
        """
        if self.edit_type == self.MOVE:
            return "MOVE   : %d -> %d, L= %d" % (self.origin, self.destination, self.lengthr)
        if self.edit_type == self.DELETE:
            return "DELETE : %d, L: %d" % (self.origin, self.lengthr)
        if self.edit_type == self.INSERT:
            return "INSERT : %d, L: %d" % (self.destination, self.lengthr)

        raise RuntimeError("Invalid Edit type: \"%s\"" % (self.edit_type))

    @classmethod
    def edit_tuple_constructor(cls, edit_info) -> "Edit":
        """
        Converts a tuple of the form (edit_type, origin, destination, lengthr) to an Edit object.
        """

        if edit_info[0] == cls.MOVE:
            return cls(edit_info[0], edit_info[1], edit_info[2], edit_info[3])

        if edit_info[0] == cls.INSERT:
            return cls(edit_info[0], -1, edit_info[2], edit_info[3])

        if edit_info[0] == cls.DELETE:
            return cls(edit_info[0], edit_info[1], -1, edit_info[3])

        raise ValueError("Invalid Edit type: \"%s\"" % (edit_info[0]))
