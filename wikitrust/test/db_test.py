import database.db_schema as schema 
import database.controllers.create as create
import database.controllers.computation_controller as comp
import json

def populate():
    with open('resources/LadyGagaMeatDressRevisions/all_revision.json', encoding="utf-8") as f:
        data = json.load(f)
    db = schema.connect_to_db()
    env = create.create_environment(db, 'ladygaga').id
    create.create_page(db, data['pageId'], env, 'LadyGagaMeatDress', None)

    for rev in data['revisions']:
        print(rev['revisionId'])
        create.create_revision(db, rev['revisionId'], data['pageId'], rev['userId'])
        create.create_user(db, rev['userId'])
    comp.populate_prev_rev(db, data['pageId'])
