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

  def __init__(self, objtype,  elements, label = None, 
               n_dimension = 1,index = None, direction = None):
    """Inits an object:

    :objtype: such as Point, Line, ...
    :elements: list of elements; for Point: x, y, z; for Line: points; ...
    :label: makes .geo file reading easier
    :index: object id

    """
    self._elements = elements
    self._objtype = objtype
    self._n_dimension = n_dimension
    self._label = label
    if type(index) is int:
      self._index = index
    else:
      self._index = NextObj[objtype]
    
    self._direction = []
    if direction is None:
      for i in range(len(self._elements)):
        self._direction.append(1)
    else:
      self._direction = direction

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
        if self._direction[i] == -1:
          str_list = str_list + '-' + str(self._elements[i]._label) + ', '
        else:
          str_list = str_list + str(self._elements[i]._label) + ', '

      if self._direction[-1] == -1:
        str_list = str_list + '-' + str(self._elements[-1]._label)
      else:
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

  def SetDirection(self, vector):
    """Set direction for elements

    :vector: @todo
    :returns: @todo

    """
    self._direction = vector
    pass


class Object1D(GeneralObject):
  """Docstring for Object1D """

  def __init__(self, objtype, elements, label = None, index = None):
    """@todo: to be defined1 """
    GeneralObject.__init__(self, objtype, elements, label, 1, index)

    
class Object2D(GeneralObject):
  """General 2-D object """

  def __init__(self, objtype, elements, label = None, 
               index = None, direction = None):
    """@todo: to be defined1 """
    GeneralObject.__init__(self, objtype, elements, label, 2, index, direction)

  def Extrude(self, vector, index = 0, prefix = 'ext'):
    """Extrude a 2D object

    :vector: a list of x, y, z
    :returns: points, curves and surface

    """
    points = ObjectList(prefix + str(index) +'_p')
    curves = ObjectList(prefix + str(index) +'_c')
    lineloops = ObjectList(prefix + str(index) +'_ll')
    surfaces = ObjectList(prefix + str(index) +'_sf')
    surfaceloops = ObjectList(prefix + str(index) +'_sl')
    volumes = ObjectList(prefix + str(index) +'_vl')

    if self._elements[0]._n_dimension == 1: 
      """ 
      Lines and circle arcs
      """
      for i in range(len(self._elements)): 
        points.Add(self._elements[i].Translate(vector))

      curves.Add(Line([self._elements[-1],points[-1]]))
      curves.Add(Object2D(self._objtype, points))
      curves.Add(Line([points[0],self._elements[0]]))
      lineloops.Add(LineLoop([self,curves[0],curves[1],curves[2]]))
      surfaces.Add(RuledSurface(lineloops))
      pass

    elif type(self) is LineLoop:
      """ 
      Line loops
      """
      org_points = []
      org_points_2 = []
      new_points = []
      point_map = {}
      """ 
      fisrtly, translate all points and make a map for them; 
      then, copy original line loop to new one 
      finally, make side surfaces
      """
      for i in range(len(self._elements)): #  translating points
        for j in range(len(self._elements[i]._elements)):
          if self._elements[i]._elements[j] in org_points:
            pass
          else:
            org_points.append(self._elements[i]._elements[j])
            if j == 0 or j == len(self._elements[i]._elements) - 1:
              org_points_2.append(self._elements[i]._elements[j])
              pass
            pass
        pass

      for i in range(len(org_points)): #  mapping
        points.Add(org_points[i].Translate(vector))
        new_points.append(points[-1])
        point_map[org_points[i]._label] = new_points[-1]
        pass

      tmp_curve = []
      curve_map = {}
      for i in range(len(self._elements)): #  copying line loop
        tmp_point_list = []
        for j in range(len(self._elements[i]._elements)):
          tmp_point_list.append(
            point_map[self._elements[i]._elements[j]._label])
          pass

        curves.Add(Object2D(self._elements[i]._objtype,tmp_point_list))
        tmp_curve.append(curves[-1])
        curve_map[self._elements[i]._label] = curves[-1]
        pass

      lineloops.Add(LineLoop(tmp_curve[:]))
      surfaces.Add(RuledSurface(lineloops[-1::]))

      line_map = {}
      for i in range(len(org_points_2)): #  making side faces
        curves.Add(Line([org_points_2[i],point_map[org_points_2[i]._label]]))
        line_map[org_points_2[i]._label] = curves[-1]
        pass
      for i in range(len(self._elements)):
        lineloops.Add(
          LineLoop([
            self._elements[i],
            line_map[self._elements[i]._elements[-1]._label],
            curve_map[self._elements[i]._label],
            line_map[self._elements[i]._elements[0]._label]
          ]))
        surfaces.Add(RuledSurface([lineloops[-1]]))
        pass
      pass

    elif (type(self) is RuledSurface) or (type(self) is PlaneSurface):
      """ 
      Ruled surfaces and plane surfaces
      """
      tmp_top_ll = []
      for i in range(len(self._elements)):
        tmp_ext = self._elements[i].Extrude(vector, i, prefix + str(index)+ 's')
        points.AddList(tmp_ext['points'])
        curves.AddList(tmp_ext['curves'])
        lineloops.AddList(tmp_ext['lineloops'])
        surfaces.AddList(tmp_ext['surfaces'][1:])
        tmp_top_ll.append(tmp_ext['lineloops'][0])
        pass
      surfaces.Add(Object2D(self._objtype, tmp_top_ll[:]))

      tmp_surface_list = surfaces[:]
      tmp_surface_list.append(self)
      surfaceloops.Add(SurfaceLoop(tmp_surface_list))
      volumes.Add(Volume(surfaceloops))
      pass

    else:
      pass

    return collections.OrderedDict([('points',points),
                                    ('curves',curves),
                                    ('lineloops',lineloops),
                                    ('surfaces',surfaces),
                                    ('surfaceloops',surfaceloops),
                                    ('volumes',volumes)])

