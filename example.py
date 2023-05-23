#!/bin/usr/python3

# Prerequisite: having downloaded SEA data by running `bash download_SEA.sh`

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import GADMPostProc as gadm

# Let's create a mask for isolating countries from the Maritime Continent
Maritime_Continent = [
    'BRN', # Brunei
    'CCK', # Cocos or Keeling Islands
    'CXR', # the Christmas Island
    'IDN', # Indonesia
    'MYS', # Malaysia
    'PNG', # Papua New Guinea
    'SGP', # Singapore
    'SLB', # Solomon Islands
    'TLS', # Timor Leste
    ]

np.random.seed(0)
# Let's create the xarray.DataArray corresponding to the grid we want
## One coarse but broad
coarse_lon, coarse_lat = np.arange(90, 160, .5), np.arange(-15, 10, .5)
coarse_tem = 25 + 4 * np.random.randn(coarse_lat.size, coarse_lon.size)
coarse_da = xr.DataArray(data=coarse_tem, dims=('coarse_lat', 'coarse_lon', ),
                         coords={'coarse_lat': coarse_lat, 'coarse_lon': coarse_lon})

## One fine, centered on the Christmas Island
fine_lon, fine_lat = np.arange(105, 106, .01), np.arange(-11, -10, .01)
fine_tem = 25 + 4 * np.random.randn(fine_lat.size, fine_lon.size)
fine_da = xr.DataArray(fine_tem, dims=('fine_lat', 'fine_lon',),
                       coords={'fine_lat': fine_lat, 'fine_lon': fine_lon})

# Then call the right function
coarse_mask = gadm.region_mask(Maritime_Continent, coarse_da, lon='coarse_lon', lat='coarse_lat')
print(coarse_mask[30])
#fine_mask = gadm.region_mask(Maritime_Continent, fine_da, lon='fine_lon', lat='fine_lat')
#
## Plotting
#fig = plt.figure()
#ax1 = fig.add_subplot(221)
#ax1.pcolormesh(coarse_lon, coarse_lat, coarse_da)
#ax1.set_title('Original data (coarse)')
#ax1.set_ylabel('Latitude')
#
#ax2 = fig.add_subplot(222)
#ax2.pcolormesh(fine_lon, fine_lat, fine_da)
#ax2.set_title('Original data (fine)')
#
#ax3 = fig.add_subplot(223)
#ax3.pcolormesh(coarse_lon, coarse_lat, coarse_da*coarse_mask)
#ax3.set_title('Masked data (coarse)')
#ax3.set_xlabel('Longitude')
#ax3.set_ylabel('Latitude')
#
#ax4 = fig.add_subplot(224)
#ax4.pcolormesh(fine_lon, fine_lat, fine_da*fine_mask)
#ax4.set_title('The Christmas Island with a fine mask')
#ax4.set_xlabel('Longitude')
#
#plt.subplots_adjust(hspace=0.6, wspace=0.4)
#plt.show()
