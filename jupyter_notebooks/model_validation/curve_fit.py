'''
This script performs curve fitting on the 2D projections of aggregates and combines the 2D fits to produce a 3D fit. 

There are two modes to this script. If the first argument is 1, the script is used to estimate outlier thresholds for populations. 
If the first argument is 2, the script is used to estimate the 95% CI. 

args: 1 - mode, 2 - pop
'''

import sys
import math
import numpy as np
import common_funcs
from scipy.optimize import curve_fit 

'''
usage: defines cos input function to scipy.optimize.curvefit.
'''
def helixFitCos(pc1, r, pitch, phase):
    return r*np.cos(pc1*((2*np.pi)/pitch) + phase)

'''
usage: defines sin input function to scipy.optimize.curvefit.
'''
def helixFitSin(pc1, r, pitch, phase):
    return r*np.sin(pc1*((2*np.pi)/pitch) + phase)

'''
usage: predicts the best y, given x.
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
usage: compares sin and cos fits and picks one
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
        
#Read input     
c1,c2,c3 = common_funcs.getPoints("projections.csv")
#Predict c2 given c1
r2,pi2,ph2,rse2,pise2,phse2,fitc2 = BestFit(c1, c2) 
#Predict c3 given c1
r3,pi3,ph3,rse3,pise3,phse3,fitc3 = BestFit(c1, c3)  # Predicts C3 
#Compile params into one array
fitParams = [r2,pi2,ph2,rse2,pise2,phse2,r3,pi3,ph3,rse3,pise3,phse3]
#Write fit coordinates to file
np.savetxt("fit.csv", np.column_stack((c1, np.array(fitc2, dtype=float), np.array(fitc3, dtype=float))), delimiter=",", fmt='%s')

#Mode for outlier threshold detection
if(sys.argv[1] == 1): 
    #Append params to params.csv
    common_funcs.appendToCsv("params.csv", fitParams)

#Mode to estimate 95% CI
if(sys.argv[1] == 2):
    #Append params only after checking that it's not an outlier 
    pop = sys.argv[2] 
    out_thresh_dict = common_funcs.outlierThresholdsDict()
    threshold = float(out_thresh_dict[pop])
    rse = float((rse2 + rse3)/2)
    if(rse <= threshold):
        common_funcs.appendToCsv("params.csv", fitParams)
    else:
        #Write outlier coordinates to outliers.csv
        with open('outliers.csv','ab') as f:
            np.savetxt(f, np.column_stack((c1, c2, c3)), delimiter=",", fmt='%s')
        sys.exit(1)

#Indicate success of curve fitting and not an outlier
sys.exit(0)