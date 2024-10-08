####################################
# submit a cmsRun command as a job #
####################################

import sys
import os
sys.path.append(os.path.abspath('/user/llambrec/jobtools'))
import condorTools as ct
import qsubTools as qt

if __name__=='__main__':

    cfgfile = sys.argv[1]

    command = 'cmsRun {}'.format(cfgfile)
    commands = [command]  
    print('submitting command: '+commands[-1])

    #ct.submitCommandsAsCondorJob( 'cjob_cmsrun', commands, docmsenv=True,
    #				    cmssw_version='CMSSW_10_2_25' )
    qt.submitCommandsAsQsubJob( commands, 'qjob_cmsrun.sh', docmsenv=True,
				cmssw_version='CMSSW_10_2_25',
				wall_time='168:00:00' )
 
