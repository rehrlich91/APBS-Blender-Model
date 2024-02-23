# APBS-Blender-Model

## Purpose
Here users are able to visualize the output from the Adaptive Poisson-Boltzmann Solver APBS in Blender. The current version uses the raw output (*.dx) file from the APBS software to assign attributes to each point in the sampling grid. These attributes are the raw energy value (determined by APBS), the Cartesian coordinates, and RGBA values. The energy values are used to view the different states of the energy grid, by removing points that are below (using absolute value) a certain threshold - which also enables the user to animate the grid (seen below). Please note the following versions used:

Python: 3.9.5
Blender: 3.6.9 LTS

![gifmaker_me-3](https://github.com/rehrlich91/APBS-Blender-Model/assets/54915452/5e57e7a8-2a5f-4c10-97b1-225561e86e78)

