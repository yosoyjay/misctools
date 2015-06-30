#!/usr/bin/env python
"""
Generate errors and plots from the Warner et al. 2008 open channel test case.

Jesse Lopez
"""
# -----------------------------------------------------------------------------
#  Imports
# ------------------------------------------------------------------------------
import math
import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.tools.eval_measures as stats

from data.dataContainer import dataContainer as dc

# -----------------------------------------------------------------------------
#  Constants - from Warner
# ------------------------------------------------------------------------------
# u_* - friction velocity - m/s
USTAR = 0.0625
# z_o - bottom roughness - m
Z0 = 0.005
# D - water depth - m
DEPTH = 10
# \kappa - von Karman constant
K = 0.41
# Prandalt number = turbulent viscosity / turbulent vdiffusivity = 0.39 / 0.49
PRANDLT = 0.8
# DAV 1 m/s
U = 1.0
# Erosion rate - kg/m2/s
E0 = 5e-5
# Porosity - no units
PHI = 0.9
# Critical shear stress - N/m2
TAU_C = 0.05
# Settling velocity - m/s
WS = 0.001
# Reference density - kg/m3
RHO = 1024
# ZA
ZA = 0.5

TAU_B = RHO*USTAR**2
E = E0*(1-PHI)*(TAU_B/TAU_C - 1)
C0 = E/WS

# bp specifying the location
BP = 'warner.bp'
RUNNAME = 'Warner'

# Reference RMSE values
REF_VEL = 0.095560
REF_VIS = 0.020060
REF_DIF = 0.025119
REF_TKE = 0.002438
REL_DIFF = 0.001


# -----------------------------------------------------------------------------
#  Functions
# -----------------------------------------------------------------------------
def calc_rouse_profile(z, P, H, z0, C0):
    C = C0*(z*(H-z0) / (z0*(H-z)))**(-P)
    return C


def calc_rouse_parameter(ws=WS, alpha=PRANDLT, kappa=K, ustar=USTAR):
    P = ws/alpha/kappa/ustar
    return P


def calcSediment(z, depth=DEPTH, z0=Z0, C0=C0):
    P = calc_rouse_parameter()
    C = calc_rouse_profile(z, P, depth, z0, C0)
    return C


