#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:05:12 2021

@author: sb16165
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

import Master
import Tracker

data = Master.data("out_5a.root")
geometry = Master.Geometry(0.5)


emE = data.E_EM
hadronE = data.E_Hadron

emEVector = data.EVector_EM
hadronEVector = data.EVector_Hadron

emEVector = np.array([np.reshape(i, (20, 4) ) for i in emEVector])
hadronEVector = np.array([np.reshape(i, (10, 2) ) for i in hadronEVector])


#plasma_energy = np.sqrt( (rho * Z)/(1000 * A) ) * 28.816 #eV

#density_correction = np.log(plasma_energy/ I) + log(v * gamma) - 0.5

#scattering_correction = 2 * np.log(2) - (v**2 / 12) * (23 + 14 / (tau + 2))