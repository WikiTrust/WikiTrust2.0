import json
import math

from pydal.migrator import InDBMigrator
from pydal import DAL, Field

#Algorithm Constants
__ALGORITHM_VER__ = "REPUTATION_GENERATOR_DEV"
__MAX_JUDGE_DIST__ = 10
__SCALING_CONST__ = 1
__SCALING_FUNC__ = lambda x: math.log(x)

def update_author_reputation(db):
    new_triangles = db(db.triangles.reputation_inc == None).iterselect(orderby=db.triangles.judged_revision)

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
            triangle_quality = (triangle_json["distances"][1] - triangle_json["distances"][2]) \
                               /(triangle_json["distances"][0])
            new_author_reputation = db(db.user_reputation.user == new_author).select()[0]

            # Computes reputation change to be applied to judged version's author
            reputation_change =  __SCALING_CONST__\
                * reference_judged_distance \
                * triangle_quality\
                * __SCALING_FUNC__(new_author_reputation)

            # Updates triangle with reputation change
            target_triangle.update(reputation_inc=reputation_change)
