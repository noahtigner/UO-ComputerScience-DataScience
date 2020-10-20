import arcpy

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise06"

shp_exists = arcpy.Exists("cities.shp")
print(shp_exists)

# if cities.shp exists, copy it over
fc = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise06\\cities.shp"
newfc = "cities_copy.shp"
if arcpy.Exists(fc):
    arcpy.CopyFeatures_management(fc, newfc)