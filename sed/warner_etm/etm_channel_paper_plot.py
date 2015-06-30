#!/usr/bin/env python
"""Create transect plot from Warner ETM case."""

import os
import datetime as dt

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import data.dataContainer as dc
import data.timeArray as ta
import plotting.plotBase as pb
import plotting.transectPlot as tp
import data.makeTransects as mt


def load_data(run_name):
    path = os.path.join(run_name, 'data/transect', 'Open_Channel_hvel_detide_0_2010-01-01_2010-01-30.nc')
    hvel = dc.dataContainer.loadFromNetCDF(path)
    path = os.path.join(run_name, 'data/transect', 'Open_Channel_salt_detide_0_2010-01-01_2010-01-30.nc')
    salt = dc.dataContainer.loadFromNetCDF(path)
    path = os.path.join(run_name, 'data/transect', 'Open_Channel_trcr_1_detide_0_2010-01-01_2010-01-30.nc')
    turb = dc.dataContainer.loadFromNetCDF(path)

    return hvel, salt, turb


def make_plot(run_name, N):
    time = dt.datetime(2010, 01, 28, 1, 0)
    hvel, salt, turb = load_data(run_name)
    dia = tp.stackTransectPlotDC(cmap='Spectral_r')
#    dia.addSample('velocity', hvel, time, unit='m s-1', clabel='Velocity')
    dia.addSample('salt', salt, time, N=30, unit='psu', clabel='Salinity', clim=[0, 32])
    dia.addSample('turb', turb, time, N=30, unit='kg m-3', clabel='Sediment', clim=[0, 1], cmap='YlOrBr')
    for ax in dia.axGrid:
        mt.addVelocityQuivers(ax, hvel, N, vSkip=3, hSkip=1, qcolor='k')
    ax.set_xticklabels(['%s' % d for d in range(20, 90, 10)])
    dia.addTitle('')
    dia.showColorBar()
    plt.gcf().savefig('test_%d.png' % N)


if __name__ == '__main__':
    make_plot('Open_Channel_ETM', 24)
