#!/usr/bin/env python
"""View or compare two or more param.in files."""
import collections


def read_param(fpath):
    """Read and return param.in parameters as dict."""
    with open(fpath) as f:
        filelines = f.readlines()

    # Throw out commented lines
    param_lines = []
    for l in filelines:
        try:
            if l.strip()[0] != '!':
                param_lines.append(l)
        except:
            continue

    # Clean strings and place param and value in dict
    params = {}
    for l in param_lines:
        line = l.strip().split()
        name = line[0]
        val = line[2]
        params[name] = val

    # Sort
    params = collections.OrderedDict(sorted(params.items()))

    return params


def print_params(param_files):
    """Print params of N files.

    Params:
    -------
    param_files : dict
      Set of parameters (name, params (OrderedDict))
    """
    # Put param in ordered dict so it's always in same order
    param_files = collections.OrderedDict(sorted(param_files.items()))

    # Create union of used params
    params = set()
    for k in param_files.keys():
        params = params.union(set(param_files[k].keys()))
    params = list(params)
    params.sort()

    # Header will include paths, but not table
    print 'Files'
    cols = []
    for i, p in enumerate(param_files.keys()):
        cols.append(i)
        print '{0:d} : {1:s}'.format(i, p)
    print ''

    # Print all params for each file
    header = '{0: <20}'.format('Parameter')
    header = header+''.join(['{0: <16}'.format(i) for i in cols])
    print header
    print '-'*len(header)
    missing = '----'
    for p in params:
        line = '{0: <20}'.format(p)
        # Add '----' if missing value
        for k in param_files.keys():
            if p not in param_files[k]:
                # print '%s missing in %s' % (p, k)
                param_files[k][p] = missing
            # Print
            line = line+''.join('{0: <16}'.format(param_files[k][p]))
        print line


def main():
    """Read and print param.in files."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('params', nargs='+', help='Path(s) to param.in(s)')
    args = parser.parse_args()

    params = {}
    for f in args.params:
        params[f] = read_param(f)
    print_params(params)


if __name__ == '__main__':
    main()
