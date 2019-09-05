#!/bin/bash

# load modules and formats
export LC_NUMERIC="en_US.UTF-8"

# parameters
array_generation=( 5 6 )
array_spacer=( 1 2 )
array_chainlength=( 1 16 128 )
array_dendr_fraction=( $(seq -f "%.2f" 0.05 0.1 0.95 ) ) # total number density is set separately

# system boxsize, reqired for the filename
boxsize=128

# check if there are files without !mcs= command, typical bfm error if write headder was called but nothing else
## check the whole directory tree G, S N and DF
nFiles=$(ls -l G*/S*/N*/DF*/*_b128.bfm | wc -l)
nCorrectFiles=$( grep "\!mcs=" G*/S*/N*/DF*/*_b128.bfm | wc -l )
if [ "$nFiles" -ne "$nCorrectFiles" ]; then
  echo $nFiles is larger than $nCorrectFiles
fi # if not sure wheter or not corrupted files are there, finish this loop at the and of the processing block below
   ## to avoid empty runs

# loop over the files
for generation in "${array_generation[@]}"; do
    generation_dir="G${generation}"
    if [ -d "${generation_dir}" ]; then
        cd ${generation_dir}
        for spacer in "${array_spacer[@]}"; do
            spacer_dir="S${spacer}"
            if [ -d "${spacer_dir}" ]; then
                cd ${spacer_dir}
                for chainlength in "${array_chainlength[@]}"; do
                    chainlength_dir="N${chainlength}"
                    if [ -d "${chainlength_dir}" ]; then
                        cd ${chainlength_dir}
                        for dendr_fraction in "${array_dendr_fraction[@]}"; do
                            dendr_fraction_dir="DF${dendr_fraction}"
                            if [ -d "${dendr_fraction_dir}" ]; then
                                cd ${dendr_fraction_dir}
				# tell me where we are
				#echo $generation $spacer $chainlength $dendr_fraction
				# setup filename
				filename="dips_wallZ_g${generation}_s${spacer}_n${chainlength}_df${dendr_fraction}_b${boxsize}"
				# check if the main bfm file was damaged, for other kinds of corruptions other checks must be implemented here
				findMCS=$(grep "mcs=" ${filename}.bfm)
				if [ -z "$findMCS" ]; then
				  echo 
				  echo found corrupted file: ${filename}.bfm
				  # get the different file sizes
				  corruptedFileSize=$(ls -la ${filename}.bfm | awk {'print $5'})
				  # get a list of existing files containing a least one correct file (the _start.bfm)
				  ls -la ${filename}_start.bfm | awk {'printf "%s %s\n", $9, $5'} > sortedFilelist.txt
				  ls -lah ${filename}_*_lastconfig.bfm | awk {'printf "%s %s\n", $9, $5'} | sort -V -k1 >> sortedFilelist.txt
				  # the second last file in this list should be the last correct file
				  lastCorrectFile=$(tail -2 sortedFilelist.txt | head -1 | awk {'print $1'})
				  fullFileSize=$(ls -la ${lastCorrectFile} | awk {'print $5'})
				  # overwrite the corrupted bfm file by the last correct file
				  cp $lastCorrectFile ${filename}.bfm
				  bfmFileSize=$(ls -la ${filename}.bfm | awk {'print $5'})
				  if [ "$fullFileSize" -eq "$bfmFileSize" ]; then
				    # get a list of all corrupted files by file size, _lastconfig and _0_ full config file should have the same header thus the same size
				    ls -la ${filename}_*.bfm | grep "$corruptedFileSize" | awk {'printf "%s\n", $9'} > removeFileList.txt
				    rm -v `cat removeFileList.txt`
				    # clean up
				    rm sortedFilelist.txt removeFileList.txt
				  else
				    echo "something went wrong after overwriting the bfm file"
				  fi
				  echo 
				fi # end check file corruption
								cd ..
			    			fi # end check dendr_fraction_dir
						done # end loop array_dendr_fraction
						cd ../
		    		fi # end check chainlength_dir
				done # end loop array_chainlength
				cd ../
	    	fi # end check spacer_dir
		done # end loop array_spacer
		cd ../
    fi # end check generation_dir
done # end loop array_generation
