#!/bin/usr/python

# GADMPostProc.data

# Alpa-3 code to English short name mapping
## Based on https://www.iso.org/obp/ui/#search/code/
## Accessed on May, the 20th of 2023
code2country = {
        'AUS': 'Australia',
        'BGD': 'Bangladesh',
        'BRN': 'Brunei Darussalam',
        'BTN': 'Bhutan',
        'CHN': 'China',
        'COK': 'Cook Islands (the)',
        'CXR': 'Christmas Island',
        'HKG': 'Hong Kong',
        'IDN': 'Indonesia',
        'IND': 'India',
        'KHM': 'Cambodia',
        'LAO': "Lao People's Democratic Republic (the)",
        'LKA': 'Sri Lanka',
        'MMR': 'Myanmar',
        'MYS': 'Malaysia',
        'NPL': 'Nepal',
        'PHL': 'Philippines (the)',
        'PLW': 'Palau',
        'PNG': 'Papua New Guinea',
        'SGP': 'Singapore',
        'SLB': 'Solomon Islands',
        'THA': 'Thailand',
        'TLS': 'Timor-Leste',
        'TWN': 'Taiwan (Province of China)',
        'VNM': 'Viet Nam',
        }

# Provide the maximum precision available
maxPrecision = {
        'AUS': 2, 
        'BGD': 4, 
        'BRN': 2, 
        'BTN': 2, 
        'CHN': 3, 
        'COK': 0, 
        'CXR': 0, 
        'HKG': 1, 
        'IDN': 4, 
        'IND': 3, 
        'KHM': 4, 
        'LAO': 2, 
        'LKA': 2, 
        'MMR': 3, 
        'MYS': 2, 
        'NPL': 4, 
        'PHL': 3, 
        'PLW': 1, 
        'PNG': 2, 
        'SGP': 1, 
        'SLB': 2, 
        'THA': 3, 
        'TLS': 3, 
        'TWN': 2, 
        'VNM': 3, 
        }

# Shapefiles' name format
shp_file = 'gadm36_%s_shp/gadm36_%s_%i.shp' # %(code, code, precision)
