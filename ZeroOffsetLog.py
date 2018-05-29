# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 11:19:59 2018

@author: nhermans
"""

import os #filenames

def change_file(Filename, Change_String):
    NewFile = Filename + '.tmp'
    n_f = open(NewFile, 'w')
    f = open(Filename, 'r')
    lines=f.readlines()
    for x in lines:
        P = x.split(' = ')
        if P[0] == Change_String:
            print(P[1])
            x = Change_String + '= 0 \n' 
        n_f.write(x)
    f.close()
    n_f.close()
    os.rename(Filename,Filename + '.old')
    os.rename(NewFile,Filename)
    os.remove(Filename + '.old')
    
folder = r'P:\18S FitFiles\wt_Regensburg_2017' #folder with chromosome sequence files (note, do not put other files in this folder)
filenames = os.listdir(folder)
os.chdir( folder )
for myfile in filenames:
    if myfile[-4:] != '.log' :
            continue
    change_file(myfile, 'z_offset (nm)')
    change_file(myfile, 'Drift (nm/s)')
