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

# v0.00 - plotting output from asymmetric chirp sims 