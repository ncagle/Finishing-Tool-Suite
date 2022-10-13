# -*- coding: utf-8 -*-
# ====================== #
# Finishing Tool v9.7    #
# Nat Cagle 2022-04-27   #
# ====================== #
import arcpy as ap
from arcpy import AddMessage as write
from arcpy import AddFieldDelimiters as fieldDelim
import datetime
from datetime import datetime as dt
from collections import OrderedDict
import pandas as pd
import numpy as np
import csv as cs
import uuid
import os
import sys
import time
import math
import traceback
import re
import imp

#import arc_dict as ad
ad = imp.load_source('arc_dict', r"Q:\Special_Projects\4_Finishing\Post Production Tools & Docs\FTX_source_dev\arc_dict.py")

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

#### Make class for TDS properties like all variations of filepath and name

# rewrite selections of default pylons and bridges and make new fc in memory for cursor
# in memory upgrade
# Defense mapping version takes too long and crashes. just rewrite with manual calculations
# Error handling for feature classes used in integration not present in database
# Error handling for featureclass <NoneType> has no attribute .sort(). Tell user that ArcMap has failed to interanlly update the location of the input TDS. Just restart ArcMap and try again.
# Pull local user profile name and add it to the "stop being cheeky" easter egg
# optional DisableEditorTracking_management (default true)

#####

# Toolbox is running slow when everything is imported. All in one script 3000 lines and growing.
# I didn't want the individual tools cz I wanted the entire workflow to be accessible from one window
# What if each of the categories does have it's own tool if it needs to be run in particular without all
# the other options. But then the main Finishing Tool Suite is a Workflow Wrapper.
# So it imports the toolbox of itself and then calls the other tools in the toolbox as they are checked.
# This way, it stays sleek. Roundabout way of having tools as functions split up and importing them while
# still keeping it all in one toolbox without extra files

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
secret = ap.GetParameterAsText(1)
vogon = ap.GetParameter(2) # Skips large building datasets
disable = ap.GetParameter(3)
repair = ap.GetParameter(4)
fcode = ap.GetParameter(5)
defaults = ap.GetParameter(6)
defaults2 = ap.GetParameter(7)
metrics = ap.GetParameter(8)
ufi = ap.GetParameter(9)
#large = ap.GetParameter(7) # Running chunk processing for integrating large datasets
hydro = ap.GetParameter(10)
hydro2 = ap.GetParameter(11)
trans = ap.GetParameter(12)
trans2 = ap.GetParameter(13)
util = ap.GetParameter(14)
util2 = ap.GetParameter(15)
dups = ap.GetParameter(16)
explode = ap.GetParameter(17)
#sdepull = ap.GetParameter(19)
#dataload = ap.GetParameter(20)
# For Top-Secret Finishing Version, what is the name of our leader?


#----------------------------------------------------------------------

""" General Functions """

# Explicit is better than implicit
# Lambda function works better than "if not fieldname:", which can falsely catch 0.
populated = lambda x: x is not None and str(x).strip() != '' # Function that returns boolean of if input field is populated or empty
not_null = lambda x: x is not None
is_null = lambda x: x is None

def replace_list_value(existing, new, llist):
	return list(map(lambda x: x.replace(existing, new), llist))

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
	trace_back = ''
	tb_info = ''
	python_errors = ''
	arcpy_errors = ''
	warnings = ''
	try:
		trace_back = sys.exc_info()[2] # Get the traceback object
		tb_info = traceback.format_tb(trace_back)[0] # Format the traceback information
		python_errors = "Traceback Info:\n{0}\nError Info:\n{1}\n".format(tb_info, sys.exc_info()[1]) # Concatenate error information together
		arcpy_errors = "ArcPy Error Output:\n{0}".format(ap.GetMessages(0))
		warnings = ap.GetMessages(1)
	except:
		pass

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
				return True
			else:
				snowflake_finish = dt.now()
				write("Regular TDS schema identified in {0}".format(runtime(snowflake_start, snowflake_finish)))
				return False

def disable_editor_tracking(featureclass): # Automatically disables editor tracking for each feature class that doesn't already have it disabled
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
	return firstl

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

