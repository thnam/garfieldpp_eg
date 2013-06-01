#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function


# Class GeneralObject
class GeneralObject(object):
  """General class for all Gmsh geometry objects: points, lines, curves,
  surfaces, volumes"""

  def __init__(self, objtype, elements, label = None, idtag = None):
    """Inits an object:

    :objtype: such as Point, Line, ...
    :elements: list of elements; for Point: x, y, z; for Line: points; ...
    :label: makes .geo file reading easier
    :idtag: object id

    """
    self._elements = elements
    self._objtype = objtype
    self._label = label
    self._idtag = idtag
    if idtag is None:
      self._idtag = 'newp'
    
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
                                       self._idtag, self._objtype,
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

# Class Point
class Point(GeneralObject):
  """Point"""

  def __init__(self, elements, label = 'p0', idtag = None):
    """Inits a point with 3 coordinates, and (optional) characteristic length

    :elements: 3 coordinates, and characteristic length
    :label: 
    :idtag: @todo

    """
    GeneralObject.__init__(self, 'Point', elements, label, idtag)

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

  def Translate(self, dx, dy, dz, lc = None, label = None, idtag = None):
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

  def __init__(self, points, label = 'l0', idtag = None):
    """A line, must provide two points

    :points: list contains two points: start point and end point

    """
    if idtag is None:
      idtag = 'newc'
    GeneralObject.__init__(self, 'Line', points, label, idtag)
    
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
    return 0

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
