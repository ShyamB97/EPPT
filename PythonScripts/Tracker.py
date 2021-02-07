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


def TrackDCTrajectory(hits, dc):
    """
    Returns the (2D) trajectories of the hits for either drift chamber.
    ---- Parameters ----
    hits    : hits from drift chamber
    dc      : drift chamber number, 1 or 2
    start   : first wire
    end     : last wire
    dist    : diplacement between the relevant hits
    _list   : np array of trajectories 
    --------------------
    """  
    # change functionalitly depending on which drift chamber hits are used
    if dc == 1:
        start = 0
        end = 1
    elif dc == 2:
        start = 3
        end = 4

    _list = []
    for i in range(len(hits.x)):
        x = hits.x[i]
        z = hits.z[i]
        
        dist = np.array([x[end] - x[start], z[end] - z[start]])
        _list.append(dist)
    # format data in a better way
    _list = np.array(_list)
    return _list.reshape(len(_list), 2)

def TrackDirection(traj):
    """
    Returns the direction vector (2D) of the hits for either drift chamber.
    ---- Parameters ----
    traj    : 2D trajectories
    mag     : length of trajectories
    _dir    : direcion vector for each event
    --------------------
    """
    
    mag = 1 / np.sqrt(np.sum(traj**2, axis=1))

    return np.multiply(traj, mag[:, np.newaxis])


def BendingAngle(dirs_1, dirs_2):
    """
    Calclulte the change in angle of the particle trajectory.
    ---- Parameters ----
    dirs_1    : direction vector before magnet
    dirs_2    : direction vector after magnet
    --------------------
    """
    return abs(dirs_2[:, 0] - dirs_1[:, 0])


def BendingRadius(hits_1, hits_2, geometry):
    """
    Calculates the bending radius of a particle moving through a magnetic field.
    Used for calculaing the particle momentum.
    ---- Parameters ----
    hits_1      : hits from drift chamber 1
    hits_2      : hits from drift chamber 2
    geometry    : class holding detector geometry
    l           : length of the magnet
    dirs_1      : direction vector (2D) of drift chamber 1 hits
    dirs_2      : direction vector (2D) of drift chamber 2 hits
    angle       : deflection angle
    --------------------
    """

    l = geometry.MagnetSize.z

    # get trajectories for eahc track
    traj_1 = TrackDCTrajectory(hits_1, 1)
    traj_2 = TrackDCTrajectory(hits_2, 2)

    # get direction vectors
    dirs_1 = TrackDirection(traj_1)
    dirs_2 = TrackDirection(traj_2)

    # get the angle using the small angle approximation
    angle = BendingAngle(dirs_1, dirs_2)
    
    return l / angle


def Momentum(q, B, r):
    """
    Calculate the particle momentum using the defleciton through the magnetic field
    ---- Parameters ----
    q           : Charge of the particle in quantum units (q = 1 for antimuons)
    B           : Magnetic field strength, get through geometry class
    r           : Bending radius, calculate using BendinRadius()
    --------------------
    """
    # 0.3 = (1.6e-19 / 1.6e-10) * 3e8
    return 0.3 * q * B * r
