#!/usr/bin/env python
"""Combine missing days"""
from subprocess import Popen, PIPE 
import glob

def find_missing_days(start, end, nfiles, list=False):
		"""ID and return list of days without all files."""
		missing_days = [] 
		for d in range(start, end+1):
				files = len(glob.glob('combined/%d_*.nc' % d))
				if files != nfiles:
						if list: print d, '%d out of %d' % (files, nfiles) 
						missing_days.append(d)

		return missing_days


def read_days_files(file):
		"""Read and return list of days to combine."""
		with open(file) as f:
				data = f.readlines()

		return [int(d.strip()) for d in data]		


def call_combine(day):
		"""Call combine for a single day."""
		cmd = 'autocombine.py -r 6 -o combined -j 10 -c -C %d %d ' % (day, day) 
		proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
		out = proc.communicate()

		return out


def combine_days(start, end, nfiles, list):
		"""Combine missing days."""
		missing_days = find_missing_days(start, end, nfiles, list)
		if not list:
				for d in missing_days:
						call_combine(d)


def main():
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument('start', type=int, help='Start stack (int)') 
		parser.add_argument('end', type=int, help='End stack (int)')
		parser.add_argument('nfiles', type=int, help='Number of files per day')
		parser.add_argument('-l', '--list', action='store_true', default=False, help='Only list days, do not combine')
		args = parser.parse_args()

		combine_days(args.start, args.end, args.nfiles, args.list) 


if __name__ == '__main__':
		main()
