import arcpy
from arcpy.sa import *

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex10"
arcpy.CheckOutExtension("Spatial")

elevraster = arcpy.Raster("elevation")

##outraster = elevraster * 3.281  # Meters to Feet
##outraster.save("elev_ft")

slope = Slope(elevraster)
goodslope = slope < 20              # slope < 20 degrees
goodelev = elevraster < 2500        # elevation < 2500 meters
goodfinal = goodslope & goodelev    # map algebra operators: Binary AND
goodfinal.save("final")
