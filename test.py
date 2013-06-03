#!/usr/bin/env python
# encoding: utf-8
import gmshlib
f = open('test.geo','w')

point = gmshlib.ObjectList('p')
point.Add(gmshlib.Point([2,0,0,.1]))
point.Add(point[-1].Translate(0,1,0))
point.Add(point[-1].Translate(-2,0,0))
point.Add(point[-1].Translate(0,-1,0))

for i in range(len(point)):
  point.Add(point[i].Translate(0,0,5))

point.Write(f)

curve = gmshlib.LineList('c')
curve.PolyLines(point[0:4])
curve.PolyLines(point[4:8])
curve.Add(gmshlib.Line([point[4],point[0]]))
curve.Add(gmshlib.Line([point[1],point[5]]))
curve.Add(gmshlib.Line([point[6],point[2]]))
curve.Add(gmshlib.Line([point[3],point[7]]))

curve.Write(f)

lineloop = gmshlib.ObjectList('ll')
lineloop.Add(gmshlib.LineLoop(curve[0:4]))
lineloop.Add(gmshlib.LineLoop(curve[4:8]))
lineloop.Add(gmshlib.LineLoop([curve[0],curve[9],curve[4].Reverse(),curve[8]]))
lineloop.Add(gmshlib.LineLoop([curve[1].Reverse(),curve[9],curve[5],curve[10]]))
lineloop.Add(gmshlib.LineLoop([curve[2],curve[11],curve[6].Reverse(),curve[10]]))
lineloop.Add(gmshlib.LineLoop([curve[3].Reverse(),curve[11],curve[7],curve[8]]))

lineloop.Write(f)

surface = gmshlib.ObjectList('sf')
for i in range(len(lineloop)):
  surface.Add(gmshlib.RuledSurface([lineloop[i]]))
surface.Add(gmshlib.PhysicalSurface(lineloop[0:1]))
surface.Add(gmshlib.PhysicalSurface(lineloop[1:2]))

surface.Write(f)

surfaceloop = gmshlib.ObjectList('sl')
surfaceloop.Add(gmshlib.SurfaceLoop(surface[0:-2]))
surfaceloop.Write(f)

vol = gmshlib.ObjectList('vol')
vol.Add(gmshlib.Volume(surfaceloop))
vol.Add(gmshlib.PhysicalVolume([vol[0]]))

vol.Write(f)
