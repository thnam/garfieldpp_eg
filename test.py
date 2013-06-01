#!/usr/bin/env python
# encoding: utf-8
import gmshlib
f = open('test.geo','w')

point = []
point.append(gmshlib.GeneralObject('Point',[0,1,0, 0.1],'p0'))
point.append(gmshlib.Point([0,0,1, 0.1],label = 'pp'))
point.append(point[1].Translate(1,1,1))

gmshlib.WriteAll(point,f)

line = []
line.append(gmshlib.Line(point[1:3]))

gmshlib.WriteAll(line,f)
