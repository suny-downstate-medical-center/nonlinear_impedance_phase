import pandas as pd 
import json 
import numpy as np 
from matplotlib import pyplot as plt
from scipy.signal import find_peaks 
from math import radians 
import argparse

parser = argparse.ArgumentParser(description = '''Plot phase advance data''')
parser.add_argument('--stim_location', nargs='?', type=str, default='soma')
parser.add_argument('--location_version', nargs='?', type=str, default='derivative')
parser.add_argument('--arrangement', nargs='?', type=str, default='original')
args = parser.parse_args()
ver = args.stim_location #'soma' #'soma'
loc_ver = args.location_version

secs = ['apic_0', 'apic_12', 'apic_36']
dists = [23.1, 261.4, 504.2]

if args.arrangement == 'original':
    fig, axs = plt.subplots(2, 2) #, sharey=True)
    fig.set_figwidth(10.5)
    fig.set_figheight(9)
else:
    fig, axs = plt.subplots(1, 3) #, sharey=True)
    fig.set_figwidth(12)
    fig.set_figheight(6)

#########################################################
# frequency dependent data 
fd = {'section' : [], 'amp' : [], 'angles' : [], 'f0' : [], 'f1' : [], 'lags' : [], 'freqs' : [], 'dist' : [], 
    'dlag' : [], 'stim_cycle' : [], 'blockIh' : []}
# for sec, dist, amp in zip(secs, dists, origamps):
if ver == 'soma':
    sec = 'apic_0' 
    amp = '1.9'
    symbol = 'o-'
else:
    sec = 'apic_36'
    amp = '3.9'
    symbol = '^-'
# sec = 'soma_0'
# amp = '1.7'
dist = dists[0]
freqs = [str(i) for i in range(1,12)]
# ts = ['20', '10', '10', '6', '6', '6', '6', '6', '6', '6', '6', '6']
ts = [15,
    8,
    6,
    6,
    6,
    6,
    6,
    6,
    6,
    6,
    6,
    6]
for freq, t in zip(freqs,ts):
    if ver == 'soma':
        filename = 'HayCellMig_%s_amp_%s_offset_0.0_f0_%s_f1_%s_s_1.0_t_%s.json' % (sec, amp, freq, freq, t)
    else:
        filename = 'HayCellMig_%s_amp_%s_offset_0.0_f0_%s_f1_%s_s_1.0_t_%s.json' % (sec, amp, freq, freq, t)
    # with open('Data/ramp_data/' + filename) as fileObj:
    with open('ramp_data/' + filename) as fileObj:
        data = json.load(fileObj)
    fd['section'].append(sec)
    fd['dist'].append(dist)
    fd['amp'].append(float(amp))
    fd['f0'].append(float(freq))
    fd['f1'].append(float(freq))
    if len(data['lags']) > 1:
        fd['lags'].append(data['lags'][1:])
        fd['dlag'].append(np.subtract(data['lags'][1:], data['lags'][1]))
        fd['freqs'].append(data['freq'][1:])
        fd['angles'].append(data['angles'][1:])
        fd['stim_cycle'].append([i+1 for i in range(len(data['lags'])-1)])
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
    x = tempdf[tempdf['f1'] == float(f)][tempdf['blockIh'] == 'False']['stim_cycle'].values[0][:15]
    y = tempdf[tempdf['f1'] == float(f)][tempdf['blockIh'] == 'False']['angles'].values[0][:15]
    y = [radians(val)*-1 for val in y]
    if args.arrangement == 'original':
        if f == '8':
            axs[1][0].plot(x, y, symbol, color='black', label=f+' Hz')
        else:
            axs[1][0].plot(x, y, symbol, color=c, label=f+' Hz')
    else:
        if f == '8':
            axs[2].plot(x, y, symbol, color='black', label=f+' Hz')
        else:
            axs[2].plot(x, y, symbol, color=c, label=f+' Hz')
if args.arrangement == 'original':
    # axs[1][0].set_title('Frequency Dependence', fontsize=18)
    axs[1][0].plot([0,25],[0,0], 'k:')
    leg = axs[1][0].legend(title='Stimulus Frequency', loc='lower right')
    # axs[0][0].set_ylabel(r'Stimulus Phase of Spike (deg)', fontsize=18)
    axs[1][0].set_xlim(0, 25)
    axs[1][0].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)
