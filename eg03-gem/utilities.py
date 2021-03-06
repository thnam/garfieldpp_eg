#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from __future__ import division

import sys
sys.path.append('../py_gmsh')

import collections

import gmshlib

# Gem parameters
lc = 2.5 # um
pitch = 140 # um
r_out = 35 # um
r_cone = 30 # um
t_copper = 5 # um
t_kapton = 50 # um
##############################################################

def MakeCopperPlate(plate_id):

  points = gmshlib.ObjectList('plate'+ str(plate_id) + '_p')
  centers = gmshlib.ObjectList('plate'+ str(plate_id) + '_cp')

  points.Add(gmshlib.Point([0,0,0,lc]))
  points.Add(points[0].Translate([pitch/2 - r_out, 0, 0]))
  centers.Add(points[0].Translate([pitch/2, 0, 0]))
  points.Add(points[0].Translate([pitch/2 + r_out, 0, 0]))
  points.Add(points[0].Translate([pitch, 0, 0]))

  points.Add(points[-1].Translate([0, pitch - r_out, 0]))
  centers.Add(points[-1].Translate([0, r_out, 0]))

  points.Add(centers[-1].Translate([-r_out, 0, 0]))
  points.Add(points[-1].Translate([- pitch + 2*r_out, 0, 0]))
  centers.Add(points[-1].Translate([-r_out, 0, 0]))

  points.Add(centers[-1].Translate([0, -r_out, 0]))

  n_p0 = len(points) # Save number of basic points
  #print (str(n_p0))
  curves = gmshlib.ObjectList('plate' + str(plate_id) +'_c')
  curves.Add(gmshlib.Line(points[0:2]))
  curves.Add(gmshlib.Circle([points[2],centers[0],points[1]]))
  curves.Add(gmshlib.Line(points[2:4]))

  curves.Add(gmshlib.Line(points[3:5]))
  curves.Add(gmshlib.Circle([points[5],centers[1],points[4]]))

  curves.Add(gmshlib.Line(points[5:7]))
  curves.Add(gmshlib.Circle([points[n_p0-1],centers[2],points[n_p0-2]]))

  curves.Add(gmshlib.Line([points[n_p0-1],points[0]]))

  lineloops = gmshlib.ObjectList('plate' + str(plate_id) +'_ll')
  lineloops.Add(gmshlib.LineLoop(curves))

  surfaces = gmshlib.ObjectList('plate' + str(plate_id) +'_sf')
  surfaces.Add(gmshlib.RuledSurface(lineloops))

  return collections.OrderedDict([('points',points),
                                  ('centers',centers),
                                  ('curves',curves),
                                  ('lineloops',lineloops),
                                  ('surfaces',surfaces)])
