'''
Usage: Fit curves in 2D first
Combining the 2D fits to get a 3D fit
pop is passed in as an argument to the script 
'''

#!/usr/bin/python
import csv, sys, math
import numpy as np
from csv import writer
from scipy.optimize import curve_fit

'''
Usage: To read a file with x,y,z coordinates, and store the data for each dimension in a separate array.
params: filename - File with x,y,z cooridnates
returns: 3 arrays with x's, y's and z's
'''
def getPoints(filename):
    x = list(); y = list(); z = list()
    with open (filename, 'r') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
            x.append(line[0]); y.append(line[1]); z.append(line[2])
    x = np.array(x, dtype = float)
    y = np.array(y, dtype = float)
    z = np.array(z, dtype = float)
    return (x, y, z)    
    
    
def appendToCsv(filename, line):
    # Open file in append mode
    with open(filename, 'a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(line)
        
'''
Usage: To create dictionary with population names as keys and 
outlier removal thresholds as values.
'''
def outlierThresholdsDict():
    keys = list(); values = list()
    a = open('population.txt','r')
    for line in a:
        keys.append(line.strip())
    b = open('threshold.txt', 'r')
    for line in b:
        values.append(line.strip())
    return dict(zip(keys, values))

'''
Defining input functions to scipy.optimize.curvefit
'''
def helixFitCos(pc1, r, pitch, phase):
    return r*np.cos(pc1*((2*np.pi)/pitch) + phase)
def helixFitSin(pc1, r, pitch, phase):
    return r*np.sin(pc1*((2*np.pi)/pitch) + phase)
'''
Given x, predict the best y 
'''
def fitFunction(x, y, function):
    try:
        popt, pcov = curve_fit(function, x, y, bounds=(0, [30, 30, 2*math.pi]))
    except RuntimeError:
        sys.exit(1)
    else:
        radius = popt[0]; pitch = popt[1]; phase = popt[2]
        StandardErr = np.sqrt(np.diag(pcov))
        return(radius, pitch, phase, StandardErr[0], StandardErr[1], StandardErr[2])
'''
Comparing sin and cos fits
'''
def BestFit(x,y):
        CosFit = fitFunction(x, y, helixFitCos)
        SinFit = fitFunction(x, y, helixFitSin)
        StdErrSumCos = CosFit[3] + CosFit[4] + CosFit[5]
        StdErrSumSin = SinFit[3] + SinFit[4] + SinFit[5]
        if(StdErrSumCos < StdErrSumSin):
                yOpt = [helixFitCos(c1, CosFit[0], CosFit[1], CosFit[2]) for c1 in x]
                return (CosFit[0],CosFit[1],CosFit[2],CosFit[3],CosFit[4],CosFit[5],yOpt)
        else:
                yOpt = [helixFitSin(c1, SinFit[0], SinFit[1], SinFit[2]) for c1 in x]
                return (SinFit[0],SinFit[1],SinFit[2],SinFit[3],SinFit[4],SinFit[5],yOpt)

#Get input     
c1,c2,c3 = getPoints("projections.csv")
c1 = np.array(c1, dtype = float); c2 = np.array(c2, dtype = float); c3 = np.array(c3, dtype = float)

#Fit
r2,pi2,ph2,rse2,pise2,phse2,fitc2 = BestFit(c1, c2) # Predicts C2 given C1
r3,pi3,ph3,rse3,pise3,phse3,fitc3 = BestFit(c1, c3)  # Predicts C3 given C1
fitParams = [r2,pi2,ph2,rse2,pise2,phse2,r3,pi3,ph3,rse3,pise3,phse3]

#Write fit coordinates to file
np.savetxt("fit.csv", np.column_stack((c1, np.array(fitc2, dtype=float), np.array(fitc3, dtype=float))), delimiter=",", fmt='%s')

#Store params after checking that it's not an outlier 
#Remove outliers from params
#Getting pop name to get outlier removal threshold from dict 
pop = sys.argv[1] 
out_thresh_dict = outlierThresholdsDict()
print(out_thresh_dict)
threshold = out_thresh_dict[pop]
print(threshold)

rse = (rse2 + rse3)/2
if(rse <= threshold)
    appendToCsv("params.csv", fitParams)
else
    #Write outlier coordinates to outliers.csv
    np.savetxt("outliers.csv", np.column_stack((c1, c2, c3)), delimiter=",", fmt='%s', mode = 'a')

sys.exit(0)