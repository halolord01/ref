'''
@file Kml_templates.py
@brief class containing all templates used for KML plotting
@author Adam Poirier
@version 1.0
@date 2017-02-22

'''

class KmlTemplates(object):
  masterTemplate ="""<?xml version="1.0" encoding="UTF-8"?>
  <kml xmlns="http://www.opengis.net/kml/2.2"
   xmlns:gx="http://www.google.com/kml/ext/2.2">
    <Document>
      <name>$document_name</name>
      <Snippet maxLines="1">$document_snippet</Snippet>
      <description>$document_description</description>
      
      <!-- color guide: hex: alpha,b,g,r   -->
      
      <!-- Normal track style -->
      <Style id="track_n">
        <IconStyle>
          <scale>.5</scale>
          <Icon>
            <href>http://earth.google.com/images/kml-icons/track-directional/track-none.png</href>
          </Icon>
        </IconStyle>
        <LabelStyle>
          <scale>0</scale>
        </LabelStyle>
        <LineStyle>
          <color>7f00ffff</color>
          <width>4</width>
        </LineStyle>
        <PolyStyle>
          <color>7f00ff00</color>
        </PolyStyle>
      </Style>

      <!-- Standard styles -->
      <Style id="NFZ">
        <LineStyle>
          <color>e00b15ff</color>
          <width>2</width>
        </LineStyle>
        <PolyStyle>
          <color>e00b15ff</color>
        </PolyStyle>
      </Style>
      <Style id="SAV">
        <LineStyle>
          <width>2</width>
          <color>7fffffff</color>
        </LineStyle>
        <PolyStyle>
          <color>9600cc00</color>
        </PolyStyle>
      </Style>
      
      <Style id="LZ">
        <LineStyle>
          <color>ff000000</color>
          <width>2</width>
        </LineStyle>
        <PolyStyle>
          <color>96ffffff</color>
        </PolyStyle>
      </Style>
      <Style id="tunnelPoly">
        <LineStyle>
          <color>ff000000</color>
          <width>2</width>
        </LineStyle>
        <PolyStyle>
          <color>44006cff</color>
        </PolyStyle>
      </Style>
      <Style id="ECP"> <!-- End cap Polygon -->
        <LineStyle>
          <color>64000000</color>
          <width>2</width>
        </LineStyle>
        <PolyStyle>
          <color>64ff0000</color>
        </PolyStyle>
      </Style>
      <!-- /Standard styles -->

      <!-- Highlighted track style -->
      <Style id="track_h">
        <IconStyle>
          <scale>1.2</scale>
          <Icon>
            <href>http://earth.google.com/images/kml-icons/track-directional/track-none.png</href>
          </Icon>
        </IconStyle>
      </Style>
      <StyleMap id="track">
        <Pair>
          <key>normal</key>
          <styleUrl>#track_n</styleUrl>
        </Pair>
        <Pair>
          <key>highlight</key>
          <styleUrl>#track_h</styleUrl>
        </Pair>
      </StyleMap>
      <Style id="transPurpleLineGreenPoly">
        <LineStyle>
          <color>7fff00ff</color>
          <width>4</width>
        </LineStyle>
        <PolyStyle>
          <color>7f00ff00</color>
        </PolyStyle>
      </Style>

      <!-- Normal multiTrack style -->
      <Style id="multiTrack_n">
        <IconStyle>
          <Icon>
            <href>http://earth.google.com/images/kml-icons/track-directional/track-0.png</href>
          </Icon>
        </IconStyle>
        <LineStyle>
          <color>7f00ffff</color>
          <width>4</width>
        </LineStyle>
        <PolyStyle>
          <color>7f00ff00</color>
        </PolyStyle>

      </Style>
      <!-- Highlighted multiTrack style -->
      <Style id="multiTrack_h">
        <IconStyle>
          <scale>1.2</scale>
          <Icon>
            <href>http://earth.google.com/images/kml-icons/track-directional/track-0.png</href>
          </Icon>
        </IconStyle>
        <LineStyle>
          <color>99ffac59</color>
          <width>8</width>
        </LineStyle>
      </Style>
      <StyleMap id="multiTrack">
        <Pair>
          <key>normal</key>
          <styleUrl>#multiTrack_n</styleUrl>
        </Pair>
        <Pair>
          <key>highlight</key>
          <styleUrl>#multiTrack_h</styleUrl>
        </Pair>
      </StyleMap>

      <!-- Normal waypoint style -->
      <Style id="waypoint_n">
        <IconStyle>
          <Icon>
            <href>http://maps.google.com/mapfiles/kml/pal4/icon61.png</href>
          </Icon>
        </IconStyle>
      </Style>
      <!-- Highlighted waypoint style -->
      <Style id="waypoint_h">
        <IconStyle>
          <scale>1.2</scale>
          <Icon>
            <href>http://maps.google.com/mapfiles/kml/pal4/icon61.png</href>
          </Icon>
        </IconStyle>
      </Style>
      <StyleMap id="waypoint">
        <Pair>
          <key>normal</key>
          <styleUrl>#waypoint_n</styleUrl>
        </Pair>
        <Pair>
          <key>highlight</key>
          <styleUrl>#waypoint_h</styleUrl>
        </Pair>
      </StyleMap>




      <!-- Templates to add (not in this order) -->
      <!-- waypoints, line-->
      <!-- flight tracks, line  -->
      <!-- LZ polypons, poly  -->
      <!-- Endcap Polygons, poly  -->
      <!-- Safe Air Volume, poly  -->
      <!-- No Fly Zones, poly  -->
      $master_data


      $look_at


    </Document>
  </kml>
  """

  '''
  document_name
  document_snippet
  document_description
  lookat_starttime
  lookat_endtime
  lookat_lon
  lookat_lat
  lookat_range_m
  lookat_tilt_deg
  lookat_heading
  '''

  # A places data in a named folder
  FolderTemplate = '''<Folder>
    <name>$folderName</name>
      $data
    </Folder>\n'''

  # folderName
  # data

  # a template for a polygon 
  PolygonTemplate = """<Placemark>
          <visibility>$visible</visibility>
          <name>$name</name>
          <styleUrl>$style</styleUrl>
          <Polygon>
            <extrude>$extrude</extrude>
            <altitudeMode>$altitudeMode</altitudeMode>
            <tessellate>$tessellate</tessellate>
            <outerBoundaryIs>
              <LinearRing>
                <coordinates>
                  $coords
                </coordinates>
              </LinearRing>
            </outerBoundaryIs>
            <innerBoundaryIs>
              <LinearRing>
                <coordinates>
                  $innerCoords
                </coordinates>
              </LinearRing>
            </innerBoundaryIs>
          </Polygon>
        </Placemark>
      """

  '''
  visible
  name
  style
  extrude
  altitudeMode
  coords
  innerCoords
  '''

  # template for a tunnel
  TUNNELTEMPLATE = '''<Placemark>
          <visibility>$visible</visibility>
          <name>$track_name</name>
          <styleUrl>$style</styleUrl>
          <LineString>
            <altitudeMode>$altitude_mode</altitudeMode>
            <extrude>$extrude</extrude>
            <tessellate>$tessellate</tessellate>
            <coordinates>
              $track_points
            </coordinates>
          </LineString>
        </Placemark>\n'''
  '''
  visible
  track_name
  style
  altitude_mode
  extrude
  tessellated
  track_points
  '''

  LineTemplate = '''<Placemark>
        <visibility>$visible</visibility>
        <name>$line_name</name>
        <styleUrl>$style</styleUrl>
          $line_type
      </Placemark>
  '''

  '''
  folder_name
  visible
  line_name
  style
  line_type
  '''

  BasicLine = '''<LineString>
            <altitudeMode>$altitude_mode</altitudeMode>
            <extrude>$extrude</extrude>
            <tessellate>$tessellate</tessellate>
            <coordinates>
                $coords
            </coordinates>
          </LineString>'''
  '''
  altitude_mode
  extrude
  tellelate
  coords
  '''

  TrackLine = '''
          <gx:Track id="$track_id">
            <altitudeMode>$altitude_mode</altitudeMode>
            <extrude>$extrude</extrude>
            <tessellate>$tessellate</tessellate>
            $track_points
          </gx:Track>
  '''
  '''
  track_id
  altitude_mode
  extrude
  tessellate
  track_points
  '''

  Point = '''
      <Placemark>
        <visibility>$visible</visibility>
        <name>$name</name>
        <Point id="$name">
          <!-- specific to Point -->
          <extrude>0</extrude>                        <!-- boolean -->
          <altitudeMode>$altitudeMode</altitudeMode>
                <!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
                <!-- or, substitute gx:altitudeMode: clampToSeaFloor, relativeToSeaFloor -->
          <coordinates>
          $coords
          </coordinates>              <!-- lon,lat[,alt] -->
        </Point>
      </Placemark>

  '''
  # point
  '''
  visible
  name
  altitudeMode
  coords
  '''

  LookAtLoc = '''
        <LookAt>
          <gx:TimeSpan>
              <begin>$lookat_starttime</begin>
              <end>$lookat_endtime</end>
          </gx:TimeSpan>
          <longitude>$lookat_lon</longitude>
        <latitude>$lookat_lat</latitude>
        <range>$lookat_range_m</range>
         <tilt>$lookat_tilt_deg</tilt>
         <heading>$lookat_heading</heading>
         <altitudeMode>clampToGround</altitudeMode>
      </LookAt>
      '''



  STYLES = {'NFZ': '#NFZ', 'SAV': '#SAV', 'WP':'#multiTrack', 'TRACK':'#multiTrack', 'LZ':'#LZ', 'TUNNEL':'transPurpleLineGreenPoly', 'TUNNEL_POLY':'#tunnelPoly'}
