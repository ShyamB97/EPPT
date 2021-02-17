#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 10:56:56 2021

@author: sb16165
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import log10, floor

import Master
import Tracker
import Calorimetry


def round_to(x, y):
    """
    Rounds x to the 1st significant figure of y
    """
    return round(x, -int(floor(log10(abs(y)))))


def GaussianFit(data, title=""):
    """
    Holds code for fitting gaussian curves to data.
    ---- Parameters ----
    y           : histogram bin heights = number of items in the bin
    binEdges    : right edge values of the bins
    x           : bin centers
    x_width     : bin width
    y_err       : 1sigma satistical errors per bin
    popt        : optimised parameters from the fit
    cov         : covariance matrix for the optimsed parameters
    x_int       : interpolated values of x
    y_int       : interpolated expected value of y i.e. value of y model predicts
    --------------------
    """
    y, binEdges = np.histogram(data, 50)
    x = (binEdges[:-1] + binEdges[1:]) / 2
    x_width = (x[-1] - x[0]) / len(x)
    y_err = np.sqrt(y)  # items in a bin should follow the Poisson distribution

    # calculate optimal fit parameters and covariance matrix using least squares method
    popt, cov = curve_fit(Gaussian, x, y, [np.mean(data), np.std(data), 10])

    # plot data
    plt.bar(x, y, x_width, yerr=y_err, color="blue", edgecolor="black", capsize=3, ecolor="black")
    
    text1 = "Mean (GeV): " + str( round_to(popt[0], cov[0, 0]) ) + " $\pm$ " + str( round_to(cov[0, 0], cov[0, 0]) )

    text2 = "Standard deviation (GeV): " + str( round_to(popt[1], cov[1, 1]) ) + " $\pm$ " + str( round_to(cov[1, 1], cov[1, 1]) )

    text = '\n'.join((text1, text2))

    # plot gaussian fit
    x_int = np.linspace(x[0], x[-1], 10*len(x))  # interpolate data
    y_int = Gaussian(x_int, *popt)
    plt.plot(x_int, y_int, label="Gaussian fit", color="red")


    plt.annotate(text, xy=(0.025, 0.8), xycoords='axes fraction')

    # plot options
    plt.legend()
    plt.xlabel("Energy (GeV)")
    plt.ylabel("Number of events (bin width=" + str(round(x_width, 2)) + " GeV)")
    plt.title(title)
    #plt.title("Beam momentum 100GeV, magnetic field " + str(geometry.B) + "T.")
    
    # return some results, mean, standard deviation, amplitude
    return [popt[0], cov[0, 0]], [popt[1], cov[1, 1]], [popt[2], cov[2, 2]]


def Gaussian(x, mu, sigma, a):
    """
    Gaussian function with modulated amplitude.
    ---- Parameters ----
    mu          : mean
    sigma       : standrad deviation
    a           : amputlide
    --------------------
    """
    amplitude = a / ( sigma * np.sqrt(2 * np.pi) )
    u = (x - mu) / sigma
    return amplitude * np.exp( -0.5 * (u**2) )


def Plot(data, bins=50, xlabel="", title=""):
    bins, edges, _ = plt.hist(data, bins, color="blue", edgecolor="black")
    binWidth = round((edges[-1] - edges[0]) / len(edges), 2)
    plt.xlabel(xlabel)
    plt.ylabel("Number of events (bin width=" + str(binWidth) + " GeV)")
    plt.title(title)


def PlotEnergies():
    plt.figure(2)

    xlabel = "energy deposited (GeV)"

    plt.subplot(121)
    Plot(emE, 50, xlabel, "Electromagentic Calorimeter")


    plt.subplot(122)
    Plot(hE, 50, xlabel, "Hadronic Calorimeter")


### MAIN CODE ###
data = Master.data("out_5b.root")
geometry = Master.Geometry(0.5)
mass = 0.98

hits_1 = data.DC1_Hits # get the hits before the field
hits_2 = data.DC2_Hits # get the hits after the field
r = Tracker.BendingRadius(hits_1, hits_2, geometry) # compute the bending radius
p = Tracker.Momentum(1, geometry.B, r) # get the momentum distribution of the events

# For proton data, momentum calculation is less reliable, remove anomolous data
p = p[p > 80]
p = p[p < 120]

# get total energy 
emE = data.E_EM
hE = data.E_Hadron

# get hadron energy vector
hEVector = data.EVector_Hadron

# energy distribuion from momentum i.e. no calorimetry
predicted_energy = Calorimetry.PredictedEnergy(p, mass)

# energy for full corrections, f=1 for positrons, f=-1 for protons
energy_allCorrections = Calorimetry.TotalEnergy(emE, hE, hEVector, geometry, f=-1)

# energy with no correction
energy_noCorrection = emE + hE

# only em correction
energy_EMCorrection = Calorimetry.TotalEnergy(emE, hE, hEVector, geometry, correctH=False, f=-1)

# only hadronic correction
energy_HCorrection = Calorimetry.TotalEnergy(emE, hE, hEVector, geometry, correctEM=False, f=-1)


# plot data, fit gaussains to get standrad deviation i.e. resoultion. Should probably use a better fitting function
plt.figure(5)

plt.subplot(231)
GaussianFit(predicted_energy, "Predicted energy")
plt.subplot(232)
GaussianFit(energy_noCorrection, "Total deposited energy")
plt.subplot(233)
GaussianFit(energy_EMCorrection, "Total energy + EM corrections")
plt.subplot(234)
GaussianFit(energy_HCorrection, "Total energy + hadronic corrections")
plt.subplot(235)
GaussianFit(energy_allCorrections, "Total energy + all corrections")
