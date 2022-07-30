# -*- coding: utf-8 -*-
#¸¸.·´¯`·.¸¸.·´¯`·.¸¸
# ║╚╔═╗╝║  │┌┘─└┐│  ▄█▀‾
#╔══════════════════════════════╗#
#║ Finishing Tool Suite ver 9.8 ║#
#║   Nat Cagle & John Jackson   ║#
#║    Last Edited 2022-05-09    ║#
#╚══════════════════════════════╝#

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



'''
╔═════════════════╗
║ Notes and To-Do ║
╚═════════════════╝

#### 4 hashtags in the code means things to be updated
## 2 hashtags in the code means recent changes/updates

#### Update Plans
  - Make class for TDS properties like all variations of filepath and name
  - Refactor tools to use in_memory workspace where possible to potentially speed up processing
  - Rewrite default pylons and bridges to be general trans/hydro/utility attribution updater
  - Defense Mapping extension is non-standard and certain computers have issues running those tools. Rewrite them around this limitation.
  - Create function to partition data into chunks for smaller processing sets
  - Pull local user profile name and add it to the "stop being cheeky" easter egg. Create user whitelist and blacklist.
  - Add dropdown with background music selection
  - Replace Royal Decree parameters with dictionary of values from tool outputs similar to initial tool parameters
  - Find and fix Bezier curves
with arcpy.da.SearchCursor("HydrographyCurves", ["OID@", "SHAPE@JSON"]) as scur:
  count = 0
  oid_list = []
  for oid, json in scur:
    count += 1
    if 'curve' in json:
      oid_list.append(oid)
    if '000' in str(count):
      print("Searched {0} curves".format(count))
  print('')
  print("OIDs of features containing Bezier curves:\n({0})".format(str(oid_list)[1:-1]))


arcpy.Densify_edit("HydrographyCurves", "ANGLE","", "", "20")


Populate Line and Point AOO
"C:\Projects\njcagle\finishing\_docs\Populate Line and Point AOO.docx"
https://community.esri.com/t5/spatial-data-science-questions/get-line-direction-orientation-as-a-numeric-field/td-p/532973

# Paste in Pre-Logic Script Code
def north_azimuth(p_line):
	deg_bearing = math.degrees(math.atan2((p_line.lastPoint.X - p_line.firstPoint.X),(p_line.lastPoint.Y - p_line.firstPoint.Y)))
	if (deg_bearing < 0):
		deg_bearing += 360.0
	return deg_bearing
#-----------------------------------
# Paste in 'AOO = '
round(north_azimuth(!Shape!))
#-----------------------------------
with arcpy.da.SearchCursor("Curves_Feature_Class", ['aoo', 'SHAPE@']) as scur:
	with arcpy.da.UpdateCursor("Point_Feature_Class", ['aoo', 'SHAPE@']) as ucur:
		for srow in scur:
			for urow in ucur:
				if not urow[-1].disjoint(srow[-1]):
					urow[0] = srow[0]
					ucur.updateRow(urow)


## Recent Changes
  -


Crevasse
A deep crack in ice.
Crevice
A narrow opening in rock.


Toolbox is running slow when everything is imported. All in one script 3000 lines and growing.
I didn't want the individual tools cz I wanted the entire workflow to be accessible from one window
What if each of the categories does have it's own tool if it needs to be run in particular without all
the other options. But then the main Finishing Tool Suite is a Workflow Wrapper.
So it imports the toolbox of itself and then calls the other tools in the toolbox as they are checked.
This way, it stays sleek. Roundabout way of having tools as functions split up and importing them while
still keeping it all in one toolbox without extra files


#### MAXAR Important FFNs (to be compared)
"Within a BUA only specifc buildings are needed for portayal.

 'FFN' = Utilities =350, Transport = 480, Hotel = 551 Resort = 552, Radio Broadcasting = 601, Television Broadcasting = 604, Public Administration = 808, Public Order, Safety and Security Services = 830, Education = 850, Human Health Activities = 860, Refugee Shelter = 883, Cultural, Arts and Entertainment = 890, Religious Activities = 930, Meeting Place = 970
OR
Height Above Surface Level >= 46 m. OR  Navigation Landmark is True"

'''



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



'''
╔═════════════════════════════════════════╗
║ Dictionaries, Parameters, and Variables ║  Oh, my!
╚═════════════════════════════════════════╝
'''

#----------------------------------------------------------------------
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


#----------------------------------------------------------------------
user = os.getenv('username')
TDS = ap.GetParameterAsText(0)
ap.env.workspace = TDS
arcpy.env.extent = TDS
ap.env.overwriteOutput = True
#workspace = os.path.dirname(ap.env.workspace)
#### Add these three to tool_list and tool_names?
secret = ap.GetParameterAsText(1) # Password for Finishing easter egg
vogon = ap.GetParameter(2) # Skips large building datasets
disable = ap.GetParameter(3) # Disables editor tracking

#----------------------------------------------------------------------
# Param(4) Data Maintenance Tools: ['Repair All NULL Geometries', 'Populate F_Codes', 'Calculate Default Values', 'Calculate Metrics', 'Update UFI Values']
# Param(5) Integration Tools: ['Integrate Hydrography Features', 'Integrate Transportation Features', 'Integrate Utility Features']
# Param(6) Geometry Correction Tools: ['Delete Identical Features', 'Hypernova Burst Multipart Features']
# Param(7) Preprocessing Tools: ['Default Bridge WID Updater', 'Default Pylon HGT Updater', 'Building in BUA Descaler', 'CACI Swap Scale and CTUU']
# Param(8) Database Management Tools: ['Database Feature Report', 'Source Analysis Report']
tool_list = ap.GetParameter(4) + ap.GetParameter(5) + ap.GetParameter(6) + ap.GetParameter(7) + ap.GetParameter(8)

#----------------------------------------------------------------------
name_class = namedtuple("name_class", "repair fcode defaults metrics ufi hydro trans util dups explode bridge pylong building swap fcount vsource")
tool_names = name_class("Repair All NULL Geometries", "Populate F_Codes", "Calculate Default Values", "Calculate Metrics", "Update UFI Values", "Integrate Hydrography Features", "Integrate Transportation Features", "Integrate Utility Features", "Delete Identical Features", "Hypernova Burst Multipart Features", "Default Bridge WID Updater", "Default Pylon HGT Updater", "Building in BUA Descaler", "CACI Swap Scale and CTUU", "Database Feature Report", "Source Analysis Report")

#----------------------------------------------------------------------
bool_dict = OrderedDict([
	(tool_names.repair, False),
	(tool_names.fcode, False),
	(tool_names.defaults, False),
	(tool_names.metrics, False),
	(tool_names.ufi, False),
	(tool_names.hydro, False),
	(tool_names.trans, False),
	(tool_names.util, False),
	(tool_names.dups, False),
	(tool_names.explode, False),
	(tool_names.bridge, False),
	(tool_names.pylong, False),
	(tool_names.building, False),
	(tool_names.swap, False),
	(tool_names.fcount, False),
	(tool_names.vsource, False)
])
for key in (key for key in bool_dict.keys() if key in tool_list): bool_dict[key] = True # Iterate generator of tools in tool_list and set True

