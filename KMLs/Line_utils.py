'''
@file line_utils.py
@brief line utilities class for polygons
@author Adam Poirier
@version 1.0
@date 2017-02-22

Line utilities class for polygons, including common KML functions involving line placemarks
'''

from Kml_templates import *
from string import Template 

KML_Templates = KmlTemplates()



# produce a kml formatted string for a list of points
# list of points must be in the list[hop][point]{lat, lon, alt}
def line_to_kml_coords(coord_list):
  ret_kml = ''
  for hop in coord_list:
    for wp in hop:
      ret_kml += '{lon},{lat},{alt}\n'.format(**wp)
  return ret_kml

def line_to_kml(line):
  ret_kml = ''
  for point in line:
    ret_kml += '{0},{1},{2}\n'.format(*point)
  return ret_kml
  pass

# Builds a formatted KML string in a placemark 
# substitutes into respective placemark dict for live lines or simple lines
def build_line_kml(name, kml_coords, style, flat = False, extrude = False, tessellate = False, visible = True, live = False, mode = 'absolute'):
  # modes: 
  # absolute
  # relativeToGround

  line_dict = {}
  type_dict = {}

  # ensures that the given style is supported
  #TODO abstract out
  if style[0] == '#':
    if style in KML_Templates.STYLES.values():
      style_ = style
    elif style in KML_Templates.STYLES.keys():
      style_ = KML_Templates.STYLES[style]
      print 'Error with input styles, using generic style NFZ: ' + name +style
      style_ = KML_Templates.STYLES['NFZ']
  else:
    try:
      style_ = KML_Templates.STYLES[style]
    except Exception as e:
      print e
      print 'Error with input styles, using generic style NFZ: ' + name +style
      style_ = KML_Templates.STYLES['NFZ']    

  # parse func input
  type_dict['altitude_mode'] = mode
  line_dict['style'] = style_
  type_dict['extrude'] = int(extrude)
  type_dict['tessellate'] = int(tessellate)
  line_dict['visible'] = int(visible)
  line_dict['line_name'] = name

  # flat indicates that the polygons are clamped to the ground
  if flat:
    type_dict['extrude'] = 0
    type_dict['tessellate'] = 1
    type_dict['altitude_mode'] = 'clampedToGround'

  # live means that the coordinates have a time associated with them
  if live:
    base_template = KML_Templates.TrackLine
    type_dict['track_id'] = name + ' track'
    type_dict['track_points'] = kml_coords
  else:
    base_template = KML_Templates.BasicLine
    type_dict['coords'] = kml_coords

  # substitute the type of line (live track or regular) into the overall line template
  line_dict['line_type'] = Template(base_template).substitute(type_dict)
  line_kml = Template(KML_Templates.LineTemplate).substitute(line_dict)

  return line_kml

# produces a KML formatted string for position data with an associated time
def kml_track_line(pos_data):
  coord_kml = ''
  for point in pos_data:
    coord_kml += "\n\t\t<when>{time}</when><gx:coord>{lon} {lat} {alt}</gx:coord>".format(**point)
  return coord_kml