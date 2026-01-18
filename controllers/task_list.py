def index():
    task_id='task_manage'
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
        
    conditions = ''
    cond=""
    if session.user_role not in ['system_admin']:
        conditions += " and pid != 'ams'"
        cond=" and project_id != 'ams'"
    
    if str(session.ams_usertype)=='single_project':
        conditions += " and pid = '"+str(session.current_project)+"'"
        cond += " and project_id = '"+str(session.current_project)+"'"
    
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True) 
    
    sql = """
    SELECT * from projects WHERE 1 """ + cond
    project_lists = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from u_task_group WHERE 1 """ + conditions
    task_groups = db.executesql(sql, as_dict=True) 
    
    sql = """
    SELECT * from u_tasks WHERE 1 """ + conditions
    task_lists = db.executesql(sql, as_dict=True) 
    return locals()

def create():
    task_id='task_manage'
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
        conditions += " and pid = '"+str(session.current_project)+"'"
        cond += " and project_id = '"+str(session.current_project)+"'"
        
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from projects WHERE 1 """ + cond 
    project_lists = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from u_task_group WHERE 1 """ + conditions

    task_groups = db.executesql(sql, as_dict=True)
    return locals()

def submit():
    task_id='task_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
    
    cid = request.vars.cid
    project_name = request.vars.project_name
    group_id = request.vars.group_id
    task_name = request.vars.task_name
    task_description = request.vars.task_description
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
    if not group_id:
        errors.append('Group Name is required.')
    if not task_name:
        errors.append('Task Name is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('task_list','create'))
    # validation end
    task_name=str(task_name).lower()
    task_name=str(task_name).replace(' ','_')
    
    group=str(group_id).split('||')
    group_id=str(group[0])
    group_name=str(group[1])

    old_task=db((db.u_tasks.task_name==str(task_name)) & (db.u_tasks.cid==str(cid)) & (db.u_tasks.pid==str(project_name))).select()
    if len(old_task) > 0:
        session.flash = {"msg_type":"error","msg":"Task Name is Duplicate"}
        redirect (URL('task_list','create'))
        
    db.u_tasks.insert(
            cid=str(cid),            
            pid=str(project_name),
            task_name=str(task_name),
            task_description=str(task_description),
            group_id=str(group_id),
            group_name=str(group_name),
            status=str(status),
            )
    
    #user log entry
    task_name='Task List'
    activity='Create'
    # user_log(task_name,activity)    
    return  dict(redirect(URL('task_list','index')))
    
def edit():
    task_id='task_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))


    if request.args(0):        
        tasks=db(db.u_tasks.id==request.args(0)).select().first()
        
        if session.user_role not in ['system_admin'] and tasks.pid == "ams":
            session.flash = {"msg_type":"error","msg":"Access is Denied !"}
            redirect (URL('default','index'))
        
        conditions = ''
        cond=""
        if session.user_role not in ['system_admin']:
            conditions += " and pid != 'ams'"
            cond=" and project_id != 'ams'"
        
        if str(session.ams_usertype)=='single_project':
            conditions += " and pid = '"+str(session.current_project)+"'"
            cond += " and project_id = '"+str(session.current_project)+"'"
            
        sql = """
        SELECT * from business_units
        """
        business_units = db.executesql(sql, as_dict=True)
        
        sql = """
        SELECT * from projects WHERE 1 """ + cond
        project_lists = db.executesql(sql, as_dict=True)

        sql = """
        SELECT * from u_task_group WHERE 1 """ + conditions

        task_groups = db.executesql(sql, as_dict=True)
        return dict(tasks=tasks,task_groups=task_groups,business_units=business_units, project_lists=project_lists)

def update():
    task_id='task_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
        

    cid = request.vars.cid
    project_name = request.vars.project_name
    group_id = request.vars.group_id
    task_name = request.vars.task_name
    task_description = request.vars.task_description
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
    if not group_id:
        errors.append('Group Name is required.')
    if not task_name:
        errors.append('Task Name is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('task_list','edit',args=request.args(0)))
    # validation end
    
    tasks=db(db.u_tasks.id==request.args(0)).select().first()
    
    task_name=str(task_name).lower()
    task_name=str(task_name).replace(' ','_')
    
    group=str(group_id).split('||')
    group_id=str(group[0])
    group_name=str(group[1])

    old_task=db((db.u_tasks.task_name==str(task_name)) & (db.u_tasks.cid==str(cid)) & (db.u_tasks.pid==str(project_name)) & (db.u_tasks.id!=request.args(0))).select()
    if len(old_task) > 0:
        session.flash = {"msg_type":"error","msg":"Task Name is Duplicate"}
        redirect (URL('task_list','edit',args=request.args(0)))

    tasks.update_record(
        cid=str(cid),
        pid=str(project_name),
        task_name=str(task_name),
        task_description=str(task_description),
        group_id=str(group_id),
        group_name=str(group_name),
        status=str(status),
        )
    
    #user log entry
    task_name='Task List'
    activity='Update'
    # user_log(task_name,activity)        
    return  dict(redirect(URL('task_list','index')))  

## delete start##
def delete():
    task_id='task_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    
    if request.args(0):
        role_tasks=db(db.u_role_has_tasks.task_id==request.args(0)).select()
        if len(role_tasks) > 0:
            session.flash = {"msg_type":"error","msg":"Task Already Used!"}
            redirect (URL('task_list','index'))
            
        session.flash = {"msg_type":"error","msg":"Information Deleted"}
        db(db.u_tasks.id==request.args(0)).delete()
        #user log entry
        task_name='Task List'
        activity='Delete'
        # user_log(task_name,activity) 
        return dict(redirect(URL('task_list','index'))) 
    ## delete end##



def get_data():
    task_id='task_manage'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    conditions = ""
    if str(session.ams_usertype)=='single_project':
        conditions += " and pid = '"+str(session.current_project)+"'"
        
    if  request.vars.cid != None and request.vars.cid != '':
        cid = str(request.vars.cid)
        conditions += " and cid = '"+cid+"'"
    if  request.vars.project_name != None and request.vars.project_name !='':
        project_name = str(request.vars.project_name)
        conditions += " and pid = '"+project_name+"'"
    if  request.vars.group_id != None and request.vars.group_id !='':
        group_id = str(request.vars.group_id)
        conditions += " and group_id = '"+group_id+"'"
        
    if  request.vars.task_id != None and request.vars.task_id !='':
        id = str(request.vars.task_id)
        conditions = conditions +" and id = '"+id+"'"
    
        #Search End## 
    if session.user_role not in ['system_admin']:
        conditions += " and pid != 'ams'"

    ##Paginate Start##
    total_result = db.executesql("SELECT count(id) as total_row from u_tasks WHERE 1" +conditions, as_dict=True)
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
    SELECT * from u_tasks
    WHERE 1 
    """+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    data = db.executesql(sql, as_dict=True)
        ##Qurry End##

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)