#----------------------------------------------------------------------
# Instantiate namedtuple results_holder class to store all the tool results for final printed outputs
results = namedtuple("results_holder", "fcode_total ufi_total hfeat_total tfeat_total ufeat_total dup_total complex_total multi_total bridge_total remaining_bridge_total pylon_total remaining_pylon_total nonimportant_ffn_total point_total curve_total surface_total all_feats_total hydro_total trans_total building_total landcover_total bridge_error no_default_bridge pylong_error no_default_pylon building_error no_bua no_bua_buildings")
# Can be set or reset all in one line like below
#results = results_holder(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, False, False, False, False, False)
#>>>results_holder(fcode_total=0, ufi_total=0, hfeat_total=0, tfeat_total=0, ufeat_total=0, dup_total=0, complex_total=0, multi_total=0, bridge_total=0, remaining_bridge_total=0, pylon_total=0, remaining_pylon_total=0, nonimportant_ffn_total=0, point_total=0, curve_total=0, surface_total=0, all_feats_total=0, hydro_total=0, trans_total=0, building_total=0, landcover_total=0, bridge_error=False, no_default_bridge=False, pylong_error=False, no_default_pylon=False, building_error=False, no_bua=False, no_bua_buildings=False)
# If set with the oneliner, the following code syntax is needed to change values during runtime
#results2 = results2._replace(fcode_total = 12432)
# But instantiated as is, each attribute can just be dynamically updated
#----------------------------------------------------------------------
# Commented categories have been included below in case future result ouputs are added
# Define defaults for all the result_holder attributes
#----------------------------------------------------------------------
''' Data Maintenance Tools '''
#'Repair All NULL Geometries'
results.fcode_total = 0
#'Populate F_Codes'
#'Calculate Default Values'
#'Calculate Metrics'
#'Update UFI Values'
results.ufi_total = 0
#----------------------------------------------------------------------
''' Integration Tools '''
#'Integrate Hydrography Features'
results.hfeat_total = 0
#'Integrate Transportation Features'
results.tfeat_total = 0
#'Integrate Utility Features'
results.ufeat_total = 0
#----------------------------------------------------------------------
''' Geometry Correction Tools '''
#'Delete Identical Features'
results.dup_total = 0
#'Hypernova Burst Multipart Features'
results.complex_total = 0
results.multi_total = 0
#----------------------------------------------------------------------
''' Preprocessing Tools '''
#'Default Bridge WID Updater'
results.bridge_total = 0
results.remaining_bridge_total = 0
results.bridge_error = False
results.no_default_bridge = False
#'Default Pylon HGT Updater'
results.pylon_total = 0
results.remaining_pylon_total = 0
results.pylon_error = False
results.no_default_pylon = False
#'Building in BUA Descaler'
results.nonimportant_ffn_total = 0
results.building_error = False
results.no_bua = False
results.no_bua_buildings = False
#'CACI Swap Scale and CTUU'
#----------------------------------------------------------------------
''' Database Management Tools '''
#'Database Feature Report'
results.point_total = 0
results.curve_total = 0
results.surface_total = 0
results.all_feats_total = 0
results.hydro_total = 0
results.trans_total = 0
results.building_total = 0
results.landcover_total = 0
#'Source Analysis Report'



'''
╔══════════════════════╗
║ GDB Inspection Class ║
╚══════════════════════╝
'''

# WIP



'''
╔═══════════════════╗
║ General Functions ║
╚═══════════════════╝
'''

#### Maybe 3 different NULL checks aren't necessary XD
#----------------------------------------------------------------------
# Explicit is better than implicit
# Lambda function works better than "if not fieldname:", which can falsely catch 0.
populated = lambda x: x is not None and str(x).strip() != '' and x != -999999 # Function that returns boolean of if input field is populated or empty or default
not_null = lambda x: x is not None
is_null = lambda x: x is None

