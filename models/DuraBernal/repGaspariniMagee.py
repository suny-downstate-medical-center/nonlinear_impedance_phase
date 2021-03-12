# import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers\
from netpyne import sim, specs
import numpy as np

#batch num
# import sys
# batch_num = sys.argv[5]

###########################################################################
# CFG stuff

import pickle, json

cfg = specs.SimConfig()  

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------
	
# cfg.simLabel = input_sec + '_at_' + sys.argv[6] + '_at_' + sys.argv[7]
cfg.simLabel = 'asyn_v_syn'# + input_sec

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
#cfg.duration = 1.5*1e3 
# cfg.duration = 1.6*1e3 # for plotting single cell
# cfg.duration = 12900+1100 # for plotting single cell
cfg.dt = 0.05
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = 0
cfg.createNEURONObj = True
cfg.createPyStruct = True 
cfg.connRandomSecFromList = False  # set to false for reproducibility  
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.1

cfg.includeParamsLabel = False
cfg.printPopAvgRates = True

cfg.checkErrors = 0


#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
allpops = ['IT2','PV2','SOM2','IT4','IT5A','PV5A','SOM5A','IT5B','PT5B','PV5B','SOM5B','IT6','CT6','PV6','SOM6']
cfg.cellsrec = 0
if cfg.cellsrec == 0:  # record all cells
	cfg.recordCells = ['all']
elif cfg.cellsrec == 1:  # record one cell of each pop
	cfg.recordCells = 	[(pop,0) for pop in allpops]
elif cfg.cellsrec == 2:  # record selected cells
	cfg.recordCells = [('IT2',10), ('IT5A',10), ('PT5B',10), ('PV5B',10), ('SOM5B',10)]
elif cfg.cellsrec == 3:  # record selected cells
	cfg.recordCells = [('IT5A',0), ('PT5B',0)]
elif cfg.cellsrec == 4:  # record selected cells
	cfg.recordCells = [] #[('PT5B_1',0), ('PT5B_ZD',0)]

cfg.recordTraces = {'v_soma': {'sec':'soma', 'loc': 0.5, 'var':'v'},
                    'nmdai': {'sec': 'apic_13', 'loc': 0.5, 'synMech': 'NMDA', 'var':'iNMDA'},
                    'ampai': {'sec': 'apic_13', 'loc': 0.5, 'synMech': 'AMPA', 'var': 'i'},
					'v_dend' : {'sec' : 'apic_13', 'loc': 0.5, 'var': 'v'}}
# cfg.recordTraces = {'V_soma' : {'sec' : 'soma', 'loc': 0.5, 'var': 'v'},
#                     'dend_52' : {'sec' : 'dend_52', 'loc' : 0.5, 'var' : 'v'},
#                     'apic_45' : {'sec' : 'apic_45', 'loc' : 0.5, 'var' : 'v'},
#                     'dend_35' : {'sec' : 'dend_35', 'loc' : 0.5, 'var' : 'v'},
                    # 'apical_60' : { 'sec' : 'apical_60', 'loc' : 0.5, 'var' : 'v'}}

#cfg.recordLFP = [[150, y, 150] for y in range(200,1300,100)]

cfg.recordStim = True  
cfg.recordTime = True
cfg.recordStep = 0.025


#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------

# cfg.saveFolder = '/oasis/scratch/comet/ckelley/temp_project/netstim_weightSweep_noise/'
cfg.saveFolder = '/home/craig/L5PYR_Resonance/' #'/oasis/scratch/comet/ckelley/temp_project/gasparini_magee/'
cfg.savePickle = False
cfg.saveJson = False
cfg.saveDat = False
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams']#, 'net']
cfg.backupCfgFile = None #['cfg.py', 'backupcfg/'] 
cfg.gatherOnlySimData = True
cfg.saveCellSecs = 1
cfg.saveCellConns = 1

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
# cfg.analysis['plotRaster'] = {'include':['all'], 'timeRange':[0,1000], 'saveFig': True, 'showFig': False, 'labels': 'overlay', 'popRates': True, 'orderInverse': True, 'figSize': (12,10),'lw': 0.3, 'markerSize':3, 'marker': '.', 'dpi': 300} 
cfg.analysis['plotTraces'] = {'include': [], 'oneFigPer': 'trace', 'overlay': 1, 'figSize': (12,8), 'fontsiz' : 12, 'timeRange': [0,1000], 'saveFig': False, 'showFig': False,\
  							 'colors': [[0,0,1],[0,0.502,0]]}#, 'ylim': [-90, 15]}

#------------------------------------------------------------------------------
# Cells
#------------------------------------------------------------------------------
cfg.cellmod =  {'IT2': 'HH_reduced',
				'IT4': 'HH_reduced',
				'IT5A': 'HH_full',
				'IT5B': 'HH_reduced',
				'PT5B': 'HH_full',
				'IT6': 'HH_reduced',
				'CT6': 'HH_reduced'}

cfg.ihModel = 'migliore'  # ih model
cfg.ihGbar = 1.0  # multiplicative factor for ih gbar in PT cells
cfg.ihGbarZD = 0.25 # multiplicative factor for ih gbar in PT cells
cfg.ihGbarBasal = 1.0 # 0.1 # multiplicative factor for ih gbar in PT cells
cfg.ihlkc = 0.2 # ih leak param (used in Migliore)
cfg.ihlkcBasal = 1.0
cfg.ihlkcBelowSoma = 0.01
cfg.ihlke = -86  # ih leak param (used in Migliore)
cfg.ihSlope = 14*2

cfg.removeNa = False  # simulate TTX; set gnabar=0s
cfg.somaNa = 5
cfg.dendNa = 0.3
cfg.axonNa = 7
cfg.axonRa = 0.005

