import arcpy

arcpy.env.workspace = "R:/Geog491_591_6/Student_Data/nzt/Labs/Lab2/Challenge"
infc = "TRANS_PLAN_ADOPTED_2006.shp"

delim_field = arcpy.AddFieldDelimiters(infc, "Layer")   # handles issues with delimiters

out1 = "majart.shp"
sql_exp = delim_field + " = 'MAJART'"
arcpy.Select_analysis(infc, out1, sql_exp)
arcpy.Buffer_analysis(out1, "majart_buffer.shp", "200 FEET", "FULL", "ROUND", "ALL")

out2 = "majcol.shp"
sql_exp = delim_field + " = 'MAJCOL'"
arcpy.Select_analysis(infc, out2, sql_exp)
arcpy.Buffer_analysis(out2, "majcol, _buffer.shp", "200 FEET", "FULL", "ROUND", "ALL")
