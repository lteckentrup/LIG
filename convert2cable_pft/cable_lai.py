import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

ds_fpc = xr.open_dataset('fpc_LPJ-GUESS_1066-1100_BC_detrend.nc')
ds_fpc['Woody'] = ds_fpc['Total'] - ds_fpc['C3G'] - ds_fpc['C4G']
ds_fpc['Grass'] = ds_fpc['C3G'] + ds_fpc['C4G']

ds = xr.open_dataset('lai_LPJ-GUESS_1066-1100_BC_detrend.nc')
ds['Evergreen Needleleaf'] = ds['BNE']+ds['BINE']+ds['TeNE']
ds['Evergreen Broadleaf'] = ds['TeBE']+ds['TrBE']+ds['TrIBE']
ds['Deciduous Needleleaf'] = ds['BNS']
ds['Deciduous Broadleaf'] = ds['BIBS']+ds['TeBS']+ds['TeIBS']+ds['TrBR']
ds['Shrub_total'] = ds['BESh']+ds['BSSh']+ds['TeESh']+ds['TeRSh']+ds['TeSSh']+ \
                    ds['TrESh']+ds['TrRSh']

shrub_total = ds.Shrub_total
tundra = xr.where((np.isnan(shrub_total[:,:,:])==False)&
                  ((shrub_total.Lat<60)|(shrub_total.Lat>75)), 0,shrub_total)
shrub = xr.where((np.isnan(shrub_total[:,:,:])==False)&
                 ((shrub_total.Lat>60)&(shrub_total.Lat<75)), 0,shrub_total)
total = ds.Total
bare = xr.where((np.isnan(total[:,:,:])==False)&
                ((ds_fpc['Grass']>0.1)|(ds_fpc['Woody']>0.1)), 0,total)

ds['Tundra'] = tundra
ds['Shrub'] = shrub
ds['Crop'] = ds['BNS']*0
ds['Wetland'] = ds['BNS']*0
ds['Ice'] = ds['BNS']*0
ds['Bare ground'] = bare

ds = ds.drop(['BNE', 'BINE', 'BNS', 'BIBS', 'TeNE', 'TeBS', 'TeIBS', 'TeBE',
              'TrBE', 'TrIBE', 'TrBR', 'BESh', 'BSSh', 'TeESh', 'TeRSh', 'TeSSh',
              'TrESh', 'TrRSh'])

ds.to_netcdf('LIG_LAI_BC.nc',
             encoding={'Lat':{'dtype': 'double'},
                       'Lon':{'dtype': 'double'},
                       'Time':{'dtype': 'double'},
                       'Evergreen Needleleaf':{'dtype': 'float32'},
                       'Evergreen Broadleaf':{'dtype': 'float32'},
                       'Deciduous Needleleaf':{'dtype': 'float32'},
                       'Deciduous Broadleaf':{'dtype': 'float32'},
                       'Shrub':{'dtype': 'float32'},
                       'Tundra':{'dtype': 'float32'},
                       'Crop':{'dtype': 'float32'},
                       'Wetland':{'dtype': 'float32'},
                       'C3G':{'dtype': 'float32'},
                       'C4G':{'dtype': 'float32'},
                       'Total':{'dtype': 'float32'}})
