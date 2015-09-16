#!/usr/bin/env python

import netCDF4 as nc
import numpy as np
import struct

from data import selfeGridUtils as sgu


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def load_hvel_data(hvel_path):
    hvel = nc.Dataset(hvel_path)
    u = hvel.variables['u'][:, -1]
    v = np.zeros_like(u)

    return u, v


def calc_velocity_profile(dav, z0, Z, depth):
    # Calc friction velocity first
    num = 0.41*dav
    denom = np.log(depth/z0) - 1 + z0/depth
    ustar = num/denom

    # Calc velocity profile
    u = (1.0/0.41)*np.log(Z/z0)*ustar

    return u


def load_velocity_profile(dav, z0, nvrt, vgrid_path, eta=0, dp=10.0):
    vgrid = sgu.verticalCoordinates.fromVGridFile(vgrid_path)
    Z, kbp2, iwet = vgrid.computeVerticalCoordinates(np.array([eta]), np.array([dp]))
    # need depths to be height from the bottom
    Z = dp + Z
    u = calc_velocity_profile(dav, z0, Z, dp)

    # remove nans at bottom
    bad_ix = Z == -0.0
    u[bad_ix] = 0.00
    v = np.zeros_like(u)

    # Swap depths and order so bottom is first level
    Z = Z[::-1, 0]
    #u = u[::-1, 0]

    print 'Above bottom[m]\t\tU [m/s]\t\tdz'
    dz = np.diff(Z)
    for i in range(Z.shape[0]):
        if i == Z.shape[0]-1:
            print '%2d\t %8f\t %8f\t ---' % (i+1, Z[i], u[i])
        else:
            print '%2d\t %8f\t %8f\t %8f' % (i+1, Z[i], u[i], dz[i])

    return u, v, Z


def plot_profile(u, Z):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.plot(u, Z, marker='o')
    ax = plt.gca()
    ax.set_ylabel('Height above bottom [m]')
    ax.set_xlabel('Velocity [m/s]')
    plt.title('Velocity profile')
    print 'Saving profile plot'
    plt.gcf().savefig('vel_prof.png')


def pack_data(nnodes, nvrt, u, v):
    # Dump data into buffer
    # nvrt*nnodes*u*2 (doubles are 2 floats)
    # nvrt*nnodes*v*2
    # 1 time is a float
    size = nvrt*nnodes*2 + 1
    out = np.empty((size,), dtype='f')
    ix = 0
    for n in range(nnodes):
        for k in range(nvrt):
            ix = ix + 4
            struct.pack_into('f', out, ix, u[k])
            ix = ix + 4
            struct.pack_into('f', out, ix, v[k])

    return out


def write_uv3D(out, ntimesteps, dt):
    # Write the file
    print 'Writing file uv3D.th'
    f = open('uv3D.th', 'wb')
    for t in range(1, ntimesteps+1):
        # Update time
        struct.pack_into('f', out, 0, t*dt)
        # Fortran record length
        # f.write(struct.pack('i', size))
        f.write(out)
        # Fortran record length
        # f.write(struct.pack('i', size))
    f.close()


def create_uv3D_file(vgrid_path, nnodes, nvrt, nts, dt, dav, z0, depth):
    """Writes logrithmic velocity profile to all nodes for all times."""
    eta = 0.0
    u, v, d = load_velocity_profile(dav, z0, nvrt, vgrid_path, dp=depth)
    plot_profile(u, d)
    buf_out = pack_data(nnodes, nvrt, u, v)
    write_uv3D(buf_out, nts, dt)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def parsecli():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('nnodes', type=int, help='Number of nodes on boundary')
    parser.add_argument('nvrt', type=int, help='Number vertical levels')
    parser.add_argument('ndays', type=float, help='Number of days')
    parser.add_argument('dt', type=float, help='Model time step')
    parser.add_argument('dav', type=float, help='Depth averaged velocity')
    parser.add_argument('z0', type=float, help='Bottom roughness length [m]')
    parser.add_argument('depth', type=float, help='Depth at boundary')
    parser.add_argument('vgrid', help='vgrid.in path')
    args = parser.parse_args()

    nts = int(args.ndays*86400/args.dt)
    create_uv3D_file(args.vgrid, args.nnodes, args.nvrt, nts, args.dt,
                     args.dav, args.z0, args.depth)


if __name__ == '__main__':
    parsecli()
