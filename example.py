#!/bin/usr/python

import sys
import xarray as xr
import numpy as np
import os.path
import matplotlib.pyplot as plt

sys.path.append('/tmpdir/desmet/py/DesmetNgoDuc_ranking')
sys.path.append('/gpfs/work/p20055/desmet/DATA/GADM')
sys.path.append('/users/p20055/desmet/oasis/post_proc')
sys.path.append('/gpfs/work/p20055/desmet/DATA/py')

import DesmetNgoDuc as dnd
import GADMPostProc as gadm
from fn_run_monthly import *
from data_SEA25_monthly import *

# -------------------- #
# Variable definitions #
# -------------------- #
# Miscellaneous:
year = 2018
fn_out = 'statistics/statistics_%s.%s.%s.nc' # variable year reference
path_to_GADM = '/gpfs/work/p20055/desmet/DATA/GADM'
regcm_mask = '/tmpdir/desmet/regcm_run/v5_era5_sym/output_41_35221R/CORE3K41_MSF.2018010100.nc'

# Strings: _*
_year      = str(year)

_run       = 'Run'

_kind1     = 'Metrics A' # for NSTD & CC
_kind2     = 'Metric B' # for B
_kind3     = 'Metrics C' # for wind (?)

_subregion = 'Subregion'
_lind      = 'Indochina' # land areas
_lmar      = 'MaritimeContinent'
_lphi      = 'Philippines'
_laus      = 'Australia'
_oind      = 'IndianOcean' # ocean areas
_oscs      = 'SouthChinaSea'
_oequ      = 'IndonesianSeas'
_ophi      = 'PhilippineSea'

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
        _lind: ['BGD', 'BTN', 'CHN', 'HKG', 'IND', 'KHM', 'LAO', 'LKA', 'MMR', 'NPL', 'THA', 'VNM'],
        _lmar: ['BRN', 'COK', 'CXR', 'IDN', 'MYS', 'PLW', 'PNG', 'SGP', 'SLB', 'TLS'],
        _lphi: ['PHL', 'TWN'],
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

def build_masks():
    # Retrieve RegCM land mask
    rcm_ds = xr.open_dataset(regcm_mask)
    rcm_mask = rcm_ds.mask # 2 -> land, 0 -> ocean
    rcm_proj = rcm_ds.crs
    rcm_ds.close()

    # Make GADM subregional masks
    gadm_masks = {key: gadm.region_mask(path_to_GADM, value, rcm_mask,
                  'xlon', 'xlat').mask for key, value in country_lists.items()}

    # Compatibility
    for key, gadm_mask in gadm_masks.items():
        mask = gadm_mask * rcm_mask
        ds = xr.Dataset({
                'mask': xr.where(np.isnan(mask), mask, 1),
                'crs': rcm_proj,
                })
        ds.to_netcdf(f'mask_{key}.nc')
        ds = xr.Dataset({
                'difference': xr.where(np.isnan(mask), 0, mask)\
                            - rcm_mask,
                'crs': rcm_proj,
                })
        ds.to_netcdf(f'mask_{key}_difference.nc')

build_masks()
