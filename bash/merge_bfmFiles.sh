#!/bin/bash

echo "merge bfm files"

if [ -n "$1" ]; then
    filenameBase=$1
fi
if [ -n "$2" ]; then
    filenameSuf=$2
fi
if [ ! -n "$1" ] && [ ! -n "$2" ]; then
    echo "no input filename given"
    exit 1
fi

#filenameBase="dips_g5_s1_n128_df0.05_b128"

if [ -s "filelist.txt" ]; then rm filelist.txt; fi

for myfile in ${filenameBase}_*.bfm; do
    # check if file in glob exists
    [[ -e $myfile ]] || continue
    # check if file is _lastconfig
    regex="_lastconfig"
    [[ $myfile =~ $regex ]] && continue
    # check if file is _start
    regex="_start"
    [[ $myfile =~ $regex ]] && continue
    # check if file is _full
    regex="_full"
    [[ $myfile =~ $regex ]] && continue

    if [ -n "$2" ]; then
        regex=$filenameSuf
        [[ $myfile =~ $regex ]] && echo $myfile >> filelist.txt
    else
        echo $myfile >> filelist.txt
    fi

done

# sort the filenames by "version" numering -V
cat filelist.txt | sort -V > sorted_filelist.txt

# write the header from the top file
sed -e '/\!mcs=/,$d' $(head -1 sorted_filelist.txt) > ${filenameBase}_full.bfm

# add the configs to the header
for myfile in $(cat sorted_filelist.txt); do
    echo ${myfile}
    sed -n -e '/\!mcs=/,$p' ${myfile} >> ${filenameBase}_full.bfm
done

#echo $size_header
#echo $size_full
#echo "total file size in kb:"
#du -k ${filenameBase}_full.bfm | cut -f1

#clean up
if [ -s "filelist.txt" ]; then rm filelist.txt; fi
if [ -s "sorted_filelist.txt" ]; then rm sorted_filelist.txt; fi
