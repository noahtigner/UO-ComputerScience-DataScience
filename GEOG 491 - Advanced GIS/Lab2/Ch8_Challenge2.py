import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Challenge"
infc = "TRANS_PLAN_ADOPTED_2006.shp"

arcpy.AddField_management(infc, "COLLECTOR", "TEXT")    # add field

delimfield = arcpy.AddFieldDelimiters(infc, "Layer")
sql_exp = delimfield = " <> '*'"    # catch all
with arcpy.da.UpdateCursor(infc, ["Layer", "COLLECTOR"], sql_exp) as cursor:
    for row in cursor:
        # if majcol or mincol then YES else NO
        row[1] = "NO"
        if row[0] == "MAJCOL" or row[0] == "MINCOL":
            row[1] = "YES"
        cursor.updateRow(row)
