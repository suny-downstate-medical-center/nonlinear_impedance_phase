from matplotlib import pyplot as plt
plt.ion()
import json 

with open('asym_data/durabernal__apic_0_amp_0.2_offset_0.0_f0_0_f1_13.json', 'rb') as fileObj:
    base = json.load(fileObj)

with open('asym_data/dura_bernal_apic_0_amp_0.2_offset_0.0_f0_0_f1_13_blockKA.json') as fileObj:
    blockKA = json.load(fileObj)

with open('asym_data/dura_bernal_apic_18_amp_0.2_offset_0.0_f0_0_f1_13.json', 'rb') as fileObj:
    apic = json.load(fileObj)

with open('asym_data/dura_bernal_apic_18_amp_0.2_offset_0.0_f0_0_f1_13_blockKA.json', 'rb') as fileObj:
    apicBlockKA = json.load(fileObj)

fig, axs = plt.subplots(1,2)

axs[0].plot(base['f_minus'], base['phi_minus'], 'b-')
axs[0].plot(base['f_plus'], base['phi_plus'], 'b--')
axs[0].plot(blockKA['f_minus'], blockKA['phi_minus'], 'r-', label=r'Block I$_A$')
axs[0].plot(blockKA['f_plus'], blockKA['phi_plus'], 'r--')
axs[0].plot([0,15],[0,0], 'k:')
axs[1].plot(apic['f_minus'], apic['phi_minus'], 'b-')
axs[1].plot(apic['f_plus'], apic['phi_plus'], 'b--')
axs[1].plot(apicBlockKA['f_minus'], apicBlockKA['phi_minus'], 'r-', label=r'Block I$_A$')
axs[1].plot([0,15],[0,0], 'k:')
axs[1].plot(apicBlockKA['f_plus'], apicBlockKA['phi_plus'], 'r--')
axs[0].legend()
axs[0].set_xlabel('Frequency (Hz)', fontsize=16)
axs[1].set_xlabel('Frequency (Hz)', fontsize=16)
axs[0].set_ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=16)
axs[0].set_xlim(0.5, 10)
axs[1].set_xlim(0.5, 10)
axs[0].set_title('Soma', fontsize=18)
axs[1].set_title('Apical Dendrite', fontsize=18)