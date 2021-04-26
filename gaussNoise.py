from getCells import M1Cell   
s = M1Cell()  
seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
from chirpUtils import getChirpLog, getNoise
from neuron import h 
stim = h.IClamp(seg)
from pylab import fft, convolve
import numpy as np 
# import argparse
import os

amp = 0.02 
t0 = 20
delay = 5
Fs = 1000
sampr = 40e3 
f0 = 0.5
f1 = 20
soma_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t)
# I, t = getChirpLog(f0, f1, t0, amp, Fs, delay)
I, t = getNoise(0.0, 0.5, t0, 0.01, Fs, delay)
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
#current = current[int(delay*sampr - 0.5*sampr+1):-int(delay*sampr- 0.5*sampr)] 
current = current - np.mean(current) 
current = np.hstack((np.repeat(0,int(delay*sampr)),current, np.repeat(0, int(delay*sampr)))) 
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
bwinsz = 1 #5
fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
zamp = convolve(zamp,fblur,'same')
phase = convolve(phase, fblur, 'same')
Freq, zamp, phase, zRes, zReact, z = Freq[mask], zamp[mask], phase[mask], zRes[mask], zReact[mask], z[mask]
freqsIn = np.argwhere(phase > 0)
if len(freqsIn) > 0:
    ZinSynchFreq = Freq[freqsIn[-1]]
    ZinPhaseL = np.trapz([float(phase[ind]) for ind in freqsIn], 
        [float(Freq[ind]) for ind in freqsIn])
else:
    ZinSynchFreq = 0 
    ZinPhaseL = 0

out = {'Freq' : Freq,
    'ZinRes' : zRes,
    'ZinReact' : zReact,
    'ZinAmp' : zamp,
    'ZinPhase' : phase,
    'ZinSynchFreq' : ZinSynchFreq,
    'ZinPhaseL' : ZinPhaseL,
    'ZinResAmp' : zResAmp,
    'ZinResFreq' : zResFreq,
    'QfactorIn' : Qfactor,
    'fVarIn' : fVar,
    'z' : z}