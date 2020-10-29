import arcpy
import listnames

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab4/Ex02"

fields = listnames.listfieldnames("streets.shp")
print(fields)