def populate_null(fc, field_list, default):
	#populate_null(fc, string_fields, <'noInformation' or -999999>)
	count = 0
	with ap.da.UpdateCursor(fc, field_list) as ucursor:
		#write("    Assigning domain defaults from coded values...")
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

def process_defaults(featureclass):
	try:
		count_nulls = 0
		write("Constructing field type lists to match default values to domain definitions.")
		for fc in featureclass:
			out_fields = ['shape', 'area', 'length', 'created', 'edited', 'f_code', 'fcsubtype', 'ufi', 'version']
			in_types = ['Double', 'Integer', 'Single', 'SmallInteger']
			string_fields = [field.name for field in arcpy.ListFields(fc, None, 'String') if not any(substring in field.name for substring in out_fields)]
			number_fields = [field.name for field in arcpy.ListFields(fc) if field.type in in_types and not any(substring in field.name for substring in out_fields)]
			string_fields.sort()
			number_fields.sort()
			fc_nulls = 0
			write("Locating NULL text and numeric fields in {0}".format(fc))
			fc_nulls += populate_null(fc, string_fields, 'noInformation')
			fc_nulls += populate_null(fc, number_fields, -999999)
			if fc_nulls > 0:
				write("  - {0} NULL values populated".format(fc_nulls))
			count_nulls += fc_nulls
		write('{0} total NULL values populated with default values'.format(count_nulls))
	except ap.ExecuteError:
		writeresults(tool_name)

# def dangling_orphans():
# 	arcpy.DeleteDangles_production(inFeatures, "10 Feet", '#', 'NON_RECURSIVE', '45')
# 	arcpy.RemoveCutbacks_production(roads, minimum_angle, "SEQUENTIAL", '#', 'IGNORE_SNAPPED_POINTS', '#')

def snap_lines_to_srf(lines, srf): #d     snap_srf__lines((((()))))
	vertex_env = [srf, "VERTEX", "0.03 Meters"] # Snap lines to the nearest srf vertex within 0.03m
	edge_env = [srf, "EDGE", "0.03 Meters"] # snap remaining lines to the nearest srf edge within 0.03m
	ap.Snap_edit(lines, [vertex_env, edge_env])
	ap.Integrate_management([[srf, 1], [lines, 2]]) # Integrate lines to srfs with default domain tolerance to create intersection vertices in them without morphing them and creating potential errors.
	ap.RepairGeometry_management(srf, "DELETE_NULL")

def snap_points_to_lines(points, lines):
	end_env = [lines, "END", "0.03 Meters"] # Snap points to the nearest line end node within 0.03m as priority over other vertices
	vertex_env = [lines, "VERTEX", "0.03 Meters"] # Snap points to the nearest line vertex within 0.03m
	edge_env = [lines, "EDGE", "0.03 Meters"] # snap remaining points to the nearest line edge within 0.03m
	ap.Snap_edit(points, [end_env, vertex_env, edge_env])
	ap.Integrate_management([[lines, 1], [points, 2]]) # Integrate points to lines with default domain tolerance to create intersection vertices in the lines without morphing them and creating potential errors.
	ap.RepairGeometry_management(points, "DELETE_NULL")
	ap.RepairGeometry_management(lines, "DELETE_NULL")

