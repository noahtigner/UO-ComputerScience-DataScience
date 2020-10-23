import arcpy
import fileinput
import os

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

newfc = "newpolyline.shp"

arcpy.CreateFeatureclass_management(workspace, newfc, "Polyline", spatial_reference="dams.shp") # create polyline feature class (overwrite if it exists)

infile = os.path.join(workspace, "coordinates.txt") # creates full path + coordinates.txt

with arcpy.da.InsertCursor(newfc, ["SHAPE@"]) as cursor:    # insert cursor for new data
    array = arcpy.Array()                                   # arrays are similar to lists but more performant and of a single type

    for line in fileinput.input(infile):        # iterate through input file
        ID, X, Y = line.split()                 # parse each line
        array.add(arcpy.Point(X, Y))            # add coordinate pair from text file to array

    cursor.insertRow([arcpy.Polyline(array)])   # insert array into the feature class
    fileinput.close()                           # clean up
