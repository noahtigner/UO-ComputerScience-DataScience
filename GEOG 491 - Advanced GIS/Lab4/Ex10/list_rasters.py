import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex10"

rasterlist = arcpy.ListRasters()
for raster in rasterlist:
    print(raster)
