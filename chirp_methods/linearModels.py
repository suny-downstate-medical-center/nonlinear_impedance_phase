from scipy.io import loadmat 
from pylab import fft, ifft, convolve
import numpy as np 
from matplotlib import pyplot as plt 

# load impedance data and traces from single ~1mV syn stim 
chirp = loadmat('data/chirp-60s_amp01.mat')
noise = loadmat('data/noise_20s_amp01_v2.mat')
syn_data = loadmat('data/single_syn.mat')

noise_pred = convolve(syn_data['i'][0], ifft(noise['zin'][0]))
chirp_pred = convolve(syn_data['i'][0], ifft(chirp['z'][0]))

# # FFT of syn stim 
# f_i = (fft(syn_data['i'][0]) / len(syn_data['i'][0]))[0:int(len(syn_data['i'][0])/2)] 
# freq_i = np.linspace(0.0, 40e3 / 2, len(f_i)) 

# ## downample f_i based on freqs in noise imped 
# f_i_noise = []
# for f in noise['Freq'][0]:
#     ind = np.argmin(np.square(np.subtract(freq_i,f)))
#     f_i_noise.append(f_i[ind])

# ## same for chirp imped 
# f_i_chirp = []
# for f in chirp['Freq'][0]:
#     ind = np.argmin(np.square(np.subtract(freq_i,f)))
#     f_i_chirp.append(f_i[ind])

# # compute output from linear transfer functions 
# noise_td = ifft(noise['zin'][0])
# chirp_td = ifft(chirp['z'][0])
# noise_pred = ifft(np.multiply(noise['zin'][0], f_i_noise))
# chirp_pred = ifft(np.multiply(chirp['z'][0], f_i_chirp))
