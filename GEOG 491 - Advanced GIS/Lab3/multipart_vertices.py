import arcpy

# Set workspace
workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab3/Ex09"
arcpy.env.workspace = workspace

fc = "hawaii.shp"                                       

cursor = arcpy.da.SearchCursor(fc, (["OID@", "SHAPE@"]))# query fc
for row in cursor:                                      # iterate through cursor
    print(f"Feature {row[0]}:")                         # print the feature and number
    partnum = 0                                         # instantiate part number to 0
    for part in row[1]:                                 # iterate through list of parts
        print(f"Part {partnum}")                        # print part number
        for point in part:                              # iterate through list of points
            print(f"{point.X:.2f}, {point.Y:.2f}")      # print each x,y pair
        partnum += 1                                    # increment part number
