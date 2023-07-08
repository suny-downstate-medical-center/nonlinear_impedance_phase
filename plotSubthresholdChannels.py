from matplotlib import pyplot as plt
plt.ion()
import json 

fig, axs = plt.subplots(4,2,sharex=True)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_blockSKv3.json', 'rb') as fileObj:
    blockSKv3 = json.load(fileObj)

with open('asym_data/HayCellMig_apic_12_amp_0.3_offset_0.0_f0_0_f1_13_blockSKv3.json', 'rb') as fileObj:
    blockSKv3Apic = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    base = json.load(fileObj)

with open('asym_data/HayCellMig_apic_12_amp_0.3_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    apic = json.load(fileObj)

with open('asym_data/HayCellMig_apic_36_amp_0.2_offset_0.0_f0_0_f1_14.json', 'rb') as fileObj:
    distal = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_blockLVACa.json', 'rb') as fileObj:
    blockLVA = json.load(fileObj)

with open('asym_data/HayCellMig_apic_36_amp_0.2_offset_0.0_f0_0_f1_13_blockLVACa.json', 'rb') as fileObj:
    blockLVAApic = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_blockIm.json', 'rb') as fileObj:
    blockIm = json.load(fileObj)

with open('asym_data/HayCellMig_apic_36_amp_0.2_offset_0.0_f0_0_f1_13_blockIm.json', 'rb') as fileObj:
    blockImApic = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.25_offset_0.0_f0_0_f1_13_blockTASK.json', 'rb') as fileObj:
    blockTASK = json.load(fileObj)

with open('asym_data/HayCellMig_apic_12_amp_0.3_offset_0.0_f0_0_f1_13_blockTASK.json', 'rb') as fileObj:
    blockTASKApic = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.25_offset_0.0_f0_0_f1_13.json', 'rb') as fileObj:
    baseTASK = json.load(fileObj)

axs[0][0].plot(base['f_minus'], base['phi_minus'], 'b-')
axs[0][0].plot(base['f_plus'], base['phi_plus'], 'b--')
axs[0][0].plot(blockSKv3['f_minus'], blockSKv3['phi_minus'], 'r-', label=r'Block SKv3.1')
axs[0][0].plot(blockSKv3['f_plus'], blockSKv3['phi_plus'], 'r--')
axs[0][0].plot([0,15],[0,0], 'k:')
axs[0][1].plot(blockSKv3Apic['f_minus'], blockSKv3Apic['phi_minus'], 'r-', label=r'Block I$_{KA}$')
axs[0][1].plot(blockSKv3Apic['f_plus'], blockSKv3Apic['phi_plus'], 'r--')
axs[0][1].plot(apic['f_minus'], apic['phi_minus'], 'b:')
axs[0][1].plot(apic['f_plus'], apic['phi_plus'], 'b--')
axs[0][1].plot([0,15],[0,0], 'k:')
axs[0][0].set_xlim(0.5,10)
axs[0][1].set_xlim(0.5,10)
axs[0][0].legend()
axs[0][0].set_title('Soma', fontsize=18)
axs[0][1].set_title('Apical Dendrite', fontsize=18)

axs[1][0].plot(base['f_minus'], base['phi_minus'], 'b-')
axs[1][0].plot(base['f_plus'], base['phi_plus'], 'b--')
axs[1][0].plot(blockIm['f_minus'], blockIm['phi_minus'], 'r:', label=r'Block I$_{m}$')
axs[1][0].plot(blockIm['f_plus'], blockIm['phi_plus'], 'r:')
axs[1][0].plot([0,15],[0,0], 'k:')
axs[1][1].plot(blockImApic['f_minus'], blockImApic['phi_minus'], 'r-', label=r'Block I$_{m}$')
axs[1][1].plot(blockImApic['f_plus'], blockImApic['phi_plus'], 'r--')
axs[1][1].plot(distal['f_minus'], distal['phi_minus'], 'b-')
axs[1][1].plot(distal['f_plus'], distal['phi_plus'], 'b--')
axs[1][1].plot([0,15],[0,0], 'k:')
axs[1][0].set_xlim(0.5,10)
axs[1][1].set_xlim(0.5,10)
axs[1][0].legend()

axs[2][0].plot(base['f_minus'], base['phi_minus'], 'b-')
axs[2][0].plot(base['f_plus'], base['phi_plus'], 'b--')
axs[2][0].plot(blockLVA['f_minus'], blockLVA['phi_minus'], 'r:', label=r'Block LVA Ca$^{2+}$')
axs[2][0].plot(blockLVA['f_plus'], blockLVA['phi_plus'], 'r:')
axs[2][0].plot([0,15],[0,0], 'k:')
axs[2][1].plot(blockLVAApic['f_minus'], blockLVAApic['phi_minus'], 'r-', label=r'Block LVA Ca$^{2+}$')
axs[2][1].plot(blockLVAApic['f_plus'], blockLVAApic['phi_plus'], 'r--')
axs[2][1].plot(distal['f_minus'], distal['phi_minus'], 'b-')
axs[2][1].plot(distal['f_plus'], distal['phi_plus'], 'b--')
axs[2][1].plot([0,15],[0,0], 'k:')
axs[2][0].set_xlim(0.5,10)
axs[2][1].set_xlim(0.5,10)
axs[2][0].legend()

axs[3][0].plot(baseTASK['f_minus'], baseTASK['phi_minus'], 'b-')
axs[3][0].plot(baseTASK['f_plus'], baseTASK['phi_plus'], 'b--')
axs[3][0].plot(blockTASK['f_minus'], blockTASK['phi_minus'], 'r-', label=r'Block I$_{TASK-like}$')
axs[3][0].plot(blockTASK['f_plus'], blockTASK['phi_plus'], 'r--')
axs[3][0].plot([0,15],[0,0], 'k:')
axs[3][1].plot(blockTASKApic['f_minus'], blockTASKApic['phi_minus'], 'r-')
axs[3][1].plot(blockTASKApic['f_plus'], blockTASKApic['phi_plus'], 'r--')
axs[3][1].plot(apic['f_minus'], apic['phi_minus'], 'b-')
axs[3][1].plot(apic['f_plus'], apic['phi_plus'], 'b--')
axs[3][1].plot([0,15],[0,0], 'k:')
axs[3][0].set_xlim(0.5,10)
axs[3][1].set_xlim(0.5,10)
axs[3][0].legend()

axs[2][0].set_ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=16)
axs[3][0].set_xlabel('Frequency (Hz)', fontsize=16)
axs[3][1].set_xlabel('Frequency (Hz)', fontsize=16)