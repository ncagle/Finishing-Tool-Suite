# -*- coding: utf-8 -*-
# ======================= #
# Preprocessing Tool v9.7 #
# Nat Cagle 2022-05-10    #
# ======================= #

# ArcPy aliasing
import arcpy as ap
from arcpy import (AddFieldDelimiters as field_delim,
	AddMessage as write,
	MakeFeatureLayer_management as make_lyr,
	MakeTableView_management as make_tbl,
	SelectLayerByAttribute_management as select_by_att,
	SelectLayerByLocation_management as select_by_loc,
	Delete_management as arcdel)
# Collections to organize and simplify
from collections import OrderedDict
from collections import namedtuple
# STOP! Hammer time
from datetime import datetime as dt
import time
# Number bumbers
import csv as cs
import pandas as pd
import numpy as np
import math
import uuid
import re
# System Modules
import os
import sys
import imp
import traceback
import subprocess
#import arc_dict as ad
ad = imp.load_source('arc_dict', r"Q:\Special_Projects\4_Finishing\Post Production Tools & Docs\6_Tools\_dict_source\arc_dict.py")

#            ________________________________
#           | It does a whole bunch of stuff |
#           | and I'm not gonna bother       |
#           | changing this speech bubble    |
#           | every time. Have a quacker.    |
#           |                                |
#           |  *quack*                       |
#           |                       *quack*  |
#           |            *quack*             |
#           |                                |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~


#----------------------------------------------------------------------

# To Do List:
#### 4 hashtags means things to be updated
## 2 hashtags means recent changes/updates


## scale_name wasn't defined after the function refactor. Added second return value from snowflake_protocol func to return schema scale field name



#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Global Dictionaries and Parameters #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# search dict_import
	# fcode_dict
		# { 'AB040' : 'AerationBasin', ...}
	# fcsub_dict
		# { 100010 : 'AerationBasin', ...}
	# sub2fcode_dict
		# {100185 : 'AQ120', ...}
	# fc_fields_og
		# { 'AeronauticCrv' : ['F_CODE','FCSUBTYPE','ZI026_CTUU','Shape','Version'], ...}
	# fc_fields
		# { 'AeronauticCrv' : ['f_code','fcsubtype','zi026_ctuu','shape@','version'], ...}
	# ffn_list_all
		# OrderedDict([('    Public Administration', 808), ...]) # Sorted, formatted, list of tuples that becomes an ordered dictionary
	# ffn_list_caci
		# Same as above but the CACI specific version cz they just have to be different


''''''''' User Parameters '''''''''
TDS = ap.GetParameterAsText(0)
ap.env.workspace = TDS
workspace = os.path.dirname(ap.env.workspace)
ap.env.overwriteOutput = True
#vogon = ap.GetParameter(1) # Skips large building datasets
secret = ap.GetParameter(1) ### update index as needed
disable = ap.GetParameter(2)
bridge = ap.GetParameter(3)
pylong = ap.GetParameter(4)
# hydrattr = ap.GetParameter(3)
# tranattr = ap.GetParameter(4)
# utilattr = ap.GetParameter(5)
building = ap.GetParameter(5) # Be sure to add Structure Srf and Pnt back if vogon is checked
swap = ap.GetParameter(6)
fcount = ap.GetParameter(7)
vsource = ap.GetParameter(8) # Michael here.
#sdepull = ap.GetParameter(19)
#dataload = ap.GetParameter(20)

#----------------------------------------------------------------------

""" General Functions """

# Explicit is better than implicit
# Lambda function works better than "if not fieldname:", which can falsely catch 0.
populated = lambda x: x is not None and str(x).strip() != '' and x != -999999 # Function that returns boolean of if input field is populated or empty or default
not_null = lambda x: x is not None
is_null = lambda x: x is None

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

def writeresults(tool_name): # If tool fails, get messages and output error report before endind process
	write("\n\n***Failed to run {0}.***\n".format(tool_name))
	trace_back = sys.exc_info()[2] # Get the traceback object
	tb_info = traceback.format_tb(trace_back)[0] # Format the traceback information
	python_errors = "Traceback Info:\n{0}\nError Info:\n{1}\n".format(tb_info, sys.exc_info()[1]) # Concatenate error information together
	arcpy_errors = "ArcPy Error Output:\n{0}".format(ap.GetMessages(0))
	warnings = ap.GetMessages(1)

	if len(warnings) > 0:
		write("Tool Warnings:")
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		write(warnings)
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	write("Error Report:")
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	ap.AddError(python_errors)
	ap.AddError(arcpy_errors)
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	write('                       ______\n                    .-"      "-.\n                   /            \\\n       _          |              |          _\n      ( \\         |,  .-.  .-.  ,|         / )\n       > "=._     | )(__/  \\__)( |     _.=" <\n      (_/"=._"=._ |/     /\\     \\| _.="_.="\\_)\n             "=._ (_     ^^     _)"_.="\n                 "=\\__|IIIIII|__/="\n                _.="| \\IIIIII/ |"=._\n      _     _.="_.="\\          /"=._"=._     _\n     ( \\_.="_.="     `--------`     "=._"=._/ )\n      > _.="                            "=._ <\n     (_/                                    \\_)\n')
	write("Please rerun the tool, but uncheck the {0} tool option.\nEither the feature class is too big or something else has gone wrong.".format(tool_name))
	write("Exiting tool.\n")
	sys.exit(0)
	#print(u'                 uuuuuuu\n             uu$$$$$$$$$$$uu\n          uu$$$$$$$$$$$$$$$$$uu\n         u$$$$$$$$$$$$$$$$$$$$$u\n        u$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$"   "$$$"   "$$$$$$u\n       "$$$$"      u$u       $$$$"\n        $$$u       u$u       u$$$\n        $$$u      u$$$u      u$$$\n         "$$$$uu$$$   $$$uu$$$$"\n          "$$$$$$$"   "$$$$$$$"\n            u$$$$$$$u$$$$$$$u\n             u$"|¨|¨|¨|¨|"$u\n  uuu        $$u|¯|¯|¯|¯|u$$       uuu\n u$$$$        $$$$$u$u$u$$$       u$$$$\n  $$$$$uu      "$$$$$$$$$"     uu$$$$$$\nu$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$\n$$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"\n """      ""$$$$$$$$$$$uu ""$"""\n           uuuu ""$$$$$$$$$$uuu\n  u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$\n  $$$$$$$$$$""""           ""$$$$$$$$$$$"\n   "$$$$$"                      ""$$$$""\n     $$$"                         $$$$"')

