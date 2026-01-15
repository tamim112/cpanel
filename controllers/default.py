from datetime import datetime

def index():    
    if session.status=="" or session.status==None:
        session.clear()
        redirect(URL(c='login',f='index'))

    count_company = db(db.business_units.id>0).count()
    query = (db.projects.id > 0)
    query2 = (db.users.id > 0)
    if str(session.ams_usertype) == 'single_project':
        query &= (db.projects.project_id == session.current_project)
        query2 &= (db.users.pid == session.current_project)

    count_project = len(db(query).select(db.projects.id, distinct=True))
    count_user = db(query2).count()
    return locals()
