#!/usr/local/bin/python
""" Creates a s-level only vgrid.in file for use with SELFE 

    Only creates s-levels and assumes the max depth is < 100m.
    
    Example:
        ./make_vgrid.py 21 

        Creats a vgrid.in.new file with 21 s levels
"""
import sys


def make_vgrid(numberOfLevels):
    try:
        vgrid = open('vgrid.in.new','w')
        vgrid.write("%d 1 100\n" % numberOfLevels)
        vgrid.write("Z levels\n")
        vgrid.write("1 -100\n")
        vgrid.write("S levels\n")
        vgrid.write("7 1 10\n")
        for i in range(1,numberOfLevels+1):
            vgrid.write("%d %f\n"  % (i, -1+(i-1)*(1/(float(numberOfLevels)-1))))
    except:
        raise
    finally:
        vgrid.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: %s [number of S levels]" % sys.argv[0]); 
    else:
        nLevels = int(sys.argv[1])

    make_vgrid(nLevels)

