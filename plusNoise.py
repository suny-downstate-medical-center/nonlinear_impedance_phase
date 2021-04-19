from getCells import M1Cell   
s = M1Cell()  
seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
from chirpUtils import getNoise, getChirpLog, getChirp 
from neuron import h 
stim = h.IClamp(seg)
from pylab import fft, convolve
import numpy as np 
# import argparse
import os
import multiprocessing
import json 
from scipy.io import savemat 

def runTrial(input_data):
    print('Do i get called?')
    stim_type, noise_amp, noise_std, t0, bnsz, outpath = input_data[0], input_data[1], input_data[2], input_data[3], input_data[4], input_data[5]
    soma_v = h.Vector().record(seg._ref_v) 
    time = h.Vector().record(h._ref_t)
    Fs = 1000
    delay = 5
    sampr = 40e3
    bwinsz = bnsz
    Inoise, tnoise = getNoise(0.0, noise_std, int(t0+2*delay), noise_amp, Fs, 0) 
    if stim_type == 'chirp':
        I, t = getChirp(0.5, 500, t0, 0.02, Fs, delay)
    elif stim_type == 'log':
        I, t = getChirpLog(0.5, 500, t0, 0.02, Fs, delay)
    elif stim_type == 'noise':
        I, t = getNoise(0.0, 0.5, t0, 0.02, Fs, delay)

    ## place current clamp on soma
    i = h.Vector().record(h.IClamp[0]._ref_i)
    stim.amp = 0
    stim.dur = (t0+delay*2) * Fs + 1
    I.play(stim._ref_amp, t)

    stimNoise = h.IClamp(seg)
    stimNoise.amp = 0
    stimNoise.dur = (t0+delay*2) * Fs + 1
    Inoise.play(stimNoise._ref_amp, tnoise)

    h.celsius = 34
    h.tstop = (t0+delay*2) * Fs + 1
    print('Running: amp-' +str(noise_amp) + ' std-' + str(noise_std) + ' t0-' + str(t0) + ' bin size-' + str(bwinsz))
    h.run()
    v_trim = [v for v, T in zip(soma_v, time) if int((delay+2)*1000) < T < int(delay*t0*1000)] 
    i_trim = [x for x, T in zip(i,time) if int((delay+2)*1000) < T < int(delay*t0*1000)] 
    time_trim = [T for v, T in zip(soma_v, time) if int((delay+2)*1000) < T < int(delay*t0*1000)] 
    current = i_trim
    v = v_trim 
    
    #current = current[int(delay*sampr - 0.5*sampr+1):-int(delay*sampr- 0.5*sampr)] 
    current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
    current = current - np.mean(current) 
    #v = v[int(delay*sampr - 0.5*sampr)+1:-int(delay*sampr - 0.5*sampr)] 
    v = np.hstack((np.repeat(v[0],int(delay*sampr)), v, np.repeat(v[-1], int(delay*sampr)))) 
    v = v - np.mean(v) 

    ## input and transfer impedance
    f_current = (fft(current)/len(current))[0:int(len(current)/2)]
    f_cis = (fft(v)/len(v))[0:int(len(v)/2)]
    z = f_cis / f_current

    ## impedance measures
    Freq       = np.linspace(0.0, sampr/2.0, len(z))
    zAmp       = abs(z)
    zPhase     = np.arctan2(np.imag(z),np.real(z))
    zRes       = np.real(z)
    zReact     = np.imag(z)
    
    ## impedance measures
    Freq       = np.linspace(0.0, sampr/2.0, len(z))
    zAmp       = abs(z)
    zPhase     = np.arctan2(np.imag(z),np.real(z))
    zRes       = np.real(z)
    zReact     = np.imag(z)

    ## smoothing
    fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
    zAmp = convolve(zAmp,fblur,'same')
    zPhase = convolve(zPhase, fblur, 'same')

    ## trim
    mask = (Freq >= 0.5) & (Freq <= 500)
    Freq, zAmp, zPhase, zRes, zReact, z = Freq[mask], zAmp[mask], zPhase[mask], zRes[mask], zReact[mask], z[mask]

    ## resonance
    zResAmp    = np.max(zAmp)
    zResFreq   = Freq[np.argmax(zAmp)]
    Qfactor    = zResAmp / zAmp[0]
    fVar       = np.std(zAmp) / np.mean(zAmp)

    peak_to_peak = np.max(v) - np.min(v)

    freqsIn = np.argwhere(zPhase > 0)
    if len(freqsIn) > 0:
        ZinSynchFreq = Freq[freqsIn[-1]]
        ZinPhaseL = np.trapz([float(zPhase[ind]) for ind in freqsIn], 
            [float(Freq[ind]) for ind in freqsIn])
    else:
        ZinSynchFreq = 0 
        ZinPhaseL = 0

    pre_v = [soma_v for soma_v, T in zip(soma_v.as_numpy(), time.as_numpy()) if (delay-1)*1000 <= T <= delay*1000]
    noise_peak_to_peak = np.max(pre_v) - np.min(pre_v)

    out = {'Freq': Freq, 
            'zRes' : zRes,
            'zReact' : zReact,
            'zAmp' : zAmp,
            'zPhase' : zPhase,
            'synchFreq' : ZinSynchFreq,
            'phaseL' : ZinPhaseL,
            'peak_to_peak' : peak_to_peak,
            'Qfactor' : Qfactor,
            'fVar' : fVar,
            'zResAmp' : zResAmp,
            'zResFreq' : zResFreq,
            'noise_peak_to_peak' : noise_peak_to_peak}

    savemat(outpath + stim_type + '_amp-' + str(noise_amp) + '-std-' + str(noise_std) + '-bnsz-' + str(bnsz) + '.mat', out)

noise_stds = [0.1, 0.3, 0.5, 0.7, 0.9]
noise_amps = np.linspace(0.005, 0.2, num=10)
binsizes = [1, 5, 10, 15, 20, 25, 30, 35, 40]

try:
    os.makedirs('data/plusNoiseData/')
except:
    pass

data = []
for noise_amp in noise_amps:
    for binsz in binsizes:
        for noise_std in noise_stds:
            data.append(['log',noise_amp, noise_std, 60, binsz, 'data/plusNoiseData/'])
# data.append(['log', 0.005, 0.3, 10, 10, 'data/plusNoiseData/'])

# runTrial(data[0])
poolSize = 50
p = multiprocessing.Pool(poolSize)
p.map(runTrial, data)