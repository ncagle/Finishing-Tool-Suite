# ============================ #
# Hypernova Burst Multipart v4 #
# Nat Cagle 2021-09-28         #
# ============================ #
import arcpy
from arcpy import AddMessage as write
from datetime import datetime as dt

#            ___________________________
#           | Hypernova Burst Multipart |
#           | explodes multipart        |
#           | features for an entire    |
#           | dataset.                  |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~


fc_fields = { 'AeronauticCrv' : ['f_code','fcsubtype','ara','axs','lzn','pcf','sbb','txp','zi005_fna','zi006_mem','zi019_asp','zi019_asp2','zi019_asp3','zi019_asu','zi019_asu2','zi019_asu3','zi019_asx','zi019_sfs','zi026_ctuu','zi001_srt','shape@','version'],
              'AeronauticPnt' : ['f_code','fcsubtype','apt','apt2','apt3','ara','axs','ffn','ffn2','ffn3','fpt','haf','hgt','lmc','mcc','mcc2','mcc3','pcf','pec','trs','trs2','trs3','zi005_fna','zi006_mem','zi019_asp','zi019_asp2','zi019_asp3','zi019_asu','zi019_asu2','zi019_asu3','zi019_asx','zi019_sfs','zi026_ctuu','zi001_srt','shape@','version'],
              'AeronauticSrf' : ['f_code','fcsubtype','apt','apt2','apt3','apu','apu2','apu3','ara','asu','asu2','asu3','axs','ffn','ffn2','ffn3','fpt','haf','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','pec','sbb','trs','trs2','trs3','txp','wid','zi005_fna','zi006_mem','zi019_asp','zi019_asp2','zi019_asp3','zi019_asu','zi019_asu2','zi019_asu3','zi019_asx','zi019_sfs','zi026_ctuu','zi001_srt','shape@','version'],
              'AgriculturePnt' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','pcf','zi005_fna','zi006_mem','zi013_csp','zi013_csp2','zi013_csp3','zi013_pig','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'AgricultureSrf' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi013_csp','zi013_csp2','zi013_csp3','zi013_pig','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'BoundaryPnt' : ['f_code','fcsubtype','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'CultureCrv' : ['f_code','fcsubtype','ara','hgt','lmc','lzn','pcf','ssc','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'CulturePnt' : ['f_code','fcsubtype','ara','hgt','lmc','pcf','ssc','tty','zi005_fna','zi006_mem','zi026_ctuu','zi037_rel','zi001_srt','shape@','version'],
              'CultureSrf' : ['f_code','fcsubtype','ara','cam','hgt','lmc','lzn','pcf','ssc','tty','wid','zi005_fna','zi006_mem','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'FacilityPnt' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','pcf','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'FacilitySrf' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'HydroAidNavigationPnt' : ['f_code','fcsubtype','ara','hgt','lmc','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'HydroAidNavigationSrf' : ['f_code','fcsubtype','ara','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'HydrographyCrv' : ['f_code','fcsubtype','aoo','ara','atc','cda','cwt','dft','dfu','fcs','hgt','lmc','loc','lzn','mcc','mcc2','mcc3','nvs','pcf','rle','sbb','tid','trs','trs2','trs3','wcc','wid','woc','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'HydrographyPnt' : ['f_code','fcsubtype','aoo','azc','dft','dfu','dmd','dof','fcs','hgt','iwt','lmc','mcc','mcc2','mcc3','mns','ocs','pcf','tid','trs','trs2','trs3','woc','wst','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'HydrographySrf' : ['f_code','fcsubtype','aoo','ara','atc','azc','cda','cwt','dft','dfu','dmd','fcs','hgt','inu','iwt','lmc','loc','lzn','mcc','mcc2','mcc3','mns','nvs','ocs','pcf','rle','sbb','tid','trs','trs2','trs3','wcc','wid','woc','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'IndustryCrv' : ['f_code','fcsubtype','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'IndustryPnt' : ['f_code','fcsubtype','cra','crm','ffn','ffn2','ffn3','hgt','lmc','loc','pby','pby2','pby3','pcf','ppo','ppo2','ppo3','rip','srl','trs','trs2','trs3','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'IndustrySrf' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','loc','lzn','pby','pby2','pby3','pcf','ppo','ppo2','ppo3','srl','wid','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'InformationCrv' : ['f_code','fcsubtype','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'InformationPnt' : ['f_code','fcsubtype','nlt','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'InformationSrf' : ['f_code','fcsubtype','ara','lzn','vca','vca2','vca3','vct','vct2','vct3','wid','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'MilitaryCrv' : ['f_code','fcsubtype','eet','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'MilitaryPnt' : ['f_code','fcsubtype','caa','ffn','ffn2','ffn3','hgt','lmc','mcc','mcc2','mcc3','pcf','ppo','ppo2','ppo3','rle','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'MilitarySrf' : ['f_code','fcsubtype','ara','caa','eet','ffn','ffn2','ffn3','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','ppo','ppo2','ppo3','rle','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PhysiographyCrv' : ['f_code','fcsubtype','azc','fic','gft','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','trs','trs2','trs3','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PhysiographyPnt' : ['f_code','fcsubtype','aoo','got','hgt','lmc','mcc','mcc2','mcc3','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PhysiographySrf' : ['f_code','fcsubtype','aoo','ara','fic','got','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','sad','sdo','sdt','sic','trs','trs2','trs3','tsm','tsm2','tsm3','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PortHarbourCrv' : ['f_code','fcsubtype','ffn','ffn2','ffn3','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','pwc','wle','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PortHarbourPnt' : ['f_code','fcsubtype','ffn','ffn2','ffn3','hgt','lmc','mcc','mcc2','mcc3','pcf','tid','zi005_fna','zi006_mem','zi025_wle','zi026_ctuu','zi001_srt','shape@','version'],
              'PortHarbourSrf' : ['f_code','fcsubtype','ffn','ffn2','ffn3','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','pwc','tid','wid','wle','zi005_fna','zi006_mem','zi025_wle','zi026_ctuu','zi001_srt','shape@','version'],
              'RecreationCrv' : ['f_code','fcsubtype','ama','hgt','lmc','lzn','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'RecreationPnt' : ['f_code','fcsubtype','ama','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'RecreationSrf' : ['f_code','fcsubtype','ama','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'SettlementPnt' : ['f_code','fcsubtype','bac','ffn','ffn2','ffn3','lmc','pcf','zi005_fna','zi005_fna2','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'SettlementSrf' : ['f_code','fcsubtype','ara','bac','ffn','ffn2','ffn3','lmc','lzn','pcf','wid','zi005_fna','zi005_fna2','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StoragePnt' : ['f_code','fcsubtype','cbp','ffn','ffn2','ffn3','hgt','lmc','lun','pcf','ppo','ppo2','ppo3','spt','ssc','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StorageSrf' : ['f_code','fcsubtype','ara','cbp','ffn','ffn2','ffn3','hgt','lmc','lun','lzn','pcf','ppo','ppo2','ppo3','spt','ssc','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StructureCrv' : ['f_code','fcsubtype','bsu','hgt','lmc','lzn','pcf','wti','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StructurePnt' : ['f_code','fcsubtype','bsu','crm','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','rle','tos','ttc','ttc2','ttc3','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'StructureSrf' : ['f_code','fcsubtype','ara','bsu','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','rle','tos','ttc','ttc2','ttc3','wid','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','shape@','version'],
              'TransportationGroundCrv' : ['f_code','fcsubtype','acc','bot','bsc','bsc2','bsc3','cat','cwt','fco','ffn','ffn2','ffn3','gtc','hgt','loc','ltn','lzn','mcc','mcc2','mcc3','mes','one','owo','pcf','rfd','rin_roi','rin_roi2','rin_roi3','rin_rtn','rin_rtn2','rin_rtn3','rle','ror','rrc','rrc2','rrc3','rsa','rta','rty','rwc','sbb','sep','tra','trp','trs','trs2','trs3','tst','wid','wle','zi005_fna','zi006_mem','zi016_roc','zi016_wd1','zi016_wtc','zi017_gaw','zi017_rgc','zi017_rir','zi017_rra','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationGroundPnt' : ['f_code','fcsubtype','bot','bsc','bsc2','bsc3','cwt','dgc','ffn','ffn2','ffn3','gtc','hgt','lmc','mcc','mcc2','mcc3','mes','pcf','pym','rfd','rin_roi','rin_roi2','rin_roi3','rin_rtn','rin_rtn2','rin_rtn3','trp','trs','trs2','trs3','wid','zi005_fna','zi006_mem','zi016_roc','zi016_wtc','zi017_gaw','zi017_rgc','zi017_rra','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationGroundSrf' : ['f_code','fcsubtype','ara','bot','bsc','bsc2','bsc3','dgc','ffn','ffn2','ffn3','hgt','lmc','ltn','lzn','mcc','mcc2','mcc3','pcf','rfd','tra','trp','trs','trs2','trs3','vet','wid','wle','zi005_fna','zi006_mem','zi016_roc','zi017_gaw','zi017_rgc','zi017_rra','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationWaterCrv' : ['f_code','fcsubtype','aoo','cda','cwt','fer','hgt','lmc','loc','lzn','pcf','rle','sbb','trs','trs2','trs3','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationWaterPnt' : ['f_code','fcsubtype','aoo','hgt','lmc','pcf','trs','trs2','trs3','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationWaterSrf' : ['f_code','fcsubtype','aoo','ara','cda','cwt','hgt','lmc','loc','lzn','pcf','rle','sbb','trs','trs2','trs3','wid','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'UtilityInfrastructureCrv' : ['f_code','fcsubtype','cab','cab2','cab3','cst','cwt','hgt','loc','lzn','owo','pcf','plt','plt2','plt3','ppo','ppo2','ppo3','rle','rta','spt','tst','zi005_fna','zi006_mem','zi020_ge4','zi026_ctuu','zi001_srt','shape@','version'],
              'UtilityInfrastructurePnt' : ['f_code','fcsubtype','at005_cab','at005_cab2','at005_cab3','hgt','lmc','pcf','pos','pos2','pos3','ppo','ppo2','ppo3','srl','zi005_fna','zi006_mem','zi026_ctuu','zi032_pyc','zi032_pym','zi032_tos','zi001_srt','shape@','version'],
              'UtilityInfrastructureSrf' : ['f_code','fcsubtype','ara','hgt','lmc','lzn','pcf','pos','pos2','pos3','ppo','ppo2','ppo3','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'VegetationCrv' : ['f_code','fcsubtype','dmt','lmc','lzn','sbc','tre','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'VegetationPnt' : ['f_code','fcsubtype','hgt','lmc','tre','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'VegetationSrf' : ['f_code','fcsubtype','ara','dmt','hgt','lmc','lzn','sbc','tid','tre','veg','vsp','vsp2','vsp3','wid','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'MetadataSrf' : ['f_code','fcsubtype','mde','rcg','zi001_srt','shape@','version'],
              'ResourceSrf' : ['f_code','fcsubtype','ava','cid','cps','dqs','ets','etz','eva','hva','hzd','mde','mem','rcg','rtl','vdt','shape@','version']
}


arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
featureclass = arcpy.ListFeatureClasses()
try:
	featureclass.remove('MetadataSrf')
	featureclass.remove('ResourceSrf')
	featureclass.sort()
except:
	write("Metadata and Resource Surfaces not present.")
	pass
featureclass.sort()


class LicenseError(Exception):
    pass

try:
	if arcpy.CheckExtension("defense") == "Available":
		write("\n~~ Checking out Defense Mapping Extension ~~\n")
		arcpy.CheckOutExtension("defense")
	else:
		# raise a custom exception
		raise LicenseError


	##### Multipart Search #####

	fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
	fc_multi_list = []
	for fc in featureclass:
		write("Searching for multiparts in " + str(fc))
		multipart = False # Assume the feature class doesn't have multiparts
		with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as scursor:
			complex = 0 # Counts complex single part features. Mainly for debugging. Might remain in final
			for row in scursor: # For each feature in the fc
				shape = row[1] # Get SHAPE@ token to extract properties
				if shape is None: # Checks for NULL geometries
					write(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
					continue
				elif shape.isMultipart is True: # Does the feature have the isMultipart flag
					shape_type = str(shape.type) # Gets the geometry type of the feature
					if shape_type == 'polygon': # If the feature is a polygon, it may be a complex single part feature with interior rings
						if shape.partCount > 1: # If the number of geometric parts is more than one, then it is a true multipart feature
							if multipart is False: # And if that multipart feature is the first in the fc
								fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
								multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
							elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
								fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
							continue # Moves on to the next feature row in the search loop
						else: # If the part count is not greater than 1, then it is a complex single part feature with interior rings
							complex += 1
							continue # Moves on to the next feature row in the search loop
					else: # Non-polygon feature geometries do not have the isMultipart flaw since they have fewer dimensions. Simply proceed as normal
						if multipart is False: # And if that multipart feature is the first in the fc
							fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
							multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
						elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
							fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
			if multipart is True:
				count = len(fc_multi[fc])
				write("*** " + str(count) + " true multipart features found in " + str(fc) + " ***")
			elif complex > 0:
				write(str(complex) + " complex polygons found in " + str(fc))
			else:
				write("No multiparts found")
		if multipart is True:
			fc_multi_list.append(fc) # Creates iterable list of feature classes that have multipart features

	write(" ")
	if complex > 0:
		write("The complex polygons found are single part polygons with complex interior holes that are more likely to become multipart features.")
	write(" ")
	for fc in fc_multi_list:
		count = len(fc_multi[fc])
		write(str(count) + " multipart features found in " + str(fc))
		write("  OIDs - " + str(fc_multi[fc]))
	write(" ")


	##### Isolate, Explode, Replace #####

	in_class = "multi"
	out_class = "single"
	for fc in fc_multi_list:
		#sanitize feature class name from sde cz the sde always has to make things more difficult than they need to be...
		fc_parts = fc.split(".")
		if fc_parts[-1] in fc_fields:
			fcr = fc_parts[-1]
		else:
			write('Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin.')

		# Variables
		fc_geom = arcpy.Describe(fc).shapeType
		oid_field = arcpy.Describe(fc).OIDFieldName # Get the OID field name. Not necessary for every loop, but simple enough to just put here.
		fieldnames = fc_fields[fcr]
		sfields = [oid_field] + fieldnames
		oid_list_str = str(fc_multi[fc]) # Convert the list to a string and remove the []
		oid_list_str = oid_list_str[1:-1]
		query = str(oid_field) + " in ({})".format(oid_list_str) # Formats the query from the above variables as: OBJECTID in (1, 2, 3)

		# Create a new feature class to put the multipart features in to decrease processing time
		arcpy.CreateFeatureclass_management(arcpy.env.workspace, in_class, fc_geom, fc, "", "", arcpy.env.workspace)

		# Add multipart features to new feature class based on OID
		oid_list = fc_multi[fc]
		with arcpy.da.SearchCursor(fc, sfields, query) as scursor: # Search current fc using fc_fields with OID@ prepended as [0]
			with arcpy.da.InsertCursor(in_class, sfields) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
				for row in scursor: # For each feature in the current fc
					#write("if {0} in {1}:".format(row[0], oid_list))
					if row[0] in oid_list:
						#write("true. doing icursor.insertRow(row)")
						icursor.insertRow(row)

		write(str(fcr) + " multipart progenitor cores collapsing.")
		before_process = dt.now().time()
		arcpy.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
		after_process = dt.now().time()
		date = dt.now().date()
		datetime1 = dt.combine(date, after_process)
		datetime2 = dt.combine(date, before_process)
		time_delta = datetime1 - datetime2
		time_elapsed = str(time_delta.total_seconds())
		write("Hypernova burst detected after " + time_elapsed + " seconds.")

		write("Removing original multipart features.")
		# Deletes features in fc that have OIDs flagged as multiparts
		with arcpy.da.UpdateCursor(fc, oid_field) as ucursor:
			for row in ucursor:
				if row[0] in oid_list:
					ucursor.deleteRow()

		write("Replacing with singlepart features.")
		# Create search cursor and insert new rows from MultipartToSinglepart output out_class
		with arcpy.da.SearchCursor(out_class, fieldnames) as scursor:
			with arcpy.da.InsertCursor(fc, fieldnames) as icursor:
				for row in scursor:
					icursor.insertRow(row)

		write("Populating NULL fields with default values.")
		arcpy.CalculateDefaultValues_defense(fc)
		write(" ")

	arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(in_class)))
	arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(out_class)))


	write("~~ Checking Defense Mapping Extension back in ~~\n")
	arcpy.CheckInExtension("defense")
except LicenseError:
	write("Defense Mapping license is unavailable")


#''''''''' Multipart Search '''''''''
#
# fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
# fc_multi_list = []
# for fc in featureclass:
# 	write("Searching for multiparts in " + str(fc))
# 	multipart = False # Assume the feature class doesn't have multiparts
# 	with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as scursor:
# 		complex = 0 # Counts complex single part features. Mainly for debugging. Might remain in final
# 		for row in scursor: # For each feature in the fc
# 			shape = row[1] # Get SHAPE@ token to extract properties
# 			if shape is None: # Checks for NULL geometries
# 				write(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
# 				continue
# 			elif shape.isMultipart is True: # Does the feature have the isMultipart flag
# 				shape_type = str(shape.type) # Gets the geometry type of the feature
# 				if shape_type == 'polygon': # If the feature is a polygon, it may be a complex single part feature with interior rings
# 					if shape.partCount > 1: # If the number of geometric parts is more than one, then it is a true multipart feature
# 						if multipart is False: # And if that multipart feature is the first in the fc
# 							fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
# 							multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
# 						elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
# 							fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
# 						continue # Moves on to the next feature row in the search loop
# 					else: # If the part count is not greater than 1, then it is a complex single part feature with interior rings
# 						complex += 1
# 						continue # Moves on to the next feature row in the search loop
# 				else: # Non-polygon feature geometries do not have the isMultipart flaw since they have fewer dimensions. Simply proceed as normal
# 					if multipart is False: # And if that multipart feature is the first in the fc
# 						fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
# 						multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
# 					elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
# 						fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
# 		if multipart is True:
# 			count = len(fc_multi[fc])
# 			write("*** " + str(count) + " true multipart features found in " + str(fc) + " ***")
# 		elif complex > 0:
# 			write(str(complex) + " complex polygons found in " + str(fc))
# 		else:
# 			write("No multiparts found")
# 	if multipart is True:
# 		fc_multi_list.append(fc) # Creates iterable list of feature classes that have multipart features
#
# write(" ")
# if complex > 0:
# 	write("The complex polygons found are single part polygons with complex interior holes that are more likely to become multipart features.")
# write(" ")
# for fc in fc_multi_list:
# 	count = len(fc_multi[fc])
# 	write(str(count) + " multipart features found in " + str(fc))
# 	write("  OIDs - " + str(fc_multi[fc]))
# write(" ")
#
#
# ''''''''' Isolate, Explode, Replace '''''''''
#
# in_class = "multi"
# out_class = "single"
# for fc in fc_multi_list:
# 	#sanitize feature class name from sde cz the sde always has to make things more difficult than they need to be...
# 	fc_parts = fc.split(".")
# 	if fc_parts[-1] in fc_fields:
# 		fcr = fc_parts[-1]
# 	else:
# 		write('Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin.')
#
# 	# Variables
# 	fc_geom = arcpy.Describe(fc).shapeType
# 	oid_field = arcpy.Describe(fc).OIDFieldName # Get the OID field name. Not necessary for every loop, but simple enough to just put here.
# 	fieldnames = fc_fields[fcr]
# 	sfields = [oid_field] + fieldnames
# 	oid_list_str = str(fc_multi[fc]) # Convert the list to a string and remove the []
# 	oid_list_str = oid_list_str[1:-1]
# 	query = str(oid_field) + " in ({})".format(oid_list_str) # Formats the query from the above variables as: OBJECTID in (1, 2, 3)
#
# 	# Create a new feature class to put the multipart features in to decrease processing time
# 	arcpy.CreateFeatureclass_management(arcpy.env.workspace, in_class, fc_geom, fc, "", "", arcpy.env.workspace)
#
# 	# Add multipart features to new feature class based on OID
# 	oid_list = fc_multi[fc]
# 	with arcpy.da.SearchCursor(fc, sfields, query) as scursor: # Search current fc using fc_fields with OID@ prepended as [0]
# 		with arcpy.da.InsertCursor(in_class, sfields) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
# 			for row in scursor: # For each feature in the current fc
# 				#write("if {0} in {1}:".format(row[0], oid_list))
# 				if row[0] in oid_list:
# 					#write("true. doing icursor.insertRow(row)")
# 					icursor.insertRow(row)
#
# 	write(str(fcr) + " multipart progenitor cores collapsing.")
# 	before_process = dt.now().time()
# 	arcpy.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
# 	after_process = dt.now().time()
# 	date = dt.now().date()
# 	datetime1 = dt.combine(date, after_process)
# 	datetime2 = dt.combine(date, before_process)
# 	time_delta = datetime1 - datetime2
# 	time_elapsed = str(time_delta.total_seconds())
# 	write("Hypernova burst detected after " + time_elapsed + " seconds.")
#
# 	write("Removing original multipart features.")
# 	# Deletes features in fc that have OIDs flagged as multiparts
# 	with arcpy.da.UpdateCursor(fc, oid_field) as ucursor:
# 		for row in ucursor:
# 			if row[0] in oid_list:
# 				ucursor.deleteRow()
#
# 	write("Replacing with singlepart features.")
# 	# Create search cursor and insert new rows from MultipartToSinglepart output out_class
# 	with arcpy.da.SearchCursor(out_class, fieldnames) as scursor:
# 		with arcpy.da.InsertCursor(fc, fieldnames) as icursor:
# 			for row in scursor:
# 				icursor.insertRow(row)
#
# 	write("Populating NULL fields with default values.")
# 	arcpy.CalculateDefaultValues_defense(fc)
# 	write(" ")
#
# arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(in_class)))
# arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(out_class)))



### Trash Bin ###
# fc_multi = []
# for fc in featureclass:
# 	write("Searching for multiparts in " + str(fc))
# 	multipart = False
# 	with arcpy.da.SearchCursor(fc, 'SHAPE@') as scursor:
# 		for row in scursor:
# 			if multipart is False:
# 				shape = row[0]
# 				parts = int(shape.partCount)
# 				if parts > 1:
# 					multipart = True
# 			#write()"id={:d} parts={:d}".format(row[0],shape.partCount))
# 	if multipart is True:
# 		fc_multi.append(fc)
#
# write(" ")
# for fc in fc_multi:
# 	write("Multipart features found in " + str(fc))


# ''''''''' Multipart Search Doublecheck '''''''''
#
# fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
# fc_multi_list = []
# for fc in featureclass:
# 	write("Searching for multiparts in " + str(fc))
# 	multipart = False # Assume the feature class doesn't have multiparts
# 	with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as scursor:
# 		complex = 0 # Counts complex single part features. Mainly for debugging. Might remain in final
# 		for row in scursor: # For each feature in the fc
# 			shape = row[1] # Get SHAPE@ token to extract properties
# 			if shape is None: # Checks for NULL geometries
# 				write(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
# 				continue
# 			elif shape.isMultipart is True: # Does the feature have the isMultipart flag
# 				shape_type = str(shape.type) # Gets the geometry type of the feature
# 				if shape_type == 'polygon': # If the feature is a polygon, it may be a complex single part feature with interior rings
# 					if shape.partCount > 1: # If the number of geometric parts is more than one, then it is a true multipart feature
# 						if multipart is False: # And if that multipart feature is the first in the fc
# 							fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
# 							multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
# 						elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
# 							fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
# 						continue # Moves on to the next feature row in the search loop
# 					else: # If the part count is not greater than 1, then it is a complex single part feature with interior rings
# 						complex += 1
# 						continue # Moves on to the next feature row in the search loop
# 				else: # Non-polygon feature geometries do not have the isMultipart flaw since they have fewer dimensions. Simply proceed as normal
# 					if multipart is False: # And if that multipart feature is the first in the fc
# 						fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
# 						multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
# 					elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
# 						fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
# 		if multipart is True:
# 			count = len(fc_multi[fc])
# 			write("*** " + str(count) + " true multipart features found in " + str(fc) + " ***")
# 		else:
# 			write("No multiparts found")
# 	if multipart is True:
# 		fc_multi_list.append(fc) # Creates iterable list of feature classes that have multipart features
#
# write(" ")
#
# write("All multipart features removed.")


#try:
# for fc in fc_multi_list:
# 	if len(fc_multi[fc]) < 1: # Make sure the oid list has something in it. just in case
# 		write("Corrupt data in " + str(fc) + ". Cancelling operation... Please repair data.")
# 		sys.exit(0)
# 	# Creates fc specific variables.
# 	out_class = fc + "_single"
# 	oid_list_str = str(fc_multi[fc]) # Convert the list to a string and remove the []
# 	oid_list_str = oid_list_str[1:-1]
# 	oid_field = arcpy.Describe(fc).OIDFieldName # Get the OID field name. Not necessary for every loop, but simple enough to just put here.
# 	query = str(oid_field) + " in ({})".format(oid_list_str) # Formats the query from the above variables as: OBJECTID in (1, 2, 3)
# 	write(fc)
# 	write(query)
#
# 	write("making feature layer 1")
# 	arcpy.MakeFeatureLayer_management(fc, fc + str("_lyr"))
# 	write("selecting layer by oid query")
# 	arcpy.SelectLayerByAttribute_management(fc + str("_lyr"), "NEW_SELECTION", query) # Selects the OIDs that have been flagged as multiparts
# 	write("making feature layer of only multipart oids")
# 	arcpy.MakeFeatureLayer_management(fc + str("_lyr"), "multi_lyr")
#
# 	write("running multipart to singlepart. probably the slow bit")
# 	before_process = dt.now().time()
# 	arcpy.MultipartToSinglepart_management("multi_lyr", out_class) # New feature class output of just the converted single parts
# 	after_process = dt.now().time()
# 	date = dt.now().date()
# 	datetime1 = dt.combine(date, after_process)
# 	datetime2 = dt.combine(date, before_process)
# 	time_elapsed = datetime1 - datetime2
# 	write(time_elapsed)
#
# 	write("finished multi to single. now deleting originals")
# 	# Deletes features in fc that have OIDs flagged as multiparts
# 	with arcpy.da.UpdateCursor(fc, oid_field) as ucursor:
# 		for row in ucursor:
# 			for oid in fc_multi[fc]:
# 				if row[0] is oid:
# 					ucursor.deleteRow()
#
# 	write("gathering field names")
# 	fieldnames = fc_fields[fc]
# 	# # Get field objects from source FC
# 	# dsc = arcpy.Describe(fc)
# 	# fields = dsc.fields
# 	# # List all field names except the OID field and geometry fields
# 	# # Replace 'SHAPE@' with 'SHAPE@'
# 	# out_fields = [dsc.OIDFieldName, dsc.lengthFieldName, dsc.areaFieldName]
# 	# fieldnames = [field.name if field.name != 'SHAPE@' else 'SHAPE@' for field in fields if field.name not in out_fields]
# 	write(fieldnames)
#
# 	write("inserting newly created single part features")
# 	# Create search cursor and insert new rows from MultipartToSinglepart output
# 	with arcpy.da.SearchCursor(out_class, fieldnames) as scursor:
# 		with arcpy.da.InsertCursor(fc, fieldnames) as icursor:
# 			for row in scursor:
# 				icursor.insertRow(row)
#
# 	write("deleting multipart to single part feature class output")
# 	arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(out_class)))
# 	write(" ")

# except arcpy.ExecuteError:
# 	write(arcpy.GetMessages())
# except Exception as err:
# 	write(err)

# if find_only is False:
# 	try:
# 		# Full rip and replace method since the MultipartToSinglepart makes a new fc anyway, just replace it.
# 		for fc in fc_multi:
# 			out_class = fc + "_single"
#
# 			# Run the tool to create a new fc with only singlepart features
# 			write("Exploding multipart features in " + str(fc))
# 			arcpy.MultipartToSinglepart_management(fc, out_class)
#
# 			# Check if there is a different number of features in the output
# 			# than there was in the input
# 			in_count = int(arcpy.GetCount_management(fc).getOutput(0))
# 			out_count = int(arcpy.GetCount_management(out_class).getOutput(0))
#
# 			# if in_count != out_count:
# 			multi_count = out_count - in_count
# 			write(str(multi_count) + " multipart features found in {0}".format(fc))
#
# 			write("Deleting originals")
# 			arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(fc)))
# 			arcpy.DeleteField_management(out_class, 'ORIG_FID')
# 			write("Replacing with single parts")
# 			arcpy.Rename_management(out_class, fc)
# 			# else:
# 			# 	write("No multipart features were found in " + str(fc))
# 			# 	arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(out_class)))

		# # Method replaces just the multipart features back into the original fc
		# # but it still has to make an entire copy of the fc with all single parts.
		# for fc in featureclass:
		# 	out_class = fc + "_singlepart"
		#
		# 	# Determine what the name of the Object ID is
		# 	oid_field = arcpy.Describe(fc).OIDFieldName
		#
		# 	# Run the tool to create a new fc with only singlepart features
		# 	arcpy.MultipartToSinglepart_management(fc, out_class)
		#
		# 	# Check if there is a different number of features in the output
		# 	# than there was in the input
		# 	in_count = int(arcpy.GetCount_management(fc).getOutput(0))
		# 	out_count = int(arcpy.GetCount_management(out_class).getOutput(0))
		#
		# 	if in_count != out_count:
		# 		multi_count = out_count - in_count
		#
		# 		# If there is a difference, write out the FID of the input
		# 		# features which were multipart
		# 		arcpy.Frequency_analysis(out_class, out_class + "_freq", 'ORIG_FID') ### DELETE
		#
		# 		# Use a search cursor to go through the table, and add the duplicate ORIG_FIDs to a list
		# 		write(str(multi_count) + "multipart features found in {0}".format(fc))
		# 		multi_oids = []
		# 		with arcpy.da.SearchCursor(out_class + "_freq", ['ORIG_FID'], "FREQUENCY > 1") as scursor:
		# 			for row in scursor:
		# 				multi_oids.append(int(row[0]))
		# 			multi_oids = list(set(multi_oids))
		#
		# 		# Deletes features in fc that have the OID of the multipart features
		# 		with arcpy.da.UpdateCursor(fc, oid_field) as ucursor:
		# 			for row in ucursor:
		# 				for oid in multi_oids:
		# 					if row[0] == oid:
		# 						ucursor.deleteRow()
		#
		# 		# Get field objects from source FC
		# 		dsc = arcpy.Describe(fc)
		# 		fields = dsc.fields
		#
		# 		# List all field names except the OID field and geometry fields
		# 		# Replace 'SHAPE@' with 'SHAPE@'
		# 		out_fields = [dsc.OIDFieldName, dsc.lengthFieldName, dsc.areaFieldName]
		# 		fieldnames = [field.name if field.name != 'SHAPE@' else 'SHAPE@' for field in fields if field.name not in out_fields]
		#
		# 		# Create search cursor and insert new rows from MultipartToSinglepart output
		# 		with arcpy.da.SearchCursor(out_class, fieldnames) as scursor:
		# 			with arcpy.da.InsertCursor(fc, fieldnames) as icursor:
		# 				for row in scursor:
		# 					icursor.insertRow(row)
		#
		# 	else:
		# 		write("No multipart features were found")
		#
		# 	# Dont forget to delete the _singlepart feature class

	# except arcpy.ExecuteError:
	# 	write(arcpy.GetMessages())
	# except Exception as err:
	# 	write(err)
