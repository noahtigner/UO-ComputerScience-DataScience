import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Ex08"
fc = "airports.shp"

with arcpy.da.InsertCursor(fc, "NAME") as cursor:
    cursor.insertRow(["New Airport"])
