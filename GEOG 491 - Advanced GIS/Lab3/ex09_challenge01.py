import arcpy

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

infc = "hawaii.shp"
outfc = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09/hawaii_singlepart.shp"

arcpy.MultipartToSinglepart_management(infc, outfc) # one part per each island

# print the perimeter and area of each feature (island)
for row in arcpy.da.SearchCursor(outfc, ["SHAPE@LENGTH", "SHAPE@AREA"]):    # query perimeter and area
    print(f"Perimeter: {row[0]:.2f} Meters\tArea: {row[1]:.2f} Meters^2")   # print and formatting
