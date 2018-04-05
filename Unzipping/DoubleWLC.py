# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 15:03:46 2017

@author: nhermans
"""
import numpy as np
import matplotlib.pyplot as plt


#open file:
FilePath="D:\\test\\170710_data_101_0.fit" #work-pc

#headers
f = open(FilePath, 'r')
headers_lines=f.readlines()[0]
f.close()
f = open(FilePath, 'r')
data_lines=f.readlines()[1:]
f.close()
    
headers=[]
headers=headers_lines.split('\t')

Force=[]
y=[]
Time=[] 
Extension=[]

for n,x in enumerate(data_lines):
    Force.append(float(x.split()[headers.index('F (pN)')])) 
    Time.append(float(x.split()[headers.index('t (s)')]))
    Extension.append(float(x.split()[headers.index('z (um)')]))
       
Force=np.array(Force)
Time=np.array(Time)
Extension=np.array(Extension)
Extension_nm = [x * 1000 for x in Extension]

#functions
kT=4.1 #pn nm
def ex_WLC(f, p, L, S):
    return L*(1-0.5*(np.sqrt(kT/(f*p)))+f/S)

def WLC(f, p, L, S):
    return L*(1-0.5*(np.sqrt(kT/(f*p))))

def WLC_FJC(f,CLss_nm): #WLC extensible + WLC
    return (CLds_nm*(1-0.5*np.sqrt(Kb*T/(f*PLds))+f/SM))+ (CLss_nm*(1-0.5*np.sqrt(Kb*T/(f*PLss))))

#split data in unzipping and annealing
timeup = []
timedown = []
extensionup = []
extensiondown = []
forceup = []
forcedown = []
      
for i in range(0,len(Force)-1):
    if Force[i] <= Force[i+1]:
            timeup.append(Time[i])
            extensiondown.append(Extension_nm[i])
            forcedown.append(Force[i])
    else:
            timedown.append(Time[i])
            extensionup.append(Extension_nm[i])
            forceup.append(Force[i])
            
#Contour length histogram generation

#down generation
index_down = list(range(0,len(extensiondown)))
CLss_down_array = list(range(0,len(extensiondown)))
CLss_down = []

for i in index_down:
    CLss_down_array[i], cov = curve_fit(WLC_FJC, forcedown[i],extensiondown[i])
    
CLss_down = np.concatenate(CLss_down_array).ravel().tolist()

index_up = list(range(0,len(extensionup)))
CLss_up_array = list(range(0,len(extensionup)))
CLss_up = []

#Up generation
for i in index_up:
    CLss_up_array[i], cov = curve_fit(WLC_FJC, forceup[i],extensionup[i])
    
CLss_up = np.concatenate(CLss_up_array).ravel().tolist()

CLss_up_bp = [x /1.36 for x in CLss_up]
CLss_down_bp = [x /1.36 for x in CLss_down]

#Contour length histogram generation
CLss_down_array = list(range(0,len(extensiondown)))
CLss_down = []
Guess=1

for i in CLss_down_array:
    #CLss_down_array[i], cov = curve_fit(WLC_FJC, forcedown[i],extensiondown[i])
    Solution = fsolve(lambda CLss_nm : extensionup[i]-(CLds_nm*(1-0.5*np.sqrt(Kb*T/(forceup[i]*PLds))+forceup[i]/SM))+ (CLss_nm*(1-0.5*np.sqrt(Kb*T/(forceup[i]*PLss)))), Guess)
    CLss_down_array[i]=Solution
#CLss_down = np.concatenate(CLss_down_array).ravel().tolist()

CLss_up_array = list(range(0,len(extensionup)))
CLss_up = []

for i in CLss_up_array:#Up generation
    #CLss_up_array[i], cov = curve_fit(WLC_FJC, forceup[i],extensionup[i])
    Solution = fsolve(lambda CLss_nm : extensionup[i]-(CLds_nm*(1-0.5*np.sqrt(Kb*T/(forceup[i]*PLds))+forceup[i]/SM))+ (CLss_nm*(1-0.5*np.sqrt(Kb*T/(forceup[i]*PLss)))), Guess)
    CLss_up_array[i]=Solution
    Guess=Solution
#CLss_up = np.concatenate(CLss_up_array).ravel().tolist()
