
"""
netParams.py 

High-level specifications for M1 network model using NetPyNE

Contributors: salvadordura@gmail.com
"""

from netpyne import specs
import pickle, json

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

netParams.version = 48

try:
	from __main__ import cfg  # import SimConfig object with params from parent module
except:
	from cfg_unified import cfg

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = cfg.scale # Scale factor for number of cells
netParams.sizeX = cfg.sizeX # x-dimension (horizontal length) size in um
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

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
cellModels = ['HH_simple', 'HH_reduced', 'HH_full']
layer = {'2': [0.12,0.31], '4': [0.31,0.42], '5A': [0.42,0.52], '45A':[0.31,0.52], '5B': [0.52,0.77], '6': [0.77,1.0], 'long': [2.0,3.0]}  # normalized layer boundaries

#------------------------------------------------------------------------------
## Load cell rules previously saved using netpyne format

# if cfg.simType == 'GroupNetParams':         # cfg_cell.py
#     cellParamLabels = [ 'IT2_reduced', 
#                         'IT4_reduced', 
#                         'IT5A_reduced', 
#                         'IT5B_reduced',
#                     	'PT5B_reduced',  
#                         'IT6_reduced', 
#                         'CT6_reduced', 
#                         'PV_simple', 
#                         'SOM_simple',
#                         'IT5A_full']    #, 'PT5B_full'] #  # list of cell rules to load from file
#     loadCellParams = cellParamLabels
#     saveCellParams = True
# else:                                       # cfg.py
#     cellParamLabels = [ 'IT5A_full', 
#                         'IT2_reduced', 
#                         'IT4_reduced', 
#                         'IT5A_reduced',
#                         'IT5B_reduced',
# 	                    'PT5B_reduced',
#                         'IT6_reduced', 
#                         'CT6_reduced', 
#                         'PV_simple', 
#                         'SOM_simple']   #, 'PT5B_full'] #  # list of cell rules to load from file
#     loadCellParams = []
#     saveCellParams = False

# for ruleLabel in loadCellParams:
# 	netParams.loadCellParamsRule(label=ruleLabel, fileName='cells/'+ruleLabel+'_cellParams.pkl')

loadCellParams = []
saveCellParams = False

# #------------------------------------------------------------------------------
# # Specification of cell rules not previously loaded
# # Includes importing from hoc template or python class, and setting additional params

# #------------------------------------------------------------------------------
# if cfg.simType == 'GroupNetParams':         # cfg_cell.py
#     # Reduced cell model params (6-comp) 
#     reducedCells = {  # layer and cell type for reduced cell models
#         'IT2_reduced': 	{'layer': '2', 	'cname': 'CSTR6', 'carg': 'BS1578'}, 
#         'IT4_reduced': 	{'layer': '4', 	'cname': 'CSTR6', 'carg': 'BS1578'},
#         'IT5A_reduced': {'layer': '5A', 'cname': 'CSTR6', 'carg': 'BS1579'},
#         'IT5B_reduced': {'layer': '5B', 'cname': 'CSTR6', 'carg': 'BS1579'},
#         'PT5B_reduced': {'layer': '5B', 'cname': 'SPI6',  'carg':  None},
#         'IT6_reduced': 	{'layer': '6', 	'cname': 'CSTR6', 'carg': 'BS1579'},
#         'CT6_reduced':	{'layer': '6', 	'cname': 'CSTR6', 'carg': 'BS1578'}}

#     reducedSecList = {  # section Lists for reduced cell model
#         'alldend': 	['Adend1', 'Adend2', 'Adend3', 'Bdend'],
#         'spiny': 	['Adend1', 'Adend2', 'Adend3', 'Bdend'],
#         'apicdend': ['Adend1', 'Adend2', 'Adend3'],
#         'perisom': 	['soma']}

#     for label, p in reducedCells.items():  # create cell rules that were not loaded 
#         if label not in loadCellParams:
#             cellRule = netParams.importCellParams(label=label, conds={'cellType': label[0:2], 'cellModel': 'HH_reduced', 'ynorm': layer[p['layer']]},
#             fileName='cells/'+p['cname']+'.py', cellName=p['cname'], cellArgs={'params': p['carg']} if p['carg'] else None)
#             dendL = (layer[p['layer']][0]+(layer[p['layer']][1]-layer[p['layer']][0])/2.0) * cfg.sizeY  # adapt dend L based on layer
#             for secName in ['Adend1', 'Adend2', 'Adend3', 'Bdend']: cellRule['secs'][secName]['geom']['L'] = dendL / 3.0  # update dend L
#             for k,v in reducedSecList.items(): cellRule['secLists'][k] = v  # add secLists
#             netParams.addCellParamsWeightNorm(label, 'conn/'+label+'_weightNorm.pkl', threshold=cfg.weightNormThreshold)  # add weightNorm

