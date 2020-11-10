from pydal import DAL, Field
from datetime import date

def create_environment(
    db, 
    environment_name = ''
):
    try:
        ret = db.environment.insert(environment_name = environment_name)
        db.commit()
        return ret
    except: pass

def create_page(
    db, 
    page_id=-1, 
    environment_id = None, 
    page_title = "", 
    last_check_time = None
):
    try:
        ret = db.page.insert(page_id = page_id, environment_id = environment_id, page_title = page_title, last_check_time = last_check_time)
        db.commit()
        return ret
    except: pass

def create_user(
    db, 
    user_id=-1, 
    user_name=''
):
    try:
        ret = db.user.insert(user_id = user_id, user_name = user_name)
        db.commit()
        return ret
    except: pass

def create_revision(
    db, 
    rev_id = -1, 
    page_id = -1, 
    user_id = -1, 
    rev_date = None, 
    prev_rev = -1, 
    text_retrieved = 'F', 
    last_attempt_date = None, 
    num_attempts = -1,
):
    try:
        ret = db.revision.insert(rev_id = rev_id, page_id = page_id, user_id = user_id, rev_date = rev_date, prev_rev = prev_rev, text_retrieved = text_retrieved, last_attempt_date = last_attempt_date, num_attempts = num_attempts)
        db.commit()
        return ret
    except: pass

def create_revision_log(
    db, 
    version = '', 
    stage = '', 
    page_id = -1, 
    last_rev = None, 
    lock_date = None
):
    x = db.revision_log.version = version
    y = db.revision_log.page_id = page_id
    q = db(x & y).select().first()
    if(q == None)
        ret = db.revision_log.insert(version = version, stage = stage, page_id = page_id, last_rev = last_rev, lock_date = lock_date)
        db.commit()
        return ret
    return q

def create_user_reputation(
    db, 
    version = '', 
    user_id = -1, 
    environment = None, 
    reputation_value = 0
):
    x = db.user_reputation.version = version
    y = db.user_reputation.user_id = user_id
    z = db.user_reputation.environment = environment
    q = db(x & y & z).select().first()
    if(q == None):
        ret = db.user_reputation.insert(version = version, user_id = user_id, environment = environment, reputation_value = reputation_value)
        db.commit()
        return ret
    return q

def create_text_storage(
    db, 
    version = '', 
    page_id = -1,
    rev_id = -1,
    text_type = '',
    blob = ''
):
    ret = db.text_storage.insert(version = version, page_id = page_id, rev_id = rev_id, text_type = text_type, blob = blob)
    db.commit()
    return ret

def create_triangles(
    db,
    version = '',
    page_id = -1,
    rev_id_1 = -1,
    rev_id_2 = -1,
    rev_id_3 = -1,
    reputation_inc = 0
):
    ret = db.triangles.insert(version = version, page_id = page_id, rev_id_1 = rev_id_1, rev_id_2 = rev_id_2, rev_id_3 = rev_id_3, reputation_inc = reputation_inc)
    db.commit()
    return ret

def create_text_diff(
    db,
    version = '',
    rev_id_1 = -1,
    rev_id_2 = -1,
    info = ''
):
    ret = db.text_diff.insert(version = version, rev_id_1 = rev_id_1, rev_id_2 = rev_id_2, info=info)
    db.commit()
    return ret

def create_text_distance(
    db, 
    version = '',
    rev_id_1 = -1,
    rev_id_2 = -1,
    distance = ''
):
    ret = db.text_distance.insert(version = version, rev_id_1 = rev_id_1, rev_id_2 = rev_id_2, distance = distance)
    db.commit()
    return ret
