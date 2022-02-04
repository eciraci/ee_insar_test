"""
Enrico Ciraci 02/2022
"""
# - python dependencies
from __future__ import print_function
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib_scalebar.scalebar import ScaleBar
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def plot_interf_map(infer: np.array, x_centroids: np.array,
                    y_centroids: np.array, cmap: plt = plt.get_cmap('jet'),
                    ice_color: str = 'k'):

    # - Not Editable Parameters
    map_extent = [-61.1, -59.9, 80.4, 81.2]
    figsize = (6, 9)
    label_size = 12

    # - Path to Glaciers Mask
    ics_shp = os.path.join('.', 'esri_shp',
                           'Petermann_Domain_glaciers_epsg3413.shp')

    # - set Coordinate Reference System
    ref_crs = ccrs.NorthPolarStereo(central_longitude=-45,
                                    true_scale_latitude=70)
    # - Initialize figure object
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1, projection=ref_crs)
    # - Set map extent
    ax.set_extent(map_extent, crs=ccrs.PlateCarree())
    # - Set Map Grid
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False,
                      y_inline=False, color='k', linestyle='dotted',
                      alpha=0.3)
    gl.top_labels = False
    gl.bottom_labels = True
    gl.right_labels = False
    gl.xlocator \
        = mticker.FixedLocator(np.arange(np.floor(map_extent[0]) - 3.5,
                                         np.floor(map_extent[1]) + 3, 1))
    gl.ylocator \
        = mticker.FixedLocator(np.arange(np.floor(map_extent[2]) - 5,
                                         np.floor(map_extent[3]) + 5, 0.2))
    gl.xlabel_style = {'rotation': 0, 'weight': 'bold', 'size': label_size}
    gl.ylabel_style = {'rotation': 0, 'weight': 'bold', 'size': label_size}
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # - Plot Glaciers Mask
    shape_feature = ShapelyFeature(Reader(ics_shp).geometries(),
                                   crs=ref_crs)
    ax.add_feature(shape_feature, facecolor='None', edgecolor=ice_color)

    # - Plot Interferogram
    xx, yy = np.meshgrid(x_centroids, y_centroids)
    im = ax.pcolormesh(x_centroids, y_centroids, infer, cmap=cmap,
                       zorder=0, vmin=-np.pi, vmax=np.pi,
                       rasterized=True)

    # add an axes above the main axes.
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size='5%', pad=0.1, axes_class=plt.Axes)
    fig.add_axes(ax_cb)
    cb = plt.colorbar(im, cax=ax_cb)
    cb.ax.tick_params(labelsize='medium')
    plt.show()

