from getCells import M1Cell   
s = M1Cell()  
seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
from chirpUtils import getChirpLog, getChirp, getNoise
from neuron import h 
stim = h.IClamp(seg)
from pylab import fft, convolve
import numpy as np 
# import argparse
import os
from sklearn.metrics import mean_squared_error
import json 
import multiprocessing