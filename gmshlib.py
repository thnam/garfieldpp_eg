#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
import collections
#from __future__ import division

# Dictionary for next Gmsh object
NextObj = {'Point':'newp',
           'Line':'newl',
           'Circle':'newc',
           'Line Loop':'newll',
           'Plane Surface':'news',
           'Ruled Surface':'news',
           'Physical Surface':'news',
           'Surface Loop':'newsl',
           'Volume':'newv',
           'Physical Volume':'newv'
           }

# Class GeneralObject
class GeneralObject(object):
  """General class for all Gmsh geometry objects: points, lines, curves,
  surfaces, volumes"""

  def __init__(self, objtype, elements, label = None, index = None):
    """Inits an object:

    :objtype: such as Point, Line, ...
    :elements: list of elements; for Point: x, y, z; for Line: points; ...
    :label: makes .geo file reading easier
    :index: object id

    """
    self._elements = elements
    self._objtype = objtype
    self._label = label
    if type(index) is int:
      self._index = index
    else:
      self._index = NextObj[objtype]
    
  def __str__(self):
    """Will be called by str() function

    :returns: Gmsh declaration for the object

    """
    str_list = ''

    try:
      #for element in self._elements:
        #if element == self._elements[-1]:
          #str_list = str_list + str(element._label)
        #else:
          #str_list = str_list + str(element._label) + ', '
      for i in range(len(self._elements) - 1): 
        str_list = str_list + str(self._elements[i]._label) + ', '
      str_list = str_list + str(self._elements[-1]._label)

    except AttributeError: # in case of elements are coordinates
      for i in range(len(self._elements) - 1): 
        str_list = str_list + str(self._elements[i]) + ', '
      str_list = str_list + str(self._elements[-1])

    return '%s = %s; %s(%s) = {%s};' %(self._label, 
                                       self._index, self._objtype,
                                       self._label,str_list)

  def Reverse(self):
    """Reverse the direction of the object, use for lines, loops, surfaces

    :returns: @todo

    """
    newobj = GeneralObject(self._objtype,self._elements, '-' + self._label)
    return newobj

  def Write(self, outputfile):
    """Writes declaration to a file

    :outputfile: must be defined before calling this function

    """
    print(str(self),file=outputfile)
    pass

  def SetLabel(self, new_label):
    """Set new label

    :new_label: @todo
    :returns: @todo

    """
    self._label = new_label
    pass

  def GetLabel(self):
    """Gets label from the object
    :returns: @todo

    """
    return self._label

  def Setindex(self, index):
    """Set id tag 

    :index: @todo
    :returns: @todo

    """
    self._index = index
    pass

# Class GeneralList
class ObjectList(object):
  """General class for all object lists"""

  def __init__(self, prefix, start_index = None):
    """Inits a list

    :prefix:  will be used for all objects in the list

    """
    self._list = []
    self._prefix = prefix
    self._start_index = start_index

  def Add(self, an_object):
    """Adds an object to the list

    :an_object: @todo
    :returns: @todo

    """
    import copy
    tmp_object = copy.copy(an_object)
    if (len(self._list) == 0) and (type(self._start_index) is int):
      tmp_object.Setindex(self._start_index)
    else:
      try:
        tmp_object.SetLabel(self._prefix + str(len(self)))
      except IndexError:
        tmp_object.SetLabel(GetNextLabel(self._prefix))
      except AttributeError:
        pass

    self._list.append(tmp_object)
    pass

  def AddList(self, a_list):
    """Add a list of objects

    :a_list: @todo
    :returns: @todo

    """
    for i in range(len(a_list)):
      self._list.append(a_list[i])
    pass

  def Write(self, outputfile):
    """Write all elements in the list to a file

    :outputfile: @todo
    :returns: @todo

    """
    WriteAll(self._list,outputfile)
    pass

  def __len__(self):
    return len(self._list)
  
  def __getitem__(self, key):
    return self._list[key]
  
  def __setitem__(self, key, value):
    self._list[key] = value
    pass


class LineList(ObjectList):
  """List of lines"""

  def __init__(self, prefix = 'l'):
    """Inits a list of lines

    :prefix: @todo

    """
    ObjectList.__init__(self, prefix)
    
  def PolyLines(self, points):
    """Makes lines from a list of points

    :points: @todo
    :returns: @todo

    """
    for i in range(len(points) - 1):
      self.Add(Line(points[i:i+2]))
    self.Add(Line([points[len(points)-1],points[0]]))
    pass

