#!/bin/usr/python3

# GADMPostProc.functions
#
# quentin.desmet@cnrs.fr
# last update: 2023-05-22

import xarray as xr
import geopandas as gpd
import regionmask
from .data import *

# Return a xarray.DataArray containing the mask based on the provided code
# (see data.code2country for country name correspondance) and on the grid
# of the xarray.DataArray da, with longitude and latitude coordinate names
# given with lon and lat.
# gadm_dir is the path where to find this package.
def country_mask(gadm_dir, code, da, lon='longitude', lat='latitude'):
    return regionmask.Regions(gpd.read_file(f'{gadm_dir}/' + shp_file %(code, code, 0))\
                           .geometry.values).mask(da, lon_name=lon, lat_name=lat)

# Return a xarray.DataArray containing the mask based on the provided list of codes
# (see data.code2country for country name correspondance) and on the grid
# of the xarray.DataArray da, with longitude and latitude coordinate names
# given with lon and lat.
# gadm_dir is the path where to find this package.
def region_mask(gadm_dir, code_list, da, lon='longitude', lat='latitude'):
    return xr.merge([country_mask(gadm_dir, code, da, lon, lat) for code in code_list])
