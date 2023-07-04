import pandas as pd 
import json 
import numpy as np 
from matplotlib import pyplot as plt
from math import radians 
from scipy.signal import find_peaks 

#####################################################################
#                       retreat
#####################################################################
ver = 'soma'
ad =  {'section' : [], 'amp' : [], 'angles' : [], 'f0' : [], 'f1' : [], 'lags' : [], 'freqs' : [], 'dist' : [], 
    'dlag' : [], 'stim_cycle' : [], 'blockIh' : []}
# for freq, famps in zip(freqs, allfamps):
freq = '8'
sec = 'apic_0' 
amps = ['0.9', '1.0', '1.1', '1.2', '1.3', '1.4',
        '1.5', '1.6']
dists = [23.1, 261.4, 504.2]
dist = dists[0]
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
amp_fig, amps_axs = plt.subplots(1,2, sharex=True, sharey=True)
f = freq 
tempdf = adf[adf['section'] == sec]
normF = [(float(a) - float(amps[0])) / (float(amps[-1])-float(amps[0])) for a in amps]
cols = plt.cm.plasma(normF)
for amp, c in zip(amps, cols):
    x = tempdf[tempdf['amp'] == float(amp)][tempdf['f1'] == float(f)]['stim_cycle'].values[0][:14]
    y = tempdf[tempdf['amp'] == float(amp)][tempdf['f1'] == float(f)]['angles'].values[0][:14]
    y = [radians(val)*-1 for val in y]
    if amp == '1.0':
        amps_axs[0].plot(x, y, 'o-', color='black', label=amp+' nA')
    else:
        amps_axs[0].plot(x, y, 'o-', color=c, label=amp+' nA')
amps_axs[0].plot([0,15],[0,0], 'k:')
amps_axs[0].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18) #set_title('Amplitude Dependence', fontsize=18)
leg = amps_axs[0].legend(title='Stimulus Amplitude', loc='lower right')

#####################################################################
#                       advance
#####################################################################


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
        amps_axs[1].plot(x, y, '^-', color='black', label=sl+' nA/s')
    elif s == '1.9':
        amps_axs[1].plot(x, y, '^-', color='black', label=sl+' nA/s')
    else:
        amps_axs[1].plot(x, y, '^-', color=c, label=sl+' nA/s')
amps_axs[1].plot([-1,25],[0,0], 'k:')
# amps_axs[1].set_title('Amplitude Dependence', fontsize=18)
leg = amps_axs[1].legend(title='Stimulus Slope', loc='lower right')
amps_axs[1].set_xlim(0, 15)
# amps_axs[1].set_ylabel(r'$\Phi_n^+$ (rad)', fontsize=18)
amps_axs[1].set_xlabel('Stimulus cycle (n)', fontsize=18)
amps_axs[0].set_xlabel('Stimulus cycle (n)', fontsize=18)
amps_axs[1].set_title('Phase Retreat', fontsize=18)
amps_axs[0].set_title('Phase Advance', fontsize=18)
plt.ion()
plt.show()