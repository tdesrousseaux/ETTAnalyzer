########################################################################################################################
##-- 14 May 2021
##-- Abraham Tishelman-Charny 
##
## The purpose of this cmssw configuration file is to run over ZeroBias datasets In order to evaluate the expected gain from 
## double weights in CMS reconstruction.
##
##-- Dataset names:
## /ZeroBias/Run2018C-v1/RAW#162eb239-00fd-4f18-a0ba-58e02f83a1c0
## /ZeroBias/Run2018C-v1/RAW#88bfc4ee-4270-48d6-8127-a86a15ba3094
## /ZeroBias/Run2018C-v1/RAW#e0cfe3d4-0e42-4448-9a4f-6a421c827a99
## # 342333 --> MWGR 4 2021 
##-- Rucio related ids:
## f47cb01988e14e04802f52f38cf54759
## de2d9c7a898248bdafe802fbb4f134fe
## 53cce64c867f4faa9dd2963b0a2994ab
##
##-- cmsRun commands:
## Run ETT analyzer locally:
## ##-- run 2 config 
## cmsRun conf_11_3_0.py Debug=0 TPModeSqliteFile=TPModes/EcalTPG_TPMode_Run2_default.db TPModeTag=EcalTPG_TPMode_Run2_default TPinfoPrintout=0 userMaxEvents=1 OddWeightsSqliteFile=weights/ZeroCandidateSet.db BarrelOnly=1 RunETTAnalyzer=1
## 
## ##-- debug 
## cmsRun conf_11_3_0.py Debug=1 TPModeSqliteFile=TPModes/EcalTPG_TPMode_Run2_default.db TPModeTag=EcalTPG_TPMode_Run2_default TPinfoPrintout=1 userMaxEvents=1 OddWeightsSqliteFile=weights/ZeroCandidateSet.db BarrelOnly=1 RunETTAnalyzer=0
##
## Candidate double weights config 
## cmsRun conf_11_3_0.py Debug=0 TPModeSqliteFile=TPModes/EcalTPG_TPMode_Run3_zeroing.db TPModeTag=EcalTPG_TPMode_Run3_zeroing TPinfoPrintout=0 userMaxEvents=10000 OddWeightsSqliteFile=weights/ZeroCandidateSet.db BarrelOnly=1 RunETTAnalyzer=1 
##
##-- Misc notes: 
## crab status -d crab_projects/crab_ETT_Test --verboseErrors
## /afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/CMSSW_11_3_0/src/ECALDoubleWeights/ETTAnalyzer/crab_projects/crab_ETT_Test/crab.log
########################################################################################################################

##-- Imports 
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras
import os 

##-- Define cms process 
process = cms.Process("ECALDoubleWeightsETTAnalyzer",eras.Run2_2017)
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_readDBOffline_cff") ##-- Configuration for module which produces an EcalTrigPrimDigiCollection
# process.load("SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_CosmicsConfiguration_cff") 
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# process.GlobalTag.globaltag = '113X_dataRun2_relval_v1'
process.GlobalTag.globaltag = '113X_dataRun3_HLT_v3'
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('EventFilter.L1TRawToDigi.gtStage2Digis_cfi')

##-- Options that can be set on the command line 
options = VarParsing.VarParsing('analysis')

options.register ('userMaxEvents',
                -1, # default value
                VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                VarParsing.VarParsing.varType.int,           # string, int, or float
                "userMaxEvents")
options.register ('TPinfoPrintout',
                False, # default value
                VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                VarParsing.VarParsing.varType.bool,           # string, int, or float
                "TPinfoPrintout")
options.register ('Debug',
                False, # default value
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.bool,          
                "Debug")   
options.register ('BarrelOnly',
                # False, # default value
                True, # default value
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.bool,          
                "BarrelOnly")                                