def make_integrate_layers(name_list, tool_name):
	#name_list = ['FeaturePnt', 'FeatureCrv', 'FeatureSrf', 'feat_pnt', 'feat_crv', 'feat_srf']
	if not ap.Exists(name_list[0]):
		write("** {0} feature class not found\n  To run Integrate, copy an empty {0} feature class from a blank schema into this dataset and run the tool again. **".format(name_list[0]))
		writeresults(tool_name)
	if not ap.Exists(name_list[1]):
		write("** {0} feature class not found\n  To run Integrate, copy an empty {0} feature class from a blank schema into this dataset and run the tool again. **".format(name_list[1]))
		writeresults(tool_name)
	if not ap.Exists(name_list[2]):
		write("** {0} feature class not found\n  To run Integrate, copy an empty {0} feature class from a blank schema into this dataset and run the tool again. **".format(name_list[2]))
		writeresults(tool_name)

	write("- - - - - - - - - - - - - - - - - - - - - - ")
	write(" ~ {0} ~ ".format(tool_name))
	write("Making {0}, {1}, and {2} feature layers".format(name_list[0], name_list[1], name_list[2]))
	if name_list[0] == 'UtilityInfrastructurePnt':
		ap.MakeFeatureLayer_management(name_list[0], name_list[3], "f_code = 'AT042' AND zi026_ctuu >= 50000")
	else:
		ap.MakeFeatureLayer_management(name_list[0], name_list[3], "zi026_ctuu >= 50000")
	if name_list[1] == 'UtilityInfrastructureCrv':
		ap.MakeFeatureLayer_management(name_list[1], name_list[4], "f_code = 'AT005' AND zi026_ctuu >= 50000")
	else:
		ap.MakeFeatureLayer_management(name_list[1], name_list[4], "zi026_ctuu >= 50000")
	ap.MakeFeatureLayer_management(name_list[2], name_list[5], "zi026_ctuu >= 50000")
	write("Repairing {0} lines and {1} polygons before Integration".format(name_list[1], name_list[2]))
	ap.RepairGeometry_management(name_list[4], "DELETE_NULL")
	ap.RepairGeometry_management(name_list[5], "DELETE_NULL")

def repair_and_clean(name_list):
	write("Repairing {0} and {1} features after Integration".format(name_list[1], name_list[2]))
	ap.RepairGeometry_management(name_list[4], "DELETE_NULL")
	ap.RepairGeometry_management(name_list[5], "DELETE_NULL")
	write("Clearing process cache")
	ap.Delete_management(name_list[3])
	ap.Delete_management(name_list[4])
	ap.Delete_management(name_list[5])
	write("- - - - - - - - - - - - - - - - - - - - - -")

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
if repair:
	write(u"    |     - Repair All NULL Geometries           {0}|".format(exs))
if fcode:
	write(u"    |     - Populate F_Codes                     {0}|".format(exs))
if defaults:
	write(u"    |     - Calculate Default Values             {0}|".format(exs))
if metrics:
	write(u"    |     - Calculate Metrics                    {0}|".format(exs))
if ufi:
	write(u"    |     - Update UFI Values                    {0}|".format(exs))
if hydro or trans or util:
	write(u"    |     - Integrate and Repair:                {0}|".format(exs))
	if hydro:
		write(u"    |          Hydro                             {0}|".format(exs))
	if trans:
		write(u"    |          Trans                             {0}|".format(exs))
	if util:
		write(u"    |          Utilities                         {0}|".format(exs))
if dups:
	write(u"    |     - Delete Identical Features            {0}|".format(exs))
if explode:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")

#----------------------------------------------------------------------

featureclass = create_fc_list(vogon)
caci_schema = snowflake_protocol(featureclass)
if disable:
	disable_start = dt.now()
	write("\nDisabling Editor Tracking for {0}".format(gdb_name))
	if not disable_editor_tracking(featureclass):
		write("Editor Tracking has already been disabled.")
	disable_finish = dt.now()
	write("Time to disable Editor Tracking: {0}".format(runtime(disable_start, disable_finish)))
check_defense('out', defaults, metrics, explode)
where_scale = "zi026_ctuu >= 50000" #### Add option to specify what scale and up to run the tool on.

#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Data Maintenance Tools Category   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Repair All NULL Geometry '''''''''
# Repairs all NULL geometries in each feature class
#### rewrite with intersect geometry method to remove duplicate vertices and kickbacks
# if input_shp is None:
# write("{0} feature OID: {1} found with NULL geometry. Skipping transfer.".format(fc_strip, srow[-2]))
# continue
while repair:
	repair_start = dt.now()
	tool_name = 'Repair All NULL Geometry'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			write("Repairing NULL geometries in {0}".format(fc))
			ap.RepairGeometry_management(fc, "DELETE_NULL")
		except ap.ExecuteError:
			writeresults(tool_name)
	#arcpy.RepairBadGeometry_production(featureclass, 'REPAIR_ONLY', 'DELETE_NULL_GEOMETRY', '#') # Repair Bad Geometry Production Mapping tool
	repair_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(repair_start, repair_finish)))
	break




