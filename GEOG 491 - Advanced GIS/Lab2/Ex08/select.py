import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Ex08"
infc = "airports.shp"
outfc = "airports_anchorage.shp"

delim_field = arcpy.AddFieldDelimiters(infc, "COUNTY")   # handles issues with delimiters
sql_exp = delim_field + " = 'Anchorage Borough'"
arcpy.Select_analysis(infc, outfc, sql_exp)
    
