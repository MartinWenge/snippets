
# file reader for bfm files
import sys  
import os
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():
    # set filename and check if file exists
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    # read in the xyz file 
    coordinates = np.genfromtxt(filepath, delimiter="\t", comments="#")[:,:-1]
    # compute the convex hull and the area
    hull = ConvexHull(coordinates)
    print(hull.area)
    
    # create the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot defining corner points
    ax.plot(coordinates.T[0], coordinates.T[1], coordinates.T[2], "ko")

    # 12 = 2 * 6 faces are the simplices (2 simplices per square face)
    for s in hull.simplices:
        s = np.append(s, s[0])  # Here we cycle back to the first coordinate
        ax.plot(coordinates[s, 0], coordinates[s, 1], coordinates[s, 2], "r-")

    #plt.show()

    # create the output
    fig.savefig('convexHullPlot.png')
    np.savetxt("area.dat",np.array([hull.area]))

if __name__ == '__main__':
    main()