class Object3D(GeneralObject):
  """Docstring for Object3D """

  def __init__(self, objtype, elements, label = None, 
               index = None, direction = None):
    """@todo: to be defined1 """
    GeneralObject.__init__(self, objtype, elements, label, 3, index, direction)


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
    tmp_object = copy.deepcopy(an_object)
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
class Point(Object1D):
  """Point"""

  def __init__(self, elements, label = 'p0', index = None):
    """Inits a point with 3 coordinates, and (optional) characteristic length

    :elements: 3 coordinates, and characteristic length
    :label: 
    :index: @todo

    """
    Object1D.__init__(self, 'Point', elements, label, index)

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

  #def Translate(self, dx, dy, dz, lc = None, label = None, index = None):
  def Translate(self, vector, lc = None, label = None, index = None):
    """Makes new point by translation

    :label: new point's label
    :(dx, dy, dz): translation vector
    :lc: characteristic length of the next point, if needed
    :returns: new point by translation

    """
    x = self._elements[0] + vector[0]
    y = self._elements[1] + vector[1]
    z = self._elements[2] + vector[2]
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
class Line(Object2D):
  """Line, connects two points"""

  def __init__(self, points, label = 'l0', index = None, direction = None):
    """A line, must provide two points

    :points: list contains two points: start point and end point

    """
    if len(points) is not 2:
      pass
    else:
      if index is None:
        index = 'newc' 
      Object2D.__init__(self, 'Line', points, label, index, direction)
    

class Circle(Object2D):
  """Part of circle, from start point to end point"""

  def __init__(self, points, label = 'c0', index = None, direction = None):
    """A circle, must provide three points

    :points: list contains three points: start point, center point and end point

    """
    if index is None:
      index = 'newc'
    Object2D.__init__(self, 'Circle', points, label, index, direction)


class LineLoop(Object2D):
  """Closed loop of curves"""

  def __init__(self, curves, label = 'll0', index = None, direction = None):
    """A closed loop of curves

    :points: list of curves, must be in correct order and orientation

    """
    import copy
    if index is None:
      index = 'newreg'
    Object2D.__init__(self, 'Line Loop', curves, label, index, direction)

    tmpe = copy.deepcopy(self._elements) #  elements
    tmpd = copy.deepcopy(self._direction)  #  direction
    nswap = 0
    while nswap < len(tmpe):
      for i in range(len(tmpe)-1):
        if tmpd[i] == 1:
          if tmpe[i]._elements[-1]._label == tmpe[i+1]._elements[0]._label:
            pass
          else:
            tmpd[i+1] = -1
            pass 
          pass 
        elif tmpd[i] == -1:
          tmpe[i]._elements[0], tmpe[i]._elements[-1] = tmpe[i]._elements[-1], tmpe[i]._elements[0]
          self._direction[i] = -1
          tmpd = [1]*len(tmpd)
          break
        pass
      nswap += 1
      pass

    if tmpe[-1]._elements[-1]._label != tmpe[0]._elements[0]._label:
      self._direction[-1] = -1
      pass


class RuledSurface(Object2D):
  """Ruled surface"""

  def __init__(self, elements, label = 'rs0', index = None, direction = None):
    """A ruled surface from a line loop

    """
    if index is None:
      index = 'newreg'
    Object2D.__init__(self, 'Ruled Surface', elements, label, index, direction)


class PlaneSurface(Object2D):
  """Plane surface"""

  def __init__(self, elements, label = 'rs0', index = None, direction = None):
    """A plane surface from a line loop

    """
    if index is None:
      index = 'newreg'
    Object2D.__init__(self, 'Plane Surface', elements, label, index, direction)


class PhysicalSurface(Object2D):
  """Physical surface"""

  def __init__(self, elements, label = 'ps0', index = None, direction = None):
    """A physical surface

    """
    if index is None:
      index = 'newreg'
    Object2D.__init__(self, 'Physical Surface', elements, label, index,
                      direction)


class SurfaceLoop(Object3D):
  """Surface Loop"""

  def __init__(self, elements, label = 'sl0', index = None, direction = None):
    """A physical surface

    """
    if index is None:
      index = 'newreg'
    Object3D.__init__(self, 'Surface Loop', elements, label, index, direction)


class Volume(Object3D):
  """Volume"""

  def __init__(self, elements, label = 'vl0', index = None):
    """A volume

    """
    if index is None:
      index = 'newreg'
    Object3D.__init__(self, 'Volume', elements, label, index)


class PhysicalVolume(Object3D):
  """Physical Volume"""

  def __init__(self, elements, label = 'pv0', index = None):
    """A volume

    """
    if index is None:
      index = 'newreg'
    Object3D.__init__(self, 'Physical Volume', elements, label, index)


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

def MakePolyLines(points, prefix = None):
  """Makes lines through all points

  :returns: list of lines

  """
  if prefix is None:
    prefix = 'l'

  lines = ObjectList(prefix)
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
  points.Add(points[-1].Translate([lx,0,0]))
  points.Add(points[-1].Translate([0,ly,0]))
  points.Add(points[-1].Translate([-lx,0,0]))
  for i in range(len(points)):
    points.Add(points[i].Translate([0,0,lz]))

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
