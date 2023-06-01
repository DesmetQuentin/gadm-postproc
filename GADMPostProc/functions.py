#!/usr/bin/env python3

"""
GADMPostProc.functions.py

author: Quentin Desmet
contact: quentin.desmet@univ-tlse3.fr
"""

import xarray as xr

def country_mask(code, da, lon='longitude', lat='latitude'):
    """
    Return a xarray.DataArray containing the mask based on the provided code
    (see data.code2country for country name correspondance) and on the grid
    of the xarray.DataArray da, with longitude and latitude coordinate names
    given with lon and lat.
    """
    import geopandas as gpd
    import regionmask
    from .data import *

    mask = regionmask.Regions(gpd.read_file(shp_file(code, 0))\
                .geometry.values).mask(da, lon_name=lon, lat_name=lat) + 1
    return (mask/mask).round()

def region_mask(code_list, da, lon='longitude', lat='latitude'):
    """
    Return a xarray.DataArray containing the mask based on the provided list of codes
    (see data.code2country for country name correspondance) and on the grid
    of the xarray.DataArray da, with longitude and latitude coordinate names
    given with lon and lat.
    """
    return xr.merge([country_mask(code, da, lon, lat) for code in code_list]).mask
