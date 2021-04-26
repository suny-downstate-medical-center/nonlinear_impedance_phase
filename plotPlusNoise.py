import numpy as np 
from matplotlib import pyplot as plt 
plt.ion()
import os 
from scipy.io import loadmat 
import json
import multiprocessing 

# noise with varied parameters 
filenames = os.listdir('data/chirpNoiseData/')
noise_stds = [0.1, 0.3, 0.5, 0.7, 0.9]
noise_amps = np.linspace(0.005, 0.2, num=10)
# binsizes = [1, 5, 10, 15, 20, 25, 30, 35, 40]
binsizes = [1, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200]

noise_v_std = np.zeros((len(noise_amps), len(noise_stds)))
noise_v_amp = np.zeros((len(noise_amps), len(noise_stds)))
zPhaseErrs = np.zeros((len(noise_amps), len(noise_stds)))
zAmpErrs = np.zeros((len(noise_amps), len(noise_stds)))
optFiltAmp = np.zeros((len(noise_amps), len(noise_stds)))
optFiltPhs = np.zeros((len(noise_amps), len(noise_stds)))
optPhsErr = np.zeros((len(noise_amps), len(noise_stds)))
optAmpErr = np.zeros((len(noise_amps), len(noise_stds)))

for filename in filenames:
    noise_amp = float(filename.split('-')[1])
    noise_std = float(filename.split('-')[3])
    bnsz = int(filename.split('-')[-1].split('.')[0])
    amperrs = []
    phserrs = []
    if bnsz == 1:
        data = loadmat('data/chirpNoiseData/' + filename)
        xind = np.argmin(np.square(np.subtract(noise_amps,noise_amp)))
        yind = np.argmin(np.square(np.subtract(noise_stds, noise_std)))
        zPhaseErrs[xind][yind] = data['zPhaseErr']
        zAmpErrs[xind][yind] = data['zAmpErr']
        noise_v_std[xind][yind] = data['noise_v_std']
        noise_v_amp[xind][yind] = data['noise_peak_to_peak']
        amperrs.append(data['zAmpErr'])
        phserrs.append(data['zPhaseErr'])
        for bnsz in binsizes[1:]:
            data = loadmat('data/chirpNoiseData/' + filename.split('bnsz')[0] 
                + 'bnsz-' + str(bnsz) + '.mat')
            amperrs.append(data['zAmpErr'])
            phserrs.append(data['zPhaseErr'])
        optFiltAmp[xind][yind] = binsizes[np.argmin(amperrs)]
        optFiltPhs[xind][yind] = binsizes[np.argmin(phserrs)]
        optAmpErr[xind][yind] = np.min(amperrs)
        optPhsErr[xind][yind] = np.min(phserrs)

noise_v_std_trim = []
noise_v_amp_trim = []
zPhaseErrs_trim = []
zAmpErrs_trim = []
optFiltAmp_trim = []
optFiltPhs_trim = []
optPhsErr_trim = []
optAmpErr_trim = []

for noisevamp, noisestd, amperr, phserr, optphserr, optamperr, optphswin, optampwin in sorted(zip(noise_v_amp.flatten(), noise_v_std.flatten(), zAmpErrs.flatten(), zPhaseErrs.flatten(), optPhsErr.flatten(), optAmpErr.flatten(), optFiltAmp.flatten(), optFiltPhs.flatten())):
    if noisevamp < 6.0:
        noise_v_std_trim.append(noisestd)
        noise_v_amp_trim.append(noisevamp)
        zPhaseErrs_trim.append(phserr)
        zAmpErrs_trim.append(amperr)
        optFiltAmp_trim.append(optampwin)
        optFiltPhs_trim.append(optphswin)
        optPhsErr_trim.append(optphserr)
        optAmpErr_trim.append(optamperr)


# v0.00 - plot amplitude and phase errs by amp and std of noise 
# v0.01 - adding optimal filter window size