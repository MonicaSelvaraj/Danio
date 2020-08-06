'''
This script reads in the csv file with coorindates of all channels, and saves the data
of each of the channels as individual files, after removing particles with radius less than 0.28
Extra:
Writes out the filename into FileNames.txt
'''
#!/usr/bin/python
import sys, os
import numpy 
import csv

print("Splitting Channels")

#Variables to store Channel 1 data
x1 = list(); y1 = list(); z1 = list(); s1 = list()
#Variables to store Channel 2 data 
x2 = list(); y2 =  list(); z2 = list(); s2 = list()

#opening the csv file
# 'r' specifies that we want to read this file
#csv_reader is the name of the reader object that we have created 
with open (sys.argv[1], 'r') as csv_file:
    filename = sys.argv[1][6:]
    csv_reader = csv.reader (csv_file)
    #Iterating through contents in the file
    for line in csv_reader:
        #Removing points with radius less than 0.27
        if float(line[6]) > 0.28:
            if line[2] == 'vasa':
                x1.append(line[3]); y1.append(line[4]); z1.append(line[5]); s1.append(line[6])
            else:
                x2.append(line[3]); y2.append(line[4]); z2.append(line[5]); s2.append(line[6])
        
x1 = numpy.array(x1, dtype=float); y1 = numpy.array(y1, dtype=float); z1 = numpy.array(z1, dtype=float); s1 = numpy.array(s1, dtype=float)
x2 = numpy.array(x2, dtype=float); y2 = numpy.array(y2, dtype=float); z2 = numpy.array(z2, dtype=float); s2 = numpy.array(s2, dtype=float)

#Saving each channel's data in new files
numpy.savetxt("C1.csv", numpy.column_stack((x1, y1, z1, s1)), delimiter=",", fmt='%s')
numpy.savetxt("C2.csv", numpy.column_stack((x2, y2, z2, s2)), delimiter=",", fmt='%s')

#Writing out the filename 
with open("FileNames.txt", "a") as text_file:
    filename = filename[:-4]
    text_file.write( filename + "\n")