cfg.gpas = 0.5  # multiplicative factor for pas g in PT cells
cfg.epas = 0.9  # multiplicative factor for pas e in PT cells

#------------------------------------------------------------------------------
# Synapses
#------------------------------------------------------------------------------
cfg.synWeightFractionEE = [0.5, 0.5] # E->E AMPA to NMDA ratio
cfg.synWeightFractionEI = [0.5, 0.5] # E->I AMPA to NMDA ratio
cfg.synWeightFractionSOME = [0.9, 0.1] # SOM -> E GABAASlow to GABAB ratio

cfg.synsperconn = {'HH_full': 5, 'HH_reduced': 1, 'HH_simple': 1}

cfg.excTau2Factor = 1.0

#------------------------------------------------------------------------------
# Network 
#------------------------------------------------------------------------------
cfg.singleCellPops = 1 # Create pops with 1 single cell (to debug)
cfg.weightNorm = 1  # use weight normalization
cfg.weightNormThreshold = 4.0  # weight normalization factor threshold

cfg.addConn = 0
cfg.scale = 1.0
cfg.sizeY = 1350.0
cfg.sizeX = 60.0
cfg.sizeZ = 60.0

cfg.EEGain = 1.0
cfg.EIGain = 1.0
cfg.IEGain = 1.0
cfg.IIGain = 1.0

cfg.IEdisynapticBias = None  # increase prob of I->Ey conns if Ex->I and Ex->Ey exist 

#------------------------------------------------------------------------------
## E->I gains
cfg.EPVGain = 1.0
cfg.ESOMGain = 1.0

#------------------------------------------------------------------------------
## I->E gains
cfg.PVEGain = 1.0
cfg.SOMEGain = 1.0

#------------------------------------------------------------------------------
## I->I gains
cfg.PVIGain = 1.0
cfg.SOMIGain = 1.0

#------------------------------------------------------------------------------
## I->E/I layer weights (L2/3+4, L5, L6)
cfg.IEweights = [1.0, 1.0, 1.0]
cfg.IIweights = [1.0, 1.0, 1.0]

cfg.IPTGain = 1.0

#------------------------------------------------------------------------------
# Subcellular distribution
#------------------------------------------------------------------------------
cfg.addSubConn = 0

cfg.ihSubConn = 0
cfg.ihX = 4
cfg.ihY = 14


#------------------------------------------------------------------------------
# Long range inputs
#------------------------------------------------------------------------------
cfg.addLongConn = 0
cfg.numCellsLong = 1000  # num of cells per population
cfg.noiseLong = 1.0  # firing rate random noise
cfg.delayLong = 5.0  # (ms)
cfg.weightLong = 0.5  # corresponds to unitary connection somatic EPSP (mV)
cfg.startLong = 0  # start at 0 ms
cfg.ratesLong = {'TPO': [0,2], 'TVL': [0,2], 'S1': [0,2], 'S2': [0,2], 'cM1': [0,2], 'M2': [0,2], 'OC': [0,2]}

#cfg.ratesLong = {'TPO': [0,2], 'TVL': [0,2], 'S1': [0,2], 'S2': 'cells/ssc-3_lowrate_spikes.json', 'cM1': [0,2], 'M2': [0,2], 'OC': [0,2]}
#cfg.ratesLong = {'TPO': [0,0.1], 'TVL': [0,0.1], 'S1': [0,0.1], 'S2': 'cells/ssc-3_lowrate_spikes.json', 'cM1': [0,0.1], 'M2': [0,0.1], 'OC': [0,0.1]}
#cfg.ratesLong = {'TPO': [0,0.1], 'TVL': [0,0.1], 'S1': 'cells/ssc-3_spikes.json', 'S2': [0,0.1], 'cM1': [0,0.1], 'M2': [0,0.1], 'OC': [0,0.1]}


## input pulses
cfg.addPulses = 0
cfg.pulse = {'pop': 'None', 'start': 2000, 'end': 2200, 'rate': 30, 'noise': 0.5}


#------------------------------------------------------------------------------
# Current inputs 
#------------------------------------------------------------------------------
cfg.addIClamp = 0

			  ## pop,   sec,   loc, start,dur, amp (nA)
cfg.IClamp1 = {'pop': 'PT5B', 'sec': 'dend_52', 'loc': 0.5, 'start': 1000, 'dur': 400, 'amp': 0.01}

cfg.groupWeight = 0.05
cfg.groupRate = 20

#------------------------------------------------------------------------------
# Network clamp
#------------------------------------------------------------------------------
cfg.netClamp = 0

# cfg.netClampConnsFile = '/oasis/scratch/comet/ckelley/temp_project/netpyne_test/v47_batch9_0.json'
# cfg.netClampSpikesFile = '/oasis/scratch/comet/ckelley/temp_project/netpyne_test/v47_batch5_1_1_2_0_1_1_1_0.json'
cfg.netClampPop = ['PT5B_1']
cfg.netClampGid = 5198
cfg.netClampCreateAllConns = 1

############################################################################
# netParams stuff
############################################################################

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

netParams.version = 53

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = cfg.scale # Scale factor for number of cells
netParams.sizeX = cfg.sizeX # x-dimension (hofor weight in weights:
#  rizontal length) size in um   
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = cfg.sizeZ # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume


