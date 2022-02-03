import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

##-- Options that can be set on the command line 
options = VarParsing.VarParsing('analysis')

options.register ('input', # input text file with encoded weight groups                             
                'input/MinDelta_2p5_OddWeights.txt', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "input")           
options.register ('output', # output file with SQLite format                              
                'output/MinDelta_2p5_OddWeights.db', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "output")                                                               

options.parseArguments()

process = cms.Process("ProcessOne")

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('*'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('DEBUG')
    ),
    destinations = cms.untracked.vstring('cout')
)

process.source = cms.Source("EmptyIOVSource",
    lastValue = cms.uint64(100000000000),
    timetype = cms.string('runnumber'),
    firstValue = cms.uint64(100000000000),
    interval = cms.uint64(1)
)

process.load("CondCore.CondDB.CondDB_cfi")

process.CondDB.connect = 'sqlite_file:%s'%(options.output)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
  process.CondDB, 
  logconnect = cms.untracked.string('sqlite_file:log.db'),   
  toPut = cms.VPSet(
    cms.PSet(
      record = cms.string('EcalTPGOddWeightIdMapRcd'),
      tag = cms.string('EcalTPGOddWeightIdMap_test')
    )
  )
)

process.Test1 = cms.EDAnalyzer("ExTestEcalTPGOddWeightIdMapAnalyzer",
  record = cms.string('EcalTPGOddWeightIdMapRcd'),
  loggingOn= cms.untracked.bool(True),
  IsDestDbCheckedInQueryLog=cms.untracked.bool(True),
  SinceAppendMode=cms.bool(True),
  Source=cms.PSet(
    firstRun = cms.string('1'),
    lastRun = cms.string('10'),
    OnlineDBSID = cms.string(''),
    OnlineDBUser = cms.string(''),
    OnlineDBPassword = cms.string(''),
    LocationSource = cms.string(''),
    Location = cms.string(''),
    GenTag = cms.string(''),
    RunType = cms.string(''),
#    fileType = cms.string('xml'),
    fileType = cms.string('txt'),
#    fileName = cms.string('EcalTPGOddWeightIdMap.xml'),
    fileName = cms.string(options.input),
  )                            
)

process.p = cms.Path(process.Test1)
