from matplotlib import pyplot as plt 
import json 
import numpy as np 

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    base = json.load(fileObj)

# holding/resting voltage 
fig2, axs2 = plt.subplots(2,2, sharex=True, sharey=True)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_-0.22_f0_0_f1_12.json', 'rb') as fileObj:
    low = json.load(fileObj)
with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_-0.55_f0_0_f1_12.json', 'rb') as fileObj:
    lower = json.load(fileObj)

# ll = r'$\Phi^-$: %.0f mV' %  (base['v_init'])
# lu = r'$\Phi^+$: %.0f mV' %  (base['v_init'])
ll = r'$\Phi^-$: Baseline'
lu = r'$\Phi^+$: Baseline'
axs2[1][0].plot(base['f_minus'], base['phi_minus'], 'b-', label=ll)
axs2[1][0].plot(base['f_plus'], base['phi_plus'], 'b--', label=lu)
# ll = r'$\Phi^-$: %.0f mV' %  (low['v_init'])
# lu = r'$\Phi^+$: %.0f mV' %  (low['v_init'])
ll = r'$\Phi^-$: Baseline - 5 mV'
lu = r'$\Phi^+$: Baseline - 5 mV'
axs2[1][0].plot(low['f_minus'], low['phi_minus'], 'm-', label=ll)
axs2[1][0].plot(low['f_plus'], low['phi_plus'], 'm--', label=lu)
# ll = r'$\Phi^-$: %.0f mV' %  (lower['v_init'])
# lu = r'$\Phi^+$: %.0f mV' %  (lower['v_init'])
ll = r'$\Phi^-$: Baseline - 10 mV'
lu = r'$\Phi^+$: Baseline - 10 mV'
axs2[1][0].plot(lower['f_minus'], lower['phi_minus'], 'g-', label=ll)
axs2[1][0].plot(lower['f_plus'], lower['phi_plus'], 'g--', label=lu)
axs2[1][0].legend(title=r'RMP')
axs2[0][0].set_ylabel(r'$\Phi$(f)$^{+/-}$ (rad)', fontsize=16)
axs2[1][0].set_xlabel('Frequency (Hz)', fontsize=16)
axs2[1][0].plot([0,12], [0,0], 'k:')
axs2[1][0].set_xlim(0.5,10)
axs2[1][0].set_title(r'RMP Dependence', fontsize=18)

## sync freq and total inductive phase 
data = [lower, low, base]
vholdfig, vholdaxs = plt.subplots(1,2, sharex=True)

### sync freq 
sync_minus = [d['f_minus'][np.argmin(np.square(np.array(d['phi_minus'])-0))] for d in data]
sync_plus = [d['f_plus'][np.argmin(np.square(np.array(d['phi_plus'])-0))] for d in data]
vhold = [d['v_init'] for d in data]
vholdaxs[0].plot(vhold, sync_minus, 'k*-')
vholdaxs[0].plot(vhold, sync_plus, 'k*--')

### inductive phase 
induc_plus = []
induc_minus = []
for d in data:
    lead_plus = [p for p in d['phi_plus'] if p > 0]
    lead_minus = [p for p in d['phi_minus'] if p > 0]
    flead_plus = [f for p, f in zip(d['phi_plus'], d['f_plus']) if p > 0]
    flead_minus = [f for p, f in zip(d['phi_minus'], d['f_minus']) if p > 0]
    induc_plus.append(np.trapz(lead_plus, flead_plus))
    induc_minus.append(np.trapz(lead_minus, flead_minus))
vholdaxs[1].plot(vhold, induc_minus, 'k*-')
vholdaxs[1].plot(vhold, induc_plus, 'k*--')
vholdaxs[0].set_xlabel(r'V$_{hold}$', fontsize=14)
vholdaxs[0].set_ylabel('Synchony Point (Hz)', fontsize=14)
vholdaxs[1].set_xlabel(r'V$_{hold}$', fontsize=14)
vholdaxs[1].set_ylabel('Total Inductive Phase (Hz*radians)', fontsize=14)

