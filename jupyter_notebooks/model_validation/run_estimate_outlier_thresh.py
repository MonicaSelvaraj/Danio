'''
This script estimates outlier thresholds for all populations with varying spatial errors.
Sample command: 
python estimate_outlier_thresh.py numPoints, radius, pitch, percentError, numBoot, numSamples population_name
'''

import os

#Delete threshold.txt and population.txt if they exist from the previous run
if os.path.exists("threshold.txt"): os.remove('threshold.txt')
if os.path.exists("population.txt"): os.remove('population.txt')    
    
os.system('python estimate_outlier_thresh.py 1000 3 14 5 5000 250 pop1_5')
os.system('python estimate_outlier_thresh.py 1000 3 14 10 5000 250 pop1_10')
os.system('python estimate_outlier_thresh.py 1000 3 14 15 5000 250 pop1_15')
os.system('python estimate_outlier_thresh.py 1000 3 14 20 5000 250 pop1_20')

