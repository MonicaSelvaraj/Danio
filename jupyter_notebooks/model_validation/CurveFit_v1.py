'''
Usage: Fit curves in 2D first
Combining the 2D fits to get a 3D fit
'''

import sys
import math
import numpy as np
import common_funcs
from scipy.optimize import curve_fit 

'''
Defining input functions to scipy.optimize.curvefit
'''
def helixFitCos(pc1, r, pitch, phase):
    return r*np.cos(pc1*((2*np.pi)/pitch) + phase)
def helixFitSin(pc1, r, pitch, phase):
    return r*np.sin(pc1*((2*np.pi)/pitch) + phase)
'''
Given x, predict the best y 
'''
def fitFunction(x, y, function):
    try:
        popt, pcov = curve_fit(function, x, y, bounds=(0, [30, 30, 2*math.pi]))
    except RuntimeError:
        sys.exit(1)
    else:
        radius = popt[0]; pitch = popt[1]; phase = popt[2]
        StandardErr = np.sqrt(np.diag(pcov))
        return(radius, pitch, phase, StandardErr[0], StandardErr[1], StandardErr[2])
'''
Comparing sin and cos fits
'''
def BestFit(x,y):
        CosFit = fitFunction(x, y, helixFitCos)
        SinFit = fitFunction(x, y, helixFitSin)
        StdErrSumCos = CosFit[3] + CosFit[4] + CosFit[5]
        StdErrSumSin = SinFit[3] + SinFit[4] + SinFit[5]
        if(StdErrSumCos < StdErrSumSin):
                yOpt = [helixFitCos(c1, CosFit[0], CosFit[1], CosFit[2]) for c1 in x]
                return (CosFit[0],CosFit[1],CosFit[2],CosFit[3],CosFit[4],CosFit[5],yOpt)
        else:
                yOpt = [helixFitSin(c1, SinFit[0], SinFit[1], SinFit[2]) for c1 in x]
                return (SinFit[0],SinFit[1],SinFit[2],SinFit[3],SinFit[4],SinFit[5],yOpt)
        
#Get input     
c1,c2,c3 = common_funcs.getPoints("projections.csv")
c1 = np.array(c1, dtype = float); c2 = np.array(c2, dtype = float); c3 = np.array(c3, dtype = float)
#Fit
r2,pi2,ph2,rse2,pise2,phse2,fitc2 = BestFit(c1, c2) # Predicts C2 given C1
r3,pi3,ph3,rse3,pise3,phse3,fitc3 = BestFit(c1, c3)  # Predicts C3 given C1
#Store params
fitParams = [r2,pi2,ph2,rse2,pise2,phse2,r3,pi3,ph3,rse3,pise3,phse3]

#Write fit coordinates to file
np.savetxt("fit.csv", np.column_stack((c1, np.array(fitc2, dtype=float), np.array(fitc3, dtype=float))), delimiter=",", fmt='%s')
#Write params to file
common_funcs.appendToCsv("params.csv", fitParams)
sys.exit(0)