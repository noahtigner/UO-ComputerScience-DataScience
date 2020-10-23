import arcpy

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace

fc = "rivers.shp"

# print pair of x,y coords for each vertex in each feature
# works for polygon and polyline, not multipart features
with arcpy.da.SearchCursor(fc, (["OID@", "SHAPE@"])) as cursor:
    for row in cursor:
        print(f"Feature: {row[0]}")
        for point in row[1].getPart(0):
            print(f"{point.X:.3f}, {point.Y:.3f}")