''''''''' Populate F_Codes '''''''''
## Added 50k+ restriction
# John Jackson's Fcode tool refactored from standalone with included dictionaries instead of imported
while fcode:
	fcode_start = dt.now()
	tool_name = 'Populate F_Codes'
	write("\n--- {0} ---\n".format(tool_name))
	fcode_total = 0
	for fc in featureclass:
		fcode_count = 0
		try:
			try:
				fields = ['f_code', 'fcsubtype']
				with ap.da.UpdateCursor(fc, fields, where_scale) as fcursor:
					for row in fcursor: # Checks if F_Code matches the FCSubtype value. Updates F_Code if they don't match assuming proper subtype
						if row[0] != str(ad.sub2fcode_dict[row[1]]): #dict_import
							row[0] = str(ad.sub2fcode_dict[row[1]]) #dict_import
							fcode_count += 1
							fcursor.updateRow(row)
				write("Updated {0} {1} feature F_Codes".format(fcode_count, fc))
				fcode_total += fcode_count
			except:
				write("{0} does not contain F_codes.".format(fc))
		except ap.ExecuteError:
			writeresults(tool_name)
	fcode_finish = dt.now()
	write("{0} fixed {1} total F_Code errors in {2}".format(tool_name, fcode_total, runtime(fcode_start, fcode_finish)))
	break

#Populate F_Codes fixed 675 total F_Code errors in 0:00:6.9260


''''''''' Calculate Default Values '''''''''
#### make 50k+ restriction in function
# Calculate default values for NULL attributes
# All or nothing. Functions on datasets not individual feature classes
#### rewrite using domains and coded values thru cursors
while defaults or defaults2:
	defaults_start = dt.now()
	tool_name = 'Calculate Default Values'
	write("\n--- {0} ---\n".format(tool_name))
	if defaults:
		write("Locating NULL fields")
		try:
			write("Assigning domain defaults from coded values...")
			ap.CalculateDefaultValues_defense(ap.env.workspace)
			write("Complete")
		except ap.ExecuteError:
			writeresults(tool_name)
	if defaults2:
		process_defaults(featureclass)
	defaults_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(defaults_start, defaults_finish)))
	break

#default2 finished in 0:01:25.0860
#Calculate Default Values finished in 0:01:18.5650



''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
## Only run on Polygon ARA and Polyline LZN
#### Defense mapping version takes too long and crashes. just rewrite with manual calculations
# for line and polygon metrics, if area or length is tool small throw warning with output.
while metrics:
	metrics_start = dt.now()
	tool_name = 'Calculate Metrics'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			if get_count(fc) == 0:
				continue
			shape_type = ap.Describe(fc).shapeType, # Polygon, Polyline, Point, Multipoint, MultiPatch
			if shape_type[0] == 'Polyline':
				write("Calculating Length field for {0}".format(fc))
				ap.CalculateMetrics_defense(fc, 'LENGTH', "LZN", "#", "#", "#", "#", "#")
			elif shape_type[0] == 'Polygon':
				write("Calculating Area field for {0}".format(fc))
				ap.CalculateMetrics_defense(fc, 'AREA', "#", "#", "ARA", "#", "#", "#")
		except ap.ExecuteError:
			writeresults(tool_name)
	metrics_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(metrics_start, metrics_finish)))
	break

#Calculate Metrics finished in 0:02:28.6500

