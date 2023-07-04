from matplotlib import pyplot as plt
plt.ion()
import json 
from math import radians 

fig, axs = plt.subplots(4,4, sharex=True)

filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8.json'
with open('Data/supra_data/' + filename) as fileObj:
    retreat = json.load(fileObj)

filename = 'HayCellMig_apic_36_amp_3.45_offset_0.0_f0_8_f1_8.json'
with open('Data/supra_data/' + filename) as fileObj:
    retreatApic = json.load(fileObj)

with open('supra_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_blockSKv3.json', 'rb') as fileObj:
    retreatSKv3 = json.load(fileObj)

with open('supra_data/HayCellMig_apic_36_amp_3.45_offset_0.0_f0_8_f1_8_blockSKv3.json', 'rb') as fileObj:
    retreatSKv3Apic = json.load(fileObj)

with open('supra_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_blockIm.json', 'rb') as fileObj:
    retreatIm = json.load(fileObj)

with open('supra_data/HayCellMig_apic_36_amp_3.45_offset_0.0_f0_8_f1_8_blockIm.json', 'rb') as fileObj:
    retreatImApic = json.load(fileObj)

with open('supra_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_blockLVACa.json', 'rb') as fileObj:
    retreatLVA = json.load(fileObj)

with open('supra_data/HayCellMig_apic_36_amp_3.45_offset_0.0_f0_8_f1_8_blockLVACa.json', 'rb') as fileObj:
    retreatLVAApic = json.load(fileObj)

with open('supra_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_blockTASK.json', 'rb') as fileObj:
    retreatTASK = json.load(fileObj)

with open('supra_data/HayCellMig_apic_36_amp_3.45_offset_0.0_f0_8_f1_8_blockTASK.json', 'rb') as fileObj:
    retreatTASKApic = json.load(fileObj)

axs[0][0].plot([i for i in range(len(retreat['lags']))], [radians(val)*-1 for val in retreat['angles']], 'o-', color='blue', label='Baseline')
axs[0][0].plot([i for i in range(len(retreatSKv3['lags']))], [radians(val)*-1 for val in retreatSKv3['angles']], 'o-', color='red', label=r'Block SKv3')
axs[0][0].plot([0,15], [0,0], 'k:')
axs[0][0].set_xlim(-0.1, 10)

axs[0][1].plot([i for i in range(len(retreatApic['lags']))], [radians(val)*-1 for val in retreatApic['angles']], 'o-', color='blue', label='Baseline')
axs[0][1].plot([i for i in range(len(retreatSKv3Apic['lags']))], [radians(val)*-1 for val in retreatSKv3Apic['angles']], 'o-', color='red', label='Baseline')
axs[0][1].plot([0,15], [0,0], 'k:')
axs[0][1].set_xlim(-0.1, 10)

axs[1][0].plot([i for i in range(len(retreat['lags']))], [radians(val)*-1 for val in retreat['angles']], 'o-', color='blue', label='Baseline')
axs[1][0].plot([i for i in range(len(retreatIm['lags']))], [radians(val)*-1 for val in retreatIm['angles']], 'o-', color='red', label=r'Block I$_m$')
axs[1][0].plot([0,15], [0,0], 'k:')
axs[1][0].set_xlim(-0.1, 10)

axs[1][1].plot([i for i in range(len(retreatApic['lags']))], [radians(val)*-1 for val in retreatApic['angles']], 'o-', color='blue', label='Baseline')
axs[1][1].plot([i for i in range(len(retreatImApic['lags']))], [radians(val)*-1 for val in retreatImApic['angles']], 'o-', color='red', label='Baseline')
axs[1][1].plot([0,15], [0,0], 'k:')
axs[1][1].set_xlim(-0.1, 10)

axs[2][0].plot([i for i in range(len(retreat['lags']))], [radians(val)*-1 for val in retreat['angles']], 'o-', color='blue', label='Baseline')
axs[2][0].plot([i for i in range(len(retreatLVA['lags']))], [radians(val)*-1 for val in retreatLVA['angles']], 'o-', color='red', label=r'Block LVA Ca$^{2+}$')
axs[2][0].plot([0,15], [0,0], 'k:')
axs[2][0].set_xlim(-0.1, 10)

axs[2][1].plot([i for i in range(len(retreatApic['lags']))], [radians(val)*-1 for val in retreatApic['angles']], 'o-', color='blue', label='Baseline')
axs[2][1].plot([i for i in range(len(retreatLVAApic['lags']))], [radians(val)*-1 for val in retreatLVAApic['angles']], 'o-', color='red', label='Baseline')
axs[2][1].plot([0,15], [0,0], 'k:')
axs[2][0].set_xlim(-0.1, 10)

axs[3][0].plot([i for i in range(len(retreat['lags']))], [radians(val)*-1 for val in retreat['angles']], 'o-', color='blue', label='Baseline')
axs[3][0].plot([i for i in range(len(retreatTASK['lags']))], [radians(val)*-1 for val in retreatTASK['angles']], 'o-', color='red', label=r'Block TASK-like Channel')
axs[3][0].plot([0,15], [0,0], 'k:')

