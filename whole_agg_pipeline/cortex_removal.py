'''
- Counting the number of points in each z
- Creating a scatter plot with z in the x axis and number of points in the y axis
- Clustering points using agglomerative clustering
- Finding the centroids of each cluster
- Checking if the standard deviation of the cluster centeres are greater than 5(arbitrary number)
- Checking if the highest density cluster is greater than one sd from the mean density 
- Picking the centroid with highest number of points(y)
- Seeing if it is within the first 10 z's or the last 10 z's 
- If it is - find the z spread in that cluster and determine where to chop off the z  
'''

#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy 
import csv
from matplotlib import style
style.use("ggplot")
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering

fig = plt.figure( )
f_read = open("FileNames.txt", "r")
last_line = f_read.readlines()[-1]
last_line = last_line[:-1] #Ignoring newline character
f_read.close()

print("Removing the cortex")

#Variables for cortex removal
X = list(); Y = list(); Z = list()
uniqueZ = list()

#Variables to store Channel 1 data after cortex removal
X1 = list(); Y1 = list(); Z1 = list()
#Variables to store Channel 2 data after cortex removal 
X2 = list(); Y2 =  list(); Z2 = list()

with open ('ClusteredC1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        X.append(line[0])
        Y.append(line[1])
        Z.append(line[2])
        
with open ('ClusteredC2.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        X.append(line[0])
        Y.append(line[1])
        Z.append(line[2])
'''
Given a list of x's or y's returns the highest and lowest x's or y's to keep in the cortex
'''
def findSpread(a):
    mean = numpy.mean(a)
    sd = numpy.std(a)

    #Fnding lower bound 
    for i in range(0, len(a)):
        if(a[i] <= (mean - 2*sd)):
            continue
        else:
            low = a[i]
            break

    #Finding upper bound
    for i in range(len(a)-1, 0, -1):
        if(a[i] >= (mean + 2*sd)):
            continue
        else:
            high = a[i]
            break
    return(low, high)

'''
Given a z-range returns a list of x's and y's within that range
z1 - lowerz, z2 - upper z
X, Y - X, Y, Z points 
'''
def listOfPoints(z1, z2, x, y, z):
    xInRange = list(); yInRange = list()
    for i in range(0, len(Z)):
        if(Z[i] >= z1 or Z[i] <= z2):
            xInRange.append(X[i])
            yInRange.append(Y[i])
    xInRange = numpy.array(xInRange, dtype = float)
    yInRange = numpy.array(yInRange, dtype = float)
    return(xInRange, yInRange)

for z in Z:
    if z not in uniqueZ:
        uniqueZ.append(z)

Z = numpy.array(Z, dtype=float); 
uniqueZ = numpy.array(uniqueZ, dtype = float)
uniqueZ = numpy.sort(uniqueZ) #This is a list of Z's from highest to lowest

zCount = list()
for uz in uniqueZ:
    counter = 0
    for z in Z:
        if (z == uz):
            counter = counter+1
    zCount.append(counter)

plt.scatter(uniqueZ, zCount)
plt.xlabel('Z')
plt.ylabel('ZPointCount')
fig.savefig('Output/%s/ZvsDensity.png' % last_line)
#plt.show()
plt.clf()

#The input for clustering is in the form [[z, count], [z, count], .. ]
clusterInput = numpy.array(list(zip(uniqueZ,zCount)))
clusterInput = numpy.array(clusterInput ); clusterInput  = clusterInput .astype(float)

#Agglomerative Clustering

#Creating Dendrogram - change 
dendrogram = sch.dendrogram(sch.linkage(clusterInput, method='ward'))
#fig.savefig('Output/%s/Dendrogram.png' % last_line)
#plt.show()
plt.clf()

#Creating four clusters 
hc = AgglomerativeClustering(n_clusters=4, affinity = 'euclidean', linkage = 'ward')
y_hc = hc.fit_predict(clusterInput)#Labels each point as cluster 0,1,2, or 3

#Finding the cluster centers 
centroidX = list(); centroidY = list()

for c in range(4):
    zList = list(); zDensity = list() #Creating  a new list for each cluster 
    zList = clusterInput[y_hc ==c,0] #Creates a list of all the z's in that cluster
    zDensity = clusterInput[y_hc == c,1] #Creates a list of densities for the z's of that cluster 
    #Finding the centroids
    centroidX.append(sum(zList) / len(zList))
    centroidY.append(sum(zDensity) / len(zDensity))

#Displaying the clusters with centroids
plt.scatter(clusterInput[y_hc ==0,0], clusterInput[y_hc == 0,1], s=100, c='red')
plt.scatter(clusterInput[y_hc==1,0], clusterInput[y_hc == 1,1], s=100, c='black')
plt.scatter(clusterInput[y_hc == 2,0], clusterInput[y_hc == 2,1], s=100, c='blue')
plt.scatter(clusterInput[y_hc ==3,0], clusterInput[y_hc == 3,1], s=100, c='cyan')
plt.scatter(centroidX, centroidY, s = 200, c = 'green')
plt.xlabel('Z')
plt.ylabel('ZPointCount')
fig.savefig('Output/%s/AgglomerativeClustering.png' % last_line)
plt.clf()
#plt.show()

centroidX = numpy.array(centroidX, dtype = float)
centroidY = numpy.array(centroidY, dtype = float)


#Finding the cluster center with highest zDensity
highestDensityCluster = numpy.amax(centroidY)
#Finding the position of that cluster 
highestDensityPos = numpy.where(highestDensityCluster == centroidY)
highestDensityPos = highestDensityPos[0][0]

PossibleCortexZPositions = numpy.where(y_hc == highestDensityPos)
PossibleCortexZs = list()
for z in PossibleCortexZPositions:
    PossibleCortexZs.append(clusterInput[z, 0])


#Mean and standard deviation of the z density 
MeanDensity = numpy.mean(centroidY, axis = 0)
with open("MeanCortexDensity.txt", "a") as text_file:
    text_file.write( str(MeanDensity) + "\n" )
    
sdDensity= numpy.std(centroidY, axis = 0)
with open("sdCortexDensity.txt", "a") as text_file:
    text_file.write( str(sdDensity) + "\n" )


cortexFound = True
#Checking if the standard deviation of the density of the clusters is greater than 5
if(sdDensity >= 5):
    #Checking if the cluster center with highest density of greater than one sd away from the mean density
    if(centroidY[highestDensityPos] >= (sdDensity + MeanDensity)):
        if(centroidX[highestDensityPos] >= uniqueZ[10]): #Within the last 10 z's
            #Finding the lowest z in that cluster and removing all the z's after it
            lowestZ = numpy.amin(PossibleCortexZs) - 2
            #Find x's and y's in the three z's below the lowest z 
            #pointsToFindRange = listOfPoints(lowestZ-4, lowestZ-1, X,Y, Z)
            #Find the x and y range to keep in the cortex
            #xRange = findSpread(pointsToFindRange[0])
            #yRange = findSpread(pointsToFindRange[1])
            with open ('ClusteredC1.csv', 'r') as csv_file:
                csv_reader = csv.reader (csv_file)
                for line in csv_reader:
                    if(float(line[2]) < lowestZ): #or (float(line[0])>xRange[0] and float(line[0])<xRange[1] and float(line[1])>yRange[0] and float(line[1])<yRange[1])):
                        X1.append(line[0])
                        Y1.append(line[1])
                        Z1.append(line[2])
            with open ('ClusteredC2.csv', 'r') as csv_file:
                csv_reader = csv.reader (csv_file)
                for line in csv_reader:
                    if(float(line[2]) < lowestZ): #or (float(line[0])>xRange[0] and float(line[0])<xRange[1] and float(line[1])>yRange[0] and float(line[1])<yRange[1])):
                        X2.append(line[0])
                        Y2.append(line[1])
                        Z2.append(line[2])
        elif(centroidX[highestDensityPos] <= uniqueZ[len(uniqueZ) - 10]): #Within the first 10 z's
            #Finding the highest z in that cluster and all the z's before it
            highestZ = numpy.amax(PossibleCortexZs) + 2
            #Find x's and y's in the three z's above the highest z 
            #pointsToFindRange = listOfPoints(highestZ+1, highestZ+4, X,Y, Z)
            #Find the x and y range to keep in the cortex
            #xRange = findSpread(pointsToFindRange[0])
            #yRange = findSpread(pointsToFindRange[1])                      
            with open ('ClusteredC1.csv', 'r') as csv_file:
                csv_reader = csv.reader (csv_file)
                for line in csv_reader:
                    if(float(line[2]) > highestZ): #or (float(line[0])>xRange[0] and float(line[0])<xRange[1] and float(line[1])>yRange[0] and float(line[1])<yRange[1])):
                        X1.append(line[0])
                        Y1.append(line[1])
                        Z1.append(line[2])
            with open ('ClusteredC2.csv', 'r') as csv_file:
                csv_reader = csv.reader (csv_file)
                for line in csv_reader:
                    if(float(line[2]) < highestZ): #or (float(line[0])>xRange[0] and float(line[0])<xRange[1] and float(line[1])>yRange[0] and float(line[1])<yRange[1])):
                        X2.append(line[0])
                        Y2.append(line[1])
                        Z2.append(line[2])
        else:
            print("No cortex found")
            cortexFound = False
    else:
        print("No cortex found")
        cortexFound = False
else:
    print("No cortex found")
    cortexFound = False

if(cortexFound == False):
    with open ('ClusteredC1.csv', 'r') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
            X1.append(line[0])
            Y1.append(line[1])
            Z1.append(line[2])
    with open ('ClusteredC2.csv', 'r') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
            X2.append(line[0])
            Y2.append(line[1])
            Z2.append(line[2])

    
X1 = numpy.array(X1, dtype=float); Y1 = numpy.array(Y1, dtype=float); Z1 = numpy.array(Z1, dtype=float)
X2 = numpy.array(X2, dtype=float); Y2 = numpy.array(Y2, dtype=float); Z2 = numpy.array(Z2, dtype=float)

#Saving each channel's data after removing the cortex in new files
numpy.savetxt("CortexRemovedC1.csv", numpy.column_stack((X1, Y1, Z1)), delimiter=",", fmt='%s')
numpy.savetxt("CortexRemovedC2.csv", numpy.column_stack((X2, Y2, Z2)), delimiter=",", fmt='%s')










    
