######################################################################
# Submit scheduled jobs prepared by gridpack_to_miniaodsim_submit.py #
######################################################################

import sys
import os
import json
sys.path.append('../tools')
import optiontools as opt

if __name__=='__main__':

    options = []
    options.append( opt.Option('jobdir', vtype='path', required=True) )
    options.append( opt.Option('exename', required=True) )
    options.append( opt.Option('maxrunningjobs', vtype='int', required=True) )
    options.append( opt.Option('sleeptime', vtype='int', default=300) )
    options.append( opt.Option('overwrite', vtype='bool', default=False) )
    options.append( opt.Option('resubmit', vtype='bool', default=False) )
    options.append( opt.Option('logfile', 
	default='log_gridpack_to_miniaodsim_submit_scheduled.txt') )
    options = opt.OptionCollection( options )
    if len(sys.argv)==1:
        print('Use with following options:')
        print(options)
        sys.exit()
    else:
        options.parse_options( sys.argv[1:] )
        print('Found following configuration:')
        print(options)

    # hard coded options
    failtags = '\'["Begin Fatal Exception", "fatal system signal"]\''

    # make basic command
    scheduler_command = 'python ../tools/submitscheduler.py'
    scheduler_command += ' --jobdir {}'.format(options.jobdir)
    scheduler_command += ' --exename {}'.format(options.exename)
    scheduler_command += ' --maxrunningjobs {}'.format(options.maxrunningjobs)
    scheduler_command += ' --sleeptime {}'.format(options.sleeptime)
    scheduler_command += ' --overwrite {}'.format(options.overwrite)
    scheduler_command += ' --resubmit {}'.format(options.resubmit)
    scheduler_command += ' --failtags {}'.format(failtags)

    # redirect stdout and stderr
    scheduler_command += ' &>{}'.format(options.logfile)

    # run in background
    scheduler_command = 'nohup '+scheduler_command+' &'

    os.system(scheduler_command)
