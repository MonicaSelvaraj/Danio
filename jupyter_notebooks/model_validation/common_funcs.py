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

'''
usage: To create a dictionary with keys from population.txt and values from threshold.txt

params: none

returns: dictionary with population names as keys and 
outlier removal thresholds as values.
'''
def outlierThresholdsDict():
    keys = list(); values = list()
    a = open('population.txt','r')
    for line in a: keys.append(line.strip())
    b = open('threshold.txt', 'r')
    for line in b: values.append(line.strip())
    return dict(zip(keys, values))

'''
usage: To read the params file and store each param in a separate array.

args: filename - file with params

returns: params in individual arrays
'''
def getParams(filename):
    r2 = list(); pi2 = list(); ph2 = list(); rse2 = list(); pise2 = list(); phse2 = list()
    r3 = list(); pi3 = list(); ph3 = list(); rse3 = list(); pise3 = list(); phse3 = list()
    with open (filename, 'r') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
            r2.append(line[0]); pi2.append(line[1]); ph2.append(line[2])
            rse2.append(line[3]); pise2.append(line[4]); phse2.append(line[5])
            r3.append(line[6]); pi3.append(line[7]); ph3.append(line[8])
            rse3.append(line[9]); pise3.append(line[10]); phse3.append(line[11])
    r2 = np.array(r2, dtype = float); pi2 = np.array(pi2, dtype = float); ph2 = np.array(ph2, dtype = float)
    rse2 = np.array(rse2, dtype = float); pise2 = np.array(pise2, dtype = float); phse2 = np.array(phse2, dtype = float)
    r3 = np.array(r3, dtype = float); pi3 = np.array(pi3, dtype = float); ph3 = np.array(ph3, dtype = float)
    rse3 = np.array(rse3, dtype = float); pise3 = np.array(pise3, dtype = float); phse3 = np.array(phse3, dtype = float)
    return (r2, pi2, ph2, rse2, pise2, phse2, r3, pi3, ph3, rse3, pise3, phse3)
