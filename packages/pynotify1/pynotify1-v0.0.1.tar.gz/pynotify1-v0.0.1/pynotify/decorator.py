# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 07:15:17 2021

@author: tommy
"""

from functools import wraps, partial
from .helpers import _exec_func

def notify(function=None, *, email=None, timeit=1, logger=None, printf=False,
           notes=None, error=True, host=None, persist=False, test=False):
    if test:
        def test_func():
            return "Pass"
        function = test_func
    if persist:
        return partial(notify, email=email, timeit=timeit, logger=logger, 
                       printf=printf, notes=notes, error=error, host=host)
    if function is None: # if @notifiy is used w/ args passed, return decorator
        return partial(notify, email=email, timeit=timeit, logger=logger, 
                       printf=printf, notes=notes, error=error, host=host)
    @wraps(function)
    def wrapper(*args, **kwargs):
        return _exec_func(function, email, timeit, logger, printf, notes,  
                          error, host, *args, **kwargs)
    if test:
        return wrapper()
    return wrapper