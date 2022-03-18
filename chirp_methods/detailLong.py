from getCells import M1Cell 
s = M1Cell()
from neuron import h, gui 
import numpy as np 
from matplotlib import pyplot as plt 
from pylab import fft 
from chirpUtils import applyChirp, getChirp
import sys
from scipy.io import savemat
zPhase = []
zAmp = []
amp = 0.025
t0, Fs, delay = 5, 1000, 1
#seg = s.net.cells[0].secs['apic_13']['hObj'](0.5) 
seg = s.net.cells[0].secs['soma']['hObj'](0.5) 
soma_seg = s.net.cells[0].secs['soma']['hObj'](0.5) 
#freqs = [i/2 for i in range(1,500)]
freqs = [i for i in range(int(sys.argv[-2]),int(sys.argv[-1]))]
soma_v = h.Vector().record(soma_seg._ref_v) 
dend_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t)
sampr = 40e3
for f in freqs: 
    print(f)
    f0, f1 = f, f 
    I, t = getChirp(f0,f1,t0,amp,Fs,delay)
    #i = h.Vector().record(h.IClamp[0]._ref_i)
    out = applyChirp(I, t, seg, soma_seg, t0, delay, Fs, f1)
    v_trim = [v for v, T in zip(soma_v, time) if 3000 < T < 5000] 
    i_trim = [i for i, T in zip(I,t) if 3000 < T < 5000] 
    t_trim = [T for i, T in zip(I,t) if 3000 < T < 5000] 
    time_trim = [T for v, T in zip(soma_v, time) if 3000 < T < 5000] 
    current = i_trim
    v = v_trim 
    current = current[int(delay*sampr - 0.5*sampr+1):-int(delay*sampr- 0.5*sampr)] 
    current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
    current = current - np.mean(current) 
    v = v[int(delay*sampr - 0.5*sampr)+1:-int(delay*sampr - 0.5*sampr)] 
    v = np.hstack((np.repeat(v[0],int(delay*sampr)), v, np.repeat(v[-1], int(delay*sampr)))) 
    v = v - np.mean(v) 
    f_current = (fft(current)/len(current))[0:int(len(current)/2)] 
    f_cis = (fft(v)/len(v))[0:int(len(v)/2)] 
    z = f_cis / f_current 
    phase = np.arctan2(np.imag(z), np.real(z))
    Freq       = np.linspace(0.0, sampr/2.0, len(z))
    zamp = abs(z)
    ind = np.argmin(np.square(Freq-f))
    zPhase.append(phase[ind])
    zAmp.append(zamp[ind])
out = {'freqs' : freqs, 'zAmp' : zAmp, 'zPhase' : zPhase}
savemat('longImpedSoma/detail_imped_' + sys.argv[-2] + '-' + sys.argv[-1]+'.mat', out)
 
