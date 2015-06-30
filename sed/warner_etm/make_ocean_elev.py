#!/usr/bin/env python
"""
Generates elevation for Warner et al. 2007

jesse.e.lopez - 2015-03-09
"""

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
NDAYS = 100     # Number of days in run (days)
TIME_STEP = 15 	# Time step (s)
U = 0.40        # Average tidal velocity (m/s)
H = 10          # Average height (m)
W = 100         # Channel width (m)
T = 12*3600     # Tidal period (12 hours * 3600 seconds) (s)

# -----------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import numpy as np
import os
import matplotlib
if 'stccmop' in os.environ.get('HOSTNAME'):
    matplotlib.use('AGG')
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# Functions - Q = U*H*sin(2*pi*t/T)
# ------------------------------------------------------------------------------


def make_tidal_elev(times, tide, dt):
    """Make elevation for open channel case for tidal time periods.

    Params:
    -------
    times - np.array
      Time in seconds to calculate elevation
    tide - str
      Either 'sd' for semi-diurnal or 'fn' for fortnightly
    tide - float
      Simulation time step

    Notes:
    ------
      Surface displacement:
      ---------------------
      \eta_{x=0} = A sin \left( \omega t \right)

      Tidal periods:
      --------------
      T = 2 \pi / \omega
    """
    if tide == 'sd':
        amp = 0.4                   # meters
        omega = 2*np.pi/(12*60*60)  # 12 hours
        eta = amp*np.sin(omega*times)
    else:
        amp1 = 0.45
        omega1 = 2*np.pi/(14*24*60*60)
        amp2 = 0.4                   # meters
        omega2 = 2*np.pi/(12*60*60)  # 12 hours

        eta1 = amp1*np.sin(omega1*times)
        eta2 = amp2*np.sin(omega2*times)
        eta = eta1 + eta2

    return eta


def write_elev_to_file(times, elev, fn='elev.th.new'):
    """Write to file for input at time history file."""
    print '- saving elev time history to %s' % fn
    f = file(fn, 'w')
    for i in range(len(times)):
        f.write('%f %f\n' % (times[i], elev[i]))
    f.close()


def make_plot(times, elev, tide):
    """Plot generated elevation."""
    plt.subplot(2, 1, 1)
    plt.plot(times, elev, color='r', linewidth=3)
    plt.ylabel('Elevation [m]')
    plt.grid()
    plt.title('Warner et al. 2007 Open Channel Ocean Free Surface')

    # 24 hour plot
    plt.subplot(2, 1, 2)
    ix = 86400/TIME_STEP
    plt.plot(times[:ix], elev[:ix], color='r', linewidth=3)
    plt.ylabel('Elevation [m]')
    plt.xlabel('Time [s]')
    plt.grid()

    fname = 'warner_elevation_%s.png' % tide
    print '- saving figure to %s' % fname
    plt.savefig(fname)


def make_warner_elev(plot, tide, dt, ndays):
    """Generates elevation specified in Warner et al. 2005.
    """
    times = np.arange(dt, ndays*86400, dt)
    elev = make_tidal_elev(times, tide, dt)
    if tide == 'sd':
        f = 'elev.sd.%d.%d.th' % (dt, ndays)
    elif tide == 'fn':
        f = 'elev.fn.%d.%d.th' % (dt, ndays)
    else:
        print 'tide type not recognized: %s' % tide
        return
    write_elev_to_file(times, elev, f)
    if plot:
        make_plot(times, elev, tide)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def parse_cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plot', default=False, action='store_true', help='Make plot.')
    parser.add_argument('dt', type=float, help='Simulation time step.')
    parser.add_argument('ndays', type=float, help='Number of simulation days.')
    parser.add_argument('tide', default=False, type=str,
                        help='\'sd\' for semi-dirunal or \'fn\' for fortnightly')
    args = parser.parse_args()

    print 'Generating elevation for Warner et al. 2007 open channel'
    print '- %s tide' % args.tide
    make_warner_elev(args.plot, args.tide, args.dt, args.ndays)


if __name__ == '__main__':
    parse_cli()
