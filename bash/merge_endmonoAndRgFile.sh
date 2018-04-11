#!/bin/bash

# use this grep command to select 
grep "^5[[:space:]][1-8][[:space:]]" maxOfEndMonoDistr_G5_sdips_sum.dat > endMono.dat
grep "^5[[:space:]][1-8][[:space:]]" rg_sdips_sum.dat > rg.dat

if [ $(rg.dat | wc -l) -eq $(endMono.dat | wc -l) ]; then
    head endMono.dat
    head rg.dat
    awk '{print $6"\t"$7"\t"$9}' rg.dat > rgOnly.dat
    head rgOnly.dat
    paste endMono.dat rgOnly.dat > 1
    mv 1 maxOfEndMonoDistr_rg_G5_sdips_sum.dat
    rm rgOnly.dat rg.dat endMono.dat
    head maxOfEndMonoDistr_rg_G5_sdips_sum.dat
    head -1 maxOfEndMonoDistr_G5_sdips_sum.dat > 1
    awk '{print $6"\t"$7"\t"$9}' rg_sdips_sum.dat | head -1 > 2
    paste 1 2 > 3
    sed -i "1s/^/$(head -1 3)\n/" maxOfEndMonoDistr_rg_G5_sdips_sum.dat
    head maxOfEndMonoDistr_rg_G5_sdips_sum.dat

    echo "merged endnumDist and rg"
else
    echo "files do not fit: "rg.dat | wc -l", "endMono.dat | wc -l
fi
