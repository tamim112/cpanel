def index():
    task_id='project_management'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))

    isSearch = False
    if  request.vars.cid != None and request.vars.cid != '':
        isSearch = True
    if  request.vars.task_id != None and request.vars.task_id !='':
        isSearch = True
    
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True) 
    conditions = ""
    if str(session.ams_usertype)=='single_project':
        conditions += " and project_id = '"+str(session.current_project)+"'"
    
    sql = """
    SELECT * from projects where 1=1 """+conditions+""" ORDER BY id DESC
    """
    project_lists = db.executesql(sql, as_dict=True) 
    return locals()

def create():
    task_id='project_management'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
    # if session.emp_role in ['management','unit_management']:
    #     return "Access Denied"
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True)
    
    return locals()

def submit():
    task_id='project_management'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
    
    cid = request.vars.cid
    project_name = request.vars.project_name
    project_description = request.vars.project_description
    if request.vars.status is not None:
        status = str(request.vars.status)
    else:
        status = "0"
    # validation
    errors =[]
    if not cid:
        errors.append('SBU is required.')
    if not project_name:
        errors.append('Project Name is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('project_list','create'))
    # validation end
    project_name=str(project_name).lower()
    project_name=str(project_name).replace(' ','_')


    old_project=db((db.projects.project_name==str(project_name)) & (db.projects.cid==str(cid))).select()
    if len(old_project) > 0:
        session.flash = {"msg_type":"error","msg":"Project Name is Duplicate"}
        redirect (URL('project_list','create'))
        
    db.projects.insert(
            cid=str(cid),
            project_id=str(project_name),
            project_name=str(project_name),
            project_description=str(project_description),
            status=str(status),
            )
    
    #user log entry
    project_name='Project List'
    activity='Create'
    # user_log(task_name,activity)    
    return  dict(redirect(URL('project_list','index')))
    
def edit():
    task_id='project_management'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    if request.args(0):        
        projects=db(db.projects.id==request.args(0)).select().first()

        sql = """
        SELECT * from business_units
        """
        business_units = db.executesql(sql, as_dict=True)

        return dict(projects=projects,business_units=business_units)

def update():
    task_id='project_management'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
        

    cid = request.vars.cid
    project_name = request.vars.project_name
    project_description = request.vars.project_description
    if request.vars.status is not None:
        status = str(request.vars.status)
    else:
        status = "0"
    # validation
    errors =[]
    if not cid:
        errors.append('SBU is required.')
    if not project_name:
        errors.append('Project Name is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('project_list','edit',args=request.args(0)))
    # validation end

    projects=db(db.projects.id==request.args(0)).select().first()

    project_name=str(project_name).lower()
    project_name=str(project_name).replace(' ','_')
    old_project=db((db.projects.project_name==str(project_name)) & (db.projects.cid==str(cid)) & (db.projects.id!=request.args(0))).select()

    if len(old_project) > 0:
        session.flash = {"msg_type":"error","msg":"Project Name is Duplicate"}
        redirect (URL('project_list','edit',args=request.args(0)))

    projects.update_record(
        cid=str(cid),
        project_id=str(project_name),
        project_name=str(project_name),
        project_description=str(project_description),
        status=str(status),
        )
    
    #user log entry
    project_name='Project List'
    activity='Update'
    # user_log(task_name,activity)        
    return  dict(redirect(URL('project_list','index')))  

## delete start##
def delete():
    task_id='project_management'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    if request.args(0):

        db(db.projects.id==request.args(0)).delete()
        session.flash = {"msg_type":"error","msg":"Information Deleted"}
        #user log entry
        project_name='Project List'
        activity='Delete'
        # user_log(task_name,activity) 
        return dict(redirect(URL('project_list','index'))) 
    ## delete end##



def get_data():

    conditions = ""
    if str(session.ams_usertype)=='single_project':
        conditions += " and project_id = '"+str(session.current_project)+"'"
    
    if  request.vars.cid != None and request.vars.cid != '':
        cid = str(request.vars.cid)
        conditions += " and cid = '"+cid+"'"
    if  request.vars.project_id != None and request.vars.project_id !='':
        id = str(request.vars.project_id)
        conditions = conditions +" and id = '"+id+"'"
    
        #Search End## 

    ##Paginate Start##
    total_result = db.executesql("SELECT count(id) as total_row from projects WHERE 1" +conditions, as_dict=True)
    total_rows = total_result[0]['total_row'] if total_result else 0
    
    
    page = int(request.vars.page or 1)
    rows_per_page = int(request.vars.rows_per_page or 10)
    if rows_per_page == -1:
            rows_per_page = total_rows
    start = (page - 1) * rows_per_page         
    end = rows_per_page
    ##Paginate End##

        ##Ordering Start##
    sort_column_index = int(request.vars['order[0][column]'] or 0)
    if sort_column_index == 0:
            sort_column_index = 1 #defult sorting column define
    sort_column_name = request.vars['columns[' + str(sort_column_index) + '][data]']
    sort_direction = request.vars['order[0][dir]']
        ##Ordering End##

        ##Querry Start##
    sql = """
    SELECT * from projects
    WHERE 1 
    """+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    data = db.executesql(sql, as_dict=True)
        ##Qurry End##

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)