#----------------------------------------------------------------------
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
	ap.AddError("\n\n***Failed to run {0}.***\n".format(tool_name))
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
		ap.AddError("Tool Warnings:")
		ap.AddError("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		ap.AddError(warnings)
		ap.AddError("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	ap.AddError("Error Report:")
	ap.AddError("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	ap.AddError(python_errors)
	ap.AddError(arcpy_errors)
	ap.AddError("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	ap.AddError('                       ______\n                    .-"      "-.\n                   /            \\\n       _          |              |          _\n      ( \\         |,  .-.  .-.  ,|         / )\n       > "=._     | )(__/  \\__)( |     _.=" <\n      (_/"=._"=._ |/     /\\     \\| _.="_.="\\_)\n             "=._ (_     ^^     _)"_.="\n                 "=\\__|IIIIII|__/="\n                _.="| \\IIIIII/ |"=._\n      _     _.="_.="\\          /"=._"=._     _\n     ( \\_.="_.="     `--------`     "=._"=._/ )\n      > _.="                            "=._ <\n     (_/                                    \\_)\n')
	ap.AddError("Please rerun the tool, but uncheck the {0} tool option.\nEither the feature class is too big or something else has gone wrong.".format(tool_name))
	ap.AddError("Exiting tool.\n")
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

#----------------------------------------------------------------------
def make_field_list(dsc): # Construct a list of proper feature class fields
	# Sanitizes Geometry fields to work on File Geodatabases or SDE Connections
	#field_list = make_field_list(describe_obj)
	fields = dsc.fields # List of all fc fields
	out_fields = [dsc.OIDFieldName, dsc.lengthFieldName, dsc.areaFieldName, 'shape', 'area', 'length', 'global'] # List Geometry and OID fields to be removed
	# Construct sanitized list of field names
	field_list = [field.name for field in fields if field.type not in ['Geometry'] and not any(substring in field.name.lower() for substring in out_fields if substring)]
	# Add ufi field to index[-3], OID@ token to index[-2], and Shape@ geometry token to index[-1]
	field_list.append('OID@')
	field_list.append('SHAPE@')
	return field_list

def replace_list_value(existing, new, llist):
	return list(map(lambda x: x.replace(existing, new), llist))

#----------------------------------------------------------------------
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

#----------------------------------------------------------------------
def get_count(fc_layer): # Returns feature count
	results = int(ap.GetCount_management(fc_layer).getOutput(0))
	return results


'''
╔════════════════╗
║ Tool Functions ║
╚════════════════╝
'''

#----------------------------------------------------------------------
def repair_geometry(featureclass):
	repair_start = dt.now()
	tool_name = 'Repair All NULL Geometry'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			write("Repairing NULL geometries in {0}".format(fc))
			ap.RepairGeometry_management(fc, "DELETE_NULL")
		except ap.ExecuteError:
			writeresults(tool_name)
	#ap.RepairBadGeometry_production(featureclass, 'REPAIR_ONLY', 'DELETE_NULL_GEOMETRY', '#') # Repair Bad Geometry Production Mapping tool
	repair_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(repair_start, repair_finish)))

#----------------------------------------------------------------------
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
			string_fields = [field.name for field in ap.ListFields(fc, None, 'String') if not any(substring in field.name.lower() for substring in out_fields)]
			number_fields = [field.name for field in ap.ListFields(fc) if field.type in in_types and not any(substring in field.name.lower() for substring in out_fields)]
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
		writeresults('Calculate Default Values')

#----------------------------------------------------------------------
# def dangling_orphans():
# 	ap.DeleteDangles_production(inFeatures, "10 Feet", '#', 'NON_RECURSIVE', '45')
# 	ap.RemoveCutbacks_production(roads, minimum_angle, "SEQUENTIAL", '#', 'IGNORE_SNAPPED_POINTS', '#')

#----------------------------------------------------------------------
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

def snap_lines_to_srf(lines, srf): #d     snap_srf__lines((((()))))
	vertex_env = [srf, "VERTEX", "0.03 Meters"] # Snap lines to the nearest srf vertex within 0.03m
	edge_env = [srf, "EDGE", "0.03 Meters"] # snap remaining lines to the nearest srf edge within 0.03m
	ap.Snap_edit(lines, [vertex_env, edge_env])
	ap.Integrate_management([[srf, 1], [lines, 2]]) # Integrate lines to srfs with default domain tolerance to create intersection vertices in them without morphing them and creating potential errors.
	ap.RepairGeometry_management(srf, "DELETE_NULL")

####snap points to lines at 0.1m tol to meet GAIT expectations
def snap_points_to_lines(points, lines):
	end_env = [lines, "END", "0.03 Meters"] # Snap points to the nearest line end node within 0.03m as priority over other vertices
	vertex_env = [lines, "VERTEX", "0.03 Meters"] # Snap points to the nearest line vertex within 0.03m
	edge_env = [lines, "EDGE", "0.03 Meters"] # snap remaining points to the nearest line edge within 0.03m
	ap.Snap_edit(points, [end_env, vertex_env, edge_env])
	ap.Integrate_management([[lines, 1], [points, 2]]) # Integrate points to lines with default domain tolerance to create intersection vertices in the lines without morphing them and creating potential errors.
	ap.RepairGeometry_management(points, "DELETE_NULL")
	ap.RepairGeometry_management(lines, "DELETE_NULL")

def repair_and_clean(name_list):
	write("Repairing {0} and {1} features after Integration".format(name_list[1], name_list[2]))
	ap.RepairGeometry_management(name_list[4], "DELETE_NULL")
	ap.RepairGeometry_management(name_list[5], "DELETE_NULL")
	write("Clearing process cache")
	ap.Delete_management(name_list[3])
	ap.Delete_management(name_list[4])
	ap.Delete_management(name_list[5])
	write("- - - - - - - - - - - - - - - - - - - - - -")



'''
╔═════════════════════════════════════╗
║ Royal Decree & Foundation Functions ║
╚═════════════════════════════════════╝
'''

#----------------------------------------------------------------------
def format_count(count): # format counts with the right amount of spacing for output report
	cnt_str = str(count)
	end_spacing = ""
	if len(cnt_str) > 0:
		for i in range(7-len(cnt_str)):
			end_spacing += " "
	return end_spacing

def format_name(name): # format name with the right amount of spacing for output report
	end_spacing = ''
	for i in range(37-len(name)):
		end_spacing += ' '
	return end_spacing

def royal_decree(ent_fin, gdb_name, tool_names, bool_dict, results, secret, vogon, disable, user):
	# Tool title with GDB name formatting
	write('')
	slines = u'______________________________________'
	sspaces = u'                                      '
	exl = ''
	exs = ''
	exgl = '' # odd left dominant
	exgr = ''
	range_len = 38 - len(gdb_name)
	if range_len > 0:
		if (range_len % 2) == 0:
			rn0 = range_len/2
			for i in range(int(rn0)):
				exgl += ' '
				exgr += ' '
		else:
			rn1 = int(float(range_len)/2)
			for i in range(rn1):
				exgl += ' '
			rn2 = rn1 + 1
			for i in range(int(rn2)):
				exgr += ' '
	if len(gdb_name) > 38:
		extra = len(gdb_name) - 38

		for i in range(extra):
			exl += '_'
			exs += ' '

	if ent_fin == 'Entrance':
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

		if bool_dict[tool_names.repair]:
			write(u"    |     - Repair All NULL Geometries           {0}|".format(exs))
		if bool_dict[tool_names.fcode]:
			write(u"    |     - Populate F_Codes                     {0}|".format(exs))
		if bool_dict[tool_names.defaults]:
			write(u"    |     - Calculate Default Values             {0}|".format(exs))
		if bool_dict[tool_names.metrics]:
			write(u"    |     - Calculate Metrics                    {0}|".format(exs))
		if bool_dict[tool_names.ufi]:
			write(u"    |     - Update UFI Values                    {0}|".format(exs))
		if bool_dict[tool_names.hydro] or bool_dict[tool_names.trans] or bool_dict[tool_names.util]:
			write(u"    |     - Integrate and Repair:                {0}|".format(exs))
			if bool_dict[tool_names.hydro]:
				write(u"    |          Hydro                             {0}|".format(exs))
			if bool_dict[tool_names.trans]:
				write(u"    |          Trans                             {0}|".format(exs))
			if bool_dict[tool_names.util]:
				write(u"    |          Utilities                         {0}|".format(exs))
		if bool_dict[tool_names.dups]:
			write(u"    |     - Delete Identical Features            {0}|".format(exs))
		if bool_dict[tool_names.explode]:
			write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
		if bool_dict[tool_names.bridge]:
			write(u"    |     - Default Bridge WID Updater           {0}|".format(exs))
		if bool_dict[tool_names.pylong]:
			write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
		if bool_dict[tool_names.building]:
			write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
		if bool_dict[tool_names.swap]:
			write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
		if bool_dict[tool_names.fcount]:
			write(u"    |     - Generate Feature Report              {0}|".format(exs))
		if bool_dict[tool_names.vsource]:
			write(u"    |     - Generate Source Report               {0}|".format(exs))

		write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
		write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
		write("\n")

	if ent_fin == 'Finale':
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
		if disable:
			write(u"    |        ~ Editor Tracking DISABLED ~        {0}|".format(exs))
		else:
			write(u"    |   ** Editor Tracking is still ENABLED **   {0}|".format(exs))
		if vogon:
			write(u"    |     - Buildings skipped                    {0}|".format(exs))
		if bool_dict[tool_names.repair]:
			write(u"    |     - Repaired NULL Geometries             {0}|".format(exs))
		if bool_dict[tool_names.fcode]:
			f_fcode_total = format_count(results.fcode_total)
			write(u"    |     - Populated F_Codes                    {0}|".format(exs))
			write(u"    |          {0} F_Code errors fixed       {1}{2}|".format(results.fcode_total, f_fcode_total, exs))
		if bool_dict[tool_names.defaults]:
			write(u"    |     - Calculated Default Values            {0}|".format(exs))
		if bool_dict[tool_names.metrics]:
			write(u"    |     - Calculated Metrics                   {0}|".format(exs))
		if bool_dict[tool_names.ufi]:
			f_ufi_count = format_count(results.ufi_total)
			write(u"    |     - Updated UFI Values                   {0}|".format(exs))
			write(u"    |          {0} Duplicate or blank UFIs   {1}{2}|".format(results.ufi_total, f_ufi_count, exs))
		if bool_dict[tool_names.hydro] or bool_dict[tool_names.trans] or bool_dict[tool_names.util]:
			write(u"    |     - Integrated and Repaired:             {0}|".format(exs))
			if bool_dict[tool_names.hydro]:
				f_hfeat_count = format_count(results.hfeat_total)
				write(u"    |          {0} Hydro                     {1}{2}|".format(results.hfeat_total, f_hfeat_count, exs))
			if bool_dict[tool_names.trans]:
				f_tfeat_count = format_count(results.tfeat_total)
				write(u"    |          {0} Trans                     {1}{2}|".format(results.tfeat_total, f_tfeat_count, exs))
			if bool_dict[tool_names.util]:
				f_ufeat_count = format_count(results.ufeat_total)
				write(u"    |          {0} Utilities                 {1}{2}|".format(results.ufeat_total, f_ufeat_count, exs))
		if bool_dict[tool_names.dups]:
			f_dup_count = format_count(results.dup_total)
			write(u"    |     - Deleted Identical Features           {0}|".format(exs))
			write(u"    |          {0} Duplicates found          {1}{2}|".format(results.dup_total, f_dup_count, exs))
		if bool_dict[tool_names.explode]:
			f_complex_count = format_count(results.complex_total)
			f_multi_count = format_count(results.multi_total)
			write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
			write(u"    |          {0} Complex features found    {1}{2}|".format(results.complex_total, f_complex_count, exs))
			write(u"    |          {0} Features exploded         {1}{2}|".format(results.multi_total, f_multi_count, exs))
		if bool_dict[tool_names.bridge]:
			f_bridge_count = format_count(results.bridge_total)
			f_total_rem_b = format_count(results.remaining_bridge_total)
			write(u"    |     - Default Bridge WID Updater           {0}|".format(exs))
			if bridge_error:
				write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
				write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
			elif no_default_bridge:
				write(u"    |          No default bridges found          {0}|".format(exs))
			else:
				write(u"    |          {0} Bridges updated           {1}{2}|".format(results.bridge_total, f_bridge_count, exs))
				write(u"    |          {0} Defaults not updated      {1}{2}|".format(results.remaining_bridge_total, f_total_rem_b, exs))
				write(u"    |          Check the output for more info    {0}|".format(exs))
		if bool_dict[tool_names.pylong]:
			f_lecount = format_count(results.pylon_total)
			f_total_rem_p = format_count(results.remaining_pylon_total)
			write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
			if pylon_error:
				write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
				write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
			elif no_default_pylon:
				write(u"    |          No default pylons found           {0}|".format(exs))
			else:
				write(u"    |          {0} Pylons updated            {1}{2}|".format(results.pylon_total, f_lecount, exs))
				write(u"    |          {0} Defaults not updated      {1}{2}|".format(results.remaining_pylon_total, f_total_rem_p, exs))
				write(u"    |          Check the output for more info    {0}|".format(exs))
		if bool_dict[tool_names.building]:
			f_total_non = format_count(results.nonimportant_ffn_total)
			write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
			if building_error:
				write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
				write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
			elif no_bua:
				write(u"    |          No BUAs found                     {0}|".format(exs))
			elif no_bua_buildings:
				write(u"    |          No un-important buildings found   {0}|".format(exs))
			else:
				write(u"    |          {0} Buildings descaled        {1}{2}|".format(results.nonimportant_ffn_total, f_total_non, exs))
				write(u"    |          Check the output for more info    {0}|".format(exs))
		if bool_dict[tool_names.swap]:
			write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
		if bool_dict[tool_names.fcount]:
			f_pnt_cnt = format_count(results.point_total)
			f_crv_cnt = format_count(results.curve_total)
			f_srf_cnt = format_count(results.surface_total)
			f_tots_f = format_count(results.all_feats_total)
			f_hydro_cnt = format_count(results.hydro_total)
			f_trans_cnt = format_count(results.trans_total)
			f_building_cnt = format_count(results.building_total)
			f_landcover_cnt = format_count(results.landcover_total)
			write(u"    |     - Feature report generated             {0}|".format(exs))
			write(u"    |          {0} Point Features            {1}{2}|".format(results.point_total, f_pnt_cnt, exs))
			write(u"    |          {0} Curve Features            {1}{2}|".format(results.curve_total, f_crv_cnt, exs))
			write(u"    |          {0} Surface Features          {1}{2}|".format(results.surface_total, f_srf_cnt, exs))
			write(u"    |          {0} Total Features            {1}{2}|".format(results.all_feats_total, f_tots_f, exs))
			write(u"    |          {0} Hydrography Features      {1}{2}|".format(results.hydro_total, f_hydro_cnt, exs))
			write(u"    |          {0} Transportation Features   {1}{2}|".format(results.trans_total, f_trans_cnt, exs))
			write(u"    |          {0} Buildings                 {1}{2}|".format(results.building_total, f_building_cnt, exs))
			write(u"    |          {0} Landcover Surfaces        {1}{2}|".format(results.landcover_total, f_landcover_cnt, exs))
			write(u"    |          Check the output for more info    {0}|".format(exs))
		if bool_dict[tool_names.vsource]:
			write(u"    |     - Source report generated              {0}|".format(exs))
			write(u"    |          Check the output for more info    {0}|".format(exs))

		# Easter Egg
		if not bool_dict[tool_names.repair] and not bool_dict[tool_names.fcode] and not bool_dict[tool_names.defaults] and not bool_dict[tool_names.metrics] and not bool_dict[tool_names.ufi] and not bool_dict[tool_names.hydro] and not bool_dict[tool_names.trans] and not bool_dict[tool_names.util] and not bool_dict[tool_names.dups] and not bool_dict[tool_names.explode] and not bool_dict[tool_names.bridge] and not bool_dict[tool_names.pylong] and not bool_dict[tool_names.building] and not bool_dict[tool_names.swap] and not bool_dict[tool_names.fcount] and not bool_dict[tool_names.vsource]:
			f_user = format_count(user)
			write(u"    |   {0}   {1}|".format(sspaces, exs))
			write(u"    |       {0}, click a check box and       {1}{0}|".format(user, f_user, exs))
			write(u"    |             stop being cheeky.             {0}|".format(exs))

		write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
		write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
		write("\n")

def background_music(start_stop):
	if start_stop == 'start':
		with open('tmp.vbs', 'w') as vbs_script:
			vbs_script.write(r'CreateObject("Wscript.Shell").Run "wmplayer /play /close ""C:\Users\njcagle\Downloads\WANGAN_RUN_Synthwave_Mix.mp3""", 0, False')

		subprocess.call('cscript tmp.vbs')
		if os.path.exists('tmp.vbs'):
			os.remove('tmp.vbs')

	if start_stop == 'stop':
		os.system("taskkill /im wmplayer.exe /t /f")

#----------------------------------------------------------------------
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



      '''.          ,~~.          ,~~.          ,~~.          ,~~.
     (  6 )-_,     (  6 )-_,     (  6 )-_,     (  6 )-_,     (  6 )-_,
(\___ )=='-'  (\___ )=='-'  (\___ )=='-'  (\___ )=='-'  (\___ )=='-'
 \ .   ) )     \ .   ) )     \ .   ) )     \ .   ) )     \ .   ) )
  \ `-' /       \ `-' /       \ `-' /       \ `-' /       \ `-' /
 ~'`~'`~'`~`~'`~'`~'`~'`~`~'`~'`~'`~'`~`~'`~'`~'`~'`~'`~`~'`~'`~'`~'`~
              ..........................................
			  :       ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄        :
      ,~~.    :       █ ╔══════════════════╗= █        :      ,~~.
     (  9 )-_,:       █ ║ >>> execute(     ║  █        :     (  9 )-_,
(\___ )=='-'  :       █ ║     __main__     ║  █        :(\___ )=='-'
 \ .   ) )    :       █ ║     )            ║o █        : \ .   ) )
  \ `-' /     :       █ ╚══════════════════╝o █        :  \ `-' /
 ~'`~'`~'`~`~ :       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀        : ~'`~'`~'`~'`~
              :........................................:
      ,~~.          ,~~.          ,~~.          ,~~.          ,~~.
     (  6 )-_,     (  6 )-_,     (  6 )-_,     (  6 )-_,     (  6 )-_,
(\___ )=='-'  (\___ )=='-'  (\___ )=='-'  (\___ )=='-'  (\___ )=='-'
 \ .   ) )     \ .   ) )     \ .   ) )     \ .   ) )     \ .   ) )
  \ `-' /       \ `-' /       \ `-' /       \ `-' /       \ `-' /
 ~'`~'`~'`~`~'`~'`~'`~'`~`~'`~'`~'`~'`~`~'`~'`~'`~'`~`~'`~'`~'`~'`~'''

# WIP



'''
╔════════════════════════════╗
║ Grand Entrance & Foundation║
╚════════════════════════════╝
'''

# Sanitizing GDB name
gdb_name = re.findall(r"[\w']+", os.path.basename(os.path.split(TDS)[0]))[0]
gdb_folder = os.path.split(os.path.split(TDS)[0])[0]

royal_decree('Entrance', gdb_name, bool_dict, results, secret, vogon, disable, user)
background_music('start')
featureclass = create_fc_list(vogon)
caci_schema = snowflake_protocol(featureclass)
if disable:
	disable_editor_tracking(featureclass, gdb_name)
check_defense('out', defaults, metrics, explode)
where_scale = "zi026_ctuu >= 50000" #### Add option to specify what scale and up to run the tool on.



'''
╔═════════════════╗
║ Tool Executions ║
╚═════════════════╝
'''

	if bool_dict[tool_names.repair]:
		tool_function()
	if bool_dict[tool_names.fcode]:
		tool_function()
	if bool_dict[tool_names.defaults]:
		tool_function()
	if bool_dict[tool_names.metrics]:
		tool_function()
	if bool_dict[tool_names.ufi]:
		tool_function()
	if bool_dict[tool_names.hydro]:
		tool_function()
	if bool_dict[tool_names.trans]:
		tool_function()
	if bool_dict[tool_names.util]:
		tool_function()
	if bool_dict[tool_names.dups]:
		tool_function()
	if bool_dict[tool_names.explode]:
		tool_function()
	if bool_dict[tool_names.bridge]:
		tool_function()
	if bool_dict[tool_names.pylong]:
		tool_function()
	if bool_dict[tool_names.building]:
		tool_function()
	if bool_dict[tool_names.swap]:
		tool_function()
	if bool_dict[tool_names.fcount]:
		tool_function()
	if bool_dict[tool_names.vsource]:
		tool_function()



'''
╔════════════════════════╗
║ Grand Finale & Wrap Up ║
╚════════════════════════╝
'''

check_defense('in', defaults, metrics, explode)
royal_decree('Finale', gdb_name, tool_names, bool_dict, results, secret, vogon, disable, user)
background_music('stop')











# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Data Maintenance Tools Category   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
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
	#ap.RepairBadGeometry_production(featureclass, 'REPAIR_ONLY', 'DELETE_NULL_GEOMETRY', '#') # Repair Bad Geometry Production Mapping tool
	repair_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(repair_start, repair_finish)))
	break

