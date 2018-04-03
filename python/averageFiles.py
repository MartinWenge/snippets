# import a module to check if file exists
from pathlib import Path
# import the exit stuff
import sys
# import numpy
import numpy as np

dataContainer = []
for i in range(1,2):
    filename = "no"+str(i)+"/.dat"
    myfile = Path(filename)
    
    if myfile.is_file():
        all_file = np.loadtxt(filename,dtype=float,comments='#')
        dataContainer.append(all_file)
    else:
        sys.exit("file was not found")

averageData = dataContainer[0]
for i, data in enumerate(dataContainer):
    if i>0:
        averageData += data

averageData/=float(len(dataContainer))

filename = "testdata1.dat"
headerText = open(filename).readline().rstrip()

#print(headerText)
np.savetxt('testdata_average.dat', averageData, fmt='%.4e', delimiter='\t', header=str(headerText))
