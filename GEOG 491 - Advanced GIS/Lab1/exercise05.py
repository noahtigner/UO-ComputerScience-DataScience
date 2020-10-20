import arcpy

arcpy.Clip_analysis("parks", "zip","R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05\\parks_clip.shp")

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05"

arcpy.Buffer_analysis("facilities.shp", "facilities_buffer.shp", "500 METERS")

in_features = "bike_routes.shp"
clip_features = "zip.shp"
out_features = "bike_clip.shp"
xy_tolerance = ""
arcpy.Clip_analysis(in_features, clip_features, out_features, xy_tolerance)

arcpy.Exists("hospitals.shp")

arcpy.Usage("Clip_analysis")

prjfile = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05\\facilities.prj"
spatial_ref = arcpy.SpatialReference(prjfile)
arcpy.DefineProjection_management("hospitals", spatial_ref)

print(spatial_ref.name)
print(spatial_ref.linearUnitName)
print(spatial_ref.XYResolution)

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = spatial_ref

# **************************************************************

print(arcpy.GetMessages())
msgCount = arcpy.GetMessageCount()
print(arcpy.GetMessages(msgCount-1))


# **************************************************************

in_fc = "parks.shp"
out_fc = "parks_centroid.shp"
if arcpy.ProductInfo() == "arcInfo":
    arcpy.FeatureToPoint_management(in_fc, out_fc)
else:
    print("An ArcInfo license is not available")