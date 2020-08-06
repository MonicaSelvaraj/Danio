#!/usr/bin/python
import csv
import numpy as np
import matplotlib.pyplot as plt

numBoot = 10000; ##SET

plt.style.use('dark_background')

def getParams(filename):
    r = list(); pi = list(); ph = list(); rse = list(); pise = list(); phse = list()
    with open (filename, 'r') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
            r.append(line[0]); pi.append(line[1]); ph.append(line[2])
            rse.append(line[3]); pise.append(line[4]); phse.append(line[5])
    r = np.array(r, dtype = float)
    pi = np.array(pi, dtype = float)
    ph = np.array(ph, dtype = float)
    rse = np.array(rse, dtype = float)
    pise = np.array(pise, dtype = float)
    phse = np.array(phse, dtype = float)
    return (r, pi, ph, rse, pise, phse)

r,pi,ph,rse,pise,phse = getParams("params.csv")
y = list(range(1,numBoot+1)) 

#plots
plt.scatter(r, y, c='b',s=1); plt.title('Radius'); plt.xlim(2, 8); plt.savefig("Radius"); plt.close()
plt.scatter(rse, y, c='g',s=1); plt.title('Radius standard error'); plt.savefig("Radius standard error"); plt.close()

plt.scatter(pi, y, c='b',s=1); plt.title('Pitch'); plt.xlim(11, 17); plt.savefig("Pitch"); plt.close()

plt.scatter(pise, y, c='g',s=1); plt.title('Pitch standard error'); plt.savefig("Pitch standard error"); plt.close()

plt.scatter(ph, y, c='b',s=1); plt.title('Phase'); plt.savefig("Phase"); plt.close()
plt.scatter(phse, y, c='g',s=1); plt.title('Phase standard error'); plt.savefig("Phase standard error");  plt.close()

