#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 12:32:21 2021

@author: sb16165

Handles particle calorimetry information
"""
import numpy as np


def TotalEnergy(EMEnergy, hadronEnergy, hadronEnergyVector, geometry, f=1, paRatio=20, correctEM=True, correctH=True):
    """
    Sums the energy deposited in the Hadron and EM Calorimeter including
    corrections made to account for leekage missing energy etc.
    ---- Parameters ----
    paRatio                 : ratio of passive/active material in the Hcal,
                              taken as ratio of the entire depth and the
                              depth of the calorimeter part
    CorrectEM               : should the EM corrections be applied?
    CorrectH                : should the hadronic correcitons be applied?
    EMCorrection            : correction due to potential energy leekage in ECal
    HCorrection             : correction to due missing ionisation in Hcal
    total                   : total energy distribution 
    --------------------    
    """
    
    if correctH is False:
        paRatio = 1
        HCorrection = 0
    else:
        HCorrection = HCalCorrection(hadronEnergyVector, geometry)
    
    if correctEM is True:
        EMCorrection = EMCalCorrection(EMEnergy, geometry, f)
    else:
        EMCorrection = 0
    
    total = EMEnergy + EMCorrection + hadronEnergy * paRatio + HCorrection
    
    return total


def EMCalCorrection(energy, geometry, f=1):
    """
    Corrects the energy deposited in the EM caloirmeter by estimating the amount of energy
    leekage due to the calorimeter length being too short. Note the correction
    is a empirical guess of how much energy should have been deposited if the
    depth of the calorimeter was apppropriate. This is done using the exponential
    model for the energy deposition and that the smallest energy deposited is
    the critical energy multiplied by some factor (energy_critical_corr).
    ---- Parameters ----
    f                       : factor to adjust t_max by, should be 1 for electrons/positrons and -1 for protons
    energy_critical         : citcial energy for the given material
    t_em                    : depth of calorimeter in units of X0
    t_max                   : depth at which most shower daughters are created
    t_95                    : depth at which the whole shower energy is deposited
    energy_critical_corr    : the critical energy, adjusted to account for the leekage (purely empirical)
    --------------------
    """
    energy_critical = 0.610 / (geometry.CsI.Z + 1.24)
    
    t_em = 0.3 / geometry.CsI.X0
    
    t_max = np.log( energy/energy_critical ) - f * 0.5
    
    t_95 = t_max + 0.08*geometry.CsI.Z + 9.6
    
    energy_critical_corr = (t_95 / t_max) * energy_critical
    
    return energy_critical_corr * ( 1 - np.exp(t_95) ) / ( 1 - np.exp(t_em) )


def HCalCorrection(energyVector, geometry):
    """
    Attempted correction to account for missing energy from ionisation.
    ---- Parameters ----
    E0          : hadronic interaction cutoff energy
    hadronN     : number of hits found in the calorimeter
    --------------------
    """
    
    E0 = 1.3

    hadronN = np.array([len(evt[evt>E0]) for evt in energyVector])  # energy < E0 rejected

    return hadronN * E0


def PredictedEnergy(momentum, mass):
    """
    Calculates a predicted energy distribution using the reconstructed momenta
    and the mass of the particle (we are fortunate this is a simulation, so
    know what the particle is).
    """
    return np.sqrt(momentum**2 + mass**2)


