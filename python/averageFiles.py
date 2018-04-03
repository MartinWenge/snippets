# import a module to check if file exists
#from pathlib import Path
# import the exit stuff
import os
# import numpy
import numpy as np

fileprefix = "tanglotron-8-shaped_1_M"
filesuffix = "_simRest_contacts4.dat"

momentumArray = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.25, 2.5, 2.75, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10]

for moment in momentumArray:

    dataContainer = []

    for i in range(1,10):
        filepath = os.path.join("no"+str(i),fileprefix+str(moment)+filesuffix)
        if os.path.isfile(filepath):
            all_file = np.loadtxt(filepath,dtype=float,comments='#')
            dataContainer.append(all_file)
    
    averageData = dataContainer[0]
    for i, data in enumerate(dataContainer):
        if i>0:
            averageData += data
    averageData/=float(len(dataContainer))

    resultfilename = "average/"+fileprefix+str(moment)+filesuffix
    headerText = open("no1/data_N256_lang.dat").readline().rstrip()

    someFilename = os.path.join("no1",fileprefix+"0"+filesuffix)
    headerText = ""
    with open(someFilename, "r") as fi:
        for ln in fi:
            if ln.startswith("#"):
                headerText = headerText + ln

    np.savetxt(resultfilename, averageData, fmt='%d %.6f', delimiter='\t', header=str(headerText))

