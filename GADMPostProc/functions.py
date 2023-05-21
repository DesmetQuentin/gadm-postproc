#!/bin/usr/python

# GADMPostProc.functions

import geopandas as gpd
import regionmask
import xarray as xr
from .data import *

def country_mask(gadm_dir, code, da, lon='longitude', lat='latitude'):
    return regionmask.Regions(gpd.read_file(f'{gadm_dir}/' + shp_file %(code, code, 0))\
                           .geometry.values).mask(da, lon_name=lon, lat_name=lat)

def region_mask(gadm_dir, code_list, da, lon='longitude', lat='latitude'):
    return xr.merge([country_mask(gadm_dir, code, da, lon, lat) for code in code_list])
