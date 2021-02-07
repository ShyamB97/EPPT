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

data = Master.data("out_5b.root")
geometry = Master.Geometry(0.5)

emE = data.E_EM / 1000
hadronE = data.E_Hadron / 1000


plt.hist(emE, 50)
plt.hist(hadronE, 50)