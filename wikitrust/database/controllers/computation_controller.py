from pydal import DAL, Field
from datetime import date

def populate_prev_rev(db, page_id):
    all_revs = db(db.revision.page_id == page_id).iterselect(orderby=db.revision.rev_id)
    x=0
    prev2 = None
    for rev in all_revs:
        prev = rev
        rev.prev_rev = prev2
        rev.update_record()
        db.commit()
        prev2 = prev.rev_id
        print(str(rev.rev_id) + " : " + str(prev2))
        x+=1
    print(x)
        