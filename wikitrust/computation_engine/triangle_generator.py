import math
import json
import datetime

#Standard library imports
from typing import List, Tuple, Dict, Callable, Sequence

from pydal.migrator import InDBMigrator
from pydal import DAL, Field

from wikitrust_lib.text_diff.edit import Edit

class TriangleGenerator:
    def __init__(self, dbcontroller, text_storage_engine, algorithm_ver, max_judge_dist, text_diff_function, index_function):
        self.dbcontroller = dbcontroller
        self.text_storage_engine = text_storage_engine
        self.algorithm_ver = algorithm_ver
        self.max_judge_dist = max_judge_dist
        self.text_diff_function = text_diff_function
        self.index_function = index_function

    def compute_triangles_batch(self, page_id):
        #Maps class variables to shorter local variables
        storage_engine = self.text_storage_engine

        #Retrieves page revisions
        page_revs = self.dbcontroller.get_all_revisions(page_id)

        # Rolls over current revision into reference revision, initialized to none
        reference_revision_text = None
        reference_revision_author = None

        for rev_num in range(len(page_revs)):
            # If this is the first revision, there is no reference revision so we cannot judge it.
            # We will however, populate reference_revision_text
            if rev_num == 0:
                #Checks that we have access to the reference text, add advanced error handling later
                assert(page_revs[rev_num-1].text_retrieved == True)
                #Populates reference_revision_text with current text for use in next iteration
                reference_revision_id = page_revs[rev_num].revision_id
                reference_revision_blob = page_revs[rev_num].revision_blob
                reference_revision_text = storage_engine.read(page_id, self.algorithm_ver, rev_num)
                reference_revision_author = page_revs[rev_num].user_id

            #Checks that we have access to the reference judged text, add advanced error handling later
            assert(page_revs[rev_num].text_retrieved == True)

            #Get revision text for current (judged) revision
            judged_revision_id = page_revs[rev_num].revision_id
            judged_revision_blob = page_revs[rev_num].revision_blob
            judged_revision_text = storage_engine.read(page_id, self.algorithm_ver, rev_num)
            judged_revision_author = page_revs[rev_num].user_id

            #Computes edit distance between reference and current once
            reference_current_distance = self.compute_edit_distance(reference_revision_text, judged_revision_text)

            for new_rev_num in range(rev_num + 1, rev_num + self.max_judge_dist):
                #Get revision text for new revision
                new_revision_id = page_revs[new_rev_num].revision_id
                new_revision_blob = page_revs[new_rev_num].revision_blob
                new_revision_text = storage_engine.read(page_id, self.algorithm_ver, new_rev_num)
                new_revision_author = page_revs[new_rev_num].user_id

                reference_new_distance = self.compute_edit_distance(reference_revision_text, new_revision_text)
                current_new_distance = self.compute_edit_distance(judged_revision_text, new_revision_text)

                triangle_dict = {"revisions": [reference_revision_id, judged_revision_id, new_revision_id], \
                                 "distances": [reference_current_distance, reference_new_distance, current_new_distance], \
                                 "authors":   [reference_revision_author, judged_revision_author, new_revision_author]}

                triangle_json = json.dumps(triangle_dict)

                self.dbcontroller.update_or_insert_triangle(self.algorithm_ver, page_id, reference_revision_id, judged_revision_id, new_revision_id)

            self.dbcontroller.update_revision_log(self.algorithm_ver, page_id, judged_revision_id)

            #Rolls over current revision variables into reference revision variables
            reference_revision_id = judged_revision_id
            reference_revision_text = judged_revision_text
            reference_revision_author = judged_revision_author


    def compute_triangles_keepup(self):
        pass

    def compute_edit_distance(self, rev_1_text, rev_2_text):
        """
        Computes the edit distance between two revision's text
        """

        #Gets list of tuples representings edits
        split_text_1: List[str] = rev_1_text.text.split()
        split_text_2: List[str] = rev_2_text.text.split()
        edit_index: Dict[Tuple[str, str], List[int]] = self.index_function(split_text_2)
        edit_list_tuples: List[Tuple[int, int, int, int]] = self.text_diff_function(split_text_1, split_text_2, edit_index)

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

        #Creates a list of all destination valid pairs in move_list.
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
