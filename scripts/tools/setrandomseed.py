##########################################################################
# Script to call cfgfileparsing.py / setrandomseed from the command line #
##########################################################################

import sys
import os
from cfgfileparsing import setrandomseed

cfgfile = sys.argv[1]
seed = int(sys.argv[2])
setrandomseed( cfgfile, seed )
