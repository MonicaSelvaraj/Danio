'''
This script contains commonly used functions.
'''

import csv
from csv import writer
import numpy as np

'''
usage: To read a file with x,y,z coordinates and store the data for each dimension in a separate array.

params: filename - file with x,y,z cooridnates

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
usage: To append a line of text to the end of a file

params: filename - file to append to, line - text to append

returns: none
'''
def appendToCsv(filename, line):
    # Open file in append mode
    with open(filename, 'a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(line)





