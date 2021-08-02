from getCells import M1Cell   
s = M1Cell()  
soma_seg = s.net.cells[0].secs['soma']['hObj'](0.5)   
seg = s.net.cells[0].secs['apic_22']['hObj'](0.5)   
from neuron import h, gui    
import numpy as np  
#from chirpUtils import getNoise, getChirp, getLogCh 

h.load_file('iclamp_circuit.ses')
h.tstop = 27000
h.LinearCircuit[0].R1 = 1 # 1 mOhm
h.LinearCircuit[0].R2 = 4 # 4 Momh
h.LinearCircuit[0].Cpip = 0.0001 # 0.1 pF
h.LinearCircuit[0].Rseal = 10000 # 110 Gohm
# h.LinearCircuit[0].Racc = 2.0
# h.LinearCircuit[0].J = 0.2 
j = h.Vector([2 for i in range(int(1/h.dt * h.tstop))])
t = h.Vector([i/(1/h.dt) for i in range(int(1/h.dt * h.tstop))])
j.play(h.LinearCircuit[0]._ref_J, t)

dummy = h.Section(name='dummy')
fz = h.Fzap(dummy(0.5))
fz.f0 = 0.5 
fz.f1 = 20
fz.amp = 0.1
fz.delay = 6000 
fz.dur = 20000
fz._ref_x = h.LinearCircuit[0]._ref_Isrc

time = h.Vector().record(h._ref_t)
soma_v = h.Vector().record(soma_seg._ref_v)
seg_v = h.Vector().record(seg._ref_v)
ivec = h.Vector().record(h.LinearCircuit[0]._ref_Isrc)
v_obs = h.Vector().record(h.LinearCircuit[0]._ref_Vobs)
v_memb = h.Vector().record(h.LinearCircuit[0]._ref_Vm)

h.run()

from matplotlib import pyplot as plt 
plt.ion()
plt.subplot(311)
plt.plot(time, ivec)
plt.xlim(5000,27000)
plt.ylabel('Current Stimulus (nA)', fontsize=16)
plt.subplot(312)
plt.plot(time, v_obs, label='Observed')
plt.plot(time, v_memb, label='Vmemb')
plt.xlim(5000, 27000)
plt.ylim(-77.5, -67.5)
plt.ylabel(r'V$_{apic}$ (mV)', fontsize=16)
plt.legend(fontsize=14)
plt.subplot(313)
plt.plot(time, soma_v)
plt.xlim(5000, 27000)
plt.ylim(-77.5, -70)
plt.xlabel('Time (ms)', fontsize=16)
plt.ylabel(r'V$_{soma}$ (mV)', fontsize=16)