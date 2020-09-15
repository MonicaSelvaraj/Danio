'''
This script estimates the outlier removal threshold for the specified population.

args: 1 - numPoints, 2 - radius, 3 - pitch, 4 - percentError, 5 - numBoot, 6 - numSamples, 7 - pop
'''

import sys, os, csv
import numpy as np
import statistics
import common_funcs

#Clear threshold list
thresh = list()

#Run model validation 10 times, store mean of threshold
for i in range(0,10):
    os.system('python model_validation_v1.py ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4] + ' ' + sys.argv[5] + ' ' + sys.argv[6])

    #Get params for the current model validation run
    r2,pi2,ph2,rse2,pise2,phse2,r3,pi3,ph3,rse3,pise3,phse3 = common_funcs.getParams("params.csv")
    
    #Estimate outlier threshold for the current run
    rse = (rse2 + rse3)/2
    rse_mean = statistics.mean(rse)
    rse_sd = statistics.stdev(rse)
    outlier_thresh = rse_mean + 2*(rse_sd)
    thresh.append(outlier_thresh)
    
#Calculate the mean threshold of 10 runs
mean_thresh = statistics.mean(thresh)

#Write to file
with open("threshold.txt", "a") as text_file:
    text_file.write( str(mean_thresh) + "\n")
with open("population.txt", "a") as text_file:
    text_file.write( sys.argv[7] + "\n")