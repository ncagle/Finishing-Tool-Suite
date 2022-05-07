import ap as ap
from ap import AddMessage as write
from ap import AddFieldDelimiters as fieldDelim
import os
import math
import datetime as dt
import pandas as pd
import numpy as np
import sys

# Place Constants Here

""" ArcMagic Functions """
# Explicit is better than implicit
# Lambda function works better than "if not fieldname:", which can falsely catch 0.
populated = lambda x: x is not None and str(x).strip() != '' # Function that returns boolean of if input field is populated or empty
not_null = lambda x: x is not None
is_null = lambda x: x is None

def add_row_tuple(add_row, index, val): # Adds new index in row tuple with specified value
	# Reminder: The length of the row tuple has to match the target cursor to be applied
	#for add_row in cursor:
	##add_row = add_row_tuple(add_row, index, value)
	##icursor.insertRow(add_row)
	add_row = list(add_row)
	place = int((abs(index)-1) * (index/abs(index)))
	add_row.insert(place, val)
	return tuple(add_row)

def update_row_tuple(edit_row, index, val): # Update a specific row field inside a cursor tuple
	# Usually used for updating geometry before copying the row
	# For short tuples, slicing and concatenation is faster
	# But performance of long tuples is more consistently efficient with list conversion
	#for edit_row in cursor:
	##edit_row = update_row_tuple(edit_row, index, value)
	##icursor.insertRow(edit_row)
	edit_row = list(edit_row)
	edit_row[index] = val
	return tuple(edit_row)

def remove_row_tuple(rem_row, index): # Remove specified index from row tuple
	# Reminder: The length of the row tuple has to match the target cursor to be applied
	#for rem_row in cursor:
	##rem_row = remove_row_tuple(rem_row, index, value)
	##icursor.insertRow(rem_row)
	rem_row = list(rem_row)
	rem_row.pop(index)
	return tuple(rem_row)

def writeresults(tool_name):
	write("\n\n***Failed to run {0}.***\n".format(tool_name))
	messages = ap.GetMessages(0)
	warnings = ap.GetMessages(1)
	errors = ap.GetMessages(2)
	write("GP Tool Outputs:")
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	write(messages)
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	if len(warnings) > 0:
		write("Tool Warnings:")
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		write(warnings)
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	if len(errors) > 0:
		write("Error Report:")
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		write(errors)
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	write('                       ______\n                    .-"      "-.\n                   /            \\\n       _          |              |          _\n      ( \\         |,  .-.  .-.  ,|         / )\n       > "=._     | )(__/  \\__)( |     _.=" <\n      (_/"=._"=._ |/     /\\     \\| _.="_.="\\_)\n             "=._ (_     ^^     _)"_.="\n                 "=\\__|IIIIII|__/="\n                _.="| \\IIIIII/ |"=._\n      _     _.="_.="\\          /"=._"=._     _\n     ( \\_.="_.="     `--------`     "=._"=._/ )\n      > _.="                            "=._ <\n     (_/                                    \\_)\n')
	write("Please rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong.".format(tool_name))
	write("Exiting tool.\n")
	sys.exit(0)
	#print(u'                 uuuuuuu\n             uu$$$$$$$$$$$uu\n          uu$$$$$$$$$$$$$$$$$uu\n         u$$$$$$$$$$$$$$$$$$$$$u\n        u$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$"   "$$$"   "$$$$$$u\n       "$$$$"      u$u       $$$$"\n        $$$u       u$u       u$$$\n        $$$u      u$$$u      u$$$\n         "$$$$uu$$$   $$$uu$$$$"\n          "$$$$$$$"   "$$$$$$$"\n            u$$$$$$$u$$$$$$$u\n             u$"|¨|¨|¨|¨|"$u\n  uuu        $$u|¯|¯|¯|¯|u$$       uuu\n u$$$$        $$$$$u$u$u$$$       u$$$$\n  $$$$$uu      "$$$$$$$$$"     uu$$$$$$\nu$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$\n$$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"\n """      ""$$$$$$$$$$$uu ""$"""\n           uuuu ""$$$$$$$$$$uuu\n  u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$\n  $$$$$$$$$$""""           ""$$$$$$$$$$$"\n   "$$$$$"                      ""$$$$""\n     $$$"                         $$$$"')


def populate_null(fc, field_list, default):
	#populate_null(fc, string_fields, <'noInformation' or -999999>)
	count = 0
	with arcpy.da.UpdateCursor(fc, field_list) as ucursor:
		print("Assigning domain defaults from coded values...")
		for urow in ucursor: #for j, urow in enumerate(ucursor) where j+1 gives the row number
			row_count = 0
			if any(map(is_null, urow)):
				for i, val in enumerate(urow):
					if not_null(val):
						continue
					else:
						urow = update_row_tuple(urow, i, default)
						row_count +=1
						count +=1
			else:
				continue
			if row_count > 0:
				ucursor.updateRow(urow)
	return count









