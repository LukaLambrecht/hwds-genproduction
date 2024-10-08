##############################################################
# Directory to perform conversion of LHE files to GEN format #
##############################################################

NOTE: superseded by convert_gridpack_to_gen,
      that takes a gridpack directly as an input and generates LHE events + pythia decays,
      no need for intermediate explicit/manual .lhe file production.

Temporary structure, not sure yet what the best approach is to organize this.
Current approach:

Step 1:
create LHE files with MadGraph, Powheg, or another event generator.
see e.g. the Madgraph_tools and Powheg_tools in my home directory.
result of this step: an LHE file conventionally named cmsgrid_final.lhe
(both for Madgraph and Powheg).
examples:
    - Configuration/GenProduction/bin/Powheg/gg_H_quark-mass-effects_slc6_amd64_gcc700_CMSSW_10_2_25_tutorial_ggH_runcmsgrid/cmsgrid_final.lhe
    - Configuration/GenProduction/bin/MadGraph5_aMCatNLO/tzq_top_ll_5f_NLO_slc6_amd64_gcc700_CMSSW_10_2_24_patch1_tarball_runcmsgrid/cmsgrid_final.lhe

Step 2:
manually copy the lhe file you want to process to this directory
(or a subdirectory of it)

Step 3:
create a hadronizer configuration files in Configuration/GenProduction/python
with the settings you need.
see the examples present in that directory, or here:
https://docs.google.com/document/d/1YghFcqPGS8lx4OIpHWtpNHD8keQQf1vL5XtAP4TJBuo/edit 

Step 4:
run a cmsDriver.py command.
see cmsdriver_commands.txt for examples

Step 5:
run cmsRun on the file created by cmsDriver
TO DO: put this part in job submission!

The result is a GEN level root file.
See e.g. here https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenIntro  
and here https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGeneration 
for some info on how to analyze this file.