else:
    # axs[1][0].set_title('Frequency Dependence', fontsize=18)
    axs[2].plot([0,25],[0,0], 'k:')
    leg = axs[2].legend(title='Stimulus Frequency', loc='lower right')
    # axs[0][0].set_ylabel(r'Stimulus Phase of Spike (deg)', fontsize=18)
    axs[2].set_xlim(0, 15)
    axs[2].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)
    

##################################################3
# amplitude dependent data
ad =  {'section' : [], 'amp' : [], 'angles' : [], 'f0' : [], 'f1' : [], 'lags' : [], 'freqs' : [], 'dist' : [], 
    'dlag' : [], 'stim_cycle' : [], 'blockIh' : []}
# for freq, famps in zip(freqs, allfamps):
freq = '8'
if ver=='soma':
    amps = ['1.6', '1.7', '1.8', '1.9', '2.0', '2.1',
            '2.2', '2.3', '2.4', '2.5']
else:
    ampsf = [2.9,
            3.1,
            3.3,
            3.5,
            3.7,
            3.9,
            4.1,
            4.3,
            4.5,
            4.7,
            4.9]
    amps = [str(a) for a in ampsf]
for amp in amps:
    if ver == 'soma':
        filename = 'HayCellMig_%s_amp_%s_offset_0.0_f0_%s_f1_%s_s_1.0_t_6.json' % (sec, amp, freq, freq)
    else:
        filename = 'HayCellMig_%s_amp_%s_offset_0.0_f0_%s_f1_%s_s_1.0_t_6.json' % (sec, amp, freq, freq)
    with open('ramp_data/' + filename) as fileObj:
    # with open('ramp_data/' + filename) as fileObj:
        data = json.load(fileObj)
    ad['section'].append(sec)
    ad['dist'].append(dist)
    ad['amp'].append(float(amp))
    ad['f0'].append(float(freq))
    ad['f1'].append(float(freq))
    # ad['slope'].append(float(s))
    if len(data['lags']) > 1:
        ad['lags'].append(data['lags'][1:])
        ad['dlag'].append(np.subtract(data['lags'][1:], data['lags'][1]))
        ad['freqs'].append(data['freq'][1:])
        ad['angles'].append(data['angles'][1:])
        ad['stim_cycle'].append([i+1 for i in range(len(data['lags'])-1)])
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
if args.arrangement == 'original':
    f = freq 
    tempdf = adf[adf['section'] == sec]
    normF = [(float(s) - float(amps[0])) / (float(amps[-1])-float(amps[0])) for s in amps]
    cols = plt.cm.plasma(normF)
    for s, c in zip(amps, cols):
        x = tempdf[tempdf['amp'] == float(s)][tempdf['f1'] == float(f)]['stim_cycle'].values[0][:15]
        y = tempdf[tempdf['amp'] == float(s)][tempdf['f1'] == float(f)]['angles'].values[0][:15]
        y = [radians(val)*-1 for val in y]
        sl = str(round(float(s) / 6.0,2))
        if s == '3.9':
            axs[1][1].plot(x, y, '^-', color='black', label=sl+' nA/s')
        elif s == '1.9':
            axs[1][1].plot(x, y, '^-', color='black', label=sl+' nA/s')
        else:
            axs[1][1].plot(x, y, '^-', color=c, label=sl+' nA/s')
    axs[1][1].plot([-1,25],[0,0], 'k:')
    # axs[1][1].set_title('Amplitude Dependence', fontsize=18)
    leg = axs[1][1].legend(title='Stimulus Slope', loc='lower right')
    axs[1][1].set_xlim(0, 15)
    axs[1][1].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)

#################################################################
# location dependence 
filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6.json'
# filename = 'HayCellMig_soma_0_amp_1.7_offset_0.0_f0_8_f1_8_s_0.5_t_6.json'
with open('Data/ramp_data/' + filename) as fileObj:
# with open('ramp_data/' + filename) as fileObj:
    peri = json.load(fileObj)
filename = 'HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6.json'
# filename = 'HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_0.5_t_6.json'
# with open('Data/ramp_data/' + filename) as fileObj:
with open('Data/ramp_data/' + filename) as fileObj:
# with open('ramp_data/' + filename) as fileObj:
    apical = json.load(fileObj)

