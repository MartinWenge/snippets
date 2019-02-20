#!/bin/bash

## setup configs on taurus:
# dendrimer in polymer melt from linear melt to dendrimer melt
# by setting up the directories and copy/call the slurm scripts 
# executing the setup

# load modules and formats
export LC_NUMERIC="en_US.UTF-8"

#module load foss/2018a
#module load Boost/1.66.0-foss-2018a

# directories
EXECUTABLE_DIR="/home/s7146169/softwareSCS5/LeMonADE/LeMonADE-tools/LeMonADE-dendrimer-tools/executables/build/bin"

# parameters
array_generation=( 5 6 )
array_spacer=( 1 2 )
array_chainlength=( 128 )
array_dendr_fraction=( $(seq -f "%.2f" 0.05 0.1 0.95 ) ) # total number density is set separately

boxsize=128
functionality=3
total_density=0.5

runtime="96:00:00"


for generation in "${array_generation[@]}"; do
    generation_dir="G${generation}"
    if [ ! -d "${generation_dir}" ]; then mkdir ${generation_dir}; fi

    if [ -d "${generation_dir}" ]; then
        cd ${generation_dir}

        for spacer in "${array_spacer[@]}"; do
            spacer_dir="S${spacer}"
            if [ ! -d "${spacer_dir}" ]; then mkdir ${spacer_dir}; fi

            if [ -d "${spacer_dir}" ]; then
                cd ${spacer_dir}

                for chainlength in "${array_chainlength[@]}"; do
                    chainlength_dir="N${chainlength}"
                    if [ ! -d "${chainlength_dir}" ]; then mkdir ${chainlength_dir}; fi

                    if [ -d "${chainlength_dir}" ]; then
                        cd ${chainlength_dir}

                        for dendr_fraction in "${array_dendr_fraction[@]}"; do
                            dendr_fraction_dir="DF${dendr_fraction}"
                            if [ ! -d "${dendr_fraction_dir}" ]; then mkdir ${dendr_fraction_dir}; fi

                            if [ -d "${dendr_fraction_dir}" ]; then
                                cd ${dendr_fraction_dir}

                                # tell me where we are
                                echo "g=${generation}, s=${spacer}, n=${chainlength}, df=${dendr_fraction}"
#
###########
# here we have well defined parameters and can work with them to setup the configs

# calculate all the numbers we need for system setup
num_monos_dendr="$(awk -v g=$generation -v s=$spacer -v f=$functionality "BEGIN {printf \"%.0f\",(1+(f*s*((f-1)^g-1)/(f-2)))}")"

filename="dips_g${generation}_s${spacer}_n${chainlength}_df${dendr_fraction}_b${boxsize}"

num_dendr="$(awk -v box="$boxsize" -v fracD=$dendr_fraction -v totDens=$total_density -v nmonosd=$num_monos_dendr "BEGIN {printf \"%i\",((box*box*box)*fracD*totDens)/(8*nmonosd)}")"

num_chain="$(awk -v box="$boxsize" -v fracD=$dendr_fraction -v totDens=$total_density -v nmonosc=$chainlength "BEGIN {printf \"%i\",((box*box*box)*(1-fracD)*totDens)/(8*nmonosc)}")"

num_monos_total="$(awk -v box="$boxsize" -v totDens=$total_density -v nmonosc=$N "BEGIN {printf \"%i\",((box*box*box)*totDens)/(8)}")"

sum_monos=$((${num_dendr}*${num_monos_dendr} + ${num_chain}*${chainlength}))

echo "${num_dendr}*${num_monos_dendr} + ${num_chain}*${chainlength} = ${sum_monos} < ${num_monos_total}"

