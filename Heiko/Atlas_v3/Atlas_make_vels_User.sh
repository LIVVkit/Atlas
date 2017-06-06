#!/bin/bash

# create additional velocity magnitude files

########### User settings

# Path to model data archive
apath=/Volumes/ISMIP6/Archive/05
# Region
aregion=GIS
# Group
agroup=IMAU
# Model
amodel=IMAUICE05

##########################################

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
