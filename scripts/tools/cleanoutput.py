#################################################################
# automatically remove job directories that contain failed jobs #
#################################################################

import sys
import os
import re
import checkoutput

if __name__=='__main__':

    inputdir = sys.argv[1]
    toremove = []

    # loop over job directories
    jobdirs = [os.path.join(inputdir,d) for d in os.listdir(inputdir) if re.match('job*',d)]
    for jobdir in jobdirs:
	# find the error log file
	efiles = [os.path.join(jobdir,f) for f in os.listdir(jobdir) if '.sh.e' in f]
	if len(efiles)!=1:
	    print('WARNING: unexpected number of error log files, skipping...')
	    continue
	efile = efiles[0]
	failed = checkoutput.has_failed(efile,
			    do_check_start_done=False,
			    do_check_content=True,
			    contentlist=[
                                    'Begin Fatal Exception',
                                    'fatal system signal'
                                    ])
        if failed: toremove.append(jobdir)

    print('will remove {} job directories:'.format(len(toremove)))
    for d in toremove: print('  - {}'.format(d))
    print('continue? (y/n)')
    go = raw_input()
    if not go=='y': sys.exit()

    for jobdir in toremove:
	os.system('rm -r {}'.format(jobdir))
    print('done')
