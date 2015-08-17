#!/usr/bin/env python
"""Create time history files for sediment simulations with an upstream boundary
at Beaver Army Terminal using a rating curve developed from USGS data.
"""
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
# From ratings curves of form log(c) = log(a)+log(flux)*b based on
# USGS data from Beaver Army Terminal 1990 - 2015
# http://cida.usgs.gov/sediment/

# Total SPM
# r2 = 0.786, p < 0.01, std_err = 0.088
SPM = {'a': -18.6132492602, 'b':  1.65095653426}

# Silt class, or those less than d50 (P63)
# r2 = 0.740, p < 0.01, std_err = 0.088
SILT = {'a': -16.938280665, 'b':  1.43398603797}

# Sand class, or those greater than d50 (P63)
# r2 = 0.742, p < 0.01, std_err = 0.162
SAND = {'a': -29.3524701378, 'b':  2.64448615935}

# Percent of silt/clay sizes from LMER water samples (data + Fain et al. 2001)
# wash = 0.07
# fine silt = 0.40
# coarse silt = 0.53


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def make_th_files(fluxpath, silt_percents, plot=False):
    """Create .th files based on Beaver Army rating curve."""
    time, flux = read_flux(fluxpath)

    silt = calc_silt(flux)
    sand = calc_sand(flux)
    silts = calc_silt_classes(silt, silt_percents)
    write_th_files(time, silts, sand)
    if plot:
        make_plots(time, silts, sand)


def read_flux(fluxpath):
    """Read and return a flux file."""
    print 'Reading flux file %s' % fluxpath
    data = np.genfromtxt(fluxpath)
    time = data[:, 0]
    # Only have positive values on inflow (negative values)
    flux = -1*data[:, 1]
    # Miniscule value when flowing upstream
    flux[flux <= 0.0] = 0.001

    return time, flux


def calc_sand(flux):
    """Calculate and return sand concentrations based on BA flux."""
    sand = np.exp(SAND['a'] + np.log(flux)*SAND['b'])
    return sand


def calc_silt(flux):
    """Calculate and return sand concentrations based on BA flux."""
    silt = np.exp(SILT['a'] + np.log(flux)*SILT['b'])
    return silt


def calc_silt_classes(silt, silt_percents):
    """Calculate silts by percents in silts"""
    silts = []
    for s in silt_percents:
        silts.append(silt*s)
    return silts


def make_plots(time, silts, sand):
    """Make a plot of the resulting time series of silts + sands."""
    nplots = len(silts)+1
    fig, ax = plt.subplots(nplots, 1, sharex=True)

    # Silts
    for i, s in enumerate(silts):
        ax[i].plot(time, s, label='silt %d' % (i+1))
        ax[i].set_ylabel('SSC [kg/m3]')
        ax[i].set_xlabel('Simulation time')
        ax[i].legend()

    # Sand
    ax[-1].plot(time, sand, label='sand')
    ax[-1].set_ylabel('SSC [kg/m3]')
    ax[-1].set_xlabel('Simulation time')
    ax[-1].legend()

    # Save
    figname = 'sed_tracer_th.png'
    print 'Saving figure %s' % figname
    plt.savefig(figname)


def write_th_files(time, silts, sand):
    """Create time history files."""
    out_num = 0
    out_fmt = '%d %.2e'

    # Silts
    for s in silts:
        out_num = out_num + 1
        out = np.array([time, s]).T
        fname = 'htr_%s.th' % out_num
        print 'Writing class %d (silt/clay) to %s' % (out_num, fname)
        np.savetxt(fname, out, fmt=out_fmt)

    # Sand
    out_num = out_num + 1
    out = np.array([time, sand]).T
    fname = 'htr_%s.th' % out_num
    print 'Writing class %d (sand) to %s' % (out_num, fname)
    np.savetxt(fname, out, fmt=out_fmt)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('flux_file', type=str, help='path to flux.th file.')
    parser.add_argument('-s', '--silt_perc', type=str,
                        help='Custum percent of spm per silt class, e.g. \'0.25,0.5,0.75\'')
    parser.add_argument('-p', '--plot', action='store_true', default=False, help='plot results')
    args = parser.parse_args()
    if args.silt_perc:
        silt_percents = [float(s) for s in args.silt_perc.split(',')]
    else:
        # Based on literature and water sample values
        silt_percents = [0.07, 0.40, 0.53]
    print 'Using %d silt/clay classes' % len(silt_percents)
    for i, p in enumerate(silt_percents):
        print '- silt/clay class %d : %f' % (i+1, p)
    make_th_files(args.flux_file, silt_percents, args.plot)

if __name__ == '__main__':
    main()