#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
netParams.scaleConnWeight = 1.0 # Connection weight scale factor (default if no model specified)
netParams.scaleConnWeightModels = {'HH_simple': 1.0, 'HH_reduced': 1.0, 'HH_full': 1.0} #scale conn weight factor for each cell model
netParams.scaleConnWeightNetStims = 1.0 #0.5  # scale conn weight factor for NetStims
netParams.defaultThreshold = 0.0 # spike threshold, 10 mV is NetCon default, lower it for all cells
netParams.defaultDelay = 2.0 # default conn delay (ms)
netParams.propVelocity = 500.0 # propagation velocity (um/ms)
netParams.probLambda = 100.0  # length constant (lambda) for connection probability decay (um)
netParams.convertCellShapes = True  # convert stylized geoms to 3d points


#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
cellModels = ['HH_simple', 'HH_reduced', 'HH_full']
layer = {'2': [0.1,0.29], '4': [0.29,0.37], '5A': [0.37,0.47], '24':[0.1,0.37], '5B': [0.47,0.8], '6': [0.8,1.0], 
'longTPO': [2.0,2.1], 'longTVL': [2.1,2.2], 'longS1': [2.2,2.3], 'longS2': [2.3,2.4], 'longcM1': [2.4,2.5], 'longM2': [2.5,2.6], 'longOC': [2.6,2.7]}  # normalized layer boundaries

#------------------------------------------------------------------------------
## Load cell rules previously saved using netpyne format
cellParamLabels = [ 'IT2_reduced', 'IT4_reduced', 'IT5A_reduced', 'IT5B_reduced',
    'PT5B_reduced',  'IT6_reduced', 'CT6_reduced', 'PV_simple', 'SOM_simple','IT5A_full']#, 'PT5B_full'] #  # list of cell rules to load from file
loadCellParams = [] #cellParamLabels
saveCellParams = 0

for ruleLabel in loadCellParams:
    netParams.loadCellParamsRule(label=ruleLabel, fileName='cells/'+ruleLabel+'_cellParams.pkl')

#------------------------------------------------------------------------------
# Specification of cell rules not previously loaded
# Includes importing from hoc template or python class, and setting additional params

#------------------------------------------------------------------------------
# Reduced cell model params (6-comp) 
reducedCells = {}  # layer and cell type for reduced cell models

reducedSecList = {  # section Lists for reduced cell model
    'alldend':  ['Adend1', 'Adend2', 'Adend3', 'Bdend'],
    'spiny':    ['Adend1', 'Adend2', 'Adend3', 'Bdend'],
    'apicdend': ['Adend1', 'Adend2', 'Adend3'],
    'perisom':  ['soma']}

for label, p in reducedCells.items():  # create cell rules that were not loaded 
    if label not in loadCellParams:
        cellRule = netParams.importCellParams(label=label, conds={'cellType': label[0:2], 'cellModel': 'HH_reduced', 'ynorm': layer[p['layer']]},
        fileName='cells/'+p['cname']+'.py', cellName=p['cname'], cellArgs={'params': p['carg']} if p['carg'] else None)
        dendL = (layer[p['layer']][0]+(layer[p['layer']][1]-layer[p['layer']][0])/2.0) * cfg.sizeY  # adapt dend L based on layer
        for secName in ['Adend1', 'Adend2', 'Adend3', 'Bdend']: cellRule['secs'][secName]['geom']['L'] = dendL / 3.0  # update dend L
        for k,v in reducedSecList.items(): cellRule['secLists'][k] = v  # add secLists
        if cfg.weightNorm:
            netParams.addCellParamsWeightNorm(label, 'conn/'+label+'_weightNorm.pkl', threshold=cfg.weightNormThreshold)  # add weightNorm

        # set 3D pt geom
        offset, prevL = 0, 0
        somaL = netParams.cellParams[label]['secs']['soma']['geom']['L']
        for secName, sec in netParams.cellParams[label]['secs'].items():
            sec['geom']['pt3d'] = []
            if secName in ['soma', 'Adend1', 'Adend2', 'Adend3']:  # set 3d geom of soma and Adends
                sec['geom']['pt3d'].append([offset+0, prevL, 0, sec['geom']['diam']])
                prevL = float(prevL + sec['geom']['L'])
                sec['geom']['pt3d'].append([offset+0, prevL, 0, sec['geom']['diam']])
            if secName in ['Bdend']:  # set 3d geom of Bdend
                sec['geom']['pt3d'].append([offset+0, somaL, 0, sec['geom']['diam']])
                sec['geom']['pt3d'].append([offset+sec['geom']['L'], somaL, 0, sec['geom']['diam']])        
            if secName in ['axon']:  # set 3d geom of axon
                sec['geom']['pt3d'].append([offset+0, 0, 0, sec['geom']['diam']])
                sec['geom']['pt3d'].append([offset+0, -sec['geom']['L'], 0, sec['geom']['diam']])   


        if saveCellParams: netParams.saveCellParamsRule(label=label, fileName='cells/'+label+'_cellParams.pkl')

