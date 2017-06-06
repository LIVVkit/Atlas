#!/bin/bash

# create additional velocity magnitude files

########### User settings

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
    count=${#models[@]}
else
    echo Error: length of groups and models has to match ! ${#groups[@]} ${#models[@]}
    exit 1
fi

# loop trough labs/models
counter=0
while [ $counter -lt ${count} ]; do

    agroup=${groups[$counter]}
    amodel=${models[$counter]}
    alabel=$agroup_amodel

    for aexp in init ctrl asmb; do

	ncap2 -O -s "uvelmean2=uvelmean*uvelmean" -v ${apath}/${agroup}/${amodel}/${aexp}/uvelmean_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velmean_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncap2 -A -s "vvelmean2=vvelmean*vvelmean" -v ${apath}/${agroup}/${amodel}/${aexp}/vvelmean_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velmean_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncap2 -O -s "velmean=sqrt(vvelmean2*uvelmean2)" -v ${apath}/${agroup}/${amodel}/${aexp}/velmean_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velmean_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncatted -a standard_name,velmean,o,c,land_ice_vertical_mean_velocity ${apath}/${agroup}/${amodel}/${aexp}/velmean_${aregion}_${agroup}_${amodel}_${aexp}.nc
	
	ncap2 -O -s "uvelsurf2=uvelsurf*uvelsurf" -v ${apath}/${agroup}/${amodel}/${aexp}/uvelsurf_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velsurf_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncap2 -A -s "vvelsurf2=vvelsurf*vvelsurf" -v ${apath}/${agroup}/${amodel}/${aexp}/vvelsurf_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velsurf_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncap2 -O -s "velsurf=sqrt(vvelsurf2*uvelsurf2)" -v ${apath}/${agroup}/${amodel}/${aexp}/velsurf_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velsurf_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncatted -a standard_name,velsurf,o,c,land_ice_surface_velocity ${apath}/${agroup}/${amodel}/${aexp}/velsurf_${aregion}_${agroup}_${amodel}_${aexp}.nc

	ncap2 -O -s "uvelbase2=uvelbase*uvelbase" -v ${apath}/${agroup}/${amodel}/${aexp}/uvelbase_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velbase_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncap2 -A -s "vvelbase2=vvelbase*vvelbase" -v ${apath}/${agroup}/${amodel}/${aexp}/vvelbase_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velbase_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncap2 -O -s "velbase=sqrt(vvelbase2*uvelbase2)" -v ${apath}/${agroup}/${amodel}/${aexp}/velbase_${aregion}_${agroup}_${amodel}_${aexp}.nc ${apath}/${agroup}/${amodel}/${aexp}/velbase_${aregion}_${agroup}_${amodel}_${aexp}.nc
	ncatted -a standard_name,velbase,o,c,land_ice_basal_velocity ${apath}/${agroup}/${amodel}/${aexp}/velbase_${aregion}_${agroup}_${amodel}_${aexp}.nc

    done

counter=$(( counter+1 ))
done
# end lab/model loop
