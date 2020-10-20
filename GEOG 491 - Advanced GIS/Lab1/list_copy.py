import arcpy 
import os 

ws = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise06"

fgdb = "Copy.gdb" 
arcpy.CreateFileGDB_management(ws, fgdb) 
arcpy.env.workspace = ws 

# copy each feature class to a new db
fclist = arcpy.ListFeatureClasses() 
for fc in fclist:     
    fcname = arcpy.da.Describe(fc)["baseName"]     
    newfc = os.path.join(ws, fgdb, fcname)     
    arcpy.CopyFeatures_management(fc, newfc)