''''''''' Update UFI Values '''''''''
## Only populates blanks, duplicates, or incorrect values such as 'noInformation'
## Added 50k+ restriction
# Iterate through all features and update the ufi field with uuid4 random values
while ufi:
	ufi_start = dt.now()
	tool_name = 'Update UFI Values'
	write("\n--- {0} ---\n".format(tool_name))
	ufi_total = 0
	for fc in featureclass:
		try:
			ufi_count = 0
			with ap.da.SearchCursor(fc, 'ufi', where_scale) as scursor:
				values = [row[0] for row in scursor]
			with ap.da.UpdateCursor(fc, 'ufi', where_scale) as ucursor:
				for row in ucursor:
					if not populated(row[0]):
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					elif len(row[0]) != 36: # 36 character random alphanumeric string. GOTOHELL-FUCK-COCK-PISS-MOTHERFUCKER is valid tho XD
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					elif values.count(row[0]) > 1:
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					ucursor.updateRow(row)
				write("Updated {0} UFIs in {1}".format(ufi_count, fc))
				ufi_total += ufi_count
		except ap.ExecuteError:
			writeresults(tool_name)
	ufi_finish = dt.now()
	write("{0} updated {1} invalid or missing UFI values in {2}".format(tool_name, ufi_total, runtime(ufi_start, ufi_finish)))
	break

#Update UFI Values updated 149134 invalid or missing UFI values in 0:00:29.7570

#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Feature Specific Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Integrate and Repair '''''''''
## Removed layered integration and dropped tolerance to 0.02m
## Moved Integrate Large Datasets option to backend. It is now default since it runs faster regardless.
#### Add integration of hydro VanishingPoints and NaturalPools
#### Major rework of logic behind integrate step.
#### Potentially do away with Integrate and make a few tools that just do the major things we need integrate to do
####   - Run snap tool with low tolerance for helping keep certain features coincident.
####   - Decrease the integrate tolerance to 0.02m. We used 0.03m for a while, but for older clients, we used to use 0.01m. So this splits the difference and should cut down on the duplicate vertices errors.
# User choice to Integrate and Repair Hydrography curves, TransportationGround curves, or Utility points and surfaces to curves
if hydro or trans or util or hydro2 or trans2 or util2:
	tool_name = 'Integrate and Repair'
	write("\n--- {0} ---\n".format(tool_name))
while hydro or hydro2:
	if hydro:
		hydro_start = dt.now()
		tool_name = 'Hydrography Curves'
		fc1 = 'HydrographyCrv'
		fc2 = 'HydrographySrf'
		if not ap.Exists(fc1):
			write("**HydrographyCrv feature class not found\n  To run Integrate, copy an empty Hydro curve feature class from a blank schema into this dataset and run the tool again.")
			break
		if not ap.Exists(fc2):
			write("**HydrographySrf feature class not found\n  To run Integrate, copy an empty Hydro surface feature class from a blank schema into this dataset and run the tool again.")
			break

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
						ap.Integrate_management("hc_scale 1;hs_scale 2", "0.02 Meters")
					elif feat_count > 0:
						ap.Integrate_management('hc_scale', "0.02 Meters")
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
		hydro_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(hydro_start, hydro_finish)))
		break

	if hydro2:
		hydro_start = dt.now()
		tool_name = 'Integrate Hydrography Features'
		hydro_list = ['HydrographyPnt', 'HydrographyCrv', 'HydrographySrf', 'hydro_pnt', 'hydro_crv', 'hydro_srf']
		hydro_pnt = hydro_list[3]
		hydro_crv = hydro_list[4]
		hydro_srf = hydro_list[5]
		make_integrate_layers(hydro_list, tool_name)
		hfeat_count = 0

		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(hydro_list[1])
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			ap.MinimumBoundingGeometry_management(hydro_list[1], rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with ap.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", hydro_list[1], "POLYGON")
			#ap.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			grid = 'hgrid'
			ap.MakeFeatureLayer_management(mem_fc, grid)
			with ap.da.SearchCursor(grid, ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					ap.SelectLayerByAttribute_management(grid, "NEW_SELECTION", select)
					ap.SelectLayerByLocation_management(hydro_pnt, "INTERSECT", grid, "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management(hydro_crv, "INTERSECT", grid, "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management(hydro_srf, "INTERSECT", grid, "", "NEW_SELECTION")
					pnt_count = get_count(hydro_pnt)
					crv_count = get_count(hydro_crv)
					srf_count = get_count(hydro_srf)
					hfeat_count = hfeat_count + pnt_count + crv_count + srf_count
					write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(pnt_count, hydro_list[0], crv_count, hydro_list[1], srf_count, hydro_list[2], row[0]))
					if crv_count > 0 and srf_count > 0:
						snap_lines_to_srf(hydro_crv, hydro_srf)
					if pnt_count > 0 and crv_count > 0:
						snap_points_to_lines(hydro_pnt, hydro_crv)
					if pnt_count == 0 and srf_count == 0 and crv_count > 0:
						ap.Integrate_management(hydro_crv, "0.02 Meters")
			write("Freeing partition memory")
			ap.Delete_management("in_memory")
			ap.Delete_management(grid)
		except ap.ExecuteError:
			writeresults(tool_name)

		repair_and_clean(hydro_list)
		hydro_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(hydro_start, hydro_finish)))
		break