#------------------------------------------------------------------------------
# PT5B full cell model params (700+ comps)
if 'PT5B_full' not in loadCellParams:
    ihMod2str = {'harnett': 1, 'kole': 2, 'migliore': 3}
    cellRule = netParams.importCellParams(label='PT5B_full', conds={'cellType': 'PT', 'cellModel': 'HH_full'},
      fileName='cells/PTcell.hoc', cellName='PTcell', cellArgs=[ihMod2str[cfg.ihModel], cfg.ihSlope], somaAtOrigin=True)
    nonSpiny = ['apic_0', 'apic_1']
    netParams.addCellParamsSecList(label='PT5B_full', secListName='perisom', somaDist=[0, 50])  # sections within 50 um of soma
    netParams.addCellParamsSecList(label='PT5B_full', secListName='apic_upper', somaDist=[300, 900])  # sections within 300-900 um of soma
    netParams.addCellParamsSecList(label='PT5B_full', secListName='apic_lower', somaDist=[0, 300])  # sections within 0-300 um of soma
    netParams.addCellParamsSecList(label='PT5B_full', secListName='below_soma', somaDistY=[-600, 0])  # sections within 0-300 um of soma
    for sec in nonSpiny: cellRule['secLists']['perisom'].remove(sec)
    cellRule['secLists']['alldend'] = [sec for sec in cellRule.secs if ('dend' in sec or 'apic' in sec)] # basal+apical
    cellRule['secLists']['apicdend'] = [sec for sec in cellRule.secs if ('apic' in sec)] # apical
    cellRule['secLists']['basaldend'] = [sec for sec in cellRule.secs if ('dend' in sec)] # apical
    cellRule['secLists']['spiny'] = [sec for sec in cellRule['secLists']['alldend'] if sec not in nonSpiny]
    # Adapt ih params based on cfg param
    for secName in cellRule['secs']:
        for mechName,mech in cellRule['secs'][secName]['mechs'].items():
            if mechName in ['ih','h','h15', 'hd']: 
                mech['gbar'] = [g*cfg.ihGbar for g in mech['gbar']] if isinstance(mech['gbar'],list) else mech['gbar']*cfg.ihGbar
                if cfg.ihModel == 'migliore':   
                    mech['clk'] = cfg.ihlkc  # migliore's shunt current factor
                    mech['elk'] = cfg.ihlke  # migliore's shunt current reversal potential
                if secName.startswith('dend'): 
                    mech['gbar'] *= cfg.ihGbarBasal  # modify ih conductance in soma+basal dendrites
                    mech['clk'] *= cfg.ihlkcBasal  # modify ih conductance in soma+basal dendrites
                if secName in cellRule['secLists']['below_soma']: #secName.startswith('dend'): 
                    mech['clk'] *= cfg.ihlkcBelowSoma  # modify ih conductance in soma+basal dendrites
                    
    # Reduce dend Na to avoid dend spikes (compensate properties by modifying axon)
    for secName in cellRule['secLists']['alldend']:
        cellRule['secs'][secName]['mechs']['nax']['gbar'] = 0.0153130368342 * cfg.dendNa #0.25 
        cellRule['secs'][secName]['mechs']['pas']['e'] *= cfg.epas
        cellRule['secs'][secName]['mechs']['pas']['g'] *= cfg.gpas
    cellRule['secs']['soma']['mechs']['nax']['gbar'] = 0.0153130368342  * cfg.somaNa
    cellRule['secs']['axon']['mechs']['nax']['gbar'] = 0.0153130368342  * cfg.axonNa #11  
    cellRule['secs']['axon']['geom']['Ra'] = 137.494564931 * cfg.axonRa #0.005 
    # Remove Na (TTX)
    if cfg.removeNa:
        for secName in cellRule['secs']:
            cellRule['secs'][secName]['mechs']['nax']['gbar'] = 0.0
    if cfg.weightNorm and not cfg.netClamp:
        netParams.addCellParamsWeightNorm('PT5B_full', 'conn/PT5B_full_weightNorm.pkl', threshold=cfg.weightNormThreshold)  # load weight norm
    # cellRule['secs']['apic_0']['weightNorm'] = [1e-6] # set temporarily to 0, so subConn rules determine if syns provide input or not
    if saveCellParams: netParams.saveCellParamsRule(label='PT5B_full', fileName='cells/PT5B_full_cellParams.pkl')


#------------------------------------------------------------------------------
## PT5B full cell model params (700+ comps)
if cfg.ihGbarZD is not None and 'PT5B_full2' not in loadCellParams:
    import copy
    cellRule = copy.deepcopy(netParams.cellParams['PT5B_full'].todict())
    cellRule['conds']['cellType'] = ['PT2']
    netParams.cellParams['PT5B_full2'] = cellRule
    for secName in cellRule['secs']:
        for mechName,mech in cellRule['secs'][secName]['mechs'].items():
            if mechName in ['ih','h','h15', 'hd']: 
                mech['gbar'] = [g/cfg.ihGbar*cfg.ihGbarZD for g in mech['gbar']] if isinstance(mech['gbar'],list) else mech['gbar']/cfg.ihGbar*cfg.ihGbarZD


#------------------------------------------------------------------------------
## PV cell params (3-comp)
if 'PV_simple' not in loadCellParams:
    cellRule = netParams.importCellParams(label='PV_simple', conds={'cellType':'PV', 'cellModel':'HH_simple'}, 
      fileName='cells/FS3.hoc', cellName='FScell1', cellInstance = True)
    cellRule['secLists']['spiny'] = ['soma', 'dend']
    netParams.addCellParamsWeightNorm('PV_simple', 'conn/PV_simple_weightNorm.pkl', threshold=cfg.weightNormThreshold)
    if saveCellParams: netParams.saveCellParamsRule(label='PV_simple', fileName='cells/PV_simple_cellParams.pkl')
    

#------------------------------------------------------------------------------
## SOM cell params (3-comp)
if 'SOM_simple' not in loadCellParams:
    cellRule = netParams.importCellParams(label='SOM_simple', conds={'cellType':'SOM', 'cellModel':'HH_simple'}, 
      fileName='cells/LTS3.hoc', cellName='LTScell1', cellInstance = True)
    cellRule['secLists']['spiny'] = ['soma', 'dend']
    netParams.addCellParamsWeightNorm('SOM_simple', 'conn/SOM_simple_weightNorm.pkl', threshold=cfg.weightNormThreshold)
    netParams.saveCellParamsRule(label='SOM_simple', fileName='cells/SOM_simple_cellParams.pkl')
    



#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------
## Local populations
netParams.popParams['PT5B'] = {'cellModel': cfg.cellmod['PT5B'], 'cellType': 'PT', 'ynormRange': layer['5B'], 'numCells':1}#, 'density': 0.5*density[('M1','E')][3]}#, 'xRange': [100,100], 'yRange': [735,735]}


