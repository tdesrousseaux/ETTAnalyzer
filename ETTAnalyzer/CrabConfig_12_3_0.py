
"""
16 August 2021 
Abraham Tishelman-Charny 

The purpose of this crab configuration file is to run the ETTAnalyzer over many CMSSW data files in parallel. 
crab submit -c CrabConfig_12_1_0_pre3.py 

IMPORTANT: must be run with submit_crab.sh or delay scan lines must be commented
"""
# import os
# Choose dataset to re-emulate:
# Dataset = "2022_FR"
Dataset = "Run scan" # 2021 Pilot Beam double weights runs: Full Readout
# Dataset = "Run2_FR" # 306425: 2017F. 324725: 2018D
# Dataset = "ZeroBias2018C"

DatasetInfo = {
    "2022_FR" : [["352912"], "Run_352912", "123X_dataRun3_HLT_v7"],
    "PilotBeam2021" : [["346446", "346447"], "Runs_346446_346447_PilotBeam_2021", "123X_dataRun3_HLT_v7"], 
    "ZeroBias2018C" : [None, None, None],
    "Run2_FR" : [["324725", "306425"], "Runs_324725_306425_FullReadoutData", "103X_dataRun2_v6"],
    "Run scan" : [["366713"], "Run_366713", "123X_dataRun3_HLT_v7"]
}

runs, DatasetLabel, UserGlobalTag = DatasetInfo[Dataset]

# Configuration parameters 
# inDir = "/afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/CMSSW_12_1_0_pre3/src/ETTAnalyzer/ETTAnalyzer/"
inDir = "/afs/cern.ch/user/t/tdesrous/CMSSW_13_0_3/src/ETTAnalyzer/ETTAnalyzer/"
OverrideWeights = 0 # override weights and TPmode of global tag with user input sqlite files 
oneFile = 0 # Run over one file as a test (recommended before running over large datasets to test incompatibility issues)
WeightsWP = "2p5Prime"  # odd weights working point. Options: [2p5Prime, 0p5Prime] 
ODD_PF = 0 # 0: No ODD peak finder. 1: With ODD peak finder
addFilePrefix = 0 # Add "file:" to start of file paths 
removeEOSprefix = 1 
RecoMethod = "weights" # options: Multifit, weights
if(Dataset == "2022_FR" or Dataset == "PilotBeam2021" or Dataset == "Run scan"): 
    ERA = "Run3"
else: 
    ERA = "Run2"

if(ODD_PF): 
    TPMode_file = "EcalTPG_TPMode_Run3_zeroingOddPeakFinder.db"
    TPMode_Tag = "EcalTPG_TPMode_Run3_zeroingOddPeakFinder"
    ODD_PF_string = "WithOddPeakFinder"
else: 
    TPMode_file = "EcalTPG_TPMode_Run3_zeroing.db"
    TPMode_Tag = "EcalTPG_TPMode_Run3_zeroing"
    ODD_PF_string = "WithoutOddPeakFinder"

print("Configuration parameters:")
print("oneFile:",oneFile)
print("WeightsWP:",WeightsWP)
print("TPMode_file:",TPMode_file)
print("ODD_PF_string:",ODD_PF_string)
print("RecoMethod:",RecoMethod)

CMS_files = []
print("Adding CMS files...")

# By run number 
# for run in runs:
#      print("Run",run)
#      text_file_path = "RunsAndFiles/Files_Run_%s.txt"%(run)
#      with open(text_file_path) as f: # https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
#          content = f.readlines()
#          content = [x.strip() for x in content] 
#          for file in content:
#              if(addFilePrefix): file_path = "file:%s"%(file)
#              else: 
#                  if(removeEOSprefix): file = file.replace("/eos/cms", "")
#                  file_path = file 

#              CMS_files.append("root://xrootd-cms.infn.it/" + file_path)

# Delay scans : only one delay at a time or all using a bash script
# delay = -6
import os
delay = int(os.environ["DELAY"])


text_file_path = "Scan_files/Scan_delay_%s.txt"%(delay)
with open(text_file_path) as f:
    content = f.readlines()
    content = [x.strip() for x in content] 
    for file in content:
        CMS_files.append("root://xrootd-cms.infn.it/" + file)
        # CMS_files.append(file)

# To get 2018D ZeroBias data files 
"""
Nblocks = 11 # Max: 11 
##-- By block number 
for block_i in range(0, Nblocks):
    print "On block",block_i
    text_file_path = "RunsAndFiles/Files_Block_%s.txt"%(block_i)
    with open(text_file_path) as f: 
        content = f.readlines()
        content = [x.strip() for x in content] 
        for file in content:
            CMS_files.append(file)  

# for computing lumi 
# https://twiki.cern.ch/twiki/bin/view/CMS/AbrahamTishelmanCharnyHomepage#Checking_Dataset_Luminosity
# export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
# pip install --install-option="--prefix=$HOME/.local" brilws
# https://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html
# voms 
# http://opendata.cern.ch/docs/cms-guide-luminosity-calculation ?

##-- brilcalc lumi -r 320038            

"""

if(oneFile):
    CMS_files = [CMS_files[0]] # take first file of files list 

print("Number of input files:",len(CMS_files))

# Crab configuration parameters
from CRABClient.UserUtilities import config
config = config()

oneFileStr = ""
if(oneFile): oneFileStr = "_oneFile"

