import time as systime
start_time = systime.time()
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
parser.add_argument('--saveTraces', nargs='?', type=str, default=None)
parser.add_argument('--vhalfl', nargs='?', type=float, default=None)
parser.add_argument('--ih_gbar_factor', nargs='?', type=float, default=None)
parser.add_argument('--TTX', nargs='?', type=str, default=None)
parser.add_argument('--blockSKv3', nargs='?', type=str, default=None)
parser.add_argument('--blockSKE', nargs='?', type=str, default=None)
args = parser.parse_args()


if args.cellModel == 'M1Cell':
    from getCells import M1Cell   
    s = M1Cell()  
    soma_seg = s.net.cells[0].secs['soma']['hObj'](0.5)  
    seg = s.net.cells[0].secs[sys.argv[-1]]['hObj'](0.5)
    from neuron import h
elif args.cellModel == 'HayCellMig':
    from getCells import HayCellMig
    cell, _ = HayCellMig()
    soma_seg = cell.soma[0](0.5)
    sec_name = args.section.split('_')[0]
    sec_num = args.section.split('_')[1]
    execstr = 'seg = cell.' + sec_name + '[' + sec_num + '](0.5)'
    # seg = soma_seg
    exec(execstr)
    from neuron import h
elif args.cellModel == 'RichHuman':
    from getCells import RichHuman
    h, trunk = RichHuman()
    soma_seg = h.filament_100000042[0](0.5)
    seg = h.filament_100000042[trunk[int(len(trunk)/2)]](0.5)

from chirpUtils import getChirp, fromtodistance
stim = h.IClamp(seg)
from pylab import fft
import numpy as np 
from scipy.signal import find_peaks, hilbert
import json 
import os

try:
    os.makedirs('supra_data/')
    os.makedirs('supra_traces/')
except:
    pass

if args.blockIh:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.gbar_hd = 0
            except:
                pass
if args.vhalfl:
    for sec in h.allsec():
        for seg in sec.allseg():
            try:
                seg.hd.vhalfl = args.vhalfl
            except:
                pass 

if args.ih_gbar_factor:
    for sec in h.allsec():
        for sec in sec.allseg():
            try:
                seg.gbar_hd = seg.gbar_hd * args.ih_gbar_factor
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
I, t = getChirp(f0, f1, t0, amp, Fs, delay, offset=args.offset)
i = h.Vector().record(h.IClamp[0]._ref_i)
ih = h.Vector().record(soma_seg.hd._ref_i)
inat = h.Vector().record(soma_seg.NaTa_t._ref_ina)
inap = h.Vector().record(soma_seg.Nap_Et2._ref_ina)
iske2 = h.Vector().record(soma_seg.SK_E2._ref_ik)
iskv3 = h.Vector().record(soma_seg.SKv3_1._ref_ik)
icahva = h.Vector().record(soma_seg.Ca_HVA._ref_ica)
icalva = h.Vector().record(soma_seg.Ca_LVAst._ref_ica)
ikpst = h.Vector().record(soma_seg.K_Pst._ref_ik)
iktst = h.Vector().record(soma_seg.K_Tst._ref_ik)
stim.amp = 0
stim.dur = (t0+delay*2) * Fs + 1
I.play(stim._ref_amp, t)
## run simulation
h.celsius = 34
h.tstop = (t0+delay*2) * Fs + 1
print('running ' + args.cellModel + ' ' + args.section + ' f0-' + str(round(args.f0)) + ' f1-' + str(round(args.f1)))
h.run()
v_trim = [v for v, T in zip(soma_v, time) if int((delay)*1000) < T < int((delay+t0)*1000)] 
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
f = np.hstack((np.repeat(0,int(delay*sampr)), np.linspace(f0,f1,len(v_trim)),np.repeat(0,int(delay*sampr))))

iphase = np.angle(hilbert(current))
allspks, _ = find_peaks(v_trim, 0)
pks, _ = find_peaks(v)
trghs, _ = find_peaks(v*-1)
ipks, _ = find_peaks(current)
itrghs, _ = find_peaks(current*-1)
trghs = [tr for tr in trghs if tr > pks[0]]
f_minus = None
phi_minus = None
asym = -np.min(v)-np.max(v)
peak_to_peak = np.max(v) - np.min(v)
v_init = v_trim[0]

if len(allspks):
    phi_plus = []
    f_plus = []
    for peakt, finish, nextt in zip(ipks[:-1], itrghs[:-1], ipks[1:]):
        start = peakt - (finish-peakt) 
        spks, _ = find_peaks(v[start:finish], 0)
        if len(spks):
            phi_plus.append(iphase[peakt]-iphase[spks[0]+start])
        else:
            phi_plus.append(np.nan)
        f_plus.append(f[peakt])
    trghs, _ = find_peaks(v*-1, 0)
    trghs = [tr for tr in trghs if tr > pks[0]]
    phi_minus = []
    for trgh, itrgh in zip(trghs, itrghs):
        if iphase[trgh] < 0 and iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - (iphase[trgh] + 2*np.pi))
        elif iphase[trgh] < 0:
            phi_minus.append(iphase[itrgh]-(iphase[trgh] + 2*np.pi))
        elif iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - iphase[trgh])
        else:
            phi_minus.append(iphase[itrgh]-iphase[trgh])            
    f_minus = [f[trgh] for trgh in itrghs]
