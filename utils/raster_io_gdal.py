#!/usr/bin/env python
"""
Enrico Ciraci 02/2022.

For more info about GDAL/OGR in Python see:
https://gdal.org/api/python.html
"""
import numpy as np
from osgeo import gdal
from osgeo import osr


def read_geotiff(input_geo_tif: str) -> dict:
    """
    Import Raster file saved in Geotiff format employing
    GDAL Python binding
    :param input_geo_tif: absolute path to the input geotiff archive
    :return: dictionary containing raster as numpy array + crs parameters.
    """
    dataset = gdal.Open(input_geo_tif)
    dataset.GetRasterBand(1).Checksum()
    if gdal.GetLastErrorType() != 0:
        raise AttributeError
    # - extract raster info
    cols = dataset.RasterXSize  # - number of columns
    rows = dataset.RasterYSize  # - number of rows
    # - get layer band info
    src_band = dataset.GetRasterBand(1)
    # - get raster Coordinate Reference System
    projection = dataset.GetProjection()
    proj = osr.SpatialReference(wkt=projection)
    crs = int(proj.GetAttrValue('AUTHORITY', 1))
    no_val = src_band.GetNoDataValue()
    geotransform = dataset.GetGeoTransform()
    origin_x = geotransform[0]          # - x-axis first value
    origin_y = geotransform[3]          # - y-axis first value
    pixel_width_x = geotransform[1]     # - pixel width
    pixel_width_y = geotransform[5]     # - pixel height
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize
    # - import raster layer as a numpy array
    data = src_band.ReadAsArray(0, 0, cols, rows)
    # - close input raster
    dataset = None
    # - define x and y-axis
    x_axis = np.arange(origin_x, origin_x + (cols * pixel_width_x),
                       pixel_width_x)
    y_axis = np.arange(origin_y, origin_y + (rows * pixel_width_y),
                       pixel_width_y)
    # - Upper Left Corner
    ul_corner = (origin_x, origin_y)
    # - Lower Right Corner
    lr_corner = (x_axis[-1]+pixel_width_x, y_axis[-1]+pixel_width_y)

    return{'data': data, 'nodata': no_val, 'projection': projection,
           'ul_corner': ul_corner, 'lr_corner': lr_corner,
           'xres': pixel_width_x, 'yres': pixel_width_y,
           'xsize': xsize, 'ysize': ysize,
           'x_axis': x_axis, 'y_axis': y_axis,
           'geotransform': geotransform, 'crs': crs}


def write_geotiff(raster_data: np.ndarray, x_min: float, y_max: float,
                  dst_filename: str, pixel_size: float = 5.,
                  epsg: int = 3413, no_val: int = -9999) -> None:
    """ - Convert and input array to a raster file. """
    cols = raster_data.shape[1]   # - array number of columns
    rows = raster_data.shape[0]   # - array number of rows
    origin_x = x_min    # - array upper left corner x-coord
    origin_y = y_max    # - array upper left corner y-coord
    driver = gdal.GetDriverByName('GTiff')  # - output data format
    # - create raster file
    out_raster = driver.Create(dst_filename, cols, rows, 1,
                               gdal.GDT_Float32)
    out_raster.SetGeoTransform((origin_x, pixel_size, 0,
                                origin_y, 0, -pixel_size))
    outband = out_raster.GetRasterBand(1)
    outband.WriteArray(raster_data)
    outband.SetNoDataValue(no_val)
    # - define coordinate reference system
    out_raster_srs = osr.SpatialReference()
    # - use EPGS3413 crs by default
    out_raster_srs.ImportFromEPSG(epsg)
    out_raster.SetProjection(out_raster_srs.ExportToWkt())
    # - write output file on disk
    outband.FlushCache()


def clip_raster(src_file: str, ref_shp: str, out_file: str) -> None:
    """
    Clip Input Raster using GDAL WARP. Find more info hre:
    https://gdal.org/python/
    :param src_file: absolute path to input raster file
    :param ref_shp: absolute path to reference shapefile
    :param out_file: absolute path to output raster file
    :return: None
    """
    out_tile = gdal.Warp(out_file, src_file, cutlineDSName=ref_shp,
                         cropToCutline=True,  dstNodata=-9999)
    out_tile = None
