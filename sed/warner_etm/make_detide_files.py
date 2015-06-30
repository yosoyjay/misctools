#!/usr/bin/env python
"""Create detided transect files"""
import os
import glob

import numpy as np

from data import dataContainer as dc
from data import timeSeriesFilters as tsf
from plotting import transectPlot as tsp

import matplotlib.pyplot as plt


def make_detide_transect(file):
    var = dc.dataContainer.loadFromNetCDF(file)
    var_detide = tsf.removeTides(var)
    detide_name = file.replace('_0_', '_detide_0_')
    var_detide.saveAsNetCDF(detide_name)
    return detide_name


def make_detide_files(files):
    detide_files = []
    for f in files:
        print 'Creating detided file for %s' % f
        detide_files.append(make_detide_transect(f))
    return detide_files


def make_plot(detide_files):
    fig = plt.figure()
    dia = tsp.stackTransectPlotDC()

    for f in detide_files:
        data = dc.dataContainer.loadFromNetCDF(f)
        var = data.fieldNames[0]
        dia.addSample(var, data, 0, clabel=var, unit='units')

    dia.showColorBar()
    plt.gcf().savefig('hvel_salt_trcr_detide.png')


def find_files(transect_dir, vars=['salt', 'hvel', 'trcr_1']):
    nested = [glob.glob(os.path.join(transect_dir, '*%s*.nc' % v)) for v in vars]
    files = [item for sublist in nested for item in sublist]
    if len(files) == 0:
        print 'NOTE: 0 files found'
        print 'NOTE: no detided files will be created'
    return files


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to transect directory')
    parser.add_argument('-p', '--plot', action='store_true', help='Create plot of newly created tided files.') 
    args = parser.parse_args()

    print 'Creating detided transect files in %s' % args.path
    files = find_files(args.path)
    dtf = make_detide_files(files)
    if args.plot:
        make_plot(dtf)


if __name__ == '__main__':
    main()

#salt = dc.dataContainer.loadFromNetCDF('./run13/data/transect/Warner_2007_ETM_salt_0_2010-01-01_2010-02-01.nc')
#hvel = dc.dataContainer.loadFromNetCDF('./run13/data/transect/Warner_2007_ETM_hvel_0_2010-01-01_2010-02-01.nc')
#trcr = dc.dataContainer.loadFromNetCDF('./run13/data/transect/Warner_2007_ETM_trcr_1_0_2010-01-01_2010-02-01.nc')
#salt_detide = tsf.removeTides(salt)
#hvel_detide = tsf.removeTides(hvel)
#trcr_detide = tsf.removeTides(trcr)
#salt_detide.saveAsNetCDF('./run13/data/transect/Warner_2007_ETM_salt_detide_0_2010-01-01_2010-02-01.nc')
#hvel_detide.saveAsNetCDF('./run13/data/transect/Warner_2007_ETM_hvel_detide_0_2010-01-01_2010-02-01.nc')
#trcr_detide.saveAsNetCDF('./run13/data/transect/Warner_2007_ETM_trcr_detide_0_2010-01-01_2010-02-01.nc')

#fig = plt.figure()
#dia = tsp.stackTransectPlotDC()
#dia.addSample('hvel', hvel, 0, clabel='hvel', unit='ms')
#dia.addSample('hvel_dt', hvel_detide, 0, clabel='hvel', unit='ms')
#dia.addSample('salt', salt, 0, clabel='salt', unit='psu')
#dia.addSample('salt_dt', salt_detide, 0, clabel='salt', unit='psu')
#dia.addSample('trcr', trcr, 0, clabel='dirt', unit='kg/m3')
#dia.addSample('trcr_dt', trcr_detide, 0, clabel='dirt', unit='kg/m3')
#dia.showColorBar()
#plt.gcf().savefig('hvel_salt_trcr.png')
