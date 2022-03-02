import arcpy
import fc_fields
import os

#            ___________________________
#           | Finds connected lines     |
#           | with matching attribution |
#           | and merges them back      |
#           | together.                 |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~

arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

# Pull in feature classes from TDS and only keep the curves
featureclass = arcpy.ListFeatureClasses()
featureclass = [ x for x in featureclass if "Pnt" not in x and "Srf" not in x]
#arcpy.AddMessage(featureclass)

# Set the output directory for the UnsplitLine tool
out_shape = os.path.dirname(arcpy.env.workspace)
arcpy.AddMessage(out_shape)
# Precreate the path for the output dBASE table
path = out_shape.split(".")
path.pop()
shape_loc = path[0] + str(".shp")
arcpy.AddMessage("Creating temporary output file: " + str(shape_loc))
# Get name of shp output alone
##shape = shape_loc.split("\\")
##shape = shape.pop()
##arcpy.AddMessage(shape)

fc = str(featureclass[11])
dick = fc_fields.crv_fields[fc]
arcpy.UnsplitLine_management(fc, shape_loc, dick)

### Loop feature classes and FindIdentical to get a count, then delete any found
##for fc in featureclass:
##    dick = fc_fields.crv_fields[fc]
##    arcpy.UnsplitLine(fc, out_table, dick)
##    rows = arcpy.GetCount_management(table_loc)
##    arcpy.AddMessage("Found " + str(rows) + " duplicate " + str(fc) + " features.")
##    if rows > 0:
##        arcpy.DeleteIdentical_management(fc, fc_fields.fc_fields[fc])
##        arcpy.AddMessage("Deleted " + str(rows) + " duplicate " + str(fc) + " features.")
##
### Clean up before next process
##del table_loc

from collections import Counter

def count_duplicates(path_to_data, field_to_count):
    #Add the count field
    data_layer = arcpy.MakeFeatureLayer_management(path_to_data, 'data')
    arcpy.AddField_management(data_layer, 'COUNT', 'LONG')
    arcpy.Delete_management(data_layer)
    del data_layer

    #Do the counting:
    value_list = []
    with arcpy.da.SearchCursor(path_to_data, [field_to_count]) as search_rows:
        for row in search_rows:
            value_list.append(row[0])

    counts = Counter(value_list)
    del value_list
    
    with arcpy.da.UpdateCursor(path_to_data, [field_to_count, 'COUNT']) as update_rows:
        for row in udpate_rows:
            row[1] = counts[row[0]]
            update_rows.updateRow(row)



arcpy.Statistics_analysis("Export_Output","in_memory/x",[["ID","COUNT"]],"ID")


mfl(shape_loc, "cur_shp")
mfl(fc, "cur_lyr")
sbl(cur_lyr, 'ARE_IDENTICAL_TO', cur_shp, "", "", INVERT)
mfl(cur_lyr, "shp_replace")
FindIdentical(shp_replace) -> GBD.dbf
n = getCount(^^output)
for i in range(n) #FEAT_SEQ = i+1 indexes at 0
search cursor or statistics_analysis?
    - Iterate thru selections of mathing atts from shp_replace
    - set SHAPE of OID1 to SHAPE of matching cur_shp
    - delete the others
