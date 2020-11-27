from wikitrust.database.controllers.create_entry import create_entry 
from wikitrust.database.controllers.computation_engine_db_controller import computation_engine_db_controller as comp
import json

def populate(db):
    create = create_entry(db)
    with open('resources/LadyGagaMeatDressRevisions/all_revision.json', encoding="utf-8") as f:
        data = json.load(f)
    env = create.create_environment('ladygaga').id
    create.create_page(data['pageId'], env, 'LadyGagaMeatDress', None)
    create.create_revision_log('test', None, data['pageId'])

    for rev in data['revisions']:
        create.create_revision(rev['revisionId'], data['pageId'], rev['userId'])
        create.create_user(rev['userId'])
        create.create_user_reputation('test', rev['userId'], env)
    print("Revisions Populated")
    x = comp(db, create)
    x.populate_prev_rev(data['pageId'])
