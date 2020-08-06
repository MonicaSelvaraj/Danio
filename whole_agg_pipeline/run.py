'''
Runs the pipeline 
'''
#!/usr/bin/python
import sys, os

#All the input csv files for analysis should be in the file named Input 
InputPath = 'InputTimeCourse'

#For each input file, a results folder with the same name as the input file can be found in Output 
os.mkdir("Output")
os.mkdir("StraightenedAggregates_projections")

#Passing all the files in Input through the pipeline 
for filename in os.listdir(InputPath):
    if (filename == '.DS_Store'):
        continue

    #Printing out the name of the file 
    os.system('echo && echo && echo'); os.system('echo InputTimeCourse/%s' % filename); os.system('echo')

    #Creating an Output file with the same name as the input file so results have a destination 
    os.chdir('Output')
    outputFile = filename[:-4]
    os.mkdir('%s' % outputFile)
    os.chdir('..')
    
    #Splitting channels and visualizing the aggregate 
    os.system('python split_channels_tc.py InputTimeCourse/%s' % filename)
    os.system('python scatter_plot.py')

    
    #Clustering
    os.system('python clustering.py C1.csv ClusteredC1.csv')
    os.system('python clustering.py C2.csv ClusteredC2.csv')
    os.system('python clustered_plots.py')
    

    #CortexRemoval
    os.system('python cortex_removal.py')
    os.system('python scatter_plot_cortex_removed.py')

    #Orienting aggregate
    #os.system('python Orientation.py')
    
    #Straightening
    os.system('Rscript principal_curve.R')
    os.system('python straightening.py')

    #PCA and 2D plots for each RNP type
    os.system('python 2D_projections.py StraightenedC1.csv ComponentsC1.csv r Output/%s/PrincipalComponentsC1.png' % outputFile)
    os.system('python 2D_projections.py StraightenedC2.csv ComponentsC2.csv g Output/%s/PrincipalComponentsC2.png' % outputFile)

    #Removing outliers
    os.system('python outliers.py')

    #Curve Fitting
    os.system('python curve_fitting_components.py')

#Formatting the data collected
os.system('python data_formatting.py')









    
