from matplotlib import pyplot as plt
plt.ion()
import json 
from math import radians 

fig, axs = plt.subplots(4, 3)

# subthreshold 
with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    base = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.1_offset_0.0_f0_0_f1_12.json', 'rb') as fileObj:
    baseLow = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_cell2.json', 'rb') as fileObj:
    cell2 = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.4_offset_0.0_f0_0_f1_13_cell3.json', 'rb') as fileObj:
    cell3 = json.load(fileObj)

with open('asym_data/HayCellMig_apic_0_amp_0.1_offset_0.0_f0_0_f1_13_V1.json', 'rb') as fileObj:
    cell4 = json.load(fileObj)

axs[0][0].plot(base['f_minus'], base['phi_minus'], 'k-')
axs[0][0].plot(base['f_plus'], base['phi_plus'], 'k--')
axs[0][0].set_xlim(0.5,10)
axs[0][0].set_title('Subthreshold', fontsize=18)

axs[1][0].plot(base['f_minus'], base['phi_minus'], 'k-')
axs[1][0].plot(base['f_plus'], base['phi_plus'], 'k--')
axs[1][0].plot(cell2['f_minus'], cell2['phi_minus'], 'r-')
axs[1][0].plot(cell2['f_plus'], cell2['phi_plus'], 'r--')
axs[1][0].set_xlim(0.5,10)

axs[2][0].plot(base['f_minus'], base['phi_minus'], 'k-')
axs[2][0].plot(base['f_plus'], base['phi_plus'], 'k--')
axs[2][0].plot(cell3['f_minus'], cell3['phi_minus'], 'r-')
axs[2][0].plot(cell3['f_plus'], cell3['phi_plus'], 'r--')
axs[2][0].set_xlim(0.5,10)
axs[2][0].set_ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=16)

axs[3][0].plot(baseLow['f_minus'], baseLow['phi_minus'], 'k-')
axs[3][0].plot(baseLow['f_plus'], baseLow['phi_plus'], 'k--')
axs[3][0].plot(cell4['f_minus'], cell4['phi_minus'], 'r-')
axs[3][0].plot(cell4['f_plus'], cell4['phi_plus'], 'r--')
axs[3][0].set_xlim(0.5,10)
axs[3][0].set_xlabel('Frequency (Hz)', fontsize=16)

# phase retreat 
filename = 'HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8.json'
with open('Data/supra_data/' + filename) as fileObj:
    base = json.load(fileObj)

with open('supra_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_cell2.json', 'rb') as fileObj:
    cell2 = json.load(fileObj)

with open('supra_data/HayCellMig_apic_0_amp_2.0_offset_0.0_f0_8_f1_8_cell3.json', 'rb') as fileObj:
    cell3 = json.load(fileObj)

with open('supra_data/HayCellMig_apic_0_amp_1.2_offset_0.0_f0_8_f1_8_V1.json', 'rb') as fileObj:
    cell4 = json.load(fileObj)

axs[0][1].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[0][1].set_xlim(-0.1, 10)
axs[0][1].set_title('Phase Retreat', fontsize=18)

axs[1][1].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[1][1].plot([i for i in range(len(cell2['lags']))], [radians(val)*-1 for val in cell2['angles']], 'o-', color='red', label='Control')
axs[1][1].set_xlim(-0.1, 10)

axs[2][1].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[2][1].plot([i for i in range(len(cell3['lags']))], [radians(val)*-1 for val in cell3['angles']], 'o-', color='red', label='Control')
axs[2][1].set_xlim(-0.1, 10)
axs[2][1].set_ylabel(r'$\Phi^{+}$ (radians)', fontsize=16)

axs[3][1].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[3][1].plot([i for i in range(len(cell4['lags']))], [radians(val)*-1 for val in cell4['angles']], 'o-', color='red', label='Control')
axs[3][1].set_xlabel('Stimulus Cycle (n)', fontsize=16)
axs[3][1].set_xlim(-0.1, 10)

# phase advance 
filename = 'HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6.json'
with open('Data/ramp_data/' + filename) as fileObj:
    base = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_0_amp_3.0_offset_0.0_f0_8_f1_8_s_1.0_t_6morph2.json', 'rb') as fileObj:
    cell2 = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_0_amp_1.9_offset_0.0_f0_8_f1_8_s_1.0_t_6morph1.json', 'rb') as fileObj:
    cell3 = json.load(fileObj)

with open('ramp_data/HayCellMig_apic_0_amp_1.0_offset_0.0_f0_8_f1_8_s_1.0_t_6morphv1.json', 'rb') as fileObj:
    cell4 = json.load(fileObj)

axs[0][2].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[0][2].set_xlim(-0.1, 10)
axs[0][2].set_title('Phase Advance', fontsize=18)

axs[1][2].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[1][2].plot([i for i in range(len(cell2['lags']))], [radians(val)*-1 for val in cell2['angles']], 'o-', color='red', label='Control')
axs[1][2].set_xlim(-0.1, 10)
axs[1][2].set_ylabel(r'$\Phi^{+}$ (radians)', fontsize=16)

axs[2][2].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[2][2].plot([i for i in range(len(cell3['lags']))], [radians(val)*-1 for val in cell3['angles']], 'o-', color='red', label='Control')
axs[2][2].set_xlim(-0.1, 10)

axs[3][2].plot([i for i in range(len(base['lags']))], [radians(val)*-1 for val in base['angles']], 'o-', color='black', label='Control')
axs[3][2].plot([i for i in range(len(cell4['lags']))], [radians(val)*-1 for val in cell4['angles']], 'o-', color='red', label='Control')
axs[3][2].set_xlabel('Stimulus Cycle (n)', fontsize=16)
axs[3][2].set_xlim(-0.1, 10)