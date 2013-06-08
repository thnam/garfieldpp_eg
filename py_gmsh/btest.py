#!/usr/bin/env python
# encoding: utf-8
import gmshlib
f = open('newtest.geo','w')

p = gmshlib.ObjectList('p')
l = gmshlib.ObjectList('l')
ll = gmshlib.ObjectList('ll')
sf = gmshlib.ObjectList('sf')
sl = gmshlib.ObjectList('sl')
vl = gmshlib.ObjectList('vl')

p.Add(gmshlib.Point([0,0,0,0.2]))
p.Add(gmshlib.Point([0,2,0,0.2]))
p.Add(gmshlib.Point([0,4,0,0.2]))

l.Add(gmshlib.Circle(p[0:3]))

ext0 = l[-1].Extrude([5,0,0])

p.AddList(ext0['points'])
l.AddList(ext0['curves'])
ll.AddList(ext0['lineloops'])
sf.AddList(ext0['surfaces'])
sl.AddList(ext0['surfaceloops'])
vl.AddList(ext0['volumes'])

#ext1 = ll[-1].Extrude([0,0,1], index = 1)
ext1 = sf[-1].Extrude([0,0,1], index = 1)

p.AddList(ext1['points'])
l.AddList(ext1['curves'])
ll.AddList(ext1['lineloops'])
sf.AddList(ext1['surfaces'])
sl.AddList(ext1['surfaceloops'])
vl.AddList(ext1['volumes'])

#sl.Add(gmshlib.SurfaceLoop(sf))
#vl.Add(gmshlib.Volume(sl))

p.Write(f)
l.Write(f)
ll.Write(f)
sf.Write(f)
sl.Write(f)
vl.Write(f)
