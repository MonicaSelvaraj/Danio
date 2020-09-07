'''
This script takes in arguments in the following order: 
numPoints, radius, pitch, percentError, numBoot, numSamples, pop
'''

import sys, os, csv
import numpy as np
import statistics

#Helper functions
def getParams(filename):
    r2 = list(); pi2 = list(); ph2 = list(); rse2 = list(); pise2 = list(); phse2 = list()
    r3 = list(); pi3 = list(); ph3 = list(); rse3 = list(); pise3 = list(); phse3 = list()
    with open (filename, 'r') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
            r2.append(line[0]); pi2.append(line[1]); ph2.append(line[2])
            rse2.append(line[3]); pise2.append(line[4]); phse2.append(line[5])
            r3.append(line[6]); pi3.append(line[7]); ph3.append(line[8])
            rse3.append(line[9]); pise3.append(line[10]); phse3.append(line[11])
    r2 = np.array(r2, dtype = float); pi2 = np.array(pi2, dtype = float); ph2 = np.array(ph2, dtype = float)
    rse2 = np.array(rse2, dtype = float); pise2 = np.array(pise2, dtype = float); phse2 = np.array(phse2, dtype = float)
    r3 = np.array(r3, dtype = float); pi3 = np.array(pi3, dtype = float); ph3 = np.array(ph3, dtype = float)
    rse3 = np.array(rse3, dtype = float); pise3 = np.array(pise3, dtype = float); phse3 = np.array(phse3, dtype = float)
    return (r2, pi2, ph2, rse2, pise2, phse2, r3, pi3, ph3, rse3, pise3, phse3)

#Clear threshold list
thresh = list()

#Run model validation 10 times, store mean of threshold
for i in range(0,10):
    os.system('python model_validation.py ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4] + ' ' + sys.argv[5] + ' ' + sys.argv[6])

    #After one run of model_validation, you have a params file to work with 
    r2,pi2,ph2,rse2,pise2,phse2,r3,pi3,ph3,rse3,pise3,phse3 = getParams("params.csv")
    
    #Estimate outlier threshold for this run
    rse = (rse2 + rse3)/2
    rse_mean = statistics.mean(rse)
    rse_sd = statistics.stdev(rse)
    outlier_thresh = rse_mean + 2*(rse_sd)
    thresh.append(outlier_thresh)
mean_thresh = statistics.mean(thresh)

with open("threshold.txt", "a") as text_file:
    text_file.write( str(mean_thresh) + "\n")
with open("population.txt", "a") as text_file:
    text_file.write( sys.argv[7] + "\n")



    

