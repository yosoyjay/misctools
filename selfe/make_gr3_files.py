#!/usr/bin/env python
"""This script loads bathy for Warner 2007 open channel.

Jesse E. Lopez
"""
import shutil

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def make_const_gr3(old_file, new_file, val):
    """Create new .gr3 file with 4th column constant.

    Params:
    -------
    old_file - str
        path to refrence .gr3 file
    new_file - str
        path to new .gr3 file
    val - float
        new value to write in 4th column
    """
    with open(new_file, 'w') as outfile, open(old_file, 'r') as infile:
        for i, line in enumerate(infile):
            # Header
            if i == 0:
                outfile.write(line)
            # Nodes and elems
            elif i == 1:
                outfile.write(line)
                tmp = line.strip().split()
                nnodes = int(tmp[1])
                nelems = int(tmp[0])
            # Adjust values for nodes
            elif i > 1 and i < nnodes+2:
                tmp = line.strip().split()
                x = float(tmp[1])
                y = float(tmp[2])
                depth = float(tmp[3])
                outfile.write('%i  %f  %f  %f\n' % (i+1, x, y, val))
            # Write rest of the file
            else:
                outfile.write(line)


def create_gr3_files():
    values = {'diffmax.gr3': 1.0,
              'diffmin.gr3': 1e-15,
              'drag.gr3': 0.0088,
              'interpol.gr3': 2.0,
              'rough.gr3': 0.0005,
              'tvd.gr3': 1.0,
              'xlsc.gr3': 0.5,
              'salt.ic': 0,
              'temp.ic': 10}

    for f in values.keys():
        shutil.copy('hgrid.gr3', f)

    for f, v in values.iteritems():
        print 'Updating file %s' % f
        make_const_gr3(f, f+'.new', v)

    for f in values.keys():
        shutil.move(f+'.new', f)


#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('ref_file', type=str, help='Reference .gr3 file.')
    parser.add_argument('new_file', type=str, help='New .gr3 file.')
    args = parser.parse_args()

    load_warner(args.ref_file, args.new_file)

if __name__ == '__main__':
    create_gr3_files()