## plotting 
if args.arrangement == 'original':
    if loc_ver == 'derivative':
        axs[0][1].plot([i+1 for i in range(1,15)], np.diff([radians(val)*-1 for val in peri['angles'][:15]]), 'o-', color='k', label='Soma')
        axs[0][1].plot([i+1 for i in range(1,15)], np.diff([radians(val)*-1 for val in apical['angles'][:15]]), '^-', color='k', label='Dendrite')
        axs[0][1].plot([1, 25], [0, 0], 'k:')
        # axs[0][1].set_title('Location Dependence', fontsize=18)
        leg = axs[0][1].legend(title='Stimulus Location', loc='lower right')
        axs[0][1].set_xlim(0, 15)
        axs[0][1].set_ylabel(r'$\frac{d\Phi_n^+}{dn}$ (rad)', fontsize=18)
    elif loc_ver == 'normalize':
        ax2 = axs[0][1].twinx()
        p = [radians(val)*-1 for val in peri['angles'][:15] if not np.isnan(val)]
        a = [radians(val)*-1 for val in apical['angles'][:15] if not np.isnan(val)]
        axs[0][1].plot([i+1 for i in range(1,16)], [radians(val)*-1 for val in peri['angles'][:15]], 'o-', color='k', label='Soma')
        ax2.plot([i+1 for i in range(1,16)], [radians(val)*-1 for val in apical['angles'][:15]], '^-', color='k', label='Dendrite')
        axs[0][1].plot([1, 25], [0, 0], 'k:')
        # axs[0][1].set_title('Location Dependence', fontsize=18)
        # leg = axs[0][1].legend(title='Stimulus Location', loc='lower right')
        axs[0][1].set_xlim(4, 15)
        # ax2.set_ylim(-0.4, 0.5)
        # axs[0][1].set_ylim(0.3, 1.2)
        axs[0][1].set_ylim(0.3,0.9)
        ax2.set_ylim(-0.1, 0.5)
        axs[0][1].set_ylabel(r'$\Phi_n^+$ (rad) (Soma Stim.)', fontsize=18)
        ax2.set_ylabel(r'$\Phi_n^+$ (rad) (Dendrite Stim.)', fontsize=18)       
    else:
        axs[0][1].plot([i for i in range(1,16)], [radians(val)*-1 for val in peri['angles'][:15]], 'o-', color='k', label='Soma')
        axs[0][1].plot([i for i in range(1,16)], [radians(val)*-1 for val in apical['angles'][:15]], '^-', color='k', label='Dendrite')
        axs[0][1].plot([1, 25], [0, 0], 'k:')
        # axs[0][1].set_title('Location Dependence', fontsize=18)
        leg = axs[0][1].legend(title='Stimulus Location', loc='lower right')
        axs[0][1].set_xlim(0, 15)
        axs[0][1].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)
else:
    if loc_ver == 'derivative':
        axs[1].plot([i+1 for i in range(1,15)], np.diff([radians(val)*-1 for val in peri['angles'][:15]]), 'o-', color='k', label='Soma')
        axs[1].plot([i+1 for i in range(1,15)], np.diff([radians(val)*-1 for val in apical['angles'][:15]]), '^-', color='k', label='Dendrite')
        axs[1].plot([1, 25], [0, 0], 'k:')
        leg = axs[1].legend(title='Stimulus Location', loc='lower right')
        axs[1].set_xlim(0, 15)
        axs[1].set_ylabel(r'$\frac{d\Phi_n^+}{dn}$ (rad)', fontsize=18)
    else:
        axs[1].plot([i for i in range(1,16)], [radians(val)*-1 for val in peri['angles'][:15]], 'o-', color='k', label='Soma')
        axs[1].plot([i for i in range(1,16)], [radians(val)*-1 for val in apical['angles'][:15]], '^-', color='k', label='Dendrite')
        axs[1].plot([1, 25], [0, 0], 'k:')
        leg = axs[1].legend(title='Stimulus Location', loc='lower right')
        axs[1].set_xlim(0, 15)
        axs[1].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)

#################################################################
# ih dependence 
# filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockIh.json'
# filename = 'HayCellMig_soma_0_amp_1.7_offset_0.0_f0_8_f1_8_s_0.5_t_6_blockIh.json'
if ver=='soma':
    filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockIh.json'
    with open('Data/ramp_data/' + filename) as fileObj:
    # with open('ramp_data/' + filename) as fileObj:
        block = json.load(fileObj)
    filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockSKE.json'
    with open('ramp_data/' + filename) as fileObj:
    # with open('ramp_data/' + filename) as fileObj:
        blockSK = json.load(fileObj)
    filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockIhSKE.json'
    with open('ramp_data/' + filename) as fileObj:
    # with open('ramp_data/' + filename) as fileObj:
        blockIhSKE = json.load(fileObj)