def make_plot(image_dir, run_dirs, run_names=None, cmu0=0.5544):
    """ Make plot of runs against analytical solution.

    params:
    -------
    image_dir - str
      - Directory to save the file
    run_dirs - list
      - Names of the simulation directories
    run_names - str, optional
      - Names of simulation for legend
    cmu0 - float, optional
      - Parameter in GLS to calculate TKE (default 0.5544 Kantha-Clayson)
    """
    names = []
    m_sed = []
    m_vel = []
    m_dif = []
    for r in run_dirs:
        print r
        names.append(r)
        fileBase = r+'/Warner/data/profile'
        dataFile = os.path.join(fileBase, 'Warner-1K_trcr_1_0_2012-01-01_2012-01-02.nc')
        m_sed.append(dc.loadFromNetCDF(dataFile))
        dataFile = os.path.join(fileBase, 'Warner-1K_hvel_0_2012-01-01_2012-01-02.nc')
        m_vel.append(dc.loadFromNetCDF(dataFile))
        dataFile = os.path.join(fileBase, 'Warner-1K_tdff_0_2012-01-01_2012-01-02.nc')
        m_dif.append(dc.loadFromNetCDF(dataFile))

    # Calculate analytical values using actual water column depth H
    # z - Height above the bed.
    # H - Water column height
    z = abs(m_sed[0].z[0, -1] - m_sed[0].z[:, -1])
    z[0] = Z0
    depths = m_sed[0].z[:, -1]
    H = z[-1]
    u_star = calcFrictionVelocity(U, H, Z0)
    a_vel = calcVelocity(z, u_star, Z0)
    a_vis = calcEddyViscosity(z, u_star, H)
    a_dif = calcEddyDiffusivity(a_vis)
    a_sed = calcSediment(z)

    # "Analytical" values from imposing parabolic eddy viscosity
    print ' - test_warner_channel_analytical'
    fileBase = 'test_warner_channel_analytical/Warner/data/profile'
    dataFile = os.path.join(fileBase, 'Warner-1K_trcr_1_0_2012-01-01_2012-01-03.nc')
    m_sed.append(dc.loadFromNetCDF(dataFile))
    dataFile = os.path.join(fileBase, 'Warner-1K_hvel_0_2012-01-01_2012-01-03.nc')
    m_vel.append(dc.loadFromNetCDF(dataFile))
    dataFile = os.path.join(fileBase, 'Warner-1K_tdff_0_2012-01-01_2012-01-03.nc')
    m_dif.append(dc.loadFromNetCDF(dataFile))

    # Calculate RMSE
    vel_rmse = []
    dif_rmse = []
    sed_rmse = []
    for i, r in enumerate(run_dirs):
       vel_rmse.append(stats.rmse(m_vel[i].data[:, 0, -1], a_vel))
       dif_rmse.append(stats.rmse(m_dif[i].data[:, 0, -1], a_dif))
       sed_rmse.append(stats.rmse(m_sed[i].data[:, 0, -1], a_sed))

    # Plots
    ticks_font = matplotlib.font_manager.FontProperties(size=6)
    f, ax = plt.subplots(1, 3, sharey=True, figsize=(18, 7))
    f.subplots_adjust(wspace=0.4, top=0.9)
    #plt.rc('axes', color_cycle=['r', 'g', 'b', 'y'])

    for vel in m_vel:
        ax[0].plot(np.squeeze(vel.data[:, 0, -1]), depths, marker='.')
    p2 = ax[0].plot(a_vel, depths, color='k')
    ax[0].set_xlim([0, 1.5])
    ax[0].set_ylim([-10, 0.5])
    ax[0].xaxis.set_ticks([0, 0.5, 1, 1.5])
    ax[0].grid(True)
    ax[0].set_ylabel('Z-coordinate $m$')
    ax[0].set_xlabel('Velocity $m/s$')
    #ax[0].set_title('RMSE: %4.3f' % vel_rmse, fontsize=12)
    if run_names is None:
        legend_str = names
    else:
        legend_str = run_names
    legend_str.append('Analytical')
    ax[0].legend(legend_str, loc='upper left', fontsize=8)
    ax[0].fill_between([0, 1.5], -10, m_sed[0].z[0, -1], facecolor='brown')
    ax[0].fill_between([0, 1.5], -10, m_sed[0].z[-1, -1], facecolor='blue', alpha=0.1)

    for dif in m_dif:
        ax[1].plot(np.squeeze(dif.data[:, :, -1]), depths, marker='.')
    ax[1].plot(a_dif, depths, color='k')
    ax[1].set_xlim([0, 0.1])
    #ax[1].xaxis.set_ticks([0, 002, 0.04, 0.06, 0.08])
    ax[1].grid(True)
    ax[1].set_xlabel('Edddy diffusivity $m^2/s$')
    #ax[1].set_title('RMSE: %4.3f' % dif_rmse, fontsize=12)
    ax[1].fill_between([0, 0.1], -10, m_sed[0].z[0, -1], facecolor='brown')
    ax[1].fill_between([0, 0.1], -10, m_sed[0].z[-1, -1], facecolor='blue', alpha=0.1)

    for sed in m_sed:
        ax[2].plot(np.squeeze(sed.data[:, :, -1]), depths, marker='.')
    ax[2].plot(a_sed, depths, color='k')
#    ax[4].xaxis.set_ticks([0.150, 0.2, 0.25, 0.3, 0.35, 0.4])
    ax[2].set_xlim([0.05, 0.35])
    ax[2].grid(True)
    ax[2].set_xlabel('Sediment $kg/m^3$')
    ax[2].fill_between([0.05, 0.35], -10, m_sed[0].z[0, -1], facecolor='brown')
    ax[2].fill_between([0.05, 0.35], -10, m_sed[0].z[-1, -1], facecolor='blue', alpha=0.1)

    f.suptitle('Warner et al. 2008 open channel test', fontsize=14)

    # Save fig
    print 'saving image : warner_comparison.png'
    runName = 'warner_comparison'
    f.savefig(runName, dpi=200)
    plt.close('all')