#             if cfg.reduced3DGeom: # set 3D pt geom
#                 offset, prevL = 0, 0
#                 for secName, sec in netParams.cellParams[label]['secs'].items():
#                     sec['geom']['pt3d'] = []
#                     if secName in ['soma', 'Adend1', 'Adend2', 'Adend3']:  # set 3d geom of soma and Adends
#                         sec['geom']['pt3d'].append([offset+0, prevL, 0, sec['geom']['diam']])
#                         prevL = float(prevL + sec['geom']['L'])
#                         sec['geom']['pt3d'].append([offset+0, prevL, 0, sec['geom']['diam']])
#                     if secName in ['Bdend']:  # set 3d geom of Bdend
#                         sec['geom']['pt3d'].append([offset+0, 0, 0, sec['geom']['diam']])
#                         sec['geom']['pt3d'].append([offset+sec['geom']['L'], 0, 0, sec['geom']['diam']])		
#                     if secName in ['axon']:  # set 3d geom of axon
#                         sec['geom']['pt3d'].append([offset+0, 0, 0, sec['geom']['diam']])
#                         sec['geom']['pt3d'].append([offset+0, -sec['geom']['L'], 0, sec['geom']['diam']])	

#             if saveCellParams: netParams.saveCellParamsRule(label=label, fileName='cells/'+label+'_cellParams.pkl')

#------------------------------------------------------------------------------
# PT5B full cell model params (700+ comps)
if 'PT5B_full' not in loadCellParams:
	ihMod2str = {'harnett': 1, 'kole': 2, 'migliore': 3}
	cellRule = netParams.importCellParams(label='PT5B_full', conds={'cellType': 'PT', 'cellModel': 'HH_full'},
	  fileName='cells/PTcell.hoc', cellName='PTcell', cellArgs=[ihMod2str[cfg.ihModel], cfg.ihSlope], somaAtOrigin=True)
	nonSpiny = ['apic_0', 'apic_1']
	netParams.addCellParamsSecList(label='PT5B_full', secListName='perisom', somaDist=[0, 50])  # sections within 50 um of soma
	netParams.addCellParamsSecList(label='PT5B_full', secListName='apic_upper', somaDist=[300, 900])  # sections within 300-900 um of soma      # NOT PRESENT IN CFG.PY
	netParams.addCellParamsSecList(label='PT5B_full', secListName='apic_lower', somaDist=[0, 300])  # sections within 0-300 um of soma          # NOT PRESENT IN CFG.PY
	netParams.addCellParamsSecList(label='PT5B_full', secListName='below_soma', somaDistY=[-600, 0])  # sections within 0-300 um of soma
	for sec in nonSpiny: cellRule['secLists']['perisom'].remove(sec)
    # creates a list with different categories (alldend, apicdend, basaldend, spiny)
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
		cellRule['secs'][secName]['mechs']['pas']['e'] *= cfg.epas                              # NOT PRESENT IN CFG.PY
		cellRule['secs'][secName]['mechs']['pas']['g'] *= cfg.gpas                              # NOT PRESENT IN CFG.PY
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
	netParams.saveCellParamsRule(label='PT5B_full', fileName='cells/PT5B_full_cellParams.pkl')

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
## load densities
with open('cells/cellDensity.pkl', 'rb') as fileObj: density = pickle.load(fileObj, encoding='latin1')['density']


# ORIGINAL CONFIGURATION FOR CFG_CELL.PY
# netParams.popParams['PT5B'] =	{'cellModel': cfg.cellmod['PT5B'], 'cellType': 'PT', 'ynormRange': layer['5B'], 'density': 0.5*density[('M1','E')][3]}#, 'xRange': [100,100], 'yRange': [735,735]}

# ORIGINAL CONFIGURATION FOR CFG.PY
netParams.popParams['PT5B'] = {'cellModel': 'HH_full', 'cellType': 'PT', 'ynormRange': layer['5B'], 'numCells':1}


if cfg.singleCellPops:
	for pop in netParams.popParams.values(): pop['numCells'] = 1

# #------------------------------------------------------------------------------
# ## Long-range input populations (VecStims)
# if cfg.addLongConn:
# 	## load experimentally based parameters for long range inputs
# 	# with open('conn/conn_long.pkl', 'r') as fileObj: connLongData = pickle.load(fileObj)
# 	with open('conn/conn_long.pkl', 'rb') as fileObj: connLongData = pickle.load(fileObj, encoding='latin1')
# 	#ratesLong = connLongData['rates']

# 	numCells = cfg.numCellsLong
# 	noise = cfg.noiseLong
# 	start = cfg.startLong

# 	longPops = ['TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']
# 	## create populations with fixed 
# 	for longPop in longPops:
# 		netParams.popParams[longPop] = {'cellModel':    'VecStim', 
#                                         'numCells':     numCells, 
#                                         'rate':         cfg.ratesLong[longPop], 
# 										'noise':        noise, 
#                                         'start':        start, 
#                                         'pulses':       [], 
#                                         'ynormRange':   layer['long']}

#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
multiplier1, multiplier2 = 1, 1
if cfg.simType == 'NetStim':
    multiplier1 = cfg.AMPATau2Factor
elif cfg.simType == 'GroupNetStim':
    multiplier2 = cfg.excTau2Factor # currently have no effect, because GroupNetStim is using only AMPA and NMDA synapses, and cfg.AMPATau2Factor = 1

