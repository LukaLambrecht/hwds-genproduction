##########################################################
# script to chain cmsDriver and cmsRun commands in a job #
##########################################################

import sys
import os
sys.path.append('/user/llambrec/jobtools')
import condorTools as ct
import qsubTools as qt

# get input args from command line
if len(sys.argv)==1:
    print('Required command line args:')
    print(' - input file')
    print(' - working directory')
    sys.exit()
elif len(sys.argv)!=3:
    raise Exception('ERROR: wrong number of command line args')

# process input args
inputfile = os.path.abspath(sys.argv[1])
if not os.path.exists(inputfile):
    raise Exception('ERROR: input file file {} does not exist.'.format(inputfile))
subdir = os.path.abspath(sys.argv[2])
if os.path.exists(subdir):
    raise Exception('ERROR: working directory {} already exists.'.format(subdir)
		    +' If you want to overwrite, you need to first remove it explicitly.')
os.makedirs(subdir)

# set proxy location
proxy = '/user/llambrec/proxy/x509up_u23078'

# cmsDriver commands
# note: remove the --filein argument, it will be added automatically!
# note: remove the --fileout argument, it will be added automatically!
# note: remove the --python_filename argument, it will be added automatically!
# note: make sure they all have the --no_exec argument
# note: make sure to have a valid proxy for commands that need DAS
cmsdriver = []
cmsdriver.append('cmsDriver.py \
--eventcontent PREMIXRAW \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--datatier GEN-SIM-RAW \
--pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" \
--conditions 102X_upgrade2018_realistic_v15 \
--step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 \
--procModifiers premix_stage2 \
--geometry DB:Extended \
--datamix PreMix \
--era Run2_2018 \
--no_exec \
--mc \
-n 1000')
cmsdriver.append('cmsDriver.py \
--eventcontent AODSIM \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--datatier AODSIM \
--conditions 102X_upgrade2018_realistic_v15 \
--step RAW2DIGI,L1Reco,RECO,RECOSIM,EI \
--procModifiers premix_stage2 \
--era Run2_2018 \
--runUnscheduled \
--no_exec \
--mc \
-n 1000')
cmsdriver.append('cmsDriver.py \
--eventcontent MINIAODSIM \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--datatier MINIAODSIM \
--conditions 102X_upgrade2018_realistic_v15 \
--step PAT \
--geometry DB:Extended \
--era Run2_2018 \
--runUnscheduled \
--no_exec \
--mc \
-n 1000')

# make the commands
commands = []
commands.append( 'cd {}'.format(subdir) )
commands.append( 'export X509_USER_PROXY={}'.format(proxy) )
os.chdir( subdir )
for i,cmd in enumerate(cmsdriver):
    filein = 'gensim_to_miniaodsim_step{}.root'.format(i-1)
    if i==0: filein = inputfile
    fileout = 'gensim_to_miniaodsim_step{}.root'.format(i)
    if i==len(cmsdriver)-1: fileout = 'gensim_to_miniaodsim_stepfinal.root'
    conffilename = 'cmsrun_conf_step_{}.py'.format(i)
    cmd += ' --filein file:{}'.format(filein)
    cmd += ' --fileout file:{}'.format(fileout)
    cmd += ' --python_filename {}'.format(conffilename)
    commands.append(cmd)
    commands.append('cmsRun {}'.format(conffilename))

# submit commands as job
qt.submitCommandsAsQsubJob( commands, 'qjob_cmsrun.sh', 
			    docmsenv=True, cmssw_version = 'CMSSW_10_2_25' )

# for testing: run locally
#for cmd in commands:
#    os.system(cmd)
