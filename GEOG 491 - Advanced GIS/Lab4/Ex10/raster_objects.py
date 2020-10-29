import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex10"
arcpy.CheckOutExtension("Spatial")

outraster = arcpy.sa.Slope("elevation")

desc = arcpy.da.Describe(outraster)
print(desc["datasetType"])
print(desc["permanent"])

outraster.save("slope")
