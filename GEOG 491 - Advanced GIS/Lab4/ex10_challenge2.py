import arcpy

workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex10"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

arcpy.CreateFileGDB_management(workspace, "new.gdb")    # create new gdb in the workspace

rasters = arcpy.ListRasters()   # get a list of all rasters in the workspace
for raster in rasters:
    raster_name = workspace + "/new.gdb/" + arcpy.da.Describe(raster)['baseName']   # name and location for copied raster
    print(raster_name)  # just for testing
    arcpy.CopyRaster_management(raster, raster_name)    # copy raster to new database
