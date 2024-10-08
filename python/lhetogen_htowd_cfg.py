#############################################
# hadronizer configuration file for H -> WD #
#############################################
# references: 
# - tutorials on private MC production 
#   https://docs.google.com/document/d/1YghFcqPGS8lx4OIpHWtpNHD8keQQf1vL5XtAP4TJBuo/edit 
#   https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO 
# - generator fragment for GluGluHToZphi sample 
#   https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer15wmLHEGS-02636&page=0&shown=6815871 

# to do:
# - check if setting of decay channels behaves as expected
# - check CUEP8M1 vs CP5?
# - check PSweight settings
# - check if adding of multiple decay channels is done correctly


import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                maxEventsToPrint = cms.untracked.int32(1),
                pythiaPylistVerbosity = cms.untracked.int32(1),
                filterEfficiency = cms.untracked.double(1.0),
                pythiaHepMCVerbosity = cms.untracked.bool(False),
		comEnergy = cms.double(13000.),
                PythiaParameters = cms.PSet(
		    pythia8CommonSettingsBlock,
		    pythia8CUEP8M1SettingsBlock,
		    pythia8PowhegEmissionVetoSettingsBlock,
		    processParameters = cms.vstring(
			'POWHEG:nFinal = 1',
			'25:onMode = off',
			'25:addChannel = 1  1.00   103   24   -431',
			#'25:addChannel = 1  1.00   103   -24  431',
			'25:m0 = 125.0',
			'24:onMode = off',
			'24:onIfMatch = -11 12',
			'24:onIfMatch = -13 14',
			'24:onIfMatch = -15 16',
			'-24:onMode = off',
                        '-24:onIfMatch = 11 -12',
                        '-24:onIfMatch = 13 -14',
                        '-24:onIfMatch = 15 -16',
			# PSweights
			'UncertaintyBands:doVariations = on',
			# 3 sets of variations for ISR&FSR up/down
			# reduced sqrt(2)/(1/sqrt(2)), default 2/0.5 
			# and conservative 4/0.25 variations
			'UncertaintyBands:List = {isrRedHi isr:muRfac=0.707,fsrRedHi fsr:muRfac=0.707,isrRedLo isr:muRfac=1.414,fsrRedLo fsr:muRfac=1.414,isrDefHi isr:muRfac=0.5, fsrDefHi fsr:muRfac=0.5,isrDefLo isr:muRfac=2.0,fsrDefLo fsr:muRfac=2.0,isrConHi isr:muRfac=0.25, fsrConHi fsr:muRfac=0.25,isrConLo isr:muRfac=4.0,fsrConLo fsr:muRfac=4.0}',
			'UncertaintyBands:MPIshowers = on',
			'UncertaintyBands:overSampleFSR = 10.0',
			'UncertaintyBands:overSampleISR = 10.0',
			'UncertaintyBands:FSRpTmin2Fac = 20',
			'UncertaintyBands:ISRpTmin2Fac = 1'
		    ),
		    parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
                                    )
		)
	    )   

ProductionFilterSequence = cms.Sequence(generator)
