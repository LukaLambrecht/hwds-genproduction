############################################
# Script to batch rename output root files #
############################################

import sys
import os
import re

if __name__=='__main__':

    inputdir = sys.argv[1]
    torename = {}

    # loop over job directories
    jobdirs = [os.path.join(inputdir,d) for d in os.listdir(inputdir) if re.match('job*',d)]
    for jobdir in jobdirs:
	# find the root file
	rfiles = [os.path.join(jobdir,f) for f in os.listdir(jobdir) if '_step3.root' in f]
	if len(rfiles)!=1:
	    print('WARNING: unexpected number of root files, skipping...')
	    continue
	rfile = rfiles[0]
	
	# implement renaming here
	newrfile = rfile.replace('_step3.root','_Run2018MiniAODSIM.root')
	torename[rfile] = newrfile

    print('will rename {} files:'.format(len(torename)))
    for old,new in torename.items(): print('  - {} -> {}'.format(old,new))
    print('continue? (y/n)')
    go = raw_input()
    if not go=='y': sys.exit()

    for old,new in torename.items():
	os.system('mv {} {}'.format(old,new))
    print('done')
