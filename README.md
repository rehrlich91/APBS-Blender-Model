# APBS-Blender-Model

## Purpose
Here users are able to visualize the output from the Adaptive Poisson-Boltzmann Solver (APBS) in Blender. The current version uses the raw output (*.dx) file from the APBS software to assign attributes to each point in the sampling grid. These attributes are the raw energy value (determined by APBS), the Cartesian coordinates, and RGBA values. The energy values are used to view the different states of the energy grid, by removing points that are below (using absolute value) a certain threshold - which also enables the user to animate the grid (seen below). Please note the following versions used:

Python: 3.9.5

Blender: 3.6.9 LTS

![gifmaker_me-3](https://github.com/rehrlich91/APBS-Blender-Model/assets/54915452/5e57e7a8-2a5f-4c10-97b1-225561e86e78)

## Installation
Previous to running APBS the user must convert PDB to PQR files using PDB2PQR. This conversion adds additional information to the PDB file such that APBS is able to more accruately determine energy values. The following link contains the PDB2PQR and APBS documentation:

https://pdb2pqr.readthedocs.io/en/latest/
https://apbs.readthedocs.io/en/latest/

Conversely, the user can use the online webserver:

https://server.poissonboltzmann.org/apbs

## Producing Blender Input Data
Once the user has the desired *.dx files, they are able to produce the input *.csv file to visualize the results. A typical command line run (using the files provided) is:

``` console
python blenderVis_apbs.py -mif test_dx -pdb test_pdb -a apbs -c 4
```

After running this program the output will be stored in a new directory (blender_output)

## Visualizing in Blender