# write a slurm file
if [ ! -s "${filename}_setup.slurm" ]; then

    echo "#!/bin/bash" > ${filename}_setup.slurm
    echo >> ${filename}_setup.slurm
    echo "#SBATCH -J ${filename}.%j.slurm" >> ${filename}_setup.slurm
    echo "#SBATCH --nodes=1   # number of nodes" >> ${filename}_setup.slurm
    echo "#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)" >> ${filename}_setup.slurm

    echo "#SBATCH --time=${runtime}" >> ${filename}_setup.slurm
    echo "#SBATCH --error=setup.%j.err" >> ${filename}_setup.slurm
    echo "#SBATCH --output=setup.%j.out" >> ${filename}_setup.slurm
    echo "#SBATCH --mail-type=FAIL" >> ${filename}_setup.slurm
    echo "#SBATCH --mail-user=wengenmayr@ipfdd.de" >> ${filename}_setup.slurm
    echo "#SBATCH -A p_gitterpolymere" >> ${filename}_setup.slurm

    echo >> ${filename}_setup.slurm
    echo "JOBNAME=\"$filename\"" >> ${filename}_setup.slurm
    echo >> ${filename}_setup.slurm

    echo "echo Running on host" >> ${filename}_setup.slurm
    echo "hostname" >> ${filename}_setup.slurm
    echo "MY_TMP_DIR=\$(mktemp -d)" >> ${filename}_setup.slurm
    echo "cd \$MY_TMP_DIR" >> ${filename}_setup.slurm
    echo "pwd" >> ${filename}_setup.slurm
    echo >> ${filename}_setup.slurm

    echo >> ${filename}_setup.slurm
    echo "module load foss/2018a" >> ${filename}_setup.slurm
    echo "module load Boost/1.66.0-foss-2018a" >> ${filename}_setup.slurm
    echo >> ${filename}_setup.slurm

    echo "#### copy executables to local disk ####" >> ${filename}_setup.slurm
    echo "cp ${EXECUTABLE_DIR}/createDendrimers ." >> ${filename}_setup.slurm
    echo "cp ${EXECUTABLE_DIR}/createAddFreeChains ." >> ${filename}_setup.slurm
#createDendrimers
#createAddFreeChains - > deprecated, check option read ins ...
    echo >> ${filename}_setup.slurm
    echo "./createDendrimers -f ${filename}_start.bfm -g ${generation} -s ${spacer} -b ${boxsize} -n ${num_dendr} -u 1" >> ${filename}_setup.slurm
    echo "if [ -s \"${filename}_start.bfm\" ]; then" >> ${filename}_setup.slurm
    echo "  ./createAddFreeChains -i ${filename}_start.bfm -o ${filename}.bfm -l ${chainlength} -n ${num_chain}" >> ${filename}_setup.slurm
    echo "  cp ${filename}.bfm ${filename}_start.bfm" >> ${filename}_setup.slurm
    echo "fi" >> ${filename}_setup.slurm
    echo >> ${filename}_setup.slurm

    echo "##! IMPORTANT: copy back results" >> ${filename}_setup.slurm
    echo "rm createDendrimers" >> ${filename}_setup.slurm
    echo "rm createAddFreeChains" >> ${filename}_setup.slurm
    echo "cp * \$SLURM_SUBMIT_DIR" >> ${filename}_setup.slurm
    echo "cd ../" >> ${filename}_setup.slurm
    echo >> ${filename}_setup.slurm

    echo "##! IMPORTANT: cleaning up after myself" >> ${filename}_setup.slurm
    echo "rm -rf \$MY_TMP_DIR" >> ${filename}_setup.slurm
    echo  >> ${filename}_setup.slurm

fi

# run the slurm script
if [ -s "${filename}_setup.slurm" ]; then
    if [ ! -s "${filename}_start.bfm" ]; then
      sbatch ${filename}_setup.slurm
    fi
fi


###########
#
                            cd .. # go back to chainlength directory
                            fi
                        done # end dendr_fraction loop
                    cd .. # go back to spacer length directory
                    fi
                done # end chainlength loop
            cd .. # go back to generation directory
            fi
        done # end spacer loop
    cd .. # go back to head directory
    fi
done # end generation loop

