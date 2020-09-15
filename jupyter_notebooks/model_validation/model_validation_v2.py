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
import shutil

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
while(i < numBoot): #Set up for 100 successful runs
    print(i)
    #Delete old input file if one exists
    if os.path.exists("input.csv"): os.remove('input.csv')
    boot = resample(data, replace = True, n_samples = numSamples)
    xBoot, yBoot, zBoot = zip(*boot)
    #Write coordinates to a file
    np.savetxt("input.csv", np.column_stack((np.array(xBoot, dtype=float), np.array(yBoot, dtype=float), np.array(zBoot, dtype=float))), delimiter=",", fmt='%s')
    #Create 2D projections 
    os.system('python Project2D.py')
    #curve fit 
    cmd = 'python curve_fit.py 2 ' + pop
    ret = os.system(cmd)
    if ret == 0:
        i = i + 1
    else:
        print("Curve fit optimal parameters not found or outlier")
        continue

#Plot params - no outliers
r2,pi2,ph2,rse2,pise2,phse2,r3,pi3,ph3,rse3,pise3,phse3 = getParams("params.csv")
y = list(range(1,numBoot+1))
plt.style.use('dark_background')

#Remove old output file if it exists
#TODO: Go into results file and remove pop folder 
if os.path.exists(pop) and os.path.isdir(pop):
    shutil.rmtree(pop)

#Make output file to store images
os.mkdir(pop)
os.chdir(pop)
os.mkdir('sampling distributions')
os.mkdir('confidence intervals')
os.chdir('..')

#plots

plt.scatter(r2, y, c='b',s=1); plt.title('Radius c1c2'); plt.xlim(2, 8); plt.savefig(pop+"/sampling distributions/Radius c1c2"); plt.close()
plt.scatter(rse2, y, c='g',s=1); plt.title('Radius standard error c1c2'); plt.savefig(pop+"/sampling distributions/Radius standard error c1c2"); plt.close()
plt.scatter(r3, y, c='b',s=1); plt.title('Radius c1c3'); plt.xlim(2, 8); plt.savefig(pop+"/sampling distributions/Radius c1c3"); plt.close()
plt.scatter(rse3, y, c='g',s=1); plt.title('Radius standard error c1c3'); plt.savefig(pop+"/sampling distributions/Radius standard error c1c3"); plt.close()

plt.scatter(pi2, y, c='b',s=1); plt.title('Pitch c1c2'); plt.xlim(11, 17); plt.savefig(pop+"/sampling distributions/Pitch c1c2"); plt.close()
plt.scatter(pise2, y, c='g',s=1); plt.title('Pitch standard error c1c2'); plt.savefig(pop+"/sampling distributions/Pitch standard error c1c2"); plt.close()
plt.scatter(pi3, y, c='b',s=1); plt.title('Pitch c1c3'); plt.xlim(11, 17); plt.savefig(pop+"/sampling distributions/Pitch c1c3"); plt.close()
plt.scatter(pise3, y, c='g',s=1); plt.title('Pitch standard error c1c3'); plt.savefig(pop+"/sampling distributions/Pitch standard error c1c3"); plt.close()

plt.scatter(ph2, y, c='b',s=1); plt.title('Phase c1c2'); plt.savefig(pop+"/sampling distributions/Phase c1c2"); plt.close()
plt.scatter(phse2, y, c='g',s=1); plt.title('Phase standard error c1c2'); plt.savefig(pop+"/sampling distributions/Phase standard error c1c2");  plt.close()
plt.scatter(ph3, y, c='b',s=1); plt.title('Phase c1c3'); plt.savefig(pop+"/sampling distributions/Phase c1c3"); plt.close()
plt.scatter(phse3, y, c='g',s=1); plt.title('Phase standard error c1c3'); plt.savefig(pop+"/sampling distributions/Phase standard error c1c3");  plt.close()

#Estimating confidence intervals 
mean_r2 = statistics.mean(r2); sd_r2 = statistics.stdev(r2)
upper_boundary_r2 = mean_r2 + (1.96*sd_r2)
_=plt.hist(r2, bins = 10)
_=plt.xlabel("Radius c1c2")
_=plt.ylabel("Number of samples")
print("Radius c1c2 ci: " + str(upper_boundary_r2))
x_upper = [upper_boundary_r2]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Radius c1c2")
plt.close()

mean_rse2 = statistics.mean(rse2); sd_rse2 = statistics.stdev(rse2)
upper_boundary_rse2 = mean_rse2 + (1.96*sd_rse2)
_=plt.hist(rse2, bins = 10)
_=plt.xlabel("Radius se c1c2")
_=plt.ylabel("Number of samples")
print("Radius se c1c2 ci: " + str(upper_boundary_rse2))
x_upper = [upper_boundary_rse2]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Radius se c1c2")
plt.close()

