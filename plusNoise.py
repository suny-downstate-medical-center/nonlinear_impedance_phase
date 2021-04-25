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
from sklearn.metrics import mean_squared_error

def runTrial(input_data):
    stim_type, noise_amp, noise_std, t0, f1, binsizes, outpath = input_data[0], input_data[1], input_data[2], input_data[3], input_data[4], input_data[5], input_data[6]
    soma_v = h.Vector().record(seg._ref_v) 
    time = h.Vector().record(h._ref_t)

    ## define stim and noise parameters and signals 
    Fs = 1000
    delay = 5
    sampr = 40e3
    Inoise, tnoise = getNoise(0.0, noise_std, int(t0+2*delay), noise_amp, Fs, 0) 
    if stim_type == 'chirp':
        I, t = getChirp(0.5, f1, t0, 0.02, Fs, delay)
    elif stim_type == 'log':
        I, t = getChirpLog(0.5, f1, t0, 0.02, Fs, delay)
    elif stim_type == 'noise':
        I, t = getNoise(0.0, 0.5, t0, 0.02, Fs, delay)

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

    stimNoise = h.IClamp(seg)
    stimNoise.amp = 0
    stimNoise.dur = (t0+delay*2) * Fs + 1
    Inoise.play(stimNoise._ref_amp, tnoise)

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

    ## smoothing
    for bwinsz in binsizes:
        fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
        zAmp_smooth = convolve(zamp_orig,fblur,'same')
        zPhase_smooth = convolve(zPhase_orig, fblur, 'same')

        ### trim
        mask = (Freq >= 0.5) & (Freq <= f1)
        Freq_cut, zAmp_cut, zPhase_cut, zRes_cut, zReact_cut, z_cut = Freq[mask], zAmp_smooth[mask], zPhase_smooth[mask], zRes[mask], zReact[mask], z[mask]

        ### resonance
        zResAmp    = np.max(zAmp_cut)
        zResFreq   = Freq[np.argmax(zAmp_cut)]
        Qfactor    = zResAmp / zAmp_cut[0]
        fVar       = np.std(zAmp_cut) / np.mean(zAmp_cut)

        ### peak to peak of stim
        peak_to_peak = np.max(v) - np.min(v)

        ### synchrony and total inductive phase
        freqsIn = np.argwhere(zPhase_cut > 0)
        if len(freqsIn) > 0:
            ZinSynchFreq = Freq_cut[freqsIn[-1]]
            ZinPhaseL = np.trapz([float(zPhase_cut[ind]) for ind in freqsIn], 
                [float(Freq_cut[ind]) for ind in freqsIn])
        else:
            ZinSynchFreq = 0 
            ZinPhaseL = 0

        ### noise properties 
        pre_v = [soma_v for soma_v, T in zip(soma_v.as_numpy(), time.as_numpy()) if (delay-1)*1000 <= T <= delay*1000]
        noise_peak_to_peak = np.max(pre_v) - np.min(pre_v)
        noise_v_std = np.std(pre_v)

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
                'zAmp' : zamp_orig,
                'zPhase' : zPhase_orig,
                'synchFreq' : ZinSynchFreq,
                'phaseL' : ZinPhaseL,
                'peak_to_peak' : peak_to_peak,
                'Qfactor' : Qfactor,
                'fVar' : fVar,
                'zResAmp' : zResAmp,
                'zResFreq' : zResFreq,
                'noise_peak_to_peak' : noise_peak_to_peak,
                'noise_v_std' : noise_v_std,
                'noise_std' : noise_std,
                'noise_amp' : noise_amp, 
                'Freq_cut': Freq_cut, 
                'zRes_cut' : zRes_cut,
                'zReact_cut' : zReact_cut,
                'zAmp_cut' : zAmp_cut,
                'zPhase_cut' : zPhase_cut,
                'zAmpErr' : zAmpErr,
                'zPhaseErr' : zPhaseErr}

        savemat(outpath + stim_type + '_amp-' + str(noise_amp) + '-std-' + str(noise_std) + '-bnsz-' + str(bwinsz) + '.mat', out)

noise_stds = [0.1, 0.3, 0.5, 0.7, 0.9]
noise_amps = np.linspace(0.005, 0.2, num=10)
binsizes = [1, 5, 10, 15, 20, 25, 30, 35, 40]

try:
    os.makedirs('data/chirpNoiseData/')
except:
    pass

data = []
for noise_amp in noise_amps:
    for noise_std in noise_stds:
        data.append(['chirp',noise_amp, noise_std, 20, 20, binsizes, 'data/chirpNoiseData/'])
# data.append(['log', 0.005, 0.3, 10, 10, 'data/plusNoiseData/'])

# runTrial(data[0])
poolSize = 50
p = multiprocessing.Pool(poolSize)
p.map(runTrial, data)

# v0.01 - configured for linear chirp over 0.5 - 20 Hz over 50 noise parameter combos