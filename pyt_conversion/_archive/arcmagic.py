import arcpy as ap
from arcpy import AddMessage as write


''''''''' Repair All NULL Geometry '''''''''
# Repairs all NULL geometries in each feature class
#### rewrite with intersect geometry method to remove duplicate vertices and kickbacks
def process_repair(featureclass):
	tool_name = 'Repair All NULL Geometry'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		write("Repairing NULL geometries in {0}".format(fc))
		ap.RepairGeometry_management(fc, "DELETE_NULL")


def write_info(name, var): # Write information for given variable
	#write_info('var_name', var)
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	write("Debug info for {0}:".format(name))
	write("   Variable Type: {0}".format(type(var)))
	if type(var) is str or type(var) is unicode:
		write("   Assigned Value: '{0}'".format(var))
	else:
		write("   Assigned Value: {0}".format(var))
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
