#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 09:49:01 2021

@author: sb16165

Base module for particle techniques analysis. Holds classes for
accessing data and detector geometry.
"""
import uproot


class Vector3:
    """
    Class to implement 3 dimensional vector objects. Currently holds no mathematical properties.
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def Zero():
        return Vector3(0, 0, 0)


class Geometry:
    """
    Class holding Detector Geometry and properties (such as magnetic field strangth)
    """
    
    MagnetSize = Vector3.Zero()
    MagnetPos = Vector3.Zero()
    
    arm1Size = Vector3.Zero()
    arm2Pos = Vector3.Zero()
    
    DC1Size = Vector3.Zero()
    DC2Size = Vector3.Zero()

    DC1Pos = Vector3.Zero()
    DC2Pos = Vector3.Zero()
    
    wirePlane1Size = Vector3.Zero()
    wirePlane2Size = Vector3.Zero()
    
    
    def __init__(self, B=1):
        # Detector Properties units in m. Adding what I need at the time.

        # World Space = [10, 3, 10]

        Geometry.MagnetSize = Vector3(*[1, 1, 1]) # Magnet is a cube
        self.B = B # in T, this will change

        Geometry.MagnetPos = Vector3(*[0, 0, 0]) # manget is at the geomoetry origin

        Geometry.arm1Size = Vector3(*[1.5, 1, 3])
        Geometry.arm2Size = Vector3(*[2, 2, 3.5])

        Geometry.arm1Pos = Vector3(*[0, 0, -5])
        Geometry.arm2Pos = Vector3(*[0, 0, 5]) # can change but we will not rotate this arm, so it is constant 

        # one per arm
        Geometry.DC1Size = Vector3(*[1, 0.3, 0.01])
        Geometry.DC2Size = Vector3(*[1.5, 0.3, 0.01])

        Geometry.DC1Pos = Vector3(*[0, 0, -5])
        Geometry.DC2Pos = Vector3(*[0, 0, 5])

        # five wire planes
        Geometry.wirePlane1Size = Vector3(*[1, 0.3, 1E-4])
        Geometry.wirePlane2Size = Vector3(*[1.5, 0.3, 1E-4])


class data:
    """
    Gets data from the root file.
    ---- Parameters ----
    name            : ROOT file name
    E_Hadron        : Total deposited Energy from the Hadronic calorimeter
    E_EM            : Total deposited energy from the EM calorimeter
    EVector_Hadron  : Deposited energy components from the Hadronic calorimeter
    EVector_EM      : Deposited energy components from the EM calorimeter
    DC1_Hit         : Hit Vector of Drift chamber 1, sorted by component first
    DC2_Hits        : Hit Vector of Drift chamber 2, sorted by component first
    --------------------
    """

    E_EM = 0
    E_Hadron = 0
    EVector_EM = 0
    EVector_Hadron = 0
    DC1_Hits = 0
    DC2_Hits = 0
    
    def __init__(self, name):
        self.name = name
    
        file = uproot.open(name) # open root file
        tree = file['B5'] # access B5 directory        

        ### Retrieve Data ###
        data.E_EM = tree.arrays(library="np")['ECEnergy']
        data.E_Hadron = tree.arrays(library="np")['HCEnergy']
        
        data.EVector_EM = tree.arrays(library="np")['ECEnergyVector']
        data.EVector_Hadron = tree.arrays(library="np")['HCEnergyVector']
    
        data.DC1_Hits = Vector3(tree.arrays(library="np")['Dc1HitsVector_x'], 
                           tree.arrays(library="np")['Dc1HitsVector_y'], 
                           tree.arrays(library="np")['Dc1HitsVector_z'])
    
        data.DC2_Hits = Vector3(tree.arrays(library="np")['Dc2HitsVector_x'], 
                           tree.arrays(library="np")['Dc2HitsVector_y'], 
                           tree.arrays(library="np")['Dc2HitsVector_z'])


