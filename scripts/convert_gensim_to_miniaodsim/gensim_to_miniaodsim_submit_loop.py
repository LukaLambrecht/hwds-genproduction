##########################################
# looper for gensim_to_miniaod_submit.py #
##########################################

import sys
import os
sys.path.append('/user/llambrec/jobtools')
import condorTools as ct
import qsubTools as qt

# get input args from command line
if len(sys.argv)==1:
    print('Required command line args:')
    print(' - input directory')
    print(' - working directory')
    sys.exit()
elif len(sys.argv)!=3:
    raise Exception('ERROR: wrong number of command line args')

# process input args
inputdir = os.path.abspath(sys.argv[1])
if not os.path.exists(inputdir):
    raise Exception('ERROR: input directory {} does not exist!'.format(inputdir))
njobs = len([f for f in os.listdir(inputdir) if 'job' in f])
subdir = os.path.abspath(sys.argv[2])
if os.path.exists(subdir):
    raise Exception('ERROR: working directory {} already exists.'.format(subdir)
                    +' If you want to overwrite, you need to first remove it explicitly.')
os.makedirs(subdir)

# make the jobs
print(inputdir)

for jobn in range(1,njobs+1):
    thisinputdir = os.path.join(inputdir,'job{}'.format(jobn))
    inputfiles = ([os.path.join(thisinputdir,f) 
		    for f in os.listdir(thisinputdir)
		    if (f[-5:]=='.root' and 'inLHE' not in f)])
    if len(inputfiles)!=1:
	print('WARNING: unexpected number of input files, ignoring...')
	continue
    inputfile = inputfiles[0]
    thissubdir = os.path.join(subdir,'job{}'.format(jobn))
    cmd = 'python gensim_to_miniaodsim_submit.py'
    cmd += ' {}'.format(inputfile)
    cmd += ' {}'.format(thissubdir)
    print(cmd)
    os.system(cmd)
