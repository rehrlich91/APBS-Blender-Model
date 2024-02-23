# APBS-Blender-Model

## Purpose
Here users are able to visualize the output from the Adaptive Poisson-Boltzmann Solver (APBS) in Blender. The current version uses the raw output (*.dx) file from the APBS software to assign attributes to each point in the sampling grid. These attributes are the raw energy value (determined by APBS), the Cartesian coordinates, and RGBA values. The energy values are used to view the different states of the energy grid, by removing points that are below (using absolute value) a certain threshold - which also enables the user to animate the grid (seen below). Please note the following versions used:

Python: 3.9.5

Blender: 3.6.9 LTS

![gifmaker_me-3](https://github.com/rehrlich91/APBS-Blender-Model/assets/54915452/5e57e7a8-2a5f-4c10-97b1-225561e86e78)

## Installation
Previous to running APBS the user must convert PDB to PQR files using PDB2PQR. This conversion adds additional information to the PDB file such that APBS is able to more accruately determine energy values. The following link contains the PDB2PQR and APBS documentation:

https://pdb2pqr.readthedocs.io/en/latest/ (PDB2PQR)

https://apbs.readthedocs.io/en/latest/ (APBS)

Conversely, the user can use the online webserver:

https://server.poissonboltzmann.org/apbs

Lastly, Blender can be downloaded here:

https://www.blender.org/download/releases/3-6/ (Blender)

## Producing Blender Input Data
Once the user has the desired *.dx files, they are able to produce the input *.csv file to visualize the results. A typical command line run (using the files provided) is:

``` console
python blenderVis_apbs.py -mif test_dx -pdb test_pdb -a apbs -c 4
```

After running this program the output will be stored in a new directory (blender_output)

## Visualizing in Blender
Open Blender, select the default cube and press `x`, then select `delete`. In the top right side of the menu bar select `Scripting` and press the `New` button at the top of the scripting window. At this point the user will be able to code in the scripting window. Copy and paste the bpy_script.py here, then navigate to the main() and copy/paste the path of the blender output folder. Lastly, press the play (will say "run script" when hovering over it) button at the top of the scripting window. The results should appear!

* Important -- If the resolution of the grid was not 1 angstrom, navigate to the setup_gn() and change the `cube_mesh.inputs[0].default_value` values to equal the xyz resoltution used in your analysis. 

## Importing PDB Files to Blender
There are a few methods to do this, but here PDB files are converted to GLB files. This can be done using ChimeraX when saving any protein structure within the app:

https://www.rbvi.ucsf.edu/chimerax/download.html (ChimeraX)

Alternatively the Molecular Nodes Blender add-on can open PDB files:

https://bradyajohnston.github.io/MolecularNodes/installation.html (Molecular Nodes)



