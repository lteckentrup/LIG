pathwayIN='/CRUTS4.04'

cdo -b F64 -L -chunit,'mm/month','kg m-2' -setcalendar,365_day -selvar,pre \
    ${pathwayIN}/CRUTS4.04_prec.nc prec_CRUTS4.04.nc
ncrename -v pre,prec prec_CRUTS4.04.nc
ncatted -O -a standard_name,prec,o,c,precipitation_amount prec_CRUTS4.04.nc

cdo -b F64 -L -chunit,'degrees Celsius','K' -setcalendar,365_day -selvar,tmp \
    -addc,273.15 \
    ${pathwayIN}/CRUTS4.04_temp.nc temp_CRUTS4.04.nc
ncrename -v tmp,temp temp_CRUTS4.04.nc
ncatted -O -a standard_name,temp,o,c,air_temperature temp_CRUTS4.04.nc
ncatted -O -a long_name,temp,o,c,"Temperature at 2m" temp_CRUTS4.04.nc

cdo detrend temp_CRUTS4.04.nc temp_CRUTS4.04_detrend_prel.nc
cdo trend temp_CRUTS4.04.nc a.nc b.nc
cdo add a.nc temp_CRUTS4.04_detrend_prel.nc temp_CRUTS4.04_detrend.nc

cdo -b F64 -L -chunit,percentage,1 -setcalendar,365_day -selvar,cld \
    -divc,100 ${pathwayIN}/CRUTS4.04_cld.nc insol_CRUTS4.04.nc
ncrename -v cld,insol insol_CRUTS4.04.nc
ncatted -O -a standard_name,insol,o,c,cloud_area_fraction insol_CRUTS4.04.nc
ncatted -O -a long_name,insol,o,c,"Cloud Area Fraction" insol_CRUTS4.04.nc
