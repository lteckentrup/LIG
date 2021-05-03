import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib.colors import BoundaryNorm
import matplotlib as mpl

import numpy as np
from netCDF4 import Dataset as netcdf_dataset

def wurst():

    biomes = netcdf_dataset('LIG_bc.nc')
    
    BIOMES = biomes.variables['Biomes'][:,:]
    lats = biomes.variables['lat'][:]
    lons = biomes.variables['lon'][:]

    colors=['#ffebb0', '#ccac67', '#ffd682', '#ffac00', '#70a900', '#05714d',
            '#a46f09', '#fe0000', '#e7e600', '#02a784', '#abff02', '#73b1fe',
            '#00ffc6', '#cfff74', '#a80000', '#fbffff', '#01c4ff', '#014ea8',
            '#8500aa', '#c501ff', '#bfd0ff', '#febee8', '#c09ed5', '#e4ffff']

    biomes = ['Desert', 'Semi-desert', 'Tropical Grassland', 'Savanna',
              'Tropical Raingreen Forest', 'Tropical Evergreen Forest',
              'Temperate Shrubland', 'Unclassified', 'Warm Temperate Woodland',
              'Temperate Broad-leaved Evergreen Forest',
              'Temperate Summergreen Forest',
              'Temperate Needle-leaved Evergreen Forest', 
              'Temperate Mixed Forest', 'Temperate Parkland', 'Steppe', 
              'Ice sheet', 'Boreal Parkland', 
              'Boreal Evergreen Needle-leaved Forest',
              'Boreal Summergreen Needle-leved Forest',
              'Boreal Summergreen Broad-leaved Forest', 'Boreal Woodland',
              'Shrub Tundra', 'Tundra', 'Ocean or Lake']

    fig = plt.figure(figsize=(11.25,10))

    ax = plt.axes(projection=ccrs.PlateCarree())

    levels = np.arange(1,25)
    cmap = mpl.colors.ListedColormap(colors[:], '')
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = mpl.colors.LinearSegmentedColormap.from_list('mcm', cmaplist, cmap.N)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    p = ax.pcolormesh(lons, lats, CRUJRA, cmap=cmap, norm=norm
                      )

    plt.show()

wurst()