axs[3][1].plot([i for i in range(len(retreatApic['lags']))], [radians(val)*-1 for val in retreatApic['angles']], 'o-', color='blue', label='Baseline')
axs[3][1].plot([i for i in range(len(retreatTASKApic['lags']))], [radians(val)*-1 for val in retreatTASKApic['angles']], 'o-', color='red', label='Baseline')
axs[3][1].plot([0,15], [0,0], 'k:')

filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6.json'
with open('Data/ramp_data/' + filename) as fileObj:
    advance = json.load(fileObj)

filename = 'HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6.json'
with open('Data/ramp_data/' + filename) as fileObj:
    advanceApic = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockSKv3.json', 'rb') as fileObj:
    advanceSKv3 = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockLVACa.json', 'rb') as fileObj:
    advanceLVA = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockLVACa.json', 'rb') as fileObj:
    advanceLVAApic = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockIm.json', 'rb') as fileObj:
    advanceIm = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockIm.json', 'rb') as fileObj:
    advanceImApic = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockTASK.json', 'rb') as fileObj:
    advanceTASK = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_36_amp_3.9_offset_0.0_f0_8_f1_8_s_1.0_t_6_blockTASK.json', 'rb') as fileObj:
    advanceTASKApic = json.load(fileObj)

axs[0][2].plot([i for i in range(len(advance['lags']))], [radians(val)*-1 for val in advance['angles']], 'o-', color='blue', label='Baseline')
axs[0][2].plot([i for i in range(len(advanceSKv3['lags']))], [radians(val)*-1 for val in advanceSKv3['angles']], 'o-', color='red', label=r'Block SKv3')
axs[0][2].plot([0,15], [0,0], 'k:')

# axs[0][0].set_xlim(-0.1, 10)

axs[0][3].plot([i for i in range(len(advanceApic['lags']))], [radians(val)*-1 for val in advanceApic['angles']], 'o-', color='blue', label='Baseline')
axs[0][3].plot([i for i in range(len(retreatSKv3Apic['lags']))], [radians(val)*-1 for val in retreatSKv3Apic['angles']], 'o-', color='red', label='Baseline')
axs[0][3].plot([0,15], [0,0], 'k:')

# axs[0][1].set_xlim(-0.1, 10)

axs[1][2].plot([i for i in range(len(advance['lags']))], [radians(val)*-1 for val in advance['angles']], 'o-', color='blue', label='Baseline')
axs[1][2].plot([i for i in range(len(advanceIm['lags']))], [radians(val)*-1 for val in advanceIm['angles']], 'o-', color='red', label='Baseline')
axs[1][2].plot([0,15], [0,0], 'k:')
# axs[1][0].set_xlim(-0.1, 10)

axs[1][3].plot([i for i in range(len(advanceApic['lags']))], [radians(val)*-1 for val in advanceApic['angles']], 'o-', color='blue', label='Baseline')
axs[1][3].plot([i for i in range(len(advanceImApic['lags']))], [radians(val)*-1 for val in advanceImApic['angles']], 'o-', color='red', label='Baseline')
axs[1][3].plot([0,15], [0,0], 'k:')
# # axs[1][1].set_xlim(-0.1, 10)

axs[2][2].plot([i for i in range(len(advance['lags']))], [radians(val)*-1 for val in advance['angles']], 'o-', color='blue', label='Baseline')
axs[2][2].plot([i for i in range(len(advanceLVA['lags']))], [radians(val)*-1 for val in advanceLVA['angles']], 'o-', color='red', label='Baseline')
axs[2][2].plot([0,15], [0,0], 'k:')
# axs[2][0].set_xlim(-0.1, 10)

axs[2][3].plot([i for i in range(len(advanceApic['lags']))], [radians(val)*-1 for val in advanceApic['angles']], 'o-', color='blue', label='Baseline')
axs[2][3].plot([i for i in range(len(advanceLVAApic['lags']))], [radians(val)*-1 for val in advanceLVAApic['angles']], 'o-', color='red', label='Baseline')
axs[2][3].plot([0,15], [0,0], 'k:')
axs[2][2].set_xlim(-0.1, 14)

axs[3][2].plot([i for i in range(len(advance['lags']))], [radians(val)*-1 for val in advance['angles']], 'o-', color='blue', label='Baseline')
axs[3][2].plot([i for i in range(len(advanceTASK['lags']))], [radians(val)*-1 for val in advanceTASK['angles']], 'o-', color='red', label='Baseline')
axs[3][2].plot([0,15], [0,0], 'k:')

axs[3][3].plot([i for i in range(len(advanceApic['lags']))], [radians(val)*-1 for val in advanceApic['angles']], 'o-', color='blue', label='Baseline')
axs[3][3].plot([i for i in range(len(advanceTASKApic['lags']))], [radians(val)*-1 for val in advanceTASKApic['angles']], 'o-', color='red', label='Baseline')
axs[3][3].plot([0,15], [0,0], 'k:')

for i in range(4):
    axs[i][0].legend()
    axs[i][0].set_ylabel(r'$\Phi^+$ (radians)', fontsize=16)
    axs[-1][i].set_xlabel('Frequency (Hz)', fontsize=16)

axs[0][0].set_title('Soma', fontsize=18)
axs[0][2].set_title('Soma', fontsize=18)
axs[0][1].set_title('Apical Dendrite', fontsize=18)
axs[0][3].set_title('Apical Dendrite', fontsize=18)
