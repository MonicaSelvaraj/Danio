'''
- Plots of C1s, C2s, C3s before outliers are removed
- Plots components with lines
- Remove outliers for each channel individually
- Plots of C1s, C2s, and C3s after outliers have been removed, with lines to indicate boundaries
of removal
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

f_read = open("FileNames.txt", "r")
last_line = f_read.readlines()[-1]
last_line = last_line[:-1] #Ignoring newline character
f_read.close()

print("Removing Outliers")

plt.style.use('dark_background')

#Original data 
C1r = list(); C2r = list(); C3r = list()#C1 - red
C1g = list(); C2g = list(); C3g = list()#C2 - green

#Reading in the data 
with open ('ComponentsC1.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    for line in csv_reader:
            C1r.append(line[0])
            C2r.append(line[1])
            C3r.append(line[2])
            
with open ('ComponentsC2.csv', 'r') as csv_file:
    csv_reader = csv.reader (csv_file)
    for line in csv_reader:
            C1g.append(line[0])
            C2g.append(line[1])
            C3g.append(line[2])
        
       
C1r = numpy.array(C1r); C2r = numpy.array(C2r); C3r = numpy.array(C3r)
C1g = numpy.array(C1g); C2g = numpy.array(C2g); C3g = numpy.array(C3g)
C1r = C1r.astype(float); C2r= C2r.astype(float); C3r = C3r.astype(float)
C1g = C1g.astype(float); C2g= C2g.astype(float); C3g = C3g.astype(float)       

#Shows plots before removing outliers
plt.scatter(C2g, C3g, c='g'); plt.scatter(C2r, C3r, c='r'); plt.title('C2 vs C3');  plt.ylim(-20, 20); plt.xlim(-20,20);  plt.savefig('Output/%s/C2C3WithOutliers.png' % last_line); #plt.show();
plt.close() # Shows plot without first PC
plt.scatter(C1g, C2g, c='g'); plt.scatter(C1r, C2r, c='r'); plt.title('C1 vs C2');  plt.ylim(-20, 20); plt.xlim(-20,20);plt.savefig('Output/%s/C1C2WithOutliers.png' % last_line); #plt.show()
plt.close() # Shows plot without third PC
plt.scatter(C1g, C3g, c='g'); plt.scatter(C1r, C3r, c='r'); plt.title(' C1 vs C3');  plt.ylim(-20, 20); plt.xlim(-20,20);plt.savefig('Output/%s/C1C3WithOutliers.png' % last_line);#plt.show();
plt.close()# Shows plot without second PC

#REMOVING OUTLIERS
def removeOutliers(C1, C2, C3, sd):
        dst = list()
        #Finding distances of points from (0,0)
        for x,y in zip (C2, C3):
                a = (x,y)
                b = (0,0)
                dst.append(distance.euclidean(a,b))

        dst = numpy.array(dst); dst = dst.astype(float)
        
        #Plotting the distances from the origin to check the distribution
        #plt.hist(dst) #Auto binned histogram
        #plt.show()
 
        meanDst = numpy.mean(dst, axis = 0); #print (meanDst)
        sdDst = numpy.std(dst, axis = 0); #print (sdDst)

        #outliersIndex contains the positions of the outliers
        outliersIndex = numpy.where(dst > meanDst + sd * sdDst)
        lineDst = meanDst + sd * sdDst
        #print (outliersIndex)
        #Removing the outliers from C1, C2, C3
        newC1 = numpy.delete (C1, outliersIndex)
        newC2 = numpy.delete (C2, outliersIndex)
        newC3 = numpy.delete (C3, outliersIndex)
        return (newC1, newC2, newC3, lineDst);

CleanedChannel1 = removeOutliers (C1r, C2r, C3r,2)
lineC1 = CleanedChannel1[3]
#print (lineC1)
CleanedChannel2 = removeOutliers (C1g, C2g, C3g, 2)
lineC2 = CleanedChannel2[3]
#print (lineC2)

#Writing cleaned data to a new file
numpy.savetxt("CleanedComponentsC1.csv", numpy.column_stack((CleanedChannel1[0], CleanedChannel1[1], CleanedChannel1[2])), delimiter=",", fmt='%s')
numpy.savetxt("CleanedComponentsC2.csv", numpy.column_stack((CleanedChannel2[0], CleanedChannel2[1], CleanedChannel2[2])), delimiter=",", fmt='%s')

#Saving cleaned components to StraightenedAggregates_projections file for moving window analysis
numpy.savetxt("StraightenedAggregates_projections/%s_CleanedComponentsC1.csv" % last_line, numpy.column_stack((CleanedChannel1[0], CleanedChannel1[1], CleanedChannel1[2])), delimiter=",", fmt='%s')
numpy.savetxt("StraightenedAggregates_projections/%s_CleanedComponentsC2.csv" % last_line, numpy.column_stack((CleanedChannel2[0], CleanedChannel2[1], CleanedChannel2[2])), delimiter=",", fmt='%s')

#Shows plots with outliers and lines
plt.scatter(C2g, C3g, c='g'); plt.scatter(C2r, C3r, c='r'); plt.title('C2 vs C3'); plt.ylim(-20, 20); plt.xlim(-20,20)
plt.axvline(x=lineC1, c='r'); plt.axvline(x=-lineC1, c='r'); plt.axhline(y=lineC1, c='r'); plt.axhline(y=-lineC1, c='r') #C1 lines
plt.axvline(x=lineC2, c='g'); plt.axvline(x=-lineC2, c='g'); plt.axhline(y=lineC2, c='g'); plt.axhline(y=-lineC2, c='g') #C2 lines
plt.savefig('Output/%s/C2C3OutliersBoundary.png' % last_line)# Shows plot without first PC
#plt.show()
plt.close()

plt.scatter(C1g, C2g, c='g'); plt.scatter(C1r, C2r, c='r'); plt.title('C1 vs C2');  plt.ylim(-20, 20); plt.xlim(-20,20)
plt.axhline(y=lineC1, c='r'); plt.axhline(y=-lineC1, c='r') #C1 lines
plt.axhline(y=lineC2, c='g'); plt.axhline(y=-lineC2, c='g') #C2 lines
plt.savefig('Output/%s/C1C2OutliersBoundary.png' % last_line) # Shows plot without third PC
#plt.show()
plt.close()

plt.scatter(C1g, C3g, c='g'); plt.scatter(C1r, C3r, c='r'); plt.title(' C1 vs C3');  plt.ylim(-20, 20); plt.xlim(-20,20)
plt.axhline(y=lineC1, c='r'); plt.axhline(y=-lineC1, c='r') #C1 lines
plt.axhline(y=lineC2, c='g'); plt.axhline(y=-lineC2, c='g') #C2 lines
plt.savefig('Output/%s/C1C3OutliersBoundary.png' % last_line)# Shows plot without second PC
#plt.show()
plt.close()

#Shows plots after removing outliers
plt.scatter(CleanedChannel2[2], CleanedChannel2[1], c='g'); plt.scatter(CleanedChannel1[2],CleanedChannel1[1],c='r');plt.title('C2 vs C3'); plt.ylim(-20, 20); plt.xlim(-20,20); plt.savefig('Output/%s/C2C3WithoutOutliers.png' % last_line);#plt.show();
plt.close() # Shows plot without first PC
plt.scatter(CleanedChannel2[0], CleanedChannel2[1], c='g'); plt.scatter(CleanedChannel1[0], CleanedChannel1[1], c='r'); plt.title('C1 vs C2'); plt.ylim(-20, 20); plt.xlim(-20,20); plt.savefig('Output/%s/C1C2WithoutOutliers.png' % last_line);#plt.show();
plt.close() # Shows plot without third PC
plt.scatter(CleanedChannel2[0], CleanedChannel2[2], c='g');plt.scatter(CleanedChannel1[0], CleanedChannel1[2],  c='r'); plt.title(' C1 vs C3'); plt.ylim(-20, 20); plt.xlim(-20,20); plt.savefig('Output/%s/C1C3WithoutOutliers.png' % last_line);#plt.show();
plt.close()# Shows plot without second PC




