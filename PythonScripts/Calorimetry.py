#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 12:32:21 2021

@author: sb16165

Handles particle calorimetry information
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

import Master

def TotalEnergy(EMEnergy, HadronEnergy):
    """
    Just sums the energy deposited in the Hardon and EM Calorimeter
    """
    return EMEnergy + HadronEnergy


import Tracker # remove once done testing


ArX0 = 117.621 # m

EcAr = 0.710 / (18 + 0.92) # not exactly

CsIX0 = 1.860 #cm

CsIZ = 55 + 53 # Cs + I

Ec = 0.610 / (CsIZ + 1.24)

PbX0 = 5.613 #mm

em_cell_z = 30 # cm

t = 30 / 1.860

data = Master.data("out_5a.root")
geometry = Master.Geometry(0.5)

emE = data.E_EM / 1000
hadronE = data.E_Hadron / 1000

emEVector = data.EVector_EM / 1000
hadronEVector = data.EVector_Hadron / 1000

"""
im = 0
for i in range(len(emEVector)):
    im = im + np.reshape(emEVector[i], (20, 4))

im = im / 1000
plt.imshow(im)
"""

#eDrift = 2 * EcAr * np.exp(-geometry.DC1Size.z*100 / ArX0)

t_c = np.log(emE / Ec)
x_c = t_c * CsIX0

energy = Ec * np.exp(t - t_c)

#energy = energy + hadronE + emE

#N_e = np.array([len(i[i > 0]) for i in emEVector])
#N_h = np.array([len(i[i > 0]) for i in hadronEVector])

#energy = (N_e / 2) * Ec

#dEdx = emE/CsIX0

#f = dEdx - N_e


#emE = np.exp(-t) * emE

#energy = TotalEnergy(emE, hadronE)


#plt.hist(energy, 50)

#plt.hist(emE, 50)
#plt.hist(hadronE, 50)
