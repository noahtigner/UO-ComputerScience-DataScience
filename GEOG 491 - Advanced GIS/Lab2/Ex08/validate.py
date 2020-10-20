import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Ex08"
fc = "airports.shp"

newfield = "NEW CODE"
fieldtype = "TEXT"
fieldname = arcpy.ValidateFieldName(newfield)
fieldlist = arcpy.ListFields(fc)
fieldnames = []
for field in fieldlist:
    fieldnames.append(field.name)
if fieldname not in fieldnames:    
    arcpy.AddField_management(fc, fieldname, fieldtype, "", "", 12)
    print("New field has been added.")
else:
    print("Field name already exists, no new qfield was added.")
