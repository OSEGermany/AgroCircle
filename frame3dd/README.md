# Structural analysis using `frame3dd`

[Frame3DD](http://frame3dd.sourceforge.net/) is free open-source software
for static and dynamic structural analysis of 2D and 3D frames and trusses
with elastic and geometric stiffness.

## Instructions

1. install [`frame3dd`](http://frame3dd.sourceforge.net/) and `python-visual`
1. change parameters in "in.csv".
1. run calculation:

    ```bash
./calc.sh
    ```
1. find results in "out.csv"

## Parameters

	l: traverse length (mm)
	n: number of outer tubes (3 or 4)
	nz: number of segments (inner tube sections)
	d: center to center distance of outer tubes (mm)
	d1: outer tubes outer diameter (mm)
	w1: outer tubes wall thickness (mm)
	d2: inner tubes outer diameter (mm)
	w2: inner tubes wall thickness (mm)

## Calculations

	W: traverse total weight (kg)
	d0: deformation by own weight
	d200: deformation by central force of additional 2000N
