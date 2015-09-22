#!/usr/bin/env python
"""Combine all hotstart files.

Jesse Lopez - 2015-09-22
"""
import glob
import os
import subprocess
import argparse
import shutil

import netCDF4 as nc


def get_hotstarts(dir):
    """Find and list of times for all hotstart files."""
    string = os.path.join(dir, '*_0000_hotstart')
    stacks = glob.glob(string)

    all_times = []
    for s in stacks:
        all_times.append(int(s.split('/')[-1].split('_')[0]))

    return all_times


def get_ncores(dir, time):
    """Determine and return number of cores used for a specific time."""
    string = os.path.join(dir, '{time}_*_hotstart'.format(time=time))
    nfiles = glob.glob(string)
    ncores = len(nfiles)
    return ncores


def combine_hotstart(dir, time, ntracers, sed):
    """Combine hotstart file and return file name hotstart.in.stack ."""
    print '- stack: {time}'.format(time=time)
    ncores = get_ncores(dir, time)
    print '- ncores: {ncores}'.format(ncores=ncores)

    if sed:
        cmd = 'combine_hotstart_sed {ncores} {ntracers} {ts} 0 1 1'.format(ncores=ncores, ntracers=ntracers, ts=time)
    else:
        cmd = 'combine_hotstart4 {ncores} {ntracers} {ts} 1 0 0'.format(ncores=ncores, ntracers=ntracers, ts=time)

    old_dir = os.getcwd()
    print '- moving from {old_dir} to {dir}'.format(old_dir=old_dir, dir=dir)
    os.chdir(dir)
    print '- combining using: {cmd}'.format(cmd=cmd)
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    stdout = proc.communicate()[0]

    try:
        new_file = 'hotstart.in.{ts}'.format(ts=time)
        print '- moving hotstart.in to hotstart.in.{ts}'.format(ts=time)
        os.rename('hotstart.in', new_file)
    except:
        print '- problem with {new_file}'.format(new_file=new_file)
    print '- moving to {dir}'.format(dir=old_dir)
    os.chdir(old_dir)

    return new_file


def combine_hotstarts(outputs, hotstart, ntracers, sed):
    """Create hotstart files and move them to hotstart directory."""
    times = get_hotstarts(outputs)
    times.sort()
    for t in times:
        print '- time step {t}'.format(t=t)
        new_file = combine_hotstart(outputs, t, ntracers, sed)
        print '- new file is {new_file}'.format(new_file=new_file)
        new_file_long = os.path.join('outputs', new_file)
        print '- moving {file} to {hotstart}'.format(file=new_file_long, hotstart=hotstart)
        try:
            shutil.move(new_file_long, hotstart)
        except:
            print '- unable to move file!'
        print ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outputs_dir', type=str, help='outputs directory')
    parser.add_argument('hotstart_dir', type=str, help='directory to save output hotstart files')
    parser.add_argument('-n', '--ntracers', default=0, type=int, help='number of tracers')
    parser.add_argument('-S', '--sed', action='store_true', help='number of tracers',
                        default=False)

    args = parser.parse_args()
    print '-----'
    print 'Combining hotstart.in'
    print '- output dir: {dir}'.format(dir=args.outputs_dir)
    print '- hotstart dir: {dir}'.format(dir=args.hotstart_dir)
    if args.ntracers:
        print '- ntracers: {ntracers}.'.format(ntracers=args.ntracers)
    if args.sed:
        print '- sed enabled'
    print '-----'
    print ''

    combine_hotstarts(args.outputs_dir, args.hotstart_dir, args.ntracers, args.sed)


if __name__ == '__main__':
    main()
