#!/usr/bin/env python
# encoding: utf-8
import sys
sys.path.append('../py_gmsh')

import gmshlib
f = open('cap.geo','w')

# Outer box
box1 = gmshlib.MakeRectangularBox(2,2,2,0.1)
for key in box1:
  box1[key].Write(f)

# Inner box
box2 = gmshlib.MakeRectangularBox(1.,1.,1,0.1, center = [0,0,0], box_id = 1)
for key in box2:
  box2[key].Write(f)

ps = gmshlib.ObjectList('ps')
ps.Add(gmshlib.PhysicalSurface([box2['surfaces'][1]]))
ps.Add(gmshlib.PhysicalSurface([box2['surfaces'][4]]))
ps.Write(f)

inner_sf = box2['surfaceloops']
outer_sf = box1['surfaceloops']
outer_vol = gmshlib.Volume([outer_sf[0],inner_sf[0]])
outer_vol.Write(f)

pv = gmshlib.ObjectList('pv')
pv.Add(gmshlib.PhysicalVolume([outer_vol,box2['volumes'][0]]))
pv.Add(gmshlib.PhysicalVolume(box2['volumes']))
pv.Write(f)
