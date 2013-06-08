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

p.Add(gmshlib.Point([0,0,0,0.5]))
p.Add(gmshlib.Point([0,4,0,0.5]))
p.Add(gmshlib.Point([0,8,0,0.5]))

l.Add(gmshlib.Circle(p[0:3]))

ext0 = l[-1].Extrude([10,0,0])

p.AddList(ext0['points'])
l.AddList(ext0['curves'])
ll.AddList(ext0['lineloops'])
#sf.AddList(ext0['surfaces'])

p.Add(p[1].Translate([5,0,0]))
p.Add(p[-1].Translate([0,1,0]))
p.Add(p[-1].Translate([1,0,0]))
p.Add(p[-1].Translate([0,-2,0]))

l.AddList(gmshlib.MakePolyLines(p[-4::1], prefix='pl'))
ll.Add(gmshlib.LineLoop(l[-4::]))

p.Add(p[-1].Translate([4,0,0]))
p.Add(p[-1].Translate([0,1,0]))
p.Add(p[-1].Translate([0,1,0]))
p.Add(p[-2].Translate([2,0,0]))

l.Add(gmshlib.Line([p[-1],p[-2]]))
l.Add(gmshlib.Line([p[-1],p[-4]]))
l.Add(gmshlib.Circle([p[-2],p[-3],p[-4]]))
ll.Add(gmshlib.LineLoop([l[-3],l[-1],l[-2]]))
#sf.Add(gmshlib.RuledSurface(ll[-1::]))
sf.Add(gmshlib.RuledSurface(ll[:]))

ext1 = sf[-1].Extrude([0,0,1], index = 1)

p.AddList(ext1['points'])
l.AddList(ext1['curves'])
ll.AddList(ext1['lineloops'])
sf.AddList(ext1['surfaces'])
sl.AddList(ext1['surfaceloops'])
vl.AddList(ext1['volumes'])

p.Write(f)
l.Write(f)
ll.Write(f)
sf.Write(f)
sl.Write(f)
vl.Write(f)
