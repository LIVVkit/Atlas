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


##### Fields
echo "------------------"
echo Check on 2D files 
echo "------------------"

declare -a vars2d=(acabf dlithkdt hfgeoubed libmassbf licalvf litempbot litempsnic lithk orog sftgrf sftflf sftgif strbasemag topg uvelbase uvelmean uvelsurf vvelbase vvelmean vvelsurf wvelbase wvelsurf)
count2=${#vars2d[@]}

exps="init ctrl asmb"
res="05"

# loop trough labs/models
counter=0
while [ $counter -lt ${count} ]; do

#   # loop trough experiments    
    for exp in ${exps}; do

	echo .
	echo checking ${outp}/${labs[$counter]} ${models[$counter]} ${exp}
	
#       # loop trough variables    
	counter2=0
	while [ $counter2 -lt ${count2} ]; do	    


	    ncfile=${outp}/${labs[$counter]}/${models[$counter]}/${exp}/${vars2d[$counter2]}_GIS_${labs[$counter]}_${models[$counter]}_${exp}.nc
	    if [ ! -e $ncfile ]; then
#		echo ${ncfile} missing 
		echo ${vars2d[$counter2]} missing 
#	    else	
# get header information
#		ncdump -h ${ncfile} > head.tmp
	    fi

	    counter2=$(( counter2+1 )) 
	done
#       # end var loop

    done
#   # end exp loop

    counter=$(( counter+1 )) 
done
# end lab/model loop


