import arcpy
from arcpy.sa import *

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex10"
arcpy.CheckOutExtension("Spatial")

##myremap = RemapRange([
##    [1000, 2000, 1],
##    [2000, 3000, 2],
##    [3000, 4000, 3]
##])

# remapValue often used for discrete data (ie land cover)
myremap = RemapValue([
    [41, 1],
    [42, 2],
    [43, 3]
])

# reclassify using myremap and if a value is not in the remap table,
# then becomes NODATA
outreclass = Reclassify("landcover.tif", "VALUE", myremap, "NODATA")

# save raster to persistant memory
outreclass.save("lc_recl")
