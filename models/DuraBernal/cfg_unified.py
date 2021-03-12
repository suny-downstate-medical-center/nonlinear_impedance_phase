"""
cfg.py 

Simulation configuration for M1 model (using NetPyNE)

Contributors: salvadordura@gmail.com / joao.moreira@downstate.edu
"""

from netpyne import specs
import pickle

cfg = specs.SimConfig()  

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------
    
# cfg.simLabel_old = 'v48_tune201'
cfg.simLabel = 'jv00'

# cfg.simType = ''
# cfg.simType = 'NetStim'
cfg.simType = 'GroupNetStim'
# cfg.simType = 'GroupNetStim_delay'
# cfg.simType = 'IClamp'                  # and Rheobase
# cfg.simType = 'SpkActivity'


# print(cfg.simType)

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
if (cfg.simType == 'IClamp') or (cfg.simType == 'SpkActivity'):
    cfg.startStimTime 		= 0 # in ms
    cfg.numOfStims 			= 1
    cfg.interStimInterval 	= 50 # in ms
    cfg.duration = 1500
else:   # improve this code
    cfg.startStimTime 		= 300 # in ms
    cfg.numOfStims 			= 5
    cfg.interStimInterval 	= 50 # in ms
    cfg.extraTime           = 200
    cfg.duration 		= cfg.startStimTime+(cfg.numOfStims*cfg.interStimInterval)+cfg.extraTime

cfg.dt = 0.025
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = 0
cfg.createNEURONObj = True
cfg.createPyStruct = True  
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.1

cfg.includeParamsLabel = False
cfg.printPopAvgRates = True

cfg.checkErrors = 0 #### 0 == False?

#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
allpops = ['PT5B']
# allpops = ['IT2','PV2','SOM2','IT4','IT5A','PV5A','SOM5A','IT5B','PT5B','PV5B','SOM5B','IT6','CT6','PV6','SOM6']
cfg.cellsrec = 4
if cfg.cellsrec == 0:  cfg.recordCells = ['all'] # record all cells
elif cfg.cellsrec == 1: cfg.recordCells = [(pop,0) for pop in allpops] # record one cell of each pop
elif cfg.cellsrec == 2: cfg.recordCells = [('IT2',10), ('IT5A',10), ('PT5B',10), ('PV5B',10), ('SOM5B',10)] # record selected cells
elif cfg.cellsrec == 3: cfg.recordCells = [('IT5A',0), ('PT5B',0)]# record selected cells
elif cfg.cellsrec == 4: cfg.recordCells = [0]# other option->[('PT5B',0)] # record selected cells

cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}}

# cfg - also record
                    # 'V_Adend2': {'sec':'Adend2', 'loc':0.5, 'var':'v'}}
                    # 'I_AMPA_Adend2': {'sec':'Adend2', 'loc':0.5, 'synMech': 'AMPA', 'var': 'i'}}

# cfg_cell - also record
                    # 'i_gabab': {'sec':'soma', 'loc':0.5, 'synMech': 'GABAB', 'var':'i'},
                    # 'i_gabaa': {'sec':'soma', 'loc':0.5, 'synMech': 'GABAASlow', 'var':'i'}}
                    # 'V_Apic23': {'sec':'apic_25', 'loc':0.20901261732739618, 'var':'v'},
                    # 'V_Apic30': {'sec':'apic_30', 'loc':0.43547676639865263, 'var':'v'},
                    # 'V_Apic81': {'sec':'apic_81', 'loc':0.36259169916613432, 'var':'v'}}

cfg.recordStim = False  
cfg.recordTime = False
cfg.recordStep = cfg.dt
# cfg.recordStep = 0.1

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel            = 'M1_PTcell_'+cfg.simType
cfg.saveFolder          = '../data'
cfg.savePickle          = False
cfg.saveJson            = True
cfg.saveDataInclude     = ['simData', 'simConfig', 'netParams']#, 'net']
cfg.backupCfgFile       = None #['cfg.py', 'backupcfg/'] 
cfg.gatherOnlySimData   = False
cfg.saveCellSecs        = False #True
cfg.saveCellConns       = False #True

#------------------------------------------------------------------------------
# Cells
#------------------------------------------------------------------------------
cfg.cellmod =  {'PT5B': 'HH_full'}
# cfg.cellmod =  {'IT2': 'HH_reduced',
# 				'IT4': 'HH_reduced',
# 				'IT5A': 'HH_full',
# 				'IT5B': 'HH_reduced',
# 				'PT5B': 'HH_full',
# 				'IT6': 'HH_reduced',
# 				'CT6': 'HH_reduced'}

