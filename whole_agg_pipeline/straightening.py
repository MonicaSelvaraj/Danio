#!/usr/bin/python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np 
import csv
from scipy.spatial import distance
import math

print("Straightening")
f_read = open("FileNames.txt", "r")
last_line = f_read.readlines()[-1]
last_line = last_line[:-1] #Ignoring newline character
f_read.close()
plt.style.use('dark_background')


'''
HELPER METHODS
'''
'''
Use: To read a file with x,y,z coordinates, and store the data for each dimension in a separate array.
params: filename - File with x,y,z cooridnates
returns: 3 arrays with x's, y's and z's
'''
def getPoints(filename):
    x = list(); y = list(); z = list()
    with open (filename, 'r') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
            x.append(line[0]); y.append(line[1]); z.append(line[2])
    x = np.array(x, dtype = float); y = np.array(y, dtype = float); z = np.array(z, dtype = float)
    return (x, y, z)

'''
Use: Given a, find a's nearest neighbor in P
params: a - coordinate for which the nearest neighbor is to be found
P - set of points to look through
returns: p - index of a's nearest neighbor in P
d - distance between a and its nearest neigbor in P 
'''
def nearestNeighbor(a,P):
    d = 10000; p = -1 
    for i in range(0, len(P)):
        currdist = distance.euclidean(a,P[i])
        if(currdist<d): 
            d = currdist
            p = i
    return(p,d)

'''
Use: To swap elements in index a and b in a given list P
params: a,b - index of the elements that need to be swapped
P - list containing the elements that need to be swapped
returns: the list P with elements in index a,b swapped

'''
def swap(P,a,b):
    temp = np.copy(P[a])
    P[a] = P[b] 
    P[b] = temp
    return P

'''
Use: To order a list of points on the principal curve from start to end of the curve 
params: x,y,z - coordinates of points on the principal curve 
returns: three arrays with x,y,z coordinates in the order determined

Approach:
Given a list of points,
- For the point in index 0, call it a, find its nearest neighbor from the remaining points in the list, call it b.
- Swap a's immediate neighbor, element in index 1, with the element in position b.
- From the list of points excluding a and b, find the nearest neighbor for a, call it c, and b, call it d.
- Once c and d are found, the following two cases are checked,
  Case 1: If c == d, i.e. if both a and b have the same neighbor, check if the new nearest neighbor found is closer to a or b.
    If it is closer to b, swap b's immediate neighbor with the element in position d. If it is closer to a, add the element
    in position c to the left of a, i.e to the beginning of the list. 
  Case 2: If c != d, swap b's immediate neighbor with the element in position d and add the element
    in position c to the left of a, i.e to the beginning of the list.
- In this way keep finding the nearest neighbors of the most recently swapped/added elements, and grow the array in both directions.
- Note that this method works if the first element in the original list is in the middle of the curve or one end of the curve.
'''
def RankPC(x,y,z):
    P = np.concatenate((x[:, np.newaxis],
                       y[:, np.newaxis], 
                       z[:, np.newaxis]),
                    axis=1)
    lenP = len(P)
    
    #Finding the nearest neighbor of the first point - P0 and moving it to position P1
    p, d = nearestNeighbor(P[0],P[1:lenP])
    p+=1 #Didn't consider the 0th element while finding the position of the nearest neighbor 
    P = swap(P,1,p)

    j = 1
    while j<lenP-1:
        p0,d0 = nearestNeighbor(P[0],P[j+1:lenP]) #Finding the nearest neighbor of P0 in the remaining elements 
        p0 = p0+j+1
        pj,dj = nearestNeighbor(P[j], P[j+1:lenP]) #Finding the nearest neighbor of Pj in the remaining elements 
        pj = pj+j+1
        
        if(p0 == pj):#If they both have the same nearest neighbor
            if(d0 < dj): #If the nearest neighbor is closest to P0
                #Add the nearest neighbor to the beginning of P, and delete it from its original location 
                P = np.insert(P, 0, P[p0], axis=0); P = np.delete(P, p0+1, 0)
            else: #Else swap positions pj with j+1
                P = swap(P,j+1,pj)  
            j+=1 #incrementing by one because only one side gets an additional element 
        else: #If their nearest neighbors are different then adding both 
            P = swap(P,j+1,pj) #Swapping does not change p0
            P = np.insert(P, 0, P[p0], axis=0)
            P = np.delete(P, p0+1, 0)
            j+=2 #incrementing by two because both sides get additional elements 
    
    P = np.hsplit(P, 3)
    xr = np.concatenate(P[0], axis=0)
    yr = np.concatenate(P[1], axis=0)
    zr = np.concatenate(P[2], axis=0)
    return (xr, yr, zr)