# excitatory synapses
netParams.synMechParams['NMDA'] = {'mod':'MyExp2SynNMDABB', 'tau1NMDA': 15, 'tau2NMDA': 150,        'e': 0}
netParams.synMechParams['AMPA'] = {'mod':'MyExp2SynBB',     'tau1': 0.05,   'tau2': 5.3*multiplier1,'e': 0}
netParams.synMechParams['exc']  = {'mod':'Exp2Syn',         'tau1': 0.05,   'tau2': 5.3*multiplier2,'e': 0}
# inhibitory synapses
netParams.synMechParams['GABAB']            = {'mod':'MyExp2SynBB', 'tau1': 3.5,    'tau2': 260.9,  'e': -93} 
netParams.synMechParams['GABAA']            = {'mod':'MyExp2SynBB', 'tau1': 0.07,   'tau2': 18.2,   'e': -80}
netParams.synMechParams['GABAASlow']        = {'mod':'MyExp2SynBB', 'tau1': 2,      'tau2': 100,    'e': -80}
netParams.synMechParams['GABAASlowSlow']    = {'mod':'MyExp2SynBB', 'tau1': 200,    'tau2': 400,    'e': -80}

ESynMech =      ['AMPA', 'NMDA']
SOMESynMech =   ['GABAASlow','GABAB']
SOMISynMech =   ['GABAASlow']
PVSynMech =     ['GABAA']

# #------------------------------------------------------------------------------
# # Long range input pulses
# #------------------------------------------------------------------------------
# if cfg.addPulses:
# 	for key in [k for k in dir(cfg) if k.startswith('pulse')]:
# 		params = getattr(cfg, key, None)
# 		[pop, start, end, rate, noise] = [params[s] for s in ['pop', 'start', 'end', 'rate', 'noise']]
# 		if pop in netParams.popParams:
# 			if 'pulses' not in netParams.popParams[pop]: netParams.popParams[pop]['pulses'] = {} 	
# 			netParams.popParams[pop]['pulses'].append({'start': start, 'end': end, 'rate': rate, 'noise': noise})

