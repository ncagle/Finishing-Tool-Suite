import arcpy as ap
from arcpy import AddMessage as write


''''''''' Repair All NULL Geometry '''''''''
# Repairs all NULL geometries in each feature class
#### rewrite with intersect geometry method to remove duplicate vertices and kickbacks
def process_repair(featureclass):
    tool_name = 'Repair All NULL Geometry'
    write("\n--- {0} ---\n".format(tool_name))
    for fc in featureclass:
        try:
            write("Repairing NULL geometries in {0}".format(fc))
            ap.RepairGeometry_management(fc, "DELETE_NULL")
        except ap.ExecuteError:
            # if the code failed for the current fc, check the error
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(ap.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
            write("Exiting tool.\n")
            sys.exit(0)
