#!/bin/bash

# show queue with project, job id, partition, job name, user name, job state, runtime, walltime, number of nodes, hostname, priority
# (way more information than squeue -l) 
squeue -o "%.10a %.10i %.9P %.50j %.8u %.8T %.10M %.9l %.6D %R %p"
