import arcpy

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise05"

in_fc = "parks.shp"
out_fc = "parks_centroid.shp"

# if a license is available then run the tool, otherwise print a message
if arcpy.ProductInfo() == "arcInfo":
    arcpy.FeatureToPoint_management(in_fc, out_fc)
else:
    print("An ArcInfo license is not available")

