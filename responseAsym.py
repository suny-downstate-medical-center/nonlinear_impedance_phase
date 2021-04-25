from getCells import M1Cell   
s = M1Cell()  
seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
from chirpUtils import getNoise, getChirpLog, getChirp 
from neuron import h 
stim = h.IClamp(seg)
from pylab import fft, convolve
import numpy as np 
import os
import multiprocessing
import json 
from scipy.io import savemat 

def runTrial(input_data):
    stim_type, amp, t0, f1, outpath = input_data[0], input_data[1], input_data[2], input_data[3], input_data[4]

    soma_v = h.Vector().record(seg._ref_v) 
    time = h.Vector().record(h._ref_t)

    ## define stim and noise parameters and signals 
    Fs = 1000
    delay = 5
    sampr = 40e3
    if stim_type == 'chirp':
        I, t = getChirp(0.5, f1, t0, amp, Fs, delay)
    elif stim_type == 'log':
        I, t = getChirpLog(0.5, f1, t0, amp, Fs, delay)
    elif stim_type == 'noise':
        I, t = getNoise(0.0, 0.5, t0, amp, Fs, delay)

    ## load validation data 
    with open('data/noise_freq_validation_amp01.json', 'rb') as fileObj: 
        data = json.load(fileObj) 
    freqs_valid = [] 
    zAmp_valid = [] 
    zPhase_valid = [] 
    for f in data.keys(): 
        freqs_valid.append(float(f)) 
        zAmp_valid.append(data[f]['zAmp']) 
        zPhase_valid.append(data[f]['zPhase'])
    freqs_sort = [f for f in sorted(freqs_valid)] 
    zAmp_sort = [z for f, z in sorted(zip(freqs_valid, zAmp_valid))] 
    zPhase_sort = [z for f, z in sorted(zip(freqs_valid, zPhase_valid))]    

    ## place current clamps on soma
    i = h.Vector().record(h.IClamp[0]._ref_i)
    stim.amp = 0
    stim.dur = (t0+delay*2) * Fs + 1
    I.play(stim._ref_amp, t)

    ## run sim 
    h.celsius = 34
    h.tstop = (t0+delay*2) * Fs + 1
    print('Running: amp-' +str(noise_amp) + ' std-' + str(noise_std) + ' t0-' + str(t0))
    h.run()

    ## crop signals for during stimulation
    v_trim = [v for v, T in zip(soma_v, time) if int(delay)*1000 < T < int(delay+t0)*1000]
    i_trim = [x for x, T in zip(i,time) if int(delay)*1000 < T < int(delay+t0)*1000] 
    time_trim = [T for v, T in zip(soma_v, time) if int(delay)*1000 < T < int(delay+t0)*1000] 
    current = i_trim
    v = v_trim 
    
    ## zero padding and de-meaning
    if stim_type == 'noise':
        current = current - np.mean(current) 
        current = np.hstack((np.repeat(0,int(delay*sampr)),current, np.repeat(0, int(delay*sampr)))) 
        v = v - np.mean(v)
        v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr))))  
    elif stim_type == 'log':
        current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
        current = current - np.mean(current) 
        v = v - np.mean(v) 
        v = np.hstack((np.repeat(v[0],int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 
    elif stim_type == 'chirp':
        current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
        current = current - np.mean(current) 
        v = v - np.mean(v) 
        v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 

    ## input and transfer impedance
    f_current = (fft(current)/len(current))[0:int(len(current)/2)]
    f_cis = (fft(v)/len(v))[0:int(len(v)/2)]
    z = f_cis / f_current

    ## impedance measures
    Freq        = np.linspace(0.0, sampr/2.0, len(z))
    zamp_orig   = abs(z)
    zPhase_orig = np.arctan2(np.imag(z),np.real(z))
    zRes        = np.real(z)
    zReact      = np.imag(z)

    ### trim
    mask = (Freq >= 0.5) & (Freq <= f1)
    Freq_cut, zAmp_cut, zPhase_cut, zRes_cut, zReact_cut, z_cut = Freq[mask], zamp_orig[mask], zPhase_orig[mask], zRes[mask], zReact[mask], z[mask]

    ### resonance
    zResAmp    = np.max(zAmp_cut)
    zResFreq   = Freq[np.argmax(zAmp_cut)]
    Qfactor    = zResAmp / zAmp_cut[0]
    fVar       = np.std(zAmp_cut) / np.mean(zAmp_cut)

    ### asym peak to peak of response
    peak_to_peak = np.max(v) - np.min(v)
    asym = -np.min(v)-np.max(v)

    ### synchrony and total inductive phase
    freqsIn = np.argwhere(zPhase_cut > 0)
    if len(freqsIn) > 0:
        ZinSynchFreq = Freq_cut[freqsIn[-1]]
        ZinPhaseL = np.trapz([float(zPhase_cut[ind]) for ind in freqsIn], 
            [float(Freq_cut[ind]) for ind in freqsIn])
    else:
        ZinSynchFreq = 0 
        ZinPhaseL = 0

    ### resample validation data 
    validChirpAmp = []
    validChirpPhs = []
    validChirpFrq = []
    for f in Freq_cut:
        ind = np.argmin(np.square(np.subtract(freqs_sort, f)))
        validChirpAmp.append(zAmp_sort[ind])
        validChirpPhs.append(zPhase_sort[ind])
        validChirpFrq.append(freqs_sort[ind])
    
    ### compute errors
    zAmpErr = mean_squared_error(zAmp_cut, validChirpAmp)
    zPhaseErr = mean_squared_error(zPhase_cut, validChirpPhs)

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
            'Freq_cut': Freq_cut, 
            'zRes_cut' : zRes_cut,
            'zReact_cut' : zReact_cut,
            'zAmp_cut' : zAmp_cut,
            'zPhase_cut' : zPhase_cut,
            'zAmpErr' : zAmpErr,
            'zPhaseErr' : zPhaseErr,
            'asymmetry' : asym}

    savemat(outpath + stim_type + '_amp-' + str(amp) + '-f0-' + str(f0) + '-t0-' + str(t0) + '.mat', out)

amps = np.logspace(np.log10(0.015), np.log10(0.31), num=9, endpoint=True)
t0 = 20 
f1 = 20 

try:
    os.makedirs('data/chirpAsymV2/')
except:
    pass

data = [] 
for amp in amps:
    data.append(['chirp', amp, t0, f1, 'data/chirpAsymV2/'])
data = tuple(data)

poolSize = 9
p = multiprocessing.Pool(poolSize)
p.map(runTrial, data)

# v0.00 - replaces assymetricNoise.py, configured for 20s chirp with amps as high as 0.31