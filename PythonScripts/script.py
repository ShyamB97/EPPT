#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:43:11 2021

@author: sb16165

Main script, will act somewhat like an analyser module in lArsoft.
"""

import numpy as np
import matplotlib.pyplot as plt

import Master
import Tracker


### OUTDATED ###
z = 5 + 5 + 0.3 - 0.3 # distance between Drift chambers
B = 0.5 # magnetic field in Telsa
q = 1.6E-19  # charge of the particle in Coulombs
xPres = 1E-4  # precision of x Position in meters
nEvents = 1000

### OUTDATED ###
def MomentumCalculation(hits1, hits2):
    """
    Calculates momentum by finding how much the particle bends in the magnetic field.
    ---- Parameters ----
    hits(i) : hits from ith drift chamber
    x       : displacement along x due to the bending
    l       : distance between last hit of hits1 nd first hit of hits2
    r       : radius of delfeciton
    p       : momentum, p = mv = qBr
    sig_r   : uncertianty in r
    sig_p   : uncertainty in p
    --------------------
    Makes use of global vairables (constants).
    """
    x = abs( (hits2[4] - hits1[4]) * xPres )
    
    l = np.sqrt( ( (hits2[0] - hits1[4]) * xPres )**2 + (9.6)**2 )
    
    r = np.sqrt( ((l**2) * z ) / (4 * abs(x) ) )
    
    p = q * B * r
    
    p = p * (3E8 / 1.6E-10) # convert to GeV/c

    sig_r = RadiusUncertainty(x, l)
    
    sig_p = sig_r * (p/r)

    return p, sig_p

### OUTDATED ###
def RadiusUncertainty(x, l, sig_x = xPres):
    """
    Calculates the uncertainty in defleciton redius r.
    Only depends on the precision of x.
    ---- Parameters ----
    x       : see MomentumCalculation
    l       : see MomentumCalculation
    sig_x   : uncertainty in x (assumed)
    --------------------
    """
    return sig_x * np.sqrt( (z/x) * ( ( 2*(l**2 - 9.6**2) + (1/16) * (l/x)**2 ) ) )  # see notes



data = Master.data("out_1.root")
geometry = Master.Geometry() # get detector geometry info

# get drift chamber hits
hits_1 = data.DC1_Hits
hits_2 = data.DC2_Hits

# calculate the particle momentum for each event
r = Tracker.BendingRadius(hits_1, hits_2, geometry)
p = Tracker.Momentum(1.6E-19, geometry.B, r)
print(np.mean(p))

cutoff = 1000 # momentum value to cutoff, likely due to poor tracking
p = p[p < 1000]

plt.hist(p, bins=50)



"""
momenta = []
resolution = []
for i in range(nEvents):
    p, sig_p = MomentumCalculation(d.DC1_Hits.x[i] , d.DC2_Hits.x[i])
    momenta.append(p)
    resolution.append(sig_p)

bins, patches, _ = plt.hist(momenta, 100)
binWidth = (patches[-1] - patches[0]) / len(patches)
plt.xlabel("Momentum (GeV)")
plt.ylabel("Frequency (bin width:" + str(round(binWidth, 2)) + " GeV)")
plt.title("Beam momentum 200 GeV, B field " + str(B) + "T")


# Some values of Resolution are very large, so cut them from the plot for convience.
resPlot = []
for i in range(len(resolution)):
    if(resolution[i] < 100):
        resPlot.append(resolution[i])

#plt.hist(resPlot, 100)


print("mean Momentum (GeV): " + str(np.mean(momenta)) + " +- " + str(np.std(momenta)/nEvents) )
print("mean Resolution (GeV): " + str(np.mean(resolution)) + " +- " + str(np.std(resolution)/nEvents) )
"""

"""
DepositedEnergy = (HC_Energy + EC_Energy) / 1000 # GeV

muon_Mass = 0.105 # GeV

momentaFromCalorimeter = np.sqrt(DepositedEnergy**2 - muon_Mass**2)

bins, patches, _ = plt.hist(DepositedEnergy, 100)
binWidth = (patches[-1] - patches[0]) / len(patches)
plt.xlabel("Deposited energy (GeV)")
plt.ylabel("Frequency (bin width:" + str(round(binWidth, 2)) + " GeV)")

"""
"""
y, binEdges = np.histogram(momenta, 50)

binCenters = 0.5*(binEdges[1:]+binEdges[:-1])

yerr, _ = np.histogram(momenta, 50, weights=resolution)

plt.bar(binCenters, y, width=1, yerr=yerr)
"""
