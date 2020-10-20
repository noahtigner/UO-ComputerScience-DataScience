import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Ex08"
fc = "airports.shp"

with arcpy.da.UpdateCursor(fc, ["TOT_ENP"]) as cursor:
    for row in cursor:
        if row[0] < 100000:
            cursor.deleteRow()
        
