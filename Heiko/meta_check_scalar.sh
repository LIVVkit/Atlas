#!/bin/bash

# check data archive for basic consistency

# location of data archive
#outp=../initMIP/output;
#outp=../ftp/output;
outp=../Archive/05;

# labs list
declare -a labs=(ARC AWI AWI BGC BGC BGC DMI DMI DMI DMI DMI ILTS ILTS_PIK IMAU IMAU JPL1 LANL LGGE LGGE LSCE MIROC MIROC MPIM MPIM UAF UAF UAF UAF UAF UAF ULB ULB VUB VUB)
# models list
declare -a models=(PISM5KM ISSM1 ISSM2 BISICLES1 BISICLES2 BISICLES3 PISM0 PISM1 PISM2 PISM3 PISM4 SICOPOLIS SICOPOLIS IMAUICE05 IMAUICE10 ISSM CISM ELMER ELMER2 GRISLI ICIES00 ICIES01 PISM0COMPUTED PISM0INITMIP PISM151 PISM152 PISM301 PISM302 PISM451 PISM452 FETISH1 FETISH2 GISMHOM GISMSIA )

##### checks on operation

# array sizes match
if [ ${#labs[@]} -eq ${#models[@]} ]; then 
    count=${#models[@]}
else
    echo Error: length of labs and models has to match  
    exit 1
fi


##### SCALARS
echo "------------------"
echo Check on scalar files 
echo "------------------"
exps="init ctrl asmb"
res="05"

# loop trough labs/models
counter=0
while [ $counter -lt ${count} ]; do

#   # loop trough experiments    
    for exp in ${exps}; do

	echo .
	echo checking ${outp}/${labs[$counter]} ${models[$counter]} ${exp}
	
	./nc_check_scalars.sh ${outp}/${labs[$counter]}/${models[$counter]}/${exp}/scalar_GIS_${labs[$counter]}_${models[$counter]}_${exp}.nc 
	
    done
#   # end exp loop
    
    counter=$(( counter+1 )) 
done
# end lab/model loop


