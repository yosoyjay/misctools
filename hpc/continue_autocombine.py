#!/usr/bin/env python
"""Checks status of simulations to guide tasks in batchScriptLib."""
import glob
import os
import argparse

import netCDF4 as nc


def get_ndays(dir, var='elev'):
    """Returns number of days (stacks) in outputs based on files."""
    str = os.path.join(dir,'*_{var}.61.nc'.format(var=var))
    files = glob.glob(str)
    days = [int(os.path.basename(f).split('_')[0]) for f in files]
    return days


def get_var(file):
    """Extract variable from file name."""
    f = os.path.basename(file)
    day, var_str = f.split('_')
    var, file_type, suf = var_str.split('.')
    vector_var = ['62', '64', '67', '71']
    if file_type in vector_var: 
        var = var+'_x'
    return var


def verify_file(f, nsteps=96):
    """Verify file is good based on amount of data.""" 
    fields = ['Mesh', 'Lambert_Conformal', 'vert_coords', 'time',
              'face_nodes', 'node_x', 'node_y', 'node_lon', 'node_lat',
              'sigma', 'z', 'depth', 'elev', 'Cs', 'h_c', 'h0', 'k_bottom']
    var = get_var(f)
    try:
      file = nc.Dataset(f)
      nnodes = file.variables['node_x'][:].shape[0]
      result = None
      if file.variables.keys() != fields:
          result = False
      if file.variables['time'][:].shape != (nsteps,):
          result = False
      if (file.variables['node_x'][:].shape !=
          file.variables['node_y'][:].shape !=
          file.variables['node_lon'][:].shape !=
          file.variables['node_lat'][:].shape !=
          file.variables['depth'][:].shape !=
          file.variables['k_bottom'][:].shape):
          file.close()
          result = False
      if file.variables[var].shape != (nsteps, nnodes):
          result = False
    except RuntimeError:
        result = False
        print('- trouble with file {}'.format(f))
    else:
        file.close()
        result = True
    return result 


def quick_check(dir):
    """Returns number of combined files per day."""
    days = get_ndays(dir)
    nfiles = {} 
    for d in days:
        str = os.path.join(dir, '{day}_*.*.nc'.format(d))
        nfiles[d] = len(glob.glob(str))
    if len(set(nfiles.values())) == nfiles[d]:
        good = True
    else:
        good = False
    return good, nfiles


def thorough_check(dir, nsteps=96):
    """Return dir with days and number of combined files."""
    days = get_ndays(dir)
    days.sort()
    if len(days) == 0:
        good = False
        nfiles = {}
    else:
        nfiles = {}
        for d in days:
            nf = 0
            str = os.path.join(dir, '{}_*.*.nc'.format(d))
            files = glob.glob(str)
            for f in files:
                print '- day {}, file {}'.format(d, f)
                if verify_file(f, nsteps):
                    nf = nf + 1
            nfiles[d] = nf
        if len(set(nfiles.values())) <= 1: 
            good = True
        else:
            good = False

    return good, nfiles


def check_combined(dir, thorough=True, nsteps=96):
    print 'Checking combined files in {}'.format(dir)
    if thorough:
        good, nfiles = thorough_check(dir, nsteps=96)
    else:
        good, nfiles = quick_check(dir)
    return good, nfiles


def find_new_start_day(dir):
    good, nfiles = check_combined(dir)
    if good:
        start = max(nfiles.keys()) + 1
    else:
        # Find where to start
        nfiles_good = max(nfiles.values())
        for k, v in nfiles.iteritems(): 
            if v != nfiles_good:
                start = k
                break
    return start


def launch_continued_autocombine(end, nthreads, dir='combined', round=6, tracers=0, sed=False, debug=False):
    """Launch continuation of autocombine."""
    start = find_new_start_day(dir)
    print '- starting new combine run at day {}'.format(start)
    cmd = 'autocombine.py -D -o combined -d outputs -r {round} -j {nthreads}'.format(round=round, nthreads=nthreads)
    if tracers:
        cmd = cmd + ' -t {tracers}'.format(tracers=tracers)
    if sed:
        cmd = cmd + ' -S'
    cmd = cmd + ' {start} {end}'.format(start=start, end=end)
    if debug:
        print 'Command: '+cmd 
    else:               
        os.system(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('end', type=int, help='last day (stack)')
    parser.add_argument('nthreads', type=int, help='number of threads')
    parser.add_argument('-d', '--debug', action='store_true', help='print command', default=False)
    parser.add_argument('-r', '--round', type=int, help='number of sigdigits', default=6)
    parser.add_argument('-t', '--ntracers', type=int, help='number of tracers', default=0)
    parser.add_argument('-S', '--sed', action='store_true', help='number of tracers',
                        default=False)

    args = parser.parse_args()
    print '-----'
    print 'Setup for continuing autocombine.py'
    print '- end: {end}'.format(end=args.end)
    print '- nthreads: {nthreads}'.format(nthreads=args.nthreads)
    print '- number of sig. digits: {round}'.format(round=args.round)
    if args.ntracers:
        print '- ntracers: {ntracers}.'.format(ntracers=args.ntracers)
    if args.sed:        
        print '- sed enabled'
    if args.debug:
        print '- running in debug mode'
    print '-----'
    print ''

    launch_continued_autocombine(args.end, args.nthreads, tracers=args.ntracers,
                                 round=args.round, sed=args.sed, debug=args.debug)


if __name__ == '__main__':
    main()