# Class Point
class Point(GeneralObject):
  """Point"""

  def __init__(self, elements, label = 'p0', index = None):
    """Inits a point with 3 coordinates, and (optional) characteristic length

    :elements: 3 coordinates, and characteristic length
    :label: 
    :index: @todo

    """
    GeneralObject.__init__(self, 'Point', elements, label, index)

  def GetDistance(self, otherpoint):
    """Calculates distance from the current point to another point

    :otherpoint: @todo
    :returns: @todo

    """
    import math
    dx = self._elements[0] - otherpoint._elements[0]
    dy = self._elements[1] - otherpoint._elements[1]
    dz = self._elements[2] - otherpoint._elements[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

  def Translate(self, dx, dy, dz, lc = None, label = None, index = None):
    """Makes new point by translation

    :label: new point's label
    :(dx, dy, dz): translation vector
    :lc: characteristic length of the next point, if needed
    :returns: new point by translation

    """
    x = self._elements[0] + dx
    y = self._elements[1] + dy
    z = self._elements[2] + dz
    new_elements = []

    try:
      lc = self._elements[3]
      new_elements = [x,y,z,lc]
    except IndexError:
      new_elements = [x,y,z]

    if label is None:
      label = GetNextLabel(self._label)

    return Point(new_elements, label)

    
# Class Line
class Line(GeneralObject):
  """Line, connects two points"""

  def __init__(self, points, label = 'l0', index = None):
    """A line, must provide two points

    :points: list contains two points: start point and end point

    """
    if len(points) is not 2:
      pass
    else:
      if index is None:
        index = 'newc' 
      GeneralObject.__init__(self, 'Line', points, label, index)
    
  def Extrude(self, vector, index = 0):
    """Extrude a line

    :vector: a list of x, y, z
    :returns: points, lines and surface

    """
    points = ObjectList('ext' + str(index) +'_p')
    lines = ObjectList('ext' + str(index) +'_l')
    lineloops = ObjectList('ext' + str(index) +'_ll')
    surfaces = ObjectList('ext' + str(index) +'_sf')
    points.Add(self._elements[0].Translate(vector[0],vector[1],vector[2]))
    points.Add(self._elements[1].Translate(vector[0],vector[1],vector[2]))
    lines.Add(Line([self._elements[1],points[1]]))
    lines.Add(Line([points[1],points[0]]))
    lines.Add(Line([points[0],self._elements[0]]))
    lineloops.Add(LineLoop([self,lines[0],lines[1],lines[2]]))
    surfaces.Add(RuledSurface(lineloops))
    return collections.OrderedDict([('points',points),
                                    ('lines',lines),
                                    ('lineloops',lineloops),
                                    ('surfaces',surfaces)])

class Circle(GeneralObject):
  """Part of circle, from start point to end point"""

  def __init__(self, points, label = 'c0', index = None):
    """A circle, must provide three points

    :points: list contains three points: start point, center point and end point

    """
    if index is None:
      index = 'newc'
    GeneralObject.__init__(self, 'Circle', points, label, index)

  def Extrude(self, vector, index = 0):
    """Extrude a line

    :vector: a list of x, y, z
    :returns: points, lines and surface

    """
    points = ObjectList('ext' + str(index) +'_p')
    curves = ObjectList('ext' + str(index) +'_c')
    lineloops = ObjectList('ext' + str(index) +'_ll')
    surfaces = ObjectList('ext' + str(index) +'_sf')
    points.Add(self._elements[0].Translate(vector[0],vector[1],vector[2]))
    points.Add(self._elements[1].Translate(vector[0],vector[1],vector[2]))
    points.Add(self._elements[2].Translate(vector[0],vector[1],vector[2]))
    curves.Add(Line([self._elements[2],points[2]]))
    curves.Add(Circle(points))
    #lines.Add(Line([points[1],points[0]]))
    curves.Add(Line([points[0],self._elements[0]]))
    lineloops.Add(LineLoop([self,curves[0],curves[1].Reverse(),curves[2]]))
    surfaces.Add(RuledSurface(lineloops))
    return collections.OrderedDict([('points',points),
                                    ('curves',curves),
                                    ('lineloops',lineloops),
                                    ('surfaces',surfaces)])


class LineLoop(GeneralObject):
  """Closed loop of curves"""

  def __init__(self, curves, label = 'll0', index = None):
    """A closed loop of curves

    :points: list of curves, must be in correct order and orientation

    """
    if index is None:
      index = 'newreg'
    GeneralObject.__init__(self, 'Line Loop', curves, label, index)


class RuledSurface(GeneralObject):
  """Ruled surface"""

  def __init__(self, elements, label = 'rs0', index = None):
    """A ruled surface from a line loop

    """
    if index is None:
      index = 'newreg'
    GeneralObject.__init__(self, 'Ruled Surface', elements, label, index)


class PlaneSurface(GeneralObject):
  """Plane surface"""

  def __init__(self, elements, label = 'rs0', index = None):
    """A plane surface from a line loop

    """
    if index is None:
      index = 'newreg'
    GeneralObject.__init__(self, 'Plane Surface', elements, label, index)


class PhysicalSurface(GeneralObject):
  """Physical surface"""

  def __init__(self, elements, label = 'ps0', index = None):
    """A physical surface

    """
    if index is None:
      index = 'newreg'
    GeneralObject.__init__(self, 'Physical Surface', elements, label, index)


class SurfaceLoop(GeneralObject):
  """Surface Loop"""

  def __init__(self, elements, label = 'sl0', index = None):
    """A physical surface

    """
    if index is None:
      index = 'newreg'
    GeneralObject.__init__(self, 'Surface Loop', elements, label, index)


class Volume(GeneralObject):
  """Volume"""

  def __init__(self, elements, label = 'vl0', index = None):
    """A volume

    """
    if index is None:
      index = 'newreg'
    GeneralObject.__init__(self, 'Volume', elements, label, index)


class PhysicalVolume(GeneralObject):
  """Physical Volume"""

  def __init__(self, elements, label = 'pv0', index = None):
    """A volume

    """
    if index is None:
      index = 'newreg'
    GeneralObject.__init__(self, 'Physical Volume', elements, label, index)


###############################################################################
###############################################################################
# Generally useful functions
###############################################################################

def WriteAll(alist, outputfile):
  """Writes all elements of a list"""
  for i in range(len(alist)):
    alist[i].Write(outputfile)
  pass

def GetIndex(label):
  """Get index from a label

  :label: label of an object, assuming the index is always at the end
  :returns: index in that label, in case no index is found, return 0

  """
  import re
  match = re.search('\d+$',label)
  try:
    return int(match.group(0))
  except AttributeError:
    return -1

def GetPrefix(label):
  """Get prefix from a label

  :label: 
  :returns: the string before the index, if no index, return original label

  """
  import re
  match = re.search('\d+$',label)
  try:
    return label[:-len(match.group(0))]
  except AttributeError:
    return label

def GetNextLabel(label):
  """Gets the next label with incrmented index

  :label: @todo
  :returns: @todo

  """
  return GetPrefix(label) + str(GetIndex(label) + 1)

def MakePolyLines(points):
  """Makes lines through all points

  :returns: list of lines

  """
  lines = ObjectList('l')
  for i in range(len(points) - 1):
    lines.Add(Line(points[i:i+2]))
  lines.Add(Line([points[len(points)-1],points[0]]))
  return lines

def MakeRectangularBox( lx, ly, lz, lc, center = [0,0,0], box_id = 0):
  """Makes a rectangular box

  :center: [x0, y0, z0]
  :lx, ly, lz: length in x, y, z
  :lc: characteristic length
  :returns: list of points, lines, line loops, surface, volume

  """
  x0 = center[0]
  y0 = center[1]
  z0 = center[2]
  id_prefix = 'box' + str(box_id) + '_'

  points = ObjectList(id_prefix + 'p')
  points.Add(Point([x0 - lx/2., y0 - ly/2., z0 - lz/2., lc]))
  points.Add(points[-1].Translate(lx,0,0))
  points.Add(points[-1].Translate(0,ly,0))
  points.Add(points[-1].Translate(-lx,0,0))
  for i in range(len(points)):
    points.Add(points[i].Translate(0,0,lz))

  lines = LineList(id_prefix + 'l')
  lines.PolyLines(points[0:4])
  lines.PolyLines(points[4:8])
  lines.Add(Line([points[4],points[0]]))
  lines.Add(Line([points[1],points[5]]))
  lines.Add(Line([points[6],points[2]]))
  lines.Add(Line([points[3],points[7]]))

  lineloops = ObjectList(id_prefix + 'll')
  lineloops.Add(LineLoop([lines[0],lines[9],lines[4].Reverse(),lines[8]]))
  lineloops.Add(LineLoop(lines[0:4]))
  lineloops.Add(LineLoop([lines[1].Reverse(),lines[9],lines[5],lines[10]]))
  lineloops.Add(LineLoop([lines[2],lines[11],lines[6].Reverse(),lines[10]]))
  lineloops.Add(LineLoop(lines[4:8]))
  lineloops.Add(LineLoop([lines[3].Reverse(),lines[11],lines[7],lines[8]]))
  #lineloops.Add(LineLoop(lines[0:4]))
  #lineloops.Add(LineLoop(lines[4:8]))
  #lineloops.Add(LineLoop([lines[0],lines[9],lines[4].Reverse(),lines[8]]))
  #lineloops.Add(LineLoop([lines[1].Reverse(),lines[9],lines[5],lines[10]]))
  #lineloops.Add(LineLoop([lines[2],lines[11],lines[6].Reverse(),lines[10]]))
  #lineloops.Add(LineLoop([lines[3].Reverse(),lines[11],lines[7],lines[8]]))
  
  surfaces = ObjectList(id_prefix + 'sf')
  for i in range(len(lineloops)):
    surfaces.Add(PlaneSurface([lineloops[i]]))
  #surface.Add(PhysicalSurface(lineloop[0:1]))
  #surface.Add(PhysicalSurface(lineloop[1:2]))
  
  surfaceloops = ObjectList(id_prefix + 'sl')
  surfaceloops.Add(SurfaceLoop(surfaces))
  
  volumes = ObjectList(id_prefix + 'vol')
  volumes.Add(Volume(surfaceloops))
  #volumes.Add(PhysicalVolume([volumes[0]])) 

  return collections.OrderedDict([('points',points),
                                  ('lines',lines),
                                  ('lineloops',lineloops),
                                  ('surfaces',surfaces),
                                  ('surfaceloops',surfaceloops),
                                  ('volumes',volumes)])