def runtime(start, finish): # Time a process or code block
	# Add a start and finish variable markers surrounding the code to be timed
	#from datetime import datetime as dt
	#start/finish = dt.now()
	# Returns string of formatted elapsed time between start and finish markers
	time_delta = (finish - start).total_seconds()
	h = int(time_delta/(60*60))
	m = int((time_delta%(60*60))/60)
	s = time_delta%60.
	time_elapsed = "{}:{:>02}:{:>05.4f}".format(h, m, s) # 00:00:00.0000
	return time_elapsed

def make_field_list(dsc): # Construct a list of proper feature class fields
	# Sanitizes Geometry fields to work on File Geodatabases or SDE Connections
	#field_list = make_field_list(describe_obj)
	fields = dsc.fields # List of all fc fields
	out_fields = [dsc.OIDFieldName, dsc.lengthFieldName, dsc.areaFieldName, 'shape', 'area', 'length'] # List Geometry and OID fields to be removed
	# Construct sanitized list of field names
	field_list = [field.name for field in fields if field.type not in ['Geometry'] and not any(substring in field.name for substring in out_fields)]
	# Add ufi field to index[-3], OID@ token to index[-2], and Shape@ geometry token to index[-1]
	field_list.append('OID@')
	field_list.append('SHAPE@')
	return field_list

def replace_list_value(existing, new, llist):
	return list(map(lambda x: x.replace(existing, new), llist))

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

def format_count(count): # format counts with the right amount of spacing for output report
	cnt_str = str(count)
	end_spacing = ""
	if len(cnt_str) > 0:
		for i in range(7-len(cnt_str)):
			end_spacing += " "
	else:
		pass
	return end_spacing

def get_count(fc_layer): # Returns feature count
    results = int(ap.GetCount_management(fc_layer).getOutput(0))
    return results

def fc_exists(fc, tool_name): # Check if feature class exists
	if ap.Exists(fc):
		return True
	else:
		write("{0} feature class missing.\n{1} will skip steps involving {0} .".format(fc, tool_name))
		return False

#----------------------------------------------------------------------

""" Tool Functions """

def create_fc_list(vogon):
	fc_list_start = dt.now()
	featureclass = ap.ListFeatureClasses()
	# Formatting Feature Class list
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
	if vogon:
		if ap.Exists('StructurePnt'):
			featureclass.remove('StructurePnt')
		if ap.Exists('StructureSrf'):
			featureclass.remove('StructureSrf')
		write("StructureSrf and StructurePnt will be skipped in processing")
	# if loc_delux:
	# 	featureclass = ['MilitaryPnt', 'StoragePnt', 'TransportationGroundPnt', 'UtilityInfrastructurePnt', 'MilitaryCrv', 'TransportationGroundCrv', 'UtilityInfrastructureCrv', 'FacilitySrf', 'MilitarySrf', 'StorageSrf', 'TransportationGroundSrf', 'UtilityInfrastructureSrf']
	featureclass.sort()
	fc_list_finish = dt.now()
	write("Loaded {0} of 55 TDSv7.1 feature classes in {1}".format(len(featureclass), runtime(fc_list_start, fc_list_finish)))
	return featureclass

def snowflake_protocol(featureclass): # Checking for CACI schema cz they're "special" and have to make everything so fucking difficult
	snowflake_start = dt.now()
	scale_field = 'scale'
	write("Checking for CACI custom schema")
	for fc in featureclass:
		fc_zero = get_count(fc)
		if fc_zero == 0:
			continue
		else:
			field_check = ap.ListFields(fc)
			field_check = [field.name for field in field_check if any([scale_field in field.name.lower()])]
			if field_check:
				snowflake_finish = dt.now()
				write("Variant TDS schema identified in {0}\nSnowflake protocol activated for relevant tools".format(runtime(snowflake_start, snowflake_finish)))
				return True, field_check
			else:
				snowflake_finish = dt.now()
				write("Regular TDS schema identified in {0}".format(runtime(snowflake_start, snowflake_finish)))
				return False, scale_field

