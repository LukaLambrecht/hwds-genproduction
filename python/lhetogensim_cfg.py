############################################################
# configuration file to shower LHE events to GEN-SIM level #
############################################################
# for now, simply copied from here:
# https://docs.google.com/document/d/1YghFcqPGS8lx4OIpHWtpNHD8keQQf1vL5XtAP4TJBuo/edit 

import FWCore.ParameterSet.Config as cms
import os
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
			maxEventsToPrint = cms.untracked.int32(1),
			pythiaPylistVerbosity = cms.untracked.int32(1),
			filterEfficiency = cms.untracked.double(1.0),
			pythiaHepMCVerbosity = cms.untracked.bool(False),
			comEnergy = cms.double(13000.),
			PythiaParameters = cms.PSet(
			    pythia8CommonSettingsBlock,
			    pythia8CP5SettingsBlock,
			    parameterSets = cms.vstring('pythia8CommonSettings',							'pythia8CP5Settings')
			    )
			)
