#############################################
# script to wrap cmsDriver command in a job #
#############################################

import sys
import os
sys.path.append('/user/llambrec/jobtools')
import condorTools as ct
import qsubTools as qt

# get input args from command line
if len(sys.argv)==1:
    print('Required command line args:')
    print(' - cmsRun configuration file')
    print(' - working subdirectory')
    print(' - number of parallel submissions')
    sys.exit()
elif len(sys.argv)!=4:
    raise Exception('ERROR: wrong number of command line args')

# process input args
conffile = os.path.abspath(sys.argv[1])
if not os.path.exists(conffile):
    raise Exception('ERROR: configuration file {} does not exist.'.format(conffile))
subdir = os.path.abspath(sys.argv[2])
if os.path.exists(subdir):
    raise Exception('ERROR: working directory {} already exists.'.format(subdir)
		    +' If you want to overwrite, you need to first remove it explicitly.')
os.makedirs(subdir)
njobs = int(sys.argv[3])

# make cmsRun command
cmsrun = 'cmsRun {}'.format(os.path.basename(conffile))

# submit the commands
for jobn in range(1,njobs+1):
    thissubdir = os.path.join(subdir,'job{}'.format(jobn))
    os.makedirs(thissubdir)
    commands = []
    commands.append( 'cd {}'.format(thissubdir) )
    commands.append( 'cp {} .'.format(conffile) )
    commands.append( cmsrun )
    qt.submitCommandsAsQsubJob( commands, 'qjob_cmsrun.sh', 
			    docmsenv=True, cmssw_version = 'CMSSW_10_2_25' )
