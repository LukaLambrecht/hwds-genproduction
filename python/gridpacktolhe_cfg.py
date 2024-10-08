##########################################
# generic gridpack to lhe file processor #
##########################################
# reference: see here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PowhegBOXPrecompiled
# this externalLHEProducer is an alternative to the ./runcmsgrid.sh executable

import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer('ExternalLHEProducer',
    scriptName = cms.FileInPath("GeneratorInterface/LHEInterface/data/run_generic_tarball.sh"),
    outputFile = cms.string('cmsgrid_final.lhe'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/gg_H_quark-mass-effects_NNPDF30_13TeV_M125/v2/gg_H_quark-mass-effects_NNPDF30_13TeV_M125_tarball.tar.gz'),
    nEvents = cms.untracked.uint32(100)
    )
