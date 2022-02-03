#!/usr/bin/env python
u"""
reproject_dem_rasterio.py
Written by Enrico Ciraci' (08/2021)

Reproject TanDEM-X DEMs from their native projection [EPSG:4326] to the selected
new coordinate reference system.
Use GDAL (Geospatial Data Abstraction Library) Python bindings provided by the
Rasterio project to apply the reprojection/interpolation.
Rasterio provides more Pythonic ways to access GDAL API if compared to the
standard GDAL Python Binding.
(https://rasterio.readthedocs.io)

COMMAND LINE OPTIONS:
    --directory X, -D X: Project data directory.
    --outdir X, -O X: Output Directory.
    --crs X, -C X: Destination Coordinate Reference System - def.EPSG:3413
    --res X, -R X: Output raster Resolution. - def. 50 meters.
    --resampling_alg X: Warp Resampling Algorithm. - def. bilinear

The complete list of the available warp resampling algorithms can be found here:
https://rasterio.readthedocs.io/en/
      latest/api/rasterio.enums.html#rasterio.enums.Resampling

Note: This preliminary version of the script has been developed to process
      TanDEM-X data available between 2011 and 2020 for the area surrounding
      Petermann Glacier (Northwest Greenland).

PYTHON DEPENDENCIES:
    argparse: Parser for command-line options, arguments and sub-commands
           https://docs.python.org/3/library/argparse.html
    rasterio: access to geospatial raster data
           https://rasterio.readthedocs.io
    geopandas: extends the datatypes used by pandas to allow spatial operations
           on geometric types/ geospatial data.
           https://geopandas.org
    tqdm: A Fast, Extensible Progress Bar for Python and CLI
           https://tqdm.github.io

UPDATE HISTORY:

"""
# - Python Dependencies
from __future__ import print_function
import os
import argparse
from datetime import datetime


def main():
    # - Set Path to Project Data Directory
    data_dir = os.path.join('/', 'Volumes', 'GoogleDrive',
                            'My Drive', 'Peterman_glacier_X7_subset')
    # -
    print(data_dir)


# - run main program
if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'# - Computation Time: {end_time - start_time}')
