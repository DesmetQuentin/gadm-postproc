#!/bin/usr/python

import sys
import xarray as xr
import numpy as np
import os.path
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
import regionmask
import fiona
fiona.drvsupport.supported_drivers['KML'] = 'rw'

sys.path.append('/home/desq/work/DesmetNgoDuc_ranking')

import DesmetNgoDuc as dnd
import GADMPostProc as gadm

# -------------------- #
# Variable definitions #
# -------------------- #
# Miscellaneous:
year = 2018
fn_out = 'statistics/statistics_%s.%s.%s.nc' # variable year reference
path_to_GADM = '.'
google_earth_file = 'SEA_seas.kml'
landuse_file = '../CORE3K41_DOMAIN000.nc'

# Strings: _*
_year      = str(year)

_run       = 'Run'

_kind1     = 'Metrics A' # for NSTD & CC
_kind2     = 'Metric B' # for B
_kind3     = 'Metrics C' # for wind (?)

_subregion = 'Subregion'
_lidc      = 'IDC' #'Indochina' # land areas
_lmac      = 'MAC' #'Maritime Continent'
_lpht      = 'PHT' #'Philippines and Taiwan'
_laus      = 'AUS' #'Australia'
_oswo      = 'SWO' #'South West Ocean' # ocean areas
_oscs      = 'SCS' #'South China Sea'
_oequ      = 'EQU' #'Indonesian seas'
_oneo      = 'NEO' #'North East Ocean'

_season    = 'Season'
_djf       = 'DJF' #'Winter'
_mam       = 'MAM' #'Spring'
_jja       = 'JJA' #'Summer'
_son       = 'SON' #'Fall'

_aspect2   = 'Dimension'
_tem       = 'Temporal'
_spa       = 'Spatial'

_aspect1   = 'Aspect'
_var       = 'Variability'
_bia       = 'Systematic bias'

_variable  = 'Variable'

# Lists and dictionaries
var2pro = {
	'hfls': 'ECMWF', 
	'hfss': 'ECMWF', 
	'rsns': 'CERES', 
	'rsus': 'CERES', 
	'rsds': 'CERES', 
	'rsnl': 'CERES', 
	'rlus': 'CERES', 
	'rlds': 'CERES', 
	'rsnscl': 'CERES', 
	'rlntpcs': 'CERES', 
	'rsdt': 'CERES', 
	'rsut': 'CERES', 
	'rlut': 'CERES', 
	'rtnscl': 'CERES', 
	'rtnlcl': 'CERES', 
	'pr': 'CMORPH', 
	'tas': 'ECMWF', 
	'wind_speed_850': 'ERA5', 
	'ua_850': 'ERA5', 
	'va_850': 'ERA5', 
	'sfcWind': 'WindSat_aw', 
	'uas': 'WindSat_aw', 
	'vas': 'WindSat_aw', 
	'clt': 'CERES', 
	'clwvi': 'WindSat', 
	'prw': 'AMSR', 
	'prc': 'ERA5', 
	'tau2': 'SYM1', 
	'tauu': 'SYM1', 
	'tauv': 'SYM1', 
	'sst': 'OSTIA', 
	}

country_lists = {
        _lidc: ['BGD', 'BTN', 'CHN', 'HKG', 'IND', 'KHM', 'LAO', 'LKA', 'MMR', 'NPL', 'THA', 'VNM'],
        _lmac: ['BRN', 'COK', 'CXR', 'IDN', 'MYS', 'PLW', 'PNG', 'SGP', 'SLB', 'TLS'],
        _lpht: ['PHL', 'TWN'],
        _laus: ['AUS'],
        }

# --------- #
# Functions #
# --------- #
def init_run_list():
	keys = []
	'''
	for c in [4, 5, 6]:
		for m in [1, 2]:
			for b in [1, 2]:
				keys.append('41_3%i%i%i0' %(c, m, b))
	for kz in [23, 30, 35]:
		keys.append('%i_35220' %(kz))
	keys += ['18_35220']
	keys += ['41_35221']
	keys += ['41_35220_iconvlwp']
	keys += ['41_35220_totcl']
	'''
	keys += ['23_35220']
	for cf in [0]: #, 1]:
		for c in [4, 5, 6]:
			for m in [1]: #, 2]:
				for b in [1]: #, 2]:
					if not (cf == 0 and m == 2):
						keys.append('41_3%i%i%i%i' %(c, m, b, cf))
						keys.append('41_3%i%i%i%iR' %(c, m, b, cf))
	'''
	#keys += ['Frcd_OSTIA', 'Frcd_SYM1.1', 'Cpld_SYM1.1']
	keys += ['Cpld_SYM1.1']
	'''
	return keys

