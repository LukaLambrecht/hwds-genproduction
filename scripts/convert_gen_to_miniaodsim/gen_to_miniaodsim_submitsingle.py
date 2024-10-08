##########################################################
# script to chain cmsDriver and cmsRun commands in a job #
##########################################################

import sys
import os
sys.path.append('../tools')
import cfgfileparsing
import readcmsdriver
sys.path.append('/user/llambrec/jobtools')
import condorTools as ct
import qsubTools as qt

# get input args from command line
if len(sys.argv)==1:
    print('Required command line args:')
    print(' - txt file listing cmsDriver commands to be run sequentially')
    print(' - input file (supposed to be GEN-level)')
    print(' - working directory')
    print(' - output file tag')
    sys.exit()
elif len(sys.argv)!=5:
    raise Exception('ERROR: wrong number of command line args')

# other settings
run_cmsdriver_in_job = False
# (if True, cmsDriver will be run in each job separately;
#  if False, cmsDriver will run locally once 
#  and the configuration files will be copied to all job subdirectories.
#  This option is introduced to avoid DAS errors making most of the jobs fail...
proxy = '/user/llambrec/proxy/x509up_u23078'
# (location of proxy.
#  note: valid proxy needed for some cmsDriver commands getting info from DAS!)

# process input args
cmdfile = os.path.abspath(sys.argv[1])
if not os.path.exists(cmdfile):
    raise Exception('ERROR: command file {} does not exist.'.format(cmdfile))
inputfile = os.path.abspath(sys.argv[2])
if not os.path.exists(inputfile):
    raise Exception('ERROR: input file {} does not exist.'.format(inputfile))
workingdir = os.path.abspath(sys.argv[3])
if os.path.exists(workingdir):
    raise Exception('ERROR: working directory {} already exists.'.format(workingdir)
		    +' If you want to overwrite, you need to first remove it explicitly.')
os.makedirs(workingdir)
name = sys.argv[4]

# get the cmsDriver commands
# note: remove the --filein argument, it will be added automatically!
# note: remove the --fileout argument, it will be added automatically!
# note: remove the --python_filename argument, it will be added automatically!
# note: make sure they all have the --no_exec argument
rawcmsdriver = readcmsdriver.readcmsdriver(cmdfile)
print('### read following cmsDriver commands from cmdfile:')
for c in rawcmsdriver: print('  {}'.format(c))
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
    if i==0: filein = inputfile
    else: filein = '{}_step{}.root'.format(name,i-1)
    fileout = '{}_step{}.root'.format(name,i)
    conffile = 'cmsrun_conf_step{}.py'.format(i)
    c += ' --filein file:{}'.format(filein)
    c += ' --fileout file:{}'.format(fileout)
    c += ' --python_filename {}'.format(conffile)
    steps.append( {'cmsdriver': c,
		   'filein': filein,
		   'fileout': fileout,
		   'conffile': conffile} )
print('### parsed cmsDriver commands:')
for s in steps: print('  {}'.format(s['cmsdriver']))

# run the cmsDriver commands if requested
if not run_cmsdriver_in_job:
    for step in steps:
	cmd = step['cmsdriver']
	print('executing {} ...'.format(cmd))
	os.system(cmd)
    print('All cmsDriver commands have been executed'
	  +' and the cmsRun configuration files created.\n'
	  +' Please check for errors and if all is ok, type "y" and press enter'
	  +' to submit the jobs.')
    go = raw_input()
    if not go=='y':
	sys.exit()

topdir = os.path.abspath(os.getcwd())
# set up the working directory for this job
commands = []
commands.append( 'cd {}'.format(workingdir) )
commands.append( 'export X509_USER_PROXY={}'.format(proxy) )
os.chdir( workingdir )
# loop over processing steps
for i,step in enumerate(steps):
    # copy the existing configuration file 
    # OR add cmsDriver command to job
    if not run_cmsdriver_in_job:
	os.system('cp {} {}'.format(os.path.join(topdir,step['conffile']), workingdir))
    else:
	commands.append(step['cmsdriver'])
    # add the cmsRun command
    commands.append('cmsRun {}'.format(step['conffile']))
    # remove the input file for this step
    if i!=0: commands.append('rm {}'.format(step['filein']))

# submit commands as job
qt.submitCommandsAsQsubJob( commands, 'qjob_cmsrun.sh', 
    			    docmsenv=True, cmssw_version = 'CMSSW_10_2_25' )
# for testing: run locally
#for cmd in commands:
#    os.system(cmd)

# remove temporary files
if not run_cmsdriver_in_job:
    for step in steps:
	os.system('rm {}'.format(os.path.join(topdir,step['conffile'])))
