#!/usr/bin/python
#*********************************************************************************************
# afs_kml_parser.py
#
# Description:
#   - Parses google kml maps, converts to mgrs/llaRad/utm, and prints to file. Primarily
#   used with the AACUS Flight Testing Map to create SAV/NFZ and routes to use in simulation
#   or flight testing. Goal is to aid developers by not requiring the AVO-GCS interface.
#
# Usage:
#
#   python /path/to/afs_kml_parser.py /path/to/google_maps_example.kml /path/to/output_file_name.txt
#
#*********************************************************************************************

import sys
import os
import math
import time
from subprocess import call

# TODO: Disabled convert coordinates. Packages are not
# catkinized yet so cannot use.

#try:
#    import mgrs
#except:
#    print("ERROR: mgrs module not found")
#
#try:
#    import utm
#except:
#    print ("ERROR: utm module not found")

try:
    from xml.etree.ElementTree import ElementTree as ET
except:
    print ("ERROR: xml.etree.ElementTree module not found")

#*********************************************************************************************
# writeOutputFiles(placemarkDict, userSelectionDict, outputFilename) -
#        Takes the placemark dictionary and prints everything selected in the user selection
#        dictionary.
#
#        TODO: Currently just prints to one text file. Need to format to print
#        to files based on placemark type.
#*********************************************************************************************
def writeOutputFiles(placemarkDict, userSelectionDict, outputFilename):


    with open(outputFilename, 'w') as outputFile:
        for folderName in placemarkDict.keys():
            if folderName in userSelectionDict.values():
                outputFile.write("\n"+folderName)

                for placemarkName in placemarkDict[folderName]:
                    placemarkType = placemarkDict[folderName][placemarkName]['placemarkType']
                    llaDeg = placemarkDict[folderName][placemarkName]['llaDeg']
                    llaRad = placemarkDict[folderName][placemarkName]['llaRad']

                    # TODO: Disabled because convert coordinates utm/mgrs is disabled.
                    #utm = placemarkDict[folderName][placemarkName]['utm']
                    #mgrs = placemarkDict[folderName][placemarkName]['mgrs']

                    outputFile.write("\n\t"+placemarkName)
                    outputFile.write("\n\t\tType: "+placemarkType)
                    outputFile.write("\n\t\tLLA Deg:")
                    for coordinates in llaDeg:
                        outputFile.writelines("\n\t\t\t" + "\t".join(str(item) for item in coordinates))

                    outputFile.write("\n\t\tLLA Rad:")
                    for coordinates in llaRad:
                        outputFile.writelines("\n\t\t\t" + "\t".join(str(item) for item in coordinates))

                    # TODO: Disabled because convert coordinates utm/mgrs is disabled.
                    #outputFile.write("\n\t\tUTM:")
                    #for coordinates in utm:
                    #    outputFile.writelines("\n\t\t\t" + "\t".join(str(item) for item in coordinates))

                    #outputFile.write("\n\t\tMGRS:")
                    #for coordinates in mgrs:
                    #    outputFile.writelines("\n\t\t\t" + coordinates)

    

    #TODO:
    # for each folder/key in userSelectionDict that is in placemarkDict, get the placemark type
        # if type = polygon
            # check if .are file already exists in avo-gcs folder
            # write .area file for avo-gcs
            # write ROS msgs
        # if type = point
            # find if all points are in existing data .tif files and ask user to select folder and dem files to use
            # get point elevation on dem file to write to InitialConditions.launch
            # append point location to Bookmarks.xml file after checking if name already exists in Bookmarks
            # move point to top of bookmarks list
            # write ROs msgs
        # if type = linestring
            # get approach/departure directions from name
            # subtract 9 deg from magnetic heading to get true heading that TALOs uses
            # get user input on departure/approach fans to use.
            # write to file for jenkins and write ROS msgs

# end writeOutputFiles()


#*********************************************************************************************
# getFolderSelection(placemarkDict) -
#        Takes the placemark dictionary returned by convertCoordinates() and asks the user to
#        select which layers they want to print to file. Helpful because the map can be very
#        large and not necessary to create files for everthing.
#*********************************************************************************************
def getFolderSelection(placemarkDict):

    print '\nSelect which map layers (folder) to use for simulation:\n'

    # Return list of layers until user selections are valid/ in the placemarkDict
    userValueCheck = False
    while userValueCheck == False:

        # create dictionary to map user selection to folder names
        userSelectionDict = {}

        # print folders in placemark dictionary with coresponding numbers for selection
        number = 1
        for folderName in placemarkDict.keys():
            print (str(number) + ') ' + folderName)
            userSelectionDict[str(number)] = folderName
            number += 1

        print '\nSelect by entering numbers with space in between, such as "1 2 3"\n'

        # get user selection and parse into list
        userSelectionList = raw_input('Selection:')
        userSelectionList = userSelectionList.split()

        # check that user selections are in the dictionary
        userValueCheck = True
        for item in userSelectionList:
            if item in userSelectionDict:
                pass
            else:
                print ( item + ' is an invalid selection\n')
                userValueCheck = False

    # if all user selections are valid, delete non selected folders from user selection dictionary
    deleteFromDictList = []
    for key in userSelectionDict:
        if key in userSelectionList:
            pass
        else:
            deleteFromDictList.extend(key)

    for item in deleteFromDictList:
        userSelectionDict.pop(item, None)

    # return user selection dictionary
    return userSelectionDict

# end getFolderSelection()


