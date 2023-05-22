# Using GADM shapefiles

## What for?
This can be useful to make country/several countries/province masks,
or simply draw related borders.

## How?
1. Check out `GADMPostProc/data.py` to determine the country codes you want to get the data of;
2. Adequately customize the `url_*.txt` file, and `download_*.sh` if necessary (the current example is with South Eastern Asian countries);
3. Run: `bash download_*.sh` and wait for the download to be completed (GADM's licence will be downloaded as well);
4. Data should be ready to use (see **Python**).
**N.B.** The levels' IDs (between 0 and 3 or 4) corresponds to the depth of the territory divisions in the shapefiles, **not** to a difference in border refinement. For instance, the level 0 will only contain the country borders, the level 1 the provinces, etc.

## Python
A python package is here to get started with the data. It requires `xarray`, `geopandas`, and `regionmask`. The package doesn't use it, but during your work, you might also need `shapely.geometry` to deal with `Polygon`. In your python code header, add:

```python
import sys
GADM_dir = '/path/to/this/directory/'
sys.append(GADM_dir)
import GADMPostProc as gadm
```

Then:
- `gadm.code2country['code']` returns the related English short name;
- `gadm.maxPrecision['code']` returns the maximum level ID for this country (only filled in with South East Asian countries so far);
- `GADM_dir + gadm.shp_file %('code', 'code', 0)` returns the shapefile's name for this country at level 0;
- `gadm.country_mask(GADM_dir, 'code', da, lon, lat)` returns a xarray.DataArray containing this country mask (see `GADMPostProc/functions.py` for arguments' details);
- `gadm.region_mask(GADM_dir, ['code1', 'code2', ...], da, lon, lat)`  returns a merge of all masks for the provided list of codes (see `GADMPostProc/functions.py` for arguments' details).