if cfg.singleCellPops:
    for pop in netParams.popParams.values(): pop['numCells'] = 1

#------------------------------------------------------------------------------
## Long-range input populations (VecStims)
if cfg.addLongConn:
    ## load experimentally based parameters for long range inputs
    with open('conn/conn_long.pkl', 'r') as fileObj: connLongData = pickle.load(fileObj)
    #ratesLong = connLongData['rates']

    numCells = cfg.numCellsLong
    noise = cfg.noiseLong
    start = cfg.startLong

    longPops = ['TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']
    ## create populations with fixed 
    for longPop in longPops:
        netParams.popParams[longPop] = {'cellModel': 'VecStim', 'numCells': numCells, 'rate': cfg.ratesLong[longPop], 
                                        'noise': noise, 'start': start, 'pulses': [], 'ynormRange': layer['long'+longPop]}
        if isinstance(cfg.ratesLong[longPop], basestring): # filename to load spikes from
            spikesFile = cfg.ratesLong[longPop]
            with open(spikesFile, 'r') as f: spks = json.load(f)
            netParams.popParams[longPop].pop('rate')
            netParams.popParams[longPop]['spkTimes'] = spks


#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
netParams.synMechParams['NMDA'] = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': 15, 'tau2NMDA': 150, 'e': 0}
netParams.synMechParams['AMPA'] = {'mod':'MyExp2SynBB', 'tau1': 0.05, 'tau2': 5.3, 'e': 0}
netParams.synMechParams['exc'] = {'mod':'Exp2Syn', 'tau1': 0.05, 'tau2': 5.3*cfg.excTau2Factor, 'e': 0}
netParams.synMechParams['GABAB'] = {'mod':'MyExp2SynBB', 'tau1': 3.5, 'tau2': 260.9, 'e': -93} 
netParams.synMechParams['GABAA'] = {'mod':'MyExp2SynBB', 'tau1': 0.07, 'tau2': 18.2, 'e': -80}
netParams.synMechParams['GABAASlow'] = {'mod': 'MyExp2SynBB','tau1': 2, 'tau2': 100, 'e': -80}
netParams.synMechParams['GABAASlowSlow'] = {'mod': 'MyExp2SynBB', 'tau1': 200, 'tau2': 400, 'e': -80}

ESynMech = ['AMPA', 'NMDA']
SOMESynMech = ['GABAASlow','GABAB']
SOMISynMech = ['GABAASlow']
PVSynMech = ['GABAA']

#----------------------------------------------------------------------------
# Stim patterns from Gasparini & Magee
#----------------------------------------------------------------------------
# add stims
cfg.NetStims = []
cfg.addNetStimList = 1
cfg.addNetStim = 0
start = 1500

#---------------------------------
# Clustered
#---------------------------------
# all possible basal synapse locations
allsyns = []
# dend_list = ['apic_13', 'apic_89', 'apic_90', 'apic_91']
dend_list = ['apic_13']
# dend_list = ['dend_54', 'dend_55', 'dend_56', 'dend_57', 'dend_58']
# dend_list = netParams.cellParams['PT5B_full'].secLists.basal[52:56]
# dend_list = netParams.cellParams['PT5B_full'].secLists.basal[34:38]
# for sec in netParams.cellParams['PT5B_full'].secLists.basal:
for sec in dend_list:
    #  if netParams.cellParams['PT5B_full'].secs[sec]['geom']['nseg'] == 1:
    allsyns.append([sec, 0.5])
    #  else:
    #      nseg = netParams.cellParams['PT5B_full'].secs[sec]['geom']['nseg']
    #      for count, loc in enumerate(np.linspace(1/(nseg+1),nseg/(nseg+1),nseg)):
    #          allsyns.append([sec, loc])

delay = 0
for i in range(7):
    for syn in allsyns:
        stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['AMPA'], 'synMechWeightFactor': [1], 'start': start+delay, \
                        'rate': 71.4, 'noise': 0.2, 'number': 5, 'weight': [0.5], 'delay': 0}
        cfg.NetStims.append(stim)
    delay = delay + 140
delay = 70
for i in range(7):
    for i in range(4):
        stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': 'soma', 'loc': 0.5, 'synMech': ['GABAA'], 'synMechWeightFactor': [1], 'start': start+delay, \
                        'rate': 71.4, 'noise': 0.2, 'number': 5, 'weight': [0.5], 'delay': 0}
        cfg.NetStims.append(stim)
    delay = delay + 140

# #loops through window sizes, and number of synapses
# # n_choices = np.linspace(10, 100, 10, endpoint=True)
# n_choices = [24]
# # n_choices = np.linspace(90,110,21)
# # windows = [500, 250, 100, 50, 25, 10, 1]
# windows = [130]
# # windows = [500, 100, 50, 10, 1]
# # windows = [500]
# window_starts_basal = []
# syn_lists_basal = []
# for window in windows:
#     window_starts_basal.append(start)
#     for n in n_choices:
#         choices = np.random.choice(len(allsyns), int(n), replace=True)
#         syns = [allsyns[choice] for choice in choices]
#         syn_lists_basal.append(syns)
#         for syn in syns:
#             if window > 1:
#                 delay = np.random.randint(0,window) + np.random.rand()
#             else:
#                 delay = np.random.rand()
#             stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['AMPA', 'NMDA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#                     'interval': 10, 'noise': 0, 'number': 1, 'weight': [2.0, 2.0], 'delay': 1}
#             cfg.NetStims.append(stim)
#             # stim = {'pop': 'eeeD', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['NMDA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#             #         'interval': 10, 'noise': 0, 'number': 1, 'weight': [0.1], 'delay': 3}
#             # cfg.NetStims.append(stim)
#         start = start + 1000

