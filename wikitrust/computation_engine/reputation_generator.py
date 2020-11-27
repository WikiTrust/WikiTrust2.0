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
        #Maps class variables to shorter local variables
        storage_engine = self.text_storage_engine

        new_triangles = self.dbcontroller.get_all_unprocessed_triangles(self.algorithm_ver)

        for triangle_iter in range(len(new_triangles)):
            target_triangle = new_triangles[triangle_iter]

            # Unpacks triangle JSON
            triangle_json = json.loads(target_triangle.info)

            # Checks that the authors of the judged and reference version are not the same
            reference_author = triangle_json["authors"][0]
            judged_author = triangle_json["authors"][1]
            new_author = triangle_json["authors"][2]

            if reference_author == judged_author:
                # Same author, so no reputation change

                target_triangle.update(reputation_inc=0)

            else:
                # Different author, so reputation change applies

                # Retrieves needed information from json
                reference_judged_distance = triangle_json["distances"][0]

                #Calculates triangle_quality from triangle distances
                triangle_quality = (triangle_json["distances"][1] - triangle_json["distances"][2]) \
                                   /(triangle_json["distances"][0])

                new_author_reputation = self.dbcontroller.get_reputation(self.algorithm_ver, new_author)

                # Computes reputation change to be applied to judged version's author
                reputation_change =  self.scaling_const\
                    * reference_judged_distance \
                    * triangle_quality\
                    * self.scaling_func(new_author_reputation)

                # Updates triangle with reputation change
                target_triangle.update(reputation_inc=reputation_change)