def seasonally(ds, seasonKey = None, seasonKeys = None):
    # Make a DataArray with the number of days in each month, size = len(time)
    month_length = ds.time.dt.days_in_month

    # Calculate the weights by grouping by 'time.season'
    weights = (month_length.groupby('time.season') / month_length.groupby('time.season').sum())

    # Test that the sum of the weights for each season is 1.0
    np.testing.assert_allclose(weights.groupby('time.season').sum().values, np.ones(4))

    # Calculate the weighted average
    res = (ds * weights).groupby('time.season').sum(dim='time')

    # Name adjustments
    if not (seasonKey or seasonKeys):
        return res
    elif seasonKey and not seasonKeys:
        return res.rename({'season': seasonKey})
    elif seasonKeys and not seasonKey:
        return res.assign_coords({'season': seasonKeys})
    else:
        return res.rename({'season': seasonKey}).assign_coords({seasonKey: seasonKeys})

def build_masks(da, grid, lonlat = ['longitude', 'latitude']):
    # Make land subregion mask for key, agreeing with the RegCM land mask rcm_mask.
    #   inArea is necessary to make the masks compatible with rcm_mask.
    #   It must be xarray boolean to setup the largest area containing only land
    #   from the desired subregion.
    def GADMxRCM_lregion_mask(key, rcm_mask, inArea):
        ## Make original mask from the GADM shapefiles
        gadm_mask = gadm.region_mask(path_to_GADM, country_lists[key], rcm_mask,
                                 'xlon', 'xlat').mask
        ## Turn NaN into 0, 0 into 1
        mask1 = xr.where(gadm_mask == 0, 1, 0)
        ## Force ocean areas of RegCM to be also ocean in the resulting mask
        mask2 = xr.where(rcm_mask == 0, 0, mask1)
        ## Where RegCM sees land in the area of interest, but not GADM, fit RegCM
        diff = rcm_mask - mask2
        mask3 = xr.where(inArea & (diff == 1), 1, mask2)
        ## Turn back 0 to NaN
        mask4 = xr.where(mask3 == 1, mask3, np.nan)
        ## Provide attributes
        return mask4.assign_attrs({
                        'units': '1',
                        'coordinates': 'xlat xlon',
                        'grid_mapping': 'crs',
                        })

    # Make land subregion mask for key on the grid of da.
    def GADM_lregion_mask(key, da):
        ## Make original mask from the GADM shapefiles
        gadm_mask = gadm.region_mask(path_to_GADM, country_lists[key], da,
                                lonlat[0], lonlat[1]).mask
        ## Turn 0 into 1
        mask = xr.where(gadm_mask == 0, 1, gadm_mask)
        ## Provide attributes
        return mask.assign_attrs({
                        'units': '1',
                        'coordinates': f'{lonlat[1]} {lonlat[0]}',
                        })

    # Add ocean subregion masks to the dictionary res.
    def add_oregion_masks(res):
        ## Deduct the land mask from the subregions
        land_mask = xr.where((masks[_lidc] == 1) | (masks[_lpht] == 1) | (masks[_laus] == 1) | (masks[_lmac] == 1), 1, 0)
        if grid == '': # if it's on the RegCM grid, then link land_mask with xlon and xlat
            land_mask = land_mask.assign_coords(dict(xlon = lon, xlat = lat))
        ## Make original masks from the Google Earth polygons in google_earth_file (.kml)
        kml = gpd.read_file(google_earth_file, driver='KML') # read data
        polygons3D = dict(zip(list(kml['Name']), list(kml.geometry.values))) # shape it conveniently
        polygons2D = {key: Polygon([(x, y) for x, y, z in value.exterior.coords])\
                                           for key, value in polygons3D.items()} # remove the altitude
        tmp = {key: regionmask.Regions([value]).mask(land_mask, lon_name = 'xlon', lat_name = 'xlat')\
                                           for key, value in polygons2D.items()} # make masks
        tmp2 = {key: xr.where(value == 0, 1, value)\
                                           for key, value in tmp.items()} # turn 0 into 1
        ## Fill in the mask dictionary. Subregions were drawn on Google Earth with overlapping, 
        ##   such that SWO is itself without the intersection with SCS (which was drawn first),
        ##             EQU is itself without the intersection with SCS or SWO,
        ##         and NEO is itself without the intersection with SCS or EQU (no common border with SWO).
        ##   Furthermore, land areas must be removed.
        ### Attributes
        if grid == '': # if it's on the RegCM grid, then...
            res_attrs = {'units': '1', 'coordinates': 'xlat xlon', 'projection': 'crs'}
        else: # otherwise, ...
            res_attrs = {'units': '1', 'coordinates': f'{lonlat[1]} {lonlat[0]}'}
        ### Values
        res[_oscs] = xr.where((tmp2[_oscs] == 1)\
                & (land_mask == 0), 1, np.nan).assign_attrs(res_attrs)
        res[_oswo] = xr.where((tmp2[_oswo] == 1) & (res[_oscs] != 1)\
                & (land_mask == 0), 1, np.nan).assign_attrs(res_attrs)
        res[_oequ] = xr.where((tmp2[_oequ] == 1) & (res[_oscs] != 1) & (res[_oswo] != 1)\
                & (land_mask == 0), 1, np.nan).assign_attrs(res_attrs)
        res[_oneo] = xr.where((tmp2[_oneo] == 1) & (res[_oscs] != 1) & (res[_oequ] != 1)\
                & (land_mask == 0), 1, np.nan).assign_attrs(res_attrs)


    if grid == '': # if it's on the RegCM grid, then...
        # Retrieve RegCM land mask
        ds = xr.open_dataset(landuse_file)
        rcm_landuse = ds.landuse[1:ds.landuse.shape[0]-2, 1:ds.landuse.shape[1]-2]
        rcm_proj = ds.crs
        lon = ds.xlon[1:ds.landuse.shape[0]-2, 1:ds.landuse.shape[1]-2]
        lat = ds.xlat[1:ds.landuse.shape[0]-2, 1:ds.landuse.shape[1]-2]
        ds.close()

        rcm_mask = xr.where(rcm_landuse == 15, 0, 1) # 15 -> ocean, 14 -> inland water

    # Make subregional masks
    ## Land
    if grid == '': # if it's on the RegCM grid, then...
        masks = {}
        ### Make the three firsts with a merge between RegCM land mask and GADM borders
        masks[_lidc] = GADMxRCM_lregion_mask(_lidc, rcm_mask, (lat > 6.6) & (lon < 115))
        masks[_lpht] = GADMxRCM_lregion_mask(_lpht, rcm_mask, (((lat > 8 ) & (lat < 19)) & ((lon >  116) & (lon < 122)))\
                                                            | (((lat > 5 ) & (lat < 19)) & ((lon >= 122) & (lon < 127)))\
                                                            | (((lat > 21) & (lat < 26)) & ((lon >  120) & (lon < 123)))) 
        masks[_laus] = GADMxRCM_lregion_mask(_laus, rcm_mask, (lat < -11) & (lon > 120))
        ### Deduct the Maritime Continent mask from the remaining land without the other subregions
        masks1 = xr.where((rcm_mask == 1) & (masks[_lidc] != 1) & (masks[_lpht] != 1) & (masks[_laus] != 1), rcm_mask, np.nan, keep_attrs=True)
        ### Provide attributes for the Maritime Continent, which has been computed seperatedly
        masks[_lmac] = masks1.assign_attrs({
                        'units': '1',
                        'coordinates': 'xlat xlon',
                        'grid_mapping': 'crs',
                        })
    else: # otherwise, take the direct result from GADM masks
        masks = {key: GADM_lregion_mask(key, da) for key in country_lists.keys()}
    ## Ocean
    add_oregion_masks(masks)

    # Build the subregion xr.DataArray and compute the weights
    ## Initialization
    i = 1
    if grid == '': # if it's on the RegCM grid, then...
        da_subregion = xr.DataArray(np.zeros(rcm_mask.shape), coords={'iy': rcm_mask.coords['iy'], 'jx': rcm_mask.coords['jx']})
    else: # otherwise, ...
        da_subregion = xr.DataArray(np.zeros(da.shape), coords={lonlat[1]: da.coords[lonlat[1]], lonlat[0]: da.coords[lonlat[0]]})
    ## Core
    for key in masks.keys():
        da_subregion = xr.where(masks[key] == 1, i, da_subregion)
        i += 1
    ## Attributes
    da_subregion = da_subregion.assign_attrs({
            'units': '1',
            'coordinates': 'xlat xlon',
            'flag_values': f'{",".join([str(i+1) for i in range(len(masks))])}',
            'flag_meanings': f'{",".join(list(masks.keys()))}',
            })

    # Make the final dataset and export
    if grid == '': # if it's on the RegCM grid, then...
        ds = xr.Dataset({
                _lidc+'_mask': masks[_lidc],
                _lpht+'_mask': masks[_lpht],
                _laus+'_mask': masks[_laus],
                _lmac+'_mask': masks[_lmac],
                _oscs+'_mask': masks[_oscs],
                _oswo+'_mask': masks[_oswo],
                _oequ+'_mask': masks[_oequ],
                _oneo+'_mask': masks[_oneo],
                _subregion: da_subregion,
                'crs': rcm_proj,
                })
    else:
        ds = xr.Dataset({
                _lidc+'_mask': masks[_lidc],
                _lpht+'_mask': masks[_lpht],
                _laus+'_mask': masks[_laus],
                _lmac+'_mask': masks[_lmac],
                _oscs+'_mask': masks[_oscs],
                _oswo+'_mask': masks[_oswo],
                _oequ+'_mask': masks[_oequ],
                _oneo+'_mask': masks[_oneo],
                _subregion: da_subregion,
                })
    ds.to_netcdf(f'subregions{grid}.nc')
    return {key: float(mask.count())/mask.size for key, mask in masks.items()}

if __name__ == '__main__':
    myDa = xr.open_dataset('../mask.nc')
    print(build_masks(myDa, ''))
