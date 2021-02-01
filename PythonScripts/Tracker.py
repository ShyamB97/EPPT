#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 10:45:38 2021

@author: sb16165

Handles particle trajectory calculataions
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

import Master


def HitVisualiser(hits, n):
    """
    Plots the hit points for each wire of a drift chamber. Axes coordinates
    are dimensionless.
    ---- Parameters ----
    hits    : hits from drift chamber
    n       : number of events for plot
    fig     : figure
    ax      : 3D plot axis
    --------------------
    """
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    for i in range(n):
        x = hits.x[i]
        y = hits.y[i]
        z = hits.z[i]

        ax.scatter3D(z, x, y, cmap='hsv');
        ax.plot([z[0], z[4]], [x[0], x[4]], [y[0], y[4]])

    plt.show()

def TrackDirection(hits, dc):
    """
    Returns the direction vector (2D) of the hits for either drift chamber.
    ---- Parameters ----
    hits    : hits from drift chamber
    dc      : drift chamber number, 1 or 2
    start   : first wire
    end     : last wire
    reverse : if dc is 2, then the dirction needs to be reversed
    norm    : direcion vector for each event
    dist    : diplacement between the relevant hits
    --------------------
    """

    # change functionalitly depending on which drift chamber hits are used
    if dc == 1:
        start = 0
        end = 1
        reverse = 1
    elif dc == 2:
        start = 3
        end = 4
        reverse = -1

    norms = []
    for i in range(len(hits.x)):
        x = hits.x[i]
        z = hits.z[i]
        
        dist = np.array([x[end] - x[start], z[end] - z[start]])
        norm = (1 / np.sqrt( np.sum(dist**2) )) * dist
        norms.append(norm)

    return reverse * np.array(norms)


def ArcPointX(hits, dirs, dist, xWidth, dc):
    """
    Gets the start or end of the arc depending on the drift chamber number.
    ---- Parameters ----
    hits    : hits from drift chamber
    dirs    : hit direciton (2D)
    dist    : distance from drift chamber to magnet
    xWidth  : size of the x wire plane
    dc      : drift chamber number, 1 or 2
    point   : if dc is 2, then the dirction needs to be reversed
    h       : x distancde from center of the geometry
    --------------------
    """

    # change functionalitly depending on which drift chamber hits are used
    if dc == 1:
        point = 4
    elif dc == 2:
        point = 0
    
    h = []
    for i in range(len(dirs)):
        x = hits.x[i]
        h.append((dirs[i][0] * dist) + (xWidth/2) * x[point])
    return np.array(h)


def BendingRadius(hits_1, hits_2, geometry):
    """
    Calculates the bending radius of a particle moving through a magnetic field.
    Used for calculaing the particle momentum.
    ---- Parameters ----
    hits_1      : hits from drift chamber 1
    hits_1      : hits from drift chamber 2
    geometry    : class holding detector geometry
    l           : distance from drift chamber to magnet
    d_1         : distance from last wire to the start of magnet
    d_2         : distance from first wire to start of magnet
    dirs_1      : direction vector (2D) of drift chamber 1 hits
    dirs_2      : direction vector (2D) of drift chamber 2 hits
    h_1         : x displacement of particle before entering the magnetic field
    h_1         : x displacement of particle after exiting the magnet field
    angle       : deflection angle
    arcDist     : shortest path between the start and end of the curved trajectory 
    --------------------
    """

    l = geometry.MagnetSize.z # length of magnet along z
    d_1 = abs(geometry.DC1Pos.z) - l/2 - geometry.DC1Size.z/2
    d_2 = abs(geometry.DC2Pos.z) - l/2 - geometry.DC2Size.z/2

    dirs_1 = TrackDirection(hits_1, 1)
    dirs_2 = TrackDirection(hits_2, 2)


    h_1 = ArcPointX(hits_1, dirs_1, d_1, geometry.wirePlane1Size.x, 1)
    h_2 = ArcPointX(hits_2, dirs_2, d_2, geometry.wirePlane2Size.x, 2)

    dirs_1 = dirs_1.reshape(len(dirs_1), 2)
    dirs_2 = dirs_2.reshape(len(dirs_2), 2)

    angle = ( np.arcsin( dirs_2[:, 0] ) - np.arcsin( dirs_1[:, 0] ) ) * 180 / np.pi # deflection angle
    arcDist = np.sqrt( l**2 + (h_2 - h_1)**2 ) # shortest path between the arc points

    return arcDist / (2 * np.sin(angle))  # bending radius

def Momentum(q, B, r):
    """
    Calculate the particle momentum using the defleciton through the magnetic field
    ---- Parameters ----
    q           : Charge of the particle
    B           : Magnetic field strength, get through geometry class
    r           : Bending radius, calculate using BendinRadius()
    --------------------
    """
    p = q * B * r
    p = p * (3E8 / 1.6E-10) # convert to GeV/c
    return abs(p)

### TEST CODE ###

data = Master.data("out_2a.root")
geometry = Master.Geometry()

hits_1 = data.DC1_Hits
hits_2 = data.DC2_Hits

hitX = np.array(hits_1.x)

r = BendingRadius(hits_1, hits_2, geometry)
p = Momentum(1.6E-19, geometry.B, r)
print(np.mean(p))