def disable_editor_tracking(featureclass, gdb_name): # Automatically disables editor tracking for each feature class that doesn't already have it disabled
	disable_start = dt.now()
	write("\nDisabling Editor Tracking for {0}".format(gdb_name))
	firstl = False
	for fc in featureclass:
		desc = ap.Describe(fc)
		if desc.editorTrackingEnabled:
			try:
				ap.DisableEditorTracking_management(fc)
				if not firstl:
					write("\n")
					firstl = True
				write("{0} - Disabled".format(fc))
			except:
				write("Error disabling editor tracking for {0}. Please check the data manually and try again.".format(fc))
				pass
	if firstl:
		write("Editor Tracking has been disabled.")
	else:
		write("Editor Tracking has already been disabled.")
	disable_finish = dt.now()
	write("Time to disable Editor Tracking: {0}".format(runtime(disable_start, disable_finish)))

def check_defense(in_out, defaults, metrics, explode): # If any of the tools that require the Defense Mapping license are selected, check out the Defense license
	if defaults or metrics or explode:
		class LicenseError(Exception):
			pass
		try:
			if ap.CheckExtension('defense') == 'Available' and in_out == 'out':
				write("\n~~ Checking out Defense Mapping Extension ~~\n")
				ap.CheckOutExtension('defense')
			elif in_out == 'in':
				write("\n~~ Checking Defense Mapping Extension back in ~~\n")
				ap.CheckInExtension('defense')
			else:
				raise LicenseError
		except LicenseError:
			write("Defense Mapping license is unavailable")
		except ap.ExecuteError:
			writeresults('check_defense')

#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Title Formatting and Workspace Setup #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Sanitizing GDB name
gdb_name = re.findall(r"[\w']+", os.path.basename(os.path.split(TDS)[0]))[0]
rresults = os.path.split(os.path.split(TDS)[0])[0]

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

if secret == 'Chairman Bock':
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
if bridge:
	write(u"    |     - Default Bridge WID Updater           {0}|".format(exs))
if pylong:
	write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
if building:
	write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
if swap:
	write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
if fcount:
	write(u"    |     - Generate Feature Report              {0}|".format(exs))
if vsource:
	write(u"    |     - Generate Source Report               {0}|".format(exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")


#----------------------------------------------------------------------
featureclass = create_fc_list(False)
caci_schema, scale_name = snowflake_protocol(featureclass)
if disable:
	disable_editor_tracking(featureclass, gdb_name)
#check_defense('out', defaults, metrics, explode)
where_scale = "zi026_ctuu >= 50000" #### Add option to specify what scale and up to run the tool on.


#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Preprocessing Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Default Bridge WID Updater '''''''''
## Added 50k+ restriction
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
	bridge_start = dt.now()
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
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130') AND zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 13")
	# Make road bridges with default (-999999) width into layer
	ap.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeR")

	# Select rail bridges with default (-999999) width
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130') AND zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 12")
	# Make rail bridges with default (-999999) width into layer
	ap.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeRR")

	# Select roads that share curve with the default width bridges above
	ap.SelectLayerByAttribute_management("road_crv_lyr", "NEW_SELECTION", "F_CODE = 'AP030' AND zi026_ctuu >= 50000")
	ap.SelectLayerByLocation_management("road_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "fc_bridgeR", "", "SUBSET_SELECTION")
	# Make roads that share curve with default width bridges into layer
	ap.MakeFeatureLayer_management("road_crv_lyr", "fc_road")

	# Select rails that share curve with the default width bridges above
	ap.SelectLayerByAttribute_management("rail_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AN010', 'AN050') AND zi026_ctuu >= 50000")
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
		bridge_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(bridge_start, bridge_finish)))
		break
	# Error handling. If no roads or rails to select against, likely something will break.
	if total_roads == 0 and total_rails == 0:
		write("{0} default WID bridges found.".format(total_bridges))
		write("No underlying roads or rails for default bridges. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.")
		bridge_err = True
		bridge_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(bridge_start, bridge_finish)))
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
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE = 'AQ040' AND zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999")
	# Make these selections into a new layer and get a count
	ap.MakeFeatureLayer_management("bridge_crv_lyr", "bridges_rem")
	total_rem_b = int(ap.management.GetCount("bridges_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	bridge_count = (countR + countRR) - total_rem_b
	write("Updated {0} bridges with new WID values.".format(bridge_count))
	if total_rem_b > 0:
		write("{0} bridges still have default WID. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.".format(total_rem_b))
	bridge_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(bridge_start, bridge_finish)))
	break
#Default Bridge WID Updater finished in 0:08:51.2600

''''''''' Default Pylon HGT Updater '''''''''
## Added 50k+ restriction
# Checks for pylons with default HGT (-999999) and updates them to match the intersecting cable HGT
while pylong:
	pylong_err = False
	no_def_pylon = False
	lecount = 0
	total_rem_p = 0
	tool_name = 'Default Pylon HGT Updater'
	write("\n--- {0} ---\n".format(tool_name))
	if not ap.Exists('UtilityInfrastructurePnt') or not ap.Exists('UtilityInfrastructureCrv'):
		write("UtilityInfrastructurePnt or UtilityInfrastructureCrv feature classes missing./nCannot run Default Pylon HGT Updater.")
		pylong_err = True
		break
	break

