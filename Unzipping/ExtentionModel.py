# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 17:58:45 2017
@author: nhermans & jheinsman
Files needed:
.fit force extension of unzipping curve (corrected for offset + drift)
sequence of unzipped DNA
"""

#Imported libraries

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import Tools
import Functions as func

#Import Data
file_location="G:\\test\\"
file_name="FC2_pBlue_05ul_eh_good_data_016_39"
SequenceFile="G:\\klaas\\Unzipping\\18S_seq.txt"
file_extension=".fit"
FilePath=file_location+file_name+file_extension

Pars = Tools.default_pars()
Force, Z, Time, Extension_nm = Tools.read_data(FilePath)

Handles = Tools.Define_Handles(Select=True, Pull=True, DelBreaks=True, MinForce=2.5, MinZ=0, MedFilt=False)
Force, Extension_nm, Time = Tools.handle_data(Force, Z, Time, Extension_nm, Handles, Pars)

plt.scatter(Time, Extension_nm)
plt.xlabel('T (seconds)')
plt.ylabel('Extension [nm]')
plt.show()

#dG->NN calculator. Needs a sequence file, only the sequence in the direction of unzipping
f = open(SequenceFile, 'r')
sequence=f.read()
sequence=sequence.rstrip()
sequence=sequence.upper()
f.close()

GCcontent = func.GC_dG(sequence, window = 50) #Calls the function for calcultion of the GC content.

#split data in unzipping and annealing
Force_df = Force - np.roll(Force,1)
timeup = Time[Force_df >= 0]
timedown = Time[Force_df < 0]
extensionup = Extension_nm[Force_df >= 0]
extensiondown = Extension_nm[Force_df < 0]
forceup = Force[Force_df >= 0]
forcedown = Force[Force_df < 0]

#Fit ssDNA persistence length
Fit_Z=[]
Fit_F=[]
MaxForce=np.max(Force)
print(MaxForce)
if MaxForce < 25: MaxForce=25

for i in range(0,len(forcedown)):
     if forcedown[i] >= 20 and forcedown[i] < MaxForce :
            Fit_Z.append(extensiondown[i])
            Fit_F.append(forcedown[i])

popt = curve_fit(lambda f, p: func.fit_p(f,p, len(sequence)),Fit_F,Fit_Z,p0=0.6)

Fitted_Z=[]
for i in Fit_F:
    Fitted_Z.append(func.fit_p(i,popt[0]))

plt.scatter(Fit_Z, Fit_F)
plt.scatter(Fitted_Z,Fit_F)
plt.show()

print(popt[0])
PLss=popt

#Some reference Curves
WLC_2000 = []
WLC_2000_FJC_6000 = []
WLC_2000_FJC_4500 =[]
WLC_2000_FJC_2600 =[]

for i in Force:
    WLC_2000.append(func.wlc(i))
    WLC_2000_FJC_6000.append(func.wlc_fjc(i,len(sequence),Pars))

#FE and histogram graph generator
plt.clf() #Clear all graph plots
#Legend creator for FE graph
a  = plt.scatter(extensionup, forceup, color = 'blue', marker = 'o', s = 1, label = 'Pull')
b  = plt.scatter(extensiondown, forcedown, color = 'green', marker = 'o', s = 1, label = 'Relax')
c, = plt.plot(WLC_2000,Force, color = 'black', linewidth=1.0, label = "WLC ")
#d, = plt.plot(WLC_2000_FJC_2600, Force, color = 'yellow', linewidth=1.0, label = 'DWLC 1.2 kbp')
#e, = plt.plot(WLC_2000_FJC_4500, Force, color = 'orange', linewidth=1.0, label = 'DWLC 2.2 kbp')
f, = plt.plot(WLC_2000_FJC_6000, Force, color = 'red',linewidth=1.0, label = 'DWLC')

#Graph plot parameters for FE graph
plt.tick_params(direction = 'in', top = 'on', right = 'on')
plt.xlabel('Extension [nm]')
plt.ylabel('Force [pN]')
plt.axis([0, 3000, 0, 25])
plt.legend(handles=[a, b, c, f])
plt.savefig('170707_63_FE_DWLC.pdf') #save file name for FE graph
plt.show()

#Contour length histogram generation
basepairs = list(range(0, len(sequence)-2)) #for plotting only

  #down generation
CLss_down_array = list(range(0,len(extensiondown)))
pnull=len(sequence)
  
for i in CLss_down_array:
    CLss_down_array[i], cov = curve_fit(WLC_FJC, forcedown[i],extensiondown[i],p0=pnull)
    if cov[0] < 1: pnull=cov[0]
CLss_down_array = np.concatenate(CLss_down_array).ravel().tolist()

#Up generation  
CLss_up_array = list(range(0,len(extensionup)))

for i in CLss_up_array:
    CLss_up_array[i], cov = curve_fit(WLC_FJC, forceup[i],extensionup[i])
    if cov[0] < 1: pnull=cov[0]
CLss_up_array = np.concatenate(CLss_up_array).ravel().tolist()

CLss_up_bp = [x/par['DNAss_nm']/2 for x in CLss_up_array]
CLss_down_bp = [x/par['DNAss_nm']/2 for x in CLss_down_array]

#Contour length histogram + GC-content creator
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.hist(CLss_up_bp, bins = len(sequence)/20, color = 'blue', range = [0,len(sequence)] )
ax1.hist(CLss_down_bp, bins = len(sequence)/20, color = 'green', range = [0,len(sequence)])
ax2.plot(basepairs,GCcontent, 'r-', label = 'dG based on sequence', linewidth = 0.5)

#Graph plot parameters for histogram
ax1.tick_params(top = 'on', direction = 'in')
ax2.tick_params(direction = 'in')
ax1.set_xlabel('# of unzipped basepairs')
ax1.set_xlim((0,len(sequence)))
ax1.set_yscale('log')
ax1.set_ylim((0,10**4))
ax1.set_ylabel('Count', color='black')
ax2.set_ylabel('deltaG (kT)', color='black')
ax2.set_ylim(1,1.8)
plt.savefig('170707_63_GC_DWLC.pdf') #save file name for histogram + GC-content grapgh
plt.legend(loc=1)
plt.show()

FilePath=file_location+file_name+"_pull.dat"
file = open(FilePath, "w")

for i in range(0,len(timeup)):
    file.write("%s\t" %timeup[i])#,forceup[i],extensionup[i])
    file.write("%s\t" %forceup[i])
    file.write("%s\n" %extensionup[i])

file.close()

FilePath=file_location+file_name+"_release.dat"
file = open(FilePath, "w")

for i in range(0,len(timedown)):
    file.write("%s\t" %timedown[i])
    file.write("%s\t" %forcedown[i])
    file.write("%s\n" %extensiondown[i])

file.close()

FilePath=file_location+file_name+"_hist.dat"
file = open(FilePath, "w")

for i in range(0,len(CLss_up_bp)):
    a=0
    file.write("%s\t" % i)
    if CLss_up_bp[i]>0 and CLss_up_bp[i]<5000:
        file.write("%s\t" % CLss_up_bp[i])#,CLss_down_bp[i],GCcontent[i])
        a=1
    if i<len(CLss_down_bp) and CLss_down_bp[i]>0 and CLss_down_bp[i]<5000:
        if a==0: file.write("\t")
        file.write("%s\t" % CLss_down_bp[i])
        a=1
    if i<len(GCcontent):
        if a==0: file.write("\t \t")
        file.write("%s" % GCcontent[i])
        a=1
    if a==1:
        file.write("\n")
file.close()