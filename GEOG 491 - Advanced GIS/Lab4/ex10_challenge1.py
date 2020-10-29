import arcpy
from arcpy.sa import *

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex10"
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

slope = Slope("elevation")      # slope raster
aspect = Aspect("elevation")    # aspect raster

moderate_slope = (slope >= 5) & (slope <= 20)           # 5 <= slope <= 20 degrees
southerly_aspect = (aspect >= 150) & (aspect <= 270)    # 150 <= aspect <= 270 degrees

remap_table = RemapValue([
    [41, 1],
    [42, 1],
    [43, 1]
])
forested = Reclassify("landcover.tif", "VALUE", remap_table, "NODATA")  # 1 if land cover type 41, 42, or 42, else NODATA

finalraster = moderate_slope & southerly_aspect & forested  # Binary AND: 1 if all 3 are 1, else 0 (possibly NODATA)
finalraster.save("finalrast")    # save to persistent memory
