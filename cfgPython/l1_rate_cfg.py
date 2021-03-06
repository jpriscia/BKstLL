# import dill # needed in order to serialise lambda functions, need to be installed by the user. See http://stackoverflow.com/questions/25348532/can-python-pickle-lambda-functions
from collections import OrderedDict

import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config     import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
from CMGTools.RootTools.utils.splitFactor import splitFactor

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer         import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount    import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector        import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer    import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer       import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer     import GeneratorAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer     import LHEWeightAnalyzer
        
# Tau-tau analysers        
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer      import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.JetAnalyzer          import JetAnalyzer

# WTau3Mu analysers
from CMGTools.BKstLL.analyzers.L1RateAnalyzer               import L1RateAnalyzer    
from CMGTools.BKstLL.analyzers.L1RateTreeProducer           import L1RateTreeProducer

# import samples, signal
from CMGTools.BKstLL.samples.zerobias import ZeroBias_2017F

puFileMC   = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Moriond17_PU25ns_V1.root'
puFileData = '/afs/cern.ch/user/a/anehrkor/public/Data_Pileup_2016_271036-284044_80bins.root'

###################################################
###                   OPTIONS                   ###
###################################################
# Get all heppy options; set via "-o production" or "-o production=True"
# production = True run on batch, production = False (or unset) run locally
production         = getHeppyOption('production' , False)
pick_events        = getHeppyOption('pick_events', False)
###################################################
###               HANDLE SAMPLES                ###
###################################################
samples = [ZeroBias_2017F]

for sample in samples:
    sample.triggers  = ['HLT_ZeroBias_v%d' %i for i in range(1, 10)]
    sample.splitFactor = splitFactor(sample, 1e5)
    sample.puFileData = puFileData
    sample.puFileMC   = puFileMC

selectedComponents = samples

###################################################
###                  ANALYSERS                  ###
###################################################
eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=[
         270651544 ,
         685112686 ,
         578098843 ,
         319964730 ,
         144176365 ,
         155607171 ,
          47904360 ,
         196590218 ,
        1040634440 ,
         891877909 ,
         891572013 ,
         950544174 ,
         954243056 ,
         241846498 ,
         600269532 ,
         635462156 ,
         216450941 ,
         694776303 ,
         773635111 ,
         353462095 ,
         121181049 ,
         691880912 ,
        1043024190 ,
          11742081 ,
         698778193 ,
         112482815 ,
         422864985 ,
         427182711 ,
         848727806 ,
         947299043 ,
         497395225 ,
         146784021 ,
         556866174 ,
         278604090 ,
         519764385 ,
         968218247 ,
         660689359 ,
         732476041 ,
         765161901 ,
         813241572 ,
         978998680 ,
         185699573 ,
        1032022681 ,
        1032583535 ,
        1032525490 ,
         408752927 ,
         407724174 ,
         408983530 ,
         738831113 ,
          56482447 ,
         110540676 ,
          52119284 ,
         311430236 ,
         653755340 ,
         541193330 ,
         772841952 ,
         772836449 ,
         701224506 ,
         702978127 ,
         138603598 ,
         870667207 ,
         439120312 ,
         616502913 ,
         920258045 ,
         978270550 ,
          60020555 ,
         815945572 ,
         866252133 ,
        1026947670 ,
          17161695 ,
         711858099 ,
         724430255 ,
         750260588 ,
         479358239 ,
          69903184 ,
         352943658 ,
         389866509 ,
         639927666 ,
         909743818 ,
         910180069 ,
         418429393 ,
    ]
)

triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=True,
    usePrescaled=True,
    triggerResultsHandle=('TriggerResults', '', 'HLT'),
    triggerObjectsHandle=('slimmedPatTrigger', '', 'RECO'),
)

jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True
)

mainAna = cfg.Analyzer(
    L1RateAnalyzer,
    name = 'L1RateAnalyzer',
    onlyBX0 = True, # BE CAREFUL!
)

# see SM HTT TWiki
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016#Jet_Energy_Corrections
jetAna = cfg.Analyzer(
    JetAnalyzer,
    name              = 'JetAnalyzer',
    jetCol            = 'slimmedJets',
    jetPt             = 20.,
    jetEta            = 4.7,
    relaxJetId        = False, # relax = do not apply jet ID
    relaxPuJetId      = True, # relax = do not apply pileup jet ID
    jerCorr           = False,
    puJetIDDisc       = 'pileupJetId:fullDiscriminant',
    recalibrateJets   = False, # don't recalibrate if you take the latest & greatest samples
    applyL2L3Residual = 'MC',
    mcGT              = '80X_mcRun2_asymptotic_2016_TrancheIV_v8',
    dataGT            = '80X_dataRun2_2016SeptRepro_v7',
    selectedLeptons   = [],
    #jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
)

treeProducer = cfg.Analyzer(
    L1RateTreeProducer,
    name = 'L1RateTreeProducer',
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    eventSelector,
    jsonAna,
    triggerAna,
    vertexAna,
    pileUpAna,
    jetAna,
    mainAna,
    treeProducer,
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = ZeroBias_2017F
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
#     comp.files           = comp.files[20:40]

preprocessor = None

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = preprocessor,
    events_class = Events
)

printComps(config.components, True)