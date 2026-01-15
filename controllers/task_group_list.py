def index():
    task_id='task_group_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    isSearch = False
    if  request.vars.cid != None and request.vars.cid != '':
        isSearch = True
    if  request.vars.group_id != None and request.vars.group_id !='':
        isSearch = True
    
    conditions = ''
    cond=""
    if session.user_role not in ['system_admin']:
        conditions += " and pid != 'ams'"
        cond=" and project_id != 'ams'"
        
    if str(session.ams_usertype)=='single_project':
        cond += " and project_id = '"+str(session.current_project)+"'"
        conditions += " and pid = '"+str(session.current_project)+"'"
    
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True) 
    
    sql = """
    SELECT * from u_task_group WHERE 1
    """ + conditions
    group_lists = db.executesql(sql, as_dict=True) 
    
    sql = """
    SELECT * from projects WHERE 1
    """ + cond
    project_lists = db.executesql(sql, as_dict=True)

    return locals()

def create():
    task_id='task_group_manage'
    access_permission=check_role(task_id) 
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
        
    conditions = ''
    cond=""
    if session.user_role not in ['system_admin']:
        conditions += " and pid != 'ams'"
        cond=" and project_id != 'ams'"
        
    if str(session.ams_usertype)=='single_project':
        cond += " and project_id = '"+str(session.current_project)+"'"
        
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from projects WHERE 1
    """ + cond
    project_lists = db.executesql(sql, as_dict=True)
    
    return locals()

def submit():
    task_id='task_group_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
    
    cid = request.vars.cid
    project_name = request.vars.project_name
    group_name = request.vars.group_name
    group_description = request.vars.group_description
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
    if not group_name:
        errors.append('Group Name is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('task_group_list','create'))
    # validation end
    
    group_name=str(group_name).lower()
    group_name=str(group_name).replace(' ','_')

    old_group=db((db.u_task_group.group_name==str(group_name)) & (db.u_task_group.cid==str(cid)) & (db.u_task_group.pid==str(project_name))).select()
    if len(old_group) > 0:
        session.flash = {"msg_type":"error","msg":"Group Name is Duplicate"}
        redirect (URL('task_group_list','create'))
        
    db.u_task_group.insert(
            cid=str(cid),
            pid=str(project_name),
            group_name=str(group_name),
            group_description=str(group_description),
            status=str(status),
            )
    
    #user log entry
    task_name='Group List'
    activity='Create'
    # user_log(task_name,activity)    
    return  dict(redirect(URL('task_group_list','index')))
    
def edit():    
    task_id='task_group_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))


    if request.args(0):        
        task_groups=db(db.u_task_group.id==request.args(0)).select().first()
        
        if session.user_role not in ['system_admin'] and task_groups.pid == "ams":
            session.flash = {"msg_type":"error","msg":"Access is Denied !"}
            redirect (URL('default','index'))
        
        conditions = ''
        cond=""
        if session.user_role not in ['system_admin']:
            conditions += " and pid != 'ams'"
            cond=" and project_id != 'ams'"
            
        if str(session.ams_usertype)=='single_project':
            cond += " and project_id = '"+str(session.current_project)+"'"
            
        sql = """
        SELECT * from business_units
        """
        business_units = db.executesql(sql, as_dict=True)
        
        sql = """
        SELECT * from projects WHERE 1
        """ + cond
        project_lists = db.executesql(sql, as_dict=True)

        return dict(task_groups=task_groups,business_units=business_units, project_lists=project_lists)

def update():
    task_id='task_group_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
        

    cid = request.vars.cid
    project_name = request.vars.project_name
    group_name = request.vars.group_name
    group_description = request.vars.group_description
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
    if not group_name:
        errors.append('Group Name is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('task_group_list','edit',args=request.args(0)))
    # validation end
    
    task_groups=db(db.u_task_group.id==request.args(0)).select().first()
    group_name=str(group_name).lower()
    group_name=str(group_name).replace(' ','_')

    old_task_group=db((db.u_task_group.group_name==str(group_name)) & (db.u_task_group.cid==str(cid)) & (db.u_task_group.pid==str(project_name)) & (db.u_task_group.id!=request.args(0))).select()
    if len(old_task_group) > 0:
        session.flash = {"msg_type":"error","msg":"Group Name is Duplicate"}
        redirect (URL('task_group_list','edit',args=request.args(0)))

    task_groups.update_record(
        cid=str(cid),
        pid=str(project_name),
        group_name=str(group_name),
        group_description=str(group_description),
        status=str(status),
        )
    
    #user log entry
    task_name='Group List'
    activity='Update'
    # user_log(task_name,activity)        
    return  dict(redirect(URL('task_group_list','index')))  

## delete start##
def delete():
    task_id='task_group_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))

    # if session.emp_role in ['management','unit_management','unit_system_admin']:
    #         return "Access Denied"
    
    if request.args(0):
        task_groups=db(db.u_tasks.group_id==request.args(0)).select()
        if len(task_groups) > 0:
            session.flash = {"msg_type":"error","msg":"Group Already Used!"}
            redirect (URL('task_group_list','index'))
            
        session.flash = {"msg_type":"error","msg":"Information Deleted"}
        db(db.u_task_group.id==request.args(0)).delete()
        #user log entry
        task_name='Group List'
        activity='Delete'
        # user_log(task_name,activity) 
        return dict(redirect(URL('task_group_list','index'))) 
    ## delete end##



def get_data():    
    task_id='task_group_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
        #Search Start##
    conditions = ""
    
    if str(session.ams_usertype)=='single_project':
        conditions += " and pid = '"+str(session.current_project)+"'"
    
    if  request.vars.cid != None and request.vars.cid != '':
        cid = str(request.vars.cid)
        conditions += " and cid = '"+cid+"'"
    if  request.vars.project_name != None and request.vars.project_name !='':
        project_name = str(request.vars.project_name)
        conditions = conditions +" and pid = '"+project_name+"'"
    if  request.vars.group_id != None and request.vars.group_id !='':
        id = str(request.vars.group_id)
        conditions = conditions +" and id = '"+id+"'"
    
        #Search End## 

    if session.user_role not in ['system_admin']:
        conditions += " and pid != 'ams'"

    ##Paginate Start##
    total_result = db.executesql("SELECT count(id) as total_row from u_task_group WHERE 1" +conditions, as_dict=True)
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
    SELECT * from u_task_group
    WHERE 1 
    """+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    data = db.executesql(sql, as_dict=True)
        ##Qurry End##

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)







