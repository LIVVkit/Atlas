#!/bin/bash
#***********************************************
# ISMIP6 Atlas scripts
# Plot diagnostic model output
# Heiko Goelzer Nov 2016 (hgoelzer@uu.nl)
#
# Runs the atlas function with those with variable names and plot parameters read
# from defaults_file

# Format defaults_file:
# <exp> <var> <timestep> <colorpalette> <levelmode> <lmin> <lmax> <lstep> <levels>
# 
# If <levelmode>=0 automatic levels will be used based on data 
#     <lmin> <lmax> <lstep> <levels> are ignored
# If <levelmode>=1 levels are in range [<lmin> .. <lmax>]
#    If <lstep> is non-zero, it is used as levels spacing 
#     <levels> is ignored
# If <levelmode>=2 explicit labels <levels> are used
#     <lmin> <lmax> <lstep> is ignored
# Example automatic: init lithk 0 "WhiteBlueGreenYellowRed" 0 0 0 0 "(/0/)"  
# Example manual: init topg 0 "GMT_wysiwyg" 1 -3000 3000 500 "(/0/)"  
# Example explicit: init orog 0 "GMT_relief" 2 0 0 0 "(/0,10,100,1000,10000/)"  

########### User settings

# Atlas configuration
defaults_file="Atlas_defaults_initMIP-Greenland.txt"
# Path to model data archive
apath=/Volumes/ISMIP6/Archive/05
# Region
aregion=GIS
# Groups
declare -a groups=(ARC AWI AWI BGC BGC BGC DMI DMI DMI DMI DMI ILTS ILTS_PIK IMAU IMAU IMAU JPL1 LANL LGGE LGGE LSCE MIROC MIROC MPIM MPIM UAF UAF UAF UAF UAF UAF ULB ULB VUB VUB UCIJPL)
# Models
declare -a models=(PISM5KM ISSM1 ISSM2 BISICLES1 BISICLES2 BISICLES3 PISM0 PISM1 PISM2 PISM3 PISM4 SICOPOLIS SICOPOLIS IMAUICE05 IMAUICE10 IMAUICE20 ISSM CISM ELMER ELMER2 GRISLI ICIES00 ICIES01 PISM0COMPUTED PISM0INITMIP PISM151 PISM152 PISM301 PISM302 PISM451 PISM452 FETISH1 FETISH2 GISMHOM GISMSIA ISSM)

##########################################

date

##### checks on operation
# array sizes match
if [ ${#groups[@]} -eq ${#models[@]} ]; then
    gcount=${#models[@]}
else
    echo Error: length of groups and models has to match ! ${#groups[@]} ${#models[@]}
    exit 1
fi

# loop trough labs/models
gcounter=0
while [ $gcounter -lt ${gcount} ]; do

    agroup=${groups[$counter]}
    amodel=${models[$counter]}
    alabel=$agroup_amodel
    
    # Arrays for parameters
    exps=()
    vars=()
    tsps=()
    pals=()
    mods=()
    mins=()
    maxs=()
    lsps=()
    lvls=()

    count=0

    # Read parameters from file line by line
    while read -r parameters
    do
	IFS=" " read -a par_array <<< "$parameters"
	exps+=(${par_array[0]})
	vars+=(${par_array[1]})
	tsps+=(${par_array[2]})
	pals+=(${par_array[3]})
	mods+=(${par_array[4]})
	mins+=(${par_array[5]})
	maxs+=(${par_array[6]})
	lsps+=(${par_array[7]})
	lvls+=(${par_array[8]})
	count=$count+1
    done < "$defaults_file"


    # Loop through variables 
    for (( i=0; i<$count; i++ ))
    do

	aexp=${exps[i]}
	avar=${vars[i]}
	echo ${avar}
	afile=${apath}/${agroup}/${amodel}/${aexp}/${avar}_${aregion}_${agroup}_${amodel}_${aexp}.nc
	#    echo ${afile}
	atsp=${tsps[i]}
	#    echo ${atsp}

	apal=${pals[i]}

	amod=${mods[i]}

	amin=${mins[i]}
	amax=${maxs[i]}
	alsp=${lsps[i]}

	alvl1=${lvls[i]}
	#    echo $alvl1 
	alvl=`echo $alvl1 | tr -d '"'`
	#    echo $alvl 


	# check file exists
	if [ -e $afile ]; then
	    
	    # call ncl script passing shell variable (-Q supresses startup note)  
	    ncl -Q afile=\"${afile}\" aexp=\"${aexp}\" avar=\"${avar}\" atsp=${atsp} apal=${apal} amod=${amod} amin=${amin} amax=${amax} alsp=${alsp} alvl=${alvl} alabel=\"${alabel}\" atlas_fun.ncl
	else
	    echo Warning: $avar file not present 
	fi

    done
    # end var loop

gcounter=$(( gcounter+1 ))
done
# end lab/model loop

date

