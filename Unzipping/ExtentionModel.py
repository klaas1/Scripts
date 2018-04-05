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

#Variables
#CLss_bp = 3000 #Contour lenght of single stranded DNA [basepairs]
CLds_bp = 700 #Contour length of double stranded DNA [basepairs]
L_ss_bp = 0.67 #Interbasepair distance for single stranded DNA [nm/bp]
L_ds_bp = 0.34 #interbasepair dinstance for double stranded DNa [nm/bp]
#CLss_nm = CLss_bp * L_ss_bp #Contour lenght of single stranded DNA [nm], used from sequence file
CLds_nm = CLds_bp * L_ds_bp #Contour length of double stranded DNA [nm]
#PLss = 0.69 #Persistence length of single stranded DNA [nm], fitted from release curve
PLds = 50 #Persistence length of double stranded DNA [nm]
SM = 1000 #Strechting modules [pN]
Kb = 1.38064852*10**-2 #Boltzman constant [(pN*nm)/K]
T = 294.15 #Temperature [K]

#Import Data
file_location="D:\\test\\"
file_name="FC2_pBlue_05ul_eh_good_data_016_39"
SequenceFile="D:\\klaas\\Unzipping\\18S_seq.txt"
file_extension=".fit"
FilePath=file_location+file_name+file_extension

f = open(FilePath, 'r')
headers_lines=f.readlines()[0] #headers
f.close()

f = open(FilePath, 'r')
data_lines=f.readlines()[1:] #data
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
    Extension.append(float(x.split()[headers.index('selected z (um)')]))

Force=np.array(Force)
Time=np.array(Time)
Extension=np.array(Extension)
Extension = Extension[np.isfinite(Extension)]
Force.resize(len(Extension))
Time.resize(len(Extension))
Extension_nm = [x * 1000 for x in Extension]

print(len(Extension),len(Force),len(Time))
#plt.scatter(Time, Extension)
#plt.scatter(Time, Force)
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
#nearest neighbor parameters, value: kcal/mol
NNparam =  {'AA': 1.0, 'TT': 1.0, 'AT': 0.88, 'TA': 0.58, 'CA': 1.45, 'TG': 1.45, 'GT': 1.44, 'AC': 1.44, 'CT': 1.28,
'AG': 1.28, 'GA': 1.30, 'TC': 1.30, 'CG': 2.17, 'GC': 2.24, 'GG': 1.84, 'CC': 1.84}
window = 50 #Specify the window to calculate the dG
basepairs = list(range(0, len(sequence)-2)) #for plotting only

def GC_dG(sequence, window):
    vals = []
    values = []
    for i in range(0, len(sequence)-2):
        s = sequence[i: i + 2] #dinucleotides
        dG = NNparam[s]
        vals.append(dG)
    for i in range(0,len(vals)): #lowpass filter
        values.append(np.average(vals[i:i+window]))
    return values

GCcontent = GC_dG(sequence, window) #Calls the function for calcultion of the GC content.

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
            extensionup.append(Extension_nm[i])
            forceup.append(Force[i])
    else:
            timedown.append(Time[i])
            extensiondown.append(Extension_nm[i])
            forcedown.append(Force[i])

#Fit ssDNA persistence length
Fit_Z=[]
Fit_F=[]
MaxForce=np.max(Force)
print(MaxForce)
#MaxForce=30
for i in range(0,len(forcedown)):
     if forcedown[i] >= 20 and forcedown[i] < MaxForce :
            Fit_Z.append(extensiondown[i])
            Fit_F.append(forcedown[i])

def Fit_Pss(f,p): #WLC extensible + WLC
    return CLds_nm*(1-0.5*np.sqrt(Kb*T/(f*PLds))+f/SM) + len(sequence)*2*L_ss_bp*(1-0.5*np.sqrt(Kb*T/(f*p)))

popt = curve_fit(lambda f, p: Fit_Pss(f,p),Fit_F,Fit_Z,p0=0.6)

Fitted_Z=[]
for i in Fit_F:
    Fitted_Z.append(Fit_Pss(i,popt[0]))

plt.scatter(Fit_Z, Fit_F)
plt.scatter(Fitted_Z,Fit_F)
plt.show()

print(popt)
PLss=popt[0]

#functions
def WLC_FJC(f,CLss_nm): #WLC extensible + WLC
    return (CLds_nm*(1-0.5*np.sqrt(Kb*T/(f*PLds))+f/SM))+ (CLss_nm*(1-0.5*np.sqrt(Kb*T/(f*PLss))))

def WLC(f):
    return CLds_nm*(1-0.5*np.sqrt(Kb*T/(f*PLds))+f/SM)

#Some reference Curves
WLC_2000 = []
WLC_2000_FJC_6000 = []
WLC_2000_FJC_4500 =[]
WLC_2000_FJC_2600 =[]

for i in range(0,len(Force)):
    WLC_2000.append(WLC(Force[i]))
    WLC_2000_FJC_6000.append(WLC_FJC(Force[i],2*len(sequence)*L_ss_bp))

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

CLss_up_bp = [x/L_ss_bp/2 for x in CLss_up_array]
CLss_down_bp = [x/L_ss_bp/2 for x in CLss_down_array]

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