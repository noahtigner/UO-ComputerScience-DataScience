import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Ex08"
fc = "airports.shp"

delim_field = arcpy.AddFieldDelimiters(infc, "STATE")   # handles issues with delimiters
sql_exp = delim_field + " <> 'AK'"  # state = AK
with arcpy.da.UpdateCursor(fc, ["STATE"], sql_exp) as cursor:
    for row in cursor:
        row[0] = "AK"   # set all states to AK
        cursor.updateRow(row)