# Hydrography Curves finished in 0:02:44.5230
while trans or trans2:
	if trans:
		trans_start = dt.now()
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
						ap.Integrate_management("tgp_scale 2;tgc_scale 1", "0.02 Meters")
					elif feat_count > 0:
						ap.Integrate_management("tgc_scale", "0.02 Meters")
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
		trans_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(trans_start, trans_finish)))
		break

	if trans2:
		trans_start = dt.now()
		tool_name = 'Integrate Transportation Features'
		trans_list = ['TransportationGroundPnt', 'TransportationGroundCrv', 'TransportationGroundSrf', 'trans_pnt', 'trans_crv', 'trans_srf']
		trans_pnt = trans_list[3]
		trans_crv = trans_list[4]
		trans_srf = trans_list[5]
		make_integrate_layers(trans_list, tool_name)
		tfeat_count = 0

		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(trans_list[1])
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			ap.MinimumBoundingGeometry_management(trans_list[1], rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with ap.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", trans_list[1], "POLYGON")
			#ap.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			grid = 'tgrid'
			ap.MakeFeatureLayer_management(mem_fc, grid)
			with ap.da.SearchCursor(grid, ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					ap.SelectLayerByAttribute_management(grid, "NEW_SELECTION", select)
					ap.SelectLayerByLocation_management(trans_pnt, "INTERSECT", grid, "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management(trans_crv, "INTERSECT", grid, "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management(trans_srf, "INTERSECT", grid, "", "NEW_SELECTION")
					pnt_count = get_count(trans_pnt)
					crv_count = get_count(trans_crv)
					srf_count = get_count(trans_srf)
					tfeat_count = tfeat_count + pnt_count + crv_count + srf_count
					write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(pnt_count, trans_list[0], crv_count, trans_list[1], srf_count, trans_list[2], row[0]))
					if crv_count > 0 and srf_count > 0:
						snap_lines_to_srf(trans_crv, trans_srf)
					if pnt_count > 0 and crv_count > 0:
						snap_points_to_lines(trans_pnt, trans_crv)
					if pnt_count == 0 and srf_count == 0 and crv_count > 0:
						ap.Integrate_management(trans_crv, "0.02 Meters")
			write("Freeing partition memory")
			ap.Delete_management("in_memory")
			ap.Delete_management(grid)
		except ap.ExecuteError:
			writeresults(tool_name)

		repair_and_clean(trans_list)
		trans_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(trans_start, trans_finish)))
		break

