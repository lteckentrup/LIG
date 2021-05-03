import pandas as pd
import xarray as xr
import os
import numpy as np
from datetime import date

date_created = date.today()

def convert_ascii_netcdf_annual(var, experiment):

    df = pd.read_csv('/g/data/w35/lt0205/research/lpj_guess_modify/runs_LIG/'+
                     experiment+'/'+var+'.out',header=0,error_bad_lines=False,
                     delim_whitespace=True)

    years = np.unique(df.Year)
    first_year = str(int(years[0]))
    last_year = str(int(years[-1]))
    print(last_year)
    df2 = df.rename(columns={'Year': 'Time'})
    ds = df2.set_index(['Time', 'Lat', 'Lon']).to_xarray()

    ds.Time.encoding['units'] = 'Years since 1066-01-01 00:00:00'
    ds.Time.encoding['long_name'] = 'Time'
    ds.Time.encoding['calendar'] = '365_day'

    # add metadata
    ds['Lat'].attrs={'units':'degrees', 'long_name':'Latitude'}
    ds['Lon'].attrs={'units':'degrees', 'long_name':'Longitude'}

    ## Fill up missing latitudes and longitudes
    dx = ds.Lon - ds.Lon.shift(shifts={'Lon':1})
    dx = dx.min()
    dy = ds.Lat - ds.Lat.shift(shifts={'Lat':1})
    dy = dy.min()

    newlon = np.arange((-180.+dx/2.),180.,dx)
    newlon = xr.DataArray(newlon, dims=("Lon"),coords={"Lon":newlon},
                          attrs=ds.Lon.attrs)

    newlat = np.arange((90.+dy/2.),-90., dy)
    newlat = xr.DataArray(newlat, dims=("Lat"), coords={"Lat":newlat},
                          attrs=ds.Lat.attrs)

    foo = xr.DataArray(np.empty((ds.Time.size, newlat.size, newlon.size)),
                       dims=("Time", "Lat", "Lon"),
                       coords={"Time":ds.Time, "Lat":newlat, "Lon":newlon},
                       name="foo")

    foo[:]=np.NaN
    ds_fill = ds.broadcast_like(foo)

    # add global attributes
    ds_fill.attrs={'Conventions':'CF-1.6',
                   'Model':'LPJ-GUESS version 4.0.1.',
                   'Set-up': 'Stochastic and fire disturbance active',
                   'Date_Created':str(date_created)}

    fileOUT = var+'_LPJ-GUESS_'+first_year+'-'+last_year+'_'+experiment+'.nc'

    if var in ('fpc', 'lai'):

        ds_fill['BNE'].attrs={'units':'m2 m-2',
                              'long_name':'Boreal Needleleaved Evergreen tree'}
        ds_fill['BINE'].attrs={'units':'m2 m-2',
                              'long_name':'Boreal Shade Intolerant Needleleaved Evergreen tree'}
        ds_fill['BNS'].attrs={'units':'m2 m-2',
                              'long_name':'Boreal Needleleaved '
                              'Summergreen tree'}
        ds_fill['BIBS'].attrs={'units':'m2 m-2',
                              'long_name':'Shade-intolerant Boreal Broad-leaved '
                              'Summergreen tree'}
        ds_fill['TeNE'].attrs={'units':'m2 m-2',
                               'long_name':'Temperate Needleleaved '
                               'Evergreen tree'}
        ds_fill['TeBS'].attrs={'units':'m2 m-2',
                               'long_name':'Temperate (shade-tolerant) '
                               'Broadleaved Summergreen tree'}
        ds_fill['TeIBS'].attrs={'units':'m2 m-2',
                              'long_name':'boreal/ temperate shade-Intolerant '
                              'Broadleaved Summergreen tree'}
        ds_fill['TeBE'].attrs={'units':'m2 m-2',
                               'long_name':'Temperate Broadleaved Evergreen '
                               'tree'}
        ds_fill['TrBE'].attrs={'units':'m2 m-2',
                               'long_name':'Tropical Broadleaved Evergreen '
                               'tree'}
        ds_fill['TrIBE'].attrs={'units':'m2 m-2',
                                'long_name':'Tropical Broadleaved Evergreen '
                                'shade-Intolerant tree'}
        ds_fill['TrBR'].attrs={'units':'m2 m-2',
                               'long_name':'Tropical Broadleaved Raingreen '
                               'tree'}
        ds_fill['BESh'].attrs={'units':'m2 m-2',
                               'long_name':'Boreal Evergreen Shrub'}
        ds_fill['BSSh'].attrs={'units':'m2 m-2',
                               'long_name':'Boreal Summergreen Shrub'}
        ds_fill['TeESh'].attrs={'units':'m2 m-2',
                               'long_name':'Temperate Evergreen Shrub'}
        ds_fill['TeRSh'].attrs={'units':'m2 m-2',
                               'long_name':'Temperate Raingreen Shrub'}
        ds_fill['TeSSh'].attrs={'units':'m2 m-2',
                               'long_name':'Temperate Summergreen Shrub'}
        ds_fill['TrESh'].attrs={'units':'m2 m-2',
                               'long_name':'Tropical Evergreen Shrub'}
        ds_fill['TrRSh'].attrs={'units':'m2 m-2',
                               'long_name':'Tropical Raingreen Shrub'}
        ds_fill['C3G'].attrs={'units':'m2 m-2',
                              'long_name':'(cool) C3 Grass'}
        ds_fill['C4G'].attrs={'units':'m2 m-2',
                              'long_name':'(warm) C4 Grass'}
        ds_fill['Total'].attrs={'units':'m2 m-2',
                                       'long_name':'Total'}

        ds_fill.to_netcdf(fileOUT, encoding={'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Time':{'dtype': 'double'},
                                             'Total':{'dtype': 'float32'},
                                             'BNE':{'dtype': 'float32'},
                                             'BINE':{'dtype': 'float32'},
                                             'BNS':{'dtype': 'float32'},
                                             'BIBS':{'dtype': 'float32'},
                                             'TeNE':{'dtype': 'float32'},
                                             'TeBS':{'dtype': 'float32'},
                                             'TeIBS':{'dtype': 'float32'},
                                             'TeBE':{'dtype': 'float32'},
                                             'TrBE':{'dtype': 'float32'},
                                             'TrIBE':{'dtype': 'float32'},
                                             'TrBR':{'dtype': 'float32'},
                                             'BESh':{'dtype': 'float32'},
                                             'BSSh':{'dtype': 'float32'},
                                             'TeESh':{'dtype': 'float32'},
                                             'TeRSh':{'dtype': 'float32'},
                                             'TeSSh':{'dtype': 'float32'},
                                             'TrESh':{'dtype': 'float32'},
                                             'TrRSh':{'dtype': 'float32'},
                                             'C3G':{'dtype': 'float32'},
                                             'C4G':{'dtype': 'float32'}})

    elif var in ('aaet', 'agpp', 'clitter', 'cmass', 'cton_leaf', 'dens', 'anpp',
                 'nlitter', 'nmass', 'nuptake', 'vmaxnlim', 'height'):

        ds_fill['BNE'].attrs={'units':'kg m-2',
                              'long_name':'Boreal Needleleaved Evergreen tree'}
        ds_fill['BINE'].attrs={'units':'kg m-2',
                              'long_name':'Boreal Shade Intolerant Needleleaved Evergreen tree'}
        ds_fill['BNS'].attrs={'units':'kg m-2',
                              'long_name':'Boreal Needleleaved '
                              'Summergreen tree'}
        ds_fill['BIBS'].attrs={'units':'kg m-2',
                              'long_name':'Shade-intolerant Boreal Broad-leaved '
                              'Summergreen tree'}
        ds_fill['TeNE'].attrs={'units':'kg m-2',
                               'long_name':'Temperate Needleleaved '
                               'Evergreen tree'}
        ds_fill['TeBS'].attrs={'units':'kg m-2',
                               'long_name':'Temperate (shade-tolerant) '
                               'Broadleaved Summergreen tree'}
        ds_fill['TeIBS'].attrs={'units':'kg m-2',
                              'long_name':'boreal/ temperate shade-Intolerant '
                              'Broadleaved Summergreen tree'}
        ds_fill['TeBE'].attrs={'units':'kg m-2',
                               'long_name':'Temperate Broadleaved Evergreen '
                               'tree'}
        ds_fill['TrBE'].attrs={'units':'kg m-2',
                               'long_name':'Tropical Broadleaved Evergreen '
                               'tree'}
        ds_fill['TrIBE'].attrs={'units':'kg m-2',
                                'long_name':'Tropical Broadleaved Evergreen '
                                'shade-Intolerant tree'}
        ds_fill['TrBR'].attrs={'units':'kg m-2',
                               'long_name':'Tropical Broadleaved Raingreen '
                               'tree'}
        ds_fill['BESh'].attrs={'units':'kg m-2',
                               'long_name':'Boreal Evergreen Shrub'}
        ds_fill['BSSh'].attrs={'units':'kg m-2',
                               'long_name':'Boreal Summergreen Shrub'}
        ds_fill['TeESh'].attrs={'units':'kg m-2',
                               'long_name':'Temperate Evergreen Shrub'}
        ds_fill['TeRSh'].attrs={'units':'kg m-2',
                               'long_name':'Temperate Raingreen Shrub'}
        ds_fill['TeSSh'].attrs={'units':'kg m-2',
                               'long_name':'Temperate Summergreen Shrub'}
        ds_fill['TrESh'].attrs={'units':'kg m-2',
                               'long_name':'Tropical Evergreen Shrub'}
        ds_fill['TrRSh'].attrs={'units':'kg m-2',
                               'long_name':'Tropical Raingreen Shrub'}
        ds_fill['C3G'].attrs={'units':'kg m-2',
                              'long_name':'(cool) C3 Grass'}
        ds_fill['C4G'].attrs={'units':'kg m-2',
                              'long_name':'(warm) C4 Grass'}
        ds_fill['Total'].attrs={'units':'kg m-2',
                                       'long_name':'Total'}

        ds_fill.to_netcdf(fileOUT, encoding={'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Time':{'dtype': 'double'},
                                             'Total':{'dtype': 'float32'},
                                             'BNE':{'dtype': 'float32'},
                                             'BINE':{'dtype': 'float32'},
                                             'BNS':{'dtype': 'float32'},
                                             'BIBS':{'dtype': 'float32'},
                                             'TeNE':{'dtype': 'float32'},
                                             'TeBS':{'dtype': 'float32'},
                                             'TeIBS':{'dtype': 'float32'},
                                             'TeBE':{'dtype': 'float32'},
                                             'TrBE':{'dtype': 'float32'},
                                             'TrIBE':{'dtype': 'float32'},
                                             'TrBR':{'dtype': 'float32'},
                                             'BESh':{'dtype': 'float32'},
                                             'BSSh':{'dtype': 'float32'},
                                             'TeESh':{'dtype': 'float32'},
                                             'TeRSh':{'dtype': 'float32'},
                                             'TeSSh':{'dtype': 'float32'},
                                             'TrESh':{'dtype': 'float32'},
                                             'TrRSh':{'dtype': 'float32'},
                                             'C3G':{'dtype': 'float32'},
                                             'C4G':{'dtype': 'float32'}})

    elif var == 'cflux':
        ds_fill['Veg'].attrs={'units':'kgC/m2/year',
                              'long_name':'Vegetation NPP'}
        ds_fill['Repr'].attrs={'units':'kgC/m2/year',
                               'long_name':'Respired litter derived from '
                               'plant allocation to reproduction'}
        ds_fill['Soil'].attrs={'units':'kgC/m2/year',
                               'long_name':'Soil heterotrophic respiration'}
        ds_fill['Fire'].attrs={'units':'kgC/m2/year',
                               'long_name':'Wildfire emissions'}
        ds_fill['Est'].attrs={'units':'kgC/m2/year',
                              'long_name':'Biomass of plants establishing in '
                              'the current year'}
        ds_fill['NEE'].attrs={'units':'kgC/m2/year', 'long_name':'Net C flux '
                              '(sum of other fluxes'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Veg':{'dtype': 'float32'},
                                             'Repr':{'dtype': 'float32'},
                                             'Soil':{'dtype': 'float32'},
                                             'Fire':{'dtype': 'float32'},
                                             'Est':{'dtype': 'float32'},
                                             'NEE':{'dtype': 'float32'}})

    elif var == 'cpool':
        ds_fill['VegC'].attrs={'units':'kgC/m2',
                               'long_name':'Vegetation carbon pool'}
        ds_fill['LitterC'].attrs={'units':'kgC/m2',
                                  'long_name':'Litter carbon pool'}
        ds_fill['SoilC'].attrs={'units':'kgC/m2',
                                'long_name':'Soil carbon pool'}
        ds_fill['Total'].attrs={'units':'kgC/m2',
                                'long_name':'Total carbon pool'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'VegC':{'dtype': 'float32'},
                                             'LitterC':{'dtype': 'float32'},
                                             'SoilC':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'firert':
        ds_fill['FireRT'].attrs={'units':'yr',
                                 'long_name':'Fire return time'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'FireRT':{'dtype': 'float32'}})
    elif var == 'doc':
        ds_fill['Total'].attrs={'units':'kgC/m2r',
                                'long_name':'Total dissolved organic carbon'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Total':{'dtype': 'float32'}})
    elif var == 'nflux':
        ds_fill['dep'].attrs={'units':'kgN/ha',
                              'long_name':'Deposition'}
        ds_fill['fix'].attrs={'units':'kgN/ha',
                              'long_name':'Fixation'}
        ds_fill['fert'].attrs={'units':'kgN/ha',
                               'long_name':'fertilization'}
        ds_fill['flux'].attrs={'units':'kgN/ha',
                               'long_name':'Soil emission'}
        ds_fill['leach'].attrs={'units':'kgN/ha',
                                'long_name':'leaching'}
        ds_fill['NEE'].attrs={'units':'kgN/ha',
                              'long_name':'Net N flux (sum of other fluxes)'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'dep':{'dtype': 'float32'},
                                             'fix':{'dtype': 'float32'},
                                             'fert':{'dtype': 'float32'},
                                             'flux':{'dtype': 'float32'},
                                             'leach':{'dtype': 'float32'},
                                             'NEE':{'dtype': 'float32'}})


    elif var == 'ngases':
        ds_fill['NH3'].attrs={'units':'kgN/ha/year',
                              'long_name':'NH3 flux to atmosphere from fire'}
        ds_fill['NOx'].attrs={'units':'kgN/ha/year',
                              'long_name':'NOx flux to atmosphere from fire'}
        ds_fill['N2O'].attrs={'units':'kgN/ha/year',
                              'long_name':'N2O flux to atmosphere from fire'}
        ds_fill['N2'].attrs={'units':'kgN/ha',
                             'long_name':'N2O flux to atmosphere from fire'}
        ds_fill['NSoil'].attrs={'units':'kgN/ha', 'long_name':'??'}
        ds_fill['Total'].attrs={'units':'kgN/ha', 'long_name':'Total'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'NH3':{'dtype': 'float32'},
                                             'NOx':{'dtype': 'float32'},
                                             'N2O':{'dtype': 'float32'},
                                             'N2':{'dtype': 'float32'},
                                             'NSoil':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'npool':
        ds_fill['VegN'].attrs={'units':'kgN/m2',
                               'long_name':'Vegetation nitrogen pool'}
        ds_fill['LitterN'].attrs={'units':'kgN/m2',
                                  'long_name':'Litter nitrogen pool'}
        ds_fill['SoilN'].attrs={'units':'kgN/m2',
                                'long_name':'Soil nitrogen pool'}
        ds_fill['Total'].attrs={'units':'kgN/m2',
                                'long_name':'Total nitrogen pool'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'VegN':{'dtype': 'float32'},
                                             'LitterN':{'dtype': 'float32'},
                                             'SoilN':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'nsources':
        ds_fill['dep'].attrs={'units':'gN/ha', 'long_name':'Deposition'}
        ds_fill['fix'].attrs={'units':'gN/ha', 'long_name':'Fixation'}
        ds_fill['fert'].attrs={'units':'gN/ha', 'long_name':'fertilization'}
        ds_fill['input'].attrs={'units':'gN/ha', 'long_name':'??'}
        ds_fill['min'].attrs={'units':'gN/ha', 'long_name':'??'}
        ds_fill['imm'].attrs={'units':'gN/ha',
                              'long_name':'Nitrogen immobilisation'}
        ds_fill['netmin'].attrs={'units':'gN/ha', 'long_name':'??'}
        ds_fill['Total'].attrs={'units':'gN/ha', 'long_name':'Total'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'dep':{'dtype': 'float32'},
                                             'fix':{'dtype': 'float32'},
                                             'fert':{'dtype': 'float32'},
                                             'input':{'dtype': 'float32'},
                                             'min':{'dtype': 'float32'},
                                             'imm':{'dtype': 'float32'},
                                             'netmin':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})

    elif var == 'tot_runoff':
        ds_fill['Surf'].attrs={'units':'mm/year',  'long_name':'Surface runoff'}
        ds_fill['Drain'].attrs={'units':'mm/year', 'long_name':'??'}
        ds_fill['Base'].attrs={'units':'mm/year', 'long_name':'??'}
        ds_fill['Total'].attrs={'units':'mm/year', 'long_name':'??'}

        # save to netCDF
        ds_fill.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                             'Lat':{'dtype': 'double'},
                                             'Lon':{'dtype': 'double'},
                                             'Surf':{'dtype': 'float32'},
                                             'Drain':{'dtype': 'float32'},
                                             'Base':{'dtype': 'float32'},
                                             'Total':{'dtype': 'float32'}})
    else:
        pass

