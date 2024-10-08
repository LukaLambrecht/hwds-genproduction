################################################################
# check a given directory for .sh.e files and find failed jobs #
################################################################

import sys
import os

def check_start_done(filename, filetext, doprint=True):
    nstarted = filetext.count('### starting ###')
    if(nstarted==0):
	if doprint:
	    print('### WARNING: file '+fname+' contains no valid starting tag.')
	    print('             does the process write the correct tags to the error files?')
        return 1
    ndone = filetext.count('### done ###')
    if(nstarted==ndone): return 0
    if doprint:
	print('found issue in file '+filename+':')
	print('   '+str(nstarted)+' commands were initiated.')
	print('   '+str(ndone)+' seem to have finished normally.')
    return 1

def check_content(filename, filetext, contentlist, doprint=True):
    contains = False
    for content in contentlist:
	if filetext.count(content)>0:
	    contains = True
	    if doprint:
		print('found issue in file '+filename+':')
		print('   file contains the sequence "'+content+'",'
		      +' which was flagged as problematic.')
    if contains: return 1
    return 0

def has_failed(filename, doprint=True, 
		do_check_start_done=True, do_check_content=True,
		contentlist=[]):
    with open(filename,'r') as f:
	c = f.read()
    failed = False
    if do_check_start_done:
	if check_start_done(filename,c, doprint=doprint): failed=True
    if do_check_content:
	if check_content(filename,c, doprint=doprint, contentlist=contentlist): failed=True
    return failed


if __name__=='__main__':

    # set search directory
    searchdir = os.path.abspath('.')
    if len(sys.argv)==1:
	print('searching for error log files in current directory...')
    else:
	searchdir = os.path.abspath(sys.argv[1])
	print('searching for error log files in directory {}...'.format(searchdir))

    # find error log files
    efiles = []
    for root, dirs, files in os.walk(searchdir):
	for fname in files:
	    if '.sh.e' in fname:
		efiles.append(os.path.join(root,fname))
    print('found '+str(len(efiles))+' error log files.')
    print('start scanning...')

    nerror = 0
    for fname in efiles:
	failed = has_failed(fname, 
			do_check_start_done=False,
			do_check_content=True,
			contentlist=[
				    'Begin Fatal Exception',
				    'fatal system signal'
				    ])
	if failed: nerror += 1

    if(nerror==0):
	print('no problematic files were found by this automated checking!')
	print('(however this does not guarantee everything went completely fine...)')
    else:
	print('found {} problematic files!'.format(nerror))
