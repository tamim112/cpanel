from datetime import datetime

def index():    
    if session.status=="" or session.status==None:
        session.clear()
        redirect(URL(c='login',f='index'))

    count_company = db(db.business_units.id>0).count()
    count_project = len(db(db.projects.id>0).select(db.projects.id, distinct=True))
    count_user = db(db.users.id>0).count()
    return locals()
