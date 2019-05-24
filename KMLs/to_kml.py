import sys
import os
import pdb
import utm
from string import Template
sys.path.append(os.path.abspath('../afs_kml_parser/src/afs_kml_parser'))
# print sys.path
from afs_kml_parser import Kml_utils, Line_utils, Polygon_utils, Kml_templates

def make_kml(raw, name):
  # pdb.set_trace()
  d = Kml_utils.init_d_template()
  temps = Kml_templates.KmlTemplates()

  kml_data = ''
  if raw.splines.data != []:
    kml_data += add_splines(raw['splines']['data'], 'splines', 'WP', raw['splines']['timestamp'])
  if raw.flown.data != []:
    kml_data += add_splines(raw['flown']['data'], 'flow_spline', 'TUNNEL', raw['flown']['timestamp'])
    look_at_loc = look_at(raw['flown']['data'], raw.flown.timestamp)
    d['look_at'] = Template(temps.LookAtLoc).substitute(look_at_loc)

  if raw.traj.data != []:
    kml_data += add_splines(raw['traj']['data'], 'trajectories', 'NFZ', raw['flown']['timestamp'])

  d['master_data'] = kml_data
  d['document_name'] = name
  d['document_snippet'] = 'Flight report'

  out_kml = Template(temps.masterTemplate).substitute(d)
  return out_kml

# list of splines in lat, lon, alt (or ECEF equivilent)
def add_splines(splines, fname, style, ts_data = []):
  def build_spline(spline, name, style):
    # pdb.set_trace()
    
    s_kml = ''
    try:
      for lat, lon, alt in spline:
        # pdb.set_trace()
         # = point
        alt = abs(alt)
        # try:
        #   lat, lon = utm.to_latlon(x, y, 18, 'S')
        # except:
        # pdb.set_trace()
        s_kml += '{},{},{}\n'.format(lon, lat, alt)
    except:
      pdb.set_trace()

    return Line_utils.build_line_kml(name, s_kml, style)
    # return Line_utils.build_line_kml(name, s_kml, style, mode = 'relativeToGround')

    # pdb.set_trace()
    
    # s_kml = ''
    #  # = point
    # try:
    #   for lat, lon, alt in zip(*spline):
    #     # pdb.set_trace()
    #     alt = abs(alt)
    #     s_kml += '{},{},{}\n'.format(lon, lat, alt)
    # except:
    #   pdb.set_trace()

    # return Line_utils.build_line_kml(name, s_kml, style)
    # return Line_utils.build_line_kml(name, s_kml, style, mode = 'relativeToGround')


  spline_kml = ''
  # pdb.set_trace()

  if len(ts_data) != len(splines):
    ind_name = ['Spline ' + str(i) for i in range(len(splines))]
  else:
    ind_name = ['Spline {}'.format(ts) for ts in ts_data]

  # for spline, name in zip(splines, ts_data):
  #   # s_kml = Line_utils.line_to_kml(spline)
  #   s_kml = ''
  #   for i in range(len(spline[0])):
  #     # pdb.set_trace()
  #     lat, lon = utm.to_latlon(spline[0][i], spline[1][i], 17, 'S')
  #     s_kml += '{0},{1},{2}\n'.format(lon, lat, spline[2][i])
  #   spline_kml += Line_utils.build_line_kml(name, s_kml, style)
  # pdb.set_trace()


  # for spline, name in zip(splines, ts_data):
  #   pdb.set_trace()
  #   # s_kml = Line_utils.line_to_kml(spline)
  #   s_kml = ''
  #   if type(spline[0]) in (list, tuple):
  #     # for i_spline in zip(*spline):
  #     #   spline_kml += build_spline(i_spline, name, style)

  #   else:
  #     spline_kml += build_spline(spline, name, style)

  # wihtout the zip
  if splines != [] and type(splines[0][0]) in (list, tuple):
    for spline, name in zip(splines, ts_data):
      spline_kml += build_spline(spline, name, style)
  else:
    try:
      name = str(ts_data[0])
    except:
      pdb.set_trace()
    spline_kml += build_spline(splines, name, style)


  spline_kml = Kml_utils.kml_folder(fname, spline_kml)
  return spline_kml

# def ecef_to_kml
# convert spline data into a form readeable by the look at function
def look_at(spline, ts):
  x, y, alt = zip(*spline)
  # lat, lon = utm.to_latlon(y, x, 17, 'S')
  
  return Kml_utils.look_at_loc({'time': ts, 'lat': x, 'lon': y})

