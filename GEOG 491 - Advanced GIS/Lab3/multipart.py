import arcpy

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace

fc = "hawaii.shp"

with arcpy.da.SearchCursor(fc, (["OID@", "SHAPE@"])) as cursor:
    for row in cursor:
        if row[1].isMultipart:
            print(f"Feature {row[0]} is multipart and has {row[1].partCount} parts")
        else:
            print(f"Feature {row[0]} is singlepart")