# #---------------------------------
# # Distributed
# #---------------------------------
# # all possible basal synapse locations
# allsyns = []
# dend_list = netParams.cellParams['PT5B_full'].secLists.basal
# # for sec in netParams.cellParams['PT5B_full'].secLists.basal:
# for sec in dend_list:
#      if netParams.cellParams['PT5B_full'].secs[sec]['geom']['nseg'] == 1:
#          allsyns.append([sec, 0.5])
#      else:
#          nseg = netParams.cellParams['PT5B_full'].secs[sec]['geom']['nseg']
#          for count, loc in enumerate(np.linspace(1/(nseg+1),nseg/(nseg+1),nseg)):
#              allsyns.append([sec, loc])

# #loops through window sizes, and number of synapses
# # n_choices = np.linspace(10, 100, 10, endpoint=True)
# window_starts_apical = []
# syn_lists_apical = []
# for window in windows:
#     window_starts_apical.append(start)
#     for n in n_choices:
#         choices = np.random.choice(len(allsyns), int(n), replace=True)
#         syns = [allsyns[choice] for choice in choices]
#         syn_lists_apical.append(syns)
#         for syn in syns:
#             if window > 1:
#                 delay = np.random.randint(0,window)
#             else:
#                 delay = np.random.rand()
#             stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['AMPA','NMDA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#                     'interval': 10, 'noise': 0, 'number': 1, 'weight': [2.0, 2.0], 'delay': 1}
#             cfg.NetStims.append(stim)
#             # stim = {'pop': 'eeeD', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['NMDA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#             #         'interval': 10, 'noise': 0, 'number': 1, 'weight': [0.1], 'delay': 3}
#             # cfg.NetStims.append(stim)
#         start = start + 1000

# # all possible apical synapse locations
# allsyns = []
# dend_list = netParams.cellParams['PT5B_full'].secLists.apical
# # for sec in netParams.cellParams['PT5B_full'].secLists.basal:
# for sec in dend_list:
#      if netParams.cellParams['PT5B_full'].secs[sec]['geom']['nseg'] == 1:
#          allsyns.append([sec, 0.5])
#      else:
#          nseg = netParams.cellParams['PT5B_full'].secs[sec]['geom']['nseg']
#          for count, loc in enumerate(np.linspace(1/(nseg+1),nseg/(nseg+1),nseg)):
#              allsyns.append([sec, loc])

# #loops through window sizes, and number of synapses
# # n_choices = np.linspace(10, 100, 10, endpoint=True)
# window_starts_apical = []
# syn_lists_apical = []
# for window in windows:
#     window_starts_apical.append(start)
#     for n in n_choices:
#         choices = np.random.choice(len(allsyns), int(n), replace=True)
#         syns = [allsyns[choice] for choice in choices]
#         syn_lists_apical.append(syns)
#         for syn in syns:
#             if window > 1:
#                 delay = np.random.randint(0,window)
#             else:
#                 delay = np.random.rand()
#             stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['AMPA','NMDA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#                     'interval': 10, 'noise': 0, 'number': 1, 'weight': [2.0, 2.0], 'delay': 1}
#             cfg.NetStims.append(stim)
#             # stim = {'pop': 'eeeD', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['NMDA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#             #         'interval': 10, 'noise': 0, 'number': 1, 'weight': [0.1], 'delay': 3}
#             # cfg.NetStims.append(stim)
#         start = start + 1000
cfg.duration = 4000

# cluster vs distributed
# sec = 'dend_56'
# sec = 'apic_53'
# # nseg = netParams.cellParams['PT5B_full'].secs[sec]['geom']['nseg']
# nseg = 15
# # cluster_locs = np.linspace(1/(nseg+1),nseg/(nseg+1),nseg)
# cluster_locs = np.linspace(0.4, 0.6, nseg)
# dist_locs = np.linspace(1/(nseg+1),nseg/(nseg+1),nseg)
# choices = np.random.choice(len(allsyns), nseg, replace=False)

# choices = np.random.choice(len(allsyns), nseg, replace=False)


# clustered

    # for syn_loc in cluster_locs:
    #     delay = np.random.randint(0,window)
    #     stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': sec, 'loc': syn_loc, 'synMech': ['AMPA'], 'synMechWeightFactor': [1], 'start': start+delay, \
    #             'interval': 10, 'noise': 0, 'number': 1, 'weight': 0.25, 'delay': 1}
    #     cfg.NetStims.append(stim)
    # start = start + 2000

# distributed
# for window in windows:
#     for syn_loc in dist_locs:
#         delay = np.random.randint(0,window)
#         stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': sec, 'loc': syn_loc, 'synMech': ['AMPA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#                 'interval': 10, 'noise': 0, 'number': 1, 'weight': 0.25, 'delay': 1}
#         cfg.NetStims.append(stim)
#     start = start + 2000
# # distributed
# for window in windows:
#     for syn in syns:
#         delay = np.random.randint(0,window)
#         stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn_loc, 'synMech': ['AMPA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#                 'interval': 10, 'noise': 0, 'number': 1, 'weight': 0.1, 'delay': 1}
#         cfg.NetStims.append(stim)
#     start = start + 2000

# # choose locations
# syn_lists = []
# choices = np.random.choice(len(allsyns), 220, replace=False)
# syns = [allsyns[choice] for choice in choices]
# syn_lists.append(syns)
# syns = []
# choices = np.random.choice(len(allsyns), 110, replace=False)
# syns = [allsyns[choice] for choice in choices]
# syn_lists.append(syns)

