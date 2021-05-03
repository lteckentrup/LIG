import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib.colors import BoundaryNorm
import matplotlib as mpl
import xarray as xr
import numpy as np
from netCDF4 import Dataset as netcdf_dataset

lai = netcdf_dataset('lai_LPJ-GUESS_1066-1100_BC.nc')
cmass = netcdf_dataset('cmass_LPJ-GUESS_1066-1100_BC_grid.nc')
cmass_allen = netcdf_dataset('cmass_LPJ-GUESS_126kDVI.nc')

LAI_BNE = lai.variables['BNE'][:,:,:]
LAI_BINE = lai.variables['BINE'][:,:,:]
LAI_BNS = lai.variables['BNS'][:,:,:]
LAI_BIBS = lai.variables['BIBS'][:,:,:]
LAI_TeNE = lai.variables['TeNE'][:,:,:]
LAI_TeBS = lai.variables['TeBS'][:,:,:]
LAI_TeIBS = lai.variables['TeIBS'][:,:,:]
LAI_TeBE = lai.variables['TeBE'][:,:,:]
LAI_TrBE = lai.variables['TrBE'][:,:,:]
LAI_TrIBE = lai.variables['TrIBE'][:,:,:]
LAI_TrBR = lai.variables['TrBR'][:,:,:]
LAI_BESh = lai.variables['BESh'][:,:,:]
LAI_BSSh = lai.variables['BSSh'][:,:,:]
LAI_TeESh = lai.variables['TeESh'][:,:,:]
LAI_TeRSh = lai.variables['TeRSh'][:,:,:]
LAI_TeSSh = lai.variables['TeSSh'][:,:,:]
LAI_TrESh = lai.variables['TrESh'][:,:,:]
LAI_TrRSh = lai.variables['TrRSh'][:,:,:]
LAI_C3G = lai.variables['C3G'][:,:,:]
LAI_C4G = lai.variables['C4G'][:,:,:]
LAI_Total = lai.variables['Total'][:,:,:]

CMASS_Total = cmass.variables['Total'][:,:,:]

## stealing carbon mass and ice area from Allen et al., 2020
CMASS_area = cmass_allen.variables['area'][:,:]
CMASS_ice = cmass_allen.variables['ice-free'][:,:]

LAI_BNE_avg = np.mean(LAI_BNE[:,:,:],axis=0)
LAI_BINE_avg = np.mean(LAI_BINE[:,:,:],axis=0)
LAI_BIBS_avg = np.mean(LAI_BIBS[:,:,:],axis=0)
LAI_BNS_avg = np.mean(LAI_BNS[:,:,:],axis=0)
LAI_TeNE_avg = np.mean(LAI_TeNE[:,:,:],axis=0)
LAI_TeBS_avg = np.mean(LAI_TeBS[:,:,:],axis=0)
LAI_TeIBS_avg = np.mean(LAI_TeIBS[:,:,:],axis=0)
LAI_TeBE_avg = np.mean(LAI_TeBE[:,:,:],axis=0)
LAI_TrBE_avg = np.mean(LAI_TrBE[:,:,:],axis=0)
LAI_TrIBE_avg = np.mean(LAI_TrIBE[:,:,:],axis=0)
LAI_TrBR_avg = np.mean(LAI_TrBR[:,:,:],axis=0)
LAI_BESh_avg = np.mean(LAI_BESh[:,:,:],axis=0)
LAI_BSSh_avg = np.mean(LAI_BSSh[:,:,:],axis=0)
LAI_TeESh_avg = np.mean(LAI_TeESh[:,:,:],axis=0)
LAI_TeRSh_avg = np.mean(LAI_TeRSh[:,:,:],axis=0)
LAI_TeSSh_avg = np.mean(LAI_TeSSh[:,:,:],axis=0)
LAI_TrESh_avg = np.mean(LAI_TrESh[:,:,:],axis=0)
LAI_TrRSh_avg = np.mean(LAI_TrRSh[:,:,:],axis=0)
LAI_C3G_avg = np.mean(LAI_C3G[:,:,:],axis=0)
LAI_C4G_avg = np.mean(LAI_C4G[:,:,:],axis=0)
LAI_Total_avg = np.mean(LAI_Total[:,:,:],axis=0)

