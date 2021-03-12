# testing and comparing h_harnett.mod; h_migliore.mod

def loaddll (path='.', chd=False):
    '''load is done from directory that includes the mod files and x86_64/'''
    import neuron
    if chd: cd(path)
    neuron.load_mechanisms(path)

loaddll()
from neuron import h
sec=h.Section(name='sec')
sec.insert('h15') # h_harnett.mod
sec.insert('hd')  # h_migliore.mod

print(h.linf_hd)  # access of a NMODL global
print(sec(0.5).h15.minf)  # access of a NMODL RANGE (shouldn't be a RANGE but dm)

h.rate_h15(-5.0) # seg fault
