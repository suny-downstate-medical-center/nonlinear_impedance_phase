import pandas as pd 
import json 
import numpy as np 
from matplotlib import pyplot as plt
from math import radians 
from scipy.signal import find_peaks 
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go

# simulation parameters 
# secs = ['apic_36', 'apic_12', 'apic_0']
secs = ['apic_0', 'apic_12', 'apic_36']
dists = [23.1, 261.4, 504.2]

# fig, axs = plt.subplots(2, 2, sharey=True)
fig, axs = plt.subplots(2, 2)
fig.set_figwidth(10.5)
fig.set_figheight(9)

#########################################################
# frequency dependent data 
fd = {'section' : [], 'amp' : [], 'angles' : [], 'f0' : [], 'f1' : [], 'lags' : [], 'freqs' : [], 'dist' : [], 
    'dlag' : [], 'stim_cycle' : [], 'blockIh' : []}
# for sec, dist, amp in zip(secs, dists, origamps):
sec = 'apic_0' 
amp = '1.0'
dist = dists[0]
freqs = [str(i) for i in range(2,10)]
for freq in freqs:
    filename = 'HayCellMig_%s_amp_%s_offset_0.0_f0_%s_f1_%s.json' % (sec, amp, freq, freq)
    with open('Data/supra_data/' + filename) as fileObj:
        data = json.load(fileObj)
    fd['section'].append(sec)
    fd['dist'].append(dist)
    fd['amp'].append(float(amp))
    fd['f0'].append(float(freq))
    fd['f1'].append(float(freq))
    # if len(data['lags']) > 1:
    #     fd['lags'].append(data['lags'][1:])
    #     fd['dlag'].append(np.subtract(data['lags'][1:], data['lags'][1]))
    #     fd['freqs'].append(data['freq'][1:])
    #     fd['angles'].append(data['angles'][1:])
    #     fd['stim_cycle'].append([i+1 for i in range(len(data['lags'])-1)])
    #     fd['blockIh'].append('False')
    if len(data['lags']) > 1:
        fd['lags'].append(data['lags'])
        fd['dlag'].append(np.subtract(data['lags'], data['lags'][0]))
        fd['freqs'].append(data['freq'])
        fd['angles'].append(data['angles'])
        fd['stim_cycle'].append([i for i in range(len(data['lags']))])
        fd['blockIh'].append('False')
    else:
        fd['lags'].append([])
        fd['dlag'].append([])
        fd['angles'].append([])
        fd['freqs'].append([])
        fd['stim_cycle'].append([])
        fd['blockIh'].append('False')

fdf = pd.DataFrame(data=fd)

tempdf = fdf[fdf['section'] == sec]
normF = [(float(f)-float(freqs[0])) / (float(freqs[-1])-float(freqs[0])) for f in freqs]
cols = plt.cm.jet(normF)
for f, c in zip(freqs, cols):
    x = tempdf[tempdf['f1'] == float(f)][tempdf['blockIh'] == 'False']['stim_cycle'].values[0][:14]
    y = tempdf[tempdf['f1'] == float(f)][tempdf['blockIh'] == 'False']['angles'].values[0][:14]
    y = [radians(val)*-1 for val in y]
    if f == '8':
        axs[1][0].plot(x, y, 'o-', color='black', label=f+' Hz')
    else:
        axs[1][0].plot(x, y, 'o-', color=c, label=f+' Hz')
    # x = tempdf[tempdf['f1'] == float(f)][tempdf['blockIh'] == 'True']['stim_cycle'].values[0]
    # y = tempdf[tempdf['f1'] == float(f)][tempdf['blockIh'] == 'True']['dlag'].values[0]
    # axs[1][ind].plot(x, y, 'o-', color=c, label=f+' Hz')
axs[1][0].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18) #set_title('Frequency Dependence', fontsize=18)
axs[1][0].plot([0,15],[0,0], 'k:')
leg = axs[1][0].legend(title='Stimulus Frequency', loc='lower right')
# axs[0][0].set_ylabel(r'Stimulus Phase of Spike (rad)', fontsize=18)
# axs[1][0].set_xlim(0.8, 14.2)
axs[1][0].set_xlim(-0.2, 14.2)
# axs[0][0].set_xlabel('Stimulus Cycle', fontsize=18)

