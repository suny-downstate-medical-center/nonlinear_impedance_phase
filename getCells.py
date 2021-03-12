import os
import sys

active_model_ids = [497229117, 491766131, 497232312, 485591806,
		497232419, 497232429, 496930324, 497232564, 497232839, 497232946,
		497233049, 497233139, 497233307, 497229124]

class allenCell:
	def __init__(self):
		self.basal = []
		self.apical = []
		self.soma = []
		self.axon = []

	def generate_cell(self, h):
		for sec in h.soma:
			self.soma.append(sec)
		for sec in h.apic:
			self.apical.append(sec)
		for sec in h.dend:
			self.basal.append(sec)
		for sec in h.axon:
			self.axon.append(sec)

def GetAllenCells(neuronal_model_ids):

	from allensdk.api.queries.biophysical_api import BiophysicalApi

	bp = BiophysicalApi()
	bp.cache_stimulus = False # change to True to download the large stimulus NWB file

	for neuronal_model_id in neuronal_model_ids:
		os.system('mkdir models/' + str(neuronal_model_id))
		bp.cache_data(neuronal_model_id, working_directory=str(neuronal_model_id))
		os.system('cd ' + str(neuronal_model_id) + '; nrnivmodl ./modfiles; cd ../../')

def AllenCell(path = None):
	owd = os.getcwd()
	os.chdir(path)
	# sys.path.append('/home/craig_kelley_downstate_edu/allensdk/lib/python3.6/site-packages/')
	from allensdk.model.biophys_sim.config import Config                                         
	from allensdk.model.biophysical import utils as Utils # this is basically "implied" in the tutorial                                   
	description = Config().load('manifest.json')  
	manifest = description.manifest                                                              
	morphology_path = description.manifest.get_path('MORPHOLOGY') 
	utils = Utils.create_utils(description, model_type='Biophysical - all active') # this is insane - help doc says ALL_ACTIVE_TYPE or PERISOMATIC_TYPE for model_type
	h = utils.h
	utils.generate_morphology(morphology_path) # in tutorial, they instead use mophology_path.encode('ascii','ignore')
	utils.load_cell_parameters()
	cell = allenCell()
	cell.generate_cell(h)
	os.chdir(owd)
	return cell 

def KoleCell():
	owd = os.getcwd()
	os.chdir('./models/Kole')
	from neuron import h, init
	# h.load_file("/usr/local/nrn//share/nrn/lib/hoc/stdrun.hoc")
	h.load_file('stdrun.hoc')
	h.load_file('cellTemplate.hoc')
	cell = h.KoleCell()
	apical_maintrunk = [0, 8, 10, 18, 30, 32, 34, 36, 42, 44]
	# apical_maintrunk = [cell.apic[0], cell.apic[8], cell.apic[10], cell.apic[18],cell.apic[30], 
	# 	cell.apic[32], cell.apic[34], cell.apic[36], cell.apic[42], cell.apic[44]]
	os.chdir(owd)
	return cell, apical_maintrunk

def AckerAnticCell():
	owd = os.getcwd()
	os.chdir('./models/AckerAntic')
	import sys 
	sys.path.insert(1, './cells/')
	from eeeD import MakeCell
	cell = MakeCell()
	cell.apical_maintrunk = [i for i in range(2,9)]
	# for i in range(2,9):
	# 	cell.apical_maintrunk.append(cell.apical[i])
	os.chdir(owd)
	return cell

def NeymotinHarnettCell(slope=14*2):
	owd = os.getcwd()
	os.chdir('./models/Neymotin')
	from neuron import h, init
	h.load_file("./cells/PTcell.hoc")
	ihMod2str = {'harnett': 1, 'kole': 2, 'migliore': 3}
	cell = h.PTcell(ihMod2str['harnett'], slope)
	os.chdir(owd)
	return cell

def NeymotinKoleCell(slope=14*2):
	owd = os.getcwd()
	os.chdir('./models/Neymotin')
	from neuron import h, init
	h.load_file("./cells/PTcell.hoc")
	ihMod2str = {'harnett': 1, 'kole': 2, 'migliore': 3}
	cell = h.PTcell(ihMod2str['kole'], slope)
	os.chdir(owd)
	return cell

def NeymotinMiglioreCell(slope=14*2):
	owd = os.getcwd()
	os.chdir('./models/Neymotin')
	from neuron import h, init
	h.load_file("./cells/PTcell.hoc")
	ihMod2str = {'harnett': 1, 'kole': 2, 'migliore': 3}
	cell = h.PTcell(ihMod2str['migliore'], slope)
	os.chdir(owd)
	return cell

def HayCell(morphology_file = './morphologies/cell1.asc'):
	owd = os.getcwd()
	os.chdir('./models/Hay')
	from neuron import h#, init
	h.load_file('stdrun.hoc')
	h.load_file('import3d.hoc')
	h.load_file('./models/L5PCbiophys3.hoc') # BAP version
	h.load_file('./models/L5PCtemplate.hoc')
	cell = h.L5PCtemplate(morphology_file)
	apical_maintrunk = [0,1,2,3,14,20,26,34,36]
	# apical_maintrunk = [cell.apic[0], cell.apic[1], cell.apic[2], cell.apic[3],
	# 	cell.apic[14], cell.apic[20], cell.apic[26], cell.apic[34], cell.apic[36]]
	os.chdir(owd)
	return cell, apical_maintrunk

def HayCellMig(morphology_file = './morphologies/cell1.asc'):
	owd = os.getcwd()
	os.chdir('./models/Hay')
	from neuron import h#, init
	h.load_file('stdrun.hoc')
	h.load_file('import3d.hoc')
	h.load_file('./models/L5PCbiophysMig.hoc') # BAP version
	h.load_file('./models/L5PCtemplate.hoc')
	cell = h.L5PCtemplate(morphology_file)
	apical_maintrunk = [0,1,2,3,14,20,26,34,36]
	# apical_maintrunk = [cell.apic[0], cell.apic[1], cell.apic[2], cell.apic[3],
	# 	cell.apic[14], cell.apic[20], cell.apic[26], cell.apic[34], cell.apic[36]]
	os.chdir(owd)
	return cell, apical_maintrunk

def HayCellSWC(morphology_file = '../suter_shepherd/BS0284.CNG.swc'):
	owd = os.getcwd()
	os.chdir('./models/Hay')
	from neuron import h#, init
	# h.load_file("/usr/local/nrn//share/nrn/lib/hoc/stdrun.hoc")
	# h.load_file('/usr/local/nrn//share/nrn/lib/hoc/import3d.hoc')
	h.load_file('stdrun.hoc')
	h.load_file('import3d.hoc')
	# h.load_file('./models/L5PCbiophys3.hoc') # BAP version
	h.load_file('./models/L5PCbiophysMig.hoc')
	h.load_file('./models/templateSWC.hoc')
	cell = h.templateSWC(morphology_file)
	os.chdir(owd)
	return cell

def M1Cell():
	owd = os.getcwd()
	os.chdir('models/DuraBernal')
	from netParams_unified import netParams 
	from cfg_unified import cfg
	from netpyne import sim 
	sim.create(netParams, cfg)
	os.chdir(owd)
	return sim 