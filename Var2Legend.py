# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 17:29:58 2018

@author: nhermans
"""

import matplotlib.pyplot as plt
import inspect

x,y,z = 1,2,3

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

print(retrieve_name(y))

plt.plot(x,y, label=(retrieve_name(y))[-1])
plt.legend()
