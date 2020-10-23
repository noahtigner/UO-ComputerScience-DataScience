import arcpy

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace

fc = "dams.shp"
with arcpy.da.SearchCursor(fc, ["SHAPE@XY"]) as cursor:
    for row in cursor:
        x, y = row[0]
        print(f"{x:.3f}, {y:.3f}")
