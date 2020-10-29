import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex10"

raster = "tm.img"

desc = arcpy.da.Describe(raster)
for rband in desc["children"]:
    bandname = rband["baseName"]
    x = rband["meanCellHeight"]
    y = rband["meanCellWidth"]
    spatialref = desc["spatialReference"]
    units = spatialref.angularUnitName
    print(f"The resolution of {bandname} is {x:.7f} by {y:.7f} {units}")

    if spatialref.type == "Geographic":
        print("Yup, save that for later")

##print(f"Raster base name: {desc['baseName']}")
##print(f"Raster data type: {desc['dataType']}")
##print(f"Raster file extension: {desc['extension']}")
##print(f"Raster spatial reference: {desc['spatialReference'].name}")
##print(f"Raster format: {desc['format']}")
##print(f"Raster compression: {desc['compressionType']}")
##print(f"Raster number of bands: {desc['bandCount']}")

