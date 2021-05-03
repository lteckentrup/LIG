for var in insol prec temp; do
    ncpdq -F -O -a lat,lon,time ${var}_CRUTS4.04.nc ${var}_CRUTS4.04.nc
    ncpdq -F -O -a lat,lon,time ${var}_LIG.nc ${var}_LIG.nc
    ncpdq -F -O -a lat,lon,time ${var}_LIG_scaling_multi.nc ${var}_LIG_scaling_multi.nc
    ncpdq -F -O -a lat,lon,time ${var}_LIG_scaling_add.nc ${var}_LIG_scaling_add.nc
done