CMASS_Total_avg = np.mean(CMASS_Total[:,:,:],axis=0)

LAI_B_tree_avg = LAI_BNE_avg + LAI_BINE_avg + LAI_BNS_avg + LAI_BIBS_avg
LAI_Te_tree_avg = LAI_TeNE_avg + LAI_TeBS_avg + LAI_TeIBS_avg + LAI_TeBE_avg
LAI_Tr_tree_avg = LAI_TrBE_avg + LAI_TrIBE_avg + LAI_TrBR_avg
LAI_B_shrub_avg = LAI_BESh_avg + LAI_BSSh_avg
LAI_Te_shrub_avg = LAI_TeESh_avg + LAI_TeRSh_avg + LAI_TeSSh_avg
LAI_Tr_shrub_avg = LAI_TrESh_avg + LAI_TrRSh_avg

lat = lai.variables['Lat'][:]
lon = lai.variables['Lon'][:]

matrix = np.zeros((len(lat), len(lon)))

mask = LAI_Total_avg.filled(fill_value=np.nan)
for x in range(len(lat)):
    for y in range(len(lon)):

        sum1 = LAI_TeRSh_avg[x,y] + LAI_TeESh_avg[x,y]
        thresh = 1e9*((CMASS_area[x,y]*CMASS_ice[x,y])/100)/3087.53

        if np.isfinite(mask[x,y]) == False:
            matrix[x,y] = np.nan
        elif CMASS_Total_avg[x,y] < thresh:
            if LAI_BESh_avg[x,y] > 0.0:
                matrix[x,y] = 23 ### Tundra
            elif LAI_BESh_avg[x,y]== 0:
                matrix[x,y] = 1 ### Desert
        elif CMASS_Total_avg[x,y] > thresh:
            if LAI_C3G_avg[x,y] > 0.3:
                matrix[x,y] = 15 ### Steppe / Temperate Grassland
            elif LAI_C3G_avg[x,y] <= 0.3:
                pass
            if LAI_TrBE_avg[x,y] > 2.0:
                matrix[x,y] = 6 ### Tropical Evergreen Forest
            elif LAI_TrBE_avg[x,y] <= 2.0:
                pass
            else:
                pass
            if LAI_TrBR_avg[x,y] > 0.6:
                matrix[x,y] = 5 ### Tropical Raingreen Forest
            elif LAI_TrBR_avg[x,y] <= 0.6:
                pass
            else:
                pass

            if LAI_TeNE_avg[x,y] > 1.0:
                matrix[x,y] = 10 ### Temperate Needle-leaved Evergreen Forest
            elif LAI_TeNE_avg[x,y] <= 1.0:
                pass

            if LAI_TeBE_avg[x,y] > 1.0:
                matrix[x,y] = 10 ### Temperate Broad-leaved Evergreen Forest
            elif LAI_TeBE_avg[x,y] <= 1.0:
                pass

            if (LAI_TeRSh_avg[x,y] + LAI_TeESh_avg[x,y]) > 0.3:
                if LAI_B_tree_avg[x,y] > 0.02:
                    matrix[x,y] = 17 ### Boreal Parkland
                elif LAI_B_tree_avg[x,y] <= 0.02:
                    pass
                elif LAI_TeBS_avg[x,y] > 0.02:
                    matrix[x,y] = 14 ### Temperate Parkland
                elif LAI_TeBS_avg[x,y] <= 0.02:
                    pass
                elif LAI_TeBE_avg[x,y] > 0.3:
                    matrix[x,y] = 9 ### Warm Temperate Woodland
                elif LAI_TeBE_avg[x,y] <= 0.3:
                    pass
            elif LAI_C3G_avg[x,y] > (LAI_TeRSh_avg[x,y] + LAI_TeESh_avg[x,y]):
                matrix[x,y] = 2  ### Semi-desert
            else:
                matrix[x,y] = 7 ### Temperate Shrubland

            if LAI_BESh_avg[x,y] > 0.3:
                matrix[x,y] = 22 ### Montane/Boreal Shrubland / Shrub Tundra
            elif LAI_BESh_avg[x,y] <= 0.3:
                pass
            if LAI_BIBS_avg[x,y] > 0.1:
                matrix[x,y] = 20 ### Boreal Summergreen Broadleaf Forest
            elif LAI_BIBS_avg[x,y] <= 0.1:
                pass

            if LAI_BNE_avg[x,y] > 0.3:
                matrix[x,y] = 18 ### Boreal Evergreen Needleleaf Forest
            elif LAI_BNE_avg[x,y] <= 0.3:
                pass

            diff1 = LAI_Total_avg[x,y] - (LAI_C3G_avg[x,y] + LAI_BESh_avg[x,y])
            if diff1<= 0.01 and diff1>=0.01:
                matrix[x,y] = 23 ### Tundra (additional criterion)

            diff = LAI_Total_avg[x,y]-(LAI_TeBE_avg[x,y]+LAI_C3G_avg[x,y]+LAI_TeESh_avg[x,y]+LAI_TeRSh_avg[x,y])
            if diff <= 0.01 and diff >= -0.01:
                matrix[x,y] = 7 ### Temperate Shrubland (additional criterion5)

            if LAI_TeBS_avg[x,y] > 1.0:
                if LAI_B_tree_avg[x,y] > 0.1 or LAI_TeNE_avg[x,y] > 0.1:
                    matrix[x,y] = 13 ### Temperate Mixed Forest
                elif LAI_B_tree_avg[x,y] <= 0.1 and LAI_TeNE_avg[x,y] <= 0.1:
                    matrix[x,y] = 11 ### Temperate Summergreen Forest
            elif LAI_TeBS_avg[x,y] <= 1.0:
                pass

            if LAI_BNS_avg[x,y] > 0.1:
                if LAI_BESh_avg[x,y] > 1.0:
                    matrix[x,y] = 21 ### Boreal Woodland
                elif LAI_BESh_avg[x,y] <= 1.0:
                    matrix[x,y] = 19 ### Boreal Summergreen Needleleaf Forest
            elif LAI_BNS_avg[x,y] <= 0.1:
                pass

            if LAI_C4G_avg[x,y] > 0.3:
                if LAI_Tr_shrub_avg[x,y] > 0.3 or LAI_TrBR_avg[x,y] > 0.3:
                    matrix[x,y] = 4 ### Savanna
                elif LAI_Tr_shrub_avg[x,y] <= 0.3 and LAI_TrBR_avg[x,y] <= 0.3:
                    matrix[x,y] = 3 ### Tropical Grassland
            elif LAI_C4G_avg[x,y] <= 0.3:
                pass

            if (LAI_TrBE_avg[x,y]+LAI_TrIBE_avg[x,y]) > 1.7:
                matrix[x,y] = 6 ### Tropical Evergreen Forest (additional criterion)
            elif (LAI_TrBE_avg[x,y]+LAI_TrIBE_avg[x,y]) <= 1.7:
                pass

            if LAI_TrBR_avg[x,y] > 0.6:
                matrix[x,y] = 5 ### Tropical Raingreen Forest
            elif LAI_TrBR_avg[x,y] <= 0.6:
                pass

        else:
            matrix[x,y] = np.nan

ds = xr.Dataset({'Biomes': (('lat', 'lon'), matrix)},coords={'lat': lat,'lon': lon,},)

ds.to_netcdf('LIG.nc')
