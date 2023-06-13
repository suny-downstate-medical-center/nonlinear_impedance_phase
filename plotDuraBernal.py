from matplotlib import pyplot as plt 
plt.ion()
from math import radians 
import json 

with open('asym_data/durabernal__apic_0_amp_0.2_offset_0.0_f0_0_f1_13.json', 'rb') as fileObj:
    sub = json.load(fileObj)

with open('supra_data/dura_bernal_apic_0_amp_0.5_offset_0.0_f0_8_f1_8.json', 'rb') as fileObj:
    retreat = json.load(fileObj)

with open('ramp_data/dura_bernal_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_4.json', 'rb') as fileObj:
    advance = json.load(fileObj)

fig, axs = plt.subplots(1,3)

axs[0].plot(sub['f_minus'], sub['phi_minus'], 'k-')
axs[0].plot(sub['f_plus'], sub['phi_plus'], 'k--')
axs[0].set_ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=16)
axs[0].set_xlabel('Frequency (Hz)', fontsize=16)
axs[0].set_title('Subthreshold', fontsize=16)
axs[0].set_xlim(0.5, 10)

axs[1].plot([i for i in range(1,16)], [radians(val)*-1 for val in retreat['angles'][:15]], 'o-', color='black')
axs[1].set_xlabel('Stimulus cycle (n)', fontsize=16)
axs[1].set_ylabel(r'$\Phi^+$ (radians)', fontsize=16)
axs[1].set_title('Phase Retreat', fontsize=16)
axs[1].set_xlim(-0.3, 10)

axs[2].plot([i for i in range(1,16)], [radians(val)*-1 for val in advance['angles'][:15]], 'o-', color='black')
axs[2].set_xlabel('Stimulus cycle (n)', fontsize=16)
axs[2].set_ylabel(r'$\Phi^+$ (radians)', fontsize=16)
axs[2].set_title('Phase Advance', fontsize=16)
axs[2].set_xlim(2.7,13)