import arcpy
arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab2\\Ex07"

# print the basename and shape type for each feature
fclist = arcpy.ListFeatureClasses()
for fc in fclist:
    desc = arcpy.da.Describe(fc)
    print(f'{desc["baseName"]}: {desc["shapeType"]}')
