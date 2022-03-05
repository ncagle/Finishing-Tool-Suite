import arcpy
import sys

#            ___________________________
#           | Descales buildings within |
#           | BUAs that don't have      |
#           | important FFNs.           |
#      _    /???????????????????????????
#   __(.)< ?
#~~~\___)~~~

def buildingdescale():

	arcpy.env.workspace = arcpy.GetParameterAsText(0)
	arcpy.env.overwriteOutput = True

	# Make initial layers from the workspace
	fields = 'ZI026_CTUU'
	arcpy.AddMessage("\nRetrieving Settlement and Structure feature classes")
	arcpy.MakeFeatureLayer_management("SettlementSrf", "settlement_srf")
	arcpy.MakeFeatureLayer_management("StructureSrf", "structure_srf")
	arcpy.MakeFeatureLayer_management("StructurePnt", "structure_pnt")

	# Make layer of BUAs
	arcpy.AddMessage("Selecting BUAs")
	arcpy.SelectLayerByAttribute_management("settlement_srf", "NEW_SELECTION", "F_CODE = 'AL020'")
	arcpy.MakeFeatureLayer_management("settlement_srf", "buas")
	# Make layer of building surfaces
	arcpy.AddMessage("Selecting Buildings")
	arcpy.SelectLayerByAttribute_management("structure_srf", "NEW_SELECTION", "F_CODE = 'AL013'")
	arcpy.MakeFeatureLayer_management("structure_srf", "building_srf")
	# Make layer of building points
	arcpy.SelectLayerByAttribute_management("structure_pnt", "NEW_SELECTION", "F_CODE = 'AL013'")
	arcpy.MakeFeatureLayer_management("structure_pnt", "building_pnt")
	# Layer of building surfaces within BUAs
	arcpy.SelectLayerByLocation_management ("building_srf", "WITHIN", "buas", "", "NEW_SELECTION")
	arcpy.MakeFeatureLayer_management("building_srf", "bua_building_s")
	# Layer of building points within BUAs
	arcpy.SelectLayerByLocation_management ("building_pnt", "WITHIN", "buas", "", "NEW_SELECTION")
	arcpy.MakeFeatureLayer_management("building_pnt", "bua_building_p")
	# Select non important building surfaces
	# Adam's original list: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
	arcpy.AddMessage("Identifying buildings with important FFNs...")
	arcpy.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", "FFN IN (808, 811, 814, 813, 812, 818, 819, 822, 817, 815, 821, 825, 828, 826, 827, 835, 836, 829, 838, 837, 850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931, 932)")
	arcpy.SelectLayerByAttribute_management("bua_building_s", "SWITCH_SELECTION")
	arcpy.MakeFeatureLayer_management("bua_building_s", "non_import_s")
	# Select non important building points
	arcpy.SelectLayerByAttribute_management("bua_building_p", "NEW_SELECTION", "FFN IN (808, 811, 814, 813, 812, 818, 819, 822, 817, 815, 821, 825, 828, 826, 827, 835, 836, 829, 838, 837, 850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931, 932)")
	arcpy.SelectLayerByAttribute_management("bua_building_p", "SWITCH_SELECTION")
	arcpy.MakeFeatureLayer_management("bua_building_p", "non_import_p")

	# Count buildings and buas in selections
	bua_count = int(arcpy.GetCount_management("buas").getOutput(0))
	non_import_count_s = int(arcpy.GetCount_management("non_import_s").getOutput(0))
	non_import_count_p = int(arcpy.GetCount_management("non_import_p").getOutput(0))
	total_buildings = non_import_count_s + non_import_count_p

	# End script if there are no BUAs or no buildings inside them
	if bua_count == 0:
	    arcpy.AddMessage("\nNo BUAs found.")
	    sys.exit(0)
	elif total_buildings == 0:
	    arcpy.AddMessage("\nNo buildings in BUAs found.")
	    sys.exit(0)

	arcpy.AddMessage("\n" + str(total_buildings) + " buildings with important FFNs found in " + str(bua_count) + " total BUAs.")

	# Descale selected, non-important buildings within BUAs to CTUU 12500
	arcpy.AddMessage("Descaling unimportant building surfaces...")
	with arcpy.da.UpdateCursor("non_import_s", fields) as cursor_s:
	    for row in cursor_s:
	        row[0] = 12500
	        cursor_s.updateRow(row)

	arcpy.AddMessage("Descaling unimportant building points...")
	with arcpy.da.UpdateCursor("non_import_p", fields) as cursor_p:
	    for row in cursor_p:
	        row[0] = 12500
	        cursor_p.updateRow(row)

	arcpy.AddMessage("\n" + str(non_import_count_s) + " building surfaces descaled to CTUU 12500.")
	arcpy.AddMessage(str(non_import_count_p) + " building points descaled to CTUU 12500.\n")

buildingdescale ()

