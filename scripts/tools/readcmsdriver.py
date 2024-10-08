###########################################################################
# simple functionality to parse a text file containing cmsDriver commands #
###########################################################################

import sys
import os

def readcmsdriver( filename ):
    cmsdriver = []
    with open(filename,'r') as f:
	lines = f.readlines()
    currentcmd = ''
    for line in lines:
	line = line.strip('\t\n\\ ')
	if len(line)==0: continue
	if line[0]=='#': continue
	if 'cmsDriver.py' in line:
	    if currentcmd!='': cmsdriver.append(currentcmd)
	    currentcmd = line
	else:
	    currentcmd += ' '+line
    if currentcmd!='': cmsdriver.append(currentcmd)
    return cmsdriver

if __name__=='__main__':
   
    filename = sys.argv[1] 
    cmds = readcmsdriver(filename)
    print('found {} commands:'.format(len(cmds)))
    for cmd in cmds:
	print(' - {}'.format(cmd))
