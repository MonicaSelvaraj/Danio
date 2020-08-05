'''
Creating a scatter plot of both channels and saving the image
'''

#!/usr/bin/python

#using a library called matplotlib to make a 3D plot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy 
import csv
import os

print("Scatter Plot")
#Creating a 3D axes by using the keyword projection = '3D'
fig = plt.figure( )
plt.style.use('dark_background')

#Variables for C1
x1 = list(); y1 = list(); z1 = list(); s1 = list()
#Variables for C2
x2 = list(); y2 =  list(); z2 = list(); s2 = list()

with open ('C1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #each line has X,Y,Z,S
        x1.append(line[0]); y1.append(line[1]); z1.append(line[2]); s1.append(line[3])

with open ('C2.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #each line has X,Y,Z,S
        x2.append(line[0]); y2.append(line[1]); z2.append(line[2]); s2.append(line[3])

x1 = numpy.array(x1, dtype=float); y1 = numpy.array(y1, dtype=float); z1 = numpy.array(z1, dtype=float); s1 = numpy.array(s1, dtype=float)
x2 = numpy.array(x2, dtype=float); y2 = numpy.array(y2, dtype=float); z2 = numpy.array(z2, dtype=float); s2 = numpy.array(s2, dtype=float)

ax = fig.add_subplot(111, projection = '3d' )                            
ax.grid(False)
ax.set_xlabel ('x, axis'); ax.set_ylabel ('y axis'); ax.set_zlabel ('z axis')
ax.scatter (x1, y1, z1, c = 'r', marker='o', s=s1*5)
ax.scatter (x2, y2, z2, c = 'g', marker='o', s=s2*5)
plt.show()

f_read = open("FileNames.txt", "r")
last_line = f_read.readlines()[-1]
last_line = last_line[:-1] #Ignoring newline character
f_read.close()

fig.savefig('Output/%s/ScatterPlot.png' % last_line)
