##########################################
# script to wrap cmsRun command in a job #
##########################################

import sys
import os
sys.path.append('../tools')
import cfgfileparsing
import optiontools as opt
sys.path.append('/user/llambrec/jobtools')
import condorTools as ct
import qsubTools as qt


# get input args from command line
options = []
options.append( opt.Option('conffile', vtype='path', required=True,
    explanation='cmsRun configuration file') )
options.append( opt.Option('workingdir', vtype='path', required=True,
    explanation='working directory') )
options.append( opt.Option('njobs', vtype='int', required=True,
    explanation='number of parallel submissions') )
options.append( opt.Option('runlocal', vtype='bool', default=False,
    explanation='run locally instead of via job submission (e.g. for testing)') )
options.append( opt.Option('runtest', vtype='bool', default=False,
    explanation='prepare the job submission but do not actually submit') )
options = opt.OptionCollection( options )
if len(sys.argv)==1:
    print('Use with following options:')
    print(options)
    sys.exit()
else:
    options.parse_options( sys.argv[1:] )
    print('Found following configuration:')
    print(options)

# process input args
conffile = options.conffile
if not os.path.exists(conffile):
    raise Exception('ERROR: configuration file {} does not exist.'.format(conffile))
conffilename = os.path.basename(conffile)
workingdir = options.workingdir
if os.path.exists(workingdir):
    raise Exception('ERROR: working directory {} already exists.'.format(workingdir)
		    +' If you want to overwrite, you need to first remove it explicitly.')
os.makedirs(workingdir)
njobs = options.njobs

# loop over the requested number of submissions
# and prepare all jobs
topdir = os.path.abspath(os.getcwd())
exename = 'qjob_cmsrun.sh'
print('preparing all jobs...')
for jobn in range(1,njobs+1):
    print('preparing job {} of {}...'.format(jobn, njobs))
    # set up the working directory for this job
    thisworkingdir = os.path.join(workingdir,'job{}'.format(jobn))
    thisconffile = os.path.join(thisworkingdir, conffilename)
    os.makedirs(thisworkingdir)
    commands = []
    commands.append( 'cd {}'.format(thisworkingdir) )
    os.chdir( thisworkingdir )
    # copy the configuration file
    os.system('cp {} {}'.format(conffile, thisworkingdir))
    # important: set random seed differently for each job
    cfgfileparsing.setrandomseed( thisconffile, jobn, verbose=False )
    # add the cmsRun command
    commands.append('cmsRun {}'.format(thisconffile))
    # write the commands to file
    thisscript = os.path.join(thisworkingdir, exename)
    with open(thisscript, 'w') as script:
        qt.initializeJobScript( script, docmsenv=True, cmssw_version = 'CMSSW_10_2_25' )
        for c in commands: script.write( c + '\n' )

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
