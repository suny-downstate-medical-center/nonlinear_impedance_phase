from netpyne import sim
from neuron import h
import numpy as np
import matplotlib.pyplot as plt
from math import radians 
import json 

fig, axs = plt.subplots(1,4)
sec = h.Section(name = 'sec')
taul = []
mech = 'hd'
sec.insert(mech)
h.setdata_hd(sec(0.5))
volt = [v for v in np.arange(-100,100,1)] #left window

for v in volt:
    h.rate_hd(v)
    taul.append(sec(0.5).hd.taul)

plt.ion()
axs[0].plot(volt, taul, 'k-')
axs[0].set_xlabel('Membrane Potential (mV)', fontsize=16)
axs[0].set_ylabel(r'$\tau_{h}$ (ms)', fontsize=16)

factors = [i/10 for i in range(5,16)]
normFactors = [(f-min(factors))/max(factors) for f in factors]
cols = plt.cm.jet(normFactors)
for f, c in zip(factors, cols):
    filename = 'HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_tauFactor_%s.json' % (str(round(f,1)))
    with open('../../asym_data/'+filename, 'rb') as fileObj:
        data = json.load(fileObj)
    axs[1].plot(data['f_minus'], data['phi_minus'], '-', color=c, label=str(f))
    axs[1].plot(data['f_plus'], data['phi_plus'], '--', color=c)
    filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_tauFactor_%s.json' % (str(round(f,1)))
    with open('../../supra_data/'+filename, 'rb') as fileObj:
        data = json.load(fileObj)
    axs[2].plot([i for i in range(len(data['lags']))], [radians(val)*-1 for val in data['angles']], 'o-', color=c)
    filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_s_1.0_t_6_tauFactor_%s.json' % (str(round(f,1)))
    with open('../../ramp_data/'+filename, 'rb') as fileObj:
        data = json.load(fileObj)
    axs[3].plot([i for i in range(len(data['lags']))], [radians(val)*-1 for val in data['angles']], 'o-', color=c, label=str(f))

axs[1].set_xlim(0.5,10)
axs[1].set_xlabel('Frequency (Hz)', fontsize=16)
axs[1].set_ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=16)
axs[1].plot([0,15], [0,0], 'k:')
axs[2].set_ylabel(r'$\Phi^{+}$ (radians)', fontsize=16)
axs[2].set_xlabel('Stimulus cycle (n)', fontsize=16)
axs[2].plot([0,15], [0,0], 'k:')
axs[2].set_xlim(-0.1,15)
axs[3].set_ylabel(r'$\Phi^{+}$ (radians)', fontsize=16)
axs[3].set_xlabel('Stimulus cycle (n)', fontsize=16)
axs[3].legend(title=r'$\tau_h$ Scale Factor')
axs[3].plot([0,15], [0,0], 'k:')
axs[3].set_xlim(-0.1,15)
plt.ion()
plt.show()

