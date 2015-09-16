#!/usr/bin/env python
"""This script loads bathy for Warner 2007 open channel.

Jesse E. Lopez
"""


#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def load_warner(old_file, new_file, m=4e-4):
    """Create new .gr3 file with 4th column based on parameters for Warner 2007

    Params:
    -------
    old_file - str
        path to refrence .gr3 file
    new_file - str
        path to new .gr3 file

    Notes:
    ------
    - Slope 5m/1e5 m = 5e-5 slope
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

                # Slope from 10 to 5 m from 0 to 100km then 5 m constant
                if x <= 100000:
                    new_val = 10 - x*m
                else:
                    new_val = 5
                outfile.write('%i  %f  %f  %f\n' % (i+1, x, y, new_val))
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
    parser.add_argument('new_file', type=str, help='New .gr3 file.')
    args = parser.parse_args()

    load_warner(args.ref_file, args.new_file)

if __name__ == '__main__':
    main()
