from scipy.io import loadmat 
import os 
from matplotlib import pyplot as plt 
plt.ion()

files = os.listdir('data/chirpAsymV2/')

asym = []
zAmpErrs = []
zPhaseErrs = []
for filename in files:
    data = loadmat('data/chirpAsymV2/' + filename)
    asym.append(data['asymmetry'][0][0])
    zAmpErrs.append(data['zAmpErr'][0][0])
    zPhaseErrs.append(data['zPhaseErr'][0][0])

asym_sort = [a for a in sorted(asym)]
zAmpErr_sorted = [z for a, z in sorted(zip(asym, zAmpErrs))]
zPhaseErr_sorted = [z for a, z in sorted(zip(asym, zPhaseErrs))]

plt.figure()
data = loadmat('data/chirpAsymV2/chirp_amp-0.014999999999999996-f1-20-t0-20.mat')
plt.subplot(2,3,2)
plt.plot(data['Freq_cut'][0], data['zAmp_cut'][0], color='k')
plt.title('Input Impedance Amplitude', fontsize=16)
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.ylabel(r'|Z_{in}| (M$\Omega$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,3,3)
plt.plot(data['Freq_cut'][0], data['zPhase_cut'][0], color='k')
plt.title('Input Impedance Phase', fontsize=16)
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.ylabel(r'$\Phi_{in}$ (radians)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

data = loadmat('data/chirpAsymV2/chirp_amp-0.21230141534998076-f1-20-t0-20.mat')
plt.subplot(2,3,2)
plt.plot(data['Freq_cut'][0], data['ZinAmp'][0], color='gray')
plt.subplot(2,3,3)
plt.plot(data['Freq_cut'][0], data['ZinPhase'][0], color='gray')

plt.subplot(2,3,5)
plt.semilogx(asym_sort, zAmpErr_sorted, color='k', linestyle='-', linewidth=1.5)
plt.plot(asym_sort, zAmpErr_sorted, color='k', linewidth=1.5)
plt.title(r'|Z$_{in}$| Error', fontsize=16)
plt.xlabel('Response Asymmetry (mV)', fontsize=14)
plt.ylabel('Mean Squared Error (M$\Omega^2$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,3,6)
plt.semilogx(asym_sort, zAmpErr_sorted, color='k', linestyle='-', linewidth=1.5)
plt.plot(asym_sort, zAmpErr_sorted, color='k', linewidth=1.5)
plt.title(r'$\Phi_{in}$ (radians$^2$)', fontsize=16)
plt.xlabel('Response Asymmetry (mV)', fontsize=14)
plt.ylabel('Mean Squared Error (radians$^2$)', fontisze=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# v0.00 - plotting output from asymmetric chirp sims 