while util or util2:
	if util:
		util_start = dt.now()
		tool_name = 'Utility Points, Lines, and Surfaces'
		fc1 = 'UtilityInfrastructurePnt'
		fc2 = 'UtilityInfrastructureCrv'
		fc3 = 'UtilityInfrastructureSrf'
		if not ap.Exists(fc1):
			write("**UtilityInfrastructurePnt feature class not found\n  To run Integrate, copy an empty Utility point feature class from a blank schema into this dataset and run the tool again.")
			break
		if not ap.Exists(fc2):
			write("**UtilityInfrastructureCrv feature class not found\n  To run Integrate, copy an empty Utility curve feature class from a blank schema into this dataset and run the tool again.")
			break
		if not ap.Exists(fc3):
			write("**UtilityInfrastructureSrf feature class not found\n  To run Integrate, copy an empty Utility surface feature class from a blank schema into this dataset and run the tool again.")
			break

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
					ap.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.02 Meters")
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
		util_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(util_start, util_finish)))
		break

	if util2:
		util_start = dt.now()
		tool_name = 'Inegrate Utility Features'
		util_list = ['UtilityInfrastructurePnt', 'UtilityInfrastructureCrv', 'UtilityInfrastructureSrf', 'util_pnt', 'util_crv', 'util_srf']
		util_pnt = util_list[3]
		util_crv = util_list[4]
		util_srf = util_list[5]
		make_integrate_layers(util_list, tool_name)
		ufeat_count = 0

		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(util_list[1])
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			ap.MinimumBoundingGeometry_management(util_list[1], rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with ap.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", util_list[1], "POLYGON")
			#ap.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			grid = 'tgrid'
			ap.MakeFeatureLayer_management(mem_fc, grid)
			with ap.da.SearchCursor(grid, ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					ap.SelectLayerByAttribute_management(grid, "NEW_SELECTION", select)
					ap.SelectLayerByLocation_management(util_pnt, "INTERSECT", grid, "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management(util_crv, "INTERSECT", grid, "", "NEW_SELECTION")
					ap.SelectLayerByLocation_management(util_srf, "INTERSECT", grid, "", "NEW_SELECTION")
					pnt_count = get_count(util_pnt)
					crv_count = get_count(util_crv)
					srf_count = get_count(util_srf)
					ufeat_count = ufeat_count + pnt_count + crv_count + srf_count
					write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(pnt_count, util_list[0], crv_count, util_list[1], srf_count, util_list[2], row[0]))
					if crv_count > 0 and srf_count > 0:
						snap_lines_to_srf(util_crv, util_srf)
					if pnt_count > 0 and crv_count > 0:
						snap_points_to_lines(util_pnt, util_crv)
					if pnt_count == 0 and srf_count == 0 and crv_count > 0:
						ap.Integrate_management(util_crv, "0.02 Meters")
			write("Freeing partition memory")
			ap.Delete_management("in_memory")
			ap.Delete_management(grid)
		except ap.ExecuteError:
			writeresults(tool_name)

		repair_and_clean(util_list)
		util_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(util_start, util_finish)))
		break


#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Geometry Correction Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Delete Identical Features '''''''''
# Checks for features with identical geometry and PSG attribution and removes them
#### Test rewritten find identical code and replace existing
while dups:
	dups_start = dt.now()
	tool_name = 'Delete Identical Features'
	write("\n--- {0} ---\n".format(tool_name))
	out_table = os.path.dirname(TDS) # Output directory for Find Identical # C:/Projects/njcagle/S1_C09C_20210427.gdb
	path = os.path.join(rresults, gdb_name) # Output dBASE table location # C:/Projects/njcagle/S1_C09C_20210427
	table_loc = "{0}.dbf".format(path) # C:/Projects/njcagle/R&D/__Thunderdome/S1_C09C_20210427.dbf
	write("Creating temporary output files:\n    - {0}.dbf\n    - {0}.dbf.xml\n    - {0}.cpg\n    - {0}.IN_FID.atx".format(gdb_name))
	dup_count = 0

	for fc in featureclass: # Loop feature classes and FindIdentical to get a count, then delete any found
		try:
			dick = ad.fc_fields_og[fc] # Does not include metric fields. Uses 'Shape' instead of 'SHAPE@' #dict_import
			ap.FindIdentical_management(fc, out_table, dick, "", "", output_record_option="ONLY_DUPLICATES")
			rows = get_count("{0}.dbf".format(path))
			write("Searching for duplicate features in {0}...".format(fc))
			if rows > 0:
				ap.DeleteIdentical_management(fc, dick)
				write("  - Deleted {0} duplicate features.".format(rows))
				dup_count += rows
		except ap.ExecuteError:
			if os.path.exists("{0}.dbf".format(path)): os.remove("{0}.dbf".format(path))
			if os.path.exists("{0}.dbf.xml".format(path)): os.remove("{0}.dbf.xml".format(path))
			if os.path.exists("{0}.cpg".format(path)): os.remove("{0}.cpg".format(path))
			if os.path.exists("{0}.IN_FID.atx".format(path)): os.remove("{0}.IN_FID.atx".format(path))
			ap.RefreshCatalog(out_table)
			writeresults(tool_name)
	# Clean up before next process
	os.remove("{0}.dbf".format(path))
	os.remove("{0}.dbf.xml".format(path))
	os.remove("{0}.cpg".format(path))
	os.remove("{0}.IN_FID.atx".format(path))
	ap.RefreshCatalog(out_table)
	dups_finish = dt.now()
	write("{0} removed {1} duplicates in {2}".format(tool_name, dup_count, runtime(dups_start, dups_finish)))
	break

	# ##### check Shape vs shape@ and add xy-tolerance to find and delete identical
	# #search cursor with shape@ and oid@ check each shape against the others. if they match, store the oid in list.
	# #new cursor. check matching shapes. if the other fields match, delete the one with the higher oid value
	# 	for fc in featureclass:
	# 		try:
	# 			prev_check = []
	# 			dup_oids = []
	# 			lap_fields = ['SHAPE@XY', 'OID@']
	#
	# 			with ap.da.SearchCursor(fc, lap_fields) as scursor:
	# 				with ap.da.SearchCursor(fc, lap_fields) as tcursor:
	# 					for row in scursor:
	# 						icursor.insertRow(row)
	# 			atuple = ptGeometry.angleAndDistanceTo(ptGeometry2, "GEODESIC")
	# 			atuple == (angle in degrees, distance in meters)


