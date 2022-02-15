#!/usr/bin/env python
u"""
read_ee_phase.py
Written by Enrico Ciraci' (02/2022)

Compute the complex difference between two coregistered interferograms.

usage: read_ee_phase.py [-h] [--directory DIRECTORY]
       [--outdir OUTDIR] reference secondary

TEST: Compute the complex difference between two coregistered interferograms.

positional arguments:
  reference    Reference Interferogram.
  secondary    Secondary Interferogram.

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -D DIRECTORY
                        Project data directory.
  --outdir OUTDIR, -O OUTDIR
                        Output directory.


PYTHON DEPENDENCIES:
    argparse: Parser for command-line options, arguments and sub-commands
           https://docs.python.org/3/library/argparse.html
    datetime: Basic date and time types
           https://docs.python.org/3/library/datetime.html
    rasterio: access to geospatial raster data
           https://rasterio.readthedocs.io
    matplotlib: Visualization with Python
           https://matplotlib.org/

UPDATE HISTORY:

"""
# - Python Dependencies
from __future__ import print_function
import os
import argparse
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from utils.raster_io import load_raster
from utils.make_dir import make_dir


def add_colorbar(fig: plt.figure(), ax: plt.Axes,
                 im: plt.pcolormesh) -> plt.colorbar:
    """
    Add colorbar to the selected plt.Axes
    :param fig: plt.figure object
    :param ax: plt.Axes object
    :param im: plt.pcolormesh object
    :return: plt.colorbar
    """
    divider = make_axes_locatable(ax)
    cax = divider.new_vertical(size='5%', pad=0.6, pack_start=True)
    fig.add_axes(cax)
    cb = fig.colorbar(im, cax=cax, orientation='horizontal')
    return cb


def main():
    parser = argparse.ArgumentParser(
        description="""TEST: Compute the complex difference between two
        coregistered interferograms."""
    )
    # - Reference Interferogram
    parser.add_argument('reference', type=str,
                        help='Reference Interferogram.')
    # - Secondary Interferogram
    parser.add_argument('secondary', type=str,
                        help='Secondary Interferogram.')

    # - Absolute Path to directory containing input data.
    default_dir = os.path.join('/', 'Volumes', 'Extreme Pro',
                               'Peterman_glacier_X7_subset')
    parser.add_argument('--directory', '-D',
                        type=lambda p: os.path.abspath(os.path.expanduser(p)),
                        default=default_dir,
                        help='Project data directory.')
    # - Output directory
    parser.add_argument('--outdir', '-O',
                        type=str,  default='output_test',
                        help='Output directory.')
    args = parser.parse_args()

    # - Test Files/Volumes/Extreme Pro/Peterman_glacier_X7_subset
    file_1 = args.reference + '.tif'
    file_2 = args.secondary + '.tif'

    # - Extract Interferogram name from file name
    name_1 = file_1.replace('ICEYE-phase_geo-', '')[:17]
    name_2 = file_2.replace('ICEYE-phase_geo-', '')[:17]

    # - Load InSAR phase
    # - Input interferogram 1
    d_inter1_input = load_raster(os.path.join(args.directory, file_1))
    interf_1 = d_inter1_input['data']

    # - Input interferogram 2
    d_inter2_input = load_raster(os.path.join(args.directory, file_2))
    interf_2 = d_inter2_input['data']

    # - Convert interferometric phase [-pi, +pi] to complex polar format
    cmp_phase_1 = np.exp(1j * interf_1)
    cmp_phase_2 = np.exp(1j * interf_2)

    # - Compute Differential Interferogram
    dd_phase_complex = np.angle(cmp_phase_1 * np.conj(cmp_phase_2))

    # - Create Output directory
    out_dir = make_dir(args.directory, args.outdir)

    # - Output figure parameters
    fig_size = (15, 5)
    fig_format = 'jpeg'
    dpi = 200
    # - Initialize figure object
    fig = plt.figure(figsize=fig_size, dpi=dpi)
    # - Input Interferogram 1
    ax_1 = fig.add_subplot(1, 3, 1)
    ax_1.set_title(name_1, weight='bold')
    im_1 = ax_1.imshow(interf_1, vmin=-np.pi, vmax=np.pi,
                       cmap=plt.get_cmap('jet'))
    ax_1.grid(color='k', linestyle='dotted', alpha=0.3)
    cb_1 = add_colorbar(fig, ax_1, im_1)
    cb_1.set_label(label='Rad', weight='bold')
    cb_1.ax.tick_params(labelsize='medium')
    cb_1.ax.set_xticks([-np.pi, 0, np.pi])
    cb_1.ax.set_xticklabels(['-$\pi$', '0', r'$\pi$'])

    # - Input Interferogram 2
    ax_2 = fig.add_subplot(1, 3, 2)
    ax_2.set_title(name_2, weight='bold')
    im_2 = ax_2.imshow(interf_2, vmin=-np.pi, vmax=np.pi,
                       cmap=plt.get_cmap('jet'))
    ax_2.grid(color='k', linestyle='dotted', alpha=0.3)
    cb_2 = add_colorbar(fig, ax_2, im_2)
    cb_2.set_label(label='Rad', weight='bold')
    cb_2.ax.tick_params(labelsize='medium')
    cb_2.ax.set_xticks([-np.pi, 0, np.pi])
    cb_2.ax.set_xticklabels(['-$\pi$', '0', r'$\pi$'])

    # - Differential Interferogram
    ax_3 = fig.add_subplot(1, 3, 3)
    ax_3.set_title('Double Difference', weight='bold')
    im_3 = ax_3.imshow(dd_phase_complex, vmin=-np.pi, vmax=np.pi,
                       cmap=plt.get_cmap('jet'))
    ax_3.grid(color='k', linestyle='dotted', alpha=0.3)
    cb_3 = add_colorbar(fig, ax_3, im_3)
    cb_3.set_label(label='Rad', weight='bold')
    cb_3.ax.tick_params(labelsize='medium')
    cb_3.ax.set_xticks([-np.pi, 0, np.pi])
    cb_3.ax.set_xticklabels(['-$\pi$', '0', r'$\pi$'])

    plt.tight_layout()
    plt.savefig(
        os.path.join(out_dir, f'{name_1}-{name_2}.' + fig_format),
        dpi=dpi, format=fig_format)
    plt.close()


# - run main program
if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'# - Computation Time: {end_time - start_time}')
