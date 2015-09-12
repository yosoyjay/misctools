#!/usr/bin/env python
"""Identfies and creates latest SELFE hotstart file.

Jesse Lopez - 2015-09-10
"""
import glob
import os
import subprocess 
import argparse
import shutil

import netCDF4 as nc


def get_last_hotstart(dir):
    """Find and return last hotstart files."""
    string = os.path.join(dir, '*_0000_hotstart')
    stacks = glob.glob(string)

    ts = []
    for s in stacks:
        ts.append(int(s.split('/')[-1].split('_')[0]))
    if len(ts) > 0:
        last = max(ts)
    else:
        last = 0
    return last


def get_ncores(dir, last):
    """Determine and return number of cores used."""
    string = os.path.join(dir, '{last}_*_hotstart'.format(last=last))
    nfiles = glob.glob(string)
    ncores = len(nfiles)
    return ncores


def combine_hotstart(dir, ntracers, sed):
    """Combine hotstart file and return file name hotstart.in.stack ."""
    last = get_last_hotstart(dir)
    print '- last stack: {last}'.format(last=last)
    ncores = get_ncores(dir, last)
    print '- ncores: {ncores}'.format(ncores=ncores)

    if sed:
      cmd = 'combine_hotstart_sed {ncores} {ntracers} {ts} 0 1 1'.format(ncores=ncores, ntracers=ntracers, ts=last) 
    else:
      cmd = 'combine_hotstart4 {ncores} {ntracers} {ts} 1 0 0'.format(ncores=ncores, ntracers=ntracers, ts=last)


    old = os.getcwd()
    print '- moving to {dir}'.format(dir=dir)
    os.chdir(dir)
    print '- combining using: {cmd}'.format(cmd=cmd)
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    stdout = proc.communicate()[0]
    #print 'stdout: ', repr(stdout)

    new_file = 'hotstart.in.{ts}'.format(ts=last)
    #cmd = 'mv hotstart.in {new_file}'.format(new_file=new_file)
    #proc = subprocess.Popen([cmd], stdout=subprocess.PIPE)
    print '- moving hotstart.in to hotstart.in.{ts}'.format(ts=last)
    os.rename('hotstart.in', new_file)
    print '- moving to {dir}'.format(dir=old)
    os.chdir(old)

    return new_file    


def prepare_last_hotstart(dir, ntracers, sed):
    """Create latest hotstart file and move it to run directory."""
    run = os.path.dirname(dir)
    new_file = combine_hotstart(dir, ntracers, sed)
    print '- new file is {new_file}'.format(new_file=new_file)
    old = os.getcwd()
    print '- moving to {run}'.format(run=run)
    os.chdir(run)
    new_file_long = os.path.join('outputs', new_file)
    print '- moving {file} to {run}'.format(file=new_file_long, run=run)
    shutil.move(new_file_long, './')
    print '- unlinking hotstart.in'
    os.unlink('hotstart.in')
    print '- symlinking {new_file} to hotstart.in'.format(new_file=new_file)
    os.symlink(new_file, 'hotstart.in')
    print '- moving to {dir}'.format(dir=old)
    os.chdir(old)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, help='outputs directory')
    parser.add_argument('-n', '--ntracers', default=0, type=int, help='number of tracers')
    parser.add_argument('-S', '--sed', action='store_true', help='number of tracers',
                        default=False)

    args = parser.parse_args()
    print '-----'
    print 'Combining hotstart.in'
    print '- output dir: {dir}'.format(dir=args.dir)
    if args.ntracers:
        print '- ntracers: {ntracers}.'.format(ntracers=args.ntracers)
    if args.sed:        
        print '- sed enabled'
    print '-----'
    print ''

    prepare_last_hotstart(args.dir, args.ntracers, args.sed)


if __name__ == '__main__':
    main()
