# Using GADM shapefiles
[GADM website] is at version 4.1 as of May, 2023. However, I couldn't make use of the download links for this version and I also noticed that the license is dated from 2022. I therefore used the links I got from version 3.6, which are fine already.

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
The python package `GADMPostProc` is here to get started with the data. It requires `xarray`, `geopandas`, and `regionmask`; an example is provided with `example.py`. The package doesn't use it, but during your work, you might also need `shapely.geometry` to deal with `Polygon`. Nevertheless, *how-to-use* information is given right here. In your python code header, add:

```python
import sys

sys.append('/path/to/this/directory')
import GADMPostProc as gadm
```

Then:
- `gadm.code2country['code']` returns the related English short name;
- `gadm.maxPrecision['code']` returns the maximum level ID for this country (I only filled in with South East Asian countries so far, if you have the information because you have been downloading new data, please add it to the dictionary then create a merge request to share it with everyone);
- `gadm.shp_file('code', 0)` returns the shapefile's path for this country at level 0;
- `gadm.country_mask('code', da, lon, lat)` returns a xarray.DataArray containing this country mask (see `GADMPostProc/functions.py` for details);
- `gadm.region_mask(['code1', 'code2', ...], da, lon, lat)`  returns a merge of all masks for the provided list of codes (see `GADMPostProc/functions.py` for details).

## Author
Quentin Desmet: quentin.desmet@cnrs.fr

[GADM website]: https://gadm.org/data.html
