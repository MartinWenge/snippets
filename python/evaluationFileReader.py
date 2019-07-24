# use regular expressions
import re
# use path modification tools
import os
# use numpy
import numpy as np
# use matplotlib
import matplotlib.pyplot as plt

# define re global
# re tester at https://pythex.org/
## use this for monomer density files
# dips_wallZ_g6_s1_n128_df0.75_b128_zWallMonDistr.dat
re_MonomerDensity = re.compile(r'.*_g(\d+)_s(\d+)_n(\d+)_df(\d+.\d+)_b(\d+)_.*')

class dipsMonomerDensityFileReader:
    def __init__(self, fname):
        self.basename = os.path.basename(fname)
        myMatch = re_MonomerDensity.match(self.basename)  # if no match m = None
        if myMatch is not None:
            self.generation = int(myMatch.group(1))
            self.spacer = int(myMatch.group(2))
            self.chainLength = int(myMatch.group(3))
            self.dendrimerFraction = float(myMatch.group(4))
            self.boxsize = int(myMatch.group(5))
            # calculate numbers
            self.numMonosDendr = (3 * self.spacer * (pow(2,self.generation)-1) + 1 )
            self.numEndMonosDendr = (3 * pow(2,(self.generation-1) ) )
            self.numEndMonosChain = 2
            # load file
            self.data = np.loadtxt(fname,comments='#')
            # first column is always x axis
            self.x = self.data[:,0]
        else:
            print("did not find "+fname)
            
    # print a figure using the z distribution data logics   
    def printZComponentDataTo(self, fnamePrefix = "zMonoDistrFigure"):
        if self.data.shape[1] != 5:
            print("data seems not to be a z-monomer distribution")
            return
        #plt.figure()
        zx = self.x[self.x < (self.boxsize/2-1)]
        zData =((self.data[self.x < (self.boxsize/2-1)])[:,[1,2,3,4]]+np.flip((self.data[self.x >= (self.boxsize/2)]),0)[:,[1,2,3,4]])/2.0
        if (self.numMonosDendr < self.chainLength):
            plt.plot(zx, zData[:,0]/self.numMonosDendr, 'b--', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" all mono" )
            plt.plot(zx, zData[:,1]/self.numEndMonosDendr, 'r--', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" end mono")
            plt.plot(zx, zData[:,2]/self.chainLength, 'g+', label="N"+str(self.chainLength)+" all mono")
            plt.plot(zx, zData[:,3]/self.numEndMonosChain, 'y+', label="N"+str(self.chainLength)+" end mono")
        else:
            plt.plot(zx, zData[:,2]/self.numMonosDendr, 'b--', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" all mono")
            plt.plot(zx, zData[:,3]/self.numEndMonosDendr, 'r--', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" end mono")
            plt.plot(zx, zData[:,0]/self.chainLength, 'g+', label="N"+str(self.chainLength)+" all mono")
            plt.plot(zx, zData[:,1]/self.numEndMonosChain, 'y+', label="N"+str(self.chainLength)+" end mono")
        plt.legend(loc="upper center")
        plt.xlabel('z')
        plt.ylabel('P(z)')
        plt.title('z-monomer distribution G'+str(self.generation)+"S"+str(self.spacer)+" dendrimer ("+str(self.dendrimerFraction)+") in linear chain N"+str(self.chainLength))
        
        # write out figure to file
        fname="{}_g{}_s{}_n{}_df{:.2f}_b{}".format(fnamePrefix, self.generation, self.spacer, self.chainLength, self.dendrimerFraction, self.boxsize)
        # save to png
        plt.savefig(fname+".png", dpi=180)
        # or save to pgf
        #plt.savefig(fname+".pgf")
        
    # print a figure using the radial distribution data logics    
    def printRadialDataTo(self, fnamePrefix = "radMonoDistrFigure"):
        if self.data.shape[1] != 9:
            print("data seems not to be a radial monomer distribution")
            return
        #plt.figure()
        if (self.numMonosDendr < self.chainLength):
            plt.plot(self.x, self.data[:,2]/self.numMonosDendr, 'b-', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" all mono" )
            plt.plot(self.x, self.data[:,4]/self.numEndMonosDendr, 'r-', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" end mono" )
            plt.plot(self.x, self.data[:,6]/self.chainLength, 'g+', label="N"+str(self.chainLength)+" all mono")
            plt.plot(self.x, self.data[:,8]/self.numEndMonosChain, 'y+', label="N"+str(self.chainLength)+" end mono")
            
        else:
            plt.plot(self.x, self.data[:,6]/self.numMonosDendr, 'b-', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" all mono" )
            plt.plot(self.x, self.data[:,8]/self.numEndMonosDendr, 'r-', label="G"+str(self.generation)+"S"+str(self.spacer)+"df"+str(self.dendrimerFraction)+" end mono" )
            plt.plot(self.x, self.data[:,2]/self.chainLength, 'g+', label="N"+str(self.chainLength)+" all mono")
            plt.plot(self.x, self.data[:,4]/self.numEndMonosChain, 'y+', label="N"+str(self.chainLength)+" end mono")
            
        plt.legend(loc="upper center")
        plt.xlabel('r')
        plt.ylabel('P(r)')
        plt.title('radial monomer distribution G'+str(self.generation)+"S"+str(self.spacer)+" dendrimer ("+str(self.dendrimerFraction)+") in linear chain N"+str(self.chainLength))

        # write out figure to file
        fname="{}_g{}_s{}_n{}_df{:.2f}_b{}".format(fnamePrefix, self.generation, self.spacer, self.chainLength, self.dendrimerFraction, self.boxsize)
        # save to png
        plt.savefig(fname+".png", dpi=180)
        # or save to pgf
        #plt.savefig(fname+".pgf")

#
