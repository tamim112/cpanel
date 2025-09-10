# -- coding: utf-8 --

#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:d6160708-08e3-4217-bd9e-e9a550109a8d'   # before define_tables()
#auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
# Common Variable
#mreporting_http_pass='abC321'
# ' " / \ < > ( ) [ ] { } ,

#======================date========================
import datetime
import os

datetime_fixed=str(date_fixed)[0:19]    # default datetime 2012-07-01 11:48:10
current_date=str(date_fixed)[0:10]   # default date 2012-07-01

first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

#================mytranscom_Database===================
#--------------------------- signature
signature=db.Table(db,'signature',
                Field('field1','string',length=100,default=''), 
                Field('field2','integer',default=0),
                Field('note','string',length=255,default=''),  
                Field('created_on','datetime',default=date_fixed),
                Field('created_by',default=session.emp_id),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=session.emp_id),
                )

#*******************Start Admin Tables*******************
#=====================Business Unit================
db.define_table('business_units',
                Field('sbu_prefix','string',length=20,requires=IS_NOT_EMPTY()),
                Field('sbu_name','string',length=20,requires=IS_NOT_EMPTY()),
                Field('sbu_full_name','string',length=100,requires=IS_NOT_EMPTY()),
                Field('sbu_location','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,requires=IS_NOT_EMPTY(),default=1),
                signature,
                migrate=False
                )
#=====================Business Unit================

#=====================Projects================

db.define_table('projects',
                Field('cid','string',length=20,requires=IS_NOT_EMPTY(),default=session.cid),
                Field('project_id','string',length=20,requires=IS_NOT_EMPTY()),
                Field('project_name','string',length=100,requires=IS_NOT_EMPTY()),
                Field('project_description','string',length=200,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,requires=IS_NOT_EMPTY(),default=1),
                signature,
                migrate=False
                )
#=====================Projects================

#=====================Task group================
db.define_table('u_task_group',
                Field('cid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('pid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('group_name','string',length=200,requires=IS_NOT_EMPTY()),
                Field('group_description','string',length=200,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )

#=====================Tasks================
db.define_table('u_tasks',
                Field('cid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('pid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('task_name','string',length=200,requires=IS_NOT_EMPTY()),
                Field('task_description','string',length=200,requires=IS_NOT_EMPTY()),
                Field('group_id','string',length=20,requires=IS_NOT_EMPTY()),
                Field('group_name','string',length=100,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )

#=====================Roles================
db.define_table('u_roles',
                Field('cid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('pid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('role_name','string',length=200,requires=IS_NOT_EMPTY()),
                Field('role_description','string',length=200,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )

#=====================Role Has Tasks================
db.define_table('u_role_has_tasks',
                Field('cid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('pid','string',length=20,requires=IS_NOT_EMPTY()),
                Field('role_id','string',length=20,requires=IS_NOT_EMPTY()),
                Field('role_name','string',length=100,requires=IS_NOT_EMPTY()),
                Field('task_id','string',length=20,requires=IS_NOT_EMPTY()),
                Field('task_name','string',length=200,requires=IS_NOT_EMPTY()),
                Field('group_id','string',length=20,requires=IS_NOT_EMPTY()),
                Field('group_name','string',length=100,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )

#*******************End Admin Tables*******************



#=====================Employees Table================
db.define_table('users',
                Field('cid','string',length=20,requires=IS_NOT_EMPTY(),default=session.cid),
                Field('pid','string',length=50,requires=IS_NOT_EMPTY(),default=session.cid),
                
                Field('user_id','string',length=20,unique=True,requires=IS_NOT_EMPTY()),
                Field('first_name','string',length=100),
                Field('last_name','string',length=100),
                Field('full_name','string',length=200),
                Field('email','string',length=200),
                Field('username','string',unique=True,length=100),
                Field('mobile','string',length=20),
                Field('password','string',length=256,default='-'),
                Field('gender','string',length=10),
                Field('location','string',length=100),
                Field('user_type','string',length=20,default='general'), # employee,admin,management,unit_system_admin,unit_management
                Field('image_path','string',length=200),
                Field('role_id','string',length=10),
                Field('user_role','string',length=100),
                Field('status','integer',length=1,default=1),
                
                Field('device_id','string',length=100,default='-'),
                Field('sync_code','integer',default=0),
                Field('app_version','string',length=50),
                Field('otp_token','integer',length=6,default=0),
                Field('token_expire_time','datetime'),
                Field('otp_status','integer',length=1,default=0),

                signature,
                migrate=False
                )
