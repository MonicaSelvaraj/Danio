import numpy
import csv

print('Formatting Data')

fn = list(); mcd = list();sdcd = list()
r = list();pi = list(); ph=list(); rse = list(); pise = list();phse = list()
#Channel 1 
C1C1C2r = list(); C1C1C2pi = list(); C1C1C2ph = list(); C1C1C2rse = list(); C1C1C2pise = list(); C1C1C2phse = list()
C1C1C3r = list(); C1C1C3pi= list(); C1C1C3ph = list(); C1C1C3rse = list(); C1C1C3pise = list(); C1C1C3phse = list()
#Channel 2
C2C1C2r = list(); C2C1C2pi= list(); C2C1C2ph = list(); C2C1C2rse = list(); C2C1C2pise = list(); C2C1C2phse = list()
C2C1C3r = list(); C2C1C3pi = list(); C2C1C3ph = list(); C2C1C3rse = list(); C2C1C3pise = list(); C2C1C3phse = list()


a = open('FileNames.txt','r')
for line in a:
    fn.append(line.strip())

b = open('MeanCortexDensity.txt','r')
for line in b:
    mcd.append(line.strip())
    
c = open('sdCortexDensity.txt','r')
for line in c:
    sdcd.append(line.strip())

d = open('FitRadius.txt','r')
for line in d:
    r.append(line.strip())

e = open('FitPitch.txt','r')
for line in e:
    pi.append(line.strip())

g = open('FitPhase.txt','r')
for line in g:
    ph.append(line.strip())

h = open('FitRadiusSE.txt','r')
for line in h:
    rse.append(line.strip())

i = open('FitPitchSE.txt','r')
for line in i:
    pise.append(line.strip())

j = open('FitPhaseSE.txt','r')
for line in j:
    phse.append(line.strip())


for i in range(0,len(r),4):
    C1C1C2r.append(r[i])
for i in range(1,len(r),4):
    C1C1C3r.append(r[i])
for i in range(2,len(r),4):
    C2C1C2r.append(r[i])
for i in range(3,len(r),4):
    C2C1C3r.append(r[i])

for i in range(0,len(pi),4):
    C1C1C2pi.append(pi[i])
for i in range(1,len(pi),4):
    C1C1C3pi.append(pi[i])
for i in range(2,len(pi),4):
    C2C1C2pi.append(pi[i])
for i in range(3,len(pi),4):
    C2C1C3pi.append(pi[i])

for i in range(0,len(ph),4):
    C1C1C2ph.append(ph[i])
for i in range(1,len(ph),4):
    C1C1C3ph.append(ph[i])
for i in range(2,len(ph),4):
    C2C1C2ph.append(ph[i])
for i in range(3,len(ph),4):
    C2C1C3ph.append(ph[i])

for i in range(0,len(rse),4):
    C1C1C2rse.append(rse[i])
for i in range(1,len(rse),4):
    C1C1C3rse.append(rse[i])
for i in range(2,len(rse),4):
    C2C1C2rse.append(rse[i])
for i in range(3,len(rse),4):
    C2C1C3rse.append(rse[i])

for i in range(0,len(pise),4):
    C1C1C2pise.append(pise[i])
for i in range(1,len(pise),4):
    C1C1C3pise.append(pise[i])
for i in range(2,len(pise),4):
    C2C1C2pise.append(pise[i])
for i in range(3,len(pise),4):
    C2C1C3pise.append(pise[i])

for i in range(0,len(phse),4):
    C1C1C2phse.append(phse[i])
for i in range(1,len(phse),4):
    C1C1C3phse.append(phse[i])
for i in range(2,len(phse),4):
    C2C1C2phse.append(phse[i])
for i in range(3,len(phse),4):
    C2C1C3phse.append(phse[i])



fn = numpy.array(fn); mcd = numpy.array(mcd); sdcd = numpy.array(sdcd)
C1C1C2r = numpy.array(C1C1C2r)
C1C1C2pi = numpy.array(C1C1C2pi)
C1C1C2ph = numpy.array(C1C1C2ph)
C1C1C2rse = numpy.array(C1C1C2rse)
C1C1C2pise = numpy.array(C1C1C2pise)
C1C1C2phse = numpy.array( C1C1C2phse)
C1C1C3r = numpy.array(C1C1C3r)
C1C1C3pi = numpy.array(C1C1C3pi)
C1C1C3ph = numpy.array(C1C1C3ph)
C1C1C3rse = numpy.array(C1C1C3rse)
C1C1C3pise = numpy.array(C1C1C3pise)
C1C1C3phse = numpy.array(C1C1C3phse)
    
C2C1C2r = numpy.array(C2C1C2r)
C2C1C2pi = numpy.array(C2C1C2pi)
C2C1C2ph = numpy.array(C2C1C2ph)
C2C1C2rse = numpy.array(C2C1C2rse)
C2C1C2pise = numpy.array(C2C1C2pise)
C2C1C2phse = numpy.array( C2C1C2phse)
C2C1C3r = numpy.array(C2C1C3r)
C2C1C3pi = numpy.array(C2C1C3pi)
C2C1C3ph = numpy.array(C2C1C3ph)
C2C1C3rse = numpy.array(C2C1C3rse)
C2C1C3pise = numpy.array(C2C1C3pise)
C2C1C3phse = numpy.array(C2C1C3phse)




numpy.savetxt('Results.csv', numpy.column_stack((fn, mcd, sdcd,C1C1C2r,C1C1C2pi,C1C1C2ph,
                                                 C1C1C2rse , C1C1C2pise, C1C1C2phse, C1C1C3r, C1C1C3pi, C1C1C3ph,
                                                 C1C1C3rse, C1C1C3pise,C1C1C3phse,C2C1C2r,C2C1C2pi,C2C1C2ph,
                                                 C2C1C2rse, C2C1C2pise, C2C1C2phse, C2C1C3r, C2C1C3pi, C2C1C3ph,
                                                 C2C1C3rse,C2C1C3pise,C2C1C3phse)), delimiter=",", fmt='%s')

'''
#Re-writing file with the header line appended
with open('Results.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('Results.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['FileName', 'MeanCortexDensity', 'SDcortexdensity', 'C1C1C2r', 'C1C1C2pi', 'C1C1C2ph', 'C1C1C2rse', 'C1C1C2pise', 'C1C1C2phse', 'C1C1C3r', 'C1C1C3pi', 'C1C1C3ph', 'C1C1C3rse', 'C1C1C3pise', 'C1C1C3phse', 'C2C1C2r', 'C2C1C2pi', 'C2C1C2ph', 'C2C1C2rse', 'C2C1C2pise', 'C2C1C2phse', 'C2C1C3r', 'C2C1C3pi', 'C2C1C3ph', 'C2C1C3rse', 'C2C1C3pise', 'C2C1C3phse'])
    w.writerows(data)
'''
