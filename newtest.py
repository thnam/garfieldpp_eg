#!/usr/bin/env python
# encoding: utf-8
import gmshlib
f = open('newtest.geo','w')

#box1 = gmshlib.MakeRectangularBox(3,2,4,0.2)
#for key in box1:
  #if (key is not 'volumes') and (key is not 'surfaceloops'):
    #box1[key].Write(f)

#box2 = gmshlib.MakeRectangularBox(6,2.5,4.5,0.3, center = [1,0,0], box_id = 1)
#for key in box2:
  #if key is not 'volumes':
    #box2[key].Write(f)

#inner_vol = gmshlib.PhysicalVolume(box1['volumes'])
#outer_vol = gmshlib.PhysicalVolume(box2['volumes'])
#inner_vol = box1['surfaceloops']
#outer_vol = box2['surfaceloops']
#shell = gmshlib.Volume([outer_vol[0],inner_vol[0]])
#shell.Write(f)
#pv = gmshlib.PhysicalVolume([shell])
#pv.Write(f)
#inner_vol.Write(f)
#outer_vol.Write(f)
#a = gmshlib.Point([1,1,1,.1],label = 'aa', idtag = 1)
#a.Write(f)

p = gmshlib.ObjectList('p')
l = gmshlib.ObjectList('l')
ll = gmshlib.ObjectList('ll')
sf = gmshlib.ObjectList('sf')

p.Add(gmshlib.Point([0,0,0,0.2]))
p.Add(gmshlib.Point([0,5,0,0.2]))
p.Add(gmshlib.Point([0,10,0,0.2]))

l.Add(gmshlib.Line(p[0:2]))
l.Add(gmshlib.Circle(p[0:3]))

ex = l[0].Extrude([-7,0,0])
p.AddList(ex['points'])
l.AddList(ex['lines'])
p.Add(p[-1].Translate(0,2,0))
ll.AddList(ex['lineloops'])
sf.AddList(ex['surfaces'])

ex = l[1].Extrude([0,0,2], index=1)
p.AddList(ex['points'])
l.AddList(ex['curves'])
ll.AddList(ex['lineloops'])
sf.AddList(ex['surfaces'])


p.Write(f)
l.Write(f)
ll.Write(f)
sf.Write(f)
