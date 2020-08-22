#!/usr/bin/python
import os
import csv
import random
import numpy as np

#Set model constants
numPoints = 100000 #population size
radius = 5
pitch = 14
percentError = 15 #of radius 
numBoot = 10000 #number of bootstraps to perform 
numSamples = 200 #number of samples to pick for each run of curve fitting 

#SYNTHETIC MODEL
#Generate a perfect helix with the z axis as the long axis.
#Read this for math background: (http://mathworld.wolfram.com/Helix.html)
t = np.linspace(0, 8*np.pi, numPoints) #controls number of helical turns 
x = radius*np.cos(t)
y = radius*np.sin(t)
z = (pitch/(2*np.pi))*t

#Sampling points randomly from a normal distribution centered at 0.
mean = 0; stdDev = (percentError/100)*radius
#np.random.seed(20)
posError = np.random.normal(mean, stdDev, numPoints)

#Adding random positional error to the 10000 points on the helix.
xWithErr = x + posError
yWithErr = y + posError
zWithErr = z + posError

#BOOTSTRAPPING
#Read this article for background: https://machinelearningmastery.com/a-gentle-introduction-to-the-bootstrap-method/
from sklearn.utils import resample
data = list(zip(xWithErr, yWithErr, zWithErr))
#Delete params output file before next run
if os.path.exists("params.csv"): os.remove('params.csv')
for i in range(0,numBoot): #Number of times you want to bootstrap CHANGE: to 1000 times, has been set to 1 for testing
    boot = resample(data, replace = True, n_samples = numSamples)
    #Split chosen coordinates into separate lists for curve fitting/viz
    xBoot, yBoot, zBoot = zip(*boot)
    #Write coordinates to a file
    np.savetxt("input.csv", np.column_stack((np.array(xBoot, dtype=float), np.array(yBoot, dtype=float), np.array(zBoot, dtype=float))), delimiter=",", fmt='%s')
    #Create 2D projections 
    os.system('python Project2D.py')
    #curve fit 
    os.system('python CurveFit.py')
