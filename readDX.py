#!/usr/bin/python

###############################################################################
# readDX.py                                                                   #
# Authors: Dario Ghersi & Ryan Ehrlich                                        #
# Version: 1                                                                  #
#                                                                             #
# This module reads all *.dx files from APBS or EasyMIFs output and converts  #
# the output to pandas dataframes, which contain Cartesian coordinates. Each  #
# dataframe is returned with is associated file name.                         #
###############################################################################

import sys
import pandas as pd
from multiprocessing import Pool
import glob

################################################################################
# Grid class                                                                   #
################################################################################

class Grid:
    def __init__(self, origin, spacing, dimension, coords, energies):
        self.origin = origin
        self.spacing = spacing
        self.coords = coords
        self.energies = energies
        self.nx = dimension[0];
        self.ny = dimension[1];
        self.nz = dimension[2]
        self.npoints = self.nx * self.ny * self.nz

###############################################################################

def readgrid_easymifs(infile_name):
    """
    Read an Easymifs map file and create a grid object with coordinates
    and energy values
    """
    try:
        infile = open(infile_name, "r")
    except:
        print("Can not open " + infile_name)
        sys.exit(1)
    read_energies = False
    all_data = infile.readlines()
    infile.close()
    lc = 1  # line counter
    for line in all_data:
        if not read_energies:  # first part of the map file
            if line[:5] == "delta":
                spacing = float(line.split()[3])
            elif line.find("gridpositions") != -1:
                nx, ny, nz = map(int, line.split()[5:])
            elif line[:6] == "origin":
                lower_corner = map(float, line.split()[1:])
            elif line[:8] == "object 3":
                break
        lc += 1  # increment the line counter

    ## store the energy values and coordinates
    coords = []  # coordinates of the points whose energy is <= cutoff
    energies = []  # list with the energy values
    dimension = [nx, ny, nz]
    for cx in range(nx):
        x = lower_corner[0] + spacing * cx
        for cy in range(ny):
            y = lower_corner[1] + spacing * cy
            for cz in range(nz):
                z = lower_corner[2] + spacing * cz
                line = all_data[lc]
                value = float(line)
                coords.append([x, y, z])
                energies.append(value)
                lc += 1  # increment the line counter

    ## create a grid object
    grid = Grid(lower_corner, spacing, dimension, coords, energies)
    return grid

###############################################################################

def readgrid_apbs(infile_name):
    """
    Read an Easymifs map file and create a grid object with coordinates
    and energy values
    """
    try:
        infile = open(infile_name, "r")
    except:
        print("Cannon open " + infile_name)
        exit(1)
    read_energies = False
    all_data = infile.readlines()
    infile.close()
    lc = 1  # line counter
    for line in all_data:
        if not read_energies:  # first part of the map file
            if line[:5] == "delta":
                spacing = float(line.split()[3])
            elif line.find("gridpositions") != -1:
                nx, ny, nz = list(map(int, line.split()[5:]))
            elif line[:6] == "origin":
                lower_corner = list(map(float, line.split()[1:]))
            elif line[:8] == "object 3":
                break
        lc += 1  # increment the line counter

    ## store the energy values and coordinates
    coords = []  # coordinates of the points whose energy is <= cutoff
    energies = []  # list with the energy values
    dimension = [nx, ny, nz]
    flag = True
    for cx in range(nx):
        x = lower_corner[0] + spacing * cx
        for cy in range(ny):
            y = lower_corner[1] + spacing * cy
            for cz in range(nz):
                z = lower_corner[2] + spacing * cz
                coords.append([x, y, z])
                line = all_data[lc]
                if flag:
                    if line.find("attribute") == -1:

                        values = list(map(float, line[:-1].split()))
                        energies.extend(values)
                        lc += 1  # increment the line counter
                    else:
                        flag = False

    ## create a grid object
    grid = Grid(lower_corner, spacing, dimension, coords, energies)
    return(grid)

###############################################################################

def getGrid(infile, analysis):
    if analysis == 'apbs':
        grid = readgrid_apbs(infile)
        return(grid)
    if analysis == 'easymifs':
        grid = readgrid_easymifs(infile)
        return(grid)
    else:
        print('Invalid analysis type. Please submit "apbs" or "easymifs".')

################################################################################
# threeD class                                                                 #
################################################################################

class threeD():
    def __init__(self, file):
        self.file = file
    """
    Get lines from *.dat file, remove outliers (huge spread), remove all values greater than 0, 
    and return dataframe.
    """

    def processGrid(self, grid_):
        energies_coords = zip(grid_.energies, grid_.coords)     # combine energy and coordinates
        energy_, x_, y_, z_ = [], [], [], []
        for point in energies_coords:   # populate df with energy and coordinate values
            energy = point[0]
            x, y, z = point[1]
            energy_.append(energy)
            x_.append(x)
            y_.append(y)
            z_.append(z)
        df = pd.DataFrame()
        df['energy'] = energy_
        df['x'] = x_
        df['y'] = y_
        df['z'] = z_
        maxY = df.y.max()       # find max y-axis value
        yCut = maxY - 25        # subtract 25 (angstroms) from max value. Grid points with a lower y-axis value than
                                # this are not significant
        ## Trim grid (*.dx dimensions)
        df = df.drop(df[df.y < yCut].index)
        df = df.drop(df[(df.x < -36.5)].index)
        df = df.drop(df[(df.x > 36.5)].index)
        df = df.drop(df[(df.z < -36.5)].index)
        df = df.drop(df[(df.z > 36.5)].index)
        return (df)

    def getLines(self, analysis):
        if analysis == 'apbs':
            grid_ = getGrid(self.file, 'apbs')  # getGrid uses the *.dx file to gather Cartesian coordinates and energy
            df = self.processGrid(grid_)        # process grid_ to target the TCR interface as a pandas df
            return (df)
        if analysis == 'easymifs':
            grid_ = getGrid(self.file, 'easymifs')  # getGrid uses the *.dx file to gather Cartesian coordinates and energy
            df = self.processGrid(grid_)            # process grid_ to target the TCR interface as a pandas df
            df = df.drop(df[df.energy > 0].index)   # remove values > 0 (for easymifs only)
            return (df)

################################################################################
# Functions                                                                    #
################################################################################

def processGrids(tup):
    f = tup[0]              # *.dx file
    analysis = tup[1]       # analysis type (args.analysis, 'apbs' or 'easymifs')
    grid = threeD(f)        # instantiate threeD class
    df = grid.getLines(analysis)    # call getLines function to retrieve Cartesian coordinates and energy values
    return([f, df])

def processDX(folder, analysis, cores, flag):
    if flag:
        path = "%s/*.dx" % (''.join(glob.glob(folder)))         # path to *.dx folder
        input_files = sorted(glob.glob(path))                   # input *.dx files

        p = Pool(processes=cores)
        dxFiles = [(x, analysis) for x in input_files]         # processGrids input
        results = p.map(processGrids, dxFiles)                 # get *.dx Cartesian coordinates and energy values as a df
        p.close()
        return(results)
    else:
        p = Pool(processes=cores)
        dxFiles = [(x, analysis) for x in folder]  # processGrids input
        results = p.map(processGrids, dxFiles)  # get *.dx Cartesian coordinates and energy values as a df
        p.close()
        return (results)
