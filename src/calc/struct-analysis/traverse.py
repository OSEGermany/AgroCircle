#!/usr/bin/python2

# SPDX-FileCopyrightText: 2014 Thomas Kalka <thomas.kalka@co-buero.de>
# SPDX-FileCopyrightText: 2014 toka <toka@brutus.co-buero.de>
# SPDX-FileCopyrightText: 2020 hoijui <hoijui.quaero@gmail.com>
# SPDX-FileCopyrightText: 2023 Robin Vobruba <hoijui.quaero@gmail.com>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

# encoding: utf8
"""
calculates input data for frame3dd
"""

from __future__ import division
import os
import os.path
from math import sin, cos, pi
from visual import vector
from parse_3dd import parse

def d2b(alpha):
	return pi/2+alpha/180*pi

def polarZ(alpha, r=1.0):
	d_ = d2b(alpha)
	return (r*cos(d_), r*sin(d_), 0)

def polarX(alpha, r=1.0, x=0):
	d_ = d2b(alpha)
	return (x, r*cos(d_), r*sin(d_))

class Construction(object):
	def __init__(self):
		self.points = []
		self.P = {}
		self.C = []

	def connect(self, a, b, t):
		"connect points with index a and "
		pa = self.P[a]
		pb = self.P[b]
		#d, w = t
		#cylinder(pos = pa, axis = pb-pa, radius = d/2)
		self.C.append({
			"from": pa.count,
			"to"  : pb.count,
			"tube": t
		})

		#add( C)

class Values(object):
	pass

class Params(object):
	"""
	holds defaults for a function call

	if updated by set(d), type conversion to types given by defaults is performed
	"""

	def __init__(self, **defaults):
		self.defaults = defaults
	def __repr__(self):
		return self.defaults.repr()

	def set(self, d):
		self.values = Values()
		self.values.__dict__.update(self.defaults)

		for key,value in d.iteritems():
			if key in self.defaults:
				c = self.defaults[key].__class__
				self.values.__dict__[key] = c(value)

	def __exit__(self, *args):
		pass

	def __enter__(self):
		return self.values


