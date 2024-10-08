#############################################################
# generator fragment for W->l+nu with a Ds meson gen filter #
#############################################################
# originally copied from here: 
# https://cms-pdmv.cern.ch/mcm/requests?prepid=SMP-RunIISummer15wmLHEGS-00120&page=0&shown=6553727
# but with modifications:
# - remove muon gen filter
# - replace gridpack (yet to be created)

import FWCore.ParameterSet.Config as cms

# link to cards:
# https://github.com/cms-sw/genproductions/tree/e30fc9c7d9226a2c96869c0ddbe5e65884afd013/bin/MadGraph5_aMCatNLO/cards/examples/wellnu012j_5f_NLO_FXFX

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/user/llambrec/CMSSW_10_2_25/src/Configuration/GenProduction/bin/MadGraph5_aMCatNLO/wellnu012j_5f_NLO_FXFX_slc6_amd64_gcc700_CMSSW_10_2_25_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8aMCatNLOSettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 999.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 30.',
	    # (this is the actual merging scale)
            'JetMatching:doFxFx = on',
            'JetMatching:qCutME = 10.',
	    # (this must match the ptj cut in the lhe generation step)
            'JetMatching:nQmatch = 5', #
	    # (4 corresponds to 4-flavour scheme (no matching of b-quarks), 
	    #  5 for 5-flavour scheme)
            'JetMatching:nJetMax = 2', 
	    # (number of partons in born matrix element for highest multiplicity)
            'TimeShower:mMaxGamma = 4.0',
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8aMCatNLOSettings',
                                    'processParameters',
                                    )
    )
)


gendsfilter = cms.EDFilter("MCSmartSingleParticleFilter",
                           MinPt = cms.untracked.vdouble(0.1, 0.1),
                           MinEta = cms.untracked.vdouble(-8.,-8.),
                           MaxEta = cms.untracked.vdouble(8.,8.),
                           ParticleID = cms.untracked.vint32(431,-431),
                           Status = cms.untracked.vint32(2,2),
                           # Decay cuts are in mm
                           MaxDecayRadius = cms.untracked.vdouble(2000.,2000.),
                           MinDecayZ = cms.untracked.vdouble(-4000.,-4000.),
                           MaxDecayZ = cms.untracked.vdouble(4000.,4000.)
)


ProductionFilterSequence = cms.Sequence(generator*gendsfilter)
