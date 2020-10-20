import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Ex08"
fc = "airports.shp"

unique_name = arcpy.CreateUniqueName("buffer.shp")
arcpy.Buffer_analysis(fc, unique_name, "5000 METERS")
