import arcpy
import fcfields
import os

#            ___________________________
#           | Checks for features with  |
#           | identical geometry and    |
#           | PSG attribution and       |
#           | removes them.             |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~

arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

# Pull in feature classes from TDS
featureclass = arcpy.ListFeatureClasses()

# Set the output directory for the FindIdentical tool
out_table = os.path.dirname(arcpy.env.workspace)
# Precreate the path for the output dBASE table
path = out_table.split(".")
path.pop()
table_loc = path[0] + str(".dbf")
arcpy.AddMessage("Creating temporary output file: " + str(table_loc))

# Loop feature classes and FindIdentical to get a count, then delete any found
for fc in featureclass:
    dick = fcfields.fc_fields[fc]
    arcpy.FindIdentical_management(fc, out_table, dick, "", "", output_record_option="ONLY_DUPLICATES")
    rows = int(arcpy.management.GetCount(table_loc).getOutput(0))
    arcpy.AddMessage("Found " + str(rows) + " duplicate " + str(fc) + " features.")
    if rows > 0:
        arcpy.DeleteIdentical_management(fc, fcfields.fc_fields[fc])
        arcpy.AddMessage("Deleted " + str(rows) + " duplicate " + str(fc) + " features.")

# Clean up before next process
del table_loc
