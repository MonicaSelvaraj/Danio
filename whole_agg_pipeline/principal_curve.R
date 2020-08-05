#Importing data to R
pointsC1 <- read.csv("CortexRemovedC1.csv")
pointsC2 <- read.csv("CortexRemovedC2.csv")

#Renaming columns 
colnames(pointsC1) <- c("x","y","z")
colnames(pointsC2) <- c("x","y","z")

#Concatenating both dataframes 
allpoints <- rbind(pointsC1, pointsC2)

#Converting the dataframe to a matrix 
allpoints <- data.matrix(allpoints)

#Fitting the first principal curve 
library(princurve)
fit <-(principal_curve(allpoints))

#Obtaining fitted points on the curve and ordering of points
fits <- fit$s
fitord <- fit$ord

#Exporting to csv files 
write.table(fits, "fitpoints.csv", sep = ",", row.names = F, col.names = F)
write.table(fitord, "fitorder.csv", sep = ",", row.names = F, col.names = F)


