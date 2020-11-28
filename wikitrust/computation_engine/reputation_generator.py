import json
import math

from pydal.migrator import InDBMigrator
from pydal import DAL, Field

class ReputationGenerator:
    def __init__(self, dbcontroller, algorithm_ver, params):
        self.dbcontroller = dbcontroller
        self.algorithm_ver = algorithm_ver
        self.scaling_const = params[0]
        self.scaling_func = params[1]

    def update_author_reputation(self):
        unprocessed_triangles = self.dbcontroller.get_all_unprocessed_triangles(self.algorithm_ver)

        for target_triangle in unprocessed_triangles:
            triangle_info = self.dbcontroller.get_triangle_info(target_triangle)

            rev_info = triangle_info[0]
            author_info = triangle_info[1]
            distance_info = triangle_info[2]

            reference_rev_id = rev_info[0]
            judged_rev_id = rev_info[1]
            new_rev_id = rev_info[2]

            reference_author_id = author_info[0]
            judged_author_id = author_info[1]
            new_author_id = author_info[2]

            reference_judged_dis = distance_info[0]
            judged_new_dis = distance_info[1]
            reference_new_dis = distance_info[2]

            #Get env information
            page_id = self.dbcontroller.get_page_from_rev(judged_rev_id)
            env_id = self.dbcontroller.get_environment_by_page_id(page_id)

            # Checks that the authors of the judged and reference version are not the same
            if reference_author_id == judged_author_id:
                # Same author, so no reputation change

                self.dbcontroller.update_triangle_rep(target_triangle, 0)

            else:
                # Different author, so reputation change applies

                print("Reference Rev Id: ", reference_rev_id)
                print("Judged Rev Id: ", judged_rev_id)
                print("New Rev Id: ", new_rev_id)

                #Calculates triangle_quality from triangle distances
                #ADDING 0.00001 TO AVOID DIVISION BY ZERO
                triangle_quality = (reference_new_dis- judged_new_dis) \
                                   /(reference_judged_dis + 0.00001)

                new_author_reputation = self.dbcontroller.get_reputation(self.algorithm_ver, new_author_id, env_id)

                print("New Author Reputation: ", new_author_reputation)

                # Computes reputation change to be applied to judged version's author
                reputation_change =  self.scaling_const \
                    * reference_judged_dis \
                    * triangle_quality\
                    * self.scaling_func(new_author_reputation)

                print("Reputation Change", reputation_change)

                # Updates triangle with reputation change
                self.dbcontroller.update_triangle_rep(target_triangle, reputation_change)

                # Change reputation of judged author
                old_judged_rep = self.dbcontroller.get_reputation(self.algorithm_ver, judged_author_id, env_id)
                new_judged_rep = max(old_judged_rep + reputation_change, 0)
                self.dbcontroller.set_reputation(self.algorithm_ver, judged_author_id, env_id, new_judged_rep)