cfg.ihModel         =  'migliore'  # ih model
cfg.ihGbar          = 1.0  # multiplicative factor for ih gbar in PT cells
cfg.ihGbarZD        = None # multiplicative factor for ih gbar in PT cells
cfg.ihGbarBasal     = 1.0 # 0.1 # multiplicative factor for ih gbar in PT cells
cfg.ihlkc           = 0.2 # ih leak param (used in Migliore)
cfg.ihlkcBasal      = 1.0
cfg.ihlkcBelowSoma  = 0.01
cfg.ihlke           = -86  # ih leak param (used in Migliore)
cfg.ihSlope         = 14*2

cfg.removeNa    = False  # simulate TTX; set gnabar=0s
cfg.somaNa      = 5
cfg.dendNa      = 0.3
cfg.axonNa      = 7
cfg.axonRa      = 0.005

cfg.gpas = 0.5  # multiplicative factor for pas g in PT cells
cfg.epas = 0.9  # multiplicative factor for pas e in PT cells

#------------------------------------------------------------------------------
# Synapses
#------------------------------------------------------------------------------
cfg.synWeightFractionGeneric = 0.5
cfg.synWeightFractionEE = [cfg.synWeightFractionGeneric, 1-cfg.synWeightFractionGeneric] # E->E AMPA to NMDA ratio
cfg.synWeightFractionEI = [cfg.synWeightFractionGeneric, 1-cfg.synWeightFractionGeneric] # E->I AMPA to NMDA ratio
cfg.synWeightFractionSOME = [0.9, 0.1] # SOM -> E GABAASlow to GABAB ratio


# cfg.synWeightFractionEE = [0.5, 0.5] # E->E AMPA to NMDA ratio
# cfg.synWeightFractionEI = [0.5, 0.5] # E->I AMPA to NMDA ratio
# cfg.synWeightFractionSOME = [0.9, 0.1] # SOM -> E GABAASlow to GABAB ratio

cfg.synsperconn = {'HH_full': 5, 'HH_reduced': 1, 'HH_simple': 1}
if cfg.simType == 'GroupNetStim':
    cfg.excTau2Factor = 2.0
else:
    cfg.AMPATau2Factor = 1.0


#------------------------------------------------------------------------------
# Network 
#------------------------------------------------------------------------------
cfg.singleCellPops = 0  # Create pops with 1 single cell (to debug)
cfg.weightNorm = 1      # ADDED AS TRUE BECAUSE IN CFG.PY IT ALWAYS EXECUTES THIS LINE IN NETPARAMS.PY

cfg.weightNormThreshold = 4.0  # weight normalization factor threshold

# if cfg.simType == 'GroupNetStim':
#     cfg.addConn = 0
# else:
#     cfg.addConn = 1

cfg.scale = 1.0
cfg.sizeY = 1350.0
cfg.sizeX = 300.0
cfg.sizeZ = 300.0

#------------------------------------------------------------------------------
#
# INPUTS CONFIGURATION
#
# ------------------------------------------------------------------------------

# default cfg's
cfg.addNetStim      = 0
cfg.addGroupNetStim = 0
cfg.addIClamp       = 0
cfg.addVClamp       = 0
cfg.addSubConn      = 0
cfg.addLongConn     = 0
cfg.addPulses       = 0
cfg.netClamp        = 0
cfg.stimSubConn     = 0
cfg.addSpkActivity  = 0

if cfg.simType == 'NetStim':
    cfg.addNetStim      = 1
elif cfg.simType == 'GroupNetStim':
    cfg.addGroupNetStim = 1
    cfg.addSubConn      = 1      
elif cfg.simType == 'GroupNetStim_delay':
    cfg.addGroupNetStim = 1
    cfg.addSubConn      = 1
elif cfg.simType == 'IClamp':
    cfg.addIClamp       = 1
elif cfg.simType == 'SpkActivity':
    cfg.addSpkActivity  = 1
    cfg.addSubConn      = 1    
    cfg.addIClamp       = 1
    cfg.addGroupNetStim = 1
else:
    pass

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subcellular distribution
#------------------------------------------------------------------------------
# cfg.addSubConn = 0