class Traverse(Construction):

	def __init__(self, **params):

		Construction.__init__(self)

		self.params = Params(
			n=3, l=18000.0, d=700.0, nz=10,
			d1=48.0, w1=2.6, d2=10.0, w2=1.0
		)

		self.params.set(params)

		with self.params as p:
			n = p.n
			nz = p.nz
			d = p.d
			l = p.l
			t1 = [p.d1, p.w1]
			t2 = [p.d2, p.w2]

		assert n in [3, 4]
		assert nz > 0
		assert nz <= 100

		r_ = d / sin(pi/n) / 2
		l_ = l/nz
		for j in range(0, nz+1):
			for i in range(0, n):
				p = vector(polarX(360/n*i, r_, j*l_))
				p.count = len(self.points)
				self.points.append(p)
				self.P[(i, j)] = p
				# add( p)
				#sphere(pos=P[(i,j)],radius=30)

		for i in range(0,n):
			for j in range(0, nz+1):
				if j < nz:
					self.connect((i, j), (i, j+1), t1)
					if (i+j) % 2 == 0:
						self.connect((i, j), ((i+1)%n, j+1), t2)
					else:
						self.connect(((i+1)%n, j), (i, j+1), t2)

				self.connect((i, j), ((i+1)%n, j), t2)

	def frame3dd(self):
		"returns frame3dd input file"

		res = []

		def add(s):
			res.append(s)

		add("# node data ...\n%i # number of nodes" % len(self.points))

		for p in self.points:
			add( "%i %f %f %f 10" % (p.count+1, p[0], p[1], p[2]))

		add("# reaction data ...")
		add("4 # number of nodes")
		add("2 1 1 1 0 0 0")
		add("3 1 0 1 0 0 0")
		add("%i 0 0 1 0 0 0" % (len(self.points)))
		add("%i 0 0 1 0 0 0" % (len(self.points) - 1))

		add("# frame element data ...")
		add("%i # number of connections" % len(self.C))

		for i, c in enumerate(self.C):
			d, w = c["tube"]
			Ro = d/2
			Ri = Ro-w
			Ax = pi * (Ro**2-Ri**2)
			Asy = Ax / ( 0.54414 + 2.97294*(Ri/Ro) - 1.51899*(Ri/Ro)**2)
			Asz = Asy
			Jx = (1/2)*pi *(Ro**4 - Ri**4)
			Iy = (1/2)*Jx
			Iz = Iy
			E = 200000
			G = 79300
			roll = 0 # TODO: toka: dont understand this
			density = 7.85e-9

			add("%i  %i %i  %f %f %f  %f %f %f   %f %f %f %e" % (
				i + 1,
				c["from"]+1,
				c["to"]+1,
				Ax, Asy, Asz,
				Jx, Iy, Iz,
				E, G, roll, density
			))

		add("1 # shear")
		add("1 # geom")
		add("1 # static exageration factor")
		add("1 # x-axis increment ")

		add("""
		# load data ...

		2                        # number of static load cases,  1..30

		# Begin Static Load Case 1

		# gravitational acceleration for self-weight loading, mm/s^2 (global)
		#   gX         gY         gZ
		#   mm/s^2     mm/s^2     mm/s^2
		    0 0 9810

		0                   # number of loaded nodes (global)
		#.node  X-load   Y-load   Z-load   X-mom     Y-mom     Z-mom
		#         N        N        N        N.mm      N.mm      N.mm
		#  N[1]    Fx[1]    Fy[1]    Fz[1]    Mxx[1]    Myy[1]    Mzz[1]

		0                   # number of uniformly-distributed element loads (local)
		#.elmnt  X-load   Y-load   Z-load   uniform member loads in member coordinates
		#         N/mm     N/mm     N/mm
		# EL[1]    Ux[1]    Uy[1]    Uz[1]

		0                   # number of trapezoidally-distributed element loads (local)
		# EL[1]  xx1[1]   xx2[2]   wx1[1]   wx2[1]  # locations and loads - local x-axis
		#        xy1[1]   xy2[2]   wy1[1]   wy2[1]  # locations and loads - local y-axis
		#        xz1[1]   xz2[2]   wz1[1]   wz2[1]  # locations and loads - local z-axis

		0                   # number of concentrated interior point loads (local)
		#.elmnt  X-load   Y-load   Z-load    x-loc'n  point loads in member coordinates
		# EL[1]    Px[1]    Py[1]    Pz[1]    x[1]

		0                   # number of frame elements with temperature changes (local)
		#.elmnt   coef.  y-depth  z-depth  deltaTy+  deltaTy-  deltaTz+  deltaTz-
		#         /deg.C  mm       mm       deg.C     deg.C     deg.C     deg.C
		# EL[1]    a[1]    hy[1]    hz[1]    Ty+[1]    Ty-[1]    Tz+[1]    Tz-[1]


		0                   # number of prescribed displacements nD<=nR (global)
		#.node   X-displ  Y-displ  Z-displ  X-rot'n   Y-rot'n   Z-rot'n
		#         mm       mm       mm       radian    radian    radian
		#  N[1]    Dx[1]    Dy[1]    Dz[3]    Dxx[1]    Dyy[1]    Dzz[1]

		# Begin Static Load Case 2

		# gravitational acceleration for self-weight loading, mm/s^2 (global)
		#   gX         gY         gZ
		#   mm/s^2     mm/s^2     mm/s^2
		    0 0 9810

		1                   # number of loaded nodes (global)
		#.node  X-load   Y-load   Z-load   X-mom     Y-mom     Z-mom
		#         N        N        N        N.mm      N.mm      N.mm
		#  N[1]    Fx[1]    Fy[1]    Fz[1]    Mxx[1]    Myy[1]    Mzz[1]
		%i  0  0  2000 0 0 0

		0                   # number of uniformly-distributed element loads (local)
		#.elmnt  X-load   Y-load   Z-load   uniform member loads in member coordinates
		#         N/mm     N/mm     N/mm
		# EL[1]    Ux[1]    Uy[1]    Uz[1]

		0                   # number of trapezoidally-distributed element loads (local)
		# EL[1]  xx1[1]   xx2[2]   wx1[1]   wx2[1]  # locations and loads - local x-axis
		#        xy1[1]   xy2[2]   wy1[1]   wy2[1]  # locations and loads - local y-axis
		#        xz1[1]   xz2[2]   wz1[1]   wz2[1]  # locations and loads - local z-axis

		0                   # number of concentrated interior point loads (local)
		#.elmnt  X-load   Y-load   Z-load    x-loc'n  point loads in member coordinates
		# EL[1]    Px[1]    Py[1]    Pz[1]    x[1]

		0                   # number of frame elements with temperature changes (local)
		#.elmnt   coef.  y-depth  z-depth  deltaTy+  deltaTy-  deltaTz+  deltaTz-
		#         /deg.C  mm       mm       deg.C     deg.C     deg.C     deg.C
		# EL[1]    a[1]    hy[1]    hz[1]    Ty+[1]    Ty-[1]    Tz+[1]    Tz-[1]


		0                   # number of prescribed displacements nD<=nR (global)
		#.node   X-displ  Y-displ  Z-displ  X-rot'n   Y-rot'n   Z-rot'n
		#         mm       mm       mm       radian    radian    radian
		#  N[1]    Dx[1]    Dy[1]    Dz[3]    Dxx[1]    Dyy[1]    Dzz[1]


		# dynamic analysis data ...
		0      # number of desired dynamic modes
		""" % (int(len(self.points) / 2)))

		data_in = "\n".join(res)

		with open("traverse.in", "w") as f:
			f.write(data_in)

		try:
			os.remove("traverse.out")
		except OSError:
			pass

		os.system("frame3dd -q -i traverse.in -o traverse.out")

		tables = parse("traverse.out")

		return tables

	def simulate(self):

		tables = self.frame3dd()

		W    = -tables[5].max(3)*4/9.81
		d0   = tables[3].max(3)
		d200 = tables[7].max(3)

		results = self.params.values.__dict__.copy()
		results["W"] = W
		results["d0"] = d0
		results["d200"] = d200

		return results


import csv
dialect = csv.Sniffer().sniff(open("in.csv").read(1024))

reader = csv.DictReader(open("in.csv"), dialect=dialect)

outf = open("out.csv", "w", buffering=1)
writer = csv.DictWriter(
	outf,
	"n	l	d	nz	d1	w1	d2	w2	W	d0	d200".split("\t"),
	dialect=dialect,
	)
writer.writeheader()

for params in reader:
	results = Traverse(**params).simulate()
	writer.writerow(results)