def utility():
    task_id='task_manage'
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
        conditions += " and pid = '"+str(session.current_project)+"'"
        cond += " and project_id = '"+str(session.current_project)+"'"
        
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from projects WHERE 1 """ + cond 
    project_lists = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from u_task_group WHERE 1 """ + conditions

    task_groups = db.executesql(sql, as_dict=True)
    return locals()

def normalize_to_list(val):
    if not val:
        return []

    # already a list (JS / multiple rows)
    if isinstance(val, (list, tuple)):
        return [str(v).strip() for v in val if str(v).strip()]

    # single value
    return [str(val).strip()]

def json_error(msg):
    return response.json({
        "status": "error",
        "message": msg
    })

def json_success(msg):
    return response.json({
        "status": "success",
        "message": msg
    })



def bulk_task():
    task_id = 'task_manage'
    access_permission = check_role(task_id)

    if not access_permission:
        return json_error("Access is Denied!")

    if not request.vars.cid:
        return json_error("Invalid request")

    cid = request.vars.cid
    project_name = request.vars.project_name
    group_id = request.vars.group_id
    task_name = request.vars.task_name
    task_description = request.vars.task_description

    group_list = normalize_to_list(group_id)
    task_names_list = normalize_to_list(task_name)
    task_description_list = normalize_to_list(task_description)

    errors = []
    if not cid:
        errors.append("SBU is required")
    if not project_name:
        errors.append("Project Name is required")
    if not group_list:
        errors.append("Group Name is required")
    if not task_names_list:
        errors.append("Task Name is required")

    if errors:
        return json_error(" | ".join(errors))

    task_list_added = []
    error_tasks = []

    for i in range(len(task_names_list)):
        t_name = str(task_names_list[i]).strip().lower().replace(" ", "_")
        t_desc = task_description_list[i] if i < len(task_description_list) else ""

        grp = str(group_list[i]).split("||") if i < len(group_list) else ["", ""]
        gid, gname = grp[0], grp[1]

        exists = db(
            (db.u_tasks.task_name == t_name) &
            (db.u_tasks.cid == cid) &
            (db.u_tasks.pid == project_name)
        ).count()

        if exists:
            error_tasks.append(t_name)
        else:
            task_list_added.append({
                "cid": cid,
                "pid": project_name,
                "task_name": t_name,
                "task_description": t_desc,
                "group_id": gid,
                "group_name": gname,
                "status": "1",
            })

    if error_tasks:
        return json_error("Task already exists: " + ", ".join(error_tasks))

    if task_list_added:
        db.u_tasks.bulk_insert(task_list_added)

    return json_success("Task List Added Successfully 🔥")




