from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt 
plt.ion()
import json 
import numpy as np 
from scipy.io import loadmat 

# loading and preprocessing 
## chirp and noise data
# noise = loadmat('data/noise_20s_25ptSmth.mat')
# chirp = loadmat('data/chirp_amp025_T20.mat')
# chirpLong = loadmat('data/chirp_05-500Hz_60s.mat')
# chirpLog20 = loadmat('data/log_chirp_20s_05-20Hz.mat')
# chirpLog60 = loadmat('data/log_chirp_60s_05-500Hz.mat')
chirp = loadmat('data/chirp_05-20_20s_noFliter.mat')
noise = loadmat('data/noise_05-500_20s_5std_noFilter.mat')
chirpLog20 = loadmat('data/logChirp_05-20_20s_noFilter.mat')
chirpLog60 = loadmat('data/logChirp_05-500_60s_noFilter.mat')
chirpLong = loadmat('data/chirp_05-500_60s_noFliter.mat')
noise20 = loadmat('data/noise_05-20_20s_5std_noFilter.mat')

## noise validation data 
with open('data/noise_freq_validation_amp01.json', 'rb') as fileObj:
    data = json.load(fileObj)

freqs = [] 
zAmp = [] 
zPhase = [] 
for f in data.keys(): 
    freqs.append(float(f)) 
    zAmp.append(data[f]['zAmp']) 
    zPhase.append(data[f]['zPhase']) 
noise_freqs = [f for f in sorted(freqs)] 
noise_zAmp = [z for f, z in sorted(zip(freqs, zAmp))] 
noise_zPhase = [z for f, z in sorted(zip(freqs, zPhase))] 