mean_r3 = statistics.mean(r3); sd_r3 = statistics.stdev(r3)
upper_boundary_r3 = mean_r3 + (1.96*sd_r3)
_=plt.hist(r3, bins = 10)
_=plt.xlabel("Radius c1c3")
_=plt.ylabel("Number of samples")
print("Radius c1c3 ci: " + str(upper_boundary_r3))
x_upper = [upper_boundary_r3]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Radius c1c3")
plt.close()

mean_rse3 = statistics.mean(rse3); sd_rse3 = statistics.stdev(rse3)
upper_boundary_rse3 = mean_rse3 + (1.96*sd_rse3)
_=plt.hist(rse3, bins = 10)
_=plt.xlabel("Radius se c1c3")
_=plt.ylabel("Number of samples")
print("Radius se c1c3 ci: " + str(upper_boundary_rse3))
x_upper = [upper_boundary_rse3]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Radius se c1c3")
plt.close()

mean_pi2 = statistics.mean(pi2); sd_pi2 = statistics.stdev(pi2)
upper_boundary_pi2 = mean_pi2 + (1.96*sd_pi2)
_=plt.hist(pi2, bins = 10)
_=plt.xlabel("Pitch c1c2")
_=plt.ylabel("Number of samples")
print("Pitch c1c2 ci: " + str(upper_boundary_pi2))
x_upper = [upper_boundary_pi2]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Pitch c1c2")
plt.close()

mean_pise2 = statistics.mean(pise2); sd_pise2 = statistics.stdev(pise2)
upper_boundary_pise2 = mean_pise2 + (1.96*sd_pise2)
_=plt.hist(pise2, bins = 10)
_=plt.xlabel("Pitch se c1c2")
_=plt.ylabel("Number of samples")
print("Pitch se c1c2 ci: " + str(upper_boundary_pise2))
x_upper = [upper_boundary_pise2]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Pitch se c1c2")
plt.close()

mean_pi3 = statistics.mean(pi3); sd_pi3 = statistics.stdev(pi3)
upper_boundary_pi3 = mean_pi3 + (1.96*sd_pi3)
_=plt.hist(pi3, bins = 10)
_=plt.xlabel("Pitch c1c3")
_=plt.ylabel("Number of samples")
print("Pitch c1c3 ci: " + str(upper_boundary_pi3))
x_upper = [upper_boundary_pi3]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Pitch c1c3")
plt.close()

mean_pise3 = statistics.mean(pise3); sd_pise3 = statistics.stdev(pise3)
upper_boundary_pise3 = mean_pise3 + (1.96*sd_pise3)
_=plt.hist(pise3, bins = 10)
_=plt.xlabel("Pitch se c1c3")
_=plt.ylabel("Number of samples")
print("Pitch se c1c3 ci: " + str(upper_boundary_pise3))
x_upper = [upper_boundary_pise3]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Pitch se c1c3")
plt.close()

mean_ph2 = statistics.mean(ph2); sd_ph2 = statistics.stdev(ph2)
upper_boundary_ph2 = mean_ph2 + (1.96*sd_ph2)
_=plt.hist(ph2, bins = 10)
_=plt.xlabel("Phase c1c2")
_=plt.ylabel("Number of samples")
print("Phase c1c2 ci: " + str(upper_boundary_ph2))
x_upper = [upper_boundary_ph2]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Phase c1c2")
plt.close()

mean_phse2 = statistics.mean(phse2); sd_phse2 = statistics.stdev(phse2)
upper_boundary_phse2 = mean_phse2 + (1.96*sd_phse2)
_=plt.hist(phse2, bins = 10)
_=plt.xlabel("Phase se c1c2")
_=plt.ylabel("Number of samples")
print("Phase se c1c2 ci: " + str(upper_boundary_phse2))
x_upper = [upper_boundary_phse2]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Phase se c1c2")
plt.close()

mean_ph3 = statistics.mean(ph3); sd_ph3 = statistics.stdev(ph3)
upper_boundary_ph3 = mean_ph3 + (1.96*sd_ph3)
_=plt.hist(ph3, bins = 10)
_=plt.xlabel("Phase c1c3")
_=plt.ylabel("Number of samples")
print("Phase c1c3 ci: " + str(upper_boundary_ph3))
x_upper = [upper_boundary_ph3]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Phase c1c3")
plt.close()

mean_phse3 = statistics.mean(phse3); sd_phse3 = statistics.stdev(phse3)
upper_boundary_phse3 = mean_phse3 + (1.96*sd_phse3)
_=plt.hist(phse3, bins = 10)
_=plt.xlabel("Phase se c1c3")
_=plt.ylabel("Number of samples")
print("Phase se c1c3 ci: " + str(upper_boundary_phse3))
x_upper = [upper_boundary_phse3]*1000; y = list(range(0, 1000))
plt.plot(x_upper,y, '-g')
plt.savefig(pop+"/confidence intervals/Phase se c1c3")
plt.close()

