#!/bin/bash

echo "running awk snippet merge columns by existing key"

# define variables
file1="filename1"
file2="filename2"
resultsfile="resultfile.dat"
examplerun=0

# if there are no files create some example files
if [ ! -s "${file1}" ] && [ ! -s "${file2}" ]; then 
  echo -e "0.25 \t 1.11 \t 2.22" >  ${file1}
  echo -e "0.50 \t 1.12 \t 2.21" >> ${file1}
  echo -e "0.75 \t 1.12 \t 2.21" >> ${file1}
  echo -e "0.50 \t 1.52 \t 2.51" >  ${file2}
  examplerun=1
  cat ${file1}
  cat ${file2}
fi

# remove comments and blank lines from data files (might be added after merging again...
grep -v "#" "${file1}" | grep -v "^$"> tmp_d.dat
grep -v "#" "${file2}" | grep -v "^$"> tmp_c.dat

cat tmp_d.dat
cat tmp_c.dat

# do some magic with awk
awk -F'\t' 'BEGIN{i=0; j=0;OFS="\t "} FNR==NR{a[$1]=$0;c[i]=$0;d[i]=$1;i++;next};($1 in a) {e[j]=$0;f[$1]=$1;j++}; END {k=0;for(j=0;j<(NR-FNR);j++) {x=d[j];if(x in f){ print c[j], e[j-k]} else {print c[j], d[j],"\t0\t0";k++} } }' tmp_d.dat tmp_c.dat > ${resultsfile}

# clean up an show results
cat ${resultsfile}
if [ -s "tmp_d.dat" ]; then rm tmp_d.dat; fi
if [ -s "tmp_c.dat" ]; then rm tmp_c.dat; fi
if ((${examplerun} == 1)); then rm ${file1} ${file2} ${resultsfile}; fi

echo "awk snippet merge columns by existing key finished"
