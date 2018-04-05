# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:25:48 2015

@author: jhuisman
"""
import numpy as np
import os
from os import path
import shutil

files = [f for f in os.listdir("./input/") if path.isfile(f)]
for f in files:
    if f.endswith(".dat"):
        print(f)
        data = np.genfromtxt(f,dtype=None,delimiter="\t")
        shutil.copy2(f,"./output/"+f)
        shutil.copy2(f[:-4]+".log","./output/"+f[:-4]+".log")
        
        for i in np.arange(2,5):
                temp = np.copy(data)
                if(("bead"+str(i)+" z (um)") in temp[0]):             
                    temp[0] = np.array([s.replace("1","5") for s in temp[0]])#Replace any already existing bead1 with bead5                        
                    temp[0] = np.array([s.replace(str(i),"1") for s in temp[0]])# Replace beadi with bead1            
                    shutil.copy2(f[:-4]+".log","./output/"+f[:-4]+"_"+str(i)+".log")#Copy log file
                    np.savetxt("./output/"+f[:-4]+"_"+str(i)+".dat", temp,fmt="%s",delimiter="\t")#Save edited file      