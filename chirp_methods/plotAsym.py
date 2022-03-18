from getCells import M1Cell   
s = M1Cell()  
seg = s.net.cells[0].secs['soma']['hObj'](0.5)   
from neuron import h, gui    
import numpy as np  
from scipy.io import loadmat 
import os 
from matplotlib import pyplot as plt 
plt.ion()
from chirpUtils import getChirp, applyChirpZin  

soma_v = h.Vector().record(seg._ref_v)      
time = h.Vector().record(h._ref_t)  
f0, f1, t0, Fs, delay = 0.5, 20, 20, 1000, 5 
amp = 0.015
print('Running ' + str(amp)) 
I, t = getChirp(f0, f1, t0, amp, Fs, delay) 
base = applyChirpZin(I, t, seg, t0, delay, Fs, f1)

base_v_trim = [v for v, T in zip(soma_v, time) if 4900 < T < 25100]                  
base_v_trim = np.subtract(base_v_trim, base_v_trim[0])
t_trim = [T for T in time if 4900 < T < 25100] 

amp = 0.212
print('Running ' + str(amp)) 
I, t = getChirp(f0, f1, t0, amp, Fs, delay) 
out = applyChirpZin(I, t, seg, t0, delay, Fs, f1)   

v_trim = [v for v, T in zip(soma_v, time) if 4900 < T < 25100]                               
v_trim = np.subtract(v_trim, v_trim[0])

plt.figure()
plt.subplot(2,3,1)
plt.plot([(T-5100)/1000 for T in t_trim], base_v_trim, label='0.01 mV', color='black')
plt.title('0.02 mV Assymetry', fontsize=16)
plt.xlabel('Time (s)', fontsize=14)
plt.ylabel(r'$\Delta$ V$_{memb}$ (mV)', fontsize=14)
plt.ylim(-1, 1)
plt.xlim(-0.1,20.1)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.subplot(2,3,4)
plt.plot([(T-5100)/1000 for T in t_trim], v_trim, label='1.20 mV', color='gray')
plt.title('1.22 mV Assymetry', fontsize=16)    
plt.xlabel('Time (s)', fontsize=14)
plt.ylabel(r'$\Delta$ V$_{memb}$ (mV)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(-13,13)
plt.xlim(-0.1, 20.1)

files = os.listdir('data/chirpAsymV2/')

asym = []
zAmpErrs = []
zPhaseErrs = []
for filename in files:
    data = loadmat('data/chirpAsymV2/' + filename)
    asym.append(data['asymmetry'][0][0])
    zAmpErrs.append(data['zAmpErr'][0][0])
    zPhaseErrs.append(data['zPhaseErr'][0][0])

asym_sort = [a for a in sorted(asym)]
zAmpErr_sorted = [z for a, z in sorted(zip(asym, zAmpErrs))]
zPhaseErr_sorted = [z for a, z in sorted(zip(asym, zPhaseErrs))]

data = loadmat('data/chirpAsymV2/chirp_amp-0.014999999999999996-f1-20-t0-20.mat')
plt.subplot(2,3,2)
plt.plot(data['Freq_cut'][0], data['zAmp_cut'][0], color='k')
plt.title('Input Impedance Amplitude', fontsize=16)
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.ylabel(r'|Z$_{in}$| (M$\Omega$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,3,3)
plt.plot(data['Freq_cut'][0], data['zPhase_cut'][0], color='k')
plt.title('Input Impedance Phase', fontsize=16)
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.ylabel(r'$\Phi_{in}$ (radians)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

data = loadmat('data/chirpAsymV2/chirp_amp-0.21230141534998076-f1-20-t0-20.mat')
plt.subplot(2,3,2)
plt.plot(data['Freq_cut'][0], data['zAmp_cut'][0], color='gray')
plt.subplot(2,3,3)
plt.plot(data['Freq_cut'][0], data['zPhase_cut'][0], color='gray')

plt.subplot(2,3,5)
plt.semilogx(asym_sort, zAmpErr_sorted, color='k', linestyle='-', linewidth=1.5)
plt.scatter(asym_sort, zAmpErr_sorted, color='k', linewidth=1.5)
plt.title(r'|Z$_{in}$| Error', fontsize=16)
plt.xlabel('Response Asymmetry (mV)', fontsize=14)
plt.ylabel('Mean Squared Error (M$\Omega^2$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,3,6)
plt.semilogx(asym_sort, zPhaseErr_sorted, color='k', linestyle='-', linewidth=1.5)
plt.scatter(asym_sort, zPhaseErr_sorted, color='k', linewidth=1.5)
plt.title(r'$\Phi_{in}$ Error', fontsize=16)
plt.xlabel('Response Asymmetry (mV)', fontsize=14)
plt.ylabel('Mean Squared Error (radians$^2$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# v0.00 - plotting output from asymmetric chirp sims 