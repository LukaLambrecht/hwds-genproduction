##################################
# merge root files in EDM format #
##################################
# note that for this case, hadd seems not to work correctly!
# however, this script has a similar interface and should accomplish the same result

# note: does not work yet, as edmCopyPickMerge seems to be intended for data,
#       skipping duplicate events (which is unwanted behaviour for MC)

import sys
import os

outputfile = sys.argv[1]
inputfiles = sys.argv[2:]

cmd = 'edmCopyPickMerge'
# add input files
cmd += ' inputFiles='
for f in inputfiles[:-1]: cmd += 'file:{},'.format(f)
cmd += 'file:{}'.format(inputfiles[-1])
# add output file
cmd += ' outputFile={}'.format(outputfile)

print('running following command:')
print(cmd)
os.system(cmd)