def grand_entrance(tds_db, boolean_dict):
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
	# Title Formatting and Workspace Setup #
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

	# Sanitizing GDB name
	tds_split = tds_db.split("\\")
	tds_split.pop()
	rresults = tds_split
	gdb_file = tds_split.pop()
	name_list = gdb_file.split(".")
	name_list.pop()
	gdb_name = name_list[0]
	#rresults.pop()
	rresults = "\\".join(rresults)


	# Tool title with GDB name formatting
	write("")
	slines = u"______________________________________"
	sspaces = u"                                      "
	exl = ""
	exs = ""
	exgl = "" # odd left dominant
	exgr = ""
	range_len = 38 - len(gdb_name)
	if range_len > 0:
		if (range_len % 2) == 0:
			rn0 = range_len/2
			for i in range(int(rn0)):
				exgl += " "
				exgr += " "
		else:
			rn1 = int(float(range_len)/2)
			for i in range(rn1):
				exgl += " "
			rn2 = rn1 + 1
			for i in range(int(rn2)):
				exgr += " "
	if len(gdb_name) > 38:
		extra = len(gdb_name) - 38

		for i in range(extra):
			exl += "_"
			exs += " "


	# Report of requested tasks
	write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

	if boolean_dict['secret']:
		write(u"    |          By order of the Liberator         {0}|".format(exs))
		write(u"    |        The leader of the free people       {0}|".format(exs))
		write(u"    |      _______        _                      {0}|".format(exs))
		write(u"    |     / ___/ /  ___ _(_)_____ _  ___ ____    {0}|".format(exs))
		write(u"    |    / /__/ _ \/ _ `/ / __/  ' \/ _ `/ _ \   {0}|".format(exs))
		write(u"    |    \___/_//_/\_,_/_/_/ /_/_/_/\_,_/_//_/   {0}|".format(exs))
		write(u"    |               ___           __             {0}|".format(exs))
		write(u"    |              / _ )___  ____/ /__           {0}|".format(exs))
		write(u"    |             / _  / _ \/ __/  '_/           {0}|".format(exs))
		write(u"    |            /____/\___/\__/_/\_\            {0}|".format(exs))
		write(u"    |   {0}   {1}|".format(sspaces, exs))
		write(u"    |        The following Finishing tasks       {0}|".format(exs))
		write(u"    |              shall be executed             {0}|".format(exs))
		write(u"    |   {0}   {1}|".format(sspaces, exs))
		write(u"    |   {0}   {1}|".format(sspaces, exs))

	write(u"    |   ======  Processes  Initialized  ======   {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	if boolean_dict['repair']:
		write(u"    |     - Repair All NULL Geometries           {0}|".format(exs))
	if boolean_dict['fcode']:
		write(u"    |     - Populate F_Codes                     {0}|".format(exs))
	if boolean_dict['defaults']:
		write(u"    |     - Calculate Default Values             {0}|".format(exs))
	if boolean_dict['metrics']:
		write(u"    |     - Calculate Metrics                    {0}|".format(exs))
	if boolean_dict['ufi']:
		write(u"    |     - Update UFI Values                    {0}|".format(exs))
	if boolean_dict['hydro'] or boolean_dict['trans'] or boolean_dict['util']:
		write(u"    |     - Integrate and Repair:                {0}|".format(exs))
		if boolean_dict['large']:
			write(u"    |        ~ Large Dataset ~                   {0}|".format(exs))
		if boolean_dict['hydro']:
			write(u"    |          Hydro                             {0}|".format(exs))
		if boolean_dict['trans']:
			write(u"    |          Trans                             {0}|".format(exs))
		if boolean_dict['util']:
			write(u"    |          Utilities                         {0}|".format(exs))
	if boolean_dict['dups']:
		write(u"    |     - Delete Identical Features            {0}|".format(exs))
	if boolean_dict['explode']:
		write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
	if boolean_dict['bridge']:
		write(u"    |     - Default Bridge WID Updater           {0}|".format(exs))
	if boolean_dict['pylong']:
		write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
	if boolean_dict['building']:
		write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
	if boolean_dict['swap']:
		write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
	if boolean_dict['fcount']:
		write(u"    |     - Generate Feature Report              {0}|".format(exs))
	if boolean_dict['vsource']:
		write(u"    |     - Generate Source Report               {0}|".format(exs))

	write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
	write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
	write("\n")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Data Maintenance Tools Category   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

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
			writeresults(tool_name)


''''''''' Populate F_Codes '''''''''
# John Jackson's Fcode tool refactored from standalone with included dictionaries instead of imported
def process_fcode():
	tool_name = 'Populate F_Codes'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			try:
				fields = ['f_code', 'fcsubtype']
				write("Updating {0} Feature F_Codes".format(fc))
				with ap.da.UpdateCursor(fc, fields) as fcursor:
					for row in fcursor: # Checks if F_Code matches the FCSubtype value. Updates F_Code if they don't match assuming proper subtype
						if row[0] != str(sub2fcode_dict[row[1]]):
							row[0] = str(sub2fcode_dict[row[1]])
							fcursor.updateRow(row)
			except:
				write("{0} does not contain F_codes.".format(fc))
		except ap.ExecuteError:
			writeresults(tool_name)


''''''''' Calculate Default Values '''''''''
# Calculate default values for NULL attributes
# All or nothing. Functions on datasets not individual feature classes
def process_defaults():
	tool_name = 'Calculate Default Values'
	write("\n--- {0} ---\n".format(tool_name))
	try:
		count_nulls = 0
		for fc in featureclass:
			write("Constructing field type lists to match default values to domain definitions.")
			out_fields = ['shape', 'area', 'length', 'created', 'edited', 'f_code', 'fcsubtype', 'ufi', 'version']
			in_types = ['Double', 'Integer', 'Single', 'SmallInteger']
			string_fields = [field.name for field in arcpy.ListFields(fc, None, 'String') if not any(substring in field.name for substring in out_fields)]
			number_fields = [field.name for field in arcpy.ListFields(fc) if field.type in in_types and not any(substring in field.name for substring in out_fields)]
			string_fields.sort()
			number_fields.sort()
			fc_nulls = 0
			write("Locating NULL text fields in {0}".format(fc))
			fc_nulls += populate_null(fc, string_fields, 'noInformation')
			write("Locating NULL numeric fields in {0}".format(fc))
			fc_nulls += populate_null(fc, number_fields, -999999)
			write("{0} NULL values populated in {1}".format(fc_nulls, fc))
			count_nulls += fc_nulls
		write('{0} total NULL values populated with default values'.format(count_nulls))
	except ap.ExecuteError:
		writeresults(tool_name)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Inline working version
not_null = lambda x: x is not None
is_null = lambda x: x is None
def update_row_tuple(edit_row, index, val): # Update a specific row field inside a cursor tuple
	edit_row = list(edit_row)
	edit_row[index] = val
	return tuple(edit_row)

tool_name = 'Calculate Default Values'
print("\n--- {0} ---\n".format(tool_name))
def populate_null(fc, field_list, default):
	count = 0
	with arcpy.da.UpdateCursor(fc, field_list) as ucursor:
		print("Assigning domain defaults from coded values...")
		for urow in ucursor:
			row_count = 0
			if any(map(is_null, urow)):
				for i, val in enumerate(urow):
					if not_null(val):
						continue
					else:
						urow = update_row_tuple(urow, i, default)
						row_count +=1
						count +=1
			else:
				continue
			if row_count > 0:
				ucursor.updateRow(urow)
	return count

count_nulls = 0
featureclass = ['UtilityInfrastructureCurves', 'TransportationGroundCurves']
for fc in featureclass:
	print("Constructing {0} field lists by type to match default values to domain definitions.".format(fc))
	out_fields = ['shape', 'area', 'length', 'created', 'edited', 'f_code', 'fcsubtype', 'ufi', 'version']
	in_types = ['Double', 'Integer', 'Single', 'SmallInteger']
	string_fields = [field.name for field in arcpy.ListFields(fc, None, 'String') if not any(substring in field.name for substring in out_fields)]
	number_fields = [field.name for field in arcpy.ListFields(fc) if field.type in in_types and not any(substring in field.name for substring in out_fields)]
	string_fields.sort()
	number_fields.sort()

	fc_nulls = 0
	print("Locating NULL text fields in {0}".format(fc))
	fc_nulls += populate_null(fc, string_fields, 'noInformation')
	print("Locating NULL numeric fields in {0}".format(fc))
	fc_nulls += populate_null(fc, number_fields, -999999)
	print("{0} NULL values populated in {1}".format(fc_nulls, fc))
	count_nulls += fc_nulls
print('{0} total NULL values populated with default values'.format(count_nulls))



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEFENSE MAPPING
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
#### Defense mapping version takes too long and crashes. just rewrite with manual calculations
def process_metrics():
	tool_name = 'Calculate Metrics'
	write("\n--- {0} ---\n".format(tool_name))
	metric_type = 'LENGTH;WIDTH;AREA;ANGLE_OF_ORIENTATION'
	for fc in featureclass:
		try:
			write("Calculating AOO, ARA, LZN, and WID for {0}".format(fc))
			ap.CalculateMetrics_defense(fc, metric_type, "LZN", "WID", "ARA", "#", "#", "#")
		except ap.ExecuteError:
			writeresults(tool_name)



''''''''' Update UFI Values ''''''''' ##### add functionality to only update blank fields
# Iterate through all features and update the ufi field with uuid4 random values
def process_ufi():
	tool_name = 'Update UFI Values'
	write("\n--- {0} ---\n".format(tool_name))
	ufi_count = 0
	for fc in featureclass:
		try:
			with ap.da.SearchCursor(fc, 'ufi') as scursor:
				values = [row[0] for row in scursor]
			with ap.da.UpdateCursor(fc, 'ufi') as ucursor:
				for row in ucursor:
					if not populated(row[0]):
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					elif values.count(row[0]) > 1:
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					ucursor.updateRow(row)
				write("Updated UFIs in {0}".format(fc))
		except ap.ExecuteError:
			writeresults(tool_name)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Feature Specific Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Integrate and Repair '''''''''
# User choice to Integrate and Repair Hydrography curves, TransportationGround curves, or Utility points and surfaces to curves

def process_hydro():
	tool_name = 'Hydrography Curves'
	fc1 = 'HydrographyCrv'
	fc2 = 'HydrographySrf'
	if not ap.Exists(fc1):
		write("**HydrographyCrv feature class not found\n  To run Integrate, copy an empty Hydro curve feature class from a blank schema into this dataset and run the tool again.")
		return 0
	if not ap.Exists(fc2):
		write("**HydrographySrf feature class not found\n  To run Integrate, copy an empty Hydro surface feature class from a blank schema into this dataset and run the tool again.")
		return 0
	write("- - - - - - - - - - - - - - - - - - - - - - ")
	write(" ~ {0} ~ ".format(tool_name))
	write("Making {0} and {1} feature layers".format(fc1, fc2))
	ap.MakeFeatureLayer_management(fc1, "hc")
	ap.MakeFeatureLayer_management(fc2, "hs")
	ap.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("hs", "NEW_SELECTION", "zi026_ctuu >= 50000")
	ap.MakeFeatureLayer_management("hc", "hc_scale")
	srf_count = int(ap.GetCount_management("hs").getOutput(0))
	if srf_count > 0:
		ap.MakeFeatureLayer_management("hs", "hs_scale")
	write("Repairing {0} lines before Integration".format(fc1))
	ap.RepairGeometry_management("hc_scale", "DELETE_NULL")
	hfeat_count = 0
	if not large:
		try:
			feat_count = int(ap.GetCount_management("hc_scale").getOutput(0))
			write("Integrating {0} {1} features and \n            {2} {3} features...".format(feat_count, fc1, srf_count, fc2))
			if srf_count > 0:
				ap.Integrate_management("hc_scale 1;hs_scale 2", "0.06 Meters")
				ap.Integrate_management("hc_scale 1;hs_scale 2", "0.03 Meters")
			else:
				ap.Integrate_management('hc_scale', "0.06 Meters")
				ap.Integrate_management('hc_scale', "0.03 Meters")
			hfeat_count = feat_count + srf_count
		except ap.ExecuteError:
			writeresults(tool_name)
	if large:
		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(fc1)
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			ap.MinimumBoundingGeometry_management(fc1, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with ap.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc1, "POLYGON")
			#ap.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			ap.MakeFeatureLayer_management(mem_fc, "hgrid")
			with ap.da.SearchCursor("hgrid", ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					ap.SelectLayerByAttribute_management("hgrid", "NEW_SELECTION", select)
					if srf_count > 0:
						ap.SelectLayerByLocation_management("hs_scale", "INTERSECT", "hgrid","","NEW_SELECTION")
						ssrf_count = int(ap.GetCount_management("hs_scale").getOutput(0))
					else:
						ssrf_count = 0
					ap.SelectLayerByLocation_management("hc_scale", "INTERSECT", "hgrid","","NEW_SELECTION")
					feat_count = int(ap.GetCount_management("hc_scale").getOutput(0))
					write("Integrating {0} {1} features and\n            {2} {3} features in partition {4}...".format(feat_count, fc1, ssrf_count, fc2, row[0]))
					hfeat_count = hfeat_count + feat_count + ssrf_count
					if ssrf_count > 0:
						ap.Integrate_management("hc_scale 1;hs_scale 2", "0.06 Meters")
						ap.Integrate_management("hc_scale 1;hs_scale 2", "0.03 Meters")
					elif feat_count > 0:
						ap.Integrate_management('hc_scale', "0.06 Meters")
						ap.Integrate_management('hc_scale', "0.03 Meters")
					else:
						continue
			write("Freeing partition memory")
			ap.Delete_management("in_memory")
			ap.Delete_management("hgrid")
		except ap.ExecuteError:
			writeresults(tool_name)
	write("Repairing {0} and {1} features after Integration".format(fc1, fc2))
	ap.RepairGeometry_management("hc_scale", "DELETE_NULL")
	ap.RepairGeometry_management("hs_scale", "DELETE_NULL")
	write("Clearing process cache")
	ap.Delete_management("hc")
	ap.Delete_management("hc_scale")
	ap.Delete_management("hs")
	ap.Delete_management("hs_scale")
	if trans or util:
		write("- - - - - - - - - - - - - - - - - - - - - -\n")
	else:
		write("- - - - - - - - - - - - - - - - - - - - - -")


def process_trans():
	tool_name = 'Transportation Points and Curves'
	fc1 = 'TransportationGroundPnt'
	fc2 = 'TransportationGroundCrv'
	if not ap.Exists(fc1):
		fc1 = fc2
	if not ap.Exists(fc2):
		write("**TransportationGroundCrv feature class not found\n  To run Integrate, copy an empty Trans curve feature class from a blank schema into this dataset and run the tool again.")
		break
	write("- - - - - - - - - - - - - - - - - - - - - - ")
	write(" ~ {0} ~ ".format(tool_name))
	write("Making {0} and {1} feature layers".format(fc1, fc2))
	ap.MakeFeatureLayer_management(fc1, "tgp")
	ap.MakeFeatureLayer_management(fc2, "tgc")
	ap.SelectLayerByAttribute_management("tgp", "NEW_SELECTION", "f_code = 'AQ065' AND zi026_ctuu >= 50000")
	cul_count = int(ap.GetCount_management("tgp").getOutput(0))
	ap.SelectLayerByAttribute_management("tgc", "NEW_SELECTION", "zi026_ctuu >= 50000")
	if cul_count > 0:
		ap.MakeFeatureLayer_management("tgp", "tgp_scale")
	ap.MakeFeatureLayer_management("tgc", "tgc_scale")
	write("Repairing {0} lines before Integration".format(fc2))
	ap.RepairGeometry_management("tgc_scale", "DELETE_NULL")
	tfeat_count = 0
	if not large:
		try:
			feat_count = int(ap.GetCount_management("tgc_scale").getOutput(0))
			write("Integrating {0} {1} features and\n            {2} Culvert points...".format(feat_count, fc2, cul_count))
			if cul_count > 0:
				ap.Integrate_management("tgp_scale 2;tgc_scale 1", "0.06 Meters")
				ap.Integrate_management("tgp_scale 2;tgc_scale 1", "0.03 Meters")
			else:
				ap.Integrate_management("tgc_scale", "0.06 Meters")
				ap.Integrate_management("tgc_scale", "0.03 Meters")
			tfeat_count = feat_count + cul_count
		except ap.ExecuteError:
			writeresults(tool_name)
	if large:
		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(fc2)
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			ap.MinimumBoundingGeometry_management(fc2, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with ap.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc2, "POLYGON")
			#ap.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			ap.MakeFeatureLayer_management(mem_fc, "tgrid")
			with ap.da.SearchCursor("tgrid", ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					ap.SelectLayerByAttribute_management("tgrid", "NEW_SELECTION", select)
					if cul_count > 0:
						ap.SelectLayerByLocation_management("tgp_scale", "INTERSECT", "tgrid","","NEW_SELECTION")
						pcul_count = int(ap.GetCount_management("tgp_scale").getOutput(0))
					else:
						pcul_count = 0
					ap.SelectLayerByLocation_management("tgc_scale", "INTERSECT", "tgrid","","NEW_SELECTION")
					feat_count = int(ap.GetCount_management("tgc_scale").getOutput(0))
					write("Integrating {0} {1} features and\n            {2} Culvert points in partition {3}...".format(feat_count, fc2, pcul_count, row[0]))
					tfeat_count = tfeat_count + feat_count + pcul_count
					if pcul_count > 0:
						ap.Integrate_management("tgp_scale 2;tgc_scale 1", "0.06 Meters")
						ap.Integrate_management("tgp_scale 2;tgc_scale 1", "0.03 Meters")
					elif feat_count > 0:
						ap.Integrate_management("tgc_scale", "0.06 Meters")
						ap.Integrate_management("tgc_scale", "0.03 Meters")
					else:
						continue
			write("Freeing partition memory")
			ap.Delete_management("in_memory")
			ap.Delete_management("tgrid")
		except ap.ExecuteError:
			writeresults(tool_name)
	write("Repairing {0} lines after Integration".format(fc2))
	ap.RepairGeometry_management("tgc_scale", "DELETE_NULL")
	write("Clearing process cache")
	ap.Delete_management("tgp")
	ap.Delete_management("tgc")
	ap.Delete_management("tgp_scale")
	ap.Delete_management("tgc_scale")
	if util:
		write("- - - - - - - - - - - - - - - - - - - - - -\n")
	else:
		write("- - - - - - - - - - - - - - - - - - - - - -")


def process_util():
	tool_name = 'Utility Points, Lines, and Surfaces'
	fc1 = 'UtilityInfrastructurePnt'
	fc2 = 'UtilityInfrastructureCrv'
	fc3 = 'UtilityInfrastructureSrf'
	if not ap.Exists(fc1):
		write("**UtilityInfrastructurePnt feature class not found\n  To run Integrate, copy an empty Utility point feature class from a blank schema into this dataset and run the tool again.")
		return 0
	if not ap.Exists(fc2):
		write("**UtilityInfrastructureCrv feature class not found\n  To run Integrate, copy an empty Utility curve feature class from a blank schema into this dataset and run the tool again.")
		return 0
	if not ap.Exists(fc3):
		write("**UtilityInfrastructureSrf feature class not found\n  To run Integrate, copy an empty Utility surface feature class from a blank schema into this dataset and run the tool again.")
		return 0
	write("- - - - - - - - - - - - - - - - - - - - - - ")
	write(" ~ {0} ~ ".format(tool_name))
	write("Making {0}, {1}, and {2} feature layers".format(fc1, fc2, fc3))
	ap.MakeFeatureLayer_management(fc1, "up")
	ap.MakeFeatureLayer_management(fc2, "uc")
	ap.MakeFeatureLayer_management(fc3, "us")
	ap.SelectLayerByAttribute_management("up", "NEW_SELECTION", "zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("uc", "NEW_SELECTION", "zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("us", "NEW_SELECTION", "zi026_ctuu >= 50000")
	ap.MakeFeatureLayer_management("up", "up_scale")
	ap.MakeFeatureLayer_management("uc", "uc_scale")
	ap.MakeFeatureLayer_management("us", "us_scale")
	write("Repairing {0} lines and {1} polygons before Integration".format(fc2, fc3))
	ap.RepairGeometry_management("uc_scale", "DELETE_NULL")
	ap.RepairGeometry_management("us_scale", "DELETE_NULL")
	ufeat_count = 0
	if not large:
		try:
			feat_count1 = int(ap.GetCount_management("up_scale").getOutput(0))
			feat_count2 = int(ap.GetCount_management("uc_scale").getOutput(0))
			feat_count3 = int(ap.GetCount_management("us_scale").getOutput(0))
			write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features...".format(feat_count1, fc1, feat_count2, fc2, feat_count3, fc3))
			ap.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.06 Meters")
			ap.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.03 Meters")
			ufeat_count = feat_count1 + feat_count2 + feat_count3
		except ap.ExecuteError:
			writeresults(tool_name)
	if large:
		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(fc2)
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			ap.MinimumBoundingGeometry_management(fc2, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with ap.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc2, "POLYGON")
			#ap.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			ap.MakeFeatureLayer_management(mem_fc, "ugrid")
			with ap.da.SearchCursor("ugrid", ['OID@']) as scursor:
				##### Add check for any 0 count features selected in each loop that might default to all features instead of 0 in current partition
				for row in scursor:
					select = "OID = {}".format(row[0])
					ap.SelectLayerByAttribute_management("ugrid", "NEW_SELECTION", select)
					ap.SelectLayerByLocation_management("up_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management("uc_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management("us_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
					feat_count1 = int(ap.GetCount_management("up_scale").getOutput(0))
					feat_count2 = int(ap.GetCount_management("uc_scale").getOutput(0))
					feat_count3 = int(ap.GetCount_management("us_scale").getOutput(0))
					ufeat_count = ufeat_count + feat_count1 + feat_count2 + feat_count3
					write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(feat_count1, fc1, feat_count2, fc2, feat_count3, fc3, row[0]))
					ap.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.06 Meters")
					ap.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.03 Meters")
			write("Freeing partition memory")
			ap.Delete_management("in_memory")
			ap.Delete_management("ugrid")
		except ap.ExecuteError:
			writeresults(tool_name)
	write("Repairing {0} lines and {1} polygons after Integration".format(fc2, fc3))
	ap.RepairGeometry_management("uc_scale", "DELETE_NULL")
	ap.RepairGeometry_management("us_scale", "DELETE_NULL")
	write("Clearing process cache")
	ap.Delete_management("up")
	ap.Delete_management("uc")
	ap.Delete_management("us")
	ap.Delete_management("up_scale")
	ap.Delete_management("uc_scale")
	ap.Delete_management("us_scale")
	write("- - - - - - - - - - - - - - - - - - - - - -")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Geometry Correction Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Delete Identical Features '''''''''
# Checks for features with identical geometry and PSG attribution and removes them
#### Test rewritten find identical code and replace existing
def process_dups():
	tool_name = 'Delete Identical Features'
	write("\n--- {0} ---\n".format(tool_name))
	# Set the output directory for the FindIdentical tool
	out_table = os.path.dirname(ap.env.workspace)
	# Precreate the path for the output dBASE table
	path = out_table.split(".")
	path.pop()
	table_loc = path[0] + str(".dbf")
	write("Creating temporary output file: {0}".format(table_loc))
	dup_count = 0

# ##### check Shape vs shape@ and add xy-tolerance to find and delete identical
# #search cursor with shape@ and oid@ check each shape against the others. if they match, store the oid in list.
# #new cursor. check matching shapes. if the other fields match, delete the one with the higher oid value
#   for fc in featureclass:
#       try:
#           prev_check = []
#           dup_oids = []
#           lap_fields = ['SHAPE@XY', 'OID@']
#
#           with ap.da.SearchCursor(fc, lap_fields) as scursor:
#               with ap.da.SearchCursor(fc, lap_fields) as tcursor:
#                   for row in scursor:
#                       icursor.insertRow(row)
#           atuple = ptGeometry.angleAndDistanceTo(ptGeometry2, "GEODESIC")
#           atuple == (angle in degrees, distance in meters)

	# Loop feature classes and FindIdentical to get a count, then delete any found
	# ARA and other metric fields included
	for fc in featureclass:
		try:
			dick = fc_fields_og[fc]
			ap.FindIdentical_management(fc, out_table, dick, "", "", output_record_option="ONLY_DUPLICATES")
			rows = int(ap.management.GetCount(table_loc).getOutput(0))
			write("Found " + str(rows) + " duplicate " + str(fc) + " features.")
			if rows > 0:
				ap.DeleteIdentical_management(fc, fc_fields_og[fc])
				write("Deleted " + str(rows) + " duplicate " + str(fc) + " features.")
				dup_count += rows
		except ap.ExecuteError:
			os.remove(table_loc)
			os.remove(table_loc + str(".xml"))
			os.remove(path[0] + str(".cpg"))
			os.remove(path[0] + str(".IN_FID.atx"))
			ap.RefreshCatalog(out_table)
			writeresults(tool_name)

	# Clean up before next process
	os.remove(table_loc)
	os.remove(table_loc + str(".xml"))
	os.remove(path[0] + str(".cpg"))
	os.remove(path[0] + str(".IN_FID.atx"))
	ap.RefreshCatalog(out_table)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEFENSE MAPPING
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''''''''' Hypernova Burst Multipart Features '''''''''
# Explodes multipart features for an entire dataset
def process_explode():
	tool_name = 'Hypernova Burst Multipart Features'
	write("\n--- {0} ---\n".format(tool_name))
	##### Multipart Search #####
	fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
	fc_multi_list = []
	total_multi = 0
	total_complex = 0
	for fc in featureclass:
		try:
			write("Searching for multiparts in {0}".format(fc))
			multipart = False # Assume the feature class doesn't have multiparts
			with ap.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as scursor:
				complex = 0 # Counts complex single part features
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
				if complex > 0:
					total_complex += complex
					write("{0} complex polygons found in {1}".format(complex, fc))
				if multipart is True:
					count = len(fc_multi[fc])
					write("*** " + str(count) + " true multipart features found in " + str(fc) + " ***")
				else:
					write("No multiparts found")

		except ap.ExecuteError:
			writeresults(tool_name)
		if multipart is True:
			fc_multi_list.append(fc) # Creates iterable list of feature classes that have multipart features

	write(" ")
	if total_complex > 0:
		write("The {0} complex polygons found are single part polygons with complex interior holes that are more likely to become multipart features.".format(total_complex))
	write(" ")
	if fc_multi_list: # Only runs if fc_multi_list is not empty
		for fc in fc_multi_list:
			count = len(fc_multi[fc])
			total_multi += count
			write("{0} multipart features found in {1}".format(count, fc))
			write("  OIDs - {0}".format(fc_multi[fc]))
		write(" ")

	##### Isolate, Explode, Replace #####
	in_class = "multi"
	out_class = "single"
	for fc in fc_multi_list:
		try:
			#sanitize feature class name from sde cz the sde always has to make things more difficult than they need to be...
			fc_parts = fc.split(".")
			if fc_parts[-1] in fc_fields:
				fcr = fc_parts[-1]
			else:
				write("Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin.")

			# Variables
			oid_list = fc_multi[fc]
			og_oid = "oidid"
			fc_geom = ap.Describe(fc).shapeType
			oid_field = ap.Describe(fc).OIDFieldName # Get the OID field name. Not necessary for every loop, but simple enough to just put here.
			# Adds a field to the current fc that stores the original OID for identification after exploding.
			ap.AddField_management(fc, og_oid, "double")
			with ap.da.UpdateCursor(fc, [oid_field, og_oid]) as ucursor:
				for row in ucursor:
					if row[0] in oid_list:
						row[1] = row[0]
						ucursor.updateRow(row)
			#ap.CalculateField_management(fc, og_oid, "!" + oid_field + "!", "PYTHON")
			fieldnames = fc_fields[fcr]
			fieldnames.insert(0, og_oid)
			fieldnames.insert(0, oid_field)
			oid_list_str = str(fc_multi[fc]) # Convert the list to a string and remove the []
			oid_list_str = oid_list_str[1:-1]
			query = "{0} in ({1})".format(oid_field, oid_list_str) # Formats the query from the above variables as: OBJECTID in (1, 2, 3)

			# Create a new feature class to put the multipart features in to decrease processing time. fields based on original fc template
			ap.CreateFeatureclass_management(ap.env.workspace, in_class, fc_geom, fc, "", "", ap.env.workspace)

			# Add multipart features to new feature class based on OID
			with ap.da.SearchCursor(fc, fieldnames, query) as scursor: # Search current fc using fc_fields with OID@ and "oidid" prepended as [0,1] respectively. Queries for only OIDs in the multipart oid_list.
				with ap.da.InsertCursor(in_class, fieldnames) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
					for row in scursor: # For each feature in the current fc
						if row[0] in oid_list: # If the OID is in the oid_list of multipart features. Redundant since the scursor is queried for multipart OIDs, but meh
							icursor.insertRow(row) # Insert that feature row into the temp feature class, in_class "multi"

			write("{0} multipart progenitor cores collapsing.".format(fcr))
			before_process = dt.now().time()
			ap.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
			after_process = dt.now().time()
			date = dt.now().date()
			datetime1 = dt.combine(date, after_process)
			datetime2 = dt.combine(date, before_process)
			time_delta = datetime1 - datetime2
			time_elapsed = str(time_delta.total_seconds())
			write("Hypernova burst detected after {0} seconds.".format(time_elapsed))

			write("Removing original multipart features.")
			# Deletes features in fc that have OIDs flagged as multiparts
			with ap.da.UpdateCursor(fc, oid_field) as ucursor:
				for row in ucursor:
					if row[0] in oid_list:
						ucursor.deleteRow()

			write("Replacing with singlepart features.")
			# Create search and insert cursor to insert new rows in fc from MultipartToSinglepart output out_class
			with ap.da.SearchCursor(out_class, fieldnames) as scursor:
				with ap.da.InsertCursor(fc, fieldnames) as icursor:
					for row in scursor:
						icursor.insertRow(row)

			write("Populating NULL fields with defaults and updating UFIs for the new single part features.")
			query2 = "{0} IS NOT NULL".format(og_oid)
			ap.MakeFeatureLayer_management(fc, "curr_fc", query2)
			ap.CalculateDefaultValues_defense("curr_fc")
			write("NULL fields populated with default values")
			with ap.da.UpdateCursor(fc, 'ufi', query2) as ucursor:
				for row in ucursor:
					row[0] = str(uuid.uuid4())
					ucursor.updateRow(row)
			ap.DeleteField_management(fc, og_oid)
			write("UFI values updated")
			write(" ")

		except ap.ExecuteError:
			writeresults(tool_name)

	if fc_multi_list:
		write("All multipart feature have acheived supernova!")

	try:
		ap.Delete_management(str(ap.env.workspace) + str("\\" + str(in_class)))
		ap.Delete_management(str(ap.env.workspace) + str("\\" + str(out_class)))
		ap.Delete_management("curr_fc")
	except:
		write("No in_class or out_class created. Or processing layers have already been cleaned up. Continuing...")
		pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Preprocessing Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Default Bridge WID Updater '''''''''
# Checks for bridges with default WID (-999999) and updates them to match the underlying road or rail WID
while bridge:
	bridge_err = False
	no_def_bridge = False
	bridge_count = 0
	total_rem_b = 0
	tool_name = 'Default Bridge WID Updater'
	write("\n--- {0} ---\n".format(tool_name))
	if not ap.Exists('TransportationGroundCrv'):
		write("TransportationGroundCrv feature class missing./nCannot run Default Bridge WID Updater.")
		bridge_err = True
		break
	break

while bridge: # Needs updating from management geoprocessing to cursors
	if bridge_err:
		break
	# Pull width and geometry fields for bridges
	fieldsB = ['WID', 'SHAPE@']
	# Pull width and geometry fields for roads
	fieldsR = ['ZI016_WD1', 'SHAPE@']
	# Pull width and geometry fields for rails and sidetracks
	fieldsRR = ['ZI017_GAW', 'SHAPE@']

	# Convert the feature classes from the TDS into usable layers
	write("Making feature layers...")
	ap.MakeFeatureLayer_management("TransportationGroundCrv", "bridge_crv_lyr")
	ap.MakeFeatureLayer_management("TransportationGroundCrv", "road_crv_lyr")
	ap.MakeFeatureLayer_management("TransportationGroundCrv", "rail_crv_lyr")
	write("Successfully made the feature layers!")

	# Select road bridges with default (-999999) width
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130')")
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 13")
	# Make road bridges with default (-999999) width into layer
	ap.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeR")

	# Select rail bridges with default (-999999) width
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130')")
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 12")
	# Make rail bridges with default (-999999) width into layer
	ap.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeRR")

	# Select roads that share curve with the default width bridges above
	ap.SelectLayerByAttribute_management("road_crv_lyr", "NEW_SELECTION", "F_CODE = 'AP030'")
	ap.SelectLayerByLocation_management("road_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "fc_bridgeR", "", "SUBSET_SELECTION")
	# Make roads that share curve with default width bridges into layer
	ap.MakeFeatureLayer_management("road_crv_lyr", "fc_road")

	# Select rails that share curve with the default width bridges above
	ap.SelectLayerByAttribute_management("rail_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AN010', 'AN050')")
	ap.SelectLayerByLocation_management("rail_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "fc_bridgeRR", "", "SUBSET_SELECTION")
	# Make rails that share curve with default width bridges into layer
	ap.MakeFeatureLayer_management("rail_crv_lyr", "fc_rail")

	# Gets a count of selected bridges, roads, and rails
	fc_bridgeR_total = int(ap.management.GetCount("fc_bridgeR").getOutput(0))
	fc_bridgeRR_total = int(ap.management.GetCount("fc_bridgeRR").getOutput(0))
	total_bridges = fc_bridgeR_total + fc_bridgeRR_total
	total_roads = int(ap.management.GetCount("fc_road").getOutput(0))
	total_rails = int(ap.management.GetCount("fc_rail").getOutput(0))

	# Error handling. If 0 bridges selected the script hangs.
	if total_bridges == 0:
		write("No default bridges found.")
		no_def_bridge = True
		break
	# Error handling. If no roads or rails to select against, likely something will break.
	if total_roads == 0 and total_rails == 0:
		write("{0} default WID bridges found.".format(total_bridges))
		write("No underlying roads or rails for default bridges. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.")
		bridge_err = True
		break

	# Announces the total default bridges found.
	write("{0} default WID bridges found.".format(total_bridges))

	# Start an edit session. Must provide the workspace.
	edit = ap.da.Editor(workspace)
	# Edit session is started without an undo/redo stack for versioned data
	edit.startEditing(False, True) # For second argument, use False for unversioned data

	countR = 0
	if fc_bridgeR_total > 0:
		edit.startOperation() # Start an edit operation for road bridges
		# Loop to update bridge width to it's corresponding road width
		with ap.da.UpdateCursor("fc_bridgeR", fieldsB) as bridgeR: # UpdateCursor for bridges with width and geometry
			for i in bridgeR:
				with ap.da.SearchCursor("fc_road", fieldsR) as road: # SearchCursor for roads with width and geometry
					for j in road:
						if i[1].within(j[1]): # Check if bridge shares curve with road(if not working test contains\within)
							if i[0] < j[0]:
								i[0] = int(j[0]*1.5) # Sets current bridge width to road width * [factor]
				bridgeR.updateRow(i)
				countR += 1
		edit.stopOperation() # Stop the edit operation
	write("{0} bridges on roads updated.".format(countR))

	countRR = 0
	if fc_bridgeRR_total > 0:
		edit.startOperation() # Start an edit operation for rail bridges
		# Loop to update bridge width to it's corresponding rail width
		with ap.da.UpdateCursor("fc_bridgeRR", fieldsB) as bridgeRR: # UpdateCursor for bridges with width and geometry
			for i in bridgeRR:
				with ap.da.SearchCursor("fc_rail", fieldsRR) as rail: # SearchCursor for rails with width and geometry
					for j in rail:
						if i[1].within(j[1]): # Check if bridge shares curve with rail(if not working test contains\within)
							if i[0] < j[0]:
								i[0] = int(j[0])+1 # Sets current bridge width to integer rounded rail gauge width + [value]
				bridgeRR.updateRow(i)
				countRR += 1
		edit.stopOperation() # Stop the edit operation
	write("{0} bridges on railroads updated.".format(countRR))

	# Stop the edit session and save the changes
	try:
		edit.stopEditing(True)
	except:
		write("First attempt to save failed. Checking for updated SDE version. Trying again in 5 seconds. Please hold...")
		time.sleep(5)
		edit.stopEditing(True)

	# Select any remaining bridges with default (-999999) width
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE = 'AQ040'")
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999")
	# Make these selections into a new layer and get a count
	ap.MakeFeatureLayer_management("bridge_crv_lyr", "bridges_rem")
	total_rem_b = int(ap.management.GetCount("bridges_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	bridge_count = (countR + countRR) - total_rem_b
	write("Updated {0} bridges with new WID values.".format(bridge_count))
	if total_rem_b > 0:
		write("{0} bridges still have default WID. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.".format(total_rem_b))
	break


''''''''' Default Pylon HGT Updater '''''''''
# Checks for pylons with default HGT (-999999) and updates them to match the intersecting cable HGT
def update_pylong():
	pylong_err = False
	no_def_pylon = False
	lecount = 0
	total_rem_p = 0
	tool_name = 'Default Pylon HGT Updater'
	write("\n--- {0} ---\n".format(tool_name))
	if not ap.Exists('UtilityInfrastructurePnt') or not ap.Exists('UtilityInfrastructureCrv'):
		write("UtilityInfrastructurePnt or UtilityInfrastructureCrv feature classes missing./nCannot run Default Pylon HGT Updater.")
		pylong_err = True
		return 0


 # Needs updating from management geoprocessing to cursors
	if pylong_err:
		return 0
	# Pull height and geometry fields
	fields = ['HGT', 'SHAPE@']

	# Convert the feature classes from the TDS into usable layers
	write("Making feature layers...")
	ap.MakeFeatureLayer_management("UtilityInfrastructurePnt", "utility_pnt_lyr")
	ap.MakeFeatureLayer_management("UtilityInfrastructureCrv", "utility_crv_lyr")
	write("Successfully made the feature layers!")

	# Select pylons with default (-999999) height
	ap.SelectLayerByAttribute_management("utility_pnt_lyr", "NEW_SELECTION", "F_CODE = 'AT042'")
	ap.SelectLayerByAttribute_management("utility_pnt_lyr", "SUBSET_SELECTION", "HGT = -999999")
	ap.MakeFeatureLayer_management("utility_pnt_lyr", "fc_pylon_total")
	# Select cables that intersect the default height pylons above and removes any with default height
	ap.SelectLayerByAttribute_management("utility_crv_lyr", "NEW_SELECTION", "F_CODE = 'AT005'")
	ap.SelectLayerByLocation_management("utility_crv_lyr", "INTERSECT", "utility_pnt_lyr", "", "SUBSET_SELECTION")
	ap.MakeFeatureLayer_management("utility_pnt_lyr", "fc_cable_total")
	ap.SelectLayerByAttribute_management("utility_crv_lyr", "REMOVE_FROM_SELECTION", "HGT = -999999")
	# Select only the default pylons that intersect cables to speed up run time
	ap.SelectLayerByLocation_management("utility_pnt_lyr", "INTERSECT", "utility_crv_lyr", "", "SUBSET_SELECTION")
	# Make these selections into layers
	ap.MakeFeatureLayer_management("utility_pnt_lyr", "fc_pylon")
	ap.MakeFeatureLayer_management("utility_crv_lyr", "fc_cable")

	# Gets a count of selected pylons and cables
	total_pylons = int(ap.management.GetCount("fc_pylon_total").getOutput(0))
	total_cables = int(ap.management.GetCount("fc_cable_total").getOutput(0))
	usable_pylons = int(ap.management.GetCount("fc_pylon").getOutput(0))
	usable_cables = int(ap.management.GetCount("fc_cable").getOutput(0))

	# Error handling. If 0 pylons selected the script hangs.
	if total_pylons == 0:
		write("No default pylons found.")
		no_def_pylon = True
		return 0
	# Error handling. If no cables to select against, likely something will break.
	if total_cables == 0:
		write("{0} default value pylons found.".format(total_pylons))
		write("No intersecting cables for default pylons. \n Try running Integrate and Repair then try again. \n The default pylons are either not snapped or missing a cable.")
		pylong_err = True
		return 0

	# Announces the total default pylons found.
	no_hgt_cable = total_cables - usable_cables
	y = total_pylons - usable_pylons
	y = str(y)
	write("{0} default value pylons found.".format(total_pylons))
	write("{0} of the intersecting cables don't have a height. These will be ignored.".format(no_hgt_cable))
	write("{0} pylons are intersecting a cable with a height value and will be updated.".format(usable_pylons))

	# Loop to update pylon height to it's corresponding cable height
	with ap.da.UpdateCursor("fc_pylon", fields) as pylon: # UpdateCursor for pylons with height and geometry
		for i in pylon:
			with ap.da.SearchCursor("fc_cable", fields) as cable: # SearchCursor for cables with height and geometry
				for j in cable:
					if not i[1].disjoint(j[1]): # Check if pylon intersects a cable
						if i[0] < j[0]:
							i[0] = j[0] # Sets current pylon HGT to intersecting cable's HGT
			pylon.updateRow(i)
			lecount += 1

	# Select any remaining pylons with default (-999999) height
	ap.SelectLayerByAttribute_management("fc_pylon", "NEW_SELECTION", "F_CODE = 'AT042'")
	ap.SelectLayerByAttribute_management("fc_pylon", "SUBSET_SELECTION", "HGT = -999999")
	# Make these selections into a new layer and get a count
	ap.MakeFeatureLayer_management("fc_pylon", "pylons_rem")
	total_rem_p = int(ap.management.GetCount("pylons_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	lecount = lecount - total_rem_p
	write("Updated {0} pylons with new HGT values.".format(lecount))
	write("{0} pylons still have default HGT. \n Consider running Integrate and Repair before trying again. \n The remaining pylons are not snapped, missing a cable, or the underlying cable doesn't have a height.".format(total_rem_p))



''''''''' Building in BUA Descaler '''''''''
# Descales buildings within BUAs that don't have important FFNs
def descale_building():
	building_err = False
	no_bua = False
	no_bua_buildings = False
	total_non_imp = 0
	tool_name = 'Building in BUA Descaler'
	write("\n--- {0} ---\n".format(tool_name))
	if not ap.Exists('SettlementSrf'):
		write("SettlementSrf feature class missing./nCannot run Building in BUA Descaler.")
		building_err = True
		return 0
	if not ap.Exists('StructureSrf') and not ap.Exists('StructurePnt'):
		write("StructureSrf and StructurePnt feature classes missing./nCannot run Building in BUA Descaler.")
		building_err = True
		return 0


	# Needs updating from management geoprocessing to cursors
	if building_err:
		return 0
	# Make initial layers from the workspace
	srf_exist = False
	pnt_exist = False
	import_ffn_s = 0
	import_ffn_p = 0
	non_import_count_s = 0
	non_import_count_p = 0
	fields = 'ZI026_CTUU'
	caci_query = "FFN IN ({0})".format(", ".join(str(i) for i in ffn_list_caci.values()))
	other_query = "FFN IN ({0})".format(", ".join(str(i) for i in ffn_list_all.values()))

	if caci_schema:
		write("CACI specific important building FFNs list:")
		write("\n".join("{}: {}".format(k, v) for k, v in ffn_list_caci.items()))
	else:
		write("Current project important building FFNs list:")
		write("\n".join("{}: {}".format(k, v) for k, v in ffn_list_all.items()))

	# Make layer of BUAs
	write("\nRetrieved feature classes containing BUAs and Buildings")
	write("Selecting BUAs")
	ap.MakeFeatureLayer_management("SettlementSrf", "settlement_srf")
	ap.SelectLayerByAttribute_management("settlement_srf", "NEW_SELECTION", "F_CODE = 'AL020'")
	ap.MakeFeatureLayer_management("settlement_srf", "buas")
	write("Searching within BUAs")

	if ap.Exists('StructureSrf'):
		# Make layer of building surfaces
		ap.MakeFeatureLayer_management("StructureSrf", "structure_srf")
		ap.SelectLayerByAttribute_management("structure_srf", "NEW_SELECTION", "F_CODE = 'AL013'")
		ap.MakeFeatureLayer_management("structure_srf", "building_srf")
		# Layer of building surfaces within BUAs
		ap.SelectLayerByLocation_management ("building_srf", "WITHIN", "buas", "", "NEW_SELECTION")
		ap.MakeFeatureLayer_management("building_srf", "bua_building_s")
		# Select important building surfaces and switch selection
		# Adam's original list: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building surfaces matching criteria...")
		if caci_schema:
			ap.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", caci_query)
		else:
			ap.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", other_query)
		import_ffn_s = int(ap.GetCount_management("bua_building_s").getOutput(0))
		ap.SelectLayerByAttribute_management("bua_building_s", "SWITCH_SELECTION")
		ap.MakeFeatureLayer_management("bua_building_s", "non_import_s")
		non_import_count_s = int(ap.GetCount_management("non_import_s").getOutput(0))

	if ap.Exists('StructurePnt'):
		# Make layer of building points
		ap.MakeFeatureLayer_management("StructurePnt", "structure_pnt")
		ap.SelectLayerByAttribute_management("structure_pnt", "NEW_SELECTION", "F_CODE = 'AL013'")
		ap.MakeFeatureLayer_management("structure_pnt", "building_pnt")
		# Layer of building points within BUAs
		ap.SelectLayerByLocation_management ("building_pnt", "WITHIN", "buas", "", "NEW_SELECTION")
		ap.MakeFeatureLayer_management("building_pnt", "bua_building_p")
		# Select important building points and switch selection
		# Adam's original list: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building points matching criteria...")
		if caci_schema:
			ap.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", caci_query)
		else:
			ap.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", other_query)
		import_ffn_p = int(ap.GetCount_management("bua_building_p").getOutput(0))
		ap.SelectLayerByAttribute_management("bua_building_p", "SWITCH_SELECTION")
		ap.MakeFeatureLayer_management("bua_building_p", "non_import_p")
		non_import_count_p = int(ap.GetCount_management("non_import_p").getOutput(0))

	# Count buildings and buas in selections
	bua_count = int(ap.GetCount_management("buas").getOutput(0))
	total_import = import_ffn_s + import_ffn_p
	total_non_imp = non_import_count_s + non_import_count_p

	# End script if there are no BUAs or no buildings inside them
	if bua_count == 0:
		write("\nNo BUAs found.")
		no_bua = True
		return 0
	if total_non_imp == 0:
		write("\nNo buildings without important FFNs found in BUAs.")
		no_bua_buildings = True
		return 0

	write("\n{0} buildings with important FFNs found in {1} total BUAs.".format(total_import, bua_count))

	# Descale selected, non-important buildings within BUAs to CTUU 12500
	write("Descaling unimportant building surfaces...")
	with ap.da.UpdateCursor("non_import_s", fields) as cursor_s:
		for row in cursor_s:
			row[0] = 12500
			cursor_s.updateRow(row)

	write("Descaling unimportant building points...")
	with ap.da.UpdateCursor("non_import_p", fields) as cursor_p:
		for row in cursor_p:
			row[0] = 12500
			cursor_p.updateRow(row)

	write("\n{0} building surfaces descaled to CTUU 12500.".format(non_import_count_s))
	write("{0} building points descaled to CTUU 12500.".format(non_import_count_p))



''''''''' CACI Swap Scale and CTUU '''''''''
# Swaps the Scale field with the CTUU field so we can work normally with CACI data
def swap_ctuu():
	tool_name = 'CACI Swap Scale and CTUU'
	write("\n--- {0} ---\n".format(tool_name))
	if not caci_schema:
		write("Provided TDS does not match CACI schema containing the 'Scale' field.\nCannot run CACI Swap Scale and CTUU")
		return 0
	if caci_schema:
		write("CACI schema containing 'Scale' field identified")
	featureclass = ap.ListFeatureClasses()
	if ap.Exists('MetadataSrf'):
		featureclass.remove('MetadataSrf')
		write("MetadataSrf removed")
	else:
		write("MetadataSrf not present")
	if ap.Exists('ResourceSrf'):
		featureclass.remove('ResourceSrf')
		write("ResourceSrf removed")
	else:
		write("ResourceSrf not present")
	featureclass.sort()


	if not caci_schema:
		return 0
	write("Swapping CTUU and Scale for {0}".format(gdb_name))
	write("\nNote: The SAX_RX9 field will be changed from <NULL> to 'Scale Swapped' after the first swap. It will flip back and forth in subsequent runs.\nIf the tool was aborted on a previous run for some reason, it will reset all feature classes to the dominant swap format to maintain internal consistency. It is still up to the user to know which format they were swapping from. (Either Scale->CTUU or CTUU->Scale) Check the tool output for more information on which feature classes were changed.\n")
	fields = ['zi026_ctuu', 'scale', 'swap', 'progress', 'sax_rx9']


	write("\nChecking if any previous swaps were canceled. Please wait...")
	swap_fc = []
	none_fc = []
	empty_fc = []
	clean_proceed = False
	swap_dom = False
	none_dom = False
	for fc in featureclass:
		fc_zero = int(ap.GetCount_management(fc).getOutput(0))
		if fc_zero == 0:
			empty_fc.append(str(fc))
			continue
		# field_check = ap.ListFields(fc)
		# partialchk = False
		# swapchk = False
		# for f in field_check:
		#   if f.name == "progress":
		#       partialchk = True
		#   if f.name == "swap":
		#       swapchk = True
		#       break
		# if swapchk:
		#   continue
		with ap.da.SearchCursor(fc, ['sax_rx9']) as scursor:
			for row in scursor:
				if not populated(row[0]):
					none_fc.append(str(fc))
					break
				if row[0] == 'Scale Swapped':
					swap_fc.append(str(fc))
					break
	if not swap_fc or not none_fc:
		clean_proceed = True
	elif len(swap_fc) > len(none_fc):
		swap_dom = True
	elif len(swap_fc) < len(none_fc):
		none_dom = True
	if not clean_proceed:
		write("\n***Previous run was flagged as aborted. Resetting all feature classes to previous format.***\n")
		if swap_dom:
			write("Majority of feature classes tagged as 'Scale Swapped'. Updating the following feature classes to match:")
			write("\n".join(i for i in none_fc) + "\n")
		if none_dom:
			write("Majority of feature classes /not/ tagged as 'Scale Swapped'. Updating the following feature classes to match:")
			write("\n".join(i for i in swap_fc) + "\n")
	if clean_proceed:
		write("Previous swaps finished properly. Continuing...\n")

	# Swippity Swappity Loop
	for fc in featureclass:
		if swap_dom and fc in swap_fc:
			continue
		if none_dom and fc in none_fc:
			continue
		if clean_proceed and fc in empty_fc:
			write("*Feature Class {0} is empty*".format(fc))
			continue
		elif fc in empty_fc:
			continue
		#write("swap_dom: {0}\nnone_dom: {1}".format(swap_dom, none_dom)) ###
		write("Swapping CTUU and Scale fields for {0} features".format(fc))
		field_check = ap.ListFields(fc)
		partialchk = False
		swapchk = False
		for f in field_check:
			if f.name == "progress":
				partialchk = True
			if f.name == "swap":
				swapchk = True
		if not partialchk:
			ap.AddField_management(fc, "progress", "TEXT", 9) # Creates temporary progress field
		if not swapchk:
			ap.AddField_management(fc, "swap", "LONG", 9) # Creates temporary swap field
		with ap.da.UpdateCursor(fc, fields) as ucursor: # Update cursor to juggle values
			for row in ucursor:
				if row[3] == 'y' or row[3] == 'x':
					continue
				# Functions as three ring puzzle
				row[2] = row[1] #swap = scale
				row[1] = row[0] #scale = ctuu
				row[0] = row[2] #ctuu = swap
				row[3] = 'y' #mark row as swapped in previous run that crashed or canceled
				if not populated(row[4]):
					row[4] = 'Scale Swapped'
				elif row[4] == 'Scale Swapped':
					row[4] = None
				swap_tag = row[4]
				ucursor.updateRow(row)
			write("    SAX_RX9 field value after swap: {0}".format(swap_tag))
			if partialchk and not clean_proceed:
				write("Resetting partial feature class to dominant format.")
				for row in ucursor:
					if swap_dom and not populated(row[4]):
						row[2] = row[1] #swap = scale
						row[1] = row[0] #scale = ctuu
						row[0] = row[2] #ctuu = swap
						row[3] = 'x' #mark row as swapped in previous run that crashed or canceled
						row[4] = 'Scale Swapped'
					if none_dom and row[4] == 'Scale Swapped':
						row[2] = row[1] #swap = scale
						row[1] = row[0] #scale = ctuu
						row[0] = row[2] #ctuu = swap
						row[3] = 'x' #mark row as swapped in previous run that crashed or canceled
						row[4] = None

		# Deletes temporary swap field
		ap.DeleteField_management(fc, "swap")
		ap.DeleteField_management(fc, "progress")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Database Management Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Database Feature Report '''''''''
# Refactored from John Jackson's Feature_Itemized_Counter.py by Nat Cagle
def report_fcount():
	tool_name = 'Database Feature Report'
	write("\n--- {0} ---\n".format(tool_name))
	# Define counters for shape feature counts and total feature count
	pnt_cnt = 0
	crv_cnt = 0
	srf_cnt = 0
	tots_f = 0
	hydro_cnt = 0
	trans_cnt = 0
	building_cnt = 0
	landcover_cnt = 0


	gdb_name_full = TDS.split('\\')[-2]
	# Define fields for Search Cursor
	fields = ["FCSubtype"]
	if not 'StructurePnt' in featureclass:
		featureclass.append('StructurePnt')
	if not 'StructureSrf' in featureclass:
		featureclass.append('StructureSrf')
	# Set up dictionary and exclusion list to track feature classes
	feat_dict = OrderedDict()
	exList = []
	# Retrieve date and time for output file label and report timestamp
	today = dt.now().date() #datetime.date.today()
	time_stamp = dt.now().strftime("%Y_%m_%d_%H%M")
	current_time = dt.now().strftime("%H:%M:%S")
	# Define feature categories
	hydro_cat = 'Hydrography'
	trans_cat = 'Transportation'
	building_sub = 100083
	landcover_list = [ 100295, #'Aqueduct'
						100296, #'Bog'
						100089, #'BuiltUpArea'
						100297, #'Canal'
						100393, #'Cane'
						100329, #'Cistern'
						100396, #'ClearedWay'
						100380, #'CropLand'
						100403, #'Desert'
						100298, #'Ditch'
						100001, #'ExtractionMine'
						130380, #'Forest'
						100341, #'Glacier'
						100387, #'Grassland'
						100386, #'HopField'
						130384, #'InlandWaterbody'
						100399, #'Marsh'
						100340, #'Moraine'
						100320, #'NaturalPool'
						100384, #'Orchard'
						100313, #'RiceField'
						100314, #'River'
						100318, #'Sabkha'
						100316, #'SaltFlat'
						100374, #'SandDunes'
						100349, #'SnowIceField'
						100358, #'SoilSurfaceRegion'
						100400, #'Swamp'
						100388, #'Thicket'
						100218, #'TidalWater'
						100350, #'Tundra'
						100385, #'Vineyard'
						100473, #'VoidCollectionArea'
	]

	# Create report output file path
	results = "{0}\\{1}_Feature_Report_{2}.txt".format(rresults, gdb_name, time_stamp)
	write("Checking feature classes...\n")

	# Fill in dictionary with itemized feature subtype counts
	for i in featureclass:
		currFC = str(i)
		currShape = currFC[-3:]
		feat_dict[currFC]=[{},0]
		hydro_feat = False
		trans_feat = False
		if hydro_cat in currFC:
			hydro_feat = True
		elif trans_cat in currFC:
			trans_feat = True
		with arcpy.da.SearchCursor(i,fields) as vCursor:
			try:
				# Iterate through features in Feature Class
				for j in vCursor:
					curr_sub = int(j[0])
					# Counting Feature Subtypes
					if fcsub_dict[int(j[0])] not in feat_dict[currFC][0]:
						feat_dict[str(i)][0][fcsub_dict[int(j[0])]] = 1
					else:
						feat_dict[currFC][0][fcsub_dict[int(j[0])]] += 1
					# Count Feature Class total features
					feat_dict[currFC][1] += 1
					# Count Database total features
					tots_f += 1
					# Counting based on shape type
					if currShape == 'Srf':
						srf_cnt += 1
						if any(int(substring) == int(curr_sub) for substring in landcover_list):
							landcover_cnt += 1
					elif currShape == 'Crv':
						crv_cnt += 1
					else:
						pnt_cnt += 1
					# Counting specific categories
					if int(curr_sub) == int(building_sub):
						building_cnt += 1
					if hydro_feat:
						hydro_cnt += 1
					if trans_feat:
						trans_cnt += 1

			except:
				# If FC does not have FCSubtype field put it on exclusion list
				write("**** {0} does not have required fields ****".format(currFC))
				exList.append(currFC)
				continue
		write("{0} features counted".format(currFC))

	# Setup and write results to text file
	write("\nWriting report to TXT file...\n")
	with open(results,'w') as txt_file:
		line = []
		txt_file.write("Feature Count Report for TPC: {0}\n".format(gdb_name_full))
		txt_file.write("Report created: {0} at time: {1}\n\n\n".format(today, current_time))
		txt_file.writelines(["Point Features  :  ",str(pnt_cnt),"\n",
							"Curve Features  :  ",str(crv_cnt),"\n",
							"Surface Features:  ",str(srf_cnt),"\n",
							"Total Features  :  ",str(tots_f),"\n\n",
							"Total Hydrography Features        :  ",str(hydro_cnt),"\n",
							"Total Transportation Features     :  ",str(trans_cnt),"\n",
							"Total Building Surfaces and Points:  ",str(building_cnt),"\n",
							"Total Landcover Surfaces          :  ",str(landcover_cnt),"\n\n\n"])
		header = ['Feature Class'.ljust(25), 'Subtype'.center(25), 'Feature Count\n'.rjust(8),'\n\n']
		txt_file.writelines(header)
		for fKey in feat_dict:
			# Check exclusion list
			if fKey in exList:
				txt_file.writelines([fKey.ljust(25),
									'******** Feature Class does not contain subtypes ********','\n\n'])
				continue
			# Print Subtype list with individual counts
			if feat_dict[fKey][1] != 0:
				# Print Feature Class with count
				txt_file.writelines([fKey.ljust(25),'--------- Total Features: ',
									str(feat_dict[fKey][1]),' ---------','\n\n'])
				for sKey in feat_dict[fKey][0]:
					line = [''.ljust(25),sKey.center(25),str(feat_dict[fKey][0][sKey]).rjust(8)+'\n']
					txt_file.writelines(line)
				txt_file.write('\n\n')
		txt_file.write("\nEmpty Feature Classes:\n\n")
		for fKey in feat_dict:
			# Check exclusion list
			if fKey in exList:
				continue
			if feat_dict[fKey][1] == 0:
				txt_file.write("{0}\n".format(fKey))

	write("Feature Count Report created. File located in database folder:\n{0}".format(results))



''''''''' Source Analysis Report '''''''''
# Refactored from John Jackson's Version_Source_Counter.py by Nat Cagle
def report_vsource():
	tool_name = 'Source Analysis Report'
	write("\n--- {0} ---\n".format(tool_name))



	time_stamp = dt.now().strftime("%Y_%m_%d_%H%M")
	gdb_name_full = TDS.split('\\')[-2]
	fields = ["Version","ZI001_SDP","ZI001_SDV","ZI001_SRT"]
	results_csv = "{0}\\{1}_Source_Count_{2}.csv".format(rresults, gdb_name, time_stamp)
	results_txt = "{0}\\{1}_Source_Count_{2}.txt".format(rresults, gdb_name, time_stamp)
	feat_dict = OrderedDict()
	write("Checking feature classes...\n")

	# Fill in dictionary with leveled counts: Version -> SDP -> SDV *optional SRT
	for i in featureclass:
		feat_dict[str(i)]=OrderedDict()
		with arcpy.da.SearchCursor(i,fields) as vCursor:
			try:
				for j in vCursor:
					if str(j[0]) not in feat_dict[str(i)]:
						feat_dict[str(i)][str(j[0])]={str(j[1]):{str(j[2]):1}}

					elif str(j[1]) not in feat_dict[str(i)][str(j[0])]:
						feat_dict[str(i)][str(j[0])][str(j[1])] = {str(j[2]):1}
					elif str(j[2]).strip() not in feat_dict[str(i)][str(j[0])][str(j[1])]:
						feat_dict[str(i)][str(j[0])][str(j[1])][str(j[2]).strip()] = 1
					else:
						feat_dict[str(i)][str(j[0])][str(j[1])][str(j[2]).strip()] += 1
			except:
				write("**** {0} does not have required fields ****".format(i))
		write("{0} feature sources identified".format(i))

	# Set up and write dictionary out to CSV
	write("\nWriting report to CSV and TXT file...\n")
	with open(results_csv,'wb') as csvFile:
		writer = cs.writer(csvFile, delimiter=',')
		line = []
		header = ['Feature Class', 'Version', 'Description (SDP)', 'Source Date','Feature Count']
		writer.writerow(header)
		for fKey in feat_dict:
			if feat_dict[fKey]: # Only writes output if it exists
				writer.writerow([fKey,None,None,None,None])
				for vKey in feat_dict[fKey]:
					for sKey in feat_dict[fKey][vKey]:
						for dKey in feat_dict[fKey][vKey][sKey]:
							line = [None,vKey,sKey,dKey,feat_dict[fKey][vKey][sKey][dKey]]
							writer.writerow(line)

	# Set up and write dictionary out to TXT
	with open(results_txt,'w') as txt_file:
		line = []
		txt_file.write("Source Report for TPC: {0}\nScroll right for all information.\n**For an ordered view, see accompanying .csv file\n\n".format(gdb_name_full))
		header = ['Feature Class'.ljust(25), 'Version'.center(14), 'Description (SDP)'.ljust(65), 'Source Date'.center(16),'Feature Count\n\n'.rjust(8)]
		txt_file.writelines(header)
		for fKey in feat_dict:
			if feat_dict[fKey]:
				txt_file.write(fKey+'\n')
				for vKey in feat_dict[fKey]:
					for sKey in feat_dict[fKey][vKey]:
						for dKey in feat_dict[fKey][vKey][sKey]:
							line = [''.ljust(25),vKey.center(14),sKey.ljust(65),dKey.center(16),str(feat_dict[fKey][vKey][sKey][dKey]).rjust(8)+'\n']
							txt_file.writelines(line)

	write("Source Analysis Report created. File located in database folder:\n{0}".format(rresults))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Report Formatting and Wrap Up #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def grand_finale():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEFENSE MAPPING
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	if defaults or metrics or explode:
		if not no_defense:
			write("\n~~ Checking Defense Mapping Extension back in ~~\n")
			arcpy.CheckInExtension("defense")


	# Report of completed tasks
	def format_count(count):
		cnt_str = str(count)
		end_spacing = ""
		if len(cnt_str) > 0:
			for i in range(7-len(cnt_str)):
				end_spacing += " "
		else:
			pass
		return end_spacing

	write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}{4}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

	# Easter Egg
	if secret:
		write(u"    |        Our great and powerful leader       {0}|".format(exs))
		write(u"    |         The kind-hearted and caring        {0}|".format(exs))
		write(u"    |      _______        _                      {0}|".format(exs))
		write(u"    |     / ___/ /  ___ _(_)_____ _  ___ ____    {0}|".format(exs))
		write(u"    |    / /__/ _ \/ _ `/ / __/  ' \/ _ `/ _ \   {0}|".format(exs))
		write(u"    |    \___/_//_/\_,_/_/_/ /_/_/_/\_,_/_//_/   {0}|".format(exs))
		write(u"    |               ___           __             {0}|".format(exs))
		write(u"    |              / _ )___  ____/ /__           {0}|".format(exs))
		write(u"    |             / _  / _ \/ __/  '_/           {0}|".format(exs))
		write(u"    |            /____/\___/\__/_/\_\            {0}|".format(exs))
		write(u"    |   {0}   {1}|".format(sspaces, exs))
		write(u"    |             Thanks you for your            {0}|".format(exs))
		write(u"    |             outstanding service            {0}|".format(exs))
		write(u"    |   {0}   {1}|".format(sspaces, exs))
		write(u"    |   {0}   {1}|".format(sspaces, exs))

	write(u"    |   =======  Processes  Completed  =======   {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	if vogon:
		write(u"    |     - Buildings skipped                    {0}|".format(exs))
	if repair:
		write(u"    |     - Repaired NULL Geometries             {0}|".format(exs))
	if fcode:
		write(u"    |     - Populated F_Codes                    {0}|".format(exs))
	if defaults:
		write(u"    |     - Calculated Default Values            {0}|".format(exs))
	if metrics:
		write(u"    |     - Calculated Metrics                   {0}|".format(exs))
	if ufi:
		f_ufi_count = format_count(ufi_count)
		write(u"    |     - Updated UFI Values                   {0}|".format(exs))
		write(u"    |          {0} Duplicate or blank UFIs   {1}{2}|".format(ufi_count, f_ufi_count, exs))
	if hydro or trans or util:
		write(u"    |     - Integrated and Repaired:             {0}|".format(exs))
		if large:
			write(u"    |        ~ Large Dataset ~                   {0}|".format(exs))
		if hydro:
			f_hfeat_count = format_count(hfeat_count)
			write(u"    |          {0} Hydro                     {1}{2}|".format(hfeat_count, f_hfeat_count, exs))
		if trans:
			f_tfeat_count = format_count(tfeat_count)
			write(u"    |          {0} Trans                     {1}{2}|".format(tfeat_count, f_tfeat_count, exs))
		if util:
			f_ufeat_count = format_count(ufeat_count)
			write(u"    |          {0} Utilities                 {1}{2}|".format(ufeat_count, f_ufeat_count, exs))
	if dups:
		f_dup_count = format_count(dup_count)
		write(u"    |     - Deleted Identical Features           {0}|".format(exs))
		write(u"    |          {0} Duplicates found          {1}{2}|".format(dup_count, f_dup_count, exs))
	if explode:
		f_complex_count = format_count(total_complex)
		f_multi_count = format_count(total_multi)
		write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
		write(u"    |          {0} Complex features found    {1}{2}|".format(total_complex, f_complex_count, exs))
		write(u"    |          {0} Features exploded         {1}{2}|".format(total_multi, f_multi_count, exs))
	if bridge:
		f_bridge_count = format_count(bridge_count)
		f_total_rem_b = format_count(total_rem_b)
		write(u"    |     - Default Bridge WID Updater           {0}|".format(exs))
		if bridge_err:
			write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
			write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
		elif no_def_bridge:
			write(u"    |          No default bridges found          {0}|".format(exs))
		else:
			write(u"    |          {0} Bridges updated           {1}{2}|".format(bridge_count, f_bridge_count, exs))
			write(u"    |          {0} Defaults not updated      {1}{2}|".format(total_rem_b, f_total_rem_b, exs))
			write(u"    |          Check the output for more info    {0}|".format(exs))
	if pylong:
		f_lecount = format_count(lecount)
		f_total_rem_p = format_count(total_rem_p)
		write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
		if pylong_err:
			write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
			write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
		elif no_def_pylon:
			write(u"    |          No default pylons found           {0}|".format(exs))
		else:
			write(u"    |          {0} Pylons updated            {1}{2}|".format(lecount, f_lecount, exs))
			write(u"    |          {0} Defaults not updated      {1}{2}|".format(total_rem_p, f_total_rem_p, exs))
			write(u"    |          Check the output for more info    {0}|".format(exs))
	if building:
		f_total_non = format_count(total_non_imp)
		write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
		if building_err:
			write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
			write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
		elif no_bua:
			write(u"    |          No BUAs found                     {0}|".format(exs))
		elif no_bua_buildings:
			write(u"    |          No un-important buildings found   {0}|".format(exs))
		else:
			write(u"    |          {0} Buildings descaled        {1}{2}|".format(total_non_imp, f_total_non, exs))
			write(u"    |          Check the output for more info    {0}|".format(exs))
	if swap:
		write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
	if fcount:
		f_pnt_cnt = format_count(pnt_cnt)
		f_crv_cnt = format_count(crv_cnt)
		f_srf_cnt = format_count(srf_cnt)
		f_tots_f = format_count(tots_f)
		f_hydro_cnt = format_count(hydro_cnt)
		f_trans_cnt = format_count(trans_cnt)
		f_building_cnt = format_count(building_cnt)
		f_landcover_cnt = format_count(landcover_cnt)
		write(u"    |     - Feature report generated             {0}|".format(exs))
		write(u"    |          {0} Point Features            {1}{2}|".format(pnt_cnt, f_pnt_cnt, exs))
		write(u"    |          {0} Curve Features            {1}{2}|".format(crv_cnt, f_crv_cnt, exs))
		write(u"    |          {0} Surface Features          {1}{2}|".format(srf_cnt, f_srf_cnt, exs))
		write(u"    |          {0} Total Features            {1}{2}|".format(tots_f, f_tots_f, exs))
		write(u"    |          {0} Hydrography Features      {1}{2}|".format(hydro_cnt, f_hydro_cnt, exs))
		write(u"    |          {0} Transportation Features   {1}{2}|".format(trans_cnt, f_trans_cnt, exs))
		write(u"    |          {0} Buildings                 {1}{2}|".format(building_cnt, f_building_cnt, exs))
		write(u"    |          {0} Landcover Surfaces        {1}{2}|".format(landcover_cnt, f_landcover_cnt, exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
	if vsource:
		write(u"    |     - Source report generated              {0}|".format(exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))

	# Easter Egg
	if not vogon and not repair and not fcode and not defaults and not metrics and not ufi and not large and not hydro and not trans and not util and not dups and not explode and not bridge and not pylong and not building and not swap and not fcount and not vsource:
		write(u"    |   {0}   {1}|".format(sspaces, exs))
		write(u"    |       Kristen, click a check box and       {0}|".format(exs))
		write(u"    |             stop being cheeky.             {0}|".format(exs))

	write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
	write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
	write("\n")

def main(*argv):
	# Parameters
	TDS = argv[0]
	ap.env.workspace = TDS
	workspace = os.path.dirname(ap.env.workspace)
	bool_dict = {
		'vogon': bool(argv[1]), # Skips large building datasets
		'repair': bool(argv[2]),
		'fcode': bool(argv[3]),
		'defaults': bool(argv[4]),
		'metrics': bool(argv[5]),
		'ufi': bool(argv[6]),
		'large': bool(argv[7]), # Running chunk processing for integrating large datasets
		'hydro': bool(argv[8]),
		'trans': bool(argv[9]),
		'util': bool(argv[10]),
		'dups': bool(argv[11]),
		'explode': bool(argv[12]),
		'bridge': bool(argv[13]),
		'pylong': bool(argv[14]),
		'building': bool(argv[15]), # Be sure to add Structure Srf and Pnt back if vogon is checked
		'swap': bool(argv[16]),
		'fcount': bool(argv[17]),
		'vsource': bool(argv[18]),
		'secret': bool(argv[19]) ### update index as needed
	}

	error_count = 0
	featureclass = ap.ListFeatureClasses()

	grand_entrance(TDS, bool_dict)

	check_out_defense(bool_dict)

	if bool_dict['hydro'] or bool_dict['trans'] or bool_dict['util']:
		tool_name = 'Integrate and Repair'
		write("\n--- {0} ---\n".format(tool_name))
		# add conditional and function calls for hydro, trans, and util


if __name__=='__main__':
	ap.env.overwriteOutput = True
	argv = tuple(ap.GetParameterAsText(i) for i in range(ap.GetArgumentCount()))
	now = dt.datetime.now()
	main(*argv)
	write(dt.datetime.now() - now)
