'''
@file polygon_utils.py
@brief general polygon utilities class for polygons
@author Adam Poirier
@version 1.0
@date 2017-02-22

polygon utilities class for polygons
'''

import sys
import os
import re
from string import Template

sys.path.insert(0, os.getcwd() + '/..')
import Kml_utils
from Kml_templates import *
from Kml_debug import *

KML_Templates = KmlTemplates()



'''
1  2        5  6
  - - - - - - 
3  4        7  8'''
# constructs six sets of polygon points that form 
# a floating bounding box around the specified points
def build_split_poly(point_list):
  ret_lst = []
  for i, hop in enumerate(point_list):
    for j, point in enumerate(hop):
      if i == 0 and j == 0:
        prev = point
      else:
        a,b,c,d = prev
        e,f,g,h = point
        # pattern created 6 sided box
        ret_lst.append((a,b,f,e,a))
        ret_lst.append((c,d,h,g,c))
        ret_lst.append((a,c,d,b,a))
        ret_lst.append((e,f,h,g,e))
        ret_lst.append((b,d,h,f,b))
        ret_lst.append((a,e,g,c,a))
        prev = point

  return ret_lst


# function creates nested folders, turning group of 6 flat polys into one poly folder
# connecting points must be removed
# artifact of turning continuous points into polygons
def order_split_poly(poly_points, name, style, flat):
  t_count = 0                         # count for the tunnel LZ number
  np = [None for i in range(6)]       # node point
  base_poly = ''                      # kml return string
  # every other group of 6, including the last group is valid (for each hop (zone))
  # group of 6 because a cube has 6 sides
  for i, zone in enumerate(poly_points):
    if (i >= len(poly_points) - 6):
      ready_poly = True
      np[i%6] = zone
    if (i % 12 < 6):
      ready_poly = True
      # np.append(zone)
      np[i%12] = zone
    else:
      # if a polygon hasn't already been built for this set of 6, build it
      if ready_poly:
        t_count += 1
        # create a flat rectangular for each segment, and add it to the KML string
        base_poly += build_poly(np, name + ' ' + str(t_count), style, flat = flat)
      ready_poly = False

  # duplicated in order to get the last tunnel
  if ready_poly:
    t_count += 1
    base_poly += build_poly(np, name + ' ' + str(t_count), style, flat = flat)
    ready_poly = False
  

  return Kml_utils.kml_folder(name + 's', base_poly)

# Assembles a polygon 
# Returns: KML folder for the poly list given
def build_poly(poly_list, arg_name, style, flat = False, extrude = False, show = True, shell = False, folder=True):
  ind_poly = ''
  lst_name = False
  poly_d = {}
  poly_template = KML_Templates.PolygonTemplate
  folder_template = KML_Templates.FolderTemplate

  # if flat flag is set: clamp the polygon to the ground
  if flat:
    poly_d['altitudeMode'] = 'clampedToGround'
    poly_d['tessellate'] = str(1)
  else:
    poly_d['altitudeMode'] = 'absolute'
    poly_d['tessellate'] = str(0)


  # if arg name is a list of a new name per zone, assign names accordingly
  # test for given input names as strings or lists, else try to assign with RE
  if type(arg_name) in (list, tuple):
    lst_name = True
    name_= iter(arg_name)
  else:
    name_ = arg_name
  for i, zone in enumerate(poly_list):
    if lst_name:
      name = next(name_)
      re_obj = re.match(r'([a-zA-Z]*( )?)*', name)
      if re_obj:
        f_name = re_obj.group()
      else:
        f_name = name
    else:
      name = name_ + ' # ' + str(i)
      f_name = arg_name

    if shell:
      poly_d['innerCoords'] = poly_to_kml(zone, alt_ajust = -6000)
    else:
      poly_d['innerCoords'] = ''
    poly_d['coords'] = poly_to_kml(zone)
    poly_d['extrude'] = int(extrude)
    poly_d['visible'] = int(show)
    poly_d['name'] = name
    poly_d['style'] = style

    ind_poly += Template(poly_template).substitute(poly_d)
  if folder:
    ret_kml = Kml_utils.kml_folder(f_name, ind_poly)
  else:
    ret_kml = ind_poly
  return ret_kml
  
# processes the poly_list into kml format.
# assumes that the list is in the correct order, thus simply connects points
# poly_list: poly_list[polygon#][point]{'lat': 0, 'lon': 0, 'alt': 0}     --> in decimal degrees
def poly_to_kml(poly_list, alt_ajust = 0, tab_count = 4, height_set = None):
  ret_kml = ''
  spacer = '\t' * tab_count
  for point in poly_list:
    if height_set:
      alt = height_set
    else:
      alt = point['alt'] + alt_ajust
    ret_kml += spacer + '{0},{1},{2}\n'.format(point['lon'], point['lat'], alt)
  return ret_kml

# creates floating polygons, given upper and lower planar sets (planes do not have to be 'flat')
def build_float_poly(uppers, lowers, names, ind_name, style, flat, folder=True):
  tmp_poly = ''
  ret_polys = ''
  for i in range(len(lowers)):
    for j, tp in enumerate(zip(uppers[i], lowers[i])):
      up, down = tp
      if j == 0:
        prev_u = up
        prev_d = down
      else:
        order = (prev_u, prev_d, down, up)
        tmp_poly += build_poly([order], ind_name + ' Wall ' + str(j), style, flat=flat, folder = False)
        prev_u = up
        prev_d = down
    tmp_poly += build_poly([uppers[i]], ind_name + ' Top', style, flat = flat, folder = False)
    tmp_poly += build_poly([lowers[i]], ind_name + ' Bottom', style, flat = flat, folder = False)
    if type(names) in (list, tuple):
      zone_poly = Kml_utils.kml_folder(names[i] + '-' + str(i), tmp_poly)
    else:
      zone_poly = Kml_utils.kml_folder(names + '-' + str(i), tmp_poly)
    ret_polys += zone_poly
    tmp_poly = ''
  if folder:
    ret_polys = Kml_utils.kml_folder(ind_name, ret_polys)

  return ret_polys
