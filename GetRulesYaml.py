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

Keys = ['  Cost','  HP', '  Speed','  Weapon','Inherits@1','  LocalOffset', '  Queue', '  TurnSpeed', '  Description'] #add/edit keys according to yaml
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
            line = line.replace('\t','  ') #Removes tabs, sometimes space and tabs are used inconsistently
            if line.startswith('    Description:'): 
                line = line.replace(':',';')
                line = line.replace('Description;','Description:')
                line = line.replace('\\n','')
            if line.startswith(' ') == False and line.startswith('\n')==False: #counts blocks
                i=i+1
                data.append(Placeholder.copy())
            if line.startswith(	'  Tooltip:'): #only gathers units with tooltip (aka buildable)
                namecheck=1
            if line.startswith(	'    Name:') and namecheck==1: 
                split_line = line.split(':')[1].replace(' ','')
                data[i][0]=split_line #gets name and puts it in the first collumn. Note: some sprites do not have a name, and give empty rows
                print(split_line)
                namecheck=0
            for key in Keys:   #gatgers info from keys, can be anything just add more keys
                if line.startswith('  '+key): 
                    split_line = line.split(':')[1:]
                    split_line = (''.join(split_line)).strip()
                    if data[i][Keys.index(key)+1]==0:
                        data[i][Keys.index(key)+1] = split_line
                    else: data[i][Keys.index(key)+1] = str(data[i][Keys.index(key)+1])+', '+str(split_line)
                    print(split_line)#,  Data[i][Keys.index(key)+1])
    Data=Data+data          #Saves all data in master list
Keys.insert(0,'Unit Name')  #Fixes the collumn names
df = pd.DataFrame.from_records(Data, columns=Keys)   #saves a dataframe
pd.DataFrame.to_csv(df, '_stats.csv',  sep="\t")
