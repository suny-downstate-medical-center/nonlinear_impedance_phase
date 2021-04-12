from getCells import M1Cell   
s = M1Cell()  
seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
from chirpUtils import getChirp
from neuron import h 
stim = h.IClamp(seg)
from pylab import fft, convolve
import numpy as np 
# import argparse
import os
import multiprocessing
import json 

#computes impedance from sinusoidal signal of single frequency 
def runInputValidation(input_data):
    f, amp, t0, sampr, delay, return_dict = input_data[0], input_data[1], input_data[2], input_data[3], input_data[4], input_data[5]
    f0, f1 = f, f
    print('Running validation at f = ' + str(f))
    soma_v = h.Vector().record(seg._ref_v) 
    time = h.Vector().record(h._ref_t)
    f0, f1 = f, f 
    Fs = 1000
    I, t = getChirp(f0,f1,t0,amp,Fs,delay)
    i = h.Vector().record(h.IClamp[0]._ref_i)
    stim.amp = 0
    stim.dur = (t0+delay*2) * Fs + 1
    I.play(stim._ref_amp, t)
    ## run simulation
    h.celsius = 34
    h.tstop = (t0+delay*2) * Fs + 1
    h.run()
    v_trim = [v for v, T in zip(soma_v, time) if int((delay+2)*1000) < T < int(delay*t0*1000)] 
    i_trim = [x for x, T in zip(i,time) if int((delay+2)*1000) < T < int(delay*t0*1000)] 
    time_trim = [T for v, T in zip(soma_v, time) if int((delay+2)*1000) < T < int(delay*t0*1000)] 
    current = i_trim
    v = v_trim 
    #current = current[int(delay*sampr - 0.5*sampr+1):-int(delay*sampr- 0.5*sampr)] 
    current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
    current = current - np.mean(current) 
    #v = v[int(delay*sampr - 0.5*sampr)+1:-int(delay*sampr - 0.5*sampr)] 
    v = np.hstack((np.repeat(v[0],int(delay*sampr)), v, np.repeat(v[-1], int(delay*sampr)))) 
    v = v - np.mean(v) 
    f_current = (fft(current)/len(current))[0:int(len(current)/2)] 
    f_cis = (fft(v)/len(v))[0:int(len(v)/2)] 
    z = f_cis / f_current 
    phase = np.arctan2(np.imag(z), np.real(z))
    Freq       = np.linspace(0.0, sampr/2.0, len(z))
    zamp = abs(z)
    ind = np.argmin(np.square(Freq-f))
    temp_dict = {'zAmp' : zamp[ind], 'zPhase' : phase[ind]}
    return_dict[f] = temp_dict

# try:
#     parser = argparse.ArgumentParser(description = '''Run impedance validation''')
#     parser.add_argument('--freq_file', nargs='?', type=str, default='data/noise_freqs.json',
#                         help='''json file containinf frequencies to test''')
#     parser.add_argument('outfile', metavar='outfile', type=str,
#                         help='a file to save output data')
#     parser.add_argument('--amp', nargs='?', type=float, default=0.01)
#     parser.add_argument('--t0', nargs='?', type=int, default=5)
#     parser.add_argument('--sampr', nargs='?', type=float, default=40e3)
#     parser.add_argument('--delay', nargs='?', type=int, default=5)
#     parser.add_argument('--poolSize', nargs='?', type=int, default=1)
#     args = parser.parse_args()
# except:
#     os._exit(1)

# create output dictionary 
manager = multiprocessing.Manager()
impedance = manager.dict()


freq_file = 'data/standard_chirp_freqs.json'
with open(freq_file, 'rb') as fileObj:
    freqs = json.load(fileObj)
# freqs = np.linspace(0.5, 20, 60)

amp = 0.01 #0.02 #args.amp 
t0 = 5 #args.t0 
sampr = 40e3 #args.sampr
delay = 5 #args.delay
poolSize = 60 #args.poolSize
outfile = 'data/chirp_freq_validation_amp01.json'

# create tuple of input data 
data = []
for freq in freqs:
    data.append([freq, amp, t0, sampr, delay, impedance])
data = tuple(data)

# run over pool size
p = multiprocessing.Pool(poolSize)
p.map(runInputValidation, data)

with open(outfile, 'w') as fileObj:
    json.dump(dict(impedance), fileObj)