#*********************************************************************************************
# convertCoordinates(placemarkList) - TODO: CURRENTLY DISABLED conversion for mgrs and utm.
#       mgrs and utm packages not catkinized yet and we don't need this functionality right now
#
#       Takes the placemark dict returned by parseKML(), converts coordinates to llaDeg,
#       llaRad, mgrs, and utm coordinates. Returns a dictionary of the placemarks with
#       all the converted coordinates.
#*********************************************************************************************
def convertCoordinates(placemarkDict):

    # m = mgrs.MGRS()

    for folderName in placemarkDict:
        for placemarkName in placemarkDict[folderName]:
            coordinateSet = placemarkDict[folderName][placemarkName]['llaDeg']

            llaRadList = []
            utmList = []
            mgrsList = []

            for coordinates in coordinateSet:
                latitude = coordinates[0]
                longitude = coordinates[1]
                altitude = coordinates[2]

                # convert to radians
                llaRadList.extend([[math.radians(latitude), math.radians(longitude), altitude]])

                # utm.from_latlon returns tuple of form: (EASTING, NORTHING, ZONE NUMBER, ZONE LETTER)
                # utmCoord = utm.from_latlon(latitude, longitude)
                # utmList.extend([utmCoord])

                # returns standard MGRS coordinate string. Can change precision with MGRSPrecision argsin .toMGRS()
                # mgrsCoord = m.toMGRS(latitude, longitude)
                # mgrsList.extend([mgrsCoord])

            # add converted coordinates to dictionary
            placemarkDict[folderName][placemarkName]['llaRad'] = llaRadList
            # placemarkDict[folderName][placemarkName]['utm'] = utmList
            # placemarkDict[folderName][placemarkName]['mgrs'] = mgrsList

    return placemarkDict

# end convertCoordinates()


#*********************************************************************************************
# parseKML(kmlFile) -
#        This loops through the kml headings and extracts the data using xml elementTree.
#        We're only need the placemark names, placemark types, and placemark coordinates.
#        Each loop references the xml tag in the kml file. The kml file needs to
#        be downloaded in kml format from the AACUS Flight Testing Map here:
#        https://www.google.com/maps/d/edit?mid=1JTAQJhFH7qkVtiwGhs7dnYUlWZs
#*********************************************************************************************
def parseKML(kmlFile):

    # get kml file data into element tree
    tree = ET()
    tree.parse(kmlFile)

    # initialize placemark dictionary for holding kml data
    placemarkDict = {}

    for Document in tree.findall('{http://www.opengis.net/kml/2.2}Document'):
        documentName = Document.find('{http://www.opengis.net/kml/2.2}name').text

        for Folder in Document.findall('{http://www.opengis.net/kml/2.2}Folder'):
            folderName = Folder.find('{http://www.opengis.net/kml/2.2}name').text

            # Add dictionary to placemark Dictionary
            placemarkDict[folderName] = {}

            for Placemark in Folder.findall('{http://www.opengis.net/kml/2.2}Placemark'):
                placemarkName = Placemark.find('{http://www.opengis.net/kml/2.2}name').text

                # Get placemark type and coordinates. Each placemark can only be one type, so
                # only one of the following loops will execute for each placemark.
                for LineString in Placemark.findall('{http://www.opengis.net/kml/2.2}LineString'):
                    coordinates = LineString.find('{http://www.opengis.net/kml/2.2}coordinates').text
                    placemarkType = 'LineString'

                for Polygon in Placemark.findall('{http://www.opengis.net/kml/2.2}Polygon'):
                    for outerBoundaryIs in Polygon.findall('{http://www.opengis.net/kml/2.2}outerBoundaryIs'):
                        for LinearRing in outerBoundaryIs.findall('{http://www.opengis.net/kml/2.2}LinearRing'):
                            coordinates = LinearRing.find('{http://www.opengis.net/kml/2.2}coordinates').text
                            placemarkType = 'Polygon'

                for Point in Placemark.findall('{http://www.opengis.net/kml/2.2}Point'):
                    coordinates = Point.find('{http://www.opengis.net/kml/2.2}coordinates').text
                    placemarkType = 'Point'

                # remove commas from coordinates string and split into list
                coordinates = coordinates.replace(',',' ')
                coordinates = coordinates.split()

                # organize the coordinates list - it's one single list at this point, so take
                # each set of coordinates and add them to their own list.
                llaDegList = []
                coordinateIndex = 0

                while coordinateIndex <= len(coordinates)-3:
                    longitude = float(coordinates[coordinateIndex])        # longitude in degrees
                    latitude = float(coordinates[coordinateIndex+1])       # latitude in degrees
                    altitude = float(coordinates[coordinateIndex+2])       # altitude in meters
                    llaDegList.extend([[latitude, longitude, altitude]])
                    coordinateIndex +=3

                # Add data to the dictionary
                placemarkDict[folderName][placemarkName]={'placemarkType' : placemarkType, 'llaDeg': llaDegList}

    return placemarkDict

# end parseKML()


#*********************************************************************************************
# main() - entry point for script
#*********************************************************************************************
def main():
    # get command line args
    kmlFile = str(sys.argv[1])
    outputFilename = str(sys.argv[2])

    # main functions
    placemarkDict = parseKML(kmlFile)
    placemarkDict = convertCoordinates(placemarkDict)
    userSelectionDict = getFolderSelection(placemarkDict)
    writeOutputFiles(placemarkDict, userSelectionDict, outputFilename)

if __name__ == "__main__":
    main()
