'''
Plotting original data and clustered data (size has not been taken into account)
'''

#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import style
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy 
import csv

fig = plt.figure( )
plt.style.use('dark_background')

print("Producing scatter plot after clustering")

#Plot of original data
#Variables for C1
X1 = list(); Y1 = list(); Z1 = list()
#Variables for C2
X2 = list(); Y2 =  list(); Z2 = list()

with open ('C1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #each line has X,Y,Z,S
        X1.append(line[0])
        Y1.append(line[1])
        Z1.append(line[2])
        
with open ('C2.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #each line has X,Y,Z,S
        X2.append(line[0])
        Y2.append(line[1])
        Z2.append(line[2])
        

X1 = numpy.array(X1); Y1 = numpy.array(Y1); Z1 = numpy.array(Z1)
X2 = numpy.array(X2); Y2 = numpy.array(Y2); Z2 = numpy.array(Z2)
X1 = X1.astype(float); Y1 = Y1.astype(float); Z1 = Z1.astype(float)
X2 = X2.astype(float); Y2 = Y2.astype(float); Z2 = Z2.astype(float)

#Generating a plot of the original points
ax = fig.add_subplot(1,2,1, projection = '3d')
ax.grid(False)
red = ax.scatter (X1, Y1, Z1, c = 'r', marker='o', s=1, linewidths=2)
green = ax.scatter (X2, Y2, Z2, c = 'g', marker='o', s=1, linewidths=2)
ax.set_title('Unclustered')
ax.legend((red, green),
           ( 'C1', 'C2'),
           scatterpoints=1,
           loc='best',
           ncol=1,
           fontsize=8)
ax.set_xlabel ('x, axis')
ax.set_ylabel ('y axis')
ax.set_zlabel ('z axis')

#Generating a scatter plot of the points after clustering
#Variables for deconvolutedC1
dX1 = list(); dY1 = list(); dZ1 = list()
#Variables for deconvolutedC2
dX2 = list(); dY2 =  list(); dZ2 = list()

with open ('ClusteredC1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #each line has X,Y,Z
        dX1.append(line[0])
        dY1.append(line[1])
        dZ1.append(line[2])

with open ('ClusteredC2.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #each line has X,Y,Z
        dX2.append(line[0])
        dY2.append(line[1])
        dZ2.append(line[2])

dX1 = numpy.array(dX1); dY1 = numpy.array(dY1); dZ1 = numpy.array(dZ1)
dX2 = numpy.array(dX2); dY2 = numpy.array(dY2); dZ2 = numpy.array(dZ2)
dX1 = dX1.astype(float); dY1 = dY1.astype(float); dZ1 = dZ1.astype(float) 
dX2 = dX2.astype(float); dY2 = dY2.astype(float); dZ2 = dZ2.astype(float)

#Generating a plot of the deconvoluted points
ax = fig.add_subplot(1,2,2, projection = '3d')
ax.grid(False)
red = ax.scatter (dX1, dY1, dZ1, c = 'r', marker='o', s=1, linewidths=2)
green = ax.scatter (dX2, dY2, dZ2, c = 'g', marker='o', s=1, linewidths=2)
ax.set_title('Clustered')
ax.legend((red, green),
           ( 'C1', 'C2'),
           scatterpoints=1,
           loc='best',
           ncol=1,
           fontsize=8)
ax.set_xlabel ('x, axis')
ax.set_ylabel ('y axis')
ax.set_zlabel ('z axis')
plt.show()

f_read = open("FileNames.txt", "r")
last_line = f_read.readlines()[-1]
last_line = last_line[:-1] #Ignoring newline character
f_read.close()
fig.savefig('Output/%s/ClusteredPlot.png' % last_line)


    
    


