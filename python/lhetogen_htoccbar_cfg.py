#############################################
# hadronizer configuration file for H -> cc #
#############################################
# note: only used for testing, see lhetogen_htowd_cfg for the real deal


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
			'25:addChannel = 1 1.00 103 4 -4',
			'25:m0 = 125.0',
		    ),
		    parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
                                    )
		)
	    )   

ProductionFilterSequence = cms.Sequence(generator)
