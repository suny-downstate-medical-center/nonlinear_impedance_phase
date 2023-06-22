# Introduction
This repository contains code for simulating neuronal responses to oscillatory stimuli and 
computing an analog to electrical impedance phase that can be used for nonlinear membrane 
potential responses.
Simulating these responses in a theta-resonant neocortical thick-tufted layer 5b pyramidal neuron,
we found different phase shifts during excitation and inhibition for large amplitude, subthreshold stimuli.
We identified two patterns of spiking in response to continuing sinusoidal stimulus: 
Sinusoidal inputs produced *phase retreat*, where action potentials occurred progressively later in cycles of the input stimulus, resulting from adaptation.
Sinusoidal inputs with increasing amplitude over cycles produced *phase advance*, where action potentials occurred progressively earlier in cycles of the input stimulus.
These results are described in [Neuronal phase shifts differ for excitation vs. inhibition: a computer modeling study](https://www.biorxiv.org/content/10.1101/2023.03.20.533519v1).

# Basic Usage
Make sure you have installed [NEURON](https://www.neuron.yale.edu/neuron/) and [NETPYNE](http://netpyne.org/).

Clone this repository using 'git'
```
git clone https://github.com/suny-downstate-medical-center/nonlinear_impedance_phase.git
```

Compile the mod files for the Hay et al. 2011 model:
```
cd models/Hay/
nrnivmodl mod 
cd ../../
```

You can run an example simulation of subthreshold chirp stimulation that elicits 
V<sub>memb</sub> responses in the nonlinear regime:
```
python3 -i subthreshold_example.py 
```

You can run an example simulation of suprathreshold sinusoidal stimulation that elicits 
phase retreat:
```
python3 -i phase_retreat_example.py 
```

You can run an example simulation of suprathreshold sinusoidal stimulation whose amplitude increases linearly with time that elicits 
phase advance:
```
python3 -i phase_advance_example.py 
```

These are simplified, static programs designed to serve as examples.  
Simulations from the paper can be run with *asymChirp.py* (subthreshold), *chirpLinear.py* (suptratheshold sin), and *chirpRamp.py* (ramped suprathreshold sin), respectively.  
These programs allow for command line arguments that can block conductances, change stimulus frequencies or stimulus location , etc.