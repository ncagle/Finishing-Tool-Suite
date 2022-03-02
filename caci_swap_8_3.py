# =========================== #
# CACI Swap CTUU and Scale v3 #
# Nat Cagle 2021-10-01        #
# =========================== #
import arcpy
from arcpy import AddMessage as write
from os import path

#            ________________________
#           | Flips Scale field with |
#           | CTUU field             |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~


''''''''' Parameters and Variables '''''''''

# Gets dataset and sets workspace
bungled = arcpy.GetParameterAsText(0)
arcpy.env.workspace = bungled
write(bungled)


# Create lists of feature classes from each database
fc_bungled = arcpy.ListFeatureClasses()
try:
	fc_bungled.remove('MetadataSrf')
	fc_bungled.remove('ResourceSrf')
	fc_bungled.sort()
except:
	write("Metadata and Resource Surfaces not present.")
	pass
fc_bungled.sort()
write("\nNote: It is up to the user to keep track of when things were swapped.\n      This tool swaps the fields back and forth regardless of which is the original.\n")
write("Found Scale field and CTUU field.")
fields = ['zi026_ctuu', 'scale', 'swap']


''''''''' Swippity Swappity Loop '''''''''
# Feature class loop
for fc in fc_bungled:
	write("Swapping CTUU and Scale fields for " + str(fc))
	# Creates temporary swap field
	#arcpy.DeleteField_management(fc, "swap")
	arcpy.AddField_management(fc, "swap", "LONG", 9)
	# Update cursor to juggle values
	with arcpy.da.UpdateCursor(fc, fields) as ucursor:
	    for row in ucursor:
			# Functions as three ring puzzle
			row[2] = row[1] #swap = scale
			row[1] = row[0] #scale = ctuu
			row[0] = row[2] #ctuu = swap
			ucursor.updateRow(row)
	# Deletes temporary swap field
	arcpy.DeleteField_management(fc, "swap")


# Faster way to do the loops if you don't need to edit the fields
# for fc in arcpy.ListFeatureClasses():

