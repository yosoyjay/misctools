#!/usr/bin/env python
"""Fetch obs."""
import datetime
from crane.data import stationCollection as sc

VARS = ['elev', 'temp', 'salt', 'vel_E', 'vel_N']


def fetch_obs(start, end, vars=VARS):
    """Fetch and save observations from database."""
    obs = sc.fetchAvailableObservations(start, end, 'obs', variables=vars)
    obs.saveAsNetCDFCollection()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('end', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('-v', '--var', default=None,
                        help=('Specify a single variable to fetch '
                              '(default: elev, salt, temp, vel_E, vel_N)'))

    args = parser.parse_args()

    start = datetime.datetime.strptime(args.start, '%Y-%m-%d')
    end = datetime.datetime.strptime(args.end, '%Y-%m-%d')
    if args.var is None:
        vars = VARS
    else:
        vars = args.var

    fetch_obs(start, end, vars)


if __name__ == '__main__':
    main()