'''
Use: To find the rotation matrix that rotates unit vector a onto unit vector b
(Source: https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d/897677#897677)
params: a,b - unit vectors 
returns: A rotation matrix that when multiplied with a, aligns it with b
'''
def R(a, b):
    I = np.identity(3)
    v = np.cross(a,b)
    s = np.linalg.norm(v)
    c = np.dot(a,b)
    if(s == 0): return I #Angle between vectors is zero
    vXStr = '{} {} {}; {} {} {}; {} {} {}'.format(0, -v[2], v[1], v[2], 0, -v[0], -v[1], v[0], 0)
    vx = np.matrix(vXStr)
    Rot = I + vx + np.matmul(vx, vx) * ((1 -c)/(s**2))
    #if (math.isnan(Rot)): return I
    return (Rot)

'''
Use: Defines x,y,z axes for every point on the principal curve based on the angle of rotation between two consecutive points 
params: CurvePts - ordered points on the principal curve 
returns: three lists of vectors defining the axes for every point on the principal curve 

Approach:
For a given list of points from start to end of the principal curve,
- Find the vector between the first two points on the curve. This is the z axis for the first point. 
- Then, define the x and y axes at the first point by finding two more vectors such that the x,y,z axes are othogonal to each other.
- Next, find the vector between the second and third points on the curve. This is the z axis for the second point. 
- Find the matrix of rotation between the z axis at the first point and the second point.
- Mutiply the x and y axes of the first point by the matrix of rotation. The rotated axes are the x and y axes at the second point. 
- Repeat this for every set of consecutive points on the curve. 
'''
def Axes(CurvePts):
    #Storing the points of the principal cuve - the points are ordered 
    x = list(); y = list(); z = list()
    x = CurvePts[0]; y = CurvePts[1]; z = CurvePts[2]

    #Finding the axes for each set of consecutive points on the curve
    xAxes = list(); yAxes= list(); zAxes = list()

    for i in range(0, len(x)-1):
        
        #Finding the current z vector 
        zA = ([(x[i+1] - x[i]), (y[i+1] - y[i]), (z[i+1] - z[i])])
        #print(zA)
        zA = (zA/np.linalg.norm(zA))
        zAxes.append(zA)
        
        if( i == 0): #Defining two orthogonal axes for the first z axis
            
            #Defining the new x axis using the fact that the dot product between two orthogonal vectors is zero
            xA = [1,1, ((1*zA[0])+(1*zA[1]))/ (-zA[2])]
            xAxes.append(xA/np.linalg.norm(xA))

            #Defining the new y axis using the fact that the cross product between two vectors is an orthogonal vector
            yA = np.cross(xAxes[0], zA)
            yAxes.append(yA/np.linalg.norm(yA))
    
        else: #Finding the rotation matrix between the current z vector and the old z vector, and rotating the old x and y vectors by the same amount to find new vectors 
            Rot = R(zA, (zAxes[i-1]))
    
            #Rotating the previous x and y axes vectors by the same rotation matrix to find the new axes
            xA = np.matmul(Rot, np.squeeze(np.asarray(xAxes[i-1])))#converting the matrix to array before using for rotation
            xAxes.append(np.squeeze(np.asarray(xA/np.linalg.norm(xA))))

            yA = np.matmul(Rot, np.squeeze(np.asarray(yAxes[i-1])))
            yAxes.append(np.squeeze(np.asarray(yA/np.linalg.norm(yA))))

    #Defining the axes for the last point to be the same as the second to last point    
    xAxes.append(np.squeeze(np.asarray(xA/np.linalg.norm(xA))))
    yAxes.append(np.squeeze(np.asarray(yA/np.linalg.norm(yA))))
    zAxes.append(zA)
    return(xAxes, yAxes, zAxes)
 
'''
Use: To pick ~50 points at equal intervals from the list of ordered points on the principal curve.
Note: This method is used since there are a large number of points on the principal curve, and the matrix of rotation between two 
very closely spaced points in undefined. 
params: x,y,z - coordinates of points on the principal curve 
returns: three lists with ~50 x,y,z cooridnates picked at equal intervals
'''
def pick50points(x,y,z):
    interval = math.ceil(len(x)/50)
    i = 0
    newx = list(); newy = list();newz = list()
    newx.append(x[0]);newy.append(y[0]);newz.append(z[0])
    i+=interval
    while(i<len(x)):
        nextVector = [(x[i] - x[i-interval]), (y[i] - y[i-interval]), (z[i] - z[i-interval])]
        if(np.linalg.norm(nextVector) == 0): #Removing duplicates
            i+=interval
            continue
        else:
            newx.append(x[i])
            newy.append(y[i])
            newz.append(z[i])
            i+=interval
    newx = np.array(newx, dtype = float); newy = np.array(newy, dtype = float); newz = np.array(newz, dtype = float)
    return(newx, newy, newz)

