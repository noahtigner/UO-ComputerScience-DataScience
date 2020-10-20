import arcpy

arcpy.env.workspace = "R:\\Geog491_591_6\\Student_Data\\nzt\\Labs\\Lab1\\Exercise06"

# describe and print info about each feature class
fclist = arcpy.ListFeatureClasses()
for fc in fclist:     
    fcdesc = arcpy.da.Describe(fc) 
    name = fcdesc["name"]     
    stype = fcdesc["shapeType"]  
    spref = fcdesc["spatialReference"].name   
    print(f"{name} has geometry type {stype} and spatial reference {spref}")