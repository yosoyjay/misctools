#!/usr/bin/env python
"""Collect results from scaling and profiling simulations."""
import datetime
import glob
import os

import pandas as pd


def fetch_dirs(sim_dir, pattern, print_dirs=False):
    """Identify and return dirs following a standard naming pattern."""
    search_pattern = os.path.join(sim_dir, pattern)
    dirs = glob.glob(search_pattern)
    dirs.sort()

    if print_dirs:
       print dirs

    return dirs


def fetch_files(sim_dir, pattern, print_files=False):
    """Identify and return files following a standard naming pattern."""
    search_pattern = os.path.join(sim_dir, pattern)
    files = glob.glob(search_pattern)
    files.sort()

    if print_files:
        print files

    return files


def extract_time(file, time_line=-6, delimiters=[',', '='], walltime=-1, time_field=1):
    """Extract and return simulation time as seconds."""
    with open(file) as f:
        text = f.readlines()

    time_line_text = text[time_line]
    time_text = time_line_text.split(delimiters[0])[walltime].split(delimiters[1])[time_field].strip()
    hours = int(time_text.split(':')[0])
    mins = int(time_text.split(':')[1])
    secs = int(time_text.split(':')[2])
    return 3600*hours + mins*60 + secs


def collect_times(sim_dir, dir_pattern, file_pattern, prnt=False):
    """Collect timings for a timing simulation."""
    times = {}
    files = {}
    for d in fetch_dirs(sim_dir, dir_pattern, prnt):
        for i, f in enumerate(fetch_files(d, file_pattern, prnt)):
            files[d.strip('./'), i] = f.strip('./')
            times[d.strip('./'), i] = extract_time(f)
    
    return files, times


def collect_procs(sim_dir, dir_pattern, submit_file, prnt=False):
    """Collect number of procs used for a timing simulation."""
    procs = {}
    for d in fetch_dirs(sim_dir, dir_pattern, prnt):
        f = fetch_files(d, submit_file, prnt)[0]
        nprocs = extract_procs(f)
        procs[d.strip('./')] = nprocs

    return procs


def extract_procs(file, line=-1, proc_field=2, prnt=False):
    """Extract and return number of procs used."""
    with open(file) as f:
        data = f.readlines()

    cmd_text = data[line]
    procs = int(cmd_text.split(' ')[proc_field])

    if prnt:
      print procs

    return procs


def calc_timings(sim_dir, dir_pattern, submit_file, file_pattern):
    """Collect simulations timings and save as csv file."""
    procs = collect_procs(sim_dir, dir_pattern, submit_file)
    files, times = collect_times(sim_dir, dir_pattern, file_pattern)

    times_df = pd.DataFrame(times.values(), index=pd.MultiIndex.from_tuples(times.keys(), names=['sim', 'run']))
    times_df.columns = ['times [s]']
    times_df.sort_index(inplace=True)
    print 'Mean: ', times_df.mean(level='sim')
    print 'STD: ', times_df.std(level='sim')

    return times_df


def main(sim_dir, dir_pattern, submit_file, file_pattern, name):
    """Run calc_timings from CLI."""
    times = calc_timings(sim_dir, dir_pattern, submit_file, file_pattern)
    times.to_csv(name+'.csv')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('sim_dir', type=str, help='Main simulation directory')
    parser.add_argument('dir_pattern', type=str, help='Individual simulation dir pattern (e.g. run??)')
    parser.add_argument('submit_file', type=str, help='Name of job submit script')
    parser.add_argument('file_pattern', type=str, help='Pattern of output files with timings (e.g. run*.out')
    parser.add_argument('name', type=str, help='Name of output file')
    args = parser.parse_args()
    main(args.sim_dir, args.dir_pattern, args.submit_file, args.file_pattern, args.name)