# windows = [500, 50]
# for counter, window in enumerate(windows):
#     for syn in syn_lists[counter]:
#         delay = np.random.randint(0,window)
#         stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['AMPA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#                 'interval': 10, 'noise': 0, 'number': 1, 'weight': 0.1, 'delay': 1}
#         cfg.NetStims.append(stim)
#     start = start + 2000

# windows = np.linspace(500, 0, 20, endpoint=False)
# windows = [500, 50]
# for window in windows:
#     for syn in syns:
#         delay = np.random.randint(0,window)
#         stim = {'pop': 'PT5B', 'ynorm':[0.0, 1.0], 'sec': syn[0], 'loc': syn[1], 'synMech': ['AMPA'], 'synMechWeightFactor': [1], 'start': start+delay, \
#                 'interval': 10, 'noise': 0, 'number': 1, 'weight': 0.1, 'delay': 1}
#         cfg.NetStims.append(stim)
#     start = start + 2000
    
# cfg.recordTraces['cis'] = {'sec' : syn[0], 'loc': syn[1], 'var': 'v'}
# cfg.duration = start+2000
# cfg.duration = 0.5


#------------------------------------------------------------------------------
# Long range input pulses
#------------------------------------------------------------------------------
if cfg.addPulses:
    for key in [k for k in dir(cfg) if k.startswith('pulse')]:
        params = getattr(cfg, key, None)
        [pop, start, end, rate, noise] = [params[s] for s in ['pop', 'start', 'end', 'rate', 'noise']]
        if pop in netParams.popParams:
            if 'pulses' not in netParams.popParams[pop]: netParams.popParams[pop]['pulses'] = {}    
            netParams.popParams[pop]['pulses'].append({'start': start, 'end': end, 'rate': rate, 'noise': noise})

#------------------------------------------------------------------------------
# NetStim inputs
#------------------------------------------------------------------------------
if cfg.addNetStim:
    for key in [k for k in dir(cfg) if k.startswith('NetStim')]:
        params = getattr(cfg, key, None)
        [pop, ynorm, sec, loc, synMech, synMechWeightFactor, start, interval, noise, number, weight, delay] = \
        [params[s] for s in ['pop', 'ynorm', 'sec', 'loc', 'synMech', 'synMechWeightFactor', 'start', 'interval', 'noise', 'number', 'weight', 'delay']] 

        cfg.analysis['plotTraces']['include'].append((pop,0))

        if synMech == ESynMech:
            wfrac = cfg.synWeightFractionEE
        elif synMech == SOMESynMech:
            wfrac = cfg.synWeightFractionSOME
        else:
            wfrac = [1.0]

        # add stim source
        netParams.stimSourceParams[key] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

        # connect stim source to target
        # for i, syn in enumerate(synMech):
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop, 'ynorm': ynorm},
            'sec': sec, 
            'loc': loc,
            'synMech': synMech,
            'weight': weight,
            'synMechWeightFactor': synMechWeightFactor,
            'delay': delay}

##--------------------------------------------------------------------
# add list of netstims

if cfg.addNetStimList:
    for counter, stim in enumerate(cfg.NetStims):
        
        if stim['synMech'] == ESynMech:
            wfrac = cfg.synWeightFractionEE
        elif stim['synMech'] == SOMESynMech:
            wfrac = cfg.synWeightFractionSOME
        else:
            wfrac = [1.0]
        
        key = 'NetStim-'+str(counter+1)
        cfg.analysis['plotTraces']['include'].append((stim['pop'],0))

        # add stim source
        netParams.stimSourceParams[key] = {'type': 'NetStim', 'start': stim['start'], 'rate': stim['rate'], 'noise': stim['noise'], 'number': stim['number']}

        # connect stim source to target
        netParams.stimTargetParams[key+'_'+stim['pop']] =  {
        'source': key, 
        'conds': {'pop': stim['pop'], 'ynorm': stim['ynorm']},
        'sec': stim['sec'], 
        'loc': stim['loc'],
        'synMech': stim['synMech'],
        'weight': stim['weight'],
        'synMechWeightFactor': stim['synMechWeightFactor'],
        'delay': stim['delay']}

