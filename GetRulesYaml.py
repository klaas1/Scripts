#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 12:39:52 2018

@author: klaas
"""
###############################################################################
###########   How to use:
###########   1) Select the folder with the .yaml files
###########   2) Run the script
###############################################################################

import pandas as pd
import os 

folder =  r'/home/klaas/Documents/ReadYaml'

filenames = os.listdir(folder)
os.chdir(folder)
  
Filenames = []                                                                  #All .fit files in folder  
for filename in filenames:
    if filename[-5:] == '.yaml':
        Filenames.append(filename)

Keys = ['Cost','HP', 'Speed', 'Weapon','LocalOffset', 'Queue', 'TurnSpeed', 'Description']
Data=[]   
Placeholder = [0 for i in range(len(Keys)+1)]

#%%
###############################################################################
#############   Main script that runs thourgh all fitfiles in folder  #########
###############################################################################
for filename in Filenames:
    with open(filename,'r') as stream:
        data=[]
        i=-1
        namecheck=0
        for line in stream:
            line = line.replace('\t','  ')
            if line.startswith('    Description:'): 
                line = line.replace(':',';')
                line = line.replace('Description;','Description: ')
                line = line.replace('\\n','')
            if line.startswith(' ') == False and line.startswith('\n')==False:
                i=i+1
                data.append(Placeholder.copy())
            if line.startswith(	'  Tooltip:'): 
                namecheck=1
            if line.startswith(	'    Name:') and namecheck==1: 
                split_line = line.split(':')
                split_line[1].strip()
                data[i][0]=split_line[1]
                print(split_line[1])
                namecheck=0
            for key in Keys:
                if line.startswith('    '+key): 
                    split_line = line.split(':')
                    split_line[1].strip()
                    data[i][Keys.index(key)+1] = split_line[1]
                    print(split_line[1])#,  Data[i][Keys.index(key)+1])
    Data=Data+data          
Keys.insert(0,'Unit Name')
df = pd.DataFrame.from_records(Data, columns=Keys)
pd.DataFrame.to_csv(df, '_stats.csv')