#----------------------------------------------------------------------
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

#----------------------------------------------------------------------
''''''''' Calculate Default Values '''''''''
#### make 50k+ restriction in function
# Calculate default values for NULL attributes
# All or nothing. Functions on datasets not individual feature classes
#### rewrite using domains and coded values thru cursors
while defaults:
	defaults_start = dt.now()
	tool_name = 'Calculate Default Values'
	write("\n--- {0} ---\n".format(tool_name))
	process_defaults(featureclass)
	defaults_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(defaults_start, defaults_finish)))
	break

#default2 finished in 0:01:25.0860
#Calculate Default Values finished in 0:01:18.5650

#----------------------------------------------------------------------
''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
## Only run on Polygon ARA and Polyline LZN
#### Defense mapping version takes too long and crashes. just rewrite with manual calculations
#### See if Kristen wants to work on it
#### for line and polygon metrics, if area or length is tool small throw warning with output.
while metrics:
	metrics_start = dt.now()
	tool_name = 'Calculate Metrics'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			if get_count(fc) == 0:
				continue
			shape_type = ap.Describe(fc).shapeType # Polygon, Polyline, Point, Multipoint, MultiPatch
			if shape_type == 'Polyline':
				write("Calculating Length field for {0}".format(fc))
				ap.CalculateMetrics_defense(fc, 'LENGTH', "LZN", "#", "#", "#", "#", "#")
			elif shape_type == 'Polygon':
				write("Calculating Area field for {0}".format(fc))
				ap.CalculateMetrics_defense(fc, 'AREA', "#", "#", "ARA", "#", "#", "#")
		except ap.ExecuteError:
			writeresults(tool_name)
	metrics_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(metrics_start, metrics_finish)))
	break

