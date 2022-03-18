from scipy.io import loadmat 
from matplotlib import pyplot as plt 
from sklearn.metrics import mean_squared_error
import numpy as np 
import json
plt.ion() 
plt.figure() 

twoSec20 = loadmat('data/noise_05-20_2s_5std_noFilter.mat')
twoSec500 = loadmat('data/noise_05-500_2s_5std_noFilter.mat')
twenSec500 = loadmat('data/noise_05-500_20s_5std_noFilter.mat')
twenSec20 = loadmat('data/noise_05-20_20s_5std_noFilter.mat')

with open('data/noise_freq_validation_amp01.json', 'rb') as fileObj: 
    data = json.load(fileObj)    
freqs_temp = [] 
zAmp_temp = [] 
zPhase_temp = [] 
for f in data.keys(): 
    freqs_temp.append(float(f)) 
    zAmp_temp.append(data[f]['zAmp']) 
    zPhase_temp.append(data[f]['zPhase'])
freqs = [f for f in sorted(freqs_temp)]
zAmp = [z for f, z in sorted(zip(freqs_temp, zAmp_temp))] 
zPhase = [z for f, z in sorted(zip(freqs_temp, zPhase_temp))] 

valid_twoSec20_zAmp = []
valid_twoSec20_zPhase = []
valid_twenSec20_zAmp = []
valid_twenSec20_zPhase = []
valid_twoSec500_zAmp = []
valid_twoSec500_zPhase = []
valid_twenSec500_zAmp = []
valid_twenSec500_zPhase = []
for f in twoSec20['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(freqs,f)))
    valid_twoSec20_zAmp.append(zAmp[ind])
    valid_twoSec20_zPhase.append(zPhase[ind])
for f in twenSec20['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(freqs,f)))
    valid_twenSec20_zAmp.append(zAmp[ind])
    valid_twenSec20_zPhase.append(zPhase[ind])
for f in twoSec500['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(freqs,f)))
    valid_twoSec500_zAmp.append(zAmp[ind])
    valid_twoSec500_zPhase.append(zPhase[ind])
for f in twenSec500['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(freqs,f)))
    valid_twenSec500_zAmp.append(zAmp[ind])
    valid_twenSec500_zPhase.append(zPhase[ind])

twoSec20_zAmp_err = mean_squared_error(twoSec20['ZinAmp'][0], valid_twoSec20_zAmp)
twoSec20_zPhase_err = mean_squared_error(twoSec20['ZinPhase'][0], valid_twoSec20_zPhase)
twoSec500_zAmp_err = mean_squared_error(twoSec500['ZinAmp'][0], valid_twoSec500_zAmp)
twoSec500_zPhase_err = mean_squared_error(twoSec500['ZinPhase'][0], valid_twoSec500_zPhase)
twenSec20_zAmp_err = mean_squared_error(twenSec20['ZinAmp'][0], valid_twenSec20_zAmp)
twenSec20_zPhase_err = mean_squared_error(twenSec20['ZinPhase'][0], valid_twenSec20_zPhase)
twenSec500_zAmp_err = mean_squared_error(twenSec500['ZinAmp'][0], valid_twenSec500_zAmp)
twenSec500_zPhase_err = mean_squared_error(twenSec500['ZinPhase'][0], valid_twenSec500_zPhase)

plt.subplot(2,2,1)
l = '2s Noise: %.2f M$\Omega^2$' % (twoSec20_zAmp_err)
plt.plot(twoSec20['Freq'][0], twoSec20['ZinAmp'][0], label=l)
plt.subplot(2,2,2)
l = '2s Noise: %.4f radians$^2$' % (twoSec20_zPhase_err)
plt.plot(twoSec20['Freq'][0], twoSec20['ZinPhase'][0], label=l)

plt.subplot(2,2,3)
l = '2s Noise: %.2f M$\Omega^2$' % (twoSec500_zAmp_err)
plt.semilogx(twoSec500['Freq'][0], twoSec500['ZinAmp'][0], label=l)
plt.subplot(2,2,4)
l = '2s Noise: %.4f radians$^2$' % (twoSec500_zPhase_err)
plt.semilogx(twoSec500['Freq'][0], twoSec500['ZinPhase'][0], label=l)

plt.subplot(2,2,1)
l = '20s Noise: %.2f M$\Omega^2$' % (twenSec20_zAmp_err)
plt.plot(twenSec20['Freq'][0], twenSec20['ZinAmp'][0], label=l)
plt.subplot(2,2,2)
l = '20s Noise: %.4f radians$^2$' % (twenSec20_zPhase_err)
plt.plot(twenSec20['Freq'][0], twenSec20['ZinPhase'][0], label=l)

plt.subplot(2,2,3)
l = '20s Noise: %.2f M$\Omega^2$' % (twenSec500_zAmp_err)
plt.semilogx(twenSec500['Freq'][0], twenSec500['ZinAmp'][0], label=l)
plt.subplot(2,2,4)
l = '20s Noise: %.4f radians$^2$' % (twenSec500_zPhase_err)
plt.semilogx(twenSec500['Freq'][0], twenSec500['ZinPhase'][0], label=l)

plt.subplot(2,2,1)
plt.plot(freqs, zAmp, label='Validation')
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.setp(legend.get_title(), fontsize=12)
plt.xlim(0,20)
plt.ylabel('|Z$_{in}$| (M$\Omega$)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title('Input Impedance Amplitude', fontsize=16)

plt.subplot(2,2,2)
plt.plot(freqs, zPhase, label='Validation')
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.setp(legend.get_title(), fontsize=12)
plt.xlim(0,20)
plt.ylabel('$\Phi_{in}$ (radians)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title('Input Impedance Phase', fontsize=16)

plt.subplot(2,2,3)
plt.plot(freqs, zAmp, label='Validation')
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.setp(legend.get_title(), fontsize=12)
plt.ylabel('|Z$_{in}$| (M$\Omega$)', fontsize=14)
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,2,4)
plt.plot(freqs, zPhase, label='Validation')
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.setp(legend.get_title(), fontsize=12)
plt.ylabel('$\Phi_{in}$ (radians)', fontsize=14)
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)