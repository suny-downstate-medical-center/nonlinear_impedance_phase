from matplotlib import pyplot as plt 
import json 
import numpy as np 
from scipy.signal import find_peaks 

# with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
#     chirp_data = json.load(fileObj)
# chirp_traces = np.load('asym_traces/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.npy', allow_pickle=True)
# chirp_traces = np.load('asym_traces/HayCellMig_apic_12_amp_0.3_offset_0.0_f0_0_f1_12.npy', allow_pickle=True)
chirp_traces = np.load('asym_traces/HayCellMig_apic_0_amp_0.4_offset_-0.55_f0_0_f1_12.npy', allow_pickle=True)
chirp_traces = chirp_traces[()]
base_v = chirp_traces['soma_v'][0]
soma_v = [v*2 - base_v for v, t in zip(chirp_traces['soma_v'], chirp_traces['time']) if 2500 < t < 15500]
time = [(t/1000)-3  for t in chirp_traces['time'] if 2500 < t < 15500]
fac = np.abs(np.max(chirp_traces['i']))
stim = [i/fac*5-128 for i, t in zip(chirp_traces['i'], chirp_traces['time']) if 2500 < t < 15500]

pks, _ = find_peaks(soma_v)
trghs, _ = find_peaks(np.array(soma_v)*-1)
ipks, _ = find_peaks(stim)
itrghs, _ = find_peaks(np.array(stim)*-1)

fig, ax = plt.subplots(1,1)
ax.plot(time, soma_v, color='b', label=r'V$_{memb}$')
ax.plot(time, stim, color='k', label='Stimulus')
ax.plot([-1,13], [soma_v[0], soma_v[0]], 'b--')
ax.plot([-1,13], [stim[0], stim[0]], 'k--')
ax.plot([-1,13], [-121,-121], color='gray')
for pk in ipks:
    ax.plot(time[pk], stim[pk], 'k*')
    ax.plot(time[pk], -121, 'k*')
for trgh in itrghs:
    ax.plot(time[trgh], stim[trgh], 'ko')
    ax.plot(time[trgh] , -121, 'ko')
for pk in pks:
    ax.plot(time[pk], soma_v[pk], 'b^')
    ax.plot(time[pk], -121, 'b^')
for trgh in trghs:
    ax.plot(time[trgh], soma_v[trgh], 'bs')
    ax.plot(time[trgh], -121, 'bs')

ax.set_yticks([])
ax.tick_params(axis='x', which='major', labelsize=11)
ax.set_xlabel('Time (s)', fontsize=16)

# ax.text(2.414,-119, r'$\frac{\pi}{2}$', color='gray', fontsize=22)
# ax.text(2.583,-119, r'$\frac{\pi}{2}$', color='gray', fontsize=22)
# ax.text(2.744,-119, r'$\frac{\pi}{2}$', color='gray', fontsize=22)


# ax.set_xlim([9.0,9.16])

# plt.text(9.055, -88.55, r'$\Phi^+$', fontsize=22)
# plt.text(9.108, -94, r'$\Phi^-$', fontsize=22)
plt.legend()

plt.ion()
plt.show()