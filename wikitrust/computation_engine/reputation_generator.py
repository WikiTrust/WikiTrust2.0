import json
import math

from pydal.migrator import InDBMigrator
from pydal import DAL, Field

class ReputationGenerator:
    def __init__(self, dbcontroller, text_storage_engine, algorithm_ver, scaling_const, scaling_func):
        self.dbcontroller = dbcontroller
        self.text_storage_engine = text_storage_engine
        self.algorithm_ver = algorithm_ver
        self.scaling_const = scaling_const
        self.scaling_func = scaling_func

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

            # Checks that the authors of the judged and reference version are not the same
            if reference_author_id == judged_author_id:
                # Same author, so no reputation change

                target_triangle.update(reputation_inc=0)

            else:
                # Different author, so reputation change applies

                #Calculates triangle_quality from triangle distances
                triangle_quality = (judged_new_dis- reference_new_dis) \
                                   /reference_judged_dis

                new_author_reputation = self.dbcontroller.get_reputation(self.algorithm_ver, new_author_id)

                # Computes reputation change to be applied to judged version's author
                reputation_change =  self.scaling_const \
                    * reference_judged_dis \
                    * triangle_quality\
                    * self.scaling_func(new_author_reputation)

                # Updates triangle with reputation change
                self.dbcontroller.update_triangle_rep(target_triangle, reputation_change)
