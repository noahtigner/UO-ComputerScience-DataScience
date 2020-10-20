import arcpy

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise06"

# describe and print info on each feature class
fclist = arcpy.ListFeatureClasses()
for fc in fclist:     
    fcdesc = arcpy.da.Describe(fc)     
    dtype = fcdesc["dataType"]     
    name = fcdesc["name"]     
    stype = fcdesc["shapeType"]     
    print(f"{dtype} {name} has shapetype {stype}")  # fstrings are great

