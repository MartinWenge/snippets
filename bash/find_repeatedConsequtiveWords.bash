#!/bin/bash/

echo -e "find consequitive repeated words in textfile. \nPrint the words and the line numbers\n"

filename=$1

if [ -z "$filename" ]; then
    echo "no filename passed to script"
    exit 1
else
    # get numbered comparison and unnumbered comparison for line break consecutive words
    grep -o -E -n '\w+' $filename | uniq -d > 1
    grep -o -E '\w+' $filename | uniq -d > 2

    # display numbered results
    cat 1

    # warning if line break sensitive search found more words
    if (( $(wc -l <1) < $(wc -l <2) )); then
        echo -e "\nsome consequtive repeated words occur after linebreak!"
    fi

    # delete utility files
    rm 1 2

    echo -e "\nfind repeated consequitve words script finished\n"
fi
