#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from __future__ import division

import sys
sys.path.append('../py_gmsh')

import collections

import gmshlib
f = open('gem.geo','w')

# Gem parameters
lc = 2.5 # um
pitch = 140 # um
r_out = 35 # um
r_cone = 30 # um
t_copper = 5 # um
t_kapton = 50 # um
##############################################################

points = gmshlib.ObjectList('p')
curves = gmshlib.ObjectList('c')
lineloops = gmshlib.ObjectList('ll')
surfaces = gmshlib.ObjectList('sf')
surfaceloops = gmshlib.ObjectList('sl')
volumes = gmshlib.ObjectList('volumes')

# Bottom of lower copper plate
##############################################################
tmp_points1 =[]
points.Add(gmshlib.Point([0,0,0,lc]))

tmp_points1.append(points[-1])

points.Add(points[0].Translate([pitch/2 - r_out, 0, 0]))
curves.Add(gmshlib.Line(points[:]))

points.Add(points[0].Translate([pitch/2, 0, 0]))
points.Add(points[0].Translate([pitch/2 + r_out, 0, 0]))
curves.Add(gmshlib.Circle([points[-1], points[-2], points[-3]]))

points.Add(points[0].Translate([pitch, 0, 0]))
curves.Add(gmshlib.Line([points[-2], points[-1]]))

tmp_points1.append(points[-1])

points.Add(points[-1].Translate([0, pitch - r_out, 0]))
curves.Add(gmshlib.Line([points[-2], points[-1]]))

points.Add(points[-1].Translate([0, r_out, 0]))

tmp_points1.append(points[-1])

points.Add(points[-1].Translate([-r_out, 0, 0]))
curves.Add(gmshlib.Circle([points[-1], points[-2], points[-3]]))

points.Add(points[-1].Translate([- pitch + 2*r_out, 0, 0]))
curves.Add(gmshlib.Line([points[-2], points[-1]]))

points.Add(points[-1].Translate([-r_out, 0, 0]))

tmp_points1.append(points[-1])

points.Add(points[-1].Translate([0, -r_out, 0]))
curves.Add(gmshlib.Circle([points[-1], points[-2], points[-3]]))
curves.Add(gmshlib.Line([points[-1], points[0]]))

lineloops.Add(gmshlib.LineLoop(curves[:]))
surfaces.Add(gmshlib.PlaneSurface(lineloops))

ext0 = surfaces[-1].Extrude([0,0,5],index = 0)
points.AddList(ext0['points'])
curves.AddList(ext0['curves'])
lineloops.AddList(ext0['lineloops'])
surfaces.AddList(ext0['surfaces'])
surfaceloops.AddList(ext0['surfaceloops'])
volumes.AddList(ext0['volumes'])
##############################################################
#polyline1 = gmshlib.MakePolyLines(tmp_points1,'kapton')
#curves.AddList(polyline1)
#lineloops.Add(gmshlib.LineLoop(polyline1))
#surfaces.Add(gmshlib.RuledSurface(lineloops[-1:]))
##############################################################
ext1 = surfaces[-1].Extrude([0,0,-50],index = 1)
points.AddList(ext1['points'])
curves.AddList(ext1['curves'])
lineloops.AddList(ext1['lineloops'])
surfaces.AddList(ext1['surfaces'])
surfaceloops.AddList(ext1['surfaceloops'])
volumes.AddList(ext1['volumes'])

#print(str(surfaces[-1]), surfaces[-1]._elements[0]._elements[0].__str__())
tmp_sf = surfaces[-1]
ext2 = tmp_sf.Extrude([0,0,-5],index = 2)
points.AddList(ext2['points'])
curves.AddList(ext2['curves'])
lineloops.AddList(ext2['lineloops'])
surfaces.AddList(ext2['surfaces'])
surfaceloops.AddList(ext2['surfaceloops'])
volumes.AddList(ext2['volumes'])

# Write all
points.Write(f)
curves.Write(f)
lineloops.Write(f)
surfaces.Write(f)
surfaceloops.Write(f)
volumes.Write(f)

