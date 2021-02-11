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

