#!/usr/bin/env python
"""Create an open channel transect."""
import numpy as np

default_params = {'start': 0,
                  'end': 60000,
                  'ypos': 50,
                  'deltax': 200,
                  'depth': 1.0
                  }


def make_transect(file_name, params):
    """Create transect file.

    Params:
    file_name - str
      Name of new transect file.
    params - dict
      Parameters for creating transect. ('start', 'end', 'ypost', 'deltax')
    """
    print params
    xpos = np.arange(params['start'], params['end'], params['deltax'])
    npts = len(xpos)
    with open(file_name, 'w') as f:
        f.write(file_name+'\n')
        f.write('%d\n' % npts)
        for i in range(npts):
            f.write('%d %f %f %f\n' % (i+1, xpos[i], params['ypos'], params['depth']))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str, help='Name of file for transect build point')
    parser.add_argument('start', type=float, help='Start x position')
    parser.add_argument('end', type=float, help='End x position')
    parser.add_argument('ypos', type=float, help='Y position')
    parser.add_argument('deltax', type=float, help='Delta x in position')
    parser.add_argument('-d', '--depth', type=float, default=1.0, help='Y position')
    args = parser.parse_args()

    params = {}
    params['start'] = args.start
    params['end'] = args.end
    params['ypos'] = args.ypos
    params['deltax'] = args.deltax
    params['depth'] = args.depth

    make_transect(args.file_name, params)
