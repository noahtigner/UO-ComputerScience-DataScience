import arcpy

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

infc = "hawaii.shp"
outfc = "hawaii_envelope.shp"

for row in arcpy.da.SearchCursor(infc, ["SHAPE@"]): #query

    # extract extent of hawaii
    extent = row[0].extent
    x_min = extent.XMin
    y_min = extent.YMin
    x_max = extent.XMax
    y_max = extent.YMax

    # 4 corners
    points = [
        (x_min, y_min),
        (x_min, y_max),
        (x_max, y_max),
        (x_max, y_min)
    ]

# create polygon feature class (overwrite if it exists)
arcpy.CreateFeatureclass_management(workspace, outfc, "Polygon", spatial_reference="hawaii.shp") 

with arcpy.da.InsertCursor(outfc, ["SHAPE@"]) as cursor:    # prepare to insert data
    array = arcpy.Array()

    # add each point to the array
    for point in points:
        x, y = point
        array.add(arcpy.Point(x, y))

    # connect the points in the array to create a rectangular polygon and insert it
    cursor.insertRow([arcpy.Polygon(array)])
