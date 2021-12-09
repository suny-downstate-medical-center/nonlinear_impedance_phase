import sys

if sys.argv[-2] == 'M1Cell':
    from getCells import M1Cell   
    s = M1Cell()  
    soma_seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
    seg = s.net.cells[0].secs[sys.argv[-1]]['hObj'](0.5)
elif sys.argv[-2] == 'HayCellMig':
    from getCells import HayCellMig
    cell, _ = HayCellMig()
    soma_seg = cell.soma(0.5)
    sec_name = sys.argv[-1].split('_')[0]
    sec_num = sys.argv[-1].split('_')[1]
    execstr = 'seg = cell.' + sec_name + '[' + sec_num + '](0.5)'
    exec(execstr)

from chirpUtils import getChirp, fromtodistance
from neuron import h 
stim = h.IClamp(seg)
from pylab import fft
import numpy as np 

dist = fromtodistance(seg, soma_seg)
amp = 0.02 
t0 = 50 #20
delay = 5
Fs = 1000
sampr = 40e3 
f0 = 0.5
f1 = 50 #20
soma_v = h.Vector().record(soma_seg._ref_v) 
seg_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t)
I, t = getChirp(f0, f1, t0, amp, Fs, delay)
i = h.Vector().record(h.IClamp[0]._ref_i)
stim.amp = 0
stim.dur = (t0+delay*2) * Fs + 1
I.play(stim._ref_amp, t)
## run simulation
h.celsius = 34
h.tstop = (t0+delay*2) * Fs + 1
h.run()
v_trim = [v for v, T in zip(seg_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
i_trim = [x for x, T in zip(i,time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
time_trim = [T for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
current = i_trim
v = v_trim 
#current = current[int(delay*sampr - 0.5*sampr+1):-int(delay*sampr- 0.5*sampr)] 
current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
current = current - np.mean(current) 
#v = v[int(delay*sampr - 0.5*sampr)+1:-int(delay*sampr - 0.5*sampr)] 
v = v - np.mean(v) 
v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 
f_current = (fft(current)/len(current))[0:int(len(current)/2)] 
f_cis = (fft(v)/len(v))[0:int(len(v)/2)] 
z = f_cis / f_current 
phase = np.arctan2(np.imag(z), np.real(z))
Freq       = np.linspace(0.0, sampr/2.0, len(z))
zRes       = np.real(z)
zReact     = np.imag(z)
zamp = abs(z)
mask = (Freq >= 0.5) & (Freq <= f1)
zResAmp    = np.max(zamp)
zResFreq   = Freq[np.argmax(zamp)]
Qfactor    = zResAmp / zamp[0]
fVar       = np.std(zamp) / np.mean(zamp)
peak_to_peak = np.max(v) - np.min(v)
## smoothing
# bwinsz = 1
# fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
# zamp = convolve(zamp,fblur,'same')
# phase = convolve(phase, fblur, 'same')
Freq, zamp, phase, zRes, zReact, z = Freq[mask], zamp[mask], phase[mask], zRes[mask], zReact[mask], z[mask]
freqsIn = np.argwhere(phase > 0)
if len(freqsIn) > 0:
    ZinSynchFreq = Freq[freqsIn[-1]]
    ZinPhaseL = np.trapz([float(phase[ind]) for ind in freqsIn], 
        [float(Freq[ind]) for ind in freqsIn])
else:
    ZinSynchFreq = 0 
    ZinPhaseL = 0

out = {'Freq' : list(Freq),
    'ZinRes' : list(zRes),
    'ZinReact' : list(zReact),
    'ZinAmp' : list(zamp),
    'ZinPhase' : list(phase),
    'ZinSynchFreq' : float(ZinSynchFreq),
    'ZinPhaseL' : float(ZinPhaseL),
    'ZinResAmp' : float(zResAmp),
    'ZinResFreq' : float(zResFreq),
    'QfactorIn' : float(Qfactor),
    'fVarIn' : float(fVar)}#,
    # 'zin' : list(z)}

v_trim = [v for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
v = v_trim 
v = v - np.mean(v) 
v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 
f_cis = (fft(v)/len(v))[0:int(len(v)/2)] 
z = f_cis / f_current 
phase = np.arctan2(np.imag(z), np.real(z))
Freq       = np.linspace(0.0, sampr/2.0, len(z))
zRes       = np.real(z)
zReact     = np.imag(z)
zamp = abs(z)
mask = (Freq >= 0.5) & (Freq <= f1)
zResAmp    = np.max(zamp)
zResFreq   = Freq[np.argmax(zamp)]
Qfactor    = zResAmp / zamp[0]
fVar       = np.std(zamp) / np.mean(zamp)
peak_to_peak = np.max(v) - np.min(v)
## smoothing
# bwinsz = 1
# fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
# zamp = convolve(zamp,fblur,'same')
# phase = convolve(phase, fblur, 'same')
Freq, zamp, phase, zRes, zReact, z = Freq[mask], zamp[mask], phase[mask], zRes[mask], zReact[mask], z[mask]
freqsIn = np.argwhere(phase > 0)
if len(freqsIn) > 0:
    ZinSynchFreq = Freq[freqsIn[-1]]
    ZinPhaseL = np.trapz([float(phase[ind]) for ind in freqsIn], 
        [float(Freq[ind]) for ind in freqsIn])
else:
    ZinSynchFreq = 0 
    ZinPhaseL = 0

out['ZcRes'] = list(zRes)
out['ZcReact'] = list(zReact)
out['ZcAmp'] = list(zamp)
out['ZcPhase'] = list(phase)
out['ZcSynchFreq'] = float(ZinSynchFreq)
out['ZcPhaseL'] = float(ZinPhaseL)
out['ZcResAmp'] = float(zResAmp)
out['ZcResFreq'] = float(zResFreq)
out['QfactorC'] = float(Qfactor)
out['fVarC'] = float(fVar)
out['dist'] = dist
# out['zc'] = list(z)

import json 
filename = 'imped_data/' + sys.argv[-2] + '_' + sys.argv[-1] + '.json'
with open(filename, 'w') as fileObj:
    json.dump(out, fileObj)