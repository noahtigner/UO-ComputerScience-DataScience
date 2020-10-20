import arcpy 
import os 

ws = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise06" 

fgdb = "Albany_Polygons.gdb" 
arcpy.CreateFileGDB_management(ws, fgdb) 
arcpy.env.workspace = ws 

# copy each polygon to a new database and append "_Polygon" to the file name
fclist = arcpy.ListFeatureClasses() 
for fc in fclist:     
    fcname = arcpy.da.Describe(fc)["baseName"] + "_Polygon"
    newfc = os.path.join(ws, fgdb, fcname)     
    if arcpy.da.Describe(fc)["shapeType"]:
        arcpy.CopyFeatures_management(fc, newfc)    