'''
Use: For each RNP, finds the point on the principal curve that the RNP is closest to. The RNP is projected onto the axes at this point
to find its normalized/straightened coordinates. 
params: CurvePts - ordered points on the principal curve, x,y,z - coordinates of RNP's
returns: A list of points that specify which point on the principal curve each RNP should be projected onto
'''
def pointToProject(CurvePts, x,y,z):
    xC = list(); yC = list(); zC = list()
    xC = CurvePts[0]; yC = CurvePts[1]; zC = CurvePts[2]
    #Creating a list of the index of the point on the line that each x,y,z is closets to
    closestPointPos = 0; i=0; j=0; indexOfClosestPoints = list()
    for i in range (0, len(x)): #looping through all the x,y,z coordinates
        mindst = 10000 #Setting an upper limit on the minimum distance 
        for j in range(0, len(xC)): #For every coordinate, looping through each point on the line
            a = (x[i], y[i], z[i])
            b = (xC[j], yC[j], zC[j])
            if (distance.euclidean(a,b)) < mindst:
                mindst = (distance.euclidean(a,b))
                closestPointPos = j
        indexOfClosestPoints.append(closestPointPos)
    return (indexOfClosestPoints)

def DisplacementToLine(CurvePts, linePtsDistances):
    xPoints = list(); yPoints = list(); zPoints = list()
    xPoints = CurvePts[0]; yPoints = CurvePts[1]; zPoints = CurvePts[2]

    #Finding a vector between the first two points
    #v = ([(xPoints[1] - xPoints[0]), (yPoints[1] - yPoints[0]), (zPoints[1] - zPoints[0])])
    v = (0,0,1) #Vector pointing along the z
    #print(v)
    
    #Normalizing the vector 
    nv = v/np.linalg.norm(v)
    
    pointsAlongLine = list() 
    #Finding a point along the vector at distance d for each curve point 
    for i in range(0,len(linePtsDistances)):
        pointsAlongLine.append((0,0,0)+(nv*linePtsDistances[i]))
    #print(pointsAlongLine)
    
    #Finding the x,y,z displacement for each curve point to the point on the line 
    #Vectors for displacement 
    displacement = list()
    #print(pointsAlongLine)
    for i in range(0,len(linePtsDistances)):
        displacement.append(pointsAlongLine[i] - (xPoints[i],yPoints[i],zPoints[i]))
    
    return (pointsAlongLine, displacement)
    

'''
Use: To find the straightened/normliazed coordinates of RNPs
params: CurvePts - ordered points on the principal curve;
xAxis, yAxis, zAxis - x,y,z axes for each point on the principal curve 
x,y,z - coordinates of RNP's
returns: coordinates of RNP's after straightening/normalization.

Approach:
- For each RNP, project it onto the axes of the point on the principal curve determined from 'pointToProject'
- To the new z coordinate for each RNP, add the distance it takes to get to the point on the principal curve that 
the RNP was projected onto. 
'''
def Straighten(CurvePts, xAxis, yAxis, zAxis, x,y,z):
    xPoints = list(); yPoints = list(); zPoints = list()
    xPoints = CurvePts[0]; yPoints = CurvePts[1]; zPoints = CurvePts[2]
    
    #Finding the distance between every pair of points and storing the cumulative distances to get to that point from the first point on the curve
    linePtsDistances = list()
    cumulativeDistance = 0 #Keeps track of cumulative distance till that point
    linePtsDistances.append(0) #Don't have to add anything for the first point 
    for i in range (0, len(xPoints)-1,1):
        a = (xPoints[i], yPoints[i], zPoints[i])
        b = (xPoints[i+1], yPoints[i+1], zPoints[i+1])
        dst = distance.euclidean(a,b)
        cumulativeDistance = cumulativeDistance + dst
        linePtsDistances.append(cumulativeDistance)
        
    pointsAlongLine,displacement = DisplacementToLine(CurvePts, linePtsDistances)
    #print(displacement)
    #print(pointsAlongLine)
    
    p = pointToProject(CurvePts, x,y,z) #list of points onto which each data point should be projected onto
    sx = list(); sy = list(); sz = list()
    
    for i in range(0, len(x)-1):
        rnpCoordinate = (x[i],y[i],z[i])
        curveCoordinate  = (xPoints[p[i]],yPoints[p[i]],zPoints[p[i]])
        #Subtracting the paired curve point from the RNP coordinate before finding the dot product
        rnpShifted = rnpCoordinate[0] - curveCoordinate[0], rnpCoordinate[1] - curveCoordinate[1],rnpCoordinate[2] - curveCoordinate[2] #Shifting the RNPs origin to the curve point onto which it is projected 
        #print(rnpCoordinate)
        #print(curveCoordinate)
        #print(rnpShifted)
        
        Sx = np.dot(rnpShifted, xAxis[p[i]])
        Sy = np.dot(rnpShifted, yAxis[p[i]])
        Sz = np.dot(rnpShifted, zAxis[p[i]])
    
    
        sx.append(pointsAlongLine[p[i]][0]+Sx)
        sy.append(pointsAlongLine[p[i]][1]+Sy)
        sz.append(pointsAlongLine[p[i]][2]+Sz)
        
        #sx.append(Sx)
        #sy.append(Sy)
        #sz.append(Sz)
    
        #print(sx)
        #sz.append(np.dot([x[i], y[i], z[i]], zAxis[p[i]]) + linePtsDistances[p[i]] + displacement[p[i]][2])
    
    sx = np.array(sx, dtype = float); sy = np.array(sy, dtype = float); sz = np.array(sz, dtype = float)
    
    return(pointsAlongLine,sx, sy, sz)

