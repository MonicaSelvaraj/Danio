'''
Usage: Given coordinates in 3D (read from a file), this script draws the first (PC1), second (PC2), and third (PC3) principal components through the coordinates. 
Then the 2D projections of the coordinates wrt the principal components are obtained, to determine the components of the coordinates in  the PC1, PC2, and PC3 directions.  

Input: bootstrapped 3D coordinates from a file named "input"

Output: Components of the coordinates in the PC1, PC2, and PC3
directions to a file named "projections". 
'''

#!/usr/bin/python
import csv
import numpy as np

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

'''
Usage: To define PC1, PC2, and PC3 through input coordinates.
params: x,y,z coordinates
returns: PC1, PC2, PC3 directions
'''
def PCs(x,y,z):
    data = np.concatenate((x[:, np.newaxis],
                   y[:, np.newaxis],
                   z[:, np.newaxis]),
                  axis=1)
    datamean = data.mean(axis=0) #Center of helix
    uu, dd, vv = np.linalg.svd(data - datamean)
    #Taking the variation in the z dimension, because this is the dimension of PC1
    return vv[0], vv[1], vv[2], datamean

'''
Usage: Given PC1, PC2, and PC3, determines the components of the input coordinates in each PC direction.
params: input coordinates, center of the helix, PCs
returns: c1, c2, c3 - components in each PC direction
'''
def project2D(points, center, pc1, pc2, pc3):
    #If we don't sort - it might looks like a bunch of scribbles - sorted draws a nice line
    points.sort(key=lambda i: np.dot(pc1, i)) # Sorts by first PC so it draws lines nicely
    c1 = np.dot(points - center, pc1) # Components in first PC direction
    c2 = np.dot(points - center, pc2) # Components in second PC direction
    c3 = np.dot(points - center, pc3) # Components in third PC direction
    return c1, c2, c3

#Read input from file 
x,y,z = getPoints("input.csv")
#Get PCs
pc1,pc2,pc3, center = PCs(x,y,z)
#Get 2D projections
c1,c2,c3 = project2D(list(zip(x,y,z)), center, pc1, pc2, pc3)
#Write projections to file
np.savetxt("projections.csv", np.column_stack((c1, c2, c3)), delimiter=",", fmt='%s')







