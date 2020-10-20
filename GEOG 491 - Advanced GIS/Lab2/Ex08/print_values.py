import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Ex08"

fc = "airports.shp"
cursor = arcpy.da.SearchCursor(fc, ["NAME"])
for row in cursor:
    print(f"Airport name = {row[0]}")
