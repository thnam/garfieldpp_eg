#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from __future__ import division

import sys
sys.path.append('./py_gmsh')

import collections
import gmshlib

f = open('gem.geo','w')

# Gem parameters
lc = 0.5 # um
pitch = 140 # um
r_out = 35 # um
r_cone = 30 # um
t_copper = 5 # um
t_kapton = 50 # um
##############################################################

points = gmshlib.ObjectList('p')
curves = gmshlib.ObjectList('c')
lineloops = gmshlib.ObjectList('ll')
# Bottom of lower copper plate
points.Add(gmshlib.Point([0,0,0,lc]))
points.Add(points[0].Translate([pitch/2 - r_out, 0, 0]))
curves.Add(gmshlib.Line(points[:]))

points.Add(points[0].Translate([pitch/2, 0, 0]))
points.Add(points[0].Translate([pitch/2 + r_out, 0, 0]))
curves.Add(gmshlib.Circle([points[-1], points[-2], points[-3]]))

points.Add(points[0].Translate([pitch, 0, 0]))
curves.Add(gmshlib.Line([points[-2], points[-1]]))

points.Add(points[-1].Translate([0, pitch - r_out, 0]))
curves.Add(gmshlib.Line([points[-2], points[-1]]))

points.Add(points[-1].Translate([0, r_out, 0]))
points.Add(points[-1].Translate([-r_out, 0, 0]))
curves.Add(gmshlib.Circle([points[-1], points[-2], points[-3]]))

points.Add(points[-1].Translate([- pitch + 2*r_out, 0, 0]))
curves.Add(gmshlib.Line([points[-2], points[-1]]))

points.Add(points[-1].Translate([-r_out, 0, 0]))
points.Add(points[-1].Translate([0, -r_out, 0]))
curves.Add(gmshlib.Circle([points[-1], points[-2], points[-3]]))
curves.Add(gmshlib.Line([points[0], points[-1]]))

lineloops.Add(gmshlib.LineLoop(curves[:]))

points.Write(f)
curves.Write(f)
lineloops.Write(f)

