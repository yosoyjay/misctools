#!/usr/bin/env python
"""Fetch obs."""
import datetime
import data.stationCollection as StationCollection


def fetch_obs(start, end, vars=['elev', 'temp', 'salt', 'hvel']):
    """Fetch and save observations from database."""
    obs = StationCollection.fetchAvailableObservations(start, end, 'obs', variables=vars)
    obs.saveAsNetCDFCollection()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('end', type=str, help='End date (YYYY-MM-DD)')
    args = parser.parse_args()

    start = datetime.datetime.strptime(args.start, '%Y-%m-%d')
    end = datetime.datetime.strptime(args.end, '%Y-%m-%d')

    fetch_obs(start, end)


if __name__ == '__main__':
    main()
