'''
Clustering approach
- Particles of each size are separately
For each size:
- Particles within a specific x,y are grouped
- The spread in the z is determined for each group
- The median spred in the z is set as the z threshold for de-convolution
- Particles within the x,y,z, threshold are represented as just the center point 
'''

#!/usr/bin/python
import sys
import scipy.stats
import statistics
import numpy 
import csv
import math

if(sys.argv[1] == "C1.csv"): print("Clustering C1")
else: print("Clustering C2")


#Reading in all the x,y,z,size data for one channel 
X = list(); Y = list(); Z = list(); S = list()
with open (sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    for line in csv_reader:
        X.append(line[0])
        Y.append(line[1])
        Z.append(line[2])
        S.append(line[3])

#Going through S and figuring out how many sizes there are
sizes = list()
for size in S:
    if size not in sizes:
        sizes.append(size)

#Creating individual lists for coordinates of each size
numLists = len(sizes)
sizeLists = []
for i in range(numLists):
    sizeLists.append([[],[],[]])


#      S1           S2           S3
#{[[x][y][z]], [[x][y][z]], [[x][y][z]]]- size lists
#       0            1               2
#   0 1  2      0  1  2      0  1  2
#Example: access list 3 with list[2], and the ith item of list 3 with list[2][i].
for i in range(0, len(sizes)): #Going through the coordinates 3 times
    for j in range(0, len(X)-1):
        if (sizes[i] == S[j]):
            sizeLists[i][0].append(X[j])
            sizeLists[i][1].append(Y[j])
            sizeLists[i][2].append(Z[j])

'''
Given three numpy arrays x,y,z sorts the arrays consecutively and returns
sorted numpy arrays Xs, Ys, Zs
'''
def Sort(x,y,z):
    #For sorted data
    Xs = list(); Ys = list(); Zs = list()
    Xs = numpy.array(Xs, dtype=float); Ys = numpy.array(Ys, dtype=float); Zs = numpy.array(Zs, dtype=float)
    
    #Concatenating numpy arrays
    data = numpy.concatenate((x[:, numpy.newaxis], 
                       y[:, numpy.newaxis], 
                       z[:, numpy.newaxis]), 
                      axis=1)
    
    #Sorting wrt x, y, z consecutively like excel
    sortedData = data[numpy.lexsort(numpy.transpose(data)[::-1])]
    
    #Separating the sorted data into numpy arrays
    sortedArray = numpy.hsplit(sortedData, 3)
    Xs = numpy.concatenate(sortedArray[0], axis=0)
    Ys = numpy.concatenate(sortedArray[1], axis=0)
    Zs = numpy.concatenate(sortedArray[2], axis=0)
    return (Xs, Ys, Zs);

'''
Given numpy arrays with x,y,z coordinates and the radius of the particle
creates groups of particles to be clustered 
'''
def Groups(x,y,z, radius):
    XGroups = list(); YGroups = list(); ZGroups = list()
    
    #Keeping track of the points that have been visited, to avoid adding the same point to two clusters
    visited = numpy.zeros(x.size)

    for i in range(0, len(x)):
        #Refreshing the lists before generating another cluster
        similarX = list()
        similarY = list()
        listofZ = list()

        if(visited[i] == 1):
            continue
        visited[i] = 1
        similarX.append(x[i]) #adding the first x to the list
        similarY.append(y[i]) #adding the corresponding y to the list
        listofZ.append(z[i]) #adding the corresponding z to the list

        #Iterating through the rest of the array to find similar values that could be added to the group
        for j in range(i, len(x)):
            if (visited[j] == 1):
                continue
            if ((x[j]>=x[i]-radius and  x[j]<=x[i]+radius) and (y[j]>=y[i]-radius and y[j]<=y[i]+radius)):
                similarX.append(x[j])
                similarY.append(y[j])
                listofZ.append(z[j])
                visited[j] = 1
        #When you come out of the inner loop, you have one group of points
        XGroups.append(similarX); YGroups.append(similarY); ZGroups.append(listofZ)

    return(XGroups, YGroups, ZGroups)

'''
Given a specific group of points, generates the clustered points
'''
def generateCluster(xGroup, yGroup, zGroup, zThreshold):
    xOfCluster = 0.0; yOfCluster = 0.0; zOfCluster = 0.0

    maxz = numpy.amax(zGroup)
    minz = numpy.amin(zGroup)
    zlength = len(zGroup)
    zdist = maxz - minz #How spread apart the points are
    
    #In case I need to split up the arrays for recursion
    xarrays = list(); yarrays = list();zarrays = list()

    if (zdist<zThreshold): #Is one cluster
        pointpos = int(math.floor((zlength/2.0)))
        xOfCluster = xGroup[pointpos]
        yOfCluster = yGroup[pointpos]
        zOfCluster = zGroup[pointpos]
    if (zdist>zThreshold):#More than one cluster
        xarrays = numpy.array_split(xGroup, 2)
        yarrays = numpy.array_split(yGroup, 2)
        zarrays = numpy.array_split(zGroup, 2)
        generateCluster(xarrays[0],yarrays[0],zarrays[0],zThreshold)
        generateCluster(xarrays[1],yarrays[1],zarrays[1],zThreshold)
          
    clusterCenter = [xOfCluster, yOfCluster, zOfCluster]
    return (clusterCenter);

'''
Given x,y,z coordinates and the radius, groups them using the Groups method, generates clusters, and
returns the clustered x,y,z,s for the coordinates
'''
def Cluster(X,Y,Z, radius):
    X = numpy.array(X, dtype = float); Y = numpy.array(Y, dtype = float); Z = numpy.array(Z, dtype = float)

    #Sorting data
    sortedData = Sort(X, Y, Z)
    
    #Grouping points
    groupedPoints = Groups(sortedData[0],sortedData[1],sortedData[2],radius)
    
    #Getting the zThreshold
    numberOfZSplits = list()
    for i in range(0, len(groupedPoints[2])):
        if(len(groupedPoints[2][i]) != 1):
            numberOfZSplits.append(len(groupedPoints[2][i]))
    if(len(numberOfZSplits) == 0):
        MedianZSplits = 0
    else:
        MedianZSplits = math.ceil(statistics.median(numberOfZSplits))
    zThreshold = MedianZSplits*Z[Z.size-1]
    #print("Radius of RNP: ", radius)
    #print("Median point spread: ", zThreshold)

    #Creating lists to store the coordinates of clustered points
    xPoints = list(); yPoints = list(); zPoints = list(); ClusterPoints = list()

    #Going through each group and clustering points
    for i in range(0, len(groupedPoints[0])):
        ClusterPoints = generateCluster(groupedPoints[0][i], groupedPoints[1][i],groupedPoints[2][i], zThreshold)
        if (ClusterPoints[0] <= 0 or ClusterPoints[1] <= 0 or ClusterPoints[2] <= 0 ): 
            continue
        xPoints.append(ClusterPoints[0]); yPoints.append(ClusterPoints[1]); zPoints.append(ClusterPoints[2])
    xPoints = numpy.array(xPoints, dtype = float); yPoints = numpy.array(yPoints, dtype = float); zPoints = numpy.array(zPoints, dtype = float) 
    return(xPoints, yPoints, zPoints)         

#Clustering Points
cX = list(); cY = list(); cZ = list()
cX = numpy.array(cX, dtype = float); cY = numpy.array(cY, dtype = float); cZ = numpy.array(cZ, dtype = float)
for i in range (0, len(sizes)):
    clusteredPoints = Cluster(sizeLists[i][0],sizeLists[i][1],sizeLists[i][2], float(sizes[i]))
    clusteredPoints= numpy.array(clusteredPoints, dtype = float)
    cX = numpy.concatenate((cX, clusteredPoints[0]), axis=0)
    cY = numpy.concatenate((cY, clusteredPoints[1]), axis=0)
    cZ = numpy.concatenate((cZ, clusteredPoints[2]), axis=0)

numpy.savetxt(sys.argv[2], numpy.column_stack((cX, cY, cZ)), delimiter=",", fmt='%s')