if cfg.addSubConn and (cfg.addGroupNetStim or cfg.addSpkActivity):
    cfg.ihSubConn = 0           # used to reproduce the figure with the 2d map - 1st in the powerpoint - worry about later
    cfg.ihX = 4
    cfg.ihY = 14

# #------------------------------------------------------------------------------
# # Long range inputs
# #------------------------------------------------------------------------------
# # cfg.addLongConn = 0

# cfg.numCellsLong = 1000  # num of cells per population
# cfg.noiseLong = 1.0  # firing rate random noise
# cfg.delayLong = 5.0  # (ms)
# cfg.weightLong = 0.5  # corresponds to unitary connection somatic EPSP (mV)
# cfg.startLong = 0  # start at 0 ms
# cfg.ratesLong = {   'TPO':  [0,2], 
#                     'TVL':  [0,2], 
#                     'S1':   [0,2], 
#                     'S2':   [0,2], 
#                     'cM1':  [0,2], 
#                     'M2':   [0,2], 
#                     'OC':   [0,2]}

# # Extra stimulation for changing the firing rate at a given moment
# ## input pulses
# # cfg.addPulses = 0
# if cfg.addPulses:
#     if cfg.simType == 'GroupNetStim':
#         cfg.pulse = {   'pop':      'None', 
#                         'start':    2000, 
#                         'end':      2200, 
#                         'rate':     30, 
#                         'noise':    0.5}
#     else:
#         cfg.pulse = {   'pop':      'None', 
#                         'start':    1000, 
#                         'end':      1200, 
#                         'rate':     20, 
#                         'noise':    0.5}

#------------------------------------------------------------------------------
# Current inputs 
#------------------------------------------------------------------------------
# cfg.addIClamp = 0

              ## pop,   sec,   loc, start,dur, amp (nA)
if cfg.addIClamp and (cfg.simType == 'GroupNetStim' or cfg.simType == 'IClamp'):
    if cfg.simType == 'GroupNetStim':
        cfg.IClamp1 = { 'pop':      'PT5B_fI30', 
                        'sec':      'soma', 
                        'loc':      0.5, 
                        'start':    500, 
                        'dur':      1000, 
                        'amp':      0.30}

        cfg.IClamp2 = { 'pop':      'PT5B_fI60', 
                        'sec':      'soma', 
                        'loc':      0.5, 
                        'start':    500, 
                        'dur':      1000, 
                        'amp':      0.6}

        cfg.IClamp3 = { 'pop':      'PT5B_fI10', 
                        'sec':      'soma', 
                        'loc':      0.5, 
                        'start':    500, 
                        'dur':      1000, 
                        'amp':      0.10}

        cfg.IClamp4 = { 'pop':      'PT5B_fI40', 
                        'sec':      'soma', 
                        'loc':      0.5, 
                        'start':    500, 
                        'dur':      1000, 
                        'amp':      0.40}
    elif cfg.simType == 'IClamp':
        # improve this code to use cfg.variables to set the values
        cfg.IClamp1 = { 'pop':      'PT5B', 
                        'sec':      'soma', 
                        'loc':      0.5, 
                        'start':    cfg.startStimTime, 
                        'dur':      1000, 
                        'amp':      0.5}

        # cfg.currentAmp = 0.5
        # # improve this code to use cfg.variables to set the values
        # cfg.IClamp1 = { 'pop':      'PT5B', 
        #                 'sec':      'soma', 
        #                 'loc':      0.5, 
        #                 'start':    cfg.startStimTime, 
        #                 'dur':      1000, 
        #                 'amp':      cfg.currentAmp}

#------------------------------------------------------------------------------
# NetStim inputs 
#------------------------------------------------------------------------------
cfg.addNetStim = 0
if cfg.addNetStim:
    # cfg.addNetStim = 0
    cfg.numStims = 5 #1000.0
    cfg.netWeight = 0.5

    cfg.NetStim1 = {    'pop': 'PT5B', 
                        'ynorm':[0,1], 
                        'sec': 'soma', 
                        'loc': 0.5, 
                        'synMech': ['AMPA'], 
                        # 'synMech': ['NMDA'], 
                        # 'synMech': ['AMPA','NMDA'], 
                        'synMechWeightFactor': [1.0],
                        'start': cfg.startStimTime, 
                        'interval': cfg.interStimInterval, 
                        'noise': 0.0, 
                        'number': cfg.numStims, 
                        'weight': cfg.netWeight, 
                        'delay': 0}

