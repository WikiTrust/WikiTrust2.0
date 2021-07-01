from wikitrust.database.controllers.create_entry import create_entry
import json

def drop_tables(db):
    print(db.tables())
    for table_name in db.tables():
        db[table_name].drop()
        print(table_name + "dropped")
    db.commit()
#return controller
def drop_and_populate(compute_db_ctrl):
    # drop_tables(compu.db)
    populate(compute_db_ctrl)
    return compute_db_ctrl

def populate(compu):
    create = compu.create
    with open('resources/LadyGagaMeatDressRevisions/all_revision.json', encoding="utf-8") as f:
        data = json.load(f)
    env = create.create_environment('ladygaga')
    create.create_page(data['pageId'], env, 'LadyGagaMeatDress', None)
    create.create_revision_log('test', None, data['pageId'])

    for rev in data['revisions']:
        create.create_revision(rev['revisionId'], data['pageId'], rev['userId'])
        create.create_user(rev['userId'])
        create.create_user_reputation('test', rev['userId'], env)
    print("Revisions Populated")
    compu.populate_prev_rev(data['pageId'])
