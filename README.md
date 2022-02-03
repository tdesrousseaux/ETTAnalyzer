# ETT Analyzer

The purpose of the ETT (ECAL Trigger Team) Analyzer is to process RAW CMS data files for ETT studies and re-emulation. Possible studies include: 
- Evaluation of double weights configurations with 2018 data and 2021 CMS commissioning data
- Studies of ECAL TP pre-firing
- Studies of 5BX L1 TP readout
- `<Your creative idea here>` 

Current CMSSW version compatibility: `CMSSW_12_1_0_pre3`

## Setup

To setup the repository in `CMSSW_12_1_0_pre3`:

	export SCRAM_ARCH=slc7_amd64_gcc900 
	cmsrel CMSSW_12_1_0_pre3
	cd CMSSW_12_1_0_pre3/src
	cmsenv
	git cms-init
	
Then one should clone the repository either via HTTPS protocol:

	git clone https://github.com/CMS-ECAL-Trigger-Group/ETTAnalyzer.git
	
or SSH protocol:
	
	git clone git@github.com:CMS-ECAL-Trigger-Group/ETTAnalyzer.git
	
And proceed to build:
	
	cd ETTAnalyzer/ETTAnalyzer
	scram b -j  
	
## Examples and functionalities 

- Some ETTAnalyzer running examples can be found in the [Examples README](Examples.md).
- Encode and save custom ODD FENIX weights as SQLite files to use for re-emulation in the [weights directory](https://github.com/CMS-ECAL-Trigger-Group/ETTAnalyzer/tree/main/ETTAnalyzer/weights).
- Save custom TPModes as SQLite files to use for re-emulation in the [TPModes directory](https://github.com/CMS-ECAL-Trigger-Group/ETTAnalyzer/tree/main/ETTAnalyzer/TPModes).
