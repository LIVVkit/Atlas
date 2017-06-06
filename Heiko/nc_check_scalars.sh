#!/bin/bash
# check variable and standard names in netcdf file
# heiko goelzer Feb 2016

# check arguments
if [ $# -eq 2 ] ; then
    afile=$1
    amode=$2
elif [ $# -eq 1 ] ; then
    afile=$1
    amode=1
else 
  echo "Usage: nc_check_scalars <ncfile> [<mode>]"
  echo "optional <mode> switches between compact (1, default) and full listing (2)"
  exit 1
fi

# path to nc file
ncfile=$afile
#ncfile="/Users/hgoelzer/Documents/CMIP6/ISMIP6/initMIP/Results/VUB/GISMSIA/asmb/scalar_GIS_VUB_GISMSIA_asmb.nc"
# mode: 1 list only missing variables; 2 full report
mode=$amode
#mode=1

##### hard settings

# variable name list to check
declare -a vars=(lim limnsw iareag iareaf tendacabf tendlibmassbf tendlicalvf)
# standard name list to check
declare -a stds=(land_ice_mass land_ice_mass_not_displacing_sea_water grounded_land_ice_area floating_ice_shelf_area tendency_of_land_ice_mass_due_to_surface_mass_balance tendency_of_land_ice_mass_due_to_basal_mass_balance tendency_of_land_ice_mass_due_to_calving)

##### checks on operation

# file exists
if [ ! -e $ncfile ]; then
    echo Error: file not found
    exit 1
fi
# array sizes match
if [ ${#vars[@]} -eq ${#stds[@]} ]; then 
    count=${#vars[@]}
else
    echo Error: length of variable and standard name list does not match  
    exit 1
fi

##### operate

# get header information
ncdump -h ${ncfile} > head.tmp

# check presence of variable names
#echo Check on variable names
#echo "------------------"
counter=0
while [ $counter -lt ${count} ]; do
    if (grep -q ${vars[$counter]}\( head.tmp); then
	if [ $mode -eq 2 ]; then
	    echo ${vars[$counter]} is present
	fi
    else
	echo \#  variable \*${vars[$counter]}\* is missing
    fi
    counter=$(( counter+1 )) 
done

# check presence of standard names
#echo Check on standard names
#echo "------------------"
counter=0
while [ $counter -lt ${count} ]; do
    if (grep -q "standard_name = \"${stds[$counter]}\"" head.tmp); then
	if [ $mode -eq 2 ]; then
	    echo ${stds[$counter]} is present
	fi
    else
	echo \#  standard name \*${stds[$counter]}\* is missing
    fi
    counter=$(( counter+1 )) 
done

# check variables have correct standard names
#echo Check variables have correct standard names
#echo "------------------"
counter=0
while [ $counter -lt ${count} ]; do
    if (grep -q "${vars[$counter]}:standard_name = \"${stds[$counter]}\"" head.tmp); then
	if [ $mode -eq 2 ]; then
	    echo standard name ${stds[$counter]} matches for variable ${vars[$counter]}
	fi
    else
	echo \#  standard name \*${stds[$counter]}\* does not match for \*${vars[$counter]}\*
    fi
    counter=$(( counter+1 )) 
done
