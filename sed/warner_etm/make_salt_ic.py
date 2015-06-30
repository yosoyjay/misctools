#!/usr/bin/env python
"""This makes salt.ic for Warner 2007 open channel.

Jesse E. Lopez
"""
import shutil


#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def make_salt_ic(old_file, new_file='salt.ic'):
    """Create salt.ic for Warner 2007 channel case.

    Params:
    -------
    old_file - str
      path to hgrid.gr3
    new_file - str
      path to new file
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
                m = 30.0/50000.0
                if x < 30000:
                    salt = 30
                elif x > 80000:
                    salt = 0
                else:
                    salt = 30 - m*(x-30000)
                outfile.write('%i  %f  %f  %f\n' % (i+1, x, y, salt))
            # Write rest of the file
            else:
                outfile.write(line)


#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('ref_file', type=str, help='Reference .gr3 file.')
    parser.add_argument('-n', '--new_file', type=str, help='New .gr3 file.',
                        default='salt.ic')
    args = parser.parse_args()

    make_salt_ic(args.ref_file, args.new_file)

if __name__ == '__main__':
    main()
