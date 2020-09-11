'''
This version of model validation is used to estimate the 95% confidence interval. 
This script takes in arguments in the following order: 
numPoints, radius, pitch, percentError, numBoot, numSamples, pop
'''

import sys, os, csv, random
import numpy as np
from sklearn.utils import resample
import statistics
import matplotlib.pyplot as plt

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

'''
Usage: To read the file with helix parameters 
returns: each helix parameter in a separate array 
'''
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

#Set model params
numPoints = int(sys.argv[1]) #population size
radius = int(sys.argv[2])
pitch = int(sys.argv[3])
p_error = int(sys.argv[4]) 
numBoot = int(sys.argv[5]) #number of bootstraps to perform 
numSamples = int(sys.argv[6]) #number of samples to pick for each run of curve fitting 
pop = sys.argv[7]

#Generate a perfect helix with the z axis as the long axis.
x,y,z = generatePopulation(numPoints, radius, pitch, p_error)

#Delete outliers.csv before the next run
if os.path.exists("outliers.csv"): os.remove('outliers.csv')
#Bootstrapping
data = list(zip(x, y, z))
#Delete params output file before next run
if os.path.exists("params.csv"): os.remove('params.csv')
i = 0
while(i < numBoot):
    print(i)
    boot = resample(data, replace = True, n_samples = numSamples)
    xBoot, yBoot, zBoot = zip(*boot)
    #Write coordinates to a file
    #Delete old input file if one exists
    if os.path.exists("input.csv"): os.remove('input.csv')
    np.savetxt("input.csv", np.column_stack((np.array(xBoot, dtype=float), np.array(yBoot, dtype=float), np.array(zBoot, dtype=float))), delimiter=",", fmt='%s')
    #Create 2D projections 
    os.system('python Project2D.py')
    #curve fit 
    cmd = 'python CurveFit_v2.py ' + pop
    ret = os.system(cmd)
    if ret == 0:
        i = i + 1
    else:
        print("Curve fit optimal parameters not found")
        continue

#Plot params - no outliers
r2,pi2,ph2,rse2,pise2,phse2,r3,pi3,ph3,rse3,pise3,phse3 = getParams("params.csv")
y = list(range(1,numBoot+1))
plt.style.use('dark_background')

#plots

plt.scatter(r2, y, c='b',s=1); plt.title('Radius c1c2'); plt.xlim(2, 8); plt.savefig("Radius c1c2"); plt.close()
plt.scatter(rse2, y, c='g',s=1); plt.title('Radius standard error c1c2'); plt.savefig("Radius standard error c1c2"); plt.close()
plt.scatter(r3, y, c='b',s=1); plt.title('Radius c1c3'); plt.xlim(2, 8); plt.savefig("Radius c1c3"); plt.close()
plt.scatter(rse3, y, c='g',s=1); plt.title('Radius standard error c1c3'); plt.savefig("Radius standard error c1c3"); plt.close()

plt.scatter(pi2, y, c='b',s=1); plt.title('Pitch c1c2'); plt.xlim(11, 17); plt.savefig("Pitch c1c2"); plt.close()
plt.scatter(pise2, y, c='g',s=1); plt.title('Pitch standard error c1c2'); plt.savefig("Pitch standard error c1c2"); plt.close()
plt.scatter(pi3, y, c='b',s=1); plt.title('Pitch c1c3'); plt.xlim(11, 17); plt.savefig("Pitch c1c3"); plt.close()
plt.scatter(pise3, y, c='g',s=1); plt.title('Pitch standard error c1c3'); plt.savefig("Pitch standard error c1c3"); plt.close()

plt.scatter(ph2, y, c='b',s=1); plt.title('Phase c1c2'); plt.savefig("Phase c1c2"); plt.close()
plt.scatter(phse2, y, c='g',s=1); plt.title('Phase standard error c1c2'); plt.savefig("Phase standard error c1c2");  plt.close()
plt.scatter(ph3, y, c='b',s=1); plt.title('Phase c1c3'); plt.savefig("Phase c1c3"); plt.close()
plt.scatter(phse3, y, c='g',s=1); plt.title('Phase standard error c1c3'); plt.savefig("Phase standard error c1c3");  plt.close()