def testError(vel, vis, dif, tke):
    """ Compares RMSE from run against reference values."""
    print 'Testing results'
    failures = 0
    new_reference = 0

    diff = abs((REF_VEL - vel) / REF_VEL)
    if diff > REL_DIFF:
        print '*FAIL* velocity test. Ref: %f, Model: %f, Diff: %f' % (REF_VEL, vel, diff)
        failures = failures + 1
    elif (diff - REL_DIFF) > 0:
        print '*NEW REFERENCE* velocity %f, Relative error: %f' % (vel, diff)
        new_reference = new_reference + 1

    diff = abs((REF_DIF - dif) / REF_DIF)
    if diff > REL_DIFF:
        print '*FAIL* diffusivity test. Ref: %f, Model: %f, Diff: %f' % (REF_DIF, dif, diff)
        failures = failures + 1
    elif (diff - REL_DIFF) > 0:
        print '*NEW REFERENCE* diffusivity %f, Relative error: %f' % (dif, diff)
        new_reference = new_reference + 1

    diff = abs((REF_VIS - vis) / REF_VIS)
    if diff > REL_DIFF:
        print '*FAIL* viscosity test. Ref: %f, Model: %f, Relative error: %f' % (REF_VIS, vis, diff)
        failures = failures + 1
    elif (diff - REL_DIFF) > 0:
        print '*NEW REFERENCE* viscosity %f, Relative error: %f' % (vis, diff)
        new_reference = new_reference + 1

    diff = abs((REF_TKE - tke) / REF_TKE)
    if diff > REL_DIFF:
        print '*FAIL* TKE test. Ref: %f, Model: %f, Relative error: %f' % (REF_TKE, tke, diff)
        failures = failures + 1
    elif (diff - REL_DIFF) > 0:
        print '*NEW REFERENCE* TKE %f, Relative error: %f' % (tke, diff)
        new_reference = new_reference + 1
    if new_reference > 0:
        print '*NEW REFERENCE* make changes to script'

    passed = None
    if failures > 0:
        print '**FAILED**'
        passed = False
    else:
        print 'PASSED'
        passed = True
    return passed


def calcVelocity(vLevels, uStar, z0):
    """ Calculate the velocity profile.

    u(z) = \frac{1}{kappa} ln\left( frac{z}{z_o} \right) u_*

    params:
    -------
    * vLevels - Array of vertical level depths [m]
    * uStar - Friction velocity
    * z0 - Bottom roughess

    returns:
    --------
    * u - Analytical horizontal velocity
    """
    u = (1.0/K)*np.log(vLevels/z0)*uStar
    return u


def calcEddyViscosity(vLevels, uStar, depth):
    """ Calculate stipulated parabolic shaped eddy viscosity.

    K_M = \kappa*u_\* z \left(1 - \frac{z}{H} \right)

    params:
    -------
    * vLevels - Array of vertical level depths [m]
    * uStar - Friction velocity
    * depth - Total depth

    returns:
    --------
    * Km - Eddy viscosity
    """
    Km = K*uStar*vLevels*(1.0 - vLevels/depth)
    return Km


def calcEddyDiffusivity(Km):
    """ Calculate the eddy diffusivity (Kh).

    K_H = K_M / Prandlt assuming S_H = 0.49, S_M = 0.39, and N^2 = 0.

    params:
    -------
    * Km - Eddy viscosity
    """
    Kh = Km/PRANDLT
    return Kh


def calcFrictionVelocity(dav, depth, z0):
    """ Calculate friction velocity (u_*).

    u_* = \frac{\kappa \overbar{u}}{ln\left(H/z0 \right) - 1 + z0/H}

    params:
    -------
    * dav - Depth averaged velocity
    * depth - Depth of water column (H)
    * z0 - Roughness length
    """
    num = K*dav
    denom = math.log(depth/z0) - 1 + z0/depth
    uStar = num/denom

#    print 'Calculated analytical u_* : %f' % uStar
#    print 'Warner paper analytical u_*: %f' % USTAR
#    print 'RMSE : %f' % stats.rmse([uStar], [USTAR])
    return uStar


def calcTKE(vLevels, uStar, cmu0):
    """ Calculate analytical TKE linearly from 0 at surface to bottom value.

    k_b = (u_b^*)^2 / (c_\mu^0)^2

    param:
    ------
    vLevels - Depths. 0 at surface and positive value at bottom.
    cmu0 - Parameter in GLS to calculate TKE.

    returns:
    --------
    tke - Analytical TKE at all vertical levels
    """
    kb = uStar**2/cmu0**2
    m = kb/vLevels[0]
    tke = m*vLevels
    return tke


def calcSSC(vLevels):
    pass


# -----------------------------------------------------------------------------
#  Main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('img_dir', type=str, help='Directory to save images.')
    parser.add_argument('run_dirs', nargs='+', help='Run dirs')
    parser.add_argument('-n', nargs='+', default=None, help='Run names')
    args = parser.parse_args()

    print 'Parsed args'
    print '-----------'
    print ' Save images to %s' % args.img_dir
    print ' Run directories to plot:'
    for r in args.run_dirs:
        print ' - %s' % r
    if args.n is not None:
        print ' Use names for legend:'
        for r in args.n:
            print ' - %s' % r

    make_plot(args.img_dir, args.run_dirs, args.n)
