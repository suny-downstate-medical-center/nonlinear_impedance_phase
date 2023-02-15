# load cell model 
from getCells import HayCellMig
cell, _ = HayCellMig()
soma_seg = cell.soma[0](0.5)
seg = soma_seg 

# needed packages 
from neuron import h 
from chirpUtils import getChirp, fromtodistance
from pylab import fft
import numpy as np 
from scipy.signal import find_peaks, hilbert
import json 
import os
from matplotlib import pyplot as plt 

# basic parameters 
stim = h.IClamp(seg)
dist = fromtodistance(seg, soma_seg)
amp = 0.4 
t0 = 13
delay = 3
Fs = 1000
sampr = 40e3 
f0 = 0.5
f1 = 13
offset = 0.0

# setup stimulus 
soma_v = h.Vector().record(soma_seg._ref_v) 
seg_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t)
I, t = getChirp(f0, f1, t0, amp, Fs, delay, offset=offset)
i = h.Vector().record(h.IClamp[0]._ref_i)
stim.amp = 0
stim.dur = (t0+delay*2) * Fs + 1
I.play(stim._ref_amp, t)

## run simulation
h.celsius = 34
h.tstop = (t0+delay*2) * Fs + 1
print('running chirp: f0-' + str(f0) + ' f1-' + str(f1))
h.run()

# analysis 
v_trim = [v for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
i_trim = [x for x, T in zip(i,time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
time_trim = [T for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
current = i_trim
v = v_trim 
current = np.hstack((np.repeat(offset,int(delay*sampr)),current, np.repeat(offset, int(delay*sampr)))) 
current = current - np.mean(current) 
v = v - np.mean(v) 
v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 
f = np.hstack((np.repeat(0,int(delay*sampr)), np.linspace(f0,f1,len(v_trim)),np.repeat(0,int(delay*sampr))))

iphase = np.angle(hilbert(current))
allspks, _ = find_peaks(v_trim, 0)
pks, _ = find_peaks(v)
trghs, _ = find_peaks(v*-1)
ipks, _ = find_peaks(current)
itrghs, _ = find_peaks(current*-1)
trghs = [tr for tr in trghs if tr > pks[0]]
f_minus = None
phi_minus = None
asym = -np.min(v)-np.max(v)
peak_to_peak = np.max(v) - np.min(v)
v_init = v_trim[0]
z_plus = None 
z_minus = None

if len(allspks):
    phi_plus = []
    f_plus = []
    for peakt, finish, nextt in zip(ipks[:-1], itrghs[:-1], ipks[1:]):
        start = peakt - (finish-peakt) 
        spks, _ = find_peaks(v[start:finish], 0)
        if len(spks):
            phi_plus.append(iphase[peakt]-iphase[spks[0]+start])
        else:
            phi_plus.append(np.nan)
        f_plus.append(f[peakt])
    trghs, _ = find_peaks(v*-1, 0)
    trghs = [tr for tr in trghs if tr > pks[0]]
    phi_minus = []
    for trgh, itrgh in zip(trghs, itrghs):
        if iphase[trgh] < 0 and iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - (iphase[trgh] + 2*np.pi))
        elif iphase[trgh] < 0:
            phi_minus.append(iphase[itrgh]-(iphase[trgh] + 2*np.pi))
        elif iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - iphase[trgh])
        else:
            phi_minus.append(iphase[itrgh]-iphase[trgh])            
    f_minus = [f[trgh] for trgh in itrghs]
else:
    phi_plus = [iphase[ipk]-iphase[pk] for pk, ipk in zip(pks, ipks)]
    z_plus = [np.abs(v[pk])/amp for pk in pks]
    z_minus = [np.abs(v[trgh])/amp for trgh in trghs]
    f_plus = [f[pk] for pk in pks]
    phi_minus = [] 
    for trgh, itrgh in zip(trghs, itrghs):
        if iphase[trgh] < 0 and iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - (iphase[trgh] + 2*np.pi))
        elif iphase[trgh] < 0:
            phi_minus.append(iphase[itrgh]-(iphase[trgh] + 2*np.pi))
        elif iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - iphase[trgh])
        else:
            phi_minus.append(iphase[itrgh]-iphase[trgh])            
    f_minus = [f[trgh] for trgh in itrghs]

# plotting 
plt.figure()
plt.plot(time, soma_v)
plt.title('Membrane Potential', fontsize=18)
plt.xlabel('Time (ms)', fontsize=16)
plt.ylabel(r'V$_{memb}$ (mV)', fontsize=16)

plt.figure()
plt.plot(f_minus, phi_minus, 'k-', label='Hyperpolarization')
plt.plot(f_plus, phi_plus, 'k--', label='Depolarization')
plt.xlabel('Frequency (Hz)', fontsize=16)
plt.ylabel(r'$\Phi^\pm\!(f)$', fontsize=16)
plt.title('Frequency-Dependent Phase Shifts', fontsize=18)
plt.xlim(0,12)
plt.legend()

plt.ion()
plt.show()