# amplitude / asymmetry dependence 
with open('asym_data/HayCellMig_apic_0_amp_0.2_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    low = json.load(fileObj)
with open('asym_data/HayCellMig_apic_0_amp_0.05_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    lower = json.load(fileObj)

# ll = r'$\Phi^-$: %.1f mV' %  (base['asym'])
# lu = r'$\Phi^+$: %.1f mV' %  (base['asym'])
ll = r'$\Phi^-$: 0.4 nA' # %  (base['asym'])
lu = r'$\Phi^+$: 0.4 nA' # %  (base['asym'])
axs2[1][1].plot(base['f_minus'], base['phi_minus'], 'b-', label=ll)
axs2[1][1].plot(base['f_plus'], base['phi_plus'], 'b--', label=lu)
# ll = r'$\Phi^-$: %.1f mV' %  (low['asym'])
# lu = r'$\Phi^+$: %.1f mV' %  (low['asym'])
ll = r'$\Phi^-$: 0.2 nA' # %  (low['asym'])
lu = r'$\Phi^+$: 0.2 nA' # %  (low['asym'])
axs2[1][1].plot(low['f_minus'], low['phi_minus'], 'm-', label=ll)
axs2[1][1].plot(low['f_plus'], low['phi_plus'], 'm--', label=lu)
# ll = r'$\Phi^-$: %.1f mV' %  (lower['asym'])
# lu = r'$\Phi^+$: %.1f mV' %  (lower['asym'])
ll = r'$\Phi^-$: 0.05 nA' # %  (lower['asym'])
lu = r'$\Phi^+$: 0.05 nA' # %  (lower['asym'])
axs2[1][1].plot(lower['f_minus'], lower['phi_minus'], 'g-', label=ll)
axs2[1][1].plot(lower['f_plus'], lower['phi_plus'], 'g--', label=lu)
axs2[1][1].legend(title='Stimulus Amplitude')
# axs[0][1].set_ylabel(r'$\Phi$(f)$^{+/-}$ (rad)', fontsize=16)
# axs[0][1].set_xlabel('Frequency (Hz)', fontsize=16)
axs2[1][1].plot([0,12], [0,0], 'k:')
axs2[1][1].set_xlim(0.5,10)
axs2[1][1].set_title('Amplitude Dependence', fontsize=18)

## sync freq and total inductive phase 
data = [lower, low, base]
amps = [0.05, 0.1, 0.4]
ampfig, ampaxs = plt.subplots(1,2, sharex=True)

### sync freq 
sync_minus = [d['f_minus'][np.argmin(np.square(np.array(d['phi_minus'])-0))] for d in data]
sync_plus = [d['f_plus'][np.argmin(np.square(np.array(d['phi_plus'])-0))] for d in data]
ampaxs[0].plot(amps, sync_minus, '*-')
ampaxs[0].plot(amps, sync_plus, '*--')

### inductive phase 
induc_plus = []
induc_minus = []
for d in data:
    lead_plus = [p for p in d['phi_plus'] if p > 0]
    lead_minus = [p for p in d['phi_minus'] if p > 0]
    flead_plus = [f for p, f in zip(d['phi_plus'], d['f_plus']) if p > 0]
    flead_minus = [f for p, f in zip(d['phi_minus'], d['f_minus']) if p > 0]
    induc_plus.append(np.trapz(lead_plus, flead_plus))
    induc_minus.append(np.trapz(lead_minus, flead_minus))
ampaxs[1].plot(amps, induc_minus, '*-')
ampaxs[1].plot(amps, induc_plus, '*--')

# location dependence 
with open('asym_data/HayCellMig_apic_12_amp_0.3_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    apic = json.load(fileObj)

ll = r'$\Phi^-$: Somatic'
lu = r'$\Phi^+$: Somatic'
axs2[0][1].plot(base['f_minus'], base['phi_minus'], 'b-', label=ll)
axs2[0][1].plot(base['f_plus'], base['phi_plus'], 'b--', label=lu)
ll = r'$\Phi^-$: Apical'
lu = r'$\Phi^+$: Apical'
axs2[0][1].plot(apic['f_minus'], apic['phi_minus'], 'r-', label=ll)
axs2[0][1].plot(apic['f_plus'], apic['phi_plus'], 'r--', label=lu)
axs2[0][1].legend(title='Stimulus Location')
axs2[1][0].set_ylabel(r'$\Phi$(f)$^{+/-}$ (rad)', fontsize=16)
axs2[1][1].set_xlabel('Frequency (Hz)', fontsize=16)
axs2[0][1].plot([0,12], [0,0], 'k:')
axs2[0][1].set_xlim(0.5,10)
axs2[0][1].set_title('Location Dependence', fontsize=18)
### inductive phase 
induc_plus = []
induc_minus = []
for d in data:
    lead_plus = [p for p in apic['phi_plus'] if p > 0]
    lead_minus = [p for p in apic['phi_minus'] if p > 0]
    flead_plus = [f for p, f in zip(apic['phi_plus'], apic['f_plus']) if p > 0]
    flead_minus = [f for p, f in zip(apic['phi_minus'], apic['f_minus']) if p > 0]
    induc_plus.append(np.trapz(lead_plus, flead_plus))
    induc_minus.append(np.trapz(lead_minus, flead_minus))
sync_minus = [apic['f_minus'][np.argmin(np.square(np.array(apic['phi_minus'])-0))] for d in data]
sync_plus = [apic['f_plus'][np.argmin(np.square(np.array(apic['phi_plus'])-0))] for d in data]
print('apical values')
print('L+: ' + str(induc_plus))
print('L-: ' + str(induc_minus))
print('s+: ' + str(sync_plus))
print('s-: ' + str(sync_minus))

# h-current dependence 
with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12_blockIh.json', 'rb') as fileObj:
    block = json.load(fileObj)

ll = r'$\Phi^-$: Baseline'
lu = r'$\Phi^+$: Baseline'
axs2[0][0].plot(base['f_minus'], base['phi_minus'], 'b-', label=ll)
axs2[0][0].plot(base['f_plus'], base['phi_plus'], 'b--', label=lu)
ll = r'$\Phi^-$: Block I$_h$'
lu = r'$\Phi^+$: Block I$_h$'
axs2[0][0].plot(block['f_minus'], block['phi_minus'], 'r-', label=ll)
axs2[0][0].plot(block['f_plus'], block['phi_plus'], 'r--', label=lu)
# axs2[1][1].set_ylabel(r'$\Phi$(f)$^{+/-}$ (rad)', fontsize=16)
axs2[1][0].set_xlabel('Frequency (Hz)', fontsize=16)
axs2[0][0].plot([0,12], [0,0], 'k:')
axs2[0][0].legend(title='Condition')
axs2[0][0].set_xlim(0.5,10)
axs2[0][0].set_title(r'I$_h$ Dependence', fontsize=18)

# traces and phases 
fig = plt.figure(constrained_layout=True)
# fig = plt.figure()
subfigs = fig.subfigures(nrows=4, ncols=1)
axs0 = subfigs[0].subplots(nrows=1, ncols=2)
axs1 = subfigs[1].subplots(nrows=1, ncols=2)
axs2 = subfigs[2].subplots(nrows=1, ncols=2)
axs3 = subfigs[3].subplots(nrows=1, ncols=2)
subfigs[0].suptitle('Subthreshold, Linear Response', fontsize=16)
subfigs[1].suptitle('Subthreshold, Nonlinear Response', fontsize=16)
subfigs[2].suptitle('Suprathreshold w/ TTX', fontsize=16)
subfigs[3].suptitle('Suprathreshold', fontsize=16)
# fig, axs = plt.subplots(4, 2)

with open('sub_data/HayCellMig_apic_0_amp_0.025_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    chirp_data = json.load(fileObj)
with open('asym_data/HayCellMig_apic_0_amp_0.025_offset_0.0_f0_0_f1_13.json', 'rb') as fileObj:
    asym_data = json.load(fileObj)
chirp_traces = np.load('sub_traces/HayCellMig_apic_0_amp_0.025_offset_0.0_f0_0_f1_12.npy', allow_pickle=True)
chirp_traces = chirp_traces[()]
soma_v = [v for v, t in zip(chirp_traces['soma_v'], chirp_traces['time']) if 2500 < t < 15500]
time = [(t/1000)-3  for t in chirp_traces['time'] if 2500 < t < 15500]
axs0[0].plot(time, soma_v, 'k')
axs0[1].plot(chirp_data['Freq'], chirp_data['ZinPhase'], 'k')
axs0[1].plot(asym_data['f_minus'], asym_data['phi_minus'], color='gray')
axs0[1].plot(asym_data['f_plus'], asym_data['phi_plus'], '--', color='gray')
axs0[1].plot([0,12], [0,0], 'k:')
axs0[0].set_xlim(-0.5,12.5)
axs0[1].set_xlim(0.5, 12)
axs0[0].set_ylabel(r'V$_{memb}$ (mV)', fontsize=14)
axs0[1].set_ylabel(r'$\Phi$(f) (rad)', fontsize=14)
chirp_data_orig = chirp_data

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    chirp_data = json.load(fileObj)
chirp_traces = np.load('asym_traces/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.npy', allow_pickle=True)
chirp_traces = chirp_traces[()]
soma_v = [v for v, t in zip(chirp_traces['soma_v'], chirp_traces['time']) if 2500 < t < 15500]
time = [(t/1000)-3  for t in chirp_traces['time'] if 2500 < t < 15500]
axs1[0].plot(time, soma_v, 'b')
axs1[1].plot(chirp_data['f_minus'], chirp_data['phi_minus'], 'b-')
axs1[1].plot(chirp_data['f_plus'], chirp_data['phi_plus'], 'b--')
axs1[1].plot(chirp_data_orig['Freq'], chirp_data_orig['ZinPhase'], 'k')
axs1[1].plot([0,12], [0,0], 'k:')
axs1[0].set_xlim(-0.5,12.5)
axs1[1].set_xlim(0.5, 12)
axs1[0].set_ylabel(r'V$_{memb}$ (mV)', fontsize=14)
axs1[1].set_ylabel(r'$\Phi^{+/-}$(f) (rad)', fontsize=14)

with open('asym_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_0_f1_12_TTX.json', 'rb') as fileObj:
    chirp_data = json.load(fileObj)
chirp_traces = np.load('asym_traces/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_0_f1_12_TTX.npy', allow_pickle=True)
chirp_traces = chirp_traces[()]
soma_v = [v for v, t in zip(chirp_traces['soma_v'], chirp_traces['time']) if 2500 < t < 15500]
time = [(t/1000)-3  for t in chirp_traces['time'] if 2500 < t < 15500]
axs2[0].plot(time, soma_v, 'g')
axs2[1].plot(chirp_data['f_minus'], chirp_data['phi_minus'], 'g-')
axs2[1].plot(chirp_data['f_plus'], chirp_data['phi_plus'], 'g--')
axs2[1].plot(chirp_data_orig['Freq'], chirp_data_orig['ZinPhase'], 'k')
axs2[1].plot([0,12], [0,0], 'k:')
axs2[0].set_xlim(-0.5,12.5)
axs2[1].set_xlim(0.5, 12)
axs2[0].set_ylabel(r'V$_{memb}$ (mV)', fontsize=14)
axs2[1].set_ylabel(r'$\Phi^{+/-}$(f) (rad)', fontsize=14)

with open('asym_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    chirp_data = json.load(fileObj)
chirp_traces = np.load('asym_traces/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_0_f1_12.npy', allow_pickle=True)
chirp_traces = chirp_traces[()]
soma_v = [v for v, t in zip(chirp_traces['soma_v'], chirp_traces['time']) if 2500 < t < 15500]
time = [(t/1000)-3  for t in chirp_traces['time'] if 2500 < t < 15500]
axs3[0].plot(time, soma_v, 'm')
axs3[1].plot(chirp_data['f_minus'], chirp_data['phi_minus'], 'm-')
axs3[1].plot(chirp_data['f_plus'], chirp_data['phi_plus'], 'm--')
axs3[1].plot(chirp_data_orig['Freq'], chirp_data_orig['ZinPhase'], 'k')
axs3[1].plot([0,12], [0,0], 'k:')
axs3[0].set_xlim(-0.5,12.5)
axs3[1].set_xlim(0.5, 12)
axs3[0].set_ylabel(r'V$_{memb}$ (mV)', fontsize=14)
axs3[1].set_ylabel(r'$\Phi^{+/-}$(f) (rad)', fontsize=14)
axs3[0].set_xlabel('Time (s)', fontsize=14)
axs3[1].set_xlabel('Frequency (Hz)', fontsize=14)

plt.ion()
plt.show()