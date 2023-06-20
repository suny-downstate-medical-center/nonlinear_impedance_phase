# load cell 
# from getCells import HayCellMig
# cell, _ = HayCellMig()
import neuron
from neuron import h 
h.loadfile('stdrun.hoc')
neuron.load_mechanisms("Ih_current") # directory with mm mod files
h.xopen("Ih_current/fig-5a.hoc")
seg = soma_seg = h.soma[0](0.5)

# needed packages 
from chirpUtils import getRampChirp, fromtodistance
import numpy as np 
from scipy.signal import find_peaks, hilbert
from math import radians 
from matplotlib import pyplot as plt

# parameters 
dist = fromtodistance(seg, soma_seg)
amp = 1.9 #0.02 
t0 = 6 #20
delay = 3
Fs = 1000
sampr = 40e3 
f0 = 8
f1 = 8
soma_v = h.Vector().record(soma_seg._ref_v) 
seg_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t)
offset = 0
slope = 1

# setup stimulus 
stim = h.IClamp(seg)
I, t = getRampChirp(f0, f1, t0, amp, Fs, delay, offset=offset, slope=slope)
i = h.Vector().record(h.IClamp[0]._ref_i)
stim.amp = 0
stim.dur = (t0+delay*2) * Fs + 1
I.play(stim._ref_amp, t)

# run simulation
h.celsius = 34
h.tstop = (t0+delay*2) * Fs + 1
print('running chirp ramp: f0-' + str(f0) + ' f1-' + str(f1))
h.run()

# analysis
v_trim = [v for v, T in zip(seg_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
time_trim = [T for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
v = v_trim 

allspks, _ = find_peaks(v_trim, 0)
if len(allspks):
    stim_pks, stim_amps = find_peaks(i.as_numpy())
    stim_troughs, trough_amps = find_peaks(i.as_numpy() * -1)
    soma_np = soma_v.as_numpy()
    seg_np = seg_v.as_numpy()
    iphase = np.angle(hilbert(i.as_numpy()), deg=True)
    time_np = time.as_numpy()
    lags = []
    freq = []
    angles = []
    for peakt, finish, nextt in zip(stim_pks[:-1], stim_troughs[:-1], stim_pks[1:]):
        start = peakt - (finish-peakt) 
        spks, _ = find_peaks(soma_np[start:finish], 0)
        if len(spks):
            lags.append(time_np[start+spks[0]]-time_np[peakt])
            angles.append(iphase[start+spks[0]])
        else:
            lags.append(np.nan)
            angles.append(np.nan)
        freq.append(1 / ((time_np[finish]-time_np[start])/1000))

y = [radians(val)*-1 for val in angles]

plt.figure()
plt.plot(y, 'ko-')
plt.xlabel('Stimulus Cycle (N)', fontsize=16)
plt.ylabel(r'$\Phi_n^+$', fontsize=16)
plt.title('Phase Advance', fontsize=18)
plt.xlim(0,10)
plt.ion()
plt.show()
