import argparse

parser = argparse.ArgumentParser(description = '''Run chirp stimulus simulation''')
parser.add_argument('--cellModel', nargs='?', type=str, default='HayCellMig')
parser.add_argument('--section', nargs='?', type=str, default='apic_0')
parser.add_argument('--amp', nargs='?', type=float, default=1.0)
parser.add_argument('--f0', nargs='?', type=float, default=0.5)
parser.add_argument('--f1', nargs='?', type=float, default=20.0)
parser.add_argument('--delay', nargs='?', type=int, default=3)
parser.add_argument('--t0', nargs='?', type=int, default=20)
parser.add_argument('--offset', nargs='?', type=float, default=0.0)
parser.add_argument('--blockIh', nargs='?', type=str, default=None)
parser.add_argument('--slopeFactor', nargs='?', type=float, default=None)
parser.add_argument('--saveTraces', nargs='?', type=str, default=None)
parser.add_argument('--vhalfl', nargs='?', type=float, default=None)
parser.add_argument('--ih_gbar_factor', nargs='?', type=float, default=None)
parser.add_argument('--TTX', nargs='?', type=str, default=None)
parser.add_argument('--blockSKv3', nargs='?', type=str, default=None)
parser.add_argument('--blockSKE', nargs='?', type=str, default=None)
parser.add_argument('--blockLVACa', nargs='?', type=str, default=None)
parser.add_argument('--blockIm', nargs='?', type=str, default=None)
parser.add_argument('--blockTASK', nargs='?', type=str, default=None)
parser.add_argument('--tauFactor', nargs='?', type=float, default=None)
parser.add_argument('--morph_file', nargs='?', type=str, default=None)
args = parser.parse_args()

from getCells import M1Cell   
s = M1Cell()  
soma_seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
seg = s.net.cells[0].secs['apic_0']['hObj'](0.5)
from neuron import h

from chirpUtils import getRampChirp, fromtodistance
stim = h.IClamp(seg)
from pylab import fft
import numpy as np 
from scipy.signal import find_peaks, hilbert
import json 
import os

try:
    os.makedirs('ramp_data/')
    os.makedirs('ramp_traces/')
except:
    pass

if args.blockIh:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.gbar_hd = 0
            except:
                pass
if args.blockIm:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.gImbar_Im = 0
            except:
                pass
if args.vhalfl:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.hd.vhalfl = args.vhalfl
            except:
                pass 
if args.blockLVACa:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.Ca_LVAst.gCa_LVAstbar = 0
            except:
                pass
if args.ih_gbar_factor:
    for sec in h.allsec():
        for sec in sec.allseg():
            try:
                seg.gbar_hd = seg.gbar_hd * args.ih_gbar_factor
            except:
                pass
if args.tauFactor:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.hd.tauFactor = args.tauFactor
            except:
                pass
if args.blockTASK:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.hd.lkFactor = 0
            except:
                pass
if args.TTX:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.NaTa_t.gNaTa_tbar = 0
            except:
                pass
if args.blockSKv3:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.SKv3_1.gSKv3_1bar = 0
            except:
                pass
if args.blockSKE:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.SK_E2.gSK_E2bar = 0
            except:
                pass

dist = fromtodistance(seg, soma_seg)
amp = args.amp #0.02 
t0 = args.t0 #20
delay = args.delay
Fs = 1000
sampr = 40e3 
f0 = args.f0
f1 = args.f1
soma_v = h.Vector().record(soma_seg._ref_v) 
seg_v = h.Vector().record(seg._ref_v) 
time = h.Vector().record(h._ref_t)
if not args.slopeFactor:
    I, t = getRampChirp(f0, f1, t0, amp, Fs, delay, offset=args.offset)
else:
    slope = args.slopeFactor #1 / (t0 * args.slopeFactor)
    I, t = getRampChirp(f0, f1, t0, amp, Fs, delay, offset=args.offset, slope=slope)
