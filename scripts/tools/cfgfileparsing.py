######################################################################
# tools for post-processing configuration files created by cmsDriver #
######################################################################

import sys
import os

def setrandomseed( cfgfilepath, seed, verbose=True ):
    ### set the random seed in a configuration file
    # more info here: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGeneration
    # note: it is not very clearly mentioned on the twiki page above,
    #       but it seems that the random seed should be set for all modules being run;
    #       in most cases this is just "generator", 
    #       but a notable exception is "externalLHEProducer"!
    #       it is not fully clear whether that seed needs to be set explicitly,
    #       apart from the one for "generator".
    # to do: check if there are potentially more modules that might need
    #        explicitly setting the random seed.
    # to do: check if this crashes for files that do not contain externalLHEProducer,
    #        and if so, fix by using hasattr check.
    
    # check arguments
    if not os.path.exists(cfgfilepath):
	raise Exception('ERROR in setrandomseed: file {} does not exist.'.format(cfgfilepath))
    if not isinstance(seed, int):
	raise Exception('ERROR in setrandomseed: seed must be an int; found {}'.format(seed)
			+' (of type {})'.format(type(seed)))
    if seed<=0:
	raise Exception('ERROR in setrandomseed: seed must be > 0, found {}.'.format(seed))

    # define expressions to add/replace
    toreplace = {}
    # random seed for multipurpose "generator" module
    template = 'process.RandomNumberGeneratorService.generator.initialSeed'
    expr = 'process.RandomNumberGeneratorService.generator.initialSeed = {}'.format(seed)
    expr += '; print("MSG from tools/cfgfileparsing.setrandomseed'
    expr += ': setting generator.intialseed to {}")'.format(seed)
    toreplace[template] = expr
    # random seed for externalLHEProducer
    template = 'process.RandomNumberGeneratorService.externalLHEProducer.initialSeed'
    expr = 'process.RandomNumberGeneratorService.externalLHEProducer.initialSeed'
    expr += ' = {}'.format(seed)
    expr += '; print("MSG from tools/cfgfileparsing.setrandomseed'
    expr += ': setting externalLHEProducer.intialseed to {}")'.format(seed)
    toreplace[template] = expr

    # find if the random seed was already set and overwrite
    setseeds = []
    lines = []
    with open( cfgfilepath, 'r' ) as f:
	lines = f.readlines()
    for i,line in enumerate(lines):
	for template,expr in toreplace.items():
	    if template in line:
		if verbose: print('WARNING in setrandomseed:'
				+' random seed was already set in {},'.format(cfgfilepath)
				+' overwriting...')
		lines[i] = expr
		setseeds.append(template)

    # if the seed was not yet set, add the setting
    for template,expr in toreplace.items():
	if template not in setseeds:
	    if verbose: print('MESSAGE in setrandomseed:'
			    +' setting random seed in file {}'.format(cfgfilepath))
	    lines.append('\n')
	    lines.append(expr+'\n')

    # re-write the file
    with open( cfgfilepath, 'w' ) as f:
	for line in lines:
	    f.write(line)


if __name__=='__main__':
    
    cfgfile = sys.argv[1]
    seed = int(sys.argv[2])
    setrandomseed( cfgfile, seed )  
