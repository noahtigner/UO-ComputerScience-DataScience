import arcpy

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05"

arcpy.FeatureToLine_management("R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05\\parks.shp", "ParkLines.shp")