#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
	for key in [k for k in dir(cfg) if k.startswith('IClamp')]:
		params = getattr(cfg, key, None)
		[pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

		cfg.analysis['plotTraces']['include'].append((pop,0))  # record that pop

		# add stim source
		netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
		
		# connect stim source to target
		netParams.stimTargetParams[key+'_'+pop] =  {
			'source': key, 
			'conds': {'pop': pop},
			'sec': sec, 
			'loc': loc}

#------------------------------------------------------------------------------
# Voltage inputs (VClamp)
#------------------------------------------------------------------------------
if cfg.addVClamp:
	for key in [k for k in dir(cfg) if k.startswith('VClamp')]:
		params = getattr(cfg, key, None)
		[pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

		cfg.analysis['plotTraces']['include'].append((pop,0))  # record that pop

		# add stim source
		netParams.stimSourceParams[key] = {	'type': 'VClamp', 'dur': dur, 'amp':amp}#,
											# 'gain': 1, 'rstim': 0, 'tau1': 1, 'tau2': 1, 'i': 1}

		# Example of syntax:
		# netParams.stimSourceParams['Input_2'] = {	'type': 'VClamp', 
		# 											'dur': [0,50,200],    	# each value is a different starting time to vclamp
		# 											'amp': [-60,-30,40], 	# each value is a different clamping voltage
		# 											'gain': 1e5, 
		# 											'rstim': 1, 
		# 											'tau1': 0.1, 
		# 											'tau2': 0}

		
		# connect stim source to target
		netParams.stimTargetParams[key+'_'+pop] =  {
			'source': key, 
			'conds': {'pop': pop},
			'sec': sec, 
			'loc': loc}

#------------------------------------------------------------------------------
# NetStim inputs - FROM CFG.PY
#------------------------------------------------------------------------------
if cfg.addNetStim:
	for key in [k for k in dir(cfg) if k.startswith('NetStim')]:
		params = getattr(cfg, key, None)
		[pop, sec, loc, synMech, synMechWeightFactor, start, interval, noise, number, weight, delay] = \
		[params[s] for s in ['pop', 'sec', 'loc', 'synMech', 'synMechWeightFactor', 'start', 'interval', 'noise', 'number', 'weight', 'delay']] 

		cfg.analysis['plotTraces']['include'] = [(pop,0)]

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
			'conds': {'pop': pop},
			'sec': sec, 
			'loc': loc,
			'synMech': synMech,
			# 'weight': weight,
			'weight': cfg.netWeight if cfg.netWeight is not None else weight,
			'synMechWeightFactor': synMechWeightFactor,
			'delay': delay}

#------------------------------------------------------------------------------
# GroupNetStim inputs - FROM CFG_CELL.PY
#------------------------------------------------------------------------------
# if cfg.addGroupNetStim:
#     # Group of NetStims
#     for key in [k for k in dir(cfg) if k.startswith('GroupNetStim')]:
#         params = getattr(cfg, key, None)
#         nstype, numStims, pop, ynorm, cellRule, secList, allSegs, synMech, start, interval, noise, number, weight, delay = [params[s] for s in ['nstype', 'numStims', 'pop', 'ynorm', 'cellRule', 'secList', 'allSegs', 'synMech', 'start', 'interval', 'noise', 'number', 'weight', 'delay']]

#         cfg.analysis['plotTraces']['include'].append((pop,0))

#         if not isinstance(secList, list):
#             secList = list(netParams.cellParams[cellRule]['secLists'][secList])

#         istim = 0
#         segs = []

#         if synMech == ESynMech:
#             wfrac = cfg.synWeightFractionEE
#         elif synMech == SOMESynMech:
#             wfrac = cfg.synWeightFractionSOME
#         else:
#             wfrac = [1.0]

#         if nstype == 'stim':  # implement as a stim - [jv] not being used
#             while istim < numStims:
#                 for secName,sec in netParams.cellParams[cellRule]['secs'].items():
#                     if secName in secList:
#                         if allSegs:
#                             nseg = sec['geom']['nseg']
#                             for iseg in range(nseg):
#                                 segs.append([secName, (iseg+1)*(1.0/(nseg+1))])
#                                 istim += 1
#                                 if istim >= numStims: break
#                         else:
#                             segs.append([secName, 0.5])
#                             istim += 1
                        
#                         if istim >= numStims: break

#             for istim, seg in enumerate(segs):

#                 # add stim source
#                 netParams.stimSourceParams[key+'_'+str(istim)] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

#                 # connect stim source to target
#                 for i, syn in enumerate(synMech):
#                     netParams.stimTargetParams[key+'_'+pop+'_'+syn+'_'+str(istim)] =  {
#                         'source': key+'_'+str(istim), 
#                         'conds': {'pop': pop, 'ynorm': ynorm},
#                         'sec': seg[0], 
#                         'loc': seg[1],
#                         'synMech': syn,
#                         'weight': weight*wfrac[i],
#                         'delay': delay}

#         elif nstype == 'pop':  # implement as a pop
#             netParams.popParams[key] = {	'cellModel':'NetStim', 
# 											'numCells': numStims, 
# 											'rate': 	cfg.groupRate if cfg.groupRate else 1000/interval,
#                                          	'noise': 	noise, 
# 											'start': 	start, 
# 											'number': 	number}
            
#             netParams.connParams[key] = { 
#                         'preConds': 	{'pop': key}, 
#                         'postConds': 	{'pop': pop, 'ynorm': ynorm},
#                         'synMech': 		synMech,
#                         'weight': 		cfg.groupWeight if cfg.groupWeight is not None else weight, 
#                         'synMechWeightFactor': wfrac,
#                         'delay': 		delay,
#                         'synsPerConn': 	1,
#                         'sec': 			secList}
            
#             netParams.subConnParams[key] = {
#                         'preConds': 	{'pop': key}, 
#                         'postConds': 	{'pop': pop, 'ynorm': ynorm},  
#                         'sec': 			secList, 
#                         'groupSynMechs': ESynMech, # removed to use only AMPA and see if it affects spatial summation, and not a combination of [AMPA, NMDA] 2020_05_28
#                         'density': 		'uniform'} 

#------------------------------------------------------------------------------
# Network clamp (integrate into netpyne?)
#------------------------------------------------------------------------------
if cfg.netClamp:
	# load full files and save reduced file
	import os.path
	from netpyne.sim import ijsonLoad

	tagsFile = cfg.netClampConnsFile[:-5]+'_netClampTags_%d.json'%(cfg.netClampGid)
	connsFile = cfg.netClampConnsFile[:-5]+'_netClampConns_%d.json'%(cfg.netClampGid)

	if not os.path.isfile(tagsFile) and not os.path.isfile(connsFile): # load both tags+conns
		ijsonLoad(cfg.netClampConnsFile, tagsGidRange=None, connsGidRange=[cfg.netClampGid], loadTags=True, loadConns=True, tagFormat=['pop'], connFormat=None, 
						saveTags=tagsFile, saveConns=connsFile)
	elif not os.path.isfile(tagsFile): # load tags
		ijsonLoad(cfg.netClampConnsFile, tagsGidRange=None, loadTags=True, loadConns=False, tagFormat=['pop'], saveTags=tagsFile)
	elif not os.path.isfile(connsFile): # load conns
		ijsonLoad(cfg.netClampConnsFile, connsGidRange=[cfg.netClampGid], loadTags=False, loadConns=True, connFormat=None, saveConns=connsFile)

	# load reduced files
	with open(tagsFile, 'r') as fileObj: tags = json.load(fileObj)['tags']
	tags = {int(k) if k != 'format' else k:v  for k,v in tags.items()}
	with open(connsFile, 'r') as fileObj: conns = json.load(fileObj)['conns']#[cfg.netClampGid]
	conns = {int(k) if k != 'format' else k:v  for k,v in conns.items()}
	conns = conns[cfg.netClampGid]

	# load list of preGid cell
	preGids = list(set([conn['preGid'] for conn in conns]))

	# load spk times of preGid cells
	with open(cfg.netClampSpikesFile, 'r') as fileObj: data = json.load(fileObj)
	allSpkids,allSpkts = data['simData']['spkid'], data['simData']['spkt']
	# Note tags is imported using 'format', so is list of tags, in this case just 'pop'
	popIndex = tags['format'].index('pop')
	spkids,spkts,spkpops = zip(*[(spkid,spkt,tags[int(spkid)][popIndex]) for spkid,spkt in zip(allSpkids,allSpkts) if spkid in preGids])

	# group by prepops
	prePops = list(set(spkpops))

	# create one vectsim pop reproducing spk times per preGid; and multiple conns 
	for prePop in prePops:
		# get spkTimes for preGid
		spkGids = [spkid for spkid,spkpop in zip(spkids,spkpops) if spkpop == prePop]

		if len(spkGids) > 0:
			# get list of cell gids in this pop 
			popGids = list(set(spkGids))

			# set key/label of pop
			key = '' + str(prePop)

			# create 1 vectstim pop per conn (cellLabel=cell gid -- so can reference later)
			cellsList = []
			for popGid in popGids: 
				spkTimes = [spkt for spkid,spkt in zip(spkids,spkts) if spkid == popGid]
				if len(spkTimes) > 0:
					cellsList.append({'cellLabel': int(popGid), 'spkTimes': spkTimes})
					netParams.popParams[key] = {'cellModel': 'VecStim', 'cellsList': cellsList}

					# calculate conns for this preGid
					preConns = [conn for conn in conns if conn['preGid'] == popGid]

					for i,preConn in enumerate(preConns):
						netParams.connParams[key+'_'+str(popGid)+'_'+str(i)] = { 
								'preConds': {'cellLabel': preConn['preGid']},  # cellLabel corresponds to gid 
								'postConds': {'pop': cfg.netClampPop},
								'synMech': str(preConn['synMech']),
								'weight': float(preConn['weight']), 
								'delay': float(preConn['delay']),
								'sec': str(preConn['sec']), 
								'loc': str(preConn['loc'])}

	# longPops = ['TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']

	# #Modify netClamp pops
	# rate = 50

	# for cell in netParams.popParams['PV5B']['cellsList']:
	#     cell['spkTimes'] = []# list(random.uniform(0,cfg.duration,(rate*cfg.duration/1000)))
	
# #------------------------------------------------------------------------------
# # Local connectivity parameters
# #------------------------------------------------------------------------------
# with open('conn/conn.pkl', 'rb') as fileObj: connData = pickle.load(fileObj, encoding='latin1')
# pmat = connData['pmat']
# wmat = connData['wmat']
# bins = connData['bins']

# #------------------------------------------------------------------------------
# ## E -> E
# if cfg.addConn and cfg.EEGain > 0.0:
# 	labelsConns = [('W+AS_norm', 'IT', 'L2/3'), ('W+AS_norm', 'IT', 'L4,5A,5B'), 
# 				   ('W+AS_norm', 'PT', 'L5B'), ('W+AS_norm', 'IT', 'L6'), ('W+AS_norm', 'CT', 'L6')]
# 	labelPostBins = [('W+AS', 'IT', 'L2/3'), ('W+AS', 'IT', 'L4,5A,5B'), ('W+AS', 'PT', 'L5B'), 
# 					('W+AS', 'IT', 'L6'), ('W+AS', 'CT', 'L6')]
# 	labelPreBins = ['W', 'AS', 'AS', 'W', 'W']
# 	preTypes = [['IT'], ['IT'], ['IT', 'PT'], ['IT','CT'], ['IT','CT']] 
# 	postTypes = ['IT', 'IT', 'PT', 'IT','CT']
# 	ESynMech = ['AMPA','NMDA']

# 	for i,(label, preBinLabel, postBinLabel) in enumerate(zip(labelsConns,labelPreBins, labelPostBins)):
# 		for ipre, preBin in enumerate(bins[preBinLabel]):
# 			for ipost, postBin in enumerate(bins[postBinLabel]):
# 				for cellModel in cellModels:
# 					ruleLabel = 'EE_'+cellModel+'_'+str(i)+'_'+str(ipre)+'_'+str(ipost)
# 					netParams.connParams[ruleLabel] = { 
# 						'preConds': {'cellType': preTypes[i], 'ynorm': list(preBin)}, 
# 						'postConds': {'cellModel': cellModel, 'cellType': postTypes[i], 'ynorm': list(postBin)},
# 						'synMech': ESynMech,
# 						'probability': pmat[label][ipost,ipre],
# 						'weight': wmat[label][ipost,ipre] * cfg.EEGain / cfg.synsperconn[cellModel], 
# 						'synMechWeightFactor': cfg.synWeightFractionEE,
# 						'delay': 'defaultDelay+dist_3D/propVelocity',
# 						'synsPerConn': cfg.synsperconn[cellModel],
# 						'sec': 'spiny'}
			

# #------------------------------------------------------------------------------
# ## E -> I
# if cfg.EIGain: # Use IEGain if value set
# 	cfg.EPVGain = cfg.EIGain
# 	cfg.ESOMGain = cfg.EIGain
# else: 
# 	cfg.EIGain = (cfg.EPVGain+cfg.ESOMGain)/2.0

# if cfg.addConn and (cfg.EPVGain > 0.0 or cfg.ESOMGain > 0.0):
# 	labelsConns = ['FS', 'LTS']
# 	labelPostBins = ['FS/LTS', 'FS/LTS']
# 	labelPreBins = ['FS/LTS', 'FS/LTS']
# 	preTypes = ['IT', 'PT', 'CT']
# 	postTypes = ['PV', 'SOM']
# 	ESynMech = ['AMPA','NMDA']
# 	lGain = [cfg.EPVGain, cfg.ESOMGain] # E -> PV or E -> SOM
# 	for i,(label, preBinLabel, postBinLabel) in enumerate(zip(labelsConns,labelPreBins, labelPostBins)):
# 		for ipre, preBin in enumerate(bins[preBinLabel]):
# 			for ipost, postBin in enumerate(bins[postBinLabel]):
# 				ruleLabel = 'EI_'+str(i)+'_'+str(ipre)+'_'+str(ipost)
# 				netParams.connParams[ruleLabel] = {
# 					'preConds': {'cellType': preTypes, 'ynorm': list(preBin)},
# 					'postConds': {'cellType': postTypes[i], 'ynorm': list(postBin)},
# 					'synMech': ESynMech,
# 					'probability': pmat[label][ipost,ipre],
# 					'weight': wmat[label][ipost,ipre] * lGain[i],
# 					'synMechWeightFactor': cfg.synWeightFractionEI,
# 					'delay': 'defaultDelay+dist_3D/propVelocity',
# 					'sec': 'soma'} # simple I cells used right now only have soma

# #------------------------------------------------------------------------------
# ## I -> all
# if cfg.IEGain: # Use IEGain if value set
# 	cfg.PVEGain = cfg.IEGain
# 	cfg.SOMEGain = cfg.IEGain
# else: 
# 	cfg.IEGain = (cfg.PVEGain+cfg.SOMEGain)/2.0

# if cfg.IIGain:  # Use IIGain if value set
# 	cfg.SOMPVGain = cfg.IIGain
# 	cfg.PVSOMGain = cfg.IIGain
# 	cfg.SOMSOMGain = cfg.IIGain
# 	cfg.PVPVGain = cfg.IIGain
# else:
# 	cfg.IIGain = (cfg.PVSOMGain+cfg.SOMPVGain+cfg.SOMSOMGain+cfg.PVPVGain)/4.0

# if cfg.addConn and (cfg.IEGain > 0.0 or cfg.IIGain > 0.0):
# 	# Local, intralaminar only; all-to-all but distance-based; high weights; L5A/B->L5A/B
# 	preCellTypes = ['SOM', 'SOM', 'SOM', 'PV', 'PV', 'PV']
# 	ynorms = [(0.12,0.31), (0.31,0.77), (0.77,1.0), (0.12,0.31), (0.31,0.77), (0.77,1.0)]
# 	IEweights = cfg.IEweights * 2  # [I->E2/3+4, I->E5, I->E6] weights (Note * 2 is repeat list operator)
# 	IIweights = cfg.IIweights * 2  # [I->I2/3+4, I->I5, I->I6] weights (Note * 2 is repeat list operator)
# 	postCellTypes = ['PT', ['IT','CT'], 'PV', 'SOM']
# 	IEdisynBiases = [None, cfg.IEdisynapticBias, cfg.IEdisynapticBias, None, cfg.IEdisynapticBias, cfg.IEdisynapticBias]
# 	disynapticBias = None  # default, used for I->I

# 	for i,(preCellType, ynorm, IEweight, IIweight, IEdisynBias) in enumerate(zip(preCellTypes, ynorms, IEweights, IIweights, IEdisynBiases)):
# 		for ipost, postCellType in enumerate(postCellTypes):
# 			for cellModel in cellModels:
# 				if postCellType == 'PV':	# postsynaptic I cell
# 					sec = 'soma'
# 					synWeightFraction = [1]
# 					if preCellType == 'PV':  			# PV->PV
# 						weight = IIweight * cfg.PVPVGain
# 						synMech = PVSynMech
# 					else:  							# SOM->PV
# 						weight = IIweight * cfg.SOMPVGain
# 						synMech = SOMISynMech
# 				elif postCellType == 'SOM':	# postsynaptic I cell
# 					sec = 'soma'
# 					synWeightFraction = [1]
# 					if preCellType == 'PV':  			# PV->SOM
# 						weight = IIweight * cfg.PVSOMGain
# 						synMech = PVSynMech
# 					else:  							# SOM->SOM
# 						weight = IIweight * cfg.SOMSOMGain
# 						synMech = SOMISynMech
# 				elif postCellType == ['IT','CT']: # postsynaptic IT,CT cell
# 					disynapticBias = IEdisynBias
# 					if preCellType == 'PV':  			# PV->E
# 						weight = IEweight * cfg.PVEGain
# 						synMech = PVSynMech
# 						sec = 'perisom'
# 					else:  							# SOM->E
# 						weight = IEweight * cfg.SOMEGain
# 						synMech = SOMESynMech
# 						sec = 'spiny'
# 						synWeightFraction = cfg.synWeightFractionSOME
# 				elif postCellType == 'PT': # postsynaptic PT cell
# 					disynapticBias = IEdisynBias
# 					if preCellType == 'PV':  			# PV->E
# 						weight = IEweight * cfg.IPTGain * cfg.PVEGain
# 						synMech = PVSynMech
# 						sec = 'perisom'
# 					else:  							# SOM->E
# 						weight = IEweight * cfg.IPTGain * cfg.SOMEGain
# 						synMech = SOMESynMech
# 						sec = 'spiny'
# 						synWeightFraction = cfg.synWeightFractionSOME
# 				if cellModel == 'HH_full':
# 					weight = weight * cfg.IFullGain


# 				ruleLabel = 'I_'+cellModel+'_'+str(i)+'_'+str(ipost)
# 				netParams.connParams[ruleLabel] = {
# 					'preConds': {'cellType': preCellType, 'ynorm': ynorm},
# 					'postConds': {'cellModel': cellModel, 'cellType': postCellType, 'ynorm': ynorm},
# 					'synMech': synMech,
# 					'probability': '1.0 * exp(-dist_3D/probLambda)',
# 					'weight': weight / cfg.synsperconn[cellModel],
# 					'delay': 'defaultDelay+dist_3D/propVelocity',
# 					'synsPerConn': cfg.synsperconn[cellModel],
# 					'synMechWeightFactor': synWeightFraction,
# 					'sec': sec,
# 					'disynapticBias': disynapticBias}

# #------------------------------------------------------------------------------
# # Long-range  connectivity parameters
# #------------------------------------------------------------------------------
# if cfg.addLongConn:

# 	# load load experimentally based parameters for long range inputs
# 	cmatLong = connLongData['cmat']
# 	binsLong = connLongData['bins']

# 	longPops = ['TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']
# 	cellTypes = ['IT', 'PT', 'CT', 'PV', 'SOM']
# 	EorI = ['exc', 'inh']
# 	syns = {'exc': ESynMech, 'inh': 'GABAA'}
# 	synFracs = {'exc': cfg.synWeightFractionEE, 'inh': [1.0]}

# 	for longPop in longPops:
# 		for ct in cellTypes:
# 			for EorI in ['exc', 'inh']:
# 				for i, (binRange, convergence) in enumerate(zip(binsLong[(longPop, ct)], cmatLong[(longPop, ct, EorI)])):
# 					for cellModel in cellModels:
# 						ruleLabel = longPop+'_'+ct+'_'+EorI+'_'+cellModel+'_'+str(i)
# 						netParams.connParams[ruleLabel] = { 
# 							'preConds': {'pop': longPop}, 
# 							'postConds': {'cellModel': cellModel, 'cellType': ct, 'ynorm': list(binRange)},
# 							'synMech': syns[EorI],
# 							'convergence': convergence,
# 							'weight': cfg.weightLong / cfg.synsperconn[cellModel], 
# 							'synMechWeightFactor': cfg.synWeightFractionEE,
# 							'delay': 'defaultDelay+dist_3D/propVelocity',
# 							'synsPerConn': cfg.synsperconn[cellModel],
# 							'sec': 'spiny'}

#------------------------------------------------------------------------------
# Subcellular connectivity (synaptic distributions)
#------------------------------------------------------------------------------   		

#------------------------------------------------------------------------------
# NetStim (LSPS pixel) -> PT (Sheets fig4)
if cfg.addSubConn and cfg.ihSubConn:
	lenX = 8
	lenY = 24 
	spacing = 50
	fixedSomaY = -735
	gridX = range(0, spacing*lenX, spacing)
	gridY = range(0, -spacing*lenY, -spacing)

	map2d = [[0 for _ in range(lenY)] for _ in range(lenX)]
	map2d[cfg.ihX][cfg.ihY] = 1

	netParams.subConnParams['ih'] = {
		'preConds': {'pop': ['GroupNetStimEPT','GroupNetStimEPT2']}, 
		'postConds': {'cellType': ['PT','PT2']},  
		'sec': 'spiny',
		'groupSynMechs': ESynMech, 
		'density': {'type': '2Dmap', 'gridX': gridX, 'gridY': gridY, 'gridValues': map2d, 'fixedSomaY': fixedSomaY}} 

#------------------------------------------------------------------------------
# NetStim (L2/3 stand-in) -> PT (Sheets fig11)
if cfg.stimSubConn:
	with open('conn/conn_dend_PT.json', 'r') as fileObj: connDendPTData = json.load(fileObj)
	with open('conn/conn_dend_IT.json', 'r') as fileObj: connDendITData = json.load(fileObj)
	

	lenY = 30 
	spacing = 50
	gridY = range(0, -spacing*lenY, -spacing)
	synDens, _, fixedSomaY = connDendPTData['synDens'], connDendPTData['gridY'], connDendPTData['fixedSomaY']
	for k in synDens.keys():
		prePop,postType = k.split('_')  # eg. split 'M2_PT'
		if prePop == 'L2': prePop = ['GroupNetStimEPT', 'GroupNetStimEPT2']  # include conns from layer 2/3 and 4
		netParams.subConnParams[k] = {
		'preConds': {'pop': prePop}, 
		'postConds': {'cellType': ['PT', 'PT2']},  
		'sec': 'spiny',
		'groupSynMechs': ESynMech, 
		'density': {'type': '1Dmap', 'gridX': None, 'gridY': gridY, 'gridValues': synDens[k], 'fixedSomaY': fixedSomaY}}

#------------------------------------------------------------------------------
# Network model
if cfg.addSubConn:
	with open('conn/conn_dend_PT.json', 'r') as fileObj: connDendPTData = json.load(fileObj)
	with open('conn/conn_dend_IT.json', 'r') as fileObj: connDendITData = json.load(fileObj)
	
	#------------------------------------------------------------------------------
	# L2/3,TVL,S2,cM1,M2 -> PT (Suter, 2015)
	lenY = 30 
	spacing = 50
	gridY = [i for i in range(0, -spacing*lenY, -spacing)]
	# gridY = range(0, -spacing*lenY, -spacing)
	synDens, _, fixedSomaY = connDendPTData['synDens'], connDendPTData['gridY'], connDendPTData['fixedSomaY']
	for k in synDens.keys():
		prePop,postType = k.split('_')  # eg. split 'M2_PT'
		if prePop == 'L2': prePop = 'IT2'  # include conns from layer 2/3 and 4
		netParams.subConnParams[k] = {
		'preConds': {'pop': prePop}, 
		'postConds': {'cellType': postType},  
		'sec': 'spiny',
		'groupSynMechs': ESynMech, 
		'density': {'type': '1Dmap', 'gridX': None, 'gridY': gridY, 'gridValues': synDens[k], 'fixedSomaY': fixedSomaY}} 


	#------------------------------------------------------------------------------
	# TPO, TVL, M2, OC  -> E (L2/3, L5A, L5B, L6) (Hooks 2013)
	lenY = 26
	spacing = 50
	gridY = [i for i in range(0, -spacing*lenY, -spacing)]
	# gridY = range(0, -spacing*lenY, -spacing)
	synDens, _, fixedSomaY = connDendITData['synDens'], connDendITData['gridY'], connDendITData['fixedSomaY']
	for k in synDens.keys():
		prePop,post = k.split('_')  # eg. split 'M2_L2'
		postCellTypes = ['IT','PT','CT'] if prePop in ['OC','TPO'] else ['IT','CT']  # only OC,TPO include PT cells
		postyRange = list(layer[post.split('L')[1]]) # get layer yfrac range 
		if post == 'L2': postyRange[1] = layer['4'][1]  # apply L2 rule also to L4 
		netParams.subConnParams[k] = {
		'preConds': {'pop': prePop}, 
		'postConds': {'ynorm': postyRange , 'cellType': postCellTypes},  
		'sec': 'spiny',
		'groupSynMechs': ESynMech, 
		'density': {'type': '1Dmap', 'gridX': None, 'gridY': gridY, 'gridValues': synDens[k], 'fixedSomaY': fixedSomaY}} 

	# Removed - Bellow this point the SubConn is not being used in the Sheets figure 8 and 9

	# #------------------------------------------------------------------------------
	# # S1, S2, cM1 -> E IT/CT; no data, assume uniform over spiny
	# netParams.subConnParams['S1,S2,cM1->IT,CT'] = {
	# 	'preConds': {'pop': ['S1','S2','cM1']}, 
	# 	'postConds': {'cellType': ['IT','CT']},
	# 	'sec': 'spiny',
	# 	'groupSynMechs': ESynMech, 
	# 	'density': 'uniform'} 


	# #------------------------------------------------------------------------------
	# # rest of local E->E (exclude IT2->PT); uniform distribution over spiny
	# netParams.subConnParams['IT2->non-PT'] = {
	# 	'preConds': {'pop': ['IT2']}, 
	# 	'postConds': {'cellType': ['IT','CT']},
	# 	'sec': 'spiny',
	# 	'groupSynMechs': ESynMech, 
	# 	'density': 'uniform'} 
		
	# netParams.subConnParams['non-IT2->E'] = {
	# 	'preConds': {'pop': ['IT4','IT5A','IT5B','PT5B','IT6','CT6']}, 
	# 	'postConds': {'cellType': ['IT','PT','CT']},
	# 	'sec': 'spiny',
	# 	'groupSynMechs': ESynMech, 
	# 	'density': 'uniform'} 


	# #------------------------------------------------------------------------------
	# # PV->E; perisomatic (no sCRACM)
	# netParams.subConnParams['PV->E'] = {
	# 	'preConds': {'cellType': 'PV'}, 
	# 	'postConds': {'cellType': ['IT', 'CT', 'PT']},  
	# 	'sec': 'perisom', 
	# 	'density': 'uniform'} 


	# #------------------------------------------------------------------------------
	# # SOM->E; apical dendrites (no sCRACM)
	# netParams.subConnParams['SOM->E'] = {
	# 	'preConds': {'cellType': 'SOM'}, 
	# 	'postConds': {'cellType': ['IT', 'CT', 'PT']},  
	# 	'sec': 'apicdend',
	# 	'groupSynMechs': SOMESynMech,
	# 	'density': 'uniform'} 


	# #------------------------------------------------------------------------------
	# # All->I; apical dendrites (no sCRACM)
	# netParams.subConnParams['All->I'] = {
	# 	'preConds': {'cellType': ['IT', 'CT', 'PT', 'SOM', 'PV']+longPops}, 
	# 	'postConds': {'cellType': ['SOM', 'PV']},  
	# 	'sec': 'spiny',
	# 	'groupSynMechs': ESynMech,
	# 	'density': 'uniform'} 