# if(OverrideWeights): '{DatasetLabel}_{ODD_PF_string}_{RecoMethod}_{WeightsWP}ODDweights{oneFileStr}'.format(DatasetLabel=DatasetLabel, ODD_PF_string=ODD_PF_string, RecoMethod=RecoMethod, WeightsWP=WeightsWP, oneFileStr=oneFileStr)
# else: requestName = '{DatasetLabel}_{RecoMethod}_ReemulateFromGlobalTag{oneFileStr}'.format(DatasetLabel=DatasetLabel, RecoMethod=RecoMethod, oneFileStr=oneFileStr)
requestName = 'Scan_delay%sns'%(delay)

config.General.requestName = requestName
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True # Need this True to transfer output files, at least with eos output.
config.General.transferLogs = False 

# cmssw configuration file parameters 
# config.JobType.pyCfgParams = [
#                                 'OverrideWeights=%s'%(OverrideWeights), # whether or not to override weights from global tag 
#                                 'UserGlobalTag=%s'%(UserGlobalTag), # global tag 
#                                 'TPModeSqliteFile=%s'%(TPMode_file), # strip zeroing, with or without ODD PF configs to try: [EcalTPG_TPMode_Run3_zeroingOddPeakFinder.db, EcalTPG_TPMode_Run3_zeroing,db]
#                                 'OddWeightsGroupSqliteFile=OneEBOneEEset_adding2021Strips.db', # weights group for each strip - defines which set of ODD weights each strip should use 
#                                 'BarrelOnly=1', # only run over ECAL barrel 
#                                 'RunETTAnalyzer=1', # run ETTAnalyzer and save output root file 
#                                 'TPModeTag=%s'%(TPMode_Tag), # TPMode, aka electronics configuration
#                                 'OddWeightsSqliteFile=MinDelta_%s_OddWeights.db'%(WeightsWP), # Working points to try: [MinDelta_2p5Prime_OddWeights, MinDelta_0p5Prime_OddWeights.db]
#                                 'RecoMethod=%s'%(RecoMethod), # offline reco methods to try: [Multifit, weights] 
#                                 'era=%s'%(ERA),
#                                 'userMaxEvents=1000'
#                              ] 

config.JobType.pyCfgParams = [
                                'OverrideWeights=%s'%(OverrideWeights), # whether or not to override weights from global tag 
                                'UserGlobalTag=%s'%(UserGlobalTag), # global tag 
                                'TPModeSqliteFile=%s'%(TPMode_file), # strip zeroing, with or without ODD PF configs to try: [EcalTPG_TPMode_Run3_zeroingOddPeakFinder.db, EcalTPG_TPMode_Run3_zeroing,db]
                                'OddWeightsGroupSqliteFile=weights/output/OneEBOneEEset.db', # weights group for each strip - defines which set of ODD weights each strip should use 
                                'BarrelOnly=0', # only run over ECAL barrel 
                                'RunETTAnalyzer=1', # run ETTAnalyzer and save output root file 
                                'TPModeTag=%s'%(TPMode_Tag), # TPMode, aka electronics configuration
                                'OddWeightsSqliteFile=ZeroCandidateSet', # Working points to try: [MinDelta_2p5Prime_OddWeights, MinDelta_0p5Prime_OddWeights.db]
                                'RecoMethod=%s'%(RecoMethod), # offline reco methods to try: [Multifit, weights] 
                                'era=%s'%(ERA)
                            ] 


config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '%s/ETTAnalyzer_cfg_12_3_0.py'%(inDir)

# Splitting
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

# Output directory / file naming
config.Data.outputPrimaryDataset = '%s%s'%(DatasetLabel, oneFileStr)

if(OverrideWeights): outputDatasetTag = 'ETTAnalyzer_CMSSW_12_3_0_DoubleWeights_%sRecoMethod_StripZeroingMode_%s_%sODDweights'%(RecoMethod, ODD_PF_string, WeightsWP) # 3 DOF to vary
else: outputDatasetTag = 'ETTAnalyzer_CMSSW_12_3_0_DoubleWeights_ReemulateFromGlobalTag'
config.Data.outputDatasetTag = outputDatasetTag
config.Data.outLFNDirBase = '/store/user/tdesrous/Scan_delay_%s/'%(delay) 
config.Data.publication = False 

config.Data.userInputFiles = CMS_files 

# config.Site.whitelist = ['T2_CH_CERN'] ##-- Eventually had to change from 'T2_FR_GRIF_LLR' whitelist to this 
# config.Site.storageSite = 'T2_CH_CERN'
config.Site.whitelist = ['T2_FR_GRIF_LLR'] ##-- Eventually had to change from 'T2_FR_GRIF_LLR' whitelist to this 
config.Site.storageSite = 'T2_FR_GRIF_LLR'

# input files 
config.JobType.inputFiles = [
                            # ODD weights working points
                            '%s/weights/output/MinDelta_2p5Prime_OddWeights.db'%(inDir),
                            '%s/weights/output/MinDelta_0p5Prime_OddWeights.db'%(inDir),

                            # TPModes
                            '%s/TPModes/output/EcalTPG_TPMode_Killing.db'%(inDir),
                            #  '%s/TPModes/output/EcalTPG_TPMode_Run3_zeroingOddPeakFinder.db'%(inDir),

                            # Misc
                            '%s/weights/output/OneEBOneEEset_adding2021Strips.db'%(inDir), # OddWeightsGroup - defines odd weights to be used by each ECAL strip 
                            '%s/ConfigParams.py'%(inDir) # To define cmssw config options 
                            ]    

# print("hostname: " + os.uname()[1])