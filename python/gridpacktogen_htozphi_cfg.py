##################################################################
# configuration file for direct gridpack to gen-level processing #
##################################################################
# the intermediate cmsrungrid processing producing the cmsgrid_final.lhe is skipped
# note: copied from here: 
# https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer15wmLHEGS-02636&page=0&shown=1099518443647
# see the same link for the appropriate cmsDriver command
# modifications:
# - different path to (custom) gridpack
# - smaller number of events (for testing)
#   (note: can also be modified in cmsDriver command using --number option!)


import FWCore.ParameterSet.Config as cms

# link to cards:
# https://github.com/cms-sw/genproductions/blob/6718f234d90e34ac43b683e323a3edd6e8aa72e2/bin/Powheg/production/V2/13TeV/Higgs/gg_H_quark-mass-effects_NNPDF30_13TeV/gg_H_quark-mass-effects_NNPDF30_13TeV_M125.input


externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    #args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/gg_H_quark-mass-effects_NNPDF30_13TeV_M125/v2/gg_H_quark-mass-effects_NNPDF30_13TeV_M125_tarball.tar.gz'),
    args = cms.vstring( '/storage_mnt/storage/user/llambrec/CMSSW_10_2_25/src/Configuration/GenProduction/bin/Powheg/gg_H_quark-mass-effects_slc6_amd64_gcc700_CMSSW_10_2_25_tutorial_ggH.tgz' ),
    #args = cms.vstring( '/storage_mnt/storage/user/llambrec/CMSSW_10_2_25/src/Configuration/GenProduction/bin/Powheg/gridpacks_20210805/gg_H_quark-mass-effects_slc6_amd64_gcc700_CMSSW_10_2_25_tutorial_ggH.tgz' ),
    #args = cms.vstring( '/storage_mnt/storage/user/llambrec/CMSSW_10_2_25/src/Configuration/GenProduction/bin/Powheg/gridpacks_other/gg_H_quark-mass-effects_NNPDF30_13TeV_M125_tarball.tar.gz' ),
    #args = cms.vstring( '/storage_mnt/storage/user/llambrec/CMSSW_10_2_25/src/Configuration/GenProduction/bin/Powheg/gridpacks_other/gg_H_quark-mass-effects_slc6_amd64_gcc700_CMSSW_10_2_12_patch1_gg_H_quark-mass-effects_NNPDF31_13TeV_M125.tgz' ),
    nEvents = cms.untracked.uint32(10),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

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
            '25:addChannel = 1  1.00   103   23   333',
	    '25:onIfMatch = 23 333', # custom addition based on twiki page, see notes
            '25:m0 = 125.0',
            '23:onMode = off',
            '23:onIfMatch = 11 -11',
            '23:onIfMatch = 13 -13',
            '23:onIfMatch = 15 -15',
            #PSweights
        'UncertaintyBands:doVariations = on',
# 3 sets of variations for ISR&FSR up/down
# Reduced sqrt(2)/(1/sqrt(2)), Default 2/0.5 and Conservative 4/0.25 variations
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