##################################################3
# amplitude dependent data
ad =  {'section' : [], 'amp' : [], 'angles' : [], 'f0' : [], 'f1' : [], 'lags' : [], 'freqs' : [], 'dist' : [], 
    'dlag' : [], 'stim_cycle' : [], 'blockIh' : []}
# for freq, famps in zip(freqs, allfamps):
freq = '8'
amps = ['0.9', '1.0', '1.1', '1.2', '1.3', '1.4',
        '1.5', '1.6']
for amp in amps:
    filename = 'HayCellMig_%s_amp_%s_offset_0.0_f0_%s_f1_%s.json' % (sec, amp, freq, freq)
    with open('Data/supra_data/' + filename) as fileObj:
        data = json.load(fileObj)
    ad['section'].append(sec)
    ad['dist'].append(dist)
    ad['amp'].append(float(amp))
    ad['f0'].append(float(freq))
    ad['f1'].append(float(freq))
    # if len(data['lags']) > 1:
    #     ad['lags'].append(data['lags'][1:])
    #     ad['dlag'].append(np.subtract(data['lags'][1:], data['lags'][1]))
    #     ad['freqs'].append(data['freq'][1:])
    #     ad['angles'].append(data['angles'][1:])
    #     ad['stim_cycle'].append([i+1 for i in range(len(data['lags'])-1)])
    #     ad['blockIh'].append('False')
    if len(data['lags']) > 1:
        ad['lags'].append(data['lags'])
        ad['dlag'].append(np.subtract(data['lags'], data['lags'][0]))
        ad['freqs'].append(data['freq'])
        ad['angles'].append(data['angles'])
        ad['stim_cycle'].append([i for i in range(len(data['lags']))])
        ad['blockIh'].append('False')
    else:
        ad['lags'].append([])
        ad['dlag'].append([])
        ad['angles'].append([])
        ad['freqs'].append([])
        ad['stim_cycle'].append([])
        ad['blockIh'].append('False')
adf = pd.DataFrame(data=ad)

## plotting 
f = freq 
tempdf = adf[adf['section'] == sec]
normF = [(float(a) - float(amps[0])) / (float(amps[-1])-float(amps[0])) for a in amps]
cols = plt.cm.plasma(normF)
for amp, c in zip(amps, cols):
    x = tempdf[tempdf['amp'] == float(amp)][tempdf['f1'] == float(f)]['stim_cycle'].values[0][:14]
    y = tempdf[tempdf['amp'] == float(amp)][tempdf['f1'] == float(f)]['angles'].values[0][:14]
    y = [radians(val)*-1 for val in y]
    if amp == '1.0':
        axs[1][1].plot(x, y, 'o-', color='black', label=amp+' nA')
    else:
        axs[1][1].plot(x, y, 'o-', color=c, label=amp+' nA')
axs[1][1].plot([0,15],[0,0], 'k:')
axs[1][1].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18) #set_title('Amplitude Dependence', fontsize=18)
leg = axs[1][1].legend(title='Stimulus Amplitude', loc='lower right')
# axs[1][1].set_xlim(0.8, 14.2)
axs[1][1].set_xlim(-0.2, 14.2)

#################################################################
# location dependence 
filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8.json'
with open('Data/supra_data/' + filename) as fileObj:
    peri = json.load(fileObj)
filename = 'HayCellMig_apic_36_amp_3.45_offset_0.0_f0_8_f1_8.json'
with open('Data/supra_data/' + filename) as fileObj:
    apical = json.load(fileObj)

