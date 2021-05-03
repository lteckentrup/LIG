suffix='Amon_ACCESS-ESM1-5_lig127k_r1i1p1f1_gn_090101-110012.nc'
pathwayIN='PMIP'

cdo -b F64 -L -chunit,'kg m-2 s-1','kg m-2' -setcalendar,365_day \
    -remapycon,halfdegree.txt -mulc,86400 -muldpm -setvrange,0,1 \
    -selyear,1066/1100 ${pathwayIN}/pr/gn/latest/pr_${suffix} prec_LIG.nc
ncrename -v pr,prec prec_LIG.nc
ncatted -O -a standard_name,prec,o,c,precipitation_amount prec_LIG.nc
ncatted -O -a long_name,lat,c,c,latitude prec_LIG.nc
ncatted -O -a long_name,lon,c,c,longitude prec_LIG.nc
ncatted -O -a title,,d,, prec_LIG.nc

cdo -b F64 -L -setcalendar,365_day -remapycon,halfdegree.txt -selyear,1066/1100 \
    ${pathwayIN}/tas/gn/latest/tas_${suffix} temp_LIG.nc
ncrename -v tas,temp temp_LIG.nc
ncatted -O -a long_name,lat,c,c,latitude temp_LIG.nc
ncatted -O -a long_name,lon,c,c,longitude temp_LIG.nc
ncatted -O -a long_name,temp,o,c,"Temperature at 2m" temp_LIG.nc
ncatted -O -a title,,d,, temp_LIG.nc

cdo -b F64 -L -chunit,%,1 -setcalendar,365_day -remapycon,halfdegree.txt \
    -divc,100 -selyear,1066/1100 ${pathwayIN}/clt/gn/latest/clt_${suffix} insol_LIG.nc
ncrename -v clt,insol insol_LIG.nc
ncatted -O -a standard_name,insol,o,c,cloud_area_fraction \
        insol_LIG.nc
ncatted -O -a long_name,lat,c,c,latitude insol_LIG.nc
ncatted -O -a long_name,lon,c,c,longitude insol_LIG.nc
ncatted -O -a long_name,insol,o,c,"Cloud Area Fraction" insol_LIG.nc
ncatted -O -a title,,d,, insol_LIG.nc
