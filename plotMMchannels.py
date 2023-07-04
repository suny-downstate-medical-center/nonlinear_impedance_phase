import json 
from matplotlib import pyplot as plt 
plt.ion()

with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12.json' , 'rb') as fileObj:
    base = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12_blockIh.json' , 'rb') as fileObj:
    blockIh = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12_blockKa.json' , 'rb') as fileObj:
    blockKa = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12_blockKdr.json' , 'rb') as fileObj:
    blockKdr = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12_blockKm.json' , 'rb') as fileObj:
    blockKm = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12_blockNax.json' , 'rb') as fileObj:
    blockNax = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.5_offset_0.0_f0_0_f1_12_blockNa3.json' , 'rb') as fileObj:
    blockNa3 = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.3_offset_0.0_f0_0_f1_12_blockIh_blockKm.json', 'rb') as fileObj:
    blockIhKm = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.1_offset_0.0_f0_0_f1_12_blockIhKmKa.json', 'rb') as fileObj:
    blockIhKmKa = json.load(fileObj)
with open('asym_data/Migliore_apic_0_amp_0.1_offset_0.0_f0_0_f1_12_blockIhKmKaNa3.json', 'rb') as fileObj:
    blockIhKmKaNa3 = json.load(fileObj)

plt.plot(base['f_minus'], base['phi_minus'], 'k-', label='Control')
plt.plot(base['f_plus'], base['phi_plus'], 'k--')
plt.plot(blockIh['f_minus'], blockIh['phi_minus'], 'r-', label=r'Block I$_h$')
plt.plot(blockIh['f_plus'], blockIh['phi_plus'], 'r--')
plt.plot(blockKm['f_minus'], blockKm['phi_minus'], 'b-', label=r'Block I$_m$')
plt.plot(blockKm['f_plus'], blockKm['phi_plus'], 'b--')
# plt.plot(blockKdr['f_minus'], blockKdr['phi_minus'], 'g-', label='Block Kdr')
# plt.plot(blockKdr['f_plus'], blockKdr['phi_plus'], 'g--')
# plt.plot(blockKa['f_minus'], blockKa['phi_minus'], '-', color='orange', label='Block Ka')
# plt.plot(blockKa['f_plus'], blockKa['phi_plus'], '--', color='orange')
# plt.plot(blockNax['f_minus'], blockNax['phi_minus'], 'm-', label='Block Nax')
# plt.plot(blockNax['f_plus'], blockNax['phi_plus'], 'm--')
# plt.plot(blockNa3['f_minus'], blockNa3['phi_minus'], 'c-', label='Block Na3')
# plt.plot(blockNa3['f_plus'], blockNa3['phi_plus'], 'c--')
plt.plot(blockIhKm['f_minus'], blockIhKm['phi_minus'], '-', label=r'Block I$_h$ & I$_m$', color='orange')
plt.plot(blockIhKm['f_plus'], blockIhKm['phi_plus'], '--', color='orange')
plt.plot(blockIhKmKa['f_minus'], blockIhKmKa['phi_minus'], '-', label=r'Block I$_h$, I$_m$, & I$_A$', color='green')
plt.plot(blockIhKmKa['f_plus'], blockIhKmKa['phi_plus'], '--', color='green')
plt.plot([-0.8,15],[0,0], 'k:')
# plt.plot(blockIhKmKaNa3['f_minus'], blockIhKmKaNa3['phi_minus'], '-', label=r'Block I$_h$, I$_m$, I$_A$, & I$_{Nap}$', color='yellow')
# plt.plot(blockIhKmKaNa3['f_plus'], blockIhKmKaNa3['phi_plus'], '--', color='yellow')
plt.xlabel('Frequency (Hz)', fontsize=18)
plt.ylabel(r'$\Phi^{\pm}$ (radians)', fontsize=18)
plt.legend(title='Condition')
plt.ylim(-0.8, 0.22)
plt.xlim(0.5,10)
