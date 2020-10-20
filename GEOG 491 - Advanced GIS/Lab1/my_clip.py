import arcpy

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05"
arcpy.env.overwriteOutput = True

# run a clipping tool on bike_routes and parks, printing the last message given
# newclip = arcpy.Clip_analysis("bike-routes.shp", "parks.shp", "bike_clip.shp")
newclip = arcpy.Clip_analysis("R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05\\bike_routes.shp", "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05\\parks.shp", "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05\\bike_clip.shp")
fcount = arcpy.GetCount_management("bike_clip.shp")
msgCount = newclip.messageCount
print(newclip.getMessage(msgCount-1))