else:
    filename = 'HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockIh.json'
    with open('Data/ramp_data/' + filename) as fileObj:
    # with open('ramp_data/' + filename) as fileObj:
        block = json.load(fileObj)
    filename = 'HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockSKE.json'
    with open('ramp_data/' + filename) as fileObj:
    # with open('ramp_data/' + filename) as fileObj:
        blockSK = json.load(fileObj)

## plotting 
if args.arrangement == 'original':
    if ver == 'soma':
        axs[0][0].plot([i for i in range(1,16)], [radians(val)*-1 for val in peri['angles'][:15]], symbol, color='k', label='Control')
    else:
        axs[0][0].plot([i for i in range(1,16)], [radians(val)*-1 for val in apical['angles'][:15]], symbol, color='k', label='Control')
    axs[0][0].plot([i for i in range(1,16)], [radians(val)*-1 for val in block['angles'][:15]], symbol, color='gray', label=r'Block I$_h$')
    axs[0][0].plot([i for i in range(1,16)], [radians(val)*-1 for val in blockSK['angles'][:15]], symbol, color='green', label=r'Block I$_{AHP}$')
    # axs[0][0].plot([i for i in range(1,16)], [radians(val)*-1 for val in blockIhSKE['angles'][:15]], symbol, color='purple', label=r'Block I$_h$ and I$_{AHP}$')
    axs[0][0].plot([-1, 25], [0, 0], 'k:')
    # axs[0][0].set_title(r'I$_h$/I$_{AHP}$ Dependence', fontsize=18)
    leg = axs[0][0].legend(title='Condition', loc='lower right')
    axs[0][0].set_xlim(0, 15)
    axs[0][0].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)
else:
    if ver == 'soma':
        axs[0].plot([i for i in range(1,16)], [radians(val)*-1 for val in peri['angles'][:15]], symbol, color='k', label='Control')
    else:
        axs[0].plot([i for i in range(1,16)], [radians(val)*-1 for val in apical['angles'][:15]], symbol, color='k', label='Control')
    axs[0].plot([i for i in range(1,16)], [radians(val)*-1 for val in block['angles'][:15]], symbol, color='gray', label=r'Block I$_h$')
    axs[0].plot([i for i in range(1,16)], [radians(val)*-1 for val in blockSK['angles'][:15]], symbol, color='green', label=r'Block I$_{AHP}$')
    axs[0].plot([-1, 25], [0, 0], 'k:')
    # axs[0][0].set_title(r'I$_h$/I$_{AHP}$ Dependence', fontsize=18)
    leg = axs[0].legend(title='Condition', loc='lower right')
    axs[0].set_xlim(0, 15)
    axs[0].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)

# fig.text(0.425, 0.94, 'Phase Precession', fontsize=20)
# fig.text(0.43, 0.04, 'Stimulus Cycle (n)', fontsize=18)
# fig.text(0.05, 0.4, r'$\Phi_n^+$ (rad)', fontsize=18, rotation=90)


## traces 
if ver == 'soma':
    filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6.npy'
    traces = np.load('ramp_traces/' + filename, allow_pickle=True)
    traces = traces[()]
    fig2 = plt.figure()
    ax = fig2.add_subplot(1,1,1)
    ax.plot(traces['time'], traces['soma_v'], label=r'V$_{soma}$')
    ax.plot(traces['time'], traces['i'] * 10 - 70, 'k', label='Stimulus')
    ipks, _ = find_peaks(traces['i'])
    for pk in ipks:
        ax.plot([traces['time'][pk], traces['time'][pk]], [-100, 30], 'k:')
else:
    filename = 'HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6.npy'
    traces = np.load('ramp_traces/' + filename, allow_pickle=True)
    traces = traces[()]
    fig2 = plt.figure()
    ax = fig2.add_subplot(1,1,1)
    ax.plot(traces['time'], traces['soma_v'], label=r'V$_{soma}$')
    ax.plot(traces['time'], traces['i'] * 1.5 - 60, 'k', label='Stimulus')
    ipks, _ = find_peaks(traces['i'])
    for pk in ipks:
        ax.plot([traces['time'][pk], traces['time'][pk]], [-100, 30], 'k:')

ax.set_xticks([])
ax.set_yticks([])
ax.legend(fontsize=14, loc='upper left')

plt.ion()
plt.show()