#------------------------------------------------------------------------------
# GroupNetStim inputs 
#------------------------------------------------------------------------------
# cfg.addGroupNetStim = 1

if cfg.addGroupNetStim and cfg.simType == 'GroupNetStim':
    cfg.groupWeight = 0.3
    cfg.groupRate = 1000/cfg.interStimInterval

    cfg.GroupNetStimW1 = {  'nstype': 'pop', 
                            'numStims': 75, 
                            'pop': 'PT5B', 
                            'ynorm':[0,1], 
                            'cellRule': 'PT5B_full', 
                            'secList': 'alldend', 
                            'allSegs': True, \
                            # 'synMech': ['AMPA'], 
                            'synMech': ['AMPA','NMDA'], 
                            'start': cfg.startStimTime, 
                            'interval': cfg.interStimInterval, 
                            'noise': 0.6, 
                            'number': 1, 
                            'weight': cfg.groupWeight , 
                            'delay': 0}

if cfg.addGroupNetStim and cfg.simType == 'GroupNetStim_delay':
    cfg.groupWeight = 0.1
    cfg.groupRate = 1000/cfg.interStimInterval    # sheets fig 8

    cfg.GroupNetStimEPT = { 'nstype': 'pop', 
                            'numStims': 100, 
                            'pop': 'PT5B', 
                            # 'pop': ['PT5B','PT5B_ZD'], 
                            'ynorm':[0,1], 
                            'cellRule': 'PT5B_full', 
                            'secList': 'alldend', 
                            'allSegs': True, \
                            # 'synMech': ['AMPA'],
                            # 'synMech': ['exc'], 
                            'synMech': ['AMPA','NMDA'], 
                            'start': cfg.startStimTime, 
                            'interval': cfg.interStimInterval, 
                            'noise': 0.6, 
                            'number': 1, 
                            'weight': cfg.groupWeight, 
                            # 'weight': 0.20, 
                            'delay': 0}

    cfg.popdelay = 0
    # cfg.popdelay = 50
    cfg.startStimTime2 = 300

    cfg.GroupNetStimEPT2 = {'nstype': 'pop', 
                            'numStims': 100, 
                            'pop': 'PT5B', 
                            # 'pop': ['PT5B','PT5B_ZD'], 
                            'ynorm':[0,1], 
                            'cellRule': 'PT5B_full', 
                            'secList': 'alldend', 
                            'allSegs': True, \
                            # 'synMech': ['AMPA'],
                            # 'synMech': ['exc'], 
                            'synMech': ['AMPA','NMDA'], 
                            'start': cfg.startStimTime2, 
                            'interval': cfg.interStimInterval, 
                            'noise': 0.6, 
                            'number': 1, 
                            'weight': cfg.groupWeight, 
                            # 'weight': 0.20, 
                            'delay': cfg.popdelay}

    # # sheets fig 9
    # cfg.GroupNetStimEPT2 = {'nstype': 'pop', 
    #                         'numStims': 100, 
    #                         'pop': 'PT5B', 
    #                         # 'pop': ['PT5B','PT5B_ZD'], 
    #                         'cellRule': 'PT5B_full', 
    #                         'secList': 'alldend', 
    #                         'allSegs': True, \
    #                         'synMech': ['AMPA'],
    #                         # 'synMech': ['exc'], 
    #                         'start': cfg.startStimTime, 
    #                         'interval': cfg.interStimInterval, 
    #                         'noise': 0.25, 
    #                         'number': 1, 
    #                         'weight': 0.0, 
    #                         'delay': 25}

'''
# sheets fig 11  # num inputs = 8*16*100*0.07 = 896 (grid size * num neurons / grid * prob of exciting)
    cfg.GroupNetStimEPT = { 'nstype': 'pop', 
                            'numStims': int(8*16*100*0.07*0.16), 
                            'pop': 'PT5B', 
                            'cellRule': 'PT5B_full', 
                            'secList': 'alldend', 
                            'allSegs': True, \
                            'synMech': ['AMPA'],
 						    # 'synMech': ['AMPA','NMDA'],           # default
                            # 'synMechWeightFactor': [0.5,0.5],     # default
                            'start': cfg.startStimTime, 
                            'interval': cfg.interStimInterval, 
                            'noise': 1.0,                           # default
                            'number': cfg.groupRate*4.0,            # default
                            'weight': 0.1,                          # default
                            'delay': 0}                             # default

    cfg.GroupNetStimEPT2 = {'nstype': 'pop', 
                            'numStims': int(8*16*100*0.07*0.16), 
                            'pop': 'PT5B_ZD',                       # default: ZD-> ih=0
                            'cellRule': 'PT5B_full', 
                            'secList': 'alldend', 
                            'allSegs': True, \
						    'synMech': ['AMPA'],
 						    # 'synMech': ['AMPA','NMDA'],           # default
                            # 'synMechWeightFactor': [0.5,0.5],     # default
                            'start': cfg.startStimTime, 
                            'interval': cfg.interStimInterval, 
                            'noise': 1.0, 
                            'number': cfg.groupRate*4.0, 
                            'weight': 0.1, 
                            'delay': 0}
'''

