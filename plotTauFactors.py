from matplotlib import pyplot as plt
plt.ion()
import json 
from math import radians

factors = [i/10 for i in range(5,16)]
normFactors = [(f-min(factors))/max(factors) for f in factors]
cols = plt.cm.jet(normFactors)
for f, c in zip(factors, cols):
    filename = 'HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_tauFactor_%s.json' % (str(round(f,1)))
    with open('asym_data/'+filename, 'rb') as fileObj:
        data = json.load(fileObj)
    plt.subplot(131)
    plt.plot(data['f_minus'], data['phi_minus'], '-', color=c, label=str(f))
    plt.plot(data['f_plus'], data['phi_plus'], '--', color=c)
    filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_tauFactor_%s.json' % (str(round(f,1)))
    with open('supra_data/'+filename, 'rb') as fileObj:
        data = json.load(fileObj)
    plt.subplot(132)
    plt.plot([i for i in range(len(data['lags']))], [radians(val)*-1 for val in data['angles']], 'o-', color=c)
    filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_s_1.0_t_6_tauFactor_%s.json' % (str(round(f,1)))
    with open('ramp_data/'+filename, 'rb') as fileObj:
        data = json.load(fileObj)
    plt.subplot(133)
    plt.plot([i for i in range(len(data['lags']))], [radians(val)*-1 for val in data['angles']], 'o-', color=c)

plt.subplot(131) 
plt.plot([0,15], [0,0], 'k:')
plt.xlim(0.5,10)
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=14)
plt.subplot(132)
plt.plot([0,15], [0,0], 'k:')
plt.ylabel(r'$\Phi^{+}$ (radians)', fontsize=14)
plt.xlabel('Stimulus cycle (n)', fontsize=14)
plt.xlim(-0.1,15)
plt.subplot(133)
plt.plot([0,15], [0,0], 'k:')
plt.ylabel(r'$\Phi^{+}$ (radians)', fontsize=14)
plt.xlabel('Stimulus cycle (n)', fontsize=14)
plt.xlim(-0.1, 15)
plt.legend()
