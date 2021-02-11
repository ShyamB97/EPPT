#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 10:56:56 2021

@author: sb16165
"""

import numpy as np
import matplotlib.pyplot as plt

import Master


def Plot(data, bins=50, xlabel="", title=""):
    bins, edges, _ = plt.hist(data, bins, color="blue", edgecolor="black")
    binWidth = round((edges[-1] - edges[0]) / len(edges), 2)
    plt.xlabel(xlabel)
    plt.ylabel("Number of events (bin width=" + str(binWidth) + " GeV)")
    plt.title(title)


def PlotTotalEnergy():
    Plot(emE + hE, 50, "Total energy deposited (GeV)")


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

# get total energy 
emE = data.E_EM
hE = data.E_Hadron

PlotTotalEnergy()
#PlotEnergies()