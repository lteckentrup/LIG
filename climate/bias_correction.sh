for var in insol prec temp; do
    cdo ymonmean ${var}_CRUTS4.04.nc ${var}_CRUTS4.04_clim.nc
    cdo ymonmean ${var}_LIG.nc ${var}_LIG_clim.nc
    cdo sub ${var}_LIG_clim.nc ${var}_CRUTS4.04_clim.nc ${var}_anomaly.nc
    cdo div ${var}_CRUTS4.04_clim.nc ${var}_LIG_clim.nc ${var}_quotient.nc

    cdo sub ${var}_LIG.nc ${var}_anomaly.nc ${var}_LIG_scaling_add_prel.nc
    cdo mul ${var}_LIG.nc ${var}_quotient.nc ${var}_LIG_scaling_multi_prel.nc

    rm ${var}_CRUTS4.04_clim.nc
    rm ${var}_LIG_clim.nc
    rm ${var}_anomaly.nc
    rm ${var}_quotient.nc
done

for var in temp; do
    cdo ymonmean ${var}_CRUTS4.04_detrend.nc ${var}_CRUTS4.04_detrend_clim.nc
    cdo ymonmean ${var}_LIG.nc ${var}_LIG_clim.nc
    cdo sub ${var}_LIG_clim.nc ${var}_CRUTS4.04_detrend_clim.nc \
        ${var}_detrend_anomaly.nc

    cdo sub ${var}_LIG.nc ${var}_detrend_anomaly.nc \
        ${var}_LIG_detrend_scaling_add_prel.nc

    rm ${var}_LIG_detrend_scaling_add.nc
    rm ${var}_CRUTS4.04_detrend_clim.nc
    rm ${var}_LIG_clim.nc
    rm ${var}_trend_anomaly.nc
done

rm insol_LIG_scaling_add_prel.nc
rm insol_LIG_scaling_multi_prel.nc
cdo setrtoc,1,10000,1 insol_LIG_scaling_multi_prel.nc insol_LIG_scaling_multi.nc
rm prec_LIG_scaling_add_prel.nc
mv prec_LIG_scaling_multi_prel.nc prec_LIG_scaling_multi.nc
mv temp_LIG_scaling_add_prel.nc temp_LIG_scaling_add.nc
mv temp_LIG_scaling_multi_prel.nc temp_LIG_scaling_multi.nc
mv temp_LIG_detrend_scaling_add_prel.nc temp_LIG_detrend_scaling_add.nc
