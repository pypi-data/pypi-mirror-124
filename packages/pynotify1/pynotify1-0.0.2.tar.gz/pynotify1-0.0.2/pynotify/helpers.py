# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 07:15:17 2021

@author: tommy
"""

import re
import time
import smtplib
import traceback
import pandas as pd
from datetime import timedelta
from email.mime.text import MIMEText
from inspect import signature, getfullargspec
from email.mime.multipart import MIMEMultipart

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  

def _parse_stack(function):
    stack = traceback.extract_stack()
    #TODO: logic for finding correct lvl, maybe have user pass it, 
    # while fn_name != fn_name_guess
    _, _, _, code = stack[-4] 
    #fn_name_guess = re.search( r"\=?([^\s|=]+)\(", code).group(1)
    fn_name = function.__name__
    return code, fn_name

def _parse_fn_signature(function):
    fn_signature = str(signature(function))
    params = re.findall(r'([^\s|^,|^\(|^\)]+)', fn_signature)
    params = [re.sub(r'=.+', '', f) for f in params]
    
    #TODO: this is same thing?
    argspec = getfullargspec(function)
    params = argspec.args
    
    return params
    
def _print_msg(printf, msg):
    if printf:
        print(f"{str(pd.to_datetime('today'))[0:-4]} | {msg}")
        
def _log_msg(logger, msg):
    #TODO: pass error and logger.error instead
    if logger is not None:
        logger.info(f"{msg}")

def _format_info(a,b):
    return 'done'

def _send_email(email, host, code, fn_name, min_exec_tm, latest_error, result,
                err_traceback):
    
    if email is None:
        return None
    
    emsg = MIMEMultipart()
    if host is None:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls() #TODO: needed when host is passed?
        s.login('py.notify1@gmail.com', 'ytbxunbpmabkvmhn')
        emsg['From'] = 'py.notify1@gmail.com' 
    else:
        s = smtplib.SMTP(host=host)
        emsg['From'] = email        
        
    emsg['To'] = email
    status = 'Successfully' if latest_error is None else 'w/ Errors'
    emsg['Subject'] = f'PyNotify: {fn_name} Executed {status} ({min_exec_tm})'
    body = 'hello world'
    emsg.attach(MIMEText(body, 'plain'))
    s.send_message(emsg)
    s.quit()
            
def _exec_func(function, email, timeit, logger, printf, notes, error, host, 
               *args, **kwargs):
    
    code, fn_name = _parse_stack(function)
    _print_msg(printf, f"executing: {code}")
    _log_msg(logger, f"executing: {code}")
        
    exec_times, latest_error, err_traceback = [], None, None
    for i in range(1,timeit+1):
        try:
            start_time = time.perf_counter() 
            result = function(*args, **kwargs)
        except Exception as err:
            latest_error = err
            err_traceback = traceback.format_exc() 
        exec_times.append(time.perf_counter() - start_time)
    min_exec_tm = str(timedelta(seconds = min(exec_times))).rstrip('0')
    result = result if latest_error is None else latest_error
    
    exec_info = _format_info(err_traceback, min_exec_tm)
    _print_msg(printf, exec_info)
    _log_msg(logger, exec_info)
    _send_email(email, host, code, fn_name, min_exec_tm, latest_error, result,
                err_traceback)
        
    if error and latest_error is not None:
        raise latest_error
    
    return result
# =============================================================================
#     ic(exec_times)
#     ic(min_exec_tm)
#     ic(code)
#     ic(fn_name)
#     ic(params)
#     ic(f"args:{args}")
#     ic(f"kwargs:{kwargs}")
# ============================================================================


