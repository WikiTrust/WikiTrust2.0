"""
Module containing Article class. Part of the author_reputation package.

Eric Vin, 2019-2020
"""

#Standard library imports
from typing import List, Tuple, Dict, Callable, Sequence

#author_reputation package imports
from .version import Version
from .author import Author

#text_diff package imports
from wikitrust_algorithms.text_diff.edit import Edit
from wikitrust_algorithms.text_diff.chdiff import edit_diff_greedy, make_index2

class Article:
    """
    Class representing an article, containing all previous versions of that article.
    Also contains certain constants/parameters for reputation generation.
    """

    def __init__(self, max_judgement_dist: int, scaling_constant: float,\
                 scaling_function: Callable[[float], float]) -> None:
        """
        Article Constructor:
            -max_judgement_dist: The farthest back a version will be used as a
                reference version.
            -scaling_constant: A scaling constant >0 applied to the reputation change
            -scaling_function: A scaling function applied to the reputation change. Must
                monotonic and positive.
        """

        #Initializes a list that will hold all versions of this article
        self.versions: List[Version] = []

        #Stores constructor parameters in class attributes
        self.max_judgement_dist: int = max_judgement_dist
        self.scaling_constant: float = scaling_constant
        self.scaling_function: Callable[[float], float] = scaling_function

    def add_new_version(self, new_version) -> None:
        """
        Adds a new version to this article and updates the reputation of all versions
        covered by the max_judgement_dist.
        """

        #Adds the new version to the article's versions list
        self.versions.append(new_version)

        #Updates the reputation of all authors within max_judgement_dist
        #of this new version

        #Gets the range for the reference versions
        reference_version_range: Sequence[int] = \
            range(max(len(self.versions)-self.max_judgement_dist-1, 0), len(self.versions)-2)

        #Goes through every version being judged
        for reference_version_iter in reference_version_range:
            #Gets the reference version and the judged version (Which is directly
            #after the reference version)
            reference_version: Version = self.versions[reference_version_iter]
            judged_version: Version = self.versions[reference_version_iter+1]

            #Checks if author of new_version and the judged_version are the same
            if Author.check_same_author(judged_version.author, new_version.author):
                #Authors are the same, no reputation change
                pass
            else:
                #Authors are different. Change reputation of judged_version author

                #Computes reputation change to be applied to new_version's author
                reputation_change: float = self.scaling_constant\
                    * self.compute_edit_distance(reference_version, judged_version)\
                    * self.compute_edit_quality(reference_version, judged_version, new_version)\
                    * self.scaling_function(new_version.author.get_author_rep())

                #Applies reputation change
                judged_version.author.set_author_rep(judged_version.author.get_author_rep()\
                    + reputation_change)

    @classmethod
    def compute_edit_distance(cls, version_1, version_2) -> float:
        """
        Computes the edit distance between two versions
        """

        #Gets list of tuples representings edits
        split_version_1: List[str] = version_1.text.split()
        split_version_2: List[str] = version_2.text.split()
        edit_index: Dict[Tuple[str, str], List[int]] = make_index2(split_version_2)
        edit_list_tuples: List[Tuple[int, int, int, int]] = edit_diff_greedy(split_version_1, split_version_2, edit_index)

        #Converts list of tuples to list of Edits
        edit_list: List[Edit] = [Edit.edit_tuple_constructor(edit_tuple) for edit_tuple in edit_list_tuples]

        #Calculates insertion_total and deletion_total over all edits in edit_list
        insertion_total: int = 0
        deletion_total: int = 0

        for edit in edit_list:
            if edit.edit_type == Edit.INSERT:
                #Edit is insertion. Adding the insertion length to the insertion total.
                insertion_total += edit.length
            elif edit.edit_type == Edit.DELETE:
                #Edit is deletion. Adding the deletion length to the deletion total.
                deletion_total += edit.length

        #Calculates move_total
        move_total: int = 0

        #Creates a list of all move edits in edit_list
        move_list: List[Edit] = [edit for edit in edit_list if edit.edit_type == Edit.MOVE]

        #Sorts move_list by the origin of the moves in ascending order
        moves_origin_list: List[Edit] = sorted(move_list, key=lambda edit: edit.origin)

        #Sorts move_list by the destination of the moves in descending order
        moves_destination_list: List[Edit] = sorted(move_list, key=lambda edit: edit.destination)[::-1]

        #Now we compute two groups of pairs of moves. Assume a pair consists of (Move a, Move b).
        #These groups are origin valid pairs and destination valid pairs respectively.
        #The pair is origin valid iff a.origin < b.origin.
        #The pair is destination valid iff a.destination > b.destination.

        #Creates a list of all origin valid pairs in move_list.
        origin_valid_move_list: List[Tuple[Edit, Edit]] = []

        for move_a_iter, move_a in enumerate(moves_origin_list):
            for move_b in moves_origin_list[(move_a_iter+1):]:
                origin_valid_move_list.append((move_a, move_b))

        #Creates a list of all origin valid pairs in move_list.
        destination_valid_move_list: List[Tuple[Edit, Edit]] = []

        for move_a_iter, move_a in enumerate(moves_destination_list):
            for move_b in moves_destination_list[(move_a_iter+1):]:
                destination_valid_move_list.append((move_a, move_b))

        #Creates a list of all crossed move pairs. These are move pairs that are both
        #origin valid and destination valid.
        crossed_move_list: List[Tuple[Edit, Edit]] = []

        for move_pair in origin_valid_move_list:
            if move_pair in destination_valid_move_list:
                crossed_move_list.append(move_pair)

        #Adds the product of the moves in each pair in crossed_move_list to move_total
        for crossed_move in crossed_move_list:
            move_total += crossed_move[0].length * crossed_move[1].length

        #Computes the distance from all the totals computed previously
        distance: float = max(insertion_total, deletion_total)\
                   - (0.5*max(insertion_total, deletion_total))\
                   + move_total

        return distance

    @classmethod
    def compute_edit_quality(cls, version_1, version_2, version_3) -> float:
        """
        Computes the edit distance quality given three versions. A reference version,
        a judged version, and a new version.
        """

        edit_quality: float = (cls.compute_edit_distance(version_1, version_3)\
                       - cls.compute_edit_distance(version_2, version_3))\
                       / cls.compute_edit_distance(version_1, version_2)

        return edit_quality
