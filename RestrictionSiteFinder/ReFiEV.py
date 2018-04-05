# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:47:17 2015
@author: nhermans
"""

#finds specefic (restriction) sequence in Genome, outputs n basepairs sequence 
#around the restriction site. Note, 5' and 3' overhangs need to be defined by 
#the user. For now, only palindromic sites can be used.

restrict = 'AAGCTT' #TATAGGGAATATT define restriction site (palindrome, if not palindrome, do both sequences independently).
filename = 'K12.txt' #sequence file
probe = 'TATAGGGAATATT'
#Depending on 5' or 3' overhang, one of the output sequences needs to be converted to the complementary strand  
import re #regular expressions lib
import time # just a timer
start = time.time()

#Import genome as a single string
sequencelines = [line.strip() for line in open(filename)]
for line in sequencelines[:]:
    if line.startswith(">"):  
        sequencelines.remove(line) #remove first line
    else:
        sequence = ''.join(sequencelines) #converts to a single string
sequence = re.sub(r'\d+|\W+', '', sequence) #removes numbers etc.
sequence = sequence.upper()      #changes everything to upper case 
restrict = restrict.upper() 
probe = probe.upper()
length = len(probe) #lenght of the probe    
count=0
seqlist = re.finditer(restrict, sequence)
threeprime = []
fiveprime = []
for m in seqlist:
        count = count+1
        #print restrict,' @ ', m.start() 
        threeprime.append(sequence[(m.start()):(m.start()+length+6)]) #outputs all 5' and 3' sequences adiecent to restriction site
        fiveprime.append(sequence[(m.start()-length):m.start()+6]) #empty sequences are near the ends of the DNA
print('# restriction site',restrict,' =', count)
    
glue = '-'  #make single string with all the sequences
fiveprime = glue.join(fiveprime) #idem
eborp=probe[::-1]
subprobe=''
for x in eborp:
    subprobe = x+subprobe    
    findthis = subprobe+restrict    
    count=0    
    count = fiveprime.count(findthis)
    print('# sequence compatible with',findthis,'=', count)
    if count == 0:
        break 

qrode = "" #find 3'->5' sequences
for i in probe:  
    if(i == "T"):
        qrode = "A" + qrode
    if(i == "A"):
        qrode = "T" + qrode
    if(i == "G"):
        qrode = "C" + qrode
    if(i == "C"):
        qrode = "G" + qrode 

subprobe=''
threeprime = glue.join(threeprime)
for x in qrode:
    subprobe = x+subprobe    
    findthis = restrict + subprobe    
    count=0    
    count = threeprime.count(findthis)
    print('# (3\'->5\' lookup) sequence compatible with',findthis,'=', count)
    if count == 0:
        break 

end = time.time()

print ('sequence length =', len(sequence),'bp')
print ('# restriction sites =', count)
print ('time =', end - start)