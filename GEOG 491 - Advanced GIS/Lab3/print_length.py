import arcpy

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace

# 
fc = "rivers.shp"

#
with arcpy.da.SearchCursor(fc, ["SHAPE@LENGTH"]) as cursor:
    #
    length = 0
    #
    for row in cursor:
        length = length + row[0]
    desc = arcpy.da.Describe(fc)
    units = desc["spatialReference"].linearUnitName
    print(f"{length:.2f} {units}")
                           
                           
