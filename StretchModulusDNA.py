# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:51:40 2018

@author: nhermans
"""

import numpy as np
import matplotlib.pyplot as plt
import os
 
folder = r'P:\18S FitFiles\Leiden_wt'
filenames = os.listdir(folder)
os.chdir(folder)

def read_fit(Filename):
    """Open .dat/.fit files from magnetic tweezers"""
    f = open(Filename, 'r')
    #get headers
    headers = f.readlines()[0]
    headers = headers.split('\t')
    #get data
    f.seek(0) #seek to beginning of the file
    data = f.readlines()[1:]
    f.close()
    F = np.array([])
    Z_Selected = np.array([])
    for idx,item in enumerate(data):                                            #Get all the data from the fitfile
        F = np.append(F,float(item.split()[headers.index('F (pN)')]))
        Z_Selected = np.append(Z_Selected,float(item.split()[headers.index('selected z (um)')])*1000)
    F = np.delete(F, np.argwhere(np.isnan(Z_Selected)))
    Z_Selected = np.delete(Z_Selected, np.argwhere(np.isnan(Z_Selected)))
    return F, Z_Selected

def breaks(F, Z, Jump=1000):
    """Removes the data after a jump in z, presumably indicating the bead broke lose"""
    Test = Z[0]
    for i,x in enumerate(Z[1:]):
        if abs(x - Test) > Jump :
            F = F[:i]
            Z = Z[:i] 
            break
        Test = x
    return F, Z

def removerelease(F, Z):
    """Removes the release curve from the selected data"""
    F_diff = np.diff(F)
    F_diff = np.insert(F_diff,0,0)
    F = F[F_diff>0]
    Z = Z[F_diff>0]
    return F, Z

def maxforce(F, Z,  Max_Force=0.5):
    """Removes the data below minimum force given"""
    Z = Z[F<Max_Force]
    F = F[F<Max_Force]
    return F, Z

def read_log(Filename):
    """Open the corresponding .log files from magnetic tweezers. Returns False if the file is not found"""
    try: 
        f = open(Filename, 'r')
    except FileNotFoundError: 
        print(Filename, '========> No valid logfile found')
        return False   
    lines = f.readlines()
    f.close()
    return lines

def log_pars(LogFile):
    """Reads in parameters from the logfile generate by the labview fitting program, returns a {dict} with 'key'= paramvalue"""
    par = {}
    par['L_bp'] = float(find_param(LogFile, 'L DNA (bp)'))
    par['P_nm'] = float(find_param(LogFile, 'p DNA (nm)'))
    par['S_pN'] = float(find_param(LogFile, 'S DNA (pN)'))
    par['degeneracy'] = 0
    par['z0_nm'] = 2
    par['k_pN_nm'] = float(find_param(LogFile, 'k folded (pN/nm)'))
    par['N_tot'] = float(find_param(LogFile, 'N nuc'))
    par['N4'] = float(find_param(LogFile, 'N unfolded [F0]'))
    par['NRL_bp'] = float(find_param(LogFile, 'NRL (bp)'))
    par['ZFiber_nm'] = float(find_param(LogFile, 'l folded (nm)'))
    par['G1_kT'] = 3
    par['G2_kT'] = 4
    par['DNAds_nm'] = 0.34 # rise per basepair (nm)
    par['kBT_pN_nm'] = 4.2 #pn/nm 
    par['Innerwrap_bp'] = 79 #number of basepairs in the inner turn wrap
    par['Fiber0_bp'] = par['L_bp']-(par['N_tot']*par['Innerwrap_bp'])  #Transition between fiber and beats on a string
    par['LFiber_bp'] = (par['N_tot']-par['N4'])*(par['NRL_bp']-par['Innerwrap_bp'])  #total number of bp in the fiber
    par['FiberStart_bp']  = par['Fiber0_bp']-par['LFiber_bp']
    par['MeasurementERR (nm)'] = 5
    return par

def find_param(Logfile, Param):
    """Find a parameter in the .log file"""
    for lines in Logfile:
        P = lines.split(' = ')
        if P[0]==Param:
            return P[1].strip('\n')
    print("<<<<<<<<<<", Param, "not found >>>>>>>>>>")
    return 0

Z_m_array = np.array([])
StretchingModulus = np.array([])

Filenames = []                                                                  #All .fit files    
for filename in filenames:
    if filename[-4:] == '.log':
        Filenames.append(filename)        
        
for Filenum, Filename in enumerate(Filenames):
    LogFile = read_log(Filename)                             #loads the log file with the same name
    if LogFile: Pars = log_pars(LogFile)                                 #Reads in all the parameters from the logfile
    else: continue              
    try: F,Z = read_fit(Filename[:-4]+'.fit')
    except FileNotFoundError: continue
    F,Z = removerelease(F,Z)
    #F,Z = breaks(F,Z)
    F,Z = maxforce(F,Z,0.3)
    #Z_m = np.mean(Z)
    Z = np.sort(Z)
    Z_m=np.mean(Z[0:20])
    print(Filename, 'Z = ', Z_m , 'Stretching modulus = ', Pars['S_pN'])
    Z_m_array = np.append(Z_m_array, Z_m)
    StretchingModulus = np.append(StretchingModulus, Pars['S_pN'])

fig2 , ax2 = plt.subplots()
ax2.scatter(StretchingModulus,Z_m_array, alpha=0.5)
ax2.set_xlabel('Stretching Modulus (pN)')
ax2.set_ylabel('Start Offset (nm)')
ax2.set_title("Radius vs Stretching Modulus")
fig2.show()
