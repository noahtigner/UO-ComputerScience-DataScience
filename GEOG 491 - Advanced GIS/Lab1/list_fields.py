import arcpy 

# print all field info for cities.shp
arcpy.env.overwriteOutput = True 
arcpy.env.workspace = "C:/PythonPro/Ex06" 
fieldlist = arcpy.ListFields("cities.shp") 
for field in fieldlist:     
    print(field.name + " " + field.type)