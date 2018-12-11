#!/bin/bash/

echo -e "find consequitive repeated words in textfile. \nPrint the words and the line numbers\n"

filename=$1

if [ -z "$filename" ]; then
    echo "no filename passed to script"
    exit 1
else
    grep -o -E -n '\w+' $filename | uniq -d
    echo -e "\nfind repeated consequitve words script finished\n"
fi
