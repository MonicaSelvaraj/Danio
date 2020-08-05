'''
Fitting curves in 2D to each channel separately
Combining the 2D fits to get a 3D fit
Plots of 2D and 3D fits
'''

#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.axes import Axes
import scipy.stats
import statistics
import numpy 
import csv
import math
from matplotlib import style
from scipy.spatial import distance
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit

f_read = open("FileNames.txt", "r")
last_line = f_read.readlines()[-1]
last_line = last_line[:-1] #Ignoring newline character
f_read.close()

plt.style.use('dark_background')

print("Curve Fitting")

#2D curve fitting 
#Original data 
C1r = list(); C2r = list(); C3r = list()#C1 - red
C1g = list(); C2g = list(); C3g = list()#C2 - green

#Reading in the data 
with open ('CleanedComponentsC1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    for line in csv_reader:
            C1r.append(line[0])
            C2r.append(line[1])
            C3r.append(line[2])
            
with open ('CleanedComponentsC2.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    for line in csv_reader:
            C1g.append(line[0])
            C2g.append(line[1])
            C3g.append(line[2])
       
C1r = numpy.array(C1r, dtype = float); C2r = numpy.array(C2r, dtype = float); C3r = numpy.array(C3r, dtype = float)
C1g = numpy.array(C1g, dtype = float); C2g = numpy.array(C2g, dtype = float); C3g = numpy.array(C3g, dtype = float)

#This is to input to scipy.optimize.curvefit
def helixFitCos(pc1, r, pitch, phase):
    return r*numpy.cos(pc1*((2*numpy.pi)/pitch) + phase)
def helixFitSin(pc1, r, pitch, phase):
    return r*numpy.sin(pc1*((2*numpy.pi)/pitch) + phase)
#Given x, predict the best y 
def fitFunction(x, y, function):
        popt, pcov = curve_fit(function, x, y, bounds=(0, [15, 25, 2*math.pi]))
        radius = popt[0]; pitch = popt[1]; phase = popt[2]
        StandardErr = numpy.sqrt(numpy.diag(pcov))
        return(radius, pitch, phase, StandardErr[0], StandardErr[1], StandardErr[2])
#Comparing sin and cos fits 
def BestFit(x,y):
        CosFit = fitFunction(x, y, helixFitCos)
        SinFit = fitFunction(x, y, helixFitSin)
        StdErrSumCos = CosFit[3] + CosFit[4] + CosFit[5]
        StdErrSumSin = SinFit[3] + SinFit[4] + SinFit[5]
        if(StdErrSumCos < StdErrSumSin):
                yOpt = [helixFitCos(c1, CosFit[0], CosFit[1], CosFit[2]) for c1 in x]
                with open("FitRadius.txt", "a") as text_file:
                        text_file.write( str(CosFit[0]) + "\n" )
                with open("FitPitch.txt", "a") as text_file:
                        text_file.write( str(CosFit[1]) + "\n" )
                with open("FitPhase.txt", "a") as text_file:
                        text_file.write( str(CosFit[2]) + "\n" )
                with open("FitRadiusSE.txt", "a") as text_file:
                        text_file.write( str(CosFit[3]) + "\n" )
                with open("FitPitchSE.txt", "a") as text_file:
                        text_file.write( str(CosFit[4]) + "\n" )
                with open("FitPhaseSE.txt", "a") as text_file:
                        text_file.write( str(CosFit[5]) + "\n" )
        else:
                yOpt = [helixFitSin(c1, SinFit[0], SinFit[1], SinFit[2]) for c1 in x]
                with open("FitRadius.txt", "a") as text_file:
                        text_file.write( str(SinFit[0]) + "\n" )
                with open("FitPitch.txt", "a") as text_file:
                        text_file.write( str(SinFit[1]) + "\n" )
                with open("FitPhase.txt", "a") as text_file:
                        text_file.write( str(SinFit[2]) + "\n" )
                with open("FitRadiusSE.txt", "a") as text_file:
                        text_file.write( str(SinFit[3]) + "\n" )
                with open("FitPitchSE.txt", "a") as text_file:
                        text_file.write( str(SinFit[4]) + "\n" )
                with open("FitPhaseSE.txt", "a") as text_file:
                        text_file.write( str(SinFit[5]) + "\n" )
        return(yOpt)
'''
args - x1,y1: True, a1, b1: Fit - Channel 1
x2,y2: True, a2, b2: Fit - Channel 2
'''
def Plot2D(x1, y1, a1, b1, x2, y2, a2, b2, title, name):
        plt.scatter(x1, y1, c='r') # True
        plt.plot(a1, b1, c='b') # Fit
        plt.scatter(x2, y2, c='g') # True
        plt.plot(a2, b2, c='y') # Fit
        plt.title(title)
        plt.ylim(-20, 20); plt.xlim(-20,20)
        plt.savefig('Output/%s/%s' % (last_line, name))
        plt.show()
        plt.close()
        
print("Channel1")
C2Pr = BestFit(C1r, C2r) # Predicts C2 given C1
C3Pr = BestFit(C1r, C3r)  # Predicts C3 given C1

print("Channel2")
C2Pg = BestFit(C1g, C2g) # Predicts C2 given C1
C3Pg = BestFit(C1g, C3g)# Predicts C3 given C1

#2D plots after fit
Plot2D(C2r, C3r, C2Pr, C3Pr, C2g, C3g, C2Pg, C3Pg, 'C2 vs C3 fit', 'C2C3Fit.png')
Plot2D(C1r, C2r, C1r, C2Pr, C1g, C2g, C1g,  C2Pg, 'C1 vs C2 fit', 'C1C2Fit.png')
Plot2D(C1r, C3r, C1r, C3Pr, C1g, C3g, C1g, C3Pg, 'C1 vs C3 fit', 'C1C3Fit.png')

#3D fit
#Original data
#Variables for C1
X1 = list(); Y1 = list(); Z1 = list()
#Variables for C2
X2 = list(); Y2 =  list(); Z2 = list()

with open ('StraightenedC1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
            X1.append(line[0])
            Y1.append(line[1])
            Z1.append(line[2])
        
with open ('StraightenedC2.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
            X2.append(line[0])
            Y2.append(line[1])
            Z2.append(line[2])
        
X1 = numpy.array(X1); Y1 = numpy.array(Y1); Z1 = numpy.array(Z1)
X2 = numpy.array(X2); Y2 = numpy.array(Y2); Z2 = numpy.array(Z2)
X1 = X1.astype(float); Y1 = Y1.astype(float); Z1 = Z1.astype(float)
X2 = X2.astype(float); Y2 = Y2.astype(float); Z2 = Z2.astype(float)

def PCs(X,Y,Z):
        data = numpy.concatenate((X[:, numpy.newaxis], 
                       Y[:, numpy.newaxis], 
                       Z[:, numpy.newaxis]), 
                      axis=1)
        #print(data)
        datamean = data.mean(axis=0)
        #print (datamean) #This is going to be the center of my helix
        uu, dd, vv = numpy.linalg.svd(data - datamean)
        #Taking the variation in the z dimension, because this is the dimension of PC1
        #Linear algebra - figure out what exactly is happening in terms of dimensional collapsation
        return vv[0], vv[1], vv[2], datamean;

C1PCs = PCs(X1, Y1, Z1); C2PCs = PCs(X2, Y2, Z2)
centerC1 = C1PCs[3]; centerC2 = C2PCs[3]
C1Pc1 = C1PCs[0]; C2Pc1 = C2PCs[0]
C1Pc2 = C1PCs[1]; C2Pc2 = C2PCs[1]
C1Pc3 = C1PCs[2]; C2Pc3 = C2PCs[2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(X1, Y1, Z1, c = 'r', marker='o')
ax.scatter3D(X2, Y2, Z2, c = 'g', marker='o')
# Plot lines connecting nearby points in Helix
#Drawing a line throught the middle of C1, C2P, C3P
for i in range(len(C1r)-1): #Go from the center into the PC's direction by this much for each point
        #Plot3D, takes a start x, end x, start y, end y, start z, end z
        start = centerC1 + C1r[i]*C1Pc1 + C2Pr[i]*C1Pc2 + C3Pr[i]*C1Pc3
        end = centerC1 + C1r[i+1]*C1Pc1 + C2Pr[i+1]*C1Pc2 + C3Pr[i+1]*C1Pc3
        ax.plot3D([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], c = 'blue', linewidth = 3)
for i in range(len(C1g)-1): #Go from the center into the PC's direction by this much for each point
        #Plot3D, takes a start x, end x, start y, end y, start z, end z
        start = centerC2 + C1g[i]*C2Pc1 + C2Pg[i]*C2Pc2 + C3Pg[i]*C2Pc3
        end = centerC2 + C1g[i+1]*C2Pc1 + C2Pg[i+1]*C2Pc2 + C3Pg[i+1]*C2Pc3
        ax.plot3D([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], c = 'yellow', linewidth = 3) #alpha=0.5) 
        ax.set_title('overall fit')
plt.show()
ax.grid(False)
ax.set_xlabel ('x, axis')
ax.set_ylabel ('y axis')
ax.set_zlabel ('z axis')
fig.savefig('Output/%s/3DFit.png' % last_line)
                
