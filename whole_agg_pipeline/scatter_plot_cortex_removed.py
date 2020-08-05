'''
Creating a scatter plot of both channels after the cortex has been removed 
'''

#!/usr/bin/python

#using a library called matplotlib to make a 3D plot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy 
import csv

print("Producing Scatter Plot after cortex removal")
#Creating a 3D axes by using the keyword projection = '3D'
fig = plt.figure( )
plt.style.use('dark_background')

#Variables for C1
X1 = list(); Y1 = list(); Z1 = list()

#Variables for C2
X2 = list(); Y2 =  list(); Z2 = list()

with open ('CortexRemovedC1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #each line has X,Y,Z,S
        X1.append(line[0])
        Y1.append(line[1])
        Z1.append(line[2])

with open ('CortexRemovedC2.csv', 'r') as csv_file:
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

ax = fig.add_subplot(111, projection = '3d' )                            
ax.grid(False)
ax.set_xlabel ('x, axis'); ax.set_ylabel ('y axis'); ax.set_zlabel ('z axis')
ax.scatter (X1, Y1, Z1, c = 'r', marker='o', s = 10)
ax.scatter (X2, Y2, Z2, c = 'g', marker='o', s = 10)
plt.show()

f_read = open("FileNames.txt", "r")
last_line = f_read.readlines()[-1]
last_line = last_line[:-1] #Ignoring newline character
f_read.close()

fig.savefig('Output/%s/ScatterPlotCortexRemoved.png' % last_line)