else:
    phi_plus = [iphase[ipk]-iphase[pk] for pk, ipk in zip(pks, ipks)]
    f_plus = [f[pk] for pk in pks]
    phi_minus = []
    for trgh, itrgh in zip(trghs, itrghs):
        if iphase[trgh] < 0 and iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - (iphase[trgh] + 2*np.pi))
        elif iphase[trgh] < 0:
            phi_minus.append(iphase[itrgh]-(iphase[trgh] + 2*np.pi))
        elif iphase[itrgh] < 0:
            phi_minus.append((iphase[itrgh] + 2*np.pi) - iphase[trgh])
        else:
            phi_minus.append(iphase[itrgh]-iphase[trgh])            
    f_minus = [f[trgh] for trgh in itrghs]

out = {'f_plus' : f_plus, 
        'f_minus' : f_minus, 
        'phi_plus' : phi_plus,
        'phi_minus' : phi_minus,
        'TTX' : args.TTX,
        'offset' : args.offset,
        'v_init' : v_init,
        'peak_to_peak' : peak_to_peak, 
        'asym' : asym}

datadir = 'asym_data/'
tracedir = 'asym_traces/'
if args.blockIh:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_blockIh.json'
elif args.vhalfl:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_vhalfl_' + str(round(args.vhalfl)) + '.json'
elif args.ih_gbar_factor:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_gbarfactor_' + str(round(args.ih_gbar_factor, 2)) + '.json'
elif args.TTX:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_TTX.json'
elif args.blockSKv3:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_blockSKv3.json'
elif args.blockSKE:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_blockSKE.json'
else:
    filename = datadir + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '.json'

with open(filename, 'w') as fileObj:
    json.dump(out, fileObj)

if args.saveTraces:
    traces = {'soma_v' : soma_v.as_numpy(),
            'i' : i.as_numpy(),
            'time' : time.as_numpy(),
            'ih' : ih,
            'inat' : inat,
            'inap' : inap,
            'iske2' : iske2,
            'iskv3' : iskv3,
            'icahva' : icahva,
            'icalva' : icalva,
            'ikpst' : ikpst,
            'iktst' : iktst}
    if args.blockIh:
        tracefile = tracedir  + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_blockIh.npy'
    elif args.vhalfl:
        tracefile = tracedir  + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_vhalf_' + str(round(args.vhalfl)) + '.npy'
    elif args.ih_gbar_factor:
        tracefile = tracedir  + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_gbarfactor_' + str(round(args.ih_gbar_factor,2)) + '.npy'
    elif args.TTX:
        tracefile = tracedir  + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_TTX.npy'
    elif args.blockSKv3:
        tracefile = tracedir  + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_blockSKv3.npy'
    elif args.blockSKE:
        tracefile = tracedir  + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '_blockSKE.npy'
    else:
        tracefile = tracedir  + args.cellModel + '_' + args.section + '_amp_' + str(amp) + '_offset_' + str(args.offset) + '_f0_' + str(round(args.f0)) + '_f1_' + str(round(f1)) + '.npy'
    with open(tracefile, 'wb') as fileObj:
        np.save(fileObj, traces)

from matplotlib import pyplot as plt
fig2, axs2 = plt.subplots(3,3,sharex=True)
axs2[0][0].plot(ih)
axs2[0][0].set_title('ih')
axs2[0][1].plot(inat)
axs2[0][1].set_title('inat')
axs2[0][2].plot(inap)
axs2[0][2].set_title('inap')
axs2[1][0].plot(iske2)
axs2[1][0].set_title('iske2')
axs2[1][1].plot(iskv3)
axs2[1][1].set_title('iskv3')
axs2[1][2].plot(icahva)
axs2[1][2].set_title('icahva')
axs2[2][0].plot(icalva)
axs2[2][0].set_title('icalva')
axs2[2][1].plot(ikpst)
axs2[2][1].set_title('ikpst')
axs2[2][2].plot(iktst)
axs2[2][2].set_title('iktst')

fig, axs = plt.subplots(3,1, sharex=True)
axs[0].plot(current)
axs[1].plot(v)
axs[2].plot(iphase)
for pk in ipks:
    axs[0].plot(pk, current[pk], 'k*')
    axs[2].plot(pk, iphase[pk], 'k*')
for trgh in itrghs:
    axs[0].plot(trgh, current[trgh], 'g*')
    axs[2].plot(trgh, iphase[trgh], 'g*')
for pk in pks:
    axs[1].plot(pk, v[pk], 'r*')
    axs[2].plot(pk, iphase[pk], 'r*')
for trgh in trghs:
    axs[1].plot(trgh, v[trgh], 'y*')
    if iphase[trgh] < 0:
        axs[2].plot(trgh, iphase[trgh]+2*np.pi, 'y*')
    else:
        axs[2].plot(trgh, iphase[trgh], 'y*')

# fig2, ax = plt.subplots(1,1)
# if len(allspks):
#     ax.plot(f_plus, phi_plus, '*--', label='Spike Times')
#     ax.set_ylabel(r'$\Phi$(f)$^{+}$ (rad)', fontsize=14)
# else:
#     ax.plot(f_plus, phi_plus, '*--', label='Nonlinear Upper Envelope')  
#     ax.plot(f_minus, phi_minus, '*--', label='Nonlinear Lower Envelope')
#     ax.set_ylabel(r'$\Phi$(f)$^{+/-}$ (rad)', fontsize=14)
# # with open('sub_data/HayCellMig_soma_0_amp_0.025_offset_0.0_f0_0_f1_20.json', 'rb') as fileObj:
# #     chirp_data = json.load(fileObj)
# # ax.plot(chirp_data['Freq'], chirp_data['ZinPhase'], label='Linear Response')
# ax.set_xlabel('Frequency (Hz)', fontsize=14)

# ax.legend()

