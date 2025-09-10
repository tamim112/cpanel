#main URL
# common_url = "https://my.transcombd.com"
common_url = "http://127.0.0.1:8000"

#user log function
def user_log(task_name,activity):
    from datetime import datetime
    user_ip=str(session.user_ip)
    user_browser=str(session.browser_name)
    
    task_name=str(task_name)
    activity=str(activity)
    now = datetime.now()
    log_time = date_fixed
    cid = str(session.cid)
    user_id = str(session.emp_id)
    user_name = str(session.full_name)
    request_source = str('web')
    
    db.user_logs.insert(
        cid=cid,
        task_name=task_name,
        activity=activity,
        user_id=user_id,
        user_name=user_name,
        requested_ip=user_ip,
        log_time=log_time,
        user_agent=user_browser,
        request_source=request_source
        )
    return True


#-------------------------------- role access check
def check_role(task_id):
    t_id=task_id    
    is_valid_role=False    
    task_listStr=session.task_listStr
    for i in range(len(task_listStr)):
        taskid=task_listStr[i]
        if taskid==t_id:
            is_valid_role=True
            break
        else:
            continue    
    return is_valid_role