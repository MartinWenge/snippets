# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:20:15 2016

@author: wengenmayr

@brief: calculates the potential of mean force from a bunch of histogram files
"""

# ###################  Command line parsing starts here ###################### #
#import the command line parsing module
import argparse as ap

# defining some standart values
# find filename
G='5'
S='1'
B='64'
K='0.5'
r_start=1
r_end=32
delta_r=1

binSize=0.5

# prepare the command line parsing
parser = ap.ArgumentParser()
parser.add_argument("-g", "--generation",  help="set the dendrimers generation (default: 5)")
parser.add_argument("-s", "--spacerlength",  help="set the dendrimers spacer length (default: 1)")
parser.add_argument("-b", "--box",  help="set the box size (default: 64)")
parser.add_argument("-k", "--springconstant",  help="set the spring constant (using prefactor 1/2 internally) (default: 0.2)")
parser.add_argument("-0", "--r_start",  help="start value of com distance (default:1)")
parser.add_argument("-1", "--r_end",  help="end value of com distance (default: 32)")
parser.add_argument("-D", "--delta_r",  help="difference in com distance (default: 1)")


args=parser.parse_args()

if args.generation is not None:
    G=args.generation
    print("generation set to "+G)
if args.spacerlength is not None:
    S=args.spacerlength
    print("spacerlength set to "+S)
if args.box is not None:
    B=args.box
    print("box size set to "+B)
if args.springconstant is not None:
    K=args.springconstant
    print("spring constant set to "+K)
if args.r_start is not None:
    r_start=int(args.r_start)
    print("r_start set to "+str(r_start))
if args.r_end is not None:
    r_end=int(args.r_end)
    print("r_end set to "+str(r_end))
if args.delta_r is not None:
    delta_r=int(args.delta_r)
    print("delta_r set to "+str(delta_r))

prefilename='dpath_g'+G+'_s'+S+'_b'+B+'_k'+K
endfilename='_com_dist_histogram.dat'

# "twodath_g"$i"_s"$j"_b"$boxsize"_k"${n}"_r"${m}"_com_dist_histogram.dat"

# ###################  Command line parsing complete ###################### #

# import the numpy module
import numpy as np
# import a module to check if file exists
from pathlib import Path
#import the plot module
import matplotlib.pyplot as plt


# read in files
data_fields=[]
# map (dict in phyton) of all data in r_0 y1 y2 y3 ... format
map_of_data = dict()
# collect occuring r_0 values
r_0_field=[]
# spring constant
spring_const=0.5*float(K)

############  change things: ############
# read in files using range for the different r0 values
for dist in range(r_start,r_end,delta_r):
    filename=(prefilename+'_r{:}'+endfilename).format(dist)
    myfile=Path(filename)
    if myfile.is_file():
        print(filename)
        all_file = np.loadtxt(filename,dtype=float,comments='#')
        data_fields.append(all_file[:,[0,1]])
        r_0_field.append(dist)
    else:
        message= 'file ' + filename + ' does not exist'
        print(message)

print('read in files finished\n\tarray of r_0:')
print('\t',len(r_0_field),r_0_field)

#sorting stuff in a dictionary
l = len(data_fields)
#print(l)
for i, data in enumerate(data_fields):
    for row in data:
        #field = d.get(row[0], np.zeros(l))
        field = map_of_data.setdefault(row[0], np.zeros(l))
        field[i] = row[1]
        #d[row[0]] = field
            
#print('read in files finished')

# fill an array with the dict entries
array1 = np.zeros((l+1,len(map_of_data)))
for i, dict_entry in enumerate(map_of_data.items()):
    array1[0,i]=dict_entry[0]
    array1[1:,i]=dict_entry[1]

# sort the array by first column
array2=np.transpose(array1)
array3=np.transpose(array2[array2[:,0].argsort()])

##plot the whole stuff:
x=array3[0,:]
y=array3[1:,:]

#plt.figure()
#for i, column in enumerate(array3):
#    if i>0:
#        plt.plot(x, column,"-",label="%s"%str(r_0_field[i-1]))
#
#plt.xlabel("c2c distance")
#plt.ylabel("frequency")
#plt.legend()
#plt.show()

# apply the wham
# count the number of simulation windows
n_sim=np.array(y.sum(axis=1))
print("number of windows per simulation:")
print('\t',n_sim)

# create the bias potential ( ######## geht das kürzer? ###### )
U_bias = np.zeros((len(r_0_field),len(x)),np.float128)
for i, r_0 in enumerate(r_0_field):
    U_bias[i,:] = spring_const * np.square(x-(r_0*np.ones(len(x))))
    
#get the exp(-w_j(\chi)): array with size shape(len(r_0_field),len(x))
exp_U_bias=np.exp(-U_bias)

#plt.figure()
#for i, column in enumerate(exp_U_bias):
#    if i>0:
#        plt.plot(x, column,"o",label="%s"%str(r_0_field[i-1]))
#
#plt.xlabel("c2c distance")
#plt.ylabel("bias potential")
#plt.legend()
#plt.show()

#get the sum of all counts at a spcific value of \chi: array with len=len(x)
#########   ADDED SOME 4*Pi*R^2*dR TO THE COUNTS TO ENCOUNTER FOR CORRECT VOLUME ELEMENT ########### 
#rho_i=y[:None]/(4*np.pi*x*x*binSize)
rho_i=y[:None]/((4*np.pi/3)*(3*x*x*binSize+3*x*binSize*binSize+binSize*binSize*binSize*np.ones(len(x))))

#plt.figure()
#for i, column in enumerate(rho_i):
#    plt.plot(x,column,"-",label="%s"%str(r_0_field[i]))
#plt.xlabel("c2c distance")
#plt.ylabel("H(r)/V=rho(r)")
#plt.legend()
#plt.show()

#first guess of free energy constants: array with len(r_0_field)
minus_exp_F=np.ones(y.shape[0],np.float128)
minus_exp_F_old=np.ones(y.shape[0],np.float128)
integrand_F_i=np.zeros((len(r_0_field),len(x)))

#do the loop
for ncycles in range(10000):
    #calculate new P(r)/rho(r)
    rho=((n_sim[:,None]*rho_i).sum(axis=0))/(n_sim[:,None] * exp_U_bias / minus_exp_F[:,None]).sum(axis=0)
    #normalize
    rho=rho/rho.sum()
    
    #calculate new F_i(window)
    minus_exp_F_old=1*minus_exp_F[:]
    for i,column in enumerate(exp_U_bias):
        #minus_exp_F[i]=np.trapz(4*np.pi*x*x*column*rho,x)
        minus_exp_F[i]=np.sum(rho*column*(4*np.pi/3*(3*x*x*binSize+3*x*binSize*binSize+binSize*binSize*binSize*np.ones(len(x)))))

    #get difference in e^-F_i
    diff=np.sum(np.square(minus_exp_F-minus_exp_F_old))
    
    #print some output
    if ncycles%20 == 0:
        print(ncycles,"\t",diff,"\t", minus_exp_F, "\n")
        #print(rho,"\n")
        
    if diff < 0.00001:
        print("WHAM converged with squared difference in free energy of ")
        print('\t',diff)
        print('\n\tafter ',ncycles, ' iterations')
        break

#calculate the pmf from the correctly weighted distribution function
PMF=-np.log(rho)

#write out results
fn='pmf_dendr_atherm_g'+G+'_s'+S+'_k'+K
print(fn)
np.savetxt(fn+'.dat', np.column_stack((x,rho,PMF)), fmt='%.4e', delimiter='\t', header='r_c2c\tP(r_c2c)\tPMF')

#make a plot
plt.xlabel("c2c distance")
plt.ylabel("PMF")
plt.plot(x,PMF)
#plt.show()
plt.savefig(fn+'.pdf', bbox_inches='tight')

