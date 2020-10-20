import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/YOURNAME/Labs/Lab2/Ex08"

fc = "airports.shp"
delim_field = arcpy.AddFieldDelimiters(fc, "COUNTY")   # handles issues with delimiters
sql_exp = delim_field + " = 'Anchorage Borough'"
cursor = arcpy.da.SearchCursor(fc, ["NAME", "TOT_ENP"], sql_exp)
for row in cursor:
    print(f"Name: {row[0]}\tPassengers: {row[1]}")
    