## plotting 
# axs[0][1].plot([i+1 for i in range(len(peri['lags'])-1)], [radians(val)*-1 for val in peri['angles'][1:]], 'o-', color='black', label='Soma')
# axs[0][1].plot([i+1 for i in range(len(apical['lags'])-1)], [radians(val)*-1 for val in apical['angles'][1:]], '^-', color='black', label='Apical')
ax2 = axs[0][1].twinx()
axs[0][1].plot([i for i in range(len(peri['lags']))], [radians(val)*-1 for val in peri['angles']], 'o-', color='black', label='Soma')
# axs[0][1].plot([i for i in range(len(apical['lags']))], [radians(val)*-1 for val in apical['angles']], '^-', color='black', label='Dendrite')
ax2.plot([i for i in range(len(apical['lags']))], [radians(val)*-1 for val in apical['angles']], '^-', color='black', label='Dendrite')
axs[0][1].plot([0, 14.2], [0, 0], 'k:')
# axs[0][1].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18) #set_title('Location Dependence', fontsize=18)
axs[0][1].set_ylabel(r'$\Phi_n^+$ (rad) (Soma Stim.)', fontsize=18)
ax2.set_ylabel(r'$\Phi_n^+$ (rad) (Dendrite Stim.)', fontsize=18)     
ax2.set_ylim(-0.75,0.25)
axs[0][1].set_ylim(-0.45,0.55)
# leg = axs[0][1].legend(title='Stimulus Location', loc='center right')
# axs[0][1].set_xlim(0.8, 14.2)
axs[0][1].set_xlim(-0.2, 14.2)

#################################################################
# ih dependence 
filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_blockIh.json'
with open('Data/supra_data/' + filename) as fileObj:
    block = json.load(fileObj)
filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_blockSKE.json'
with open('supra_data/' + filename) as fileObj:
    blockSK = json.load(fileObj)

## plotting 
# axs[0][0].plot([i+1 for i in range(len(peri['lags'])-1)], [radians(val)*-1 for val in peri['angles'][1:]], 'o-', color='black', label='Control')
# axs[0][0].plot([i+1 for i in range(len(block['lags'])-1)], [radians(val)*-1 for val in block['angles'][1:]], 'o-', color='gray', label=r'Block I$_h$')
# axs[0][0].plot([i+1 for i in range(len(blockSK['lags'])-1)], [radians(val)*-1 for val in blockSK['angles'][1:]], 'o-', color='green', label=r'Block SK')
axs[0][0].plot([i for i in range(len(peri['lags']))], [radians(val)*-1 for val in peri['angles']], 'o-', color='black', label='Control')
axs[0][0].plot([i for i in range(len(block['lags']))], [radians(val)*-1 for val in block['angles']], 'o-', color='gray', label=r'Block I$_h$')
axs[0][0].plot([i for i in range(len(blockSK['lags']))], [radians(val)*-1 for val in blockSK['angles']], 'o-', color='green', label=r'Block I$_{AHP}$')
axs[0][0].plot([0, 14.2], [0, 0], 'k:')
axs[0][0].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18) #set_title(r'I$_h$/I$_{AHP}$ Dependence', fontsize=18)
leg = axs[0][0].legend(title='Condition', loc='center right')
# axs[0][0].set_xlim(0.8, 14.2)
axs[0][0].set_xlim(-0.2, 14.2)

# fig.text(0.43, 0.04, 'Stimulus Cycle (n)', fontsize=18)
# fig.text(0.05, 0.4, r'$\Phi_n^+$ (rad)', fontsize=18, rotation=90)

# trace 
filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8.npy'
traces = np.load('supra_traces/'+filename, allow_pickle=True)
traces = traces[()]
fig2 = plt.figure()
ax = fig2.add_subplot(1,1,1)
ax.plot(traces['time'], traces['soma_v'], label=r'V$_{soma}$')
ax.plot(traces['time'], traces['i'] * 10 - 70, 'k', label='Stimulus')
ipks, _ = find_peaks(traces['i'])
for pk in ipks:
    ax.plot([traces['time'][pk], traces['time'][pk]], [-100, 30], 'k:')
ax.set_xticks([])
ax.set_yticks([])
ax.legend(fontsize=14, loc='lower right')

plt.ion()
plt.show()