'''
MAIN
'''
#Reading the principal curve points from file
PCpoints = getPoints('fitpoints.csv')
#print(PCpoints)
#Ranking PC points 
PCranked = RankPC(PCpoints[0],PCpoints[1],PCpoints[2])
#print(PCranked)
#Picking 50 points of the ranked PC points 
PC50 = pick50points(PCranked[0],PCranked[1],PCranked[2])
#Defining axes for those 50 points 
axes = Axes(PC50)
#print(axes)
#Reshaping arrays for plotting axes 
xv = np.vstack(axes[0]); yv = np.vstack(axes[1]);zv = np.vstack(axes[2])
xh = np.hsplit(xv, 3); yh = np.hsplit(yv, 3); zh = np.hsplit(zv, 3)
xx = np.concatenate(xh[0], axis=0); xy = np.concatenate(xh[1], axis=0); xz = np.concatenate(xh[2], axis=0)
yx = np.concatenate(yh[0], axis=0); yy = np.concatenate(yh[1], axis=0); yz = np.concatenate(yh[2], axis=0)
zx = np.concatenate(zh[0], axis=0); zy = np.concatenate(zh[1], axis=0); zz = np.concatenate(zh[2], axis=0)

#Reading in C1 and C2 points
RNPCoordinatesC1 = getPoints('CortexRemovedC1.csv')
RNPCoordinatesC2 = getPoints('CortexRemovedC2.csv')

#Straightening/Normalization 
StraightRNPC1 = Straighten(PC50, xv, yv, zv, RNPCoordinatesC1[0],RNPCoordinatesC1[1],RNPCoordinatesC1[2])
StraightRNPC1 = StraightRNPC1[1:4]
StraightRNPC2 = Straighten(PC50, xv, yv, zv, RNPCoordinatesC2[0],RNPCoordinatesC2[1],RNPCoordinatesC2[2])
StraightRNPC2 = StraightRNPC2[1:4]

#Plotting the original points and the principal curve
fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection = '3d')
ax.scatter (RNPCoordinatesC1[0], RNPCoordinatesC1[1], RNPCoordinatesC1[2], c = 'r', marker='o', s=1, linewidths=2)
ax.scatter (RNPCoordinatesC2[0], RNPCoordinatesC2[1], RNPCoordinatesC2[2], c = 'g', marker='o', s=1, linewidths=2)
ax.scatter(PCpoints[0], PCpoints[1], PCpoints[2], c = 'b', marker = '*', s=1, linewidths=2)
ax.set_xlabel ('x, axis')
ax.set_ylabel ('y axis')
ax.set_zlabel ('z axis')
plt.show()
ax.grid(False)
fig.savefig('Output/%s/PrincipalCurve.png' % last_line)

#Plotting the straightened points
fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection = '3d')
ax.scatter (StraightRNPC1[0],StraightRNPC1[1],StraightRNPC1[2], c = 'r', marker='o', s=1, linewidths=2)
ax.scatter (StraightRNPC2[0],StraightRNPC2[1],StraightRNPC2[2], c = 'g', marker='o', s=1, linewidths=2)
ax.set_xlabel ('x, axis')
ax.set_ylabel ('y axis')
ax.set_zlabel ('z axis')
plt.show()
ax.grid(False)
fig.savefig('Output/%s/Straightened.png' % last_line)
#Writing straightened points to a file
StraightRNPC1= np.array(StraightRNPC1, dtype = float)
StraightRNPC2= np.array(StraightRNPC2, dtype = float)
np.savetxt("StraightenedC1.csv", np.column_stack((StraightRNPC1[0], StraightRNPC1[1], StraightRNPC1[2])), delimiter=",", fmt='%s')
np.savetxt("StraightenedC2.csv", np.column_stack((StraightRNPC2[0], StraightRNPC2[1], StraightRNPC2[2])), delimiter=",", fmt='%s')
