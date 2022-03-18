from getCells import M1Cell   
s = M1Cell()  
seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
from chirpUtils import getChirpLog, getChirp, getNoise
from neuron import h 
stim = h.IClamp(seg)
from pylab import fft, convolve
import numpy as np 
# import argparse
import os
from sklearn.metrics import mean_squared_error
import json 
from matplotlib import pyplot as plt 
plt.ion()

zampsBefore = []
zphasesBefore = []
zampsAfter = []
zphasesAfter = []
bnsizes = [1, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50]

stim_type = 'noise'

amp = 0.02 
t0 = 20 #20
delay = 5
Fs = 1000
sampr = 40e3 
f0 = 0.5
f1 = 500 #20
soma_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t)
I, t = getChirpLog(f0, f1, t0, amp, Fs, delay)
i = h.Vector().record(h.IClamp[0]._ref_i)
stim.amp = 0
stim.dur = (t0+delay*2) * Fs + 1
I.play(stim._ref_amp, t)
## run simulation
h.celsius = 34
h.tstop = (t0+delay*2) * Fs + 1
h.run()
v_trim = [v for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
i_trim = [x for x, T in zip(i,time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
time_trim = [T for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
current = i_trim
v = v_trim 
if stim_type == 'log':
    current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
    current = current - np.mean(current)
    v = v - np.mean(v) 
    v = np.hstack((np.repeat(v[0],int(delay*sampr)), v, np.repeat(0, int(delay*sampr))))
elif stim_type == 'noise':
    current = current - np.mean(current) 
    current = np.hstack((np.repeat(0,int(delay*sampr)),current, np.repeat(0, int(delay*sampr)))) 
    v = v - np.mean(v)
    v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr))))   
elif stim_type == 'linear':
    current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
    current = current - np.mean(current) 
    v = v - np.mean(v) 
    v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 
    
f_current = (fft(current)/len(current))[0:int(len(current)/2)] 
f_cis = (fft(v)/len(v))[0:int(len(v)/2)] 
z = f_cis / f_current 
phase_orig = np.arctan2(np.imag(z), np.real(z))
Freq       = np.linspace(0.0, sampr/2.0, len(z))
zRes       = np.real(z)
zReact     = np.imag(z)
zamp_orig = abs(z)
mask = (Freq >= 0.5) & (Freq <= f1)

## trim after smoothing 
for bwinsz in bnsizes:
    fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
    zamp = convolve(zamp_orig,fblur,'same')
    phase = convolve(phase_orig, fblur, 'same')
    zamp, phase = zamp[mask], phase[mask]
    zampsAfter.append(zamp)
    zphasesAfter.append(phase)

phase_orig, zamp_orig = phase_orig[mask], zamp_orig[mask]
for bwinsz in bnsizes:
    fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
    zamp = convolve(zamp_orig,fblur,'same')
    phase = convolve(phase_orig, fblur, 'same')
    zampsBefore.append(zamp)
    zphasesBefore.append(phase)
    # print(len(zamps))

with open('data/noise_freq_validation_amp01.json', 'rb') as fileObj: 
    data = json.load(fileObj)
freqs_temp = [] 
zAmp_temp = [] 
zPhase_temp = [] 
for f in data.keys(): 
    freqs_temp.append(float(f)) 
    zAmp_temp.append(data[f]['zAmp']) 
    zPhase_temp.append(data[f]['zPhase'])
freqs = [f for f in sorted(freqs_temp)]
zAmp = [z for f, z in sorted(zip(freqs_temp, zAmp_temp))] 
zPhase = [z for f, z in sorted(zip(freqs_temp, zPhase_temp))] 

valid_freqs = []
valid_zAmp = []
valid_zPhase = []
for f in Freq[mask]:
    ind = np.argmin(np.square(np.subtract(freqs, f)))
    valid_freqs.append(freqs[ind])
    valid_zAmp.append(zAmp[ind])
    valid_zPhase.append(zPhase[ind])

ampErrsBefore = []
phaseErrsBefore = []
ampErrsAfter = []
phaseErrsAfter = []
for amp, phs in zip(zampsBefore, zphasesBefore):
    ampErrsBefore.append(mean_squared_error(amp, valid_zAmp))
    phaseErrsBefore.append(mean_squared_error(phs, valid_zPhase))
for amp, phs in zip(zampsAfter, zphasesAfter):
    ampErrsAfter.append(mean_squared_error(amp, valid_zAmp))
    phaseErrsAfter.append(mean_squared_error(phs, valid_zPhase))

plt.figure()
plt.subplot(1,2,1)
plt.plot(bnsizes, ampErrsBefore, label='Filter After Removing Z(f < 0.5 Hz)')
plt.plot(bnsizes, ampErrsAfter, label='Filter Before Removing Z(f < 0.5 Hz)')
plt.xlabel('Filter Window Size', fontsize=14)
plt.ylabel('Mean Squared Error (M$\Omega^2$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0,12)
plt.title('|Z$_{in}$| Error', fontsize=16)
plt.subplot(1,2,2)
plt.plot(bnsizes, phaseErrsBefore, label='Filter After Removing Z(f < 0.5 Hz)')
plt.plot(bnsizes, phaseErrsAfter, label='Filter Before Removing Z(f < 0.5 Hz)')
plt.xlabel('Filter Window Size', fontsize=14)
plt.ylabel('Mean Squread Error (radians$^2$)', fontsize=14)
plt.title('$\Phi_{in}$ Error', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