def convert_ascii_netcdf_monthly(pathway, var, experiment):
    fname = '/g/data/w35/lt0205/research/lpj_guess_australia/runs/'+pathway+'/'+var+'.out'
    df = pd.read_csv(fname, header=0, delim_whitespace=True)

    months=list(df.columns)
    months=months[3:]

    lons = np.unique(df.Lon)
    lats = np.unique(df.Lat)
    years = np.unique(df.Year)
    first_year=str(int(years[0]))
    last_year=str(int(years[-1]))
    nyears = len(years)
    nrows = len(lats)
    ncols = len(lons)
    nmonths = 12
    lons.sort()
    lats.sort()
    years.sort()

    # Create the axes
    time = pd.date_range(start=f'01/{years[0]}',
                         end=f'01/{years[-1]+1}', freq='M')

    dx = 0.5
    Lon = xr.DataArray(np.arange(-180.+dx/2., 180., dx), dims=("Lon"),
                       attrs={"long_name":"longitude", "unit":"degrees_east"})
    nlon = Lon.size
    dy = 0.5
    Lat = xr.DataArray(np.arange(-90.+dy/2., 90., dy), dims=("Lat"),
                       attrs={"long_name":"latitude", "unit":"degrees_north"})
    nlat = Lat.size

    out = xr.DataArray(np.zeros((nyears*nmonths,nlat, nlon)),
                       dims=("Time","Lat","Lon"),
                       coords=({"Lat":Lat, "Lon":Lon, "Time":time}))
    out[:] = np.nan
    df_stack = df[months].stack()

    for nr in range(0,len(df.index),nyears):
        rows = df[nr:nr+nyears]
        thislon = rows["Lon"].min()
        thislat = rows["Lat"].min()
        out.loc[dict(
                Lon=thislon,
                Lat=thislat)] = df_stack[nr*nmonths:(nr+nyears)*nmonths]

    out.Time.encoding['units'] = 'Seconds since 1901-01-01 00:00:00'
    out.Time.encoding['long_name'] = 'Time'
    out.Time.encoding['calendar'] = '365_day'

    print(out['Lat'])
    out_oz = out.sel(Lat=slice(-43.25,-10.25),Lon=slice(112.25,153.25))
    print(out_oz['Lat'])
    ds= out_oz.to_dataset(name=var)

    if experiment == 'no_dist':
        ds.attrs={'Conventions':'CF-1.6',
                  'Model':'LPJ-GUESS version 4.0.1.',
                  'Set-up': 'Stochastic and fire disturbance not active',
                  'Title':experiment, 'Date_Created':str(date_created)}
    elif experiment == 'SE_CO2':
        ds.attrs={'Conventions':'CF-1.6',
                  'Model':'LPJ-GUESS version 4.0.1.',
                  'Set-up': 'Stochastic and fire disturbance active',
                  'Title':'Fixed CO2', 'Date_Created':str(date_created)}
    elif experiment == 'SE_N':
        ds.attrs={'Conventions':'CF-1.6',
                  'Model':'LPJ-GUESS version 4.0.1.',
                  'Set-up': 'Stochastic and fire disturbance active',
                  'Title':'Nitrogen cycle not active', 'Date_Created':str(date_created)}
    elif experiment == 'SE_KLATOSA':
        ds.attrs={'Conventions':'CF-1.6',
                  'Model':'LPJ-GUESS version 4.0.1.',
                  'Set-up': 'Stochastic and fire disturbance active',
                  'Title':'klatosa set to 8000', 'Date_Created':str(date_created)}
    else:
        ds.attrs={'Conventions':'CF-1.6',
                  'Model':'LPJ-GUESS version 4.0.1.',
                  'Set-up': 'Stochastic and fire disturbance active',
                  'Title':experiment, 'Date_Created':str(date_created)}

    fileOUT = pathway+'/'+var+'_LPJ-GUESS_'+first_year+'-'+last_year+'.nc'

    if var == 'maet':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly actual Evapotranspiration'}
    elif var == 'mevap':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly Evapotranspiration'}
    elif var == 'mgpp':
        ds[var].attrs={'units':'kgC/m2/month', 'long_name':'Monthly GPP'}
    elif var == 'mintercep':
        ds['mintercep'].attrs={'units':'mm/month',
                               'long_name':'Monthly interception Evaporation'}
    elif var == 'miso':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly isopene emissions'}
    elif var == 'miso':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly monterpene emissions'}
    elif var == 'mmon':
        ds[var].attrs={'units':'kg/month',
                       'long_name':'Monthly isoprene emissions'}
    elif var == 'mnee':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly NEE'}
    elif var == 'mnpp':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly NPP'}
    elif var == 'mpet':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly potential evapotranspiration'}
    elif var == 'mra':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly autotrophic respiration'}
    elif var == 'mrh':
        ds[var].attrs={'units':'kgC/m2/month',
                       'long_name':'Monthly heterotrophic respiration'}
    elif var == 'mlai':
        ds[var].attrs={'units':'m2/m2',
                       'long_name':'Monthly LAI'}
    elif var == 'mrunoff':
        ds[var].attrs={'units':'mm/month',
                       'long_name':'Monthly runoff'}
    elif var == 'mwcont_lower':
        ds[var].attrs={'units':'fraction of available water-holding capacity',
                       'long_name':'Monthly water in content in lower soil layer'
                       '(50 - 150 cm)'}
    elif var == 'mwcont_upper':
        ds[var].attrs={'units':'fraction of available water-holding capacity',
                       'long_name':'Monthly water in content in upper soil layer'
                       '(0 - 50 cm)'}
    ds.to_netcdf(fileOUT, encoding={'Time':{'dtype': 'double'},
                                    'Lat':{'dtype': 'double'},
                                    'Lon':{'dtype': 'double'},
                                     var:{'dtype': 'float32'}})
