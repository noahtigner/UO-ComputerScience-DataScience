import arcpy

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05"
arcpy.Intersect_analysis("R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05\\bike_routes.shp", "bike_intersections.shp")
