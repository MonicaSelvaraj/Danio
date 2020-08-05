'''
Reading in De-convoluted points
Drawing the first, second, and third principal component through the points
Creating 2D projections of the points wrt the PC's
writing C1s, C2s and C3s into a new file
'''

#!/usr/bin/python
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
import scipy.stats
import statistics
import numpy 
import csv
import math
from scipy.optimize import curve_fit

fig = plt.figure( )
plt.style.use('dark_background')

if(sys.argv[3] == "r" ): print("C1 2D projections")
else: print("C2 2D projections")

#Variables to store deconvoluted points 
X = list(); Y = list(); Z = list() 

#Reading in the data 
with open (sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    for line in csv_reader:
            X.append(line[0])
            Y.append(line[1])
            Z.append(line[2])
       
X = numpy.array(X); Y = numpy.array(Y); Z = numpy.array(Z)
X = X.astype(float); Y= Y.astype(float); Z= Z.astype(float)

def PCs(X,Y,Z):
        data = numpy.concatenate((X[:, numpy.newaxis], 
                       Y[:, numpy.newaxis], 
                       Z[:, numpy.newaxis]), 
                      axis=1)
        datamean = data.mean(axis=0) #Center of helix
        uu, dd, vv = numpy.linalg.svd(data - datamean)
        #Taking the variation in the z dimension, because this is the dimension of PC1
        return vv[0], vv[1], vv[2], datamean;

PCsOutput = PCs(X, Y, Z)

#Drawing PC's through data
lineptsPC1 = PCsOutput[0] * numpy.mgrid[-50:50:2j][:, numpy.newaxis]
lineptsPC2 = PCsOutput[1] * numpy.mgrid[-15:15:2j][:, numpy.newaxis]
lineptsPC3 = PCsOutput[2] * numpy.mgrid[-15:15:2j][:, numpy.newaxis]

#Moving the line to be in between the points
lineptsPC1 += PCsOutput[3]; lineptsPC2 += PCsOutput[3]; lineptsPC3 += PCsOutput[3]

#Principal components plot
ax = fig.add_subplot(1,1,1, projection = '3d')
ax.grid(False)
ax.scatter (X, Y, Z, c = sys.argv[3], marker='o', linewidths=2)
ax.set_title('Principal Components')
ax.set_xlabel ('x, axis')
ax.set_ylabel ('y axis')
ax.set_zlabel ('z axis')
ax.plot3D(*lineptsPC1.T)
ax.plot3D(*lineptsPC2.T)
ax.plot3D(*lineptsPC3.T)
plt.show()
fig.savefig(sys.argv[4])

#2D projections
Points = list(zip(X,Y,Z))
center = PCsOutput[3]
Pc1 = PCsOutput[0]
Pc2 = PCsOutput[1]
Pc3 = PCsOutput[2]
#If we don't sort - it might looks like a bunch of scribbles - sorted draws a nice line
Points.sort(key=lambda i: numpy.dot(Pc1, i)) # Sorts by first PC so it draws lines nicely
C1s = numpy.dot(Points - center, Pc1) # Components in first PC direction
C2s = numpy.dot(Points - center, Pc2) # Components in second PC direction
C3s = numpy.dot(Points - center, Pc3) # Components in third PC direction

#Writing C1s, C2s, and C3s into a file
numpy.savetxt(sys.argv[2], numpy.column_stack((C1s, C2s, C3s)), delimiter=",", fmt='%s')






