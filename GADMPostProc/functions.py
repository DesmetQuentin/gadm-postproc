#!/bin/usr/python3

# GADMPostProc.functions
#
# quentin.desmet@cnrs.fr

import xarray as xr
import geopandas as gpd
import regionmask
from .data import *

# Return a xarray.DataArray containing the mask based on the provided code
# (see data.code2country for country name correspondance) and on the grid
# of the xarray.DataArray da, with longitude and latitude coordinate names
# given with lon and lat.
def country_mask(code, da, lon='longitude', lat='latitude'):
    mask = regionmask.Regions(gpd.read_file(shp_file(code, 0))\
                .geometry.values).mask(da, lon_name=lon, lat_name=lat) + 1
    return (mask/mask).round()

# Return a xarray.DataArray containing the mask based on the provided list of codes
# (see data.code2country for country name correspondance) and on the grid
# of the xarray.DataArray da, with longitude and latitude coordinate names
# given with lon and lat.
def region_mask(code_list, da, lon='longitude', lat='latitude'):
    return xr.merge([country_mask(code, da, lon, lat) for code in code_list]).mask
