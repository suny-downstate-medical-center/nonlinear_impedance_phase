from matplotlib import pyplot as plt
plt.ion()
import json 

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    hay = json.load(fileObj)

with open('asym_data/durabernal__apic_0_amp_0.3_offset_0.0_f0_0_f1_13.json', 'rb') as fileObj:
    dura = json.load(fileObj)

with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    mm = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_cell2.json', 'rb') as fileObj:
    cell2 = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_cell3.json', 'rb') as fileObj:
    cell3 = json.load(fileObj)

fig, axs = plt.subplots(2,1, sharex=True, sharey=True)
axs[0].plot(hay['f_minus'], hay['phi_minus'], 'b-', label='Model 1 (L5b)')
axs[0].plot(hay['f_plus'], hay['phi_plus'], 'b--')
axs[0].plot(dura['f_minus'], dura['phi_minus'], 'k-', label='Model 2 (L5b)')
axs[0].plot(dura['f_plus'], dura['phi_plus'], 'k--')
axs[0].plot(mm['f_minus'], mm['phi_minus'], 'm-')
axs[0].plot(mm['f_plus'], mm['phi_plus'], 'm--', label='Model 3 (CA1)')
axs[0].plot([0,12], [0,0], 'k:')
axs[0].legend()
axs[0].set_xlim(0.5,11)
axs[0].set_ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=16)

axs[1].plot(hay['f_minus'], hay['phi_minus'], 'b-', label='Morphology 1')
axs[1].plot(hay['f_plus'], hay['phi_plus'], 'b--')
axs[1].plot(cell2['f_minus'], cell2['phi_minus'], 'r-', label='Morphology 2')
axs[1].plot(cell2['f_plus'], cell2['phi_plus'], 'r--')
axs[1].plot(cell3['f_minus'], cell3['phi_minus'], 'c-', label='Morphology 2')
axs[1].plot(cell3['f_plus'], cell3['phi_plus'], 'c--')
axs[1].plot([0,12], [0,0], 'k:')
axs[1].legend()
axs[1].set_xlabel('Frequency (Hz)', fontsize=16)
axs[1].set_ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=16)