''''''''' Hypernova Burst Multipart Features '''''''''
## Added 50k+ restriction
# Explodes multipart features for an entire dataset
while explode:
	explode_start = dt.now()
	tool_name = 'Hypernova Burst Multipart Features'
	write("\n--- {0} ---\n".format(tool_name))
	##### Multipart Search #####
	fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
	fc_multi_list = []
	total_multi = 0
	total_complex = 0
	for fc in featureclass:
		try:
			write("Searching for multipart features in {0}".format(fc))
			multipart = False # Assume the feature class doesn't have multiparts
			with ap.da.SearchCursor(fc, ['OID@', 'SHAPE@'], where_scale) as scursor:
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
					write("  - {0} complex polygons found".format(complex))
				if multipart is True:
					count = len(fc_multi[fc])
					write("  - *** {0} true multipart features found! ***".format(count))
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
			if fc_parts[-1] in ad.fc_fields:  #dict_import
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
			fieldnames = ad.fc_fields[fcr]  #dict_import
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
			multistart = dt.now()
			ap.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
			multifinish = dt.now()
			write("Hypernova burst detected after {0} seconds.".format(runtime(multistart, multifinish)))

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
	explode_finish = dt.now()
	write("{0} exploded {1} in {2}".format(tool_name, total_multi, runtime(explode_start, explode_finish)))
	break


#----------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Report Formatting and Wrap Up #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

check_defense('in', defaults, metrics, explode)

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
if vogon:
	write(u"    |     - Buildings skipped                    {0}|".format(exs))
if repair:
	write(u"    |     - Repaired NULL Geometries             {0}|".format(exs))
if fcode:
	f_fcode_total = format_count(fcode_total)
	write(u"    |     - Populated F_Codes                    {0}|".format(exs))
	write(u"    |          {0} F_Code errors fixed       {1}{2}|".format(fcode_total, f_fcode_total, exs))
if defaults:
	write(u"    |     - Calculated Default Values            {0}|".format(exs))
if metrics:
	write(u"    |     - Calculated Metrics                   {0}|".format(exs))
if ufi:
	f_ufi_total = format_count(ufi_total)
	write(u"    |     - Updated UFI Values                   {0}|".format(exs))
	write(u"    |          {0} Duplicate or blank UFIs   {1}{2}|".format(ufi_total, f_ufi_total, exs))
if hydro or trans or util:
	write(u"    |     - Integrated and Repaired:             {0}|".format(exs))
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

# Easter Egg
if not vogon and not disable and not repair and not fcode and not defaults and not defaults2 and not metrics and not ufi and not hydro and not hydro2 and not trans and not trans2 and not util and not util2 and not dups and not explode:
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |       Kristen, click a check box and       {0}|".format(exs))
	write(u"    |             stop being cheeky.             {0}|".format(exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")
