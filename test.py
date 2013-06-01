#!/usr/bin/env python
# encoding: utf-8
import gmshlib
f = open('test.geo','w')

point = gmshlib.ObjectList('p')
point.Add(gmshlib.Point([2,0,0,.1]))
point.Add(point[-1].Translate(0,1,0))
point.Add(point[-1].Translate(-2,0,0))
point.Add(point[-1].Translate(0,-1,0))

point.Write(f)

curve = gmshlib.ObjectList('c')
curve.Add(gmshlib.Line([point[0], point[1]], idtag = 200))
curve.Add(gmshlib.Line([point[1], point[2]]))
curve.Add(gmshlib.Line(point[2:4]))

curve.Write(f)


