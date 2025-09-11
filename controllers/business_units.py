def index():
    task_id='company_management'
    access_permission=check_role(task_id)   
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    isSearch = False

    if  request.vars.cid != None and request.vars.cid !='':
       isSearch = True
    conditions=''

    
    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True)

    return locals()   
  
def create():
    task_id='company_management'
    access_permission=check_role(task_id)   
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    
    return locals()



def submit():
    task_id='company_management'
    access_permission=check_role(task_id)   
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
        
    if request.vars.status is not None:
        status = str(request.vars.status)
    else:
        status = "0"

    # validation
    errors =[]
    if not request.vars.sbu_prefix:
        errors.append('SBU Prefix is required.')  
    elif len(db((db.business_units.sbu_prefix == request.vars.sbu_prefix)).select()) >0:
        errors.append('SBU Prefix is duplicate.')

    if not request.vars.sbu_name:
        errors.append('SBU Short Name is required.')
    elif len(db((db.business_units.sbu_name == request.vars.sbu_name)).select()) >0:
        errors.append('SBU Short Name is duplicate.')
            
    if not request.vars.sbu_full_name:
        errors.append('SBU Full Name is required.')
    elif len(db((db.business_units.sbu_full_name == request.vars.sbu_full_name)).select()) >0:
        errors.append('SBU Full Name is duplicate.')
        
    if not request.vars.sbu_location:
        errors.append('SBU location is required.')
        
    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('business_units','create'))
    # validation end

    db.business_units.insert(
        sbu_prefix=str(request.vars.sbu_prefix),
        sbu_name=str(request.vars.sbu_name),
        sbu_full_name=str(request.vars.sbu_full_name),
        sbu_location=str(request.vars.sbu_location),
        status=str(status))
    #user log entry
    task_name='Business Unit'
    activity='Create'
    # user_log(task_name,activity)
    return dict(redirect(URL('business_units','index')))



def edit():

    task_id='company_management'
    access_permission=check_role(task_id)   
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    if request.args(0):
        business_units = db(db.business_units.id == request.args(0)).select().first()
                
        return dict(business_units=business_units)

def update():
    task_id='company_management'
    access_permission=check_role(task_id)   
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    
    business_units = db(db.business_units.id == request.args(0)).select().first()
    if request.vars.status is not None:
        status = str(request.vars.status)
    else:
        status = "0"

    # validation
    errors =[]
    if not request.vars.sbu_prefix:
        errors.append('SBU Prefix is required.')  
    elif len(db((db.business_units.sbu_prefix == request.vars.sbu_prefix) & (db.business_units.id != business_units.id)).select()) >0:
        errors.append('SBU Prefix is duplicate.')

    if not request.vars.sbu_name:
        errors.append('SBU Short Name is required.')
    elif len(db((db.business_units.sbu_name == request.vars.sbu_name) & (db.business_units.id != business_units.id)).select()) >0:
        errors.append('SBU Short Name is duplicate.')
            
    if not request.vars.sbu_full_name:
        errors.append('SBU Full Name is required.')
    elif len(db((db.business_units.sbu_full_name == request.vars.sbu_full_name) & (db.business_units.id != business_units.id)).select()) >0:
        errors.append('SBU Full Name is duplicate.')
        
    if not request.vars.sbu_location:
        errors.append('SBU location is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('business_units','edit',args=request.args(0)))
    # validation end

    business_units.update_record(
        sbu_prefix=str(request.vars.sbu_prefix),
        sbu_name=str(request.vars.sbu_name),
        sbu_full_name=str(request.vars.sbu_full_name),
        sbu_location=str(request.vars.sbu_location),
        status=str(status)) 
    #user log entry
    task_name='Business Unit'
    activity='Update'
    # user_log(task_name,activity)
    redirect(URL('business_units','index'))


def delete():
    task_id='company_management'
    access_permission=check_role(task_id)   
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    if request.args(0):
        session.flash = T("Deleted Information")
        db(db.business_units.id == request.args(0)).delete()
    #user log entry
    task_name='Business Unit'
    activity='Delete'
    # user_log(task_name,activity)
    # session.flash = T("Deleted Information")
    return dict(redirect(URL('business_units', 'index')))

def get_data():
    #Search Start##
    conditions = ""
    if  request.vars.cid != None and request.vars.cid !='':
        cid = str(request.vars.cid)
        conditions += " and sbu_name = '"+cid+"'"
    #Search End## 

    ##Paginate Start##
    # total_rows = db(db.departments).count()
    total_rows = len(db.executesql("SELECT * FROM `business_units` where 1" +conditions, as_dict=True))
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
        sort_column_index = 0 #defult sorting column define
    sort_column_name = request.vars['columns[' + str(sort_column_index) + '][data]']
    sort_direction = request.vars['order[0][dir]']
    ##Ordering End##

    ##Querry Start##
    sql = """
    SELECT * FROM `business_units` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    data = db.executesql(sql, as_dict=True)
    ##Qurry End##

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)




