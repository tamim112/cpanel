# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from PIL import Image
import io
from datetime import datetime
import hashlib
def encrypt_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_password = sha256_hash.hexdigest()
    return hashed_password

def index():
    task_id='user_view'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
    
    isSearch = False

    if  request.vars.cid != None and request.vars.cid != '':
        isSearch = True
    elif  request.vars.emp_id != None and request.vars.emp_id !='':
        isSearch = True
    
    elif  request.vars.status != None and request.vars.status != '':
        isSearch = True
    elif  request.vars.user_role != None and request.vars.user_role != '':
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
    SELECT * from users where 1
    """+ conditions
    users = db.executesql(sql, as_dict=True)
    

    sql = """
    SELECT * from business_units
    """
    business_units = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from projects where 1
    """ +cond
    project_lists = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from u_roles where 1
    """ +conditions
    role_lists = db.executesql(sql, as_dict=True)
    
    return locals()

def create():
    task_id='user_create'
    task_id_alt='user_create_alt'
    access_permission=check_role(task_id)  
    access_permission_alt=check_role(task_id_alt)  
    if ((access_permission==False) and (access_permission_alt==False)):
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
    SELECT * from u_roles where 1
    """ +conditions
    user_roles = db.executesql(sql, as_dict=True)
    
    sql = """
    SELECT * from projects where 1
    """ +cond
    project_lists = db.executesql(sql, as_dict=True)
    
    sql= """
    SELECT distinct user_type from users
    """
    user_types = db.executesql(sql, as_dict=True)
    
    return locals()