#------------------------------------------------------------------------------
# Spiking Activity - Sheets Fig 11
#------------------------------------------------------------------------------
if cfg.addGroupNetStim and cfg.addIClamp and cfg.simType=='SpkActivity':

    # # VClamp to set the voltage at -70 mV
    # cfg.startVClamp = 100
    # cfg.VClamp1 = { 'pop':      'PT5B', 
    #                 'sec':      'soma', 
    #                 'loc':      0.5, 
    #                 'start':    cfg.startVClamp, 
    #                 'dur':      [cfg.startStimTime], # this way, the VClamp is removed right before the GroupNetStim is initiated 
    #                 'amp':      [-70]}
    
    # IClamp to set the voltage at -70 mV
    cfg.startIClamp = 100
    cfg.IClamp1 = { 'pop':      'PT5B', 
                    'sec':      'soma', 
                    'loc':      0.5, 
                    'start':    cfg.startIClamp, 
                    'dur':      cfg.duration, # this way, the IClamp is provided throughout the whole simulation
                    'amp':      0.5}

    # Group of Net Stims to trigger Action Potentials
    cfg.groupWeight = 1.0
    # cfg.groupWeight = 0.3
    cfg.groupRate = 1000/cfg.interStimInterval
    cfg.strimDur = 1000 # in ms
    cfg.GroupNetStimW1 = {  'nstype': 'pop', 
                            'numStims': 75, 
                            'pop': 'PT5B', 
                            'ynorm':[0,1], 
                            'cellRule': 'PT5B_full', 
                            'secList': 'alldend', 
                            'allSegs': True, \
                            # 'synMech': ['AMPA'], 
                            'synMech': ['AMPA','NMDA'], 
                            'start': cfg.startStimTime, 
                            'interval': cfg.interStimInterval, 
                            'noise': 0.6, 
                            'number': cfg.groupRate*(cfg.strimDur/1000), 
                            # 'number': 1, 
                            'weight': cfg.groupWeight , 
                            'delay': 0}
#------------------------------------------------------------------------------
# Network clamp
#------------------------------------------------------------------------------
# cfg.netClamp = 0

# cfg.netClampConnsFile = '../data/v47_batch9/v47_batch9_0.json'
# cfg.netClampSpikesFile = '../data/v47_batch5/v47_batch5_1_1_2_0_1_1_1_0.json'
# cfg.netClampPop = ['IT5A_1']
# cfg.netClampGid = 3597

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------

cfg.analysis['plotTraces'] = {  'include': [('PT5B',00)], 
                                'timeRange': [0,cfg.duration], 
                                'oneFigPer': 'cell', 
                                'figSize': (20,8), 
                                'saveFig': True, 
                                'showFig': True}

# cfg.analysis['plotTraces'] = {  'include': [0,1], 
#                                 'oneFigPer': 'trace', 
#                                 'overlay': 0, 
#                                 'figSize': (12,8), 
#                                 'timeRange': [0,500], 
#                                 'saveFig': True, 
#                                 'showFig': False,
#  							      'colors': [[0,0,1],[0,0.502,0]], 
#                                 'ylim': [-90, 15]}

# with open('cells/popColors.pkl', 'r') as fileObj: popColors = pickle.load(fileObj)['popColors']
# cfg.analysis['plotRaster'] = {'include': ['allCells'], 
#                               'saveFig': True, 
#                               'showFig': False, 
#                               'labels': 'overlay', 
#                               'popRates': True, 
#                               'orderInverse': True, 
#   							'popColors': popColors, 
#                               'figSize': (12,10), 
#                               'lw': 0.6, 
#                               'marker': '|'} 
