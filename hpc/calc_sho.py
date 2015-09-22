#!/usr/bin/env python
"""Calculate SHO on a daily basis.

Jesse Lopez
"""
from __future__ import print_function
import multiprocessing
import subprocess


def calc_daily_sho(day, dir='combined', out='sho'):
    """Calculate sho for a single day."""
    proc = multiprocessing.current_process()
    print('- calculating sho for day {} on proc {}'.format(day, proc))
    cmd = 'compute_sho_new {} {} ~/share/reaches_db33_cutbva.gr3 {} {}'.format(dir, out, day, day)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    return proc.returncode


def calc_sho(start_day, end_day, pool=4, dir='combined', out='sho'):
    """Calculate sho for a range of days."""
    pool = multiprocessing.Pool(4)
    for d in range(start_day, end_day+1):
        args = (d, dir, out)
        pool.apply_async(calc_daily_sho, args=args)
    pool.close()
    pool.join()


def main():
    """Calculate sho for range of days."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('start_day', type=int, help='first day (stack)')
    parser.add_argument('end_day', type=int, help='last day (stack)')
    parser.add_argument('-p', '--pool', type=int, default=4,
                        help='number of works in pool')
    args = parser.parse_args()

    calc_sho(args.start_day, args.end_day, args.pool)


if __name__ == '__main__':
    main()
