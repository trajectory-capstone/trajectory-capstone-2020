import numpy
import math
import os

# List of Constants
metricTypes = ["sample_anonymity","sample_distortion","sample_entropy"]
userStart = 1
userEnd = 10
timeStart = 1
timeEnd = 24
totalRegions= 21
regionStart = 1
regionEnd = 21
timeWindow = 24
noiseLevel = 0
appParameter = 0.3

def runScript(lppm1, lppm2, lppm3):
    cmd = "sh master.sh > logs/autoLogging_"+str(round(lppm1,2))+"_"+str(round(lppm2,2))+"_"+str(round(lppm3,2))
    os.system(cmd)
    print("RAN SCRIPTS SUCCESSFULLY FOR: "+str(round(lppm1,2))+"_"+str(round(lppm2,2))+"_"+str(round(lppm3,2)))

def writeExp(expList,expType):
    filename = metricTypes[expType-1]
    with open(filename, 'w') as file:
        for exp in expList:
            file.writelines(exp + "\n")

for lppm1 in range(0,math.ceil(math.log2(regionEnd-regionStart+1))):
    for lppm2 in numpy.arange(0, 1.1, 0.1):
        for lppm3 in numpy.arange(0, 1.1, 0.1):
            for expType in range(1,4):
                expList = []
                for sampling in range(10, 101, 10):
                    expName = "file_"+str(totalRegions)+"_"+str(timeWindow)+"_"+str(noiseLevel)+"_["+str(round(lppm1))+"]_["+str(round(lppm2,2))+"]_["+str(round(lppm3,2))\
                        +"] "+str(sampling)+" "+str(userStart)+" "+str(userEnd)+" "+str(expType)+" output_"+str(sampling)+" "+str(timeStart)+" "+str(timeEnd)\
                        +" "+str(regionStart)+" "+str(regionEnd)+" "+str(round(lppm1,2))+" "+str(round(lppm2,2))+" "+str(round(lppm3,2))\
                        +" "+str(appParameter)+" actual.trace knowledge_"+str(sampling)
                    print(expName)
                    expList.append(expName)
                writeExp(expList, expType)
            runScript(lppm1, lppm2, lppm3)