def submit():
    task_id='user_create'
    task_id_alt='user_create_alt'
    access_permission=check_role(task_id)  
    access_permission_alt=check_role(task_id_alt)  
    if ((access_permission==False) and (access_permission_alt==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
    rows = db(db.users.user_id).select(db.users.user_id, orderby=~db.users.id, limitby=(0, 1)).first()
    
    user_id =  rows['user_id']
    if str(user_id)=='':
        user_id='1001'
    else:
        user_id=int(user_id)+1
        
    try:
        uploaded_image = request.vars.image_path.file

        filename=user_id+'.jpg'

        # Open the image using Pillow
        img = Image.open(uploaded_image)

        # Compress the image and reduce its quality
        img = img.convert('RGB')  # Convert image to RGB (remove transparency if present)

        # Create a temporary file to save the compressed image
        temp_file = os.path.join(request.folder, 'static', 'temp.jpg')

        # Resize the image if it exceeds the maximum desired size (e.g., 100KB)
        max_size_kb = 50  # Maximum size in KB
        while True:
            img.save(temp_file, 'JPEG', quality=85)
            temp_file_size = os.path.getsize(temp_file)  # Get the size of the temporary file in bytes

            if temp_file_size <= max_size_kb * 1024:
                break  # If the size is within the desired limit, exit the loop

            # Reduce the size by 10% each iteration
            img = img.resize((int(img.width * 0.6), int(img.height * 0.5)))
        
        orginal_file = os.path.join(request.folder, 'static/images', str(filename))
        img.save(orginal_file, 'JPEG', quality=85)
        os.remove(temp_file)
        image_path = str(filename)
    except:
        image_path = "default_profile.png"

    #INSERT
    
    cid=str(request.vars.cid)
    user_role = str(request.vars.user_role)
    first_name = str(request.vars.first_name)
    last_name = str(request.vars.last_name)
    full_name = str(request.vars.first_name) +' '+ str(request.vars.last_name)
    mobile = str(request.vars.mobile)
    email = str(request.vars.email)
    gender = str(request.vars.gender)
    location = str(request.vars.location)
    passwordStr=str(request.vars.password)
    project_name = str(request.vars.project_name)
    user_type = str(request.vars.user_type).lower()
    remarks = str(request.vars.remarks)
    username = str(request.vars.username)
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
    if not user_role:
        errors.append('User Role is required.')
    if not first_name:
        errors.append('First Name is required.')
    if len(db(db.users.user_id == user_id).select()) >0:
        errors.append('User is duplicate.')
    if not email:
        errors.append('Email is required.')
    elif len(db((db.users.email == email ) & (db.users.cid == cid)  & (db.users.pid == project_name)).select()) >0:
        errors.append('Email is duplicate.')
    if not mobile:
        errors.append('Mobile is required.')
    elif len(db((db.users.mobile == mobile) & (db.users.cid == cid)  & (db.users.pid == project_name)).select()) >0:
        errors.append('Mobile is duplicate.')
    if not passwordStr:
        errors.append('Password is required.')
    # if not location:
    #     errors.append('Location is required.')
    if not user_type:
        errors.append('User Type is required.')
    if not username:
        errors.append('Username is required.')

    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('users','create'))

    user_roles=str(user_role).split('||')
    role_id=str(user_roles[0])
    user_role=str(user_roles[1])
        
    password=encrypt_password(passwordStr)
    
    #insert start
    db.users.insert(     
                cid = cid,
                pid = project_name,
                user_id = user_id,
                first_name = first_name,
                last_name = last_name,
                full_name = full_name,
                username = username,
                email = email,
                password = password,
                mobile = mobile,
                gender = gender,
                location = location,
                image_path = image_path,
                status = status,
                role_id = role_id,
                user_role = user_role,
                user_type = user_type,
                note = remarks,
                )
    #user log entry
    task_name='User'
    activity='Create'
    # user_log(task_name,activity)

    session.flash = {"msg_type":"success","msg":"User successfully added."}
    return  dict(redirect(URL('users','index')))


def edit():
    task_id='user_create'
    task_id_alt='user_create_alt'
    access_permission=check_role(task_id)  
    access_permission_alt=check_role(task_id_alt)  
    if ((access_permission==False) and (access_permission_alt==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    
    if request.args(0):
        user_data=db(db.users.id==request.args(0)).select().first()
        
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
        SELECT * from u_roles where 1
         """ +conditions
        user_roles = db.executesql(sql, as_dict=True)
        
        sql = """
        SELECT * from projects where 1
        """ +cond
        project_lists = db.executesql(sql, as_dict=True)
        
        sql= """
        SELECT distinct user_type from users
        """
        user_types = db.executesql(sql, as_dict=True)

        return dict(user_data=user_data,business_units=business_units,user_roles=user_roles,project_lists=project_lists,user_types=user_types)

def update():
    task_id='user_create'
    access_permission=check_role(task_id)  
    if (access_permission==False):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
        
    user_data=db(db.users.id==request.args(0)).select().first()
    user_id = str(user_data.user_id)
    
    try:
        uploaded_image = request.vars.image_path.file

        filename=user_id+'.jpg'

        # Open the image using Pillow
        img = Image.open(uploaded_image)

        # Compress the image and reduce its quality
        img = img.convert('RGB')  # Convert image to RGB (remove transparency if present)

        # Create a temporary file to save the compressed image
        temp_file = os.path.join(request.folder, 'static', 'temp.jpg')

        # Resize the image if it exceeds the maximum desired size (e.g., 100KB)
        max_size_kb = 50  # Maximum size in KB
        while True:
            img.save(temp_file, 'JPEG', quality=85)
            temp_file_size = os.path.getsize(temp_file)  # Get the size of the temporary file in bytes

            if temp_file_size <= max_size_kb * 1024:
                break  # If the size is within the desired limit, exit the loop

            # Reduce the size by 10% each iteration
            img = img.resize((int(img.width * 0.6), int(img.height * 0.5)))
        
        orginal_file = os.path.join(request.folder, 'static/images', str(filename))
        img.save(orginal_file, 'JPEG', quality=85)
        os.remove(temp_file)
        image_path = str(filename)
    except:
        image_path = "default_profile.png"

    cid=str(request.vars.cid)
    user_role = str(request.vars.user_role)
    
    first_name = str(request.vars.first_name)
    last_name = str(request.vars.last_name)
    full_name = str(request.vars.first_name) +' '+ str(request.vars.last_name)
    mobile = str(request.vars.mobile)
    email = str(request.vars.email)
    gender = str(request.vars.gender)
    
    location = str(request.vars.location)
    passwordStr=str(request.vars.password)
    project_name = str(request.vars.project_name)
    user_type = str(request.vars.user_type).lower()
    remarks = str(request.vars.remarks)
    username = str(request.vars.username)
    
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
    if not user_role:
        errors.append('User Role is required.')
    if not first_name:
        errors.append('First Name is required.')
    if len(db((db.users.user_id == user_id ) & (db.users.id != user_data.id)).select()) >0:
        errors.append('User is duplicate.')
    if not email:
        errors.append('Email is required.')
    elif len(db((db.users.email == email) & (db.users.cid == cid)  & (db.users.pid == project_name) & (db.users.id != user_data.id)).select()) >0:
        errors.append('Email is duplicate.')
    if not mobile:
        errors.append('Mobile is required.')
    elif len(db((db.users.mobile == mobile) & (db.users.cid == cid)  & (db.users.pid == project_name) & (db.users.id != user_data.id)).select()) >0:
        errors.append('Mobile is duplicate.')
    if not passwordStr:
        errors.append('Password is required.')
    # if not location:
    #     errors.append('Location is required.')
        
    # validation errors generate
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + ' <br>'
        session.flash = {"msg_type":"error","msg":msg}
        redirect (URL('users','edit',args=request.args(0)))
        
    # validation end 
    
    password=encrypt_password(passwordStr)
    
    user_roles=str(user_role).split('||')
    role_id=str(user_roles[0])
    user_role=str(user_roles[1])
    #employees update
    user_data.update_record(     
                        image_path = image_path,
                        cid = cid,
                        pid = project_name,
                        user_id = user_id,
                        first_name = first_name,
                        last_name = last_name,
                        full_name = full_name,
                        email = email,
                        password = password,
                        mobile = mobile,
                        gender = gender,
                        location = location,
                        status = status,
                        role_id = role_id,
                        user_role = user_role,
                        username=username,
                        user_type = user_type
                        )
    #user log entry
    task_name='User'
    activity='Update'
    # user_log(task_name,activity)        
    
    session.flash = {"msg_type":"success","msg":"User successfully updated."}
    redirect(URL('users','index'))

def delete():
    task_id='user_delete'
    access_permission=check_role(task_id)  
    if ((access_permission==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))

    
    if request.args(0):
        if len(db((db.users.id == request.args(0)) & (db.users.user_id == '1001')).select())>0:
            session.flash = {"msg_type":"error","msg":"Super Admin Can not delete"}
            return dict(redirect(URL('users','index'))) 
        
        session.flash = {"msg_type":"success","msg":"Deleted Information"}
        db(db.users.id == request.args(0)).delete()
        #user log entry
        task_name='User'
        activity='Delete'
        # user_log(task_name,activity)
        return dict(redirect(URL('users','index'))) 

def get_data():
    #Search Start##
    conditions = ''
    if str(session.ams_usertype)=='single_project':
        conditions += " and pid = '"+str(session.current_project)+"'"
        
    if  request.vars.cid != None and request.vars.cid != '':
        cid = request.vars.cid
        conditions = " and cid = '"+str(cid)+"'" 

    if  request.vars.user_id != None and request.vars.user_id !='':
        conditions = conditions +" and user_id = '"+request.vars.user_id+"'"  
    
    if  request.vars.status != None and request.vars.status != '':
        status = request.vars.status
        conditions = conditions +" and status = '"+status+"'"
        
    if  request.vars.role_id != None and request.vars.role_id !='':
        conditions = conditions +" and role_id = '"+request.vars.role_id+"'"
        
    if request.vars.project_name != None and request.vars.project_name != '':
        project_name = request.vars.project_name
        conditions = conditions + " and pid = '"+str(project_name)+"'"
    
    if session.user_role not in ['system_admin']:
        conditions += " and pid != 'ams'"
        

    #Search End## 

    ##Paginate Start##
    total_result = db.executesql("SELECT count(id) as total_row from users WHERE 1" +conditions, as_dict=True)
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
    SELECT * from users
    WHERE 1 """+conditions+""" 
    ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    data = db.executesql(sql, as_dict=True)
        ##Qurry End##

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)

#    import employee start  
def import_employees():
    task_id='user_create'
    task_id_alt='user_create_alt'
    access_permission=check_role(task_id)  
    access_permission_alt=check_role(task_id_alt)  
    if ((access_permission==False) and (access_permission_alt==False)):
        session.flash = {"msg_type":"error","msg":"Access is Denied !"}
        redirect (URL('default','index'))
        
    # if session.status=="" or session.status==None:
    #     redirect(URL(c='login',f='index'))
    
    # if session.user_role in ['management','unit_management']:
    #     return "Access Denied"

    c_id=session.cid
    if (c_id=='' or c_id==None):
        redirect(URL('default','index'))
        
    # btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0

    if request.vars.excel_data != '' and request.vars.excel_data != None:   
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)

        #   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=200:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                
                if len(coloum_list)==19:
    
                    flag = True
                    msge = ''
                    sql = """
                    SELECT * FROM `employees` where emp_id = '"""+str(coloum_list[1])+"""' or mobile = '"""+str(coloum_list[5])+"""' or email = '"""+str(coloum_list[4])+"""';
                    """

                    if(len(db.executesql(sql, as_dict=True)) != 0):
                        flag = False
                        msge = msge + 'duplicate entry; '
                    
                    if len(coloum_list[5])>11:
                        flag = False
                        msge = msge + 'Mobile number invalid; '
                        
                    designation = db((db.designations.designation_name == coloum_list[7])&(db.designations.cid == coloum_list[0])).select()
                    if(len(designation)>0):
                        designation_id = designation.first().id
                    else:
                        flag = False
                        msge = msge + 'designation not found; '

                    department = db((db.departments.dept_name == coloum_list[8])&(db.departments.cid == coloum_list[0])).select()
                    if(len(department)>0):
                        department_id = department.first().id
                    else:
                        flag = False
                        msge = msge + 'department not found; '
                    unit_id="0"
                    unit_name=""
                    if str(coloum_list[9])!="NULL" and str(coloum_list[9])!="null":
                        dept_unit = db((db.dept_units.unit_name == coloum_list[9])&(db.dept_units.cid == coloum_list[0])).select()
                        if(len(dept_unit)>0):
                            unit_id = dept_unit.first().id
                            unit_name = str(coloum_list[9])
                        else:
                            flag = False
                            msge = msge + 'unit not found; '

                    # supervisor = db((db.employees.emp_id == coloum_list[14])).select()
                    # if(len(supervisor)==0):
                    #       flag = False
                    #       msge = msge + 'supervisor not found; '

                    shifting = db((db.shiftings.shift_name == coloum_list[17])&(db.shiftings.cid == coloum_list[0])).select()
                    if(len(shifting)>0):
                        shift_id = shifting.first().id
                    else:
                        flag = False
                        msge = msge + 'shift not found; '

                    if flag:
                        db.employees.insert(     
                        cid = coloum_list[0],
                        emp_id = coloum_list[1],
                        first_name = coloum_list[2],
                        last_name = coloum_list[3],
                        full_name = coloum_list[2] + " " + coloum_list[3],
                        email = coloum_list[4],
                        mobile = coloum_list[5],
                        gender = coloum_list[6],
                        designation = designation_id,
                        desg_name = coloum_list[7],
                        department = department_id,
                        dept_name = coloum_list[8],
                        unit_id = unit_id,
                        unit_name = unit_name,
                        company_name = coloum_list[10],
                        location = coloum_list[11],
                        date_of_joining = coloum_list[12],
                        supervisor = coloum_list[13],
                        reporting_empid = coloum_list[14],
                        image_path = coloum_list[15],
                        status = coloum_list[16],
                        # shift_name = coloum_list[17],
                        shift_id = shift_id,
                        user_role = coloum_list[18]
                        )
                        count_inserted = count_inserted + 1

                        error_str = error_str + row_data + ' (succesful entry)\n'
                    else:
                        count_error = count_error + 1
                        error_str=error_str + row_data+' ('+msge+')\n'
                else:
                    count_error = count_error + 1
                    error_str=error_str + row_data+' (Number of column not Match )\n'
            
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
