#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 15:43:11 2021

@author: sb16165

Main script, will act somewhat like an analyser module in lArsoft.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from math import log10, floor

import Master
import Tracker


def round_to(x, y):
    """
    Rounds x to the 1st significant figure of y
    """
    return round(x, -int(floor(log10(abs(y)))))


def GaussianFit(data):
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
    
    # plot gaussian fit
    x_int = np.linspace(x[0], x[-1], 10*len(x))  # interpolate data
    y_int = Gaussian(x_int, *popt)
    plt.plot(x_int, y_int, label="Gaussian fit", color="red")    
    
    # plot options
    plt.legend()
    plt.xlabel("momentum (GeV)")
    plt.ylabel("Number of events (bin width=" + str(round(x_width, 2)) + " GeV)")
    plt.title("Beam momentum 100GeV, magnetic field " + str(geometry.B) + "T.")
    
    # print info
    print("Mean (GeV) & " + str( round_to(popt[0], cov[0, 0]) ) + " $\pm$ " + str( round_to(cov[0, 0], cov[0, 0]) ) + r" \\" )
    print("Standard deviation (GeV) & " + str( round_to(popt[1], cov[1, 1]) ) + " $\pm$ " + str( round_to(cov[1, 1], cov[1, 1]) ) + r" \\" )
    #print("Amplitude & " + str( round_to(popt[2], cov[2, 2]) ) + " $\pm$ " + str( round_to(cov[2, 2], cov[2, 2]) ) + r" \\"  )
    print("Amplitude & " + str( popt[2]) + " $\pm$ " + str( cov[2, 2]) + r" \\"  )
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

### MAIN CODE ###
data = Master.data("out_4.root")
sigma_x = 1E-4 # x precision
geometry = Master.Geometry(0.5)

hits_1 = data.DC1_Hits # get the hits before the field
hits_2 = data.DC2_Hits # get the hits after the field

traj_1 = Tracker.TrackDCTrajectory(hits_1, 1)
traj_2 = Tracker.TrackDCTrajectory(hits_2, 2)
dirs_1 = Tracker.TrackDirection(traj_1)
dirs_2 = Tracker.TrackDirection(traj_2)

r = Tracker.BendingRadius(hits_1, hits_2, geometry) # compute the bending radius
p = Tracker.Momentum(1, geometry.B, r) # get the momentum distribution of the events

mag_1 = np.sum(traj_1**2, axis=1)
mag_2 = np.sum(traj_2**2, axis=1)

angle = Tracker.BendingAngle(dirs_1, dirs_2)

res = (p / angle) * sigma_x * np.sqrt( (1 / mag_1) + (1 / mag_2) )
avgRes = np.mean(res)
errRes = np.sqrt(np.std(res))

p = p[p > 0]  # remove signifcant outliers, likely due to innacruate tacking or small angle approximation failing

#p = p[p < 120]
#p = p[p > 80]

GaussianFit(p) # perform a gaussian fit to the distribution
print("Average momentum resolution (GeV) & " + str(round_to(avgRes, errRes)) + " $\pm$ " + str(round_to(errRes, errRes)) + r" \\" )