while pylong: # Needs updating from management geoprocessing to cursors
	pylong_start = dt.now()
	if pylong_err:
		break
	# Pull height and geometry fields
	fields = ['HGT', 'SHAPE@']

	# Convert the feature classes from the TDS into usable layers
	write("Making feature layers...")
	ap.MakeFeatureLayer_management("UtilityInfrastructurePnt", "utility_pnt_lyr")
	ap.MakeFeatureLayer_management("UtilityInfrastructureCrv", "utility_crv_lyr")
	write("Successfully made the feature layers!")

	# Select pylons with default (-999999) height
	ap.SelectLayerByAttribute_management("utility_pnt_lyr", "NEW_SELECTION", "F_CODE = 'AT042' AND zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("utility_pnt_lyr", "SUBSET_SELECTION", "HGT = -999999")
	ap.MakeFeatureLayer_management("utility_pnt_lyr", "fc_pylon_total")
	# Select cables that intersect the default height pylons above and removes any with default height
	ap.SelectLayerByAttribute_management("utility_crv_lyr", "NEW_SELECTION", "F_CODE = 'AT005' AND zi026_ctuu >= 50000")
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
		pylong_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(pylong_start, pylong_finish)))
		break
	# Error handling. If no cables to select against, likely something will break.
	if total_cables == 0:
		write("{0} default value pylons found.".format(total_pylons))
		write("No intersecting cables for default pylons. \n Try running Integrate and Repair then try again. \n The default pylons are either not snapped or missing a cable.")
		pylong_err = True
		pylong_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(pylong_start, pylong_finish)))
		break

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
	ap.SelectLayerByAttribute_management("fc_pylon", "NEW_SELECTION", "F_CODE = 'AT042' AND zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("fc_pylon", "SUBSET_SELECTION", "HGT = -999999")
	# Make these selections into a new layer and get a count
	ap.MakeFeatureLayer_management("fc_pylon", "pylons_rem")
	total_rem_p = int(ap.management.GetCount("pylons_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	lecount = lecount - total_rem_p
	write("Updated {0} pylons with new HGT values.".format(lecount))
	write("{0} pylons still have default HGT. \n Consider running Integrate and Repair before trying again. \n The remaining pylons are not snapped, missing a cable, or the underlying cable doesn't have a height.".format(total_rem_p))
	pylong_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(pylong_start, pylong_finish)))
	break
#Default Pylon HGT Updater finished in 0:00:6.4830


#----------------------------------------------------------------------
''''''''' Building in BUA Descaler '''''''''
# Descales buildings within BUAs that don't have important FFNs, have a height < 46m, and aren't navigation landmarks
# Scales in buildings within BUAs that do have important FFNs, have a height >= 46m, or are navigation landmarks
while building:
	# Initialize task
	building_start = dt.now()
	tool_name = 'Building in BUA Descaler'
	write("\n--- {0} ---\n".format(tool_name))

	#~~~~~ Royal Decree Variables ~~~~~
	# Check that required feature classes exist
	bua_exist = fc_exists('SettlementSrf', tool_name) # Does SettlementSrf fc exist in the dataset
	building_s_exist = fc_exists('StructureSrf', tool_name) # Does StructureSrf fc exist in the dataset
	building_p_exist = fc_exists('StructurePnt', tool_name) # Does StructureSrf fc exist in the dataset
	bua_count = 0
	total_2upscale = 0
	total_2descale = 0
	if not bua_exist: # Task can't run if SettlementSrf fc is missing
		break
	if not building_s_exist and not building_p_exist: # Task can't run if both StructureSrf and StructurePnt fcs are missing. Only one is fine.
		break
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# Intra-task variables
	total_2upscale_s = 0
	total_2descale_s = 0
	total_2upscale_p = 0
	total_2descale_p = 0
	update_field = 'ZI026_CTUU'
	bua_query = "F_CODE = 'AL020' AND ZI026_CTUU >= 50000" # We don't need to worry about below scale BUAs, right?
	building_query_2upscale = "F_CODE = 'AL013' AND ZI026_CTUU < 50000" # Maybe less than 250k for building surfaces?
	building_query_2descale = "F_CODE = 'AL013' AND ZI026_CTUU >= 50000"
	caci_ffn_query_2upscale = "FFN IN ({0}) OR HGT >= 46 OR LMC = 1001".format(", ".join(str(i) for i in ad.ffn_list_caci.values())) #dict_import
	caci_ffn_query_2descale = "FFN NOT IN ({0}) AND HGT < 46 AND LMC <> 1001".format(", ".join(str(i) for i in ad.ffn_list_caci.values())) #dict_import
	ffn_query_2upscale = "FFN IN ({0}) OR HGT >= 46 OR LMC = 1001".format(", ".join(str(i) for i in ad.ffn_list_all.values())) #dict_import
	ffn_query_2descale = "FFN NOT IN ({0}) AND HGT < 46 AND LMC <> 1001".format(", ".join(str(i) for i in ad.ffn_list_all.values())) #dict_import

	#----------------------------------------------------------------------

	write("Retrieved Settlement and Structure feature classes")
	# Make layer of BUAs >= 50k
	make_lyr("SettlementSrf", "buas", bua_query)
	#make_tbl("SettlementSrf", "buas", bua_query) # Cannot be used for geometry.
	write("Searching within BUAs")
	bua_count = get_count("buas")

	if not bua_count: # No BUAs to check against buildings. Wrap up task.
		write("\nNo BUAs found.")
		building_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
		break

	if building_s_exist:
		# Adam's original important ffn list for just building points: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building surfaces matching criteria...\n")
		if caci_schema: # Snowflake Protocol
			write("CACI specific important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_caci.items())) #dict_import

			# Make layer of building surfaces < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_12.5k_within_2upscale", caci_ffn_query_2upscale)

			# Make layer of building surfaces >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_50k+_within_2descale", caci_ffn_query_2descale)

			# # Alternative solution
			# # This starts with a geometry comparison with all structure srfs against BUAs, not just buildings
			# # The current method makes a queries the buildings to limit the number of features before the geometry comparison
			# # That should be faster.
			# # Make layer of BUAs and layer of all building surfaces within those BUAs
			# make_lyr("SettlementSurfaces", "buas", bua_query)
			# make_lyr(
			# 	select_by_loc(
			# 		make_lyr("StructureSrf", "structure_s"),
			# 		"WITHIN", "buas", "", "NEW_SELECTION"),
			# 	"structure_s_within")
			# # Select building surfaces 50k and up that are within BUAs
			# # Make layer of important building surfaces to descale
			# make_lyr(
			# 	select_by_att("structure_s_within", "NEW_SELECTION", building_query_2descale),
			# 	"building_s_50k+_within_2descale", caci_ffn_query_2descale)
			# # Select below scale building surfaces that are within BUAs
			# # Make layer of important building surfaces to upscale
			# make_lyr(
			# 	select_by_att("structure_s_within", "NEW_SELECTION", building_query_2upscale),
			# 	"building_s_12.5k_within_2upscale", caci_ffn_query_2upscale)

		#-----------------------------------

		else:
			write("Current project important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_all.items())) #dict_import

			# Make layer of building surfaces < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_12.5k_within_2upscale", ffn_query_2upscale)

			# Make layer of building surfaces >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_50k+_within_2descale", ffn_query_2descale)

		total_2upscale_s = get_count("building_s_12.5k_within_2upscale")
		total_2descale_s = get_count("building_s_50k+_within_2descale")
		write("\n{0} below scale building surfaces in {1} BUAs are important, tall, or interesting.\nThey will be scaled up.".format(total_2upscale_s, bua_count))
		write("{0} building surfaces >= 50k in {1} BUAs are unimportant, short, and uninteresting.\nThey will be descaled.\n".format(total_2descale_s, bua_count))

		#-----------------------------------

		if total_2upscale_s:
			# Scale in important, tall, or landmark building surfaces within BUAs from below 50k to 250k (per PSG)
			write("Setting below scale important, tall, or landmark building surfaces to 250k...")
			with ap.da.UpdateCursor("building_s_12.5k_within_2upscale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 250000
					ucursor.updateRow(urow)

		if total_2descale_s:
			# Descale unimportant, short, and uninteresting building surfaces within BUAs from 50k+ to 12.5k
			write("Setting unimportant, short, and uninteresting building surfaces to 12.5k...")
			with ap.da.UpdateCursor("building_s_50k+_within_2descale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 12500
					ucursor.updateRow(urow)

		write("")

	if building_p_exist:
		# Adam's original important ffn list for just building points: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building points matching criteria...\n")
		if caci_schema: # Snowflake Protocol
			write("CACI specific important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_caci.items())) #dict_import

			# Make layer of building points < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_12.5k_within_2upscale", caci_ffn_query_2upscale)

			# Make layer of building points >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_50k+_within_2descale", caci_ffn_query_2descale)

		#-----------------------------------

		else:
			write("Current project important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_all.items())) #dict_import

			# Make layer of building points < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_12.5k_within_2upscale", ffn_query_2upscale)

			# Make layer of building points >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_50k+_within_2descale", ffn_query_2descale)

		total_2upscale_p = get_count("building_p_12.5k_within_2upscale")
		total_2descale_p = get_count("building_p_50k+_within_2descale")
		write("\n{0} below scale building points in {1} BUAs are important, tall, or interesting.\nThey will be scaled up.".format(total_2upscale_p, bua_count))
		write("{0} building points >= 50k in {1} BUAs are unimportant, short, and uninteresting.\nThey will be descaled.\n".format(total_2descale_p, bua_count))

		#-----------------------------------

		if total_2upscale_p:
			# Scale in important, tall, or landmark building points within BUAs from below 50k to 50k
			write("Setting below scale important, tall, or landmark building points to 50k...")
			with ap.da.UpdateCursor("building_p_12.5k_within_2upscale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 50000
					ucursor.updateRow(urow)

		if total_2descale_p:
			# Descale unimportant, short, and uninteresting building points within BUAs from 50k+ to 12.5k
			write("Setting unimportant, short, and uninteresting building points to 12.5k...")
			with ap.da.UpdateCursor("building_p_50k+_within_2descale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 12500
					ucursor.updateRow(urow)

		write("")

	#----------------------------------------------------------------------

	# Count total buildings being upscaled and downscaled
	total_2upscale = total_2upscale_s + total_2upscale_p
	total_2descale = total_2descale_s + total_2descale_p

	# Clean up created layers
	for lyr in ["buas", "building_s_50k+", "building_s_50k+_within_2descale", "building_s_12.5k", "building_s_12.5k_within_2upscale"]: arcdel(lyr)

	write("{0} building surfaces scaled to 250k.".format(total_2upscale_s))
	write("{0} building surfaces scaled to 12500.".format(total_2descale_s))
	write("{0} building points scaled to 50000.".format(total_2upscale_p))
	write("{0} building points scaled to 12500.".format(total_2descale_p))
	building_finish = dt.now()
	write("\n{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
	break

# ''''''''' Building in BUA Descaler '''''''''
# # Descales buildings within BUAs that don't have important FFNs
# #### make 50k+ restriction in function
# while building:
# 	building_err = False
# 	no_bua = False
# 	no_bua_buildings = False
# 	total_non_imp = 0
# 	tool_name = 'Building in BUA Descaler'
# 	write("\n--- {0} ---\n".format(tool_name))
# 	if not ap.Exists('SettlementSrf'):
# 		write("SettlementSrf feature class missing./nCannot run Building in BUA Descaler.")
# 		building_err = True
# 		break
# 	if not ap.Exists('StructureSrf') and not ap.Exists('StructurePnt'):
# 		write("StructureSrf and StructurePnt feature classes missing./nCannot run Building in BUA Descaler.")
# 		building_err = True
# 		break
# 	break
#
# while building: # Needs updating from management geoprocessing to cursors
# 	building_start = dt.now()
# 	if building_err:
# 		break
# 	# Make initial layers from the workspace
# 	srf_exist = False
# 	pnt_exist = False
# 	import_ffn_s = 0
# 	import_ffn_p = 0
# 	non_import_count_s = 0
# 	non_import_count_p = 0
# 	fields = 'ZI026_CTUU'
# 	caci_query = "FFN IN ({0}) OR HGT >= 46".format(", ".join(str(i) for i in ad.ffn_list_caci.values())) #dict_import
# 	other_query = "FFN IN ({0}) OR HGT >= 46".format(", ".join(str(i) for i in ad.ffn_list_all.values())) #dict_import
#
# 	if caci_schema:
# 		write("CACI specific important building FFNs list:")
# 		write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_caci.items())) #dict_import
# 	else:
# 		write("Current project important building FFNs list:")
# 		write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_all.items())) #dict_import
#
# 	# Make layer of BUAs
# 	write("\nRetrieved feature classes containing BUAs and Buildings")
# 	write("Selecting BUAs")
# 	ap.MakeFeatureLayer_management("SettlementSrf", "settlement_srf")
# 	ap.SelectLayerByAttribute_management("settlement_srf", "NEW_SELECTION", "F_CODE = 'AL020' AND ZI026_CTUU >= 50000")
# 	ap.MakeFeatureLayer_management("settlement_srf", "buas")
# 	write("Searching within BUAs")
#
# #### change the naming for these. descale and inscale is confusing. because descale is not descaled. non_import is descaled
#
# 	if ap.Exists('StructureSrf'):
# 		ap.MakeFeatureLayer_management("StructureSrf", "structure_srf")
# 		# Make layer of building surfaces 50k and up
# 		ap.SelectLayerByAttribute_management("structure_srf", "NEW_SELECTION", "F_CODE = 'AL013' AND ZI026_CTUU >= 50000")
# 		ap.MakeFeatureLayer_management("structure_srf", "building_srf_inscale")
# 		# Layer of in scale building surfaces within BUAs
# 		ap.SelectLayerByLocation_management ("building_srf_inscale", "WITHIN", "buas", "", "NEW_SELECTION")
# 		ap.MakeFeatureLayer_management("building_srf_inscale", "bua_building_inscale_s")
# 		# Make layer of building surfaces below 50k
# 		ap.SelectLayerByAttribute_management("structure_srf", "NEW_SELECTION", "F_CODE = 'AL013' AND ZI026_CTUU <= 50000")
# 		ap.MakeFeatureLayer_management("structure_srf", "building_srf_unscaled")
# 		# Layer of below scale building surfaces within BUAs
# 		ap.SelectLayerByLocation_management ("building_srf_unscaled", "WITHIN", "buas", "", "NEW_SELECTION")
# 		ap.MakeFeatureLayer_management("building_srf_unscaled", "bua_building_unscaled_s")
#
# 		# Select important building surfaces and switch selection
# 		# Adam's original list: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
# 		write("Identifying building surfaces matching criteria...")
# 		if caci_schema:
# 			ap.SelectLayerByAttribute_management("bua_building_inscale_s", "NEW_SELECTION", caci_query)
# 			ap.SelectLayerByAttribute_management("bua_building_unscaled_s", "NEW_SELECTION", caci_query)
# 		else:
# 			ap.SelectLayerByAttribute_management("bua_building_inscale_s", "NEW_SELECTION", other_query)
# 			ap.SelectLayerByAttribute_management("bua_building_unscaled_s", "NEW_SELECTION", other_query)
#
# 		import_ffn_inscale_s = get_count("bua_building_inscale_s")
# 		import_ffn_unscaled_s = get_count("bua_building_unscaled_s")
# 		ap.SelectLayerByAttribute_management("bua_building_inscale_s", "SWITCH_SELECTION")
# 		ap.MakeFeatureLayer_management("bua_building_inscale_s", "non_import_s")
# 		non_import_count_s = get_count("non_import_s")
#
# 	if ap.Exists('StructurePnt'):
# 		ap.MakeFeatureLayer_management("StructurePnt", "structure_pnt")
# 		# Make layer of building points 50k and up
# 		ap.SelectLayerByAttribute_management("structure_pnt", "NEW_SELECTION", "F_CODE = 'AL013' AND ZI026_CTUU <= 50000")
# 		ap.MakeFeatureLayer_management("structure_pnt", "building_pnt_inscale")
# 		# Layer of in scale building points within BUAs
# 		ap.SelectLayerByLocation_management ("building_pnt_inscale", "WITHIN", "buas", "", "NEW_SELECTION")
# 		ap.MakeFeatureLayer_management("building_pnt_inscale", "bua_building_inscale_p")
# 		# Make layer of building points below 50k
# 		ap.SelectLayerByAttribute_management("structure_pnt", "NEW_SELECTION", "F_CODE = 'AL013' AND ZI026_CTUU <= 50000")
# 		ap.MakeFeatureLayer_management("structure_pnt", "building_pnt_unscaled")
# 		# Layer of below scale building points within BUAs
# 		ap.SelectLayerByLocation_management ("building_pnt_unscaled", "WITHIN", "buas", "", "NEW_SELECTION")
# 		ap.MakeFeatureLayer_management("building_pnt_unscaled", "bua_building_unscaled_p")
#
# 		# Select important building points and switch selection
# 		# Adam's original list: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
# 		write("Identifying building points matching criteria...")
# 		if caci_schema:
# 			ap.SelectLayerByAttribute_management("bua_building_inscale_p", "NEW_SELECTION", caci_query)
# 			ap.SelectLayerByAttribute_management("bua_building_unscaled_p", "NEW_SELECTION", caci_query)
# 		else:
# 			ap.SelectLayerByAttribute_management("bua_building_inscale_p", "NEW_SELECTION", other_query)
# 			ap.SelectLayerByAttribute_management("bua_building_unscaled_p", "NEW_SELECTION", other_query)
# 		import_ffn_inscale_p = get_count("bua_building_inscale_p")
# 		import_ffn_unscaled_p = get_count("bua_building_unscaled_p")
# 		ap.SelectLayerByAttribute_management("bua_building_inscale_p", "SWITCH_SELECTION")
# 		ap.MakeFeatureLayer_management("bua_building_inscale_p", "non_import_p")
# 		non_import_count_p = get_count("non_import_p")
#
# 	# Count buildings and buas in selections
# 	bua_count = get_count("buas")
# 	total_import = import_ffn_inscale_s + import_ffn_unscaled_s + import_ffn_inscale_p + import_ffn_unscaled_p
# 	total_unscaled = import_ffn_unscaled_s + import_ffn_unscaled_p
# 	total_non_imp = non_import_count_s + non_import_count_p
#
# 	# End script if there are no BUAs or no buildings inside them
# 	if bua_count == 0:
# 		write("\nNo BUAs found.")
# 		no_bua = True
# 		building_finish = dt.now()
# 		write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
# 		break
# 	if total_non_imp == 0:
# 		write("\nNo buildings without important FFNs or taller than 46m found in BUAs.")
# 		no_bua_buildings = True
# 		building_finish = dt.now()
# 		write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
# 		break
# 	elif import_ffn_unscaled_s + import_ffn_unscaled_p == 0:
# 		write("\nNo unscaled buildings with important FFNs or taller than 46m found in BUAs.")
# 		no_bua_buildings = True ## fix this later to have its' own outro variable
# 		building_finish = dt.now()
# 		write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
# 		break
#
# 	write("\n{0} tall buildings with important FFNs found in {1} total BUAs.".format(total_import, bua_count))
# 	write("{0} of {1} are below scale and will be scaled to 50k.\n".format(total_unscaled, total_import))
#
# 	if ap.Exists('StructureSrf'):
# 		# Scale in selected, important, tall buildings within BUAs from below 50k to 50k
# 		write("Setting below scale important or tall building surfaces to 50k...")
# 		with ap.da.UpdateCursor("bua_building_unscaled_s", fields) as cursor_s:
# 			for row in cursor_s:
# 				row[0] = 50000
# 				cursor_s.updateRow(row)
#
# 		# Descale selected, non-important, short buildings within BUAs from 50k+ to 12.5k
# 		write("Setting unimportant or short building surfaces to 12.5k...")
# 		with ap.da.UpdateCursor("non_import_s", fields) as cursor_s:
# 			for row in cursor_s:
# 				row[0] = 12500
# 				cursor_s.updateRow(row)
#
# 	if ap.Exists('StructurePnt'):
# 		# Scale in selected, important, tall buildings within BUAs from below 50k to 50k
# 		write("Setting below scale important or tall building points to 50k...")
# 		with ap.da.UpdateCursor("bua_building_unscaled_p", fields) as cursor_p:
# 			for row in cursor_p:
# 				row[0] = 50000
# 				cursor_p.updateRow(row)
#
# 		# Descale selected, non-important, short buildings within BUAs from 50k+ to 12.5k
# 		write("Setting unimportant or short building points to 12.5k...")
# 		with ap.da.UpdateCursor("non_import_p", fields) as cursor_p:
# 			for row in cursor_p:
# 				row[0] = 12500
# 				cursor_p.updateRow(row)
#
# 	write("\n{0} building surfaces descaled to CTUU 12500.".format(non_import_count_s))
# 	write("{0} building points descaled to CTUU 12500.".format(non_import_count_p))
# 	building_finish = dt.now()
# 	write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
# 	break
# #Building in BUA Descaler finished in 0:00:18.7870

''''''''' CACI Swap Scale and CTUU '''''''''
# Swaps the Scale field with the CTUU field so we can work normally with CACI data
while swap:
	tool_name = 'CACI Swap Scale and CTUU'
	write("\n--- {0} ---\n".format(tool_name))
	if not caci_schema:
		write("Provided TDS does not match CACI schema containing the 'Scale' field.\nCannot run CACI Swap Scale and CTUU")
		break
	if caci_schema:
		write("CACI schema containing 'Scale' field identified")
	featureclass = create_fc_list(False)
	break

while swap:
	swap_start = dt.now()
	if not caci_schema:
		break
	write("Swapping CTUU and Scale for {0}".format(gdb_name))
	write("\nNote: The SAX_RX9 field will be changed from <NULL> to 'Scale Swapped' after the first swap. It will flip back and forth in subsequent runs.\nIf the tool was aborted on a previous run for some reason, it will reset all feature classes to the dominant swap format to maintain internal consistency. It is still up to the user to know which format they were swapping from. (Either Scale->CTUU or CTUU->Scale) Check the tool output for more information on which feature classes were changed.\n")
	fields = ['zi026_ctuu', 'scale', 'swap', 'progress', 'sax_rx9']
	fields[1] = str(scale_name)

	# Explicit is better than implicit
	populated = lambda x: x is not None and str(x).strip() != '' # Finds empty fields. See UFI process

	write("\nChecking if any previous swaps were canceled. Please wait...")
	swap_fc = []
	none_fc = []
	empty_fc = []
	chk_fields = ['sax_rx9', 'scale']
	chk_fields[1] = str(scale_name)
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
		# 	if f.name == "progress":
		# 		partialchk = True
		# 	if f.name == "swap":
		# 		swapchk = True
		# 		break
		# if swapchk:
		# 	continue
		with ap.da.SearchCursor(fc, chk_fields) as scursor:
			for row in scursor:
				if not populated(row[0]):
					if not populated(row[1]):
						continue
					none_fc.append(str(fc))
					break
				if row[0] == 'Scale Swapped':
					if not populated(row[1]):
						continue
					swap_fc.append(str(fc))
					break
	if len(swap_fc) == 0 or len(none_fc) == 0:
		clean_proceed = True
	elif len(swap_fc) > len(none_fc):
		swap_dom = True
	elif len(swap_fc) < len(none_fc):
		none_dom = True
	if not clean_proceed:
		write("\n***Previous run was flagged. Resetting feature classes to previous format.***\n")
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
	swap_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(swap_start, swap_finish)))
	break


#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Database Management Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Database Feature Report '''''''''
# Refactored from John Jackson's Feature_Itemized_Counter.py by Nat Cagle
while fcount:
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
	break

while fcount:
	fcount_start = dt.now()
	# Define fields for Search Cursor
	fields = ["FCSubtype"]
	if not 'StructurePnt' in featureclass and ap.Exists('StructurePnt'):
		featureclass.append(u'StructurePnt')
	if not 'StructureSrf' in featureclass and ap.Exists('StructureSrf'):
		featureclass.append(u'StructureSrf')

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
		with ap.da.SearchCursor(i,fields) as vCursor:
			try:
				# Iterate through features in Feature Class
				for j in vCursor:
					curr_sub = int(j[0])
					# Counting Feature Subtypes
					if ad.fcsub_dict[int(j[0])] not in feat_dict[currFC][0]: #dict_import
						feat_dict[str(i)][0][ad.fcsub_dict[int(j[0])]] = 1 #dict_import
					else:
						feat_dict[currFC][0][ad.fcsub_dict[int(j[0])]] += 1 #dict_import
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
		txt_file.write("Feature Count Report for TPC: {0}.gdb\n".format(gdb_name))
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
	fcount_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(fcount_start, fcount_finish)))
	break
#Database Feature Report finished in 0:00:14.8690

''''''''' Source Analysis Report '''''''''
# Refactored from John Jackson's Version_Source_Counter.py by Nat Cagle
while vsource:
	tool_name = 'Source Analysis Report'
	write("\n--- {0} ---\n".format(tool_name))
	break

while vsource:
	vsource_start = dt.now()
	time_stamp = dt.now().strftime("%Y_%m_%d_%H%M")
	fields = ["Version","ZI001_SDP","ZI001_SDV","ZI001_SRT"]
	results_csv = "{0}\\{1}_Source_Count_{2}.csv".format(rresults, gdb_name, time_stamp)
	results_txt = "{0}\\{1}_Source_Count_{2}.txt".format(rresults, gdb_name, time_stamp)
	feat_dict = OrderedDict()
	write("Checking feature classes...\n")

	# Fill in dictionary with leveled counts: Version -> SDP -> SDV *optional SRT
	for i in featureclass:
		feat_dict[str(i)]=OrderedDict()
		with ap.da.SearchCursor(i,fields) as vCursor:
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
		txt_file.write("Source Report for TPC: {0}.gdb\nScroll right for all information.\n**For an ordered view, see accompanying .csv file\n\n".format(gdb_name))
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
	vsource_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(vsource_start, vsource_finish)))
	break
#Source Analysis Report finished in 0:00:11.1890

#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Report Formatting and Wrap Up #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#check_defense('in', default, metrics, explode)

# Report of completed tasks
write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}{4}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

# Easter Egg
if secret == 'Chairman Bock':
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
	write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
	if not bua_exist or (not building_s_exist and not building_p_exist):
		write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not bua_count:
		write(u"    |          No BUAs found                     {0}|".format(exs))
	else:
		write(u"    |          {0} Buildings upscaled        {1}{2}|".format(total_2upscale, format_count(total_2upscale), exs))
		write(u"    |          {0} Buildings descaled        {1}{2}|".format(total_2descale, format_count(total_2descale), exs))
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
if not bridge and not pylong and not building and not swap and not fcount and not vsource:
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |       Kristen, click a check box and       {0}|".format(exs))
	write(u"    |             stop being cheeky.             {0}|".format(exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")
