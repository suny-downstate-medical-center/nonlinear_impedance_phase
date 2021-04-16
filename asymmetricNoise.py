from getCells import M1Cell  
s = M1Cell() 
seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
from neuron import h, gui   
import numpy as np 
from chirpUtils import getNoise, applyNoise 
from sklearn.metrics import mean_squared_error

amps = np.logspace(np.log10(0.015), np.log10(0.31), num=9, endpoint=True)

t0, Fs, delay = 20, 1000, 5

phaseErr = []
ampErr = []
asym = []

soma_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t) 

amp = 0.01 
print('Running ' + str(amp))
I, t = getNoise(0.0, 0.75, t0, 0.01, Fs, delay)   
base = applyNoise(I, t, seg, t0, delay, Fs, f1, binsize=25)

# compute asymmetry in voltage trace 
v_trim = [v for v, T in zip(soma_v, time) if 4900 < T < 20100]
v_trim = np.subtract(v_trim, v_trim[0])
base_asym = np.abs(np.max(v_trim)-np.min(v_trim))

for amp in amps: 
    # run chirp 
    print('Running ' + str(amp))
    I, t = getChirp(f0, f1, t0, amp, Fs, delay)
    out = applyNoise(I, t, seg, t0, delay, Fs, f1, binsize=25)
    
    # compute asymmetry in voltage trace 
    v_trim = [v for v, T in zip(soma_v, time) if 4900 < T < 20100]
    v_trim = np.subtract(v_trim, v_trim[0])
    asym.append(-np.min(v_trim)-np.max(v_trim))

    # compute MSE for Z amp and phase 
    ampErr.append(mean_squared_error(base['ZinAmp'], out['ZinAmp']))
    phaseErr.append(mean_squared_error(base['ZinPhase'], out['ZinPhase']))

out = {'phaseErr' : phaseErr, 
       'ampErr'   : ampErr,
       'asym'     : asym, 
       'base_asym': base_asym,
       'amps'     : amps}

from scipy.io import savemat 
savemat('noise_asym_sensitivity.mat', out)

# v0.01 - sensitivity analysis of asymmetric voltage responses in computing impedance