'''
Separating input tsv file into individual csv files based on codename
'''
#!/usr/bin/python
import sys
from os import listdir
import numpy 
import csv

print("Parsing tsv file")

#Making a list of samples in the file
samples = list()
with open('dazl_vasa_tc_all.tsv','r') as tsvIn:
    reader = csv.reader(tsvIn, delimiter='\t')
    for row in reader:
        if(row[1] not in samples):
            samples.append(row[1])
samples.remove('codename')
print(samples)

for sample in samples:
    with open('dazl_vasa_tc_all.tsv','r') as tsvIn, open('Input/' + sample+ '.csv', 'w') as csvOut:
        reader = csv.reader(tsvIn, delimiter='\t')
        writer = csv.writer(csvOut, delimiter=',')
        [writer.writerow(row) for row in reader if  sample in row]
