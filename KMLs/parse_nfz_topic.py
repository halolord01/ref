'''
@parse_nfz_topic.py
@brief module to parse NFZs from bag file
@author Adam Poirier
@version 1.0
@date 2017-02-22

module for mission_command_to_kml.py to parse NFZs from the mission manager bag file
'''
import sys
import os
import afs_kml_parser.Polygon_utils as p_utils
import afs_kml_parser.Line_utils as l_utils
from afs_kml_parser import Kml_utils
from afs_kml_parser.Kml_debug import *
import copy
import math
# utm = __import__('3rd_party_libs.utm').utm

# required global var to tell the main execution which topic this module processes
TOPIC = '/no_fly_zone'

# Parse NFZ polygons
def parse_nfz_topic(nfz_msgs, inputArgs):
# def parse_nfz_topic(nfz_msgs, inputArgs, utm_data):
  flat = inputArgs.flat           # input arg, flag to plot the track as a 2d representation
  nfz_names= inputArgs.nfz_names   # input arg, str or list for the name of each NFZ
  NFZ_kml = ''
  if type(nfz_names) in (list, tuple):
    nfz_names_flat = [n + ' flat' for n in nfz_names]
  else:
    nfz_names_flat = nfz_names + ' flat'

  '''
  input:
    nfz_msgs            # NFZ message from the nfz topic
    flat                # input arg to plot flat zones for easy viewing: Boolean
    nfz_names           # names for the NFZs, list or string acceptable
  output:
    nfz_polygonz        # nfz_polygons[zone][point]{lat, lon, alt}
  '''
  # debug(ran='NFZ ran', msg=nfz_msgs)
  id_zero_count = 0                           # count the zero ID number, after first valid data
  fi = 0                                      # starting index that data reaches the loop
  flag = True                                 # prevents resetting the if index each loop
  nfz_uppers = []                             # Upper surface of NFZ polys: nfz_uppers[zone][point]{lat, lon, alt}
  nfz_lowers = []                             # Lower surface of NFZ polys: nfz_lowers[zone][point]{lat, lon, alt}

  for msg in nfz_msgs:
    if len(msg.noFlyZones) > 0:
      for i, zone in enumerate(msg.noFlyZones):
        # nfz_polygons.append([{} for x in range(len(zone.polygon) * 2)])
        nfz_uppers.append([])
        nfz_lowers.append([])
        for j, point in enumerate(zone.polygon):
          nfz_uppers[i].append({})
          nfz_lowers[i].append({})
          # gather the easting and northing, then convert to lat, lon
          lat = point.latitude_deg
          lon = point.longitude_deg
          # lat, lon = utm.to_latlon(easting, northing, utm_data[0], utm_data[1]) ***
          # add point data to the lists
          nfz_uppers[i][j] = {'lon': lon, 'lat': lat, 'alt': abs(zone.maximumHAE_m)}
          nfz_lowers[i][j] = {'lon': lon, 'lat': lat, 'alt': abs(zone.minimumHAE_m)}
      break

  # construct a kml string of the NFZs 
  NFZ_kml += p_utils.build_float_poly(nfz_uppers, nfz_lowers, nfz_names, 'NFZ', '#NFZ', flat)
  NFZ_kml += p_utils.build_float_poly(nfz_uppers, nfz_lowers, nfz_names_flat, 'NFZ-Flat', '#NFZ', True)
  NFZ_kml = Kml_utils.kml_folder('No Fly Zones', NFZ_kml)
  data_dict = {'nfz_uppers':nfz_uppers, 'nfz_lowers':nfz_lowers}
  return (NFZ_kml, data_dict)
