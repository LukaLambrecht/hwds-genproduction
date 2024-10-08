##########################################################
# script to chain cmsDriver and cmsRun commands in a job #
##########################################################

import sys
import os
sys.path.append('../tools')
import cfgfileparsing
import readcmsdriver
import optiontools as opt
sys.path.append('/user/llambrec/jobtools')
import condorTools as ct
import qsubTools as qt

# get input args from command line
options = []
options.append( opt.Option('cmdfile', vtype='path', required=True,
    explanation='txt file listing cmsDriver commands') )
options.append( opt.Option('workingdir', vtype='path', required=True,
    explanation='working directory') )
options.append( opt.Option('name', required=True,
    explanation='name tag for output files') )
options.append( opt.Option('njobs', vtype='int', required=True,
    explanation='number of parallel submissions') )
options.append( opt.Option('cmsdriver_in_job', vtype='bool', default=False,
    explanation='whether to run the cmsDriver commands in the jobs or locally') )
options.append( opt.Option('ask_confirmation', vtype='bool', default=True,
    explanation='in case of local cmsDriver commands, ask confirmation before proceeding') )
options.append( opt.Option('runlocal', vtype='bool', default=False,
    explanation='run locally instead of via job submission (e.g. for testing)') )
options.append( opt.Option('runtest', vtype='bool', default=False,
    explanation='prepare the job submission but do not actually submit') )
options.append( opt.Option('proxy', vtype='path', 
    default='/user/llambrec/proxy/x509up_u23078') )
options = opt.OptionCollection( options )
if len(sys.argv)==1:
    print('Use with following options:')
    print(options)
    sys.exit()
else:
    options.parse_options( sys.argv[1:] )
    print('Found following configuration:')
    print(options)

# notes
# cmsdriver_in_job:
#   if True, cmsDriver will be run in each job separately;
#   if False, cmsDriver will run locally once 
#   and the configuration files will be copied to all job subdirectories.
#   This option is introduced to avoid DAS errors making most of the jobs fail.
# proxy:
#   location of proxy;
#   valid proxy needed for some cmsDriver commands getting info from DAS!

# process input args
cmdfile = options.cmdfile
if not os.path.exists(cmdfile):
    raise Exception('ERROR: command file {} does not exist.'.format(cmdfile))
workingdir = options.workingdir
if os.path.exists(workingdir):
    raise Exception('ERROR: working directory {} already exists.'.format(workingdir)
		    +' If you want to overwrite, you need to first remove it explicitly.')
os.makedirs(workingdir)
name = options.name
njobs = options.njobs

# get the cmsDriver commands
# note: remove the --filein argument, it will be added automatically!
# note: remove the --fileout argument, it will be added automatically!
# note: remove the --python_filename argument, it will be added automatically!
# note: make sure they all have the --no_exec argument
rawcmsdriver = readcmsdriver.readcmsdriver(cmdfile)
for i,c in enumerate(rawcmsdriver):
    if('--filein' in c): raise Exception('ERROR: command {} contains "--filein" arg'.format(c))
    if('--fileout' in c): raise Exception('ERROR: command {} contains "--fileout" arg'.format(c))
    if('--python_filename' in c): 
	raise Exception('ERROR: command {} contains "--python_filename" arg'.format(c))
    if('--no_exec' not in c): 
	print('WARNING: command {} does not contain "--no_exec" arg'.format(c)
		+', will add it automatically...')
	rawcmsdriver[i] = c+' --no_exec'

# parse the cmsDriver commands
steps = []
for i,c in enumerate(rawcmsdriver):
    filein = '{}_step{}.root'.format(name,i-1)
    fileout = '{}_step{}.root'.format(name,i)
    conffile = 'cmsrun_conf_step{}.py'.format(i)
    if i!=0: c += ' --filein file:{}'.format(filein)
    c += ' --fileout file:{}'.format(fileout)
    c += ' --python_filename {}'.format(conffile)
    steps.append( {'cmsdriver': c,
		   'filein': filein,
		   'fileout': fileout,
		   'conffile': conffile} )

# run the cmsDriver commands if requested
if not options.cmsdriver_in_job:
    # run all cmsDriver commands
    for step in steps:
	cmd = step['cmsdriver']
	print('executing {} ...'.format(cmd))
	os.system(cmd)
    print('All cmsDriver commands have been executed'
          +' and the cmsRun configuration files created.')
    # ask for confirmation
    if options.ask_confirmation:
	print('Please check for errors and if all is ok, type "y" and press enter'
	      +' to submit the jobs.')
	go = raw_input()
	if go!='y':
	    sys.exit()

# loop over the requested number of submissions
# and prepare all jobs
topdir = os.path.abspath(os.getcwd())
tooldir = os.path.join(topdir,'../tools')
exename = 'qjob_cmsrun.sh'
print('preparing all jobs...')
for jobn in range(1,njobs+1):
    print('preparing job {} of {}...'.format(jobn, njobs))
    # set up the working directory for this job
    thisworkingdir = os.path.join(workingdir,'job{}'.format(jobn))
    os.makedirs(thisworkingdir)
    commands = []
    commands.append( 'cd {}'.format(thisworkingdir) )
    commands.append( 'export X509_USER_PROXY={}'.format(options.proxy) )
    os.chdir( thisworkingdir )
    # loop over processing steps
    for i,step in enumerate(steps):
	# copy the existing configuration file 
	# OR add cmsDriver command to job
	if not options.cmsdriver_in_job:
	    os.system('cp {} {}'.format(os.path.join(topdir,step['conffile']), thisworkingdir))
	    # important: set random seed differently for each job
	    cfgfileparsing.setrandomseed( os.path.join(thisworkingdir,step['conffile']), jobn, 
					    verbose=False )
	else:
	    commands.append(step['cmsdriver'])
	    # important: set random seed differently for each job
	    cmd = 'python {}'.format(os.path.join(tooldir,'setrandomseed.py'))
	    cmd += ' {} {}'.format(os.path.join(thisworkingdir,step['conffile']), jobn)
	    commands.append(cmd)
	# add the cmsRun command
	commands.append('cmsRun {}'.format(step['conffile']))
	# remove the input file for this step
	if i!=0: commands.append('rm {}'.format(step['filein']))
    # write commands to file
    thisscript = os.path.join(thisworkingdir, exename)
    with open(thisscript, 'w') as script:
	qt.initializeJobScript( script, docmsenv=True, cmssw_version = 'CMSSW_10_2_25' )
        for c in commands: script.write( c + '\n' )

# remove temporary files
if not options.cmsdriver_in_job:
    print('cleaning up temporary fles...')
    for step in steps:
        os.system('rm {}'.format(os.path.join(topdir,step['conffile'])))

# submit all jobs
if not options.runtest:
    print('submitting all jobs...')
    for jobn in range(1,njobs+1):
	thisworkingdir = os.path.join(workingdir,'job{}'.format(jobn))
	os.chdir(thisworkingdir)
	# submit script as job
	if not options.runlocal: qt.submitQsubJob( exename )
	# for testing: run locally
	if options.runlocal: os.system('bash {}'.format(exename))