#Calculate Metrics finished in 0:02:28.6500

#----------------------------------------------------------------------
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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Integration Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Integrate and Repair '''''''''
## Removed layered integration and dropped tolerance to 0.02m
## Moved Integrate Large Datasets option to backend. It is now default since it runs faster regardless.
#### Add integration of hydro VanishingPoints and NaturalPools
#### Major rework of logic behind integrate step.
#### Potentially do away with Integrate and make a few tools that just do the major things we need integrate to do
####   - Run snap tool with low tolerance for helping keep certain features coincident.
####   - Decrease the integrate tolerance to 0.02m. We used 0.03m for a while, but for older clients, we used to use 0.01m. So this splits the difference and should cut down on the duplicate vertices errors.
# User choice to Integrate and Repair Hydrography curves, TransportationGround curves, or Utility points and surfaces to curves
if hydro or trans or util:
	tool_name = 'Integrate and Repair'
	write("\n--- {0} ---\n".format(tool_name))
while hydro:
	hydro_start = dt.now()
	tool_name = 'Integrate Hydrography Features'
	hydro_list = ['HydrographyPnt', 'HydrographyCrv', 'HydrographySrf', 'hydro_pnt', 'hydro_crv', 'hydro_srf']
	hydro_pnt = hydro_list[3]
	hydro_crv = hydro_list[4]
	hydro_srf = hydro_list[5]
	make_integrate_layers(hydro_list, tool_name)
	hfeat_total = 0

	try:
		#Create Fishnet
		write("Processing large feature class. Partitioning data in chunks to process.")
		mem_fc = "in_memory\\{0}_grid".format(hydro_list[1])
		rectangle = "in_memory\\rectangle"
		write("Defining partition envelope")
		arcpy.CopyFeatures_management(arcpy.env.extent.polygon, rectangle)
		# if ap.MinimumBoundingGeometry_management(hydro_list[1], rectangle, "RECTANGLE_BY_AREA", "ALL", "", "").maxSeverity:
		# 	write("No curve features found. Nothing to Integrate. Moving to the next tool.")
		# 	break
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
				hfeat_total = hfeat_total + pnt_count + crv_count + srf_count
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
		ap.Delete_management(rectangle)
	except ap.ExecuteError:
		writeresults(tool_name)

	repair_and_clean(hydro_list)
	hydro_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(hydro_start, hydro_finish)))
	break

# Hydrography Curves finished in 0:02:44.5230
while trans:
	trans_start = dt.now()
	tool_name = 'Integrate Transportation Features'
	trans_list = ['TransportationGroundPnt', 'TransportationGroundCrv', 'TransportationGroundSrf', 'trans_pnt', 'trans_crv', 'trans_srf']
	trans_pnt = trans_list[3]
	trans_crv = trans_list[4]
	trans_srf = trans_list[5]
	make_integrate_layers(trans_list, tool_name)
	tfeat_total = 0

	try:
		#Create Fishnet
		write("Processing large feature class. Partitioning data in chunks to process.")
		mem_fc = "in_memory\\{0}_grid".format(trans_list[1])
		rectangle = "in_memory\\rectangle"
		write("Defining partition envelope")
		arcpy.CopyFeatures_management(arcpy.env.extent.polygon, rectangle)
		# if ap.MinimumBoundingGeometry_management(trans_list[1], rectangle, "RECTANGLE_BY_AREA", "ALL", "", "").maxSeverity:
		# 	write("No curve features found. Nothing to Integrate. Moving to the next tool.")
		# 	break
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
				tfeat_total = tfeat_total + pnt_count + crv_count + srf_count
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
		ap.Delete_management(rectangle)
	except ap.ExecuteError:
		writeresults(tool_name)

	repair_and_clean(trans_list)
	trans_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(trans_start, trans_finish)))
	break

while util:
	util_start = dt.now()
	tool_name = 'Inegrate Utility Features'
	util_list = ['UtilityInfrastructurePnt', 'UtilityInfrastructureCrv', 'UtilityInfrastructureSrf', 'util_pnt', 'util_crv', 'util_srf']
	util_pnt = util_list[3]
	util_crv = util_list[4]
	util_srf = util_list[5]
	make_integrate_layers(util_list, tool_name)
	ufeat_total = 0

	try:
		#Create Fishnet
		write("Processing large feature class. Partitioning data in chunks to process.")
		mem_fc = "in_memory\\{0}_grid".format(util_list[1])
		rectangle = "in_memory\\rectangle"
		write("Defining partition envelope")
		arcpy.CopyFeatures_management(arcpy.env.extent.polygon, rectangle)
		# if ap.MinimumBoundingGeometry_management(hydro_list[1], rectangle, "RECTANGLE_BY_AREA", "ALL", "", "").maxSeverity:
		# 	write("No curve features found. Nothing to Integrate. Moving to the next tool.")
		# 	break
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
				ufeat_total = ufeat_total + pnt_count + crv_count + srf_count
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
		ap.Delete_management(rectangle)
	except ap.ExecuteError:
		writeresults(tool_name)

	repair_and_clean(util_list)
	util_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(util_start, util_finish)))
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Geometry Correction Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Delete Identical Features '''''''''
# Checks for features with identical geometry and PSG attribution and removes them
#### Test rewritten find identical code and replace existing
while dups:
	dups_start = dt.now()
	tool_name = 'Delete Identical Features'
	write("\n--- {0} ---\n".format(tool_name))
	out_table = os.path.dirname(TDS) # Output directory for Find Identical # C:/Projects/njcagle/S1_C09C_20210427.gdb
	path = os.path.join(gdb_folder, gdb_name) # Output dBASE table location # C:/Projects/njcagle/S1_C09C_20210427
	table_loc = "{0}.dbf".format(path) # C:/Projects/njcagle/R&D/__Thunderdome/S1_C09C_20210427.dbf
	write("Creating temporary output files:\n    - {0}.dbf\n    - {0}.dbf.xml\n    - {0}.cpg\n    - {0}.IN_FID.atx".format(gdb_name))
	dup_total = 0

	for fc in featureclass: # Loop feature classes and FindIdentical to get a count, then delete any found
		try:
			dick = ad.fc_fields_og[fc] # Does not include metric fields. Uses 'Shape' instead of 'SHAPE@' #dict_import
			ap.FindIdentical_management(fc, out_table, dick, "", "", output_record_option="ONLY_DUPLICATES")
			rows = get_count("{0}.dbf".format(path))
			write("Searching for duplicate features in {0}...".format(fc))
			if rows > 0:
				ap.DeleteIdentical_management(fc, dick)
				write("  - Deleted {0} duplicate features.".format(rows))
				dup_total += rows
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
	write("{0} removed {1} duplicates in {2}".format(tool_name, dup_total, runtime(dups_start, dups_finish)))
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

