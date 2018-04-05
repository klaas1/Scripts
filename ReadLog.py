# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 10:56:15 2018

@author: nhermans
"""
import numpy as np
import os #filenames
import matplotlib.pyplot as plt

def read_log(Filename):
    f = open(Filename, 'r')
    lines=f.readlines()
    f.close()
    return lines

def find_param(Logfile, Param):
    for lines in Logfile:
        P =lines.split(' = ')
        if P[0]==Param:
            return P[1].strip('\n')
    return False

def count_nuc(folder):    
    Nuc,Tetra=np.array([]),np.array([])
    for Filename in filenames:
        if Filename[-4:] != '.log' :
            continue
        LogFile=read_log(Filename[:-4]+'.log')
        if LogFile == False: continue
        N_tot = float(find_param(LogFile,'N nuc') )#number of nucleosomes N nuc
        if is_number(N_tot) == False : continue 
        N_tetra = float(find_param(LogFile,'N unfolded [F0]'))
        Nuc=np.append(Nuc,N_tot)
        Tetra=np.append(Tetra,N_tetra)
    return Nuc,Tetra

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def fixfolder(folder):
    folder = folder.replace('\\', '\\\\') 
    return folder

Legend=[]
plt.figure(1)

folder = fixfolder( r'P:\18S FitFiles\18Swt_Regensburg_2016' )#folder with chromosome sequence files (note, do not put other files in this folder)
filenames = os.listdir(folder)
os.chdir( folder )
Wt_Reg_2016=count_nuc(folder)
plt.hist(Wt_Reg_2016[0], bins = 26, range = [0,25], alpha=0.5)
Legend.append('Wt_Reg_2016')

folder = fixfolder( r'P:\18S FitFiles\dUAF_Regensburg_2017') #folder with chromosome sequence files (note, do not put other files in this folder)
filenames = os.listdir(folder)
os.chdir( folder )
dUAF_nuc=count_nuc(folder)
plt.hist(dUAF_nuc[0],  bins = 26, range = [0,25], alpha=0.5 )
Legend.append('dUAF_nuc')

folder = fixfolder( r'P:\18S FitFiles\Leiden_wt') #folder with chromosome sequence files (note, do not put other files in this folder)
filenames = os.listdir(folder)
os.chdir( folder )
Wt_Lei_2016=count_nuc(folder)
plt.hist(Wt_Lei_2016[0],  bins = 26, range = [0,25], alpha=0.5 )
Legend.append('Wt_Lei_2016')

folder = fixfolder( r'P:\18S FitFiles\wt_DualLNA_2016') #folder with chromosome sequence files (note, do not put other files in this folder)
filenames = os.listdir(folder)
os.chdir( folder )
DualLNA_wt_nuc=count_nuc(folder)
plt.hist(DualLNA_wt_nuc[0],  bins = 26, range = [0,25], alpha=0.5 )
Legend.append('DualLNA_wt_nuc')

folder = fixfolder( r'P:\18S FitFiles\wt_Regensburg_2017') #folder with chromosome sequence files (note, do not put other files in this folder)
filenames = os.listdir(folder)
os.chdir( folder )
wt_Reg_2017=count_nuc(folder)
plt.hist(wt_Reg_2017[0],  bins = 26, range = [0,25], alpha=0.5 )
Legend.append('Wt_Reg_2017')

folder = fixfolder( r'P:\18S FitFiles\All_wt_CMD_LexA' )#folder with chromosome sequence files (note, do not put other files in this folder)
filenames = os.listdir(folder)
os.chdir( folder )
Wt_CMD=count_nuc(folder)
plt.hist(Wt_CMD[0], bins = 26, range = [0,25], alpha=0.5)
Legend.append('Wt_tot')

plt.xlabel('Nuc/Fiber')
plt.ylabel('Count')
plt.title("Number of Nucleosomes")
plt.legend(Legend)
plt.legend(loc='best')
plt.show()
plt.savefig('Hist_CMD.png')
