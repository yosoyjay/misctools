"""
Recored of how flux was create for ocean open boundary for
estuarine circulation [Test case 3] of Warner et al (2005).

Writes a flux file to 'flux.th.new'
"""

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
NDAYS = 29      # Number of days in run (days) 
TIME_STEP = 30 	# Time step (s) 
U = 0.40        # Average tidal velocity (m/s)
H = 10          # Average height (m)
W = 100         # Channel width (m)
T = 12*3600     # Tidal period (12 hours * 3600 seconds) (s)

#-------------------------------------------------------------------------------
# Imports 
#-------------------------------------------------------------------------------
import numpy as np
import math

#-------------------------------------------------------------------------------
# Functions - Q = U*H*sin(2*pi*t/T)
#-------------------------------------------------------------------------------
times = range(TIME_STEP, NDAYS*86400, TIME_STEP)

f = file('flux.th.new', 'w')
for i in range(len(times)):
  flux = U*H*math.sin(2.0*math.pi*times[i]/T)
  f.write('%f %f\n' % (times[i], flux)) 

f.close()
