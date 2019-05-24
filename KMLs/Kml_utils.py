'''
@file kml_utils.py
@brief general utilities class for polygons
@author Adam Poirier
@version 1.0
@date 2017-02-22

General utilities class for polygons, including common KML functions
'''

import math
import time
from string import Template
from Kml_templates import *

KML_Templates = KmlTemplates()

# recursively flatten lists
# def flatten(lst):
def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

# returns covert ions for distance at the specified latitude
# Tested at distances up to 2km, very accurate 
# (meters per degree)
def dist_at_lat(lat_d):
  # constants for great circle calculations
  m1 = 111132.92;   # latitude calculation term 1
  m2 = -559.82;     # latitude calculation term 2
  m3 = 1.175;       # latitude calculation term 3
  m4 = -0.0023;     # latitude calculation term 4
  p1 = 111412.84;   # longitude calculation term 1
  p2 = -93.5;       # longitude calculation term 2
  p3 = 0.118;       # longitude calculation term 3

  lat = math.radians(lat_d)

  lat_dist = m1 + (m2 * math.cos(2 * lat)) + (m3 * math.cos(4 * lat)) + (m4 * math.cos(6 * lat))
  lon_dist = (p1 * math.cos(lat)) + (p2 * math.cos(3 * lat)) + (p3 * math.cos(5 * lat));
  return lat_dist  , lon_dist 

# create init values for the template dictionary
def init_d_template():
  d = {}
  d['document_name'] = 'Document Name'
  d['document_snippet'] = ''
  d['document_description'] = 'Document Description'
  d['master_data'] = ''
  return d


# Calculates the bearing between two points
# Uses the 'Great Sphere approximation'
def get_bearing(lat, lon, n_lat, n_lon):
  lat1 = math.radians(lat)
  lat2 = math.radians(n_lat)
  diff_lon = math.radians(n_lon - lon)

  x = math.sin(diff_lon) * math.cos(lat2)
  y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_lon))

  bearing_init = math.atan2(x,y)
  bearing_init = math.degrees(bearing_init)
  bearing = (bearing_init + 360) % 360

  return bearing

# returns a string representing a folder in KML of a continuous line tunnel
def continuous_tunnel_kml(tunnel_line_coordinates, flat):
  tunnel_kmls = ''
  tl_c = ''
  tr_c = ''
  bl_c = ''
  br_c = ''

  for hop in range(len(tunnel_line_coordinates)):
    for wp in range(len(tunnel_line_coordinates[hop])):
      tlp, trp, blp, brp = tunnel_line_coordinates[hop][wp]

      # kml format is: (lon, lat, alt)
      tl_c += "{lon},{lat},{alt}\n".format(**tlp)
      tr_c += "{lon},{lat},{alt}\n".format(**trp)
      bl_c += "{lon},{lat},{alt}\n".format(**blp)
      br_c += "{lon},{lat},{alt}\n".format(**brp)

  t_names = ('Top Left', 'Top Right', 'Bottom Left', 'Bottom Right')
  # build up a string of placemark lines
  for coords, name in zip((tl_c, tr_c, bl_c, br_c) , t_names):
    tunnel_kmls += build_line_kml(name, coords, 'TUNNEL', flat = flat)
  # wrap placemark line into a folder
  full_t_kml = kml_folder('Tunnels', tunnel_kmls)

  return full_t_kml

# return UTM time zone based off of flight way-points and the UTM via args
# Future: Move the UTM offset code in here (currently in parse_pose_topic.py)
def get_utm(given_utm, list_utm):
  # if utm list is homogeneous
  if list_utm[1:] == list_utm[:-1]:
    if given_utm != list_utm[0]:
      if given_utm == -1:
        # utm is not default -1
        utm_ = list_utm[0]
      else:
        print '{:*^60}'.format('Error')
        print 'Discrepancy between way-point UTM zone and given UTM zone'
        print 'Using given UTM zone, plot may be affected'
        utm_ = given_utm
    else:
      # given UTM and wp UTM zones are the same
      utm_ = given_utm

  else:
    # the UTM time zone changes in the way-point set
    if given_utm == -1:
      # set UTM zone to most common UTM zone
      utm_ = max(set(list_utm), key=list_utm.count)
  return utm_

# returns the UTM northing letter based off of latitude
def get_utm_north_letter(lat):
  northern_zones = ['N','P','Q','R','S','T','U','V','W','X']
  southern_zones = ['M','L','K','J','H','G','F','E','D','C']
  if lat > 0:
    index = int(lat) / 8
    zone = northern_zones[index]
  else:
    index = int(-lat) / 8
    zone = southern_zones[index]

  return zone

def kml_folder(f_name, data):
  sub = {'folderName':f_name, 'data':data}
  return Template(KML_Templates.FolderTemplate).substitute(sub)

# make a point in raw kml
def kml_point(name, coords, float_ = True, show = True):
  c_kml = '{lon},{lat},{alt}\n'.format(**coords)
  if float_:
    am = 'absolute'
  else:
    am = 'clampedToGroud'

  show = int(show)
  
  sub = {'coords':c_kml, 'name':name, 'altitudeMode':am, 'visible':show}
  return Template(KML_Templates.Point).substitute(sub)


# define where the camera should point
# centers around the track
def look_at_loc(pose_coords):
  time_log = []             # list of UTCs for each track point
  lats = []                 # list of lats
  lons = []                 # list of lons
  d = {}
  
  try:
    for point in pose_coords:
      time_log.append(point['time'])
      lats.append(point['lat'])
      lons.append(point['lon'])
  except:
    time_log = pose_coords['time']
    lats = pose_coords['lat']
    lons = pose_coords['lon']
  
  # position the camera at the general center of the track points
  minLat = min(lats)
  maxLat = max(lats)
  minLon = min(lons)
  maxLon = max(lons)
  diffLat = maxLat - minLat
  diffLon = maxLon - minLon
  if minLat > 0:
    centerLat = minLat + diffLat / 2
  else:
      centerLat = minLat - diffLat / 2
  if maxLat > 0:
    centerLon = minLon + diffLon / 2
  else:
    centerLon = minLon - diffLon / 2
  v_range = (diffLat + diffLon) / 2 * 180000


  if diffLat > diffLon:
    v_head = 270 + 15 / (diffLat / diffLon)
  else:
    v_head = 0 + 15 / (diffLon / diffLat)

  d['lookat_starttime'] = min(time_log)
  d['lookat_endtime'] = max(time_log)
  d['lookat_lon'] = centerLon # Look at the landing point when loading
  d['lookat_lat'] = centerLat
  d['lookat_range_m'] = v_range
  d['lookat_tilt_deg'] = 40
  d['lookat_heading'] = v_head
  return d



# initialize the viewing angle dictionary
def init_d_look_at():
  ret_d = {}
  ret_d['lookat_starttime'] = ''
  ret_d['lookat_endtime'] = ''
  ret_d['lookat_lon'] = '-77.71'
  ret_d['lookat_lat'] = '38.5'
  ret_d['lookat_range_m'] = ''
  ret_d['lookat_tilt_deg'] = ''
  ret_d['lookat_heading'] = ''
  return ret_d