import wikitrust.database.db_schema as schema 
import wikitrust.database.controllers.create_entry as create
from wikitrust.database.controllers.computation_controller import computation_engine_db_controller as comp
import json

def populate(db):
    with open('resources/LadyGagaMeatDressRevisions/all_revision.json', encoding="utf-8") as f:
        data = json.load(f)
    env = create.create_environment(db, 'ladygaga').id
    create.create_page(db, data['pageId'], env, 'LadyGagaMeatDress', None)

    for rev in data['revisions']:
        print(rev['revisionId'])
        create.create_revision(db, rev['revisionId'], data['pageId'], rev['userId'])
        create.create_user(db, rev['userId'])
    x =  comp(db)
    x.populate_prev_rev(data['pageId'])
