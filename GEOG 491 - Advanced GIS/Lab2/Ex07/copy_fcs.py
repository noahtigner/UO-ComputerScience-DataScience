import arcpy
import os
arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab2\\Ex07"
arcpy.env.overwriteOutput = True
fgdb = "Demo.gdb"

# attempt to copy the features to Demo.gdb.
# handle tool specific and general errors
try:
    fclist = arcpy.ListFeatureClasses()
    for fc in fclist:
        desc = arcpy.da.Describe(fc)
        outfc = os.path.join(fgdb, desc["baseName"])
        arcpy.CopyFeatures_management(fc, outfc)
except arcpy.ExecuteError:
    print(arcpy.GetMessage(2))
except:
    print("There has been a nontool error")