options.register ('TPModeSqliteFile',
                # 'EcalTPG_TPMode_Run2_default.db',
                'EcalTPG_TPMode_Run3_zeroing.db',
                # 'TPModes/EcalTPG_TPMode_Run2_default.db',
                # 'none.db', # default value -- 0 = Run 2 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "TPModeSqliteFile")    
options.register ('TPModeTag',
                # 'EcalTPG_TPMode_Run2_default', # default value -- 0 = Run 2 
                'EcalTPG_TPMode_Run3_zeroing', # default value -- 0 = Run 2 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "TPModeTag")  
options.register ('OddWeightsSqliteFile',                                        
                # 'weights/EcalTPGOddWeightIdMap.db', 
                'ZeroCandidateSet.db', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "OddWeightsSqliteFile") 
options.register ('RunETTAnalyzer', ##-- If true, produce output ntuple with ETTAnalyzer 
                # False, # default value
                True, # default value
                VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                VarParsing.VarParsing.varType.bool,           # string, int, or float
                "RunETTAnalyzer")     
options.register ('inFile',                                        
                # 'weights/EcalTPGOddWeightIdMap.db', 
                '', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "inFile")   
options.register ('RecoMethod', ##-- Offline energy reconstruction method                               
                'weights', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "RecoMethod")                                               

options.register ('Printerval', ##-- How often to print event information  
                99999, # default value
                VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                VarParsing.VarParsing.varType.int,           # string, int, or float
                "Printerval")     
options.parseArguments()


process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(record = cms.string("EcalTPGLinearizationConstRcd"),
         ),
    cms.PSet(record = cms.string("EcalTPGPedestalsRcd"), 
         )
)

# Load the odd weights
#process.load("CondCore.CondDB.CondDB_cfi")
# input database (in this case the local sqlite file)



# process.EcalOnTheFlyTPGconf = cms.ESSource("PoolDBESSource",
#     DumpStat=cms.untracked.bool(True),
#     toGet = cms.VPSet(cms.PSet(
#                             record = cms.string('EcalTPGOddWeightIdMapRcd'),
#                             tag = cms.string("EcalTPGOddWeightIdMap_test"),
#                             connect = cms.string('sqlite_file:%s'%(options.OddWeightsSqliteFile))
#                             # connect = cms.string('%s'%(options.OddWeightsSqliteFile))
#                         ),
#                     cms.PSet(
#                             record = cms.string('EcalTPGOddWeightGroupRcd'),
#                             tag = cms.string("EcalTPGOddWeightGroup_test"),
#                             # connect = cms.string('sqlite_file:weights/EcalTPGOddWeightGroup.db')
#                             connect = cms.string('sqlite_file:EcalTPGOddWeightGroup.db')
#                         ),
#                     cms.PSet(
#                             record = cms.string('EcalTPGTPModeRcd'),
#                             tag = cms.string(options.TPModeTag),
#                             connect = cms.string('sqlite_file:%s'%(options.TPModeSqliteFile))
#                         )
#     ),
# )

# process.es_prefer_ecalweights = cms.ESPrefer("PoolDBESSource","EcalOddWeights")

# ECAL Unpacker
process.load("EventFilter.EcalRawToDigi.EcalUnpackerMapping_cfi")
process.load("EventFilter.EcalRawToDigi.EcalUnpackerData_cfi")
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff') ##--  --> RawToDigi_cff --> Loads ecalTriggerPrimitiveDigis_cfi.py 
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('L1Trigger.Configuration.L1TReco_cff')
process.load('Configuration.EventContent.EventContent_cff')

process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step)

from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW
#,L1TEventSetupForHF1x1TPs  this last one is not in the release

#call to customisation function L1TReEmulFromRAW imported from L1Trigger.Configuration.customiseReEmul
#process = L1TReEmulFromRAW(process)
from EventFilter.L1TRawToDigi.caloStage2Digis_cfi import caloStage2Digis
process.rawCaloStage2Digis = caloStage2Digis.clone()
process.rawCaloStage2Digis.InputLabel = cms.InputTag('rawDataCollector')

