import pandas as pd
import xarray as xr
import os
import numpy as np
from datetime import date
from netCDF4 import Dataset as open_ncfile
import xesmf as xe

pathwayOUT='/g/data/w35/lt0205/research/lpj_guess/forcing/climdata/'
def LIG(var_nick, var_lpj):

    ds = xr.open_dataset(var_nick+
                         '_Amon_ACCESS-ESM1-5_lig127k_r1i1p1f1_gn_106601-110012.nc')

    ds = ds.rename(bnds='bounds')
    ds_out = xr.Dataset({'latitude': (['latitude'], 
                                      np.arange(-89.75, 90.25, 0.5)),
                         'longitude': (['longitude'], 
                                       np.arange(-179.75, 180.25, 0.5)),
                         }
                        )
    dr = ds[var_nick]
    ### REGRID
    regrid = xe.Regridder(ds, ds_out, 'conservative')
    dr_out = regrid(dr)
    dr_out=dr_out.transpose('latitude','longitude','time')
    da = dr_out.to_dataset()

    # create dataset
    if var_lpj == 'temp':
        da['tas'].attrs={'long_name': 'Temperature at 2m',
                         'standard_name': 'air_temperature',
                         'units'     : 'K'}
        da = da.rename({'tas':'temp'})

    elif var_lpj == 'prec':
        da['pr'].attrs={'long_name': 'Precipitation',
                        'standard_name': 'precipitation_flux',
                        'units': 'kg m-2 s-1'}
        da['pr']=da['pr'].where(da['pr']>0,0)
        da = da.rename({'pr':'prec'})

    elif var_lpj == 'insol':
        da['rsdt'].attrs= {'long_name':'Downward solar radiation flux',
                           'standard_name':'surface_downwelling_shortwave_flux',
                           'units'     :'W m-2'}
        da = da.rename({'rsdt':'insol'})

    else:
        pass

    da['latitude'].attrs={'units':'degrees_north', 'long_name':'latitude',
                          'standard_name':'latitude', 'axis':'Y'}
    da['longitude'].attrs={'units':'degrees_east', 'long_name':'longitude',
                           'standard_name':'longitude', 'axis':'X'}

    da = da.rename({'latitude':'lat'})
    da = da.rename({'longitude':'lon'})

    da.attrs={'Conventions':'CF-1.7 CMIP-6.2',
              'Institution':'Commonwealth Scientific and '
              'Industrial Research Organisation, Aspendale, '
              'Victoria 3195, Australia',
              'Title':'ACCESS-ESM1-5 output prepared for CMIP6'}

    da.to_netcdf(var_lpj+'_LIG_time100.nc',
                 encoding={'lat':{'dtype': 'double'},
                           'lon':{'dtype': 'double'},
                           'time':{'dtype': 'double'},
                           var_lpj:{'chunksizes':(360,720,200),
                                    'dtype': 'float32'}})
    # da.to_netcdf(var_lpj+'_LIG_time100.nc',
    #              encoding={'lat':{'dtype': 'double'},
    #                        'lon':{'dtype': 'double'},
    #                        'time':{'dtype': 'double'},
    #                        var_lpj:{'dtype': 'float32'}})
LIG('tas', 'temp')
LIG('pr', 'prec')
LIG('rsdt', 'insol')