validNoise_freqs = []
validNoise_zAmp = []
validNoise_zPhase = []
for f in noise['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(noise_freqs,f)))
    validNoise_freqs.append(noise_freqs[ind])
    validNoise_zAmp.append(noise_zAmp[ind])
    validNoise_zPhase.append(noise_zPhase[ind])

validNoise_freqs_cut = []
validNoise_zAmp_cut = []
validNoise_zPhase_cut = []
for f in noise20['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(noise_freqs,f)))
    validNoise_freqs_cut.append(noise_freqs[ind])
    validNoise_zAmp_cut.append(noise_zAmp[ind])
    validNoise_zPhase_cut.append(noise_zPhase[ind])


## chirp validation data 
# with open('data/chirp_freq_validation_amp01.json', 'rb') as fileObj:
#     data = json.load(fileObj)

# freqs = [] 
# zAmp = [] 
# zPhase = [] 
# for f in data.keys(): 
#     freqs.append(float(f)) 
#     zAmp.append(data[f]['zAmp']) 
#     zPhase.append(data[f]['zPhase']) 
validChirp_freqs = [] # [f for f in sorted(freqs)] 
validChirp_zAmp = [] # [z for f, z in sorted(zip(freqs, zAmp))] 
validChirp_zPhase = [] # [z for f, z in sorted(zip(freqs, zPhase))] 
for f in chirp['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(noise_freqs,f)))
    validChirp_freqs.append(noise_freqs[ind])
    validChirp_zAmp.append(noise_zAmp[ind])
    validChirp_zPhase.append(noise_zPhase[ind])

## create valid set for long chirp 
validChirpLong_zAmp = []
validChirpLong_zPhase = []
validChirpLong_freq = []
for f in chirpLong['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(noise_freqs,f)))
    validChirpLong_freq.append(noise_freqs[ind])
    validChirpLong_zAmp.append(noise_zAmp[ind])
    validChirpLong_zPhase.append(noise_zPhase[ind])

## valid set for log chirp 
validChirpLog20_zAmp = []
validChirpLog20_zPhase = []
validChirpLog20_freq = []
validChirpLog60_zAmp = []
validChirpLog60_zPhase = []
validChirpLog60_freq = []
for f in chirpLog20['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(noise_freqs, f)))
    validChirpLog20_zAmp.append(noise_zAmp[ind])
    validChirpLog20_zPhase.append(noise_zPhase[ind])
    validChirpLog20_freq.append(noise_freqs[ind])
for f in chirpLog60['Freq'][0]:
    ind = np.argmin(np.square(np.subtract(noise_freqs, f)))
    validChirpLog60_zAmp.append(noise_zAmp[ind])
    validChirpLog60_zPhase.append(noise_zPhase[ind])
    validChirpLog60_freq.append(noise_freqs[ind])

# compute errors 
noise_zAmpErr = mean_squared_error(noise['ZinAmp'][0], validNoise_zAmp)
noise_zPhaseErr = mean_squared_error(noise['ZinPhase'][0], validNoise_zPhase)
noise_cut_zAmpErr = mean_squared_error(noise20['ZinAmp'][0], validNoise_zAmp_cut)
noise_cut_zPhaseErr = mean_squared_error(noise20['ZinPhase'][0], validNoise_zPhase_cut)
chirp_zAmpErr = mean_squared_error(chirp['ZinAmp'][0], validChirp_zAmp)
chirp_zPhaseErr = mean_squared_error(chirp['ZinPhase'][0], validChirp_zPhase)
longChirp_zAmpErr = mean_squared_error(chirpLong['ZinAmp'][0], validChirpLong_zAmp)
longChirp_zPhaseErr = mean_squared_error(chirpLong['ZinPhase'][0], validChirpLong_zPhase)
logChirp20_zAmpErr = mean_squared_error(chirpLog20['ZinAmp'][0], validChirpLog20_zAmp)
logChirp20_zPhaseErr = mean_squared_error(chirpLog20['ZinPhase'][0], validChirpLog20_zPhase)
logChirp60_zAmpErr = mean_squared_error(chirpLog60['ZinAmp'][0], validChirpLog60_zAmp)
logChirp60_zPhaseErr = mean_squared_error(chirpLog60['ZinPhase'][0], validChirpLog60_zPhase)

# plotting
plt.figure()
plt.subplot(2,2,1)
l = r'Log Chirp: %.2f M$\Omega^2$' % (logChirp20_zAmpErr)
plt.plot(chirpLog20['Freq'][0], chirpLog20['ZinAmp'][0], label=l, color='g')
l = r'Noise: %.2f M$\Omega^2$' % (noise_cut_zAmpErr)
plt.plot(noise20['Freq'][0], noise20['ZinAmp'][0], label=l, color='r')
l = r'Linear Chirp: %.2f M$\Omega^2$' % (chirp_zAmpErr)
plt.plot(chirp['Freq'][0], chirp['ZinAmp'][0], label=l, color='b')
plt.plot(validChirp_freqs, validChirp_zAmp, label='Validation', color='k')
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.setp(legend.get_title(), fontsize=12)
plt.ylabel(r'|Z$_{in}$| (M$\Omega$)', fontsize=14)
plt.title('Input Impedance Amplitude', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,2,2)
l = r'Log Chirp: %.5f radians$^2$' % (logChirp20_zPhaseErr)
plt.plot(chirpLog20['Freq'][0], chirpLog20['ZinPhase'][0], label=l, color='g')
l = r'Noise: %.5f radians$^2$' % (noise_cut_zPhaseErr)
plt.plot(noise20['Freq'][0], noise20['ZinPhase'][0], label=l, color='r')
l = r'Linear Chirp: %.5f radians$^2$' % (chirp_zPhaseErr)
plt.plot(chirp['Freq'][0], chirp['ZinPhase'][0], label=l, color='b')
plt.plot(validChirp_freqs, validChirp_zPhase, label='Validation', color='k')
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.setp(legend.get_title(), fontsize=12)
plt.ylabel(r'$\Phi_{in}$ (radians)', fontsize=14)
plt.title('Input Impedance Phase', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,2,3)
l = r'Log Chirp: %.3f M$\Omega^2$' % (logChirp60_zAmpErr)
plt.semilogx(chirpLog60['Freq'][0], chirpLog60['ZinAmp'][0], label=l, color='g')
l = r'Noise: %.2f M$\Omega^2$' % (noise_zAmpErr)
plt.semilogx(noise['Freq'][0], noise['ZinAmp'][0], label=l, color='r')
l = r'Linear Chirp: %.3f M$\Omega^2$' % (longChirp_zAmpErr)
# plt.plot(chirpLong['Freq'][0], chirpLong['ZinAmp'][0], label=l, color='b')
# l = r'Noise: %.2f M$\Omega^2$' % (noise_zAmpErr)
# plt.plot(noise['Freq'][0], noise['ZinAmp'][0], label=l, color='r')
# plt.plot(validNoise_freqs, validNoise_zAmp, label='Validation',  color='k')
plt.semilogx(chirpLong['Freq'][0], chirpLong['ZinAmp'][0], label=l, color='b')
plt.semilogx(validNoise_freqs, validNoise_zAmp, label='Validation',  color='k')
plt.ylabel(r'|Z$_{in}$| (M$\Omega$)', fontsize=14)
plt.xlabel('Frequency (Hz)', fontsize=14)
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.setp(legend.get_title(), fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(2,2,4)
l = r'Noise: %.5f radians$^2$' % (noise_zPhaseErr)
plt.semilogx(noise['Freq'][0], noise['ZinPhase'][0], label=l, color='r')
l = r'Log Chirp: %.5f radians$^2$' % (logChirp60_zPhaseErr)
plt.semilogx(chirpLog60['Freq'][0], chirpLog60['ZinPhase'][0], label=l, color='g')
l = r'Linear Chirp: %.5f radians$^2$' % (longChirp_zPhaseErr)
# plt.plot(chirpLong['Freq'][0], chirpLong['ZinPhase'][0], label=l, color='b')
# l = r'Noise: %.2f radians$^2$' % (noise_zPhaseErr)
# plt.plot(noise['Freq'][0], noise['ZinPhase'][0], label=l, color='r')
# plt.plot(validNoise_freqs, validNoise_zPhase, label='Validation', color='k')
plt.semilogx(chirpLong['Freq'][0], chirpLong['ZinPhase'][0], label=l, color='b')
plt.semilogx(validNoise_freqs, validNoise_zPhase, label='Validation', color='k')
plt.xlabel('Frequency (Hz)', fontsize=14)
plt.ylabel(r'$\Phi_{in}$ (radians)', fontsize=14)
legend = plt.legend(title='Mean Squared Errors', fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.setp(legend.get_title(), fontsize=12)