##-- Create ECAL TP digis module 
process.ecalTriggerPrimitiveDigis = cms.EDProducer("EcalTrigPrimProducer",
   InstanceEB = cms.string('ebDigis'),
   InstanceEE = cms.string('eeDigis'),
   Label = cms.string('ecalDigis'),
#    Label = cms.string('ecalEBunpacker'), # # ecalEBunpacker, simEcalDigis two labels to try 
#    BarrelOnly = cms.bool(options.BarrelOnly),
   BarrelOnly = cms.bool(True),
   Famos = cms.bool(False),
   TcpOutput = cms.bool(False),
   Debug = cms.bool(options.Debug), ##-- Lots of printout 
   binOfMaximum = cms.int32(6), ## optional from release 200 on, from 1-10
   TPinfoPrintout = cms.bool(options.TPinfoPrintout),
#    TPmode = cms.uint32(options.TPmode) 
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.userMaxEvents) )
#process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( options.Printerval ) ##-- Printout run, lumi, event info
#process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( options.Printerval ) ##-- Printout run, lumi, event info
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 99999999 ) ##-- Printout run, lumi, event info
# process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1 ) ##-- Printout run, lumi, event info

##-- Get list of files 
# Direc = "/eos/cms/store/user/khurana/ECAL/edmFiles/%s/"%(options.SevLevel) 
# files = ["file:%s%s"%(Direc, f) for f in os.listdir(Direc) if os.path.isfile(os.path.join(Direc, f))]
# root://cms-xrd-global.cern.ch/
# copy a file from the grid: xrdcp 

files = []

##-- If a file is passed as a flag, run over it 
if(options.inFile != ""):
    print("inFile flag value found:")
    print(options.inFile)
    files.append(options.inFile)

##-- If not file is passed, process a default files from 2018 Zerobias data 
else:
    files = ["/store/data/Run2018C/ZeroBias/RAW/v1/000/320/063/00000/62F3929A-F08D-E811-8133-FA163E19E543.root"]

# files = ["file:Run_320026_Event_12323268.root"]
# files = ["/store/data/Run2018C/ZeroBias/RAW/v1/000/320/063/00000/62F3929A-F08D-E811-8133-FA163E19E543.root"]
# files = ["file:/eos/cms/store/data/Run2018C/ZeroBias/RAW/v1/000/320/065/00000/26A77465-FE8D-E811-B971-FA163E4200C7.root"] ##-- file from Run 320065 

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                files
                            )
                        )

##-- If running ETT Analyzer
if(options.RunETTAnalyzer):

    print("[conf_11_3_0.py] - Running ETT Analyzer")

    ##-- Create EDAnalyzer 
    process.tuplizer = cms.EDAnalyzer('ETTAnalyzer',
                                    ugtProducer = cms.InputTag("gtStage2Digis"),
                                    savePreFireInfo = cms.bool(False), 
                                    TPEmulatorCollection =  cms.InputTag("ecalTriggerPrimitiveDigis",""), ##-- Different name for full readout?
                                    # TPEmulatorCollection =  cms.InputTag("ecalTriggerPrimitiveDigis","ecalTriggerPrimitiveDigis"), ##-- Different name for full readout?
                                    useAlgoDecision = cms.untracked.string("initial"),
                                    firstBXInTrainAlgo = cms.untracked.string("L1_FirstCollisionInTrain"),
                                    lastBXInTrainAlgo = cms.untracked.string("L1_LastCollisionInTrain"),
                                    isoBXAlgo = cms.untracked.string("L1_IsolatedBunch"),
                                    TPCollection = cms.InputTag("ecalDigis","EcalTriggerPrimitives"), 
                                    ## for data 
                                    stage2CaloLayer2EGammaProducer = cms.InputTag("gtStage2Digis","EGamma"),
                                    ## for mc 
                                    #stage2CaloLayer2EGammaProducer = cms.InputTag("hltGtStage2Digis","EGamma"),
                                    
                                    ## For rechits 
                                    EcalRecHitCollectionEB = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                                    EcalRecHitCollectionEE = cms.InputTag("ecalRecHit","EcalRecHitsEE"),                                                                        
                                    
                                    ## for data on Raw
                                    EBdigis      = cms.InputTag("ecalDigis","ebDigis"),
                                    EEdigis      = cms.InputTag("ecalDigis","eeDigis"),
                                    
                                    ## for data on DIGIS : make sure why is this diff, w.r.t. RAW
                                    #EBdigis      = cms.InputTag("selectDigi","selectedEcalEBDigiCollection"),
                                    #EEdigis      = cms.InputTag("selectDigi","selectedEcalEEDigiCollection"),
                                    
                                    ## for mc
                                    #EBdigis      = cms.InputTag("simEcalDigis","ebDigis"),
                                    #EEdigis      = cms.InputTag("simEcalDigis","eeDigis"),
                                    genparticles = cms.InputTag("genParticles")
                                )

    ## Load appropriate processes for Rec Hits 
    process.load("Configuration/StandardSequences/Reconstruction_cff")

    if(options.RecoMethod == "Multifit"):
        print("Offline energy reconstruction to be performed with Multifit")
        ## Multifit 
        import RecoLocalCalo.EcalRecProducers.ecalMultiFitUncalibRecHit_cfi
        process.ecalUncalibHit =  RecoLocalCalo.EcalRecProducers.ecalMultiFitUncalibRecHit_cfi.ecalMultiFitUncalibRecHit.clone()
        process.ecalUncalibHit.algoPSet.activeBXs =cms.vint32(-5,-4,-3,-2,-1,0,1,2,3,4)
        process.ecalUncalibHit.algoPSet.useLumiInfoRunHeader = cms.bool (False )

    elif(options.RecoMethod == "weights"):
        print("Offline energy reconstruction to be performed with offline weights")
        ## Offline weights 
        import RecoLocalCalo.EcalRecProducers.ecalGlobalUncalibRecHit_cfi
        process.ecalUncalibHit = RecoLocalCalo.EcalRecProducers.ecalGlobalUncalibRecHit_cfi.ecalGlobalUncalibRecHit.clone()

    else:
        raise Exception("Unknown reconstruction method: %s"%(options.RecoMethod))

    process.load("RecoLocalCalo.EcalRecProducers.ecalRecHit_cfi")
    process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
    process.load("RecoLocalCalo.EcalRecProducers.ecalDetIdToBeRecovered_cfi")
    process.ecalRecHit.EBuncalibRecHitCollection = 'ecalUncalibHit:EcalUncalibRecHitsEB'
    process.ecalRecHit.EEuncalibRecHitCollection = 'ecalUncalibHit:EcalUncalibRecHitsEE'

    ##-- Used for output root files 
    process.TFileService = cms.Service("TFileService",
                                    fileName = cms.string("ETTAnalyzer_output.root")
                                    )

    ##-- Define Path Which includes necessary modules for ETTAnalyzer 
    process.p = cms.Path(
                         process.gtDigis*
                         process.RawToDigi*
                         process.L1Reco*
                         process.gtStage2Digis*
                         process.ecalTriggerPrimitiveDigis*
                         process.ecalUncalibHit*
                         process.ecalDetIdToBeRecovered*
                         process.ecalRecHit*
                         process.tuplizer
                    )

##-- If not running ETT Analyzer
else: 

    ##-- Define Path Without ETTAnalyzer modules 
    process.p = cms.Path(
                        process.L1Reco*
                        process.gtStage2Digis*
                        process.ecalTriggerPrimitiveDigis
                    )

##-- In either case, append process path to process schedule 
process.schedule.append(process.p)