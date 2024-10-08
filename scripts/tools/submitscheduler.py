################################
# Scheduled submitting of jobs #
################################

# import python modules
import os
import sys
import subprocess
import time
# import local tools
import optiontools as opt
import checkoutput as co
sys.path.append('/user/llambrec/jobtools')
import qsubTools as qt


class SubmitScheduler:

    def __init__( self, jobdir, exename, maxrunningjobs, overwrite=False, resubmit=False,
			failtags=[] ):
	### initialze a SubmitScheduler
	# input arguments:
	# jobdir: directory containing the job folders
	#         it is supposed to contain subdirectories called "job1", ..., "jobN"
	# exename: each of the subdirectories in jobdir is supposed to contain 
	#	   a submittable script called exename
	# maxrunningjobs: maximum number of simultaneously running jobs
	# overwrite: if False, job scripts that already have associated error log files 
	#            are not taken into account,
	#            if True, all job scripts in jobdir are resubmitted.
	# resubmit: if True, only job scripts that have an associated failed error log file 
	#           are resubmitted (overwrites overwrite=False)
	#	    note: it is possible to start a second SubmitScheduler with this option
	#                 while a first one is still running on the same directory.
	# failtags: list of tags in error log file by which to recognize failed jobs
	#           (needed if resubmit=True)
	print('initializing SubmitScheduler...')
	self.jobdir = jobdir
	self.exename = exename
	self.maxrunningjobs = maxrunningjobs
	# make a sorted list of all subdirectories
	subdirs = [d for d in os.listdir(jobdir) if d[:3]=='job']
	jobns = [int(d.replace('job','')) for d in subdirs]
	sorted_indices = [el[0] for el in sorted(enumerate(jobns), key=lambda el:el[1])]
	subdirs = [os.path.join(jobdir,subdirs[idx]) for idx in sorted_indices]
	self.scriptlist = []
	# loop over subdirectories
	for d in subdirs:
	    script = os.path.join(d,exename)
	    # check if script exists
	    if not os.path.exists(script):
		print('WARNING: script {} not found in {}'.format(exename,d))
		continue
	    # check if associated error and output log files exist
	    efiles = sorted([f for f in os.listdir(d) if exename+'.e' in f])
	    ofiles = sorted([f for f in os.listdir(d) if exename+'.o' in f])
	    if overwrite:
		# remove existing error and output log files and add the script to the queue
		for f in efiles+ofiles: os.system('rm {}'.format(os.path.join(d,f)))
		self.scriptlist.append(script)
	    elif resubmit:
		# skip if no error file exists
		if len(efiles)==0: continue
		# skip if error file shows no failure
		failed = co.has_failed(os.path.join(d,efiles[-1]),
				    do_check_start_done=False,
				    do_check_content=True,
				    contentlist=failtags)
		if not failed: continue
		# else remove existing error and output log files and add the script to the queue
		for f in efiles+ofiles: os.system('rm {}'.format(os.path.join(d,f)))
		self.scriptlist.append(script)
	    else:
		# skip if an error file exists
		if len(efiles)!=0: continue
		# else add the script to the queue
		self.scriptlist.append(script)
	
	# printouts	
	print('found a total of {} jobs to submit in {}'.format(len(self.scriptlist), jobdir))

    def submit( self ):
	### check how many jobs are running and submit some if there is space
	# returns: the number of jobs that is submitted in this call,
	#          or -1 if the job list is fully depleted
	nrunningjobs = self.nrunningjobs()
	njobstosubmit = self.maxrunningjobs-nrunningjobs
	if len(self.scriptlist)<njobstosubmit: njobstosubmit = len(self.scriptlist)
	print('checking submissiong status:')
	print('  currently running jobs: {}'.format(nrunningjobs))
	print('  maximum number of simultaneous jobs: {}'.format(self.maxrunningjobs))
	print('  total amount of jobs left in the queu: {}'.format(len(self.scriptlist)))
	print('  -> can submit {} jobs'.format(njobstosubmit))
	if len(self.scriptlist)==0: return -1
	if njobstosubmit<=0: return 0
	cwd = os.getcwd()
	for i in range(njobstosubmit):
	    # get the next job and submit it
	    script = self.scriptlist.pop(0)
	    os.chdir(os.path.dirname(script))
	    qt.submitQsubJob( script )
	    os.chdir(cwd)
	if len(self.scriptlist)==0: return -1
	return njobstosubmit

    def runningjobs( self ):
	### get job id's of currently running jobs
	# note: fron Willem's deepLearning repository
	# warning: only works for qsub, not for condor
	while True:
	    try:
		qstat_output = subprocess.check_output( 'qstat -u$USER', shell=True,
                            stderr=subprocess.STDOUT )
	    except subprocess.CalledProcessError:
		time.sleep( 1 )
	    else:
		jobtxt = [output_line.split('.')[0] for output_line in qstat_output.split('\n')]
		# qstat returns some other text than only the job id's, so need to clean it:
		jobids = []
		for el in jobtxt:
		    try: 
			jobid = int(el)
			jobids.append(jobid)
		    except: continue
		return jobids

    def nrunningjobs( self ):
	### get number of currently running jobs
	return len(self.runningjobs())


if __name__=='__main__':

    options = []
    options.append( opt.Option('jobdir', vtype='path', required=True) )
    options.append( opt.Option('exename', required=True) )
    options.append( opt.Option('maxrunningjobs', vtype='int', required=True) )
    options.append( opt.Option('sleeptime', vtype='int', default=300,
	explanation='waiting time between subsequent submission attempts') )
    options.append( opt.Option('overwrite', vtype='bool', default=False,
	explanation='re-run all jobs, even if they already have output and error log files') )
    options.append( opt.Option('resubmit', vtype='bool', default=False,
	explanation='submit only jobs that have failed error log files') )
    options.append( opt.Option('failtags', vtype='list', default=[],
	explanation='list of tags in error log file by which to tag failed jobs') )
    options = opt.OptionCollection( options )
    if len(sys.argv)==1:
	print('Use with following options:')
	print(options)
	sys.exit()
    else:
	options.parse_options( sys.argv[1:] )
	print('Found following configuration:')
	print(options)

    # check arguments
    if not os.path.exists(options.jobdir):
	raise Exception('ERROR: job directory {} does not seem to exist...'.format(options.jobdir))
    
    # make SubmitScheduler
    sched = SubmitScheduler( options.jobdir, options.exename, options.maxrunningjobs,
			     overwrite=options.overwrite, resubmit=options.resubmit,
			     failtags=options.failtags )
    
    # submit first batch of jobs
    nsubmittedjobs = sched.submit()
    print('submitted {} jobs'.format(nsubmittedjobs))
    sys.stdout.flush()

    # submit next jobs when there is space
    while nsubmittedjobs>=0:
	nsubmittedjobs = sched.submit()
	print('submitted {} jobs'.format(nsubmittedjobs))
	sys.stdout.flush()
	time.sleep(options.sleeptime)
