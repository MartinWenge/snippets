#!/bin/bash/

echo "replace uint by uint32_t, required by gcc 4.9+"

grep -rl "const uint max_bonds=4;" executables/* > filelist.txt
grep -rl "const uint max_bonds=4;" cudaSimulators/* >> filelist.txt

while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "$line"
    grep "const uint max_bonds=4;" $line
    sed -i 's/const uint max_bonds=4/const uint32_t max_bonds=4/g' $line
done < filelist.txt

#for i in xa*; do
#    sed -i 's/asd/dfg/g' $i
#done


echo "replacement completed"