#----------------------------------------------------------------------
''''''''' Hypernova Burst Multipart Features '''''''''
## Added 50k+ restriction
# Explodes multipart features for an entire dataset
while explode:
	explode_start = dt.now()
	tool_name = 'Hypernova Burst Multipart Features'
	write("\n--- {0} ---\n".format(tool_name))

	##### Multipart Search #####
	fc_multi = OrderedDict() # Create empty dictionary for lists of mulitpart feature OIDs for each feature class that has multiparts
	fc_multi_list = []
	multi_total = 0
	complex_total = 0
	og_oid = 'og_oid'
	multi_search_fields = ['og_oid', 'OID@', 'SHAPE@']
	for fc in featureclass:
		try:
			if get_count(fc) == 0: # Skip empty feature classes
				continue
			multi_count = 0
			fc_multi[fc] = []
			write("Searching for multipart features in {0}".format(fc))
			dsc = ap.Describe(fc)
			fc_type = dsc.shapeType # Polygon, Polyline, Point, Multipoint, MultiPatch
			ap.AddField_management(fc, og_oid, "long")
			with ap.da.UpdateCursor(fc, multi_search_fields, where_scale) as ucursor:
				if fc_type == 'Polygon':
					complex_count = 0 # Counts complex single part features
					for urow in ucursor: # For each feature in the fc
						shape = urow[-1] # Get SHAPE@ token to extract properties
						oid = urow[-2]
						if is_null(shape): # Checks for NULL geometries
							write(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
							continue
						if shape.isMultipart: # Does the feature have the isMultipart flag
							if shape.partCount > 1: # If the number of geometric parts is more than one, then it is a true multipart feature
								multi_count += 1
								fc_multi[fc].append(oid) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
								urow[-3] = oid
								ucursor.updateRow(urow)
							else: # If the part count is not greater than 1, then it is a complex single part feature with interior rings
								complex_count += 1
					if complex_count > 0:
						complex_total += complex_count
						write("    {0} complex polygons found".format(complex_count))
				else:
					for urow in ucursor: # For each feature in the fc
						shape = urow[-1] # Get SHAPE@ token to extract properties
						oid = urow[-2]
						if is_null(shape): # Checks for NULL geometries
							write(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
							continue
						if shape.isMultipart: # Does the feature have the isMultipart flag
							multi_count += 1
							fc_multi[fc].append(oid) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
							urow[-3] = oid # Non-polygon feature geometries do not have the isMultipart flaw since they have fewer dimensions. Simply proceed as normal
							ucursor.updateRow(urow)
			if multi_count > 0:
				multi_total += multi_count
				write("\n    *** {0} true multipart features found! ***".format(multi_count))
				##### Isolate, Explode, Replace #####
				in_class = "multi"
				out_class = "single"
				oid_query = """{0} IS NOT NULL""".format(field_delim(fc, og_oid))
				# Create a new feature class to put the multipart features in to decrease processing time. fields based on original fc template
				ap.CreateFeatureclass_management(TDS, in_class, fc_type, fc, "", "", TDS)
				field_list = make_field_list(dsc)
				field_list.append(og_oid)

				# Add multipart features to new feature class based on OID
				with ap.da.SearchCursor(fc, field_list, oid_query) as scursor: # Search current fc using for only non-NULL OIDs flagged as multipart
					with ap.da.InsertCursor(in_class, field_list) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
						for srow in scursor:
							icursor.insertRow(srow) # Insert that feature row into the temp feature class, in_class "multi"

				write("    {0} multipart progenitor cores collapsing.".format(fc))
				multistart = dt.now()
				ap.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
				multifinish = dt.now()
				write("    Hypernova burst detected after {0} seconds.".format(runtime(multistart, multifinish)))

				write("    Updating UFIs for new single part features.")
				with ap.da.UpdateCursor(out_class, 'ufi') as ucursor: # Populate the ufi for the newly created singlepart features
					for urow in ucursor:
						urow[0] = str(uuid.uuid4())
						ucursor.updateRow(urow)

				write("    Populating NULL fields.")
				out_fields = ['shape', 'area', 'length', 'created', 'edited', 'f_code', 'fcsubtype', 'ufi', 'version']
				in_types = ['Double', 'Integer', 'Single', 'SmallInteger']
				string_fields = [field.name for field in ap.ListFields(out_class, None, 'String') if not any(substring in field.name.lower() for substring in out_fields if substring)]
				number_fields = [field.name for field in ap.ListFields(out_class) if field.type in in_types and not any(substring in field.name.lower() for substring in out_fields if substring)]
				string_fields.sort()
				number_fields.sort()
				fc_nulls = 0
				fc_nulls += populate_null(out_class, string_fields, 'noInformation')
				fc_nulls += populate_null(out_class, number_fields, -999999)
				write("    {0} NULL fields populated with default values".format(fc_nulls))

				write("    Removing original multipart features.")
				with ap.da.UpdateCursor(fc, og_oid, oid_query) as ucursor: # Deletes features in fc that have OIDs flagged as multiparts from the oid_list
					for urow in ucursor:
						ucursor.deleteRow()

				write("    Replacing with singlepart features.")
				with ap.da.SearchCursor(out_class, field_list) as scursor: # Insert new rows in fc from MultipartToSinglepart output out_class
					with ap.da.InsertCursor(fc, field_list) as icursor:
						for srow in scursor:
							icursor.insertRow(srow)

				try:
					ap.Delete_management(in_class)
					ap.Delete_management(out_class)
					write("    Cleared temp fields and intermediate feature classes\n")
				except:
					write("    No in_class or out_class created. Or processing layers have already been cleaned up. Continuing...\n")
					pass
			else:
				del fc_multi[fc]
			ap.DeleteField_management(fc, og_oid)
		except ap.ExecuteError:
			writeresults(tool_name)
	write(" ")
	if complex_total > 0:
		write("The {0} complex polygons found are singlepart polygons with complex interior holes that are more likely to become multipart features.".format(complex_total))
	write(" ")
	if multi_total > 0: # Only runs if fc_multi is not empty
		for key in fc_multi:
			write("{0} multipart features found in {1}".format(len(fc_multi[key]), key))
			write("  OIDs - {0}".format(fc_multi[key]))
		write(" ")
		write("All multipart feature have acheived supernova!")


	##### Isolate, Explode, Replace #####
	# in_class = "multi"
	# out_class = "single"
	# for fc in fc_multi_list:
	# 	try:
	# 		#sanitize feature class name from sde cz the sde always has to make things more difficult than they need to be...
	# 		fc_parts = fc.split(".")
	# 		if fc_parts[-1] in ad.fc_fields:  #dict_import
	# 			fcr = fc_parts[-1]
	# 		else:
	# 			write("Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin.")
	#
	# 		# Variables
	# 		oid_list = fc_multi[fc]
	# 		og_oid = "oidid"
	# 		fc_geom = ap.Describe(fc).shapeType
	# 		oid_field = ap.Describe(fc).OIDFieldName # Get the OID field name. Not necessary for every loop, but simple enough to just put here.
	# 		# Adds a field to the current fc that stores the original OID for identification after exploding.
	# 		ap.AddField_management(fc, og_oid, "double")
	# 		with ap.da.UpdateCursor(fc, [oid_field, og_oid]) as ucursor:
	# 			for row in ucursor:
	# 				if row[0] in oid_list:
	# 					row[1] = row[0]
	# 					ucursor.updateRow(row)
	# 		#ap.CalculateField_management(fc, og_oid, "!" + oid_field + "!", "PYTHON")
	# 		fieldnames = ad.fc_fields[fcr]  #dict_import
	# 		fieldnames.insert(0, og_oid)
	# 		fieldnames.insert(0, oid_field)
	# 		oid_list_str = str(fc_multi[fc]) # Convert the list to a string and remove the []
	# 		oid_list_str = oid_list_str[1:-1]
	# 		query = "{0} in ({1})".format(oid_field, oid_list_str) # Formats the query from the above variables as: OBJECTID in (1, 2, 3)
	#
	# 		# Create a new feature class to put the multipart features in to decrease processing time. fields based on original fc template
	# 		ap.CreateFeatureclass_management(ap.env.workspace, in_class, fc_geom, fc, "", "", ap.env.workspace)
	#
	# 		# Add multipart features to new feature class based on OID
	# 		with ap.da.SearchCursor(fc, fieldnames, query) as scursor: # Search current fc using fc_fields with OID@ and "oidid" prepended as [0,1] respectively. Queries for only OIDs in the multipart oid_list.
	# 			with ap.da.InsertCursor(in_class, fieldnames) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
	# 				for row in scursor: # For each feature in the current fc
	# 					if row[0] in oid_list: # If the OID is in the oid_list of multipart features. Redundant since the scursor is queried for multipart OIDs, but meh
	# 						icursor.insertRow(row) # Insert that feature row into the temp feature class, in_class "multi"
	#
	# 		write("{0} multipart progenitor cores collapsing.".format(fcr))
	# 		multistart = dt.now()
	# 		ap.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
	# 		multifinish = dt.now()
	# 		write("Hypernova burst detected after {0} seconds.".format(runtime(multistart, multifinish)))
	#
	# 		write("Removing original multipart features.")
	# 		# Deletes features in fc that have OIDs flagged as multiparts
	# 		with ap.da.UpdateCursor(fc, oid_field) as ucursor:
	# 			for row in ucursor:
	# 				if row[0] in oid_list:
	# 					ucursor.deleteRow()
	#
	# 		write("Replacing with singlepart features.")
	# 		# Create search and insert cursor to insert new rows in fc from MultipartToSinglepart output out_class
	# 		with ap.da.SearchCursor(out_class, fieldnames) as scursor:
	# 			with ap.da.InsertCursor(fc, fieldnames) as icursor:
	# 				for row in scursor:
	# 					icursor.insertRow(row)
	#
	# 		write("Populating NULL fields with defaults and updating UFIs for the new single part features.")
	# 		query2 = "{0} IS NOT NULL".format(og_oid)
	# 		ap.MakeFeatureLayer_management(fc, "curr_fc", query2)
	# 		ap.CalculateDefaultValues_defense("curr_fc")
	# 		write("NULL fields populated with default values")
	# 		with ap.da.UpdateCursor(fc, 'ufi', query2) as ucursor:
	# 			for row in ucursor:
	# 				row[0] = str(uuid.uuid4())
	# 				ucursor.updateRow(row)
	# 		ap.DeleteField_management(fc, og_oid)
	# 		write("UFI values updated")
	# 		write(" ")
	#
	# 	except ap.ExecuteError:
	# 		writeresults(tool_name)
	#
	# if fc_multi_list:
	# 	write("All multipart feature have acheived supernova!")
	#
	# try:
	# 	ap.Delete_management(str(ap.env.workspace) + str("\\" + str(in_class)))
	# 	ap.Delete_management(str(ap.env.workspace) + str("\\" + str(out_class)))
	# 	ap.Delete_management("curr_fc")
	# except:
	# 	write("No in_class or out_class created. Or processing layers have already been cleaned up. Continuing...")
	# 	pass
	explode_finish = dt.now()
	write("{0} exploded {1} features in {2}".format(tool_name, total_multi, runtime(explode_start, explode_finish)))
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Preprocessing Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Default Bridge WID Updater '''''''''
## Added 50k+ restriction
# Checks for bridges with default WID (-999999) and updates them to match the underlying road or rail WID
while bridge:
	bridge_error = False
	no_default_bridge = False
	bridge_total = 0
	remaining_bridge_total = 0
	tool_name = 'Default Bridge WID Updater'
	write("\n--- {0} ---\n".format(tool_name))
	if not ap.Exists('TransportationGroundCrv'):
		write("TransportationGroundCrv feature class missing./nCannot run Default Bridge WID Updater.")
		bridge_error = True
		break
	break

while bridge: # Needs updating from management geoprocessing to cursors
	bridge_start = dt.now()
	if bridge_error:
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
		no_default_bridge = True
		bridge_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(bridge_start, bridge_finish)))
		break
	# Error handling. If no roads or rails to select against, likely something will break.
	if total_roads == 0 and total_rails == 0:
		write("{0} default WID bridges found.".format(total_bridges))
		write("No underlying roads or rails for default bridges. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.")
		bridge_error = True
		bridge_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(bridge_start, bridge_finish)))
		break

	# Announces the total default bridges found.
	write("{0} default WID bridges found.".format(total_bridges))

	# Start an edit session. Must provide the workspace.
	edit = ap.da.Editor(os.path.dirname(TDS))
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
	remaining_bridge_total = int(ap.management.GetCount("bridges_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	bridge_total = (countR + countRR) - remaining_bridge_total
	write("Updated {0} bridges with new WID values.".format(bridge_total))
	if remaining_bridge_total > 0:
		write("{0} bridges still have default WID. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.".format(remaining_bridge_total))
	bridge_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(bridge_start, bridge_finish)))
	break

#----------------------------------------------------------------------
''''''''' Default Pylon HGT Updater '''''''''
## Added 50k+ restriction
# Checks for pylons with default HGT (-999999) and updates them to match the intersecting cable HGT
while pylong:
	pylon_error = False
	no_default_pylon = False
	pylon_total = 0
	remaining_pylon_total = 0
	tool_name = 'Default Pylon HGT Updater'
	write("\n--- {0} ---\n".format(tool_name))
	if not ap.Exists('UtilityInfrastructurePnt') or not ap.Exists('UtilityInfrastructureCrv'):
		write("UtilityInfrastructurePnt or UtilityInfrastructureCrv feature classes missing./nCannot run Default Pylon HGT Updater.")
		pylon_error = True
		break
	break

while pylong: # Needs updating from management geoprocessing to cursors
	pylong_start = dt.now()
	if pylon_error:
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
		no_default_pylon = True
		pylong_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(pylong_start, pylong_finish)))
		break
	# Error handling. If no cables to select against, likely something will break.
	if total_cables == 0:
		write("{0} default value pylons found.".format(total_pylons))
		write("No intersecting cables for default pylons. \n Try running Integrate and Repair then try again. \n The default pylons are either not snapped or missing a cable.")
		pylon_error = True
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
			pylon_total += 1

	# Select any remaining pylons with default (-999999) height
	ap.SelectLayerByAttribute_management("fc_pylon", "NEW_SELECTION", "F_CODE = 'AT042' AND zi026_ctuu >= 50000")
	ap.SelectLayerByAttribute_management("fc_pylon", "SUBSET_SELECTION", "HGT = -999999")
	# Make these selections into a new layer and get a count
	ap.MakeFeatureLayer_management("fc_pylon", "pylons_rem")
	remaining_pylon_total = int(ap.management.GetCount("pylons_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	pylon_total = pylon_total - remaining_pylon_total
	write("Updated {0} pylons with new HGT values.".format(pylon_total))
	write("{0} pylons still have default HGT. \n Consider running Integrate and Repair before trying again. \n The remaining pylons are not snapped, missing a cable, or the underlying cable doesn't have a height.".format(remaining_pylon_total))
	pylong_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(pylong_start, pylong_finish)))
	break

#----------------------------------------------------------------------
''''''''' Building in BUA Descaler '''''''''
# Descales buildings within BUAs that don't have important FFNs
while building:
	building_error = False
	no_bua = False
	no_bua_buildings = False
	nonimportant_ffn_total = 0
	tool_name = 'Building in BUA Descaler'
	write("\n--- {0} ---\n".format(tool_name))
	if not ap.Exists('SettlementSrf'):
		write("SettlementSrf feature class missing./nCannot run Building in BUA Descaler.")
		building_error = True
		break
	if not ap.Exists('StructureSrf') and not ap.Exists('StructurePnt'):
		write("StructureSrf and StructurePnt feature classes missing./nCannot run Building in BUA Descaler.")
		building_error = True
		break
	break

while building: # Needs updating from management geoprocessing to cursors
	building_start = dt.now()
	if building_error:
		break
	# Make initial layers from the workspace
	srf_exist = False
	pnt_exist = False
	import_ffn_s = 0
	import_ffn_p = 0
	non_import_count_s = 0
	non_import_count_p = 0
	fields = 'ZI026_CTUU'
	caci_query = "FFN IN ({0})".format(", ".join(str(i) for i in ffn_list_caci.values())) #dict_import
	other_query = "FFN IN ({0})".format(", ".join(str(i) for i in ffn_list_all.values())) #dict_import

	if caci_schema:
		write("CACI specific important building FFNs list:")
		write("\n".join("{}: {}".format(k, v) for k, v in ffn_list_caci.items())) #dict_import
	else:
		write("Current project important building FFNs list:")
		write("\n".join("{}: {}".format(k, v) for k, v in ffn_list_all.items())) #dict_import

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
	nonimportant_ffn_total = non_import_count_s + non_import_count_p

	# End script if there are no BUAs or no buildings inside them
	if bua_count == 0:
		write("\nNo BUAs found.")
		no_bua = True
		building_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
		break
	if nonimportant_ffn_total == 0:
		write("\nNo buildings without important FFNs found in BUAs.")
		no_bua_buildings = True
		building_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
		break

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
	building_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
	break

#----------------------------------------------------------------------
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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Database Management Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Database Feature Report '''''''''
# Refactored from John Jackson's Feature_Itemized_Counter.py by Nat Cagle
while fcount:
	tool_name = 'Database Feature Report'
	write("\n--- {0} ---\n".format(tool_name))
	# Define counters for shape feature counts and total feature count
	point_total = 0
	curve_total = 0
	surface_total = 0
	all_feats_total = 0
	hydro_total = 0
	trans_total = 0
	building_total = 0
	landcover_total = 0
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
	results = "{0}\\{1}_Feature_Report_{2}.txt".format(gdb_folder, gdb_name, time_stamp)
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
					if fcsub_dict[int(j[0])] not in feat_dict[currFC][0]: #dict_import
						feat_dict[str(i)][0][fcsub_dict[int(j[0])]] = 1 #dict_import
					else:
						feat_dict[currFC][0][fcsub_dict[int(j[0])]] += 1 #dict_import
					# Count Feature Class total features
					feat_dict[currFC][1] += 1
					# Count Database total features
					all_feats_total += 1
					# Counting based on shape type
					if currShape == 'Srf':
						surface_total += 1
						if any(int(substring) == int(curr_sub) for substring in landcover_list):
							landcover_total += 1
					elif currShape == 'Crv':
						curve_total += 1
					else:
						point_total += 1
					# Counting specific categories
					if int(curr_sub) == int(building_sub):
						building_total += 1
					if hydro_feat:
						hydro_total += 1
					if trans_feat:
						trans_total += 1

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
		txt_file.writelines(["Point Features  :  ",str(point_total),"\n",
							"Curve Features  :  ",str(curve_total),"\n",
							"Surface Features:  ",str(surface_total),"\n",
							"Total Features  :  ",str(all_feats_total),"\n\n",
							"Total Hydrography Features        :  ",str(hydro_total),"\n",
							"Total Transportation Features     :  ",str(trans_total),"\n",
							"Total Building Surfaces and Points:  ",str(building_total),"\n",
							"Total Landcover Surfaces          :  ",str(landcover_total),"\n\n\n"])
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

#----------------------------------------------------------------------
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
	results_csv = "{0}\\{1}_Source_Count_{2}.csv".format(gdb_folder, gdb_name, time_stamp)
	results_txt = "{0}\\{1}_Source_Count_{2}.txt".format(gdb_folder, gdb_name, time_stamp)
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

	write("Source Analysis Report created. File located in database folder:\n{0}".format(gdb_folder))
	vsource_finish = dt.now()
	write("{0} finished in {1}".format(tool_name, runtime(vsource_start, vsource_finish)))
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Report Formatting and Wrap Up #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
check_defense('in', defaults, metrics, explode)
royal_decree('Finale', gdb_name, tool_names, bool_dict, results, secret, vogon, disable, user)
background_music('stop')







# def main(*argv):
# 	# Parameters
# 	TDS = argv[0]
# 	ap.env.workspace = TDS
# 	workspace = os.path.dirname(ap.env.workspace)
# 	bool_dict = {
# 		'vogon': bool(argv[1]), # Skips large building datasets
# 		'repair': bool(argv[2]),
# 		'fcode': bool(argv[3]),
# 		'defaults': bool(argv[4]),
# 		'metrics': bool(argv[5]),
# 		'ufi': bool(argv[6]),
# 		'large': bool(argv[7]), # Running chunk processing for integrating large datasets
# 		'hydro': bool(argv[8]),
# 		'trans': bool(argv[9]),
# 		'util': bool(argv[10]),
# 		'dups': bool(argv[11]),
# 		'explode': bool(argv[12]),
# 		'bridge': bool(argv[13]),
# 		'pylong': bool(argv[14]),
# 		'building': bool(argv[15]), # Be sure to add Structure Srf and Pnt back if vogon is checked
# 		'swap': bool(argv[16]),
# 		'fcount': bool(argv[17]),
# 		'vsource': bool(argv[18]),
# 		'secret': bool(argv[19]) ### update index as needed
# 	}
#
# 	error_count = 0
# 	featureclass = ap.ListFeatureClasses()
#
# 	grand_entrance(TDS, bool_dict)
#
# 	check_out_defense(bool_dict)
#
# 	if bool_dict['hydro'] or bool_dict['trans'] or bool_dict['util']:
# 		tool_name = 'Integrate and Repair'
# 		write("\n--- {0} ---\n".format(tool_name))
# 		# add conditional and function calls for hydro, trans, and util
#
#
# if __name__=='__main__':
# 	ap.env.overwriteOutput = True
# 	argv = tuple(ap.GetParameterAsText(i) for i in range(ap.GetArgumentCount()))
# 	now = dt.datetime.now()
# 	main(*argv)
# 	write(dt.datetime.now() - now)