if cfg.addIClamp:

    for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
        ic = getattr(cfg, iclabel, None)  # get dict with params

        # add stim source
        #netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'del': ic['del'], 'dur': ic['dur'], 'amp': ic['amp']}
        netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'del': ic['start'], 'dur': ic['dur'], 'amp': ic['amp']}
        cfg.analysis['plotTraces']['include'].append((ic['pop'],0))
        # add stim target
        for curpop in ic['pop']:
            netParams.stimTargetParams[iclabel+'_'+curpop] = \
                {'source': iclabel, 'conds': {'popLabel': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}


sim.createSimulateAnalyze(netParams, cfg)

from matplotlib import pyplot as plt 
plt.ion()
plt.subplot(2,1,1)
plt.plot(sim.simData['t'], sim.simData['v_soma']['cell_0'])
plt.title('Soma')
plt.subplot(2,1,2)
plt.plot(sim.simData['t'], sim.simData['v_dend']['cell_0'])
plt.title('Dend')
# plt.plot(sim.simData['t'],sim.simData['V_soma']['cell_0'], 'b')
# plt.plot(sim.simData['t'], sim.simData['dend_52']['cell_0'],'r')
# plt.show()

# noTTXsoma = sim.simData['V_soma']['cell_0']
# noTTXdend = sim.simData['dend_52']['cell_0']

# cfg.removeNa = True

# #------------------------------------------------------------------------------
# # PT5B full cell model params (700+ comps)
# if 'PT5B_full' not in loadCellParams:
#     ihMod2str = {'harnett': 1, 'kole': 2, 'migliore': 3}
#     cellRule = netParams.importCellParams(label='PT5B_full', conds={'cellType': 'PT', 'cellModel': 'HH_full'},
#       fileName='cells/PTcell.hoc', cellName='PTcell', cellArgs=[ihMod2str[cfg.ihModel], cfg.ihSlope], somaAtOrigin=True)
#     nonSpiny = ['apic_0', 'apic_1']
#     netParams.addCellParamsSecList(label='PT5B_full', secListName='perisom', somaDist=[0, 50])  # sections within 50 um of soma
#     netParams.addCellParamsSecList(label='PT5B_full', secListName='apic_upper', somaDist=[300, 900])  # sections within 300-900 um of soma
#     netParams.addCellParamsSecList(label='PT5B_full', secListName='apic_lower', somaDist=[0, 300])  # sections within 0-300 um of soma
#     netParams.addCellParamsSecList(label='PT5B_full', secListName='below_soma', somaDistY=[-600, 0])  # sections within 0-300 um of soma
#     for sec in nonSpiny: cellRule['secLists']['perisom'].remove(sec)
#     cellRule['secLists']['alldend'] = [sec for sec in cellRule.secs if ('dend' in sec or 'apic' in sec)] # basal+apical
#     cellRule['secLists']['apicdend'] = [sec for sec in cellRule.secs if ('apic' in sec)] # apical
#     cellRule['secLists']['basaldend'] = [sec for sec in cellRule.secs if ('dend' in sec)] # apical
#     cellRule['secLists']['spiny'] = [sec for sec in cellRule['secLists']['alldend'] if sec not in nonSpiny]
#     # Adapt ih params based on cfg param
#     for secName in cellRule['secs']:
#         for mechName,mech in cellRule['secs'][secName]['mechs'].items():
#             if mechName in ['ih','h','h15', 'hd']: 
#                 mech['gbar'] = [g*cfg.ihGbar for g in mech['gbar']] if isinstance(mech['gbar'],list) else mech['gbar']*cfg.ihGbar
#                 if cfg.ihModel == 'migliore':   
#                     mech['clk'] = cfg.ihlkc  # migliore's shunt current factor
#                     mech['elk'] = cfg.ihlke  # migliore's shunt current reversal potential
#                 if secName.startswith('dend'): 
#                     mech['gbar'] *= cfg.ihGbarBasal  # modify ih conductance in soma+basal dendrites
#                     mech['clk'] *= cfg.ihlkcBasal  # modify ih conductance in soma+basal dendrites
#                 if secName in cellRule['secLists']['below_soma']: #secName.startswith('dend'): 
#                     mech['clk'] *= cfg.ihlkcBelowSoma  # modify ih conductance in soma+basal dendrites
                    
#     # Reduce dend Na to avoid dend spikes (compensate properties by modifying axon)
#     for secName in cellRule['secLists']['alldend']:
#         cellRule['secs'][secName]['mechs']['nax']['gbar'] = 0.0153130368342 * cfg.dendNa #0.25 
#         cellRule['secs'][secName]['mechs']['pas']['e'] *= cfg.epas
#         cellRule['secs'][secName]['mechs']['pas']['g'] *= cfg.gpas
#     cellRule['secs']['soma']['mechs']['nax']['gbar'] = 0.0153130368342  * cfg.somaNa
#     cellRule['secs']['axon']['mechs']['nax']['gbar'] = 0.0153130368342  * cfg.axonNa #11  
#     cellRule['secs']['axon']['geom']['Ra'] = 137.494564931 * cfg.axonRa #0.005 
#     # Remove Na (TTX)
#     if cfg.removeNa:
#         for secName in cellRule['secs']:
#             cellRule['secs'][secName]['mechs']['nax']['gbar'] = 0.0
#     if cfg.weightNorm and not cfg.netClamp:
#         netParams.addCellParamsWeightNorm('PT5B_full', 'conn/PT5B_full_weightNorm.pkl', threshold=cfg.weightNormThreshold)  # load weight norm
#     # cellRule['secs']['apic_0']['weightNorm'] = [1e-6] # set temporarily to 0, so subConn rules determine if syns provide input or not
#     if saveCellParams: netParams.saveCellParamsRule(label='PT5B_full', fileName='cells/PT5B_full_cellParams.pkl')

# sim.createSimulateAnalyze(netParams, cfg)

# TTXsoma = sim.simData['V_soma']['cell_0']
# TTXdend = sim.simData['dend_52']['cell_0']

# from matplotlib import pyplot as plt
# plt.plot(sim.simData['t'], noTTXdend, 'b')
# plt.plot(sim.simData['t'], TTXdend, 'r')
# plt.show()

# saving output
# V_soma = sim.simData['V_soma']['cell_0']
# time = sim.simData['t']
# out = {'V_soma' : np.ndarray.tolist(np.array(V_soma)),
#         'time' : np.ndarray.tolist(np.array(time)),
#         'window_starts_apical' : window_starts_apical,
#         'syn_lists_apical' : syn_lists_apical,
#         'window_starts_basal' : window_starts_basal,
#         'syn_lists_basal' : syn_lists_basal}

# with open('/oasis/scratch/comet/ckelley/temp_project/gaspMageePTcellExSynNMDA/basal_34-37_v_dist_v' + batch_num + '.json','w') as json_file:
#     json.dump(out, json_file)

## v0.0 - beginning of replicating stimulation patter from Gasparini and Magee
## v0.1 - compare basal vs. apical, loops through window sizes, and number of synapses
## v0.2 - just basal, clustered vs. distributed, window sweep, Ninputs from 10:100
## v0.3 - different basal cluster
## v0.5 - add NMDA stims as well
## v0.6 - extrasynaptic NMDA