i = h.Vector().record(h.IClamp[0]._ref_i)
# ih = h.Vector().record(soma_seg.hd._ref_i)
# inat = h.Vector().record(soma_seg.NaTa_t._ref_ina)
# inap = h.Vector().record(soma_seg.Nap_Et2._ref_ina)
# iske2 = h.Vector().record(soma_seg.SK_E2._ref_ik)
# iskv3 = h.Vector().record(soma_seg.SKv3_1._ref_ik)
# icahva = h.Vector().record(soma_seg.Ca_HVA._ref_ica)
# icalva = h.Vector().record(soma_seg.Ca_LVAst._ref_ica)
# ikpst = h.Vector().record(soma_seg.K_Pst._ref_ik)
# iktst = h.Vector().record(soma_seg.K_Tst._ref_ik)
stim.amp = 0
stim.dur = (t0+delay*2) * Fs + 1
I.play(stim._ref_amp, t)
## run simulation
h.celsius = 34
h.tstop = (t0+delay*2) * Fs + 1
print('running ' + args.cellModel + ' ' + args.section + ' f0-' + str(round(args.f0)) + ' f1-' + str(round(args.f1)))
h.run()
v_trim = [v for v, T in zip(seg_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
i_trim = [x for x, T in zip(i,time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
time_trim = [T for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
current = i_trim
v = v_trim 
#current = current[int(delay*sampr - 0.5*sampr+1):-int(delay*sampr- 0.5*sampr)] 
current = np.hstack((np.repeat(current[0],int(delay*sampr)),current, np.repeat(current[-1], int(delay*sampr)))) 
current = current - np.mean(current) 
#v = v[int(delay*sampr - 0.5*sampr)+1:-int(delay*sampr - 0.5*sampr)] 
v = v - np.mean(v) 
v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 
f_current = (fft(current)/len(current))[0:int(len(current)/2)] 
f_cis = (fft(v)/len(v))[0:int(len(v)/2)] 
z = f_cis / f_current 
phase = np.arctan2(np.imag(z), np.real(z))
Freq       = np.linspace(0.0, sampr/2.0, len(z))
zRes       = np.real(z)
zReact     = np.imag(z)
zamp = abs(z)
mask = (Freq >= 0.5) & (Freq <= f1)
zResAmp    = np.max(zamp)
zResFreq   = Freq[np.argmax(zamp)]
Qfactor    = zResAmp / zamp[0]
fVar       = np.std(zamp) / np.mean(zamp)
peak_to_peak = np.max(v) - np.min(v)
## smoothing
# bwinsz = 10
# fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
# zamp = convolve(zamp,fblur,'same')
# phase = convolve(phase, fblur, 'same')
Freq, zamp, phase, zRes, zReact, z = Freq[mask], zamp[mask], phase[mask], zRes[mask], zReact[mask], z[mask]
freqsIn = np.argwhere(phase > 0)
if len(freqsIn) > 0:
    ZinSynchFreq = Freq[freqsIn[-1]]
    ZinPhaseL = np.trapz([float(phase[ind]) for ind in freqsIn], 
        [float(Freq[ind]) for ind in freqsIn])
else:
    ZinSynchFreq = 0 
    ZinPhaseL = 0

out = {'Freq' : list(Freq),
    'ZinRes' : list(zRes),
    'ZinReact' : list(zReact),
    'ZinAmp' : list(zamp),
    'ZinPhase' : list(phase),
    'ZinSynchFreq' : float(ZinSynchFreq),
    'ZinPhaseL' : float(ZinPhaseL),
    'ZinResAmp' : float(zResAmp),
    'ZinResFreq' : float(zResFreq),
    'QfactorIn' : float(Qfactor),
    'fVarIn' : float(fVar)}#,
    # 'zin' : list(z)}

v_trim = [v for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
v = v_trim 
v = v - np.mean(v) 
v = np.hstack((np.repeat(0,int(delay*sampr)), v, np.repeat(0, int(delay*sampr)))) 
f_cis = (fft(v)/len(v))[0:int(len(v)/2)] 
z = f_cis / f_current 
phase = np.arctan2(np.imag(z), np.real(z))
Freq       = np.linspace(0.0, sampr/2.0, len(z))
zRes       = np.real(z)
zReact     = np.imag(z)
zamp = abs(z)
mask = (Freq >= 0.5) & (Freq <= f1)
zResAmp    = np.max(zamp)
zResFreq   = Freq[np.argmax(zamp)]
Qfactor    = zResAmp / zamp[0]
fVar       = np.std(zamp) / np.mean(zamp)
peak_to_peak = np.max(v) - np.min(v)
## smoothing
# bwinsz = 10
# fblur = np.array([1.0/bwinsz for i in range(bwinsz)])
# zamp = convolve(zamp,fblur,'same')
# phase = convolve(phase, fblur, 'same')
Freq, zamp, phase, zRes, zReact, z = Freq[mask], zamp[mask], phase[mask], zRes[mask], zReact[mask], z[mask]
freqsIn = np.argwhere(phase > 0)
if len(freqsIn) > 0:
    ZinSynchFreq = Freq[freqsIn[-1]]
    ZinPhaseL = np.trapz([float(phase[ind]) for ind in freqsIn], 
        [float(Freq[ind]) for ind in freqsIn])
else:
    ZinSynchFreq = 0 
    ZinPhaseL = 0

out['ZcRes'] = list(zRes)
out['ZcReact'] = list(zReact)
out['ZcAmp'] = list(zamp)
out['ZcPhase'] = list(phase)
out['ZcSynchFreq'] = float(ZinSynchFreq)
out['ZcPhaseL'] = float(ZinPhaseL)
out['ZcResAmp'] = float(zResAmp)
out['ZcResFreq'] = float(zResFreq)
out['QfactorC'] = float(Qfactor)
out['fVarC'] = float(fVar)
out['dist'] = dist
# out['zc'] = list(z)

allspks, _ = find_peaks(v_trim, 0)

datadir = 'subramp_data/'
tracedir = 'subramp_traces/'
if len(allspks):
    stim_pks, stim_amps = find_peaks(i.as_numpy())
    stim_troughs, trough_amps = find_peaks(i.as_numpy() * -1)
    soma_np = soma_v.as_numpy()
    seg_np = seg_v.as_numpy()
    iphase = np.angle(hilbert(i.as_numpy()), deg=True)
    time_np = time.as_numpy()
    lags = []
    freq = []
    angles = []
    for peakt, finish, nextt in zip(stim_pks[:-1], stim_troughs[:-1], stim_pks[1:]):
        start = peakt - (finish-peakt) 
        spks, _ = find_peaks(soma_np[start:finish], 0)
        if len(spks):
            lags.append(time_np[start+spks[0]]-time_np[peakt])
            angles.append(iphase[start+spks[0]])
        else:
            lags.append(np.nan)
            angles.append(np.nan)
        freq.append(1 / ((time_np[finish]-time_np[start])/1000))
    out['lags'] = lags
    out['freq'] = freq
    out['angles'] = angles 
    datadir = 'ramp_data/'
    tracedir = 'ramp_traces/'
if args.blockIh and args.blockSKE:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockIhSKE.json'
elif args.blockIh:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockIh.json'
elif args.vhalfl:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_vhalfl_' + str(round(args.vhalfl)) + '.json'
elif args.ih_gbar_factor:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_gbarfactor_' + str(round(args.ih_gbar_factor, 2)) + '.json'
elif args.blockSKE:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockSKE.json'
elif args.blockSKv3:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockSKv3.json'
elif args.blockLVACa:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockLVACa.json'
elif args.blockIm:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockIm.json'
elif args.blockTASK:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockTASK.json'
elif args.tauFactor:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_tauFactor_' + str(round(args.tauFactor,3)) + '.json'
elif args.TTX:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_TTX.json'
elif args.morph_file:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + 'morphv1.json'
else:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '.json'

# with open(filename, 'w') as fileObj:
#     json.dump(out, fileObj)

if args.saveTraces:
    traces = {'soma_v' : soma_v.as_numpy(),
            'i' : i.as_numpy(),
            'time' : time.as_numpy()}
    if args.blockIh and args.blockSKE:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockIhSKE.npy'
    elif args.blockIh:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockIh.npy'
    elif args.blockIm:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockIm.npy'
    elif args.blockTASK:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockTASK.npy'
    elif args.tauFactor:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_tauFactor_' + str(round(args.tauFactor,3)) + '.json'
    elif args.vhalfl:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_vhalf_' + str(round(args.vhalfl)) + '.npy'
    elif args.ih_gbar_factor:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_gbarfactor_' + str(round(args.ih_gbar_factor,2)) + '.npy'
    elif args.blockSKE:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockSKE.npy'
    elif args.blockLVACa:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockLVACa.npy'
    elif args.TTX:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockTTX.npy'
    elif args.blockSKv3:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '_blockSKv3.npy'
    elif args.morph_file:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + 'morphv1.npy'
    else:
        tracefile = tracedir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_s_' + str(args.slopeFactor) + '_t_' + str(args.t0) + '.npy'
    # with open(tracefile, 'wb') as fileObj:
    #     np.save(fileObj, traces)

# from matplotlib import pyplot as plt
# fig2, axs2 = plt.subplots(3,3,sharex=True)
# axs2[0][0].plot(ih)
# axs2[0][0].set_title('ih')
# axs2[0][1].plot(inat)
# axs2[0][1].set_title('inat')
# axs2[0][2].plot(inap)
# axs2[0][2].set_title('inap')
# axs2[1][0].plot(iske2)
# axs2[1][0].set_title('iske2')
# axs2[1][1].plot(iskv3)
# axs2[1][1].set_title('iskv3')
# axs2[1][2].plot(icahva)
# axs2[1][2].set_title('icahva')
# axs2[2][0].plot(icalva)
# axs2[2][0].set_title('icalva')
# axs2[2][1].plot(ikpst)
# axs2[2][1].set_title('ikpst')
# axs2[2][2].plot(iktst)
# axs2[2][2].set_title('iktst')