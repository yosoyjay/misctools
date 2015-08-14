#!/usr/bin/env python
"""Combine missing days"""
from subprocess import Popen, PIPE 
import glob

def find_missing_days(start, end, nfiles):
		"""ID and return list of days without all files."""
		missing_days = [] 
		for d in range(start, end+1):
				files = len(glob.glob('combined/%d_*.nc' % d))
				if files != nfiles:
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


def combine_days(file):
		"""Combine missing days."""
		days = read_days_files(file)
		for d in days:
				call_combine(d)


def main():
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument('file', help='Missing days file.')
		args = parser.parse_args()

		combine_days(args.file)


if __name__ == '__main__':
		main()
