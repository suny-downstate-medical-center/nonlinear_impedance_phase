import numpy as np 
from matplotlib import pyplot as plt 
plt.ion()
import os 
from scipy.io import loadmat 
import json
from sklearn.metrics import mean_squared_error 

# import validation data 
with open('data/noise_freq_validation_amp01.json','rb') as fileObj:
    data = json.load(fileObj)

freqs = [] 
zAmp = [] 
zPhase = [] 
for f in data.keys(): 
    freqs.append(float(f)) 
    zAmp.append(data[f]['zAmp']) 
    zPhase.append(data[f]['zPhase'])  
freqs_valid = [f for f in sorted(freqs)] 
zAmp_valid = [z for f, z in sorted(zip(freqs, zAmp))] 
zPhase_valid = [z for f, z in sorted(zip(freqs, zPhase))] 

# noise with varied parameters 
filenames = os.listdir('data/noiseParams/')
binsizes = np.linspace(1, 25, num=5)
# parameters and error matrices  
stds = np.linspace(0.1, 0.9, num=9)
t0s = np.linspace(2, 20, num=10)
zAmpErrs = np.zeros((9,10,5))
zPhaseErrs = np.zeros((9,10,5))

# compute errors 
for filename in filenames:
    ## no soothing 
    bnsz = int(filename.split('-')[5].split('.')[0])
    # if bnsz == 13:
    data = loadmat('data/noiseParams/' + filename)
        ## extract parameters
    gstd = float(filename.split('-')[1])
    t0 = float(filename.split('-')[3])
    ## downsample validation data for comparisons 
    validDown_zAmp = []
    validDown_zPhase = []
    validDown_freq = []
    for f in data['Freq'][0]:
        ind = np.argmin(np.square(np.subtract(freqs_valid,f)))
        validDown_freq.append(freqs_valid[ind])
        validDown_zAmp.append(zAmp_valid[ind])
        validDown_zPhase.append(zPhase_valid[ind])
    ampErr = mean_squared_error(validDown_zAmp, data['zAmp'][0])
    phaseErr = mean_squared_error(validDown_zPhase, data['zPhase'][0])
    xind = np.argmin(np.square(np.subtract(stds,gstd)))
    yind = np.argmin(np.square(np.subtract(t0s, t0)))
    zind = np.argmin(np.square(np.subtract(binsizes,bnsz)))
    zAmpErrs[xind][yind][zind] = ampErr
    zPhaseErrs[xind][yind][zind] = phaseErr

