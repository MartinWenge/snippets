# import a module to check if file exists
# import the exit stuff
import os
# import numpy
import numpy as np

# arrays of paramters, cover maximum range of them
generations = [ g for g in range(3,8,1)] # 3, ... , 7
spacers = [ s for s in range(1,9,1)] # 1, ... , 8
chainlengths = [ 1 << n for n in range(2,8,1) ] # 4, ... , 128 
densities = ['{:4.2f}'.format(d/10.0) for d in range(0,6,1)]
# check arrays: 
print("parameters: ",generations, spacers, chainlengths, densities)

# prepare filename characteristics:
fileprefix = "d_sim_"
filesuffix = "_endMonos.dat"

# prepare the output
dataContainer = []

for g in generations:
    # spacer lengths
    for s in spacers:
        # chain lenghts
        for n in chainlengths:
            # densities:
            for d in densities:
                # calculate some properties resulting from other parameters
                # the boxsize, sometimes depending on the system paramters
                boxsize = 128
                # the number of dendritic monomers in one molecule for a threefunctional dendrimer
                numOfMonos = 3 * s * (2**g - 1) + 1

                # create path like this d_sim_g5_s1_n4_b128_d0.30_endMonos.dat
                filepath = os.path.join(fileprefix+"g"+str(g)+"_s"+str(s)+"_n"+str(n)+"_b"+str(boxsize)+"_d"+d+filesuffix)
                # check if path exists and do the work
                if os.path.isfile(filepath):
                    # read in the file and sort it by my datatypes
                    all_file = np.loadtxt(filepath,dtype={'names' : ('radius', 'counts', 'distribution'),'formats' : (np.float, np.float, np.float)},comments='#', delimiter='\t')

                    # check if the file contains enough data
                    if all_file.shape[0] > 6:
                        # skip the first few entries to get rid of normalisation maxima
                        subset = all_file[4:]
                        # get the maximum value of the end monomer distribution
                        maxID = np.argmax(subset['distribution'])
                        # create the lookup with all the paramter information used later
                        maxPair = (g,s,numOfMonos,n,d,subset['radius'][maxID],subset['distribution'][maxID])
                        # show the results
                        print(filepath, maxPair)
                        # add it to the output container
                        dataContainer.append(maxPair)

# after collecting the data, write the whole stuff to the summary file
resultFilePath = os.path.join("maxOfEndMonoDistribution_sdips_sum.dat")

# check if an old file is there and remove it if neccessary
if os.path.isfile(resultFilePath):
    os.remove(resultFilePath)

np.savetxt(resultFilePath, dataContainer, delimiter = '\t', header = "G\tS\tNOfMon\tNch\tphi\trMax\tphiEndsMax\n", fmt = "%s")

print("collecting max values of monomer distribution done")
