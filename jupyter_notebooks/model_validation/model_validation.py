'''
This script takes in arguments in the following order: 
numPoints, radius, pitch, percentError, numBoot, numSamples
'''

import sys, os, csv, random
import numpy as np
from sklearn.utils import resample

#Helper functions
'''
Usage: To generate a helix consisting of numPoints, with a given radius, pitch 
       and percent spatial error. 
returns: 3 arrays with x,y,z coordinates of points along the helix 
'''
def generatePopulation(numPoints, radius, pitch, p_error):
    #Generating spatial error
    posErrorx = np.random.normal(0, (p_error/100)*radius, numPoints)
    posErrory = np.random.normal(0, (p_error/100)*radius, numPoints)
    posErrorz = np.random.normal(0, (p_error/100)*pitch, numPoints)

    #Generate a helix with the z axis as the long axis.
    t = np.linspace(0, 8*np.pi, numPoints) #controls number of helical turns 
    x = radius*np.cos(t) + posErrorx
    y = radius*np.sin(t) + posErrory
    z = (pitch/(2*np.pi))*t + posErrorz
    return (x,y,z)

#Set model params
numPoints = int(sys.argv[1]) #population size
radius = int(sys.argv[2])
pitch = int(sys.argv[3])
p_error = int(sys.argv[4]) 
numBoot = int(sys.argv[5]) #number of bootstraps to perform 
numSamples = int(sys.argv[6]) #number of samples to pick for each run of curve fitting 

#Generate a perfect helix with the z axis as the long axis.
x,y,z = generatePopulation(numPoints, radius, pitch, p_error)

#Bootstrapping
data = list(zip(x, y, z))
#Delete params output file before next run
if os.path.exists("params.csv"): os.remove('params.csv')
i = 0
while(i < numBoot):
    boot = resample(data, replace = True, n_samples = numSamples)
    xBoot, yBoot, zBoot = zip(*boot)
    #Write coordinates to a file
    #Delete old input file if one exists
    if os.path.exists("input.csv"): os.remove('input.csv')
    np.savetxt("input.csv", np.column_stack((np.array(xBoot, dtype=float), np.array(yBoot, dtype=float), np.array(zBoot, dtype=float))), delimiter=",", fmt='%s')
    #Create 2D projections 
    os.system('python Project2D.py')
    #curve fit 
    ret = os.system('python CurveFit.py')
    if ret == 0:
        i = i + 1
    else:
        print("Curve fit optimal parameters not found")
        continue
           