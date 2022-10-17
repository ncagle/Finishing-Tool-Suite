# -*- coding: utf-8 -*-
#¸¸.·´¯`·.¸¸.·´¯`·.¸¸
# ║╚╔═╗╝║  │┌┘─└┐│  ▄█▀‾
# ====================== #
# Finishing Tool v9.8.5  #
# Nat Cagle 2022-10-04   #
# ====================== #

# ArcPy aliasing
import arcpy as ap
from arcpy import (AddFieldDelimiters as field_delim,
	AddMessage as write,
	AddWarning as greentext,
	AddError as oops,
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
user = os.getenv('username')
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
╔══════════════════════════════╗
║ Dividers and Style Breakdown ║
╚══════════════════════════════╝

Major Divider
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

Intermediate Divider
#----------------------------------------------------------------------

Minor Divider
#-----------------------------------

Active Construction Zone
# !_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!

Section Title
' ' '
╔══════╗
║ ____ ║
╚══════╝
' ' '

Subsection Title
# ~~~~ #
# ____ #
# ~~~~ #

Task variables for Royal Decree results summary
#~~~~~ Royal Decree Variables ~~~~~
result_or_count = defined
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Priority target for updating
####################################
code or note
####################################

Found a bug
 '-.__.-'
 /oo |--.--,--,--.
 \_.-'._i__i__i_.'
       """""""""

Crevasse
A deep crack in ice.
Crevice
A narrow opening in rock.

Style Breakdown

	asdf
	example as needed


'''


'''
╔═════════════════╗
║ Notes and To-Do ║
╚═════════════════╝

## 2 hashtags in the code - recent changes/updates
### 3 hashtags in the code - unique variable or identifier
#### 4 hashtags in the code - things to be updated


#### Update Plans
  - Rewrite Repair Geometry with intersect geometry method to remove duplicate vertices and kickbacks? Might be too much spatial processing.
  - Rewrite Calculate Metrics with manual calculations. Defense mapping tool takes too long and crashes.
  - Test rewritten Find Identical code and replace existing


## Recent Changes
Version 9.7
2022-04-27
	- Rewrote UFI check for duplicate and NULL values specifically.
	- Added 'Skip Buildings' option for data with too many buildings (does not apply to Feature Count Report).
	- Sorted tools into categories.
	- Added Tunnels to Default Bridge/Tunnel WID Updater.
	- CACI Swap Scale and CTUU populates the 'SAX_RX9' field with 'Scale Swapped' the first time the tool is run. It erases the field when the Scale field is swapped back. This only goes back and forth and is dependent on this version of the tool being run when we get the database from CACI.
	- Added an updated Database Feature Report that outputs in alphabetical order, sorts any empty feature classes, and added more general totals such as total Trans, Hydro, Buildings, and Landcover.
	- Added an updated Source Analysis Report that outputs in alphabetical order and creates a csv and txt file of the SRT data source, collection dates, and total counts.
	- Added option to Disable Editor Tracking (default true).
	- More detailed error handling for geoprocessing failures. Now with noticeable skull to catch users' attention.


Version 9.8
2022-07-14
    - Added option to specify what scale to run the tools on.
        - This applies to the following tools:
	        - Populate F_Codes
	        - Calculate Default Values
	        - Calculate Metrics
	        - Update UFI Values
	        - Integrate Hydrography Features
	        - Integrate Transportation Features
	        - Integrate Utility Features
			- Default Bridge/Tunnel WID Updater
			- Default Pylon HGT Updater
			- Default Dam WOC Updater
			- Hypernova Burst Multipart Features
	        - All Bridge/Tunnel WID Updater
	        - All Pylon HGT Updater
			- All Dam WOC Updater
	        - Building in BUA Scaler
    - Added option to run tools on only 25k_LOC feature classes.
    - Switched the order of Delete Identical Features and Hypernova Burst Multipart so that any overlapping or kickback multipart features are exploded first and then checked for duplicates and removed.
    - Limited Calculate Metrics to only look at ARA for Polygons and LZN for Polylines. (This was not standard for the Defense Mapping tool).
    - Removed layered integration and overhauled the logic behind Integration steps.
        - Refactored Integration and Repair steps as modular functions.
        - Integrate Hydrography Features includes points (VanishingPoints, NaturalPools, etc.).
        - Integrate Transportation Features includes points (Ford, Culvert, etc.).
        - Work backwards through the geometry hierarchy to minimize feature shift or disjoint. Lines->Surfaces then Points->Lines.
        - Incorporated incremental snapping with 0.05m tolerance.
            - Snap lines to the nearest surface vertex within 0.05m.
	        - Snap remaining lines to the nearest surface edge within 0.05m.
			- Integrate lines->surfaces with default domain tolerance (ESRI recommended) to create intersection vertices without morphing the features.
	        - Snap points to the nearest line end node within 0.05m as priority over other vertices.
	        - Snap remaining points to the nearest line vertex within 0.05m.
	        - Snap remaining points to the nearest line edge within 0.05m.
	    	- Integrate points->lines with default domain tolerance (ESRI recommended) to create intersection vertices without morphing the features.
	    - This should help with these GAIT errors. Although the GAIT tolerance is 0.1m, so the snap tolerance may need to be modified for further accuracy.
	        - Line-Line Undershoot/Overshoot
	        - Line-Area Perimeter Undershoot
	        - Point-Line Undershoot/Overshoot
	        - Potentially others
    - Buildings in BUA Scaler has been completely refactored using more efficient logic.
        - Descales buildings within BUAs that don't have important FFNs (client dependent), have a height < 46m, and aren't navigation landmarks (LMC=True).
	    - Scales in buildings within BUAs that do have important FFNs (client dependent), have a height >= 46m, or are navigation landmarks (LMC=True).
	- Cleaned up tool outputs and format.

Backend Updates (for nerds):
    - Updated and organized module imports.
    - Improved memory management to help with increasingly large datasets being processed on potatoes.
    - Implemented new multi-value list parameters in collapsible categories to fix checkbox lag bug.
        - New parameter set-up now creates list of chosen tool names rather than 20 individual booleans.
	    - The tool selections are stored as strings in a namedtuple collection using simplified alias.
	        - tool_names.repair = "Repair All NULL Geometries"
	    - An OrderedDictionary collection uses the tool_names namedtuple as a skeleton and uses a generator function to populate the booleans.
	        - bool_dict[tool_names.repair] = True
    - Added a TDS error check for broken Catalog references. Make sure the file path points to the correct database. Dragging the TDS from the Catalog window to the tool occasionally references a filepath that no longer exists since ArcMap is to lazy to update it's object linkages regularly. Renaming a copied or newly created GDB can cause this. A lingering LOCK file still references the pre-change version, and the only way to update it is to manually input the correct path in the tool or restart ArcMap.
    - Added checks for if a feature class exists by checking it against the featureclass list, output that information to the user and skip sections of code accordingly.
    - Added a function to recalculate feature class extents. This repairs discrepancies in data extent boundaries after spatial edits in the SDE.
    - Added a function to construct the fishnet grid for partitioning large datasets into chunks using the Extent environment variable. This is now feature class independent. It is the first step in fully partitioning entire datasets for massive geospatial processing on limited computer resources.
    - Fixed comma tuple bug in Calculate Metrics.
    - Changed the output for Update UFI Values to more accurately show which one is actively being worked on. User reading comprehension leaves something to be desired.
    - Removed use of the Defense Mapping extension in Hypernova Burst Multipart Features when calculating new default values.
    - CACI Swap scale_name variable was missing a definition after the last update. Added a second return value from the snowflake_protocol function for whatever CACI's unique Scale field name happens to be for any given schema.
    - Repair All NULL Geometries, Populate F_Codes, Calculate Default Values, Calculate Metrics, Update UFI Values, Integrate Hydrography Features, Integrate Transportation Features, and Integrate Utility Features have been refactored into functions.
	- Updated function aliases in code as well as replaced redundant code with recently made functions.
	- The create_fc_list function now runs get_count function for each feature class in the dataset at the start and constructs the list with only feature classes that have records.


Version 9.8.5
2022-08-04
	- Bridge/Tunnel WID Updater, Pylon HGT Updater, and Building in BUA Scaler have been refactored into functions.
	- Updated function aliases in code as well as replaced redundant code with recently made functions.
	- Updated tool names.
	- Updated outro summary phrasing, formatting, and statistics.
	- Updated create_fc_list function logic for detecting metadata and resource surfaces, and updated how it sorts and filters feature classes.
	- Fixed grammar for singular hour and minute outputs in runtime function.
	- If CACI Swap Scale and CTUU is checked but the GDB is not a caci schema, the CACI Swap tool parameter is set to FALSE to skip it entirely.
	- Added the runtime function output to the fishnet construction (grid_chungus) function.

	- Hypernova Burst Multipart Features
		- Updated calculation of exploded feature counts.

	- Database Feature Report
		- Added Utility feature count.

	- Bridge/Tunnel WID Updater
		- Split tool into Default Bridge/Tunnel WID Updater and All Bridge/Tunnel WID Updater. 'Default' isolates Bridges/Tunnels with default WID values for processing to save time. 'All' checks all features for any mismatched WID, not just default WID.
		- Bridge/Tunnel WID Updater can now check for Bridges/Tunnels with WID <= Trans width and updates them based on the underlying Trans feature.
		- Now with added cart tracks! Yum!
		- Updates mismatched CTUU values so the Bridge/Tunnel feature matches its underlying Trans feature.
		- Updated Bridge/Tunnel-Trans shared geometry method.
		- Rewrote tool output statistics.
		- Updated feature comparison criteria.

	- Pylon HGT Updater
		- Split tool into Default Pylon HGT Updater and All Pylon HGT Updater. 'Default' isolates Pylons with default HGT values for processing to save time. 'All' checks all Pylons for any mismatched HGT, not just default HGT.
		- Pylon HGT Updater can now check Pylons against intersecting Cables for mismatched HGT values and updates the Pylon HGT to match the Cable HGT.
		- Updates mismatched CTUU values so the Pylon feature matches its intersecting Cable feature.
		- Rewrote tool output statistics.
		- Updated feature comparison criteria.

2022-08-24
	- Reformatted Tool Dialogue layout to have one category for Finishing Tools and one category for Preprocessing Tools.
	- CACI Swap Scale and CTUU has been refactored into a function.
	- Updated function aliases in code as well as replaced redundant code with recently made functions.
	- Simplified runtime function to only have start variable and automatically get finish at time of execution.
	- Updated parameters in all runtime functions.
	- Updated important FFN list for Project 10 requirements. Uses a combination of Hexagon and Maxar requirements. Makes best assumptions based on vague guidance.
	- Refactored and included Dam WOC Updater as a function.
		- Split tool into Default Dam WOC Updater and All Dam WOC Updater. 'Default' isolates Dams with default WOC values for processing to save time. 'All' checks all features for any incorrect or unpopulated WOC, not just default WOC.
		- Updates Dam TRS based on its dominant spatial relationship to any intersecting Trans features or lack thereof.
		- Rewrote tool output statistics.
		- Updated feature comparison criteria.
	- Added Raven Queen to royal decree and Secret Finishing Version parameter.
	- Removed CACI Swap Scale and CTUU and associated checks. Functions are still present, but disabled.


Version 9.8.7
2022-10-11
	- Added Partition Cores option for choosing how to partition large dataset to allow for processing with limited computer resources.
	- Confirmed that the Calculate Default Values tool does not, in fact, populate NULL Version fields. That field is skipped in default value processing.
	- Updated tool validation script.
	- Updated feature checks for feature specific tools. Allows for tasks to continue after encountering a feature class that is not present in the dataset or does not contain any of the necessary features.
	- Added Tool Help descriptions for all Finishing Tool Suite parameters and tool options.
	- Added logo.
	- Created tool documentation.
	- Created Manual Finishing Preparation and Repair documentation of the steps required to manually perform the same tasks as the Finishing Tool Suite.
	- Rewrote Update UFI Values logic to handle godzilla databases. Overall speed of tool has increased by 192%.
	- Restructured creation of the feature class list for processing to preemptively store feature counts and reduce multiple redundant duplicate redundancies.
	- Updated text formatting for error handling and important task details/results.
	- Rewrote Calculate Metrics to not use Defense Mapping extension. Using direct, sequential geometry calculation to speed up processing. The geometries have their shape preserved assuming a geodesic geographic coordinate system. The area and length are calculated on the surface of the Earth ellipsoid.
	- Completely removed the need for the Defense Mapping Extension in any of the current tools. Checking out/in this extension caused issues on some computers. The cause could never be nailed down, so the use of the extension has been slowly phased out. In addition, this makes the tools more accessible to those without that specific ArcMap extension and avoids issues with extension versions and updates in the future.
	- Added default progressor with labels for end-users who don't read.


v9.7-v9.8.7: 123 updates




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
	# ffn_list_p10_combo
		# OrderedDict([('    Public Administration', 808), ...]) # Sorted, formatted, list of tuples that becomes an ordered dictionary


#----------------------------------------------------------------------
def TDS_check(TDS):
	if not ap.Exists(TDS):
		oops('                       ______\n                    .-"      "-.\n                   /            \\\n       _          |              |          _\n      ( \\         |,  .-.  .-.  ,|         / )\n       > "=._     | )(__/  \\__)( |     _.=" <\n      (_/"=._"=._ |/     /\\     \\| _.="_.="\\_)\n             "=._ (_     ^^     _)"_.="\n                 "=\\__|IIIIII|__/="\n                _.="| \\IIIIII/ |"=._\n      _     _.="_.="\\          /"=._"=._     _\n     ( \\_.="_.="     `--------`     "=._"=._/ )\n      > _.="                            "=._ <\n     (_/                                    \\_)\n')
		oops("Dataset {0} does not exist.\nPlease double check that the file path is correct.\nExitting tool...\n".format(TDS))
		sys.exit(0)


#----------------------------------------------------------------------
### [0] TDS   (The standard Finishing process is checked by default)   (Tools are run in list order) - Feature Dataset
TDS = ap.GetParameterAsText(0)
TDS_check(TDS)
ap.env.workspace = TDS
ap.env.extent = TDS
ap.env.overwriteOutput = True
username = os.environ['USERNAME']
### [1] For Top-Secret Finishing Version, what is the name of our leader? (Chairman Bock)- String
secret = ap.GetParameterAsText(1) # Password for Finishing easter egg
### [2] Scale to run tools: ZI026_CTUU >= - String Value List
where_scale = "zi026_ctuu >= {0}".format(ap.GetParameterAsText(2))
cores = str(int(math.sqrt(int(ap.GetParameterAsText(3)))))

#-----------------------------------
### [4] Options .............. String Value List
### Tool Processing Options:   ['Use 25k_LOC feature classes only', 'Disable Editor Tracking', 'Skip Buildings']
### [5] Finishing         String Value List
### Finishing Tools :     ['Repair All NULL Geometries', 'Populate F_Codes', 'Calculate Default Values', 'Calculate Metrics', 'Update UFI Values',
###						   'Integrate Hydrography Features', 'Integrate Transportation Features', 'Integrate Utility Features',
###						   'Default Bridge/Tunnel WID Updater', 'Default Pylon HGT Updater', 'Default Dam WOC Updater', 'Hypernova Burst Multipart Features',
###						   'Delete Identical Features']
### Default:
### 'Repair All NULL Geometries';'Populate F_Codes';'Calculate Default Values';'Calculate Metrics';'Update UFI Values';'Integrate Hydrography Features';'Integrate Transportation Features';'Integrate Utility Features';'Hypernova Burst Multipart Features';'Delete Identical Features'
### [6] Preprocessing     String Value List
### Preprocessing Tools:  ['All Bridge/Tunnel WID Updater', 'All Pylon HGT Updater', 'All Dam WOC Updater', 'Building in BUA Scaler', 'Database Feature Report',
###						   'Source Analysis Report']
### Default:

### [6] Maintenance .......... String Value List
### Data Maintenance Tools:    ['Repair All NULL Geometries', 'Populate F_Codes', 'Calculate Default Values', 'Calculate Metrics', 'Update UFI Values']
### [7] Integration .......... String Value List
### Integration Tools:         ['Integrate Hydrography Features', 'Integrate Transportation Features', 'Integrate Utility Features', 'Default Bridge/Tunnel WID Updater', 'Default Pylon HGT Updater', 'Default Dam WOC Updater']
### [8] Geometry ............. String Value List
### Geometry Correction Tools: ['Hypernova Burst Multipart Features', 'Delete Identical Features']
### [9] Preprocessing ........ String Value List
### Preprocessing Tools:       ['All Bridge/Tunnel WID Updater', 'All Pylon HGT Updater', 'All Dam WOC Updater', 'Building in BUA Scaler', 'CACI Swap Scale and CTUU']
### [10] Management .......... String Value List
### Database Management Tools: ['Database Feature Report', 'Source Analysis Report']

tool_list = ap.GetParameter(4) + ap.GetParameter(5) + ap.GetParameter(6)

#-----------------------------------
#autopcf = ap.GetParameter()
#hydrattr = ap.GetParameter()
#tranattr = ap.GetParameter()
#utilattr = ap.GetParameter()
#cultureattr = ap.GetParameter()
#landcover = ap.Getparameter()

#-----------------------------------
name_class = namedtuple("name_class", "loc disable vogon repair fcode defaults metrics ufi hydro trans util defbridge defpylong defdam explode dups allbridge allpylong alldam building fcount vsource")
# tool_names.var to get Tool Name
tool_names = name_class("Use 25k_LOC feature classes only", "Disable Editor Tracking", "Skip Buildings", "Repair All NULL Geometries", "Populate F_Codes", "Calculate Default Values", "Calculate Metrics", "Update UFI Values", "Integrate Hydrography Features", "Integrate Transportation Features", "Integrate Utility Features", "Default Bridge/Tunnel WID Updater", "Default Pylon HGT Updater", "Default Dam WOC Updater", "Hypernova Burst Multipart Features", "Delete Identical Features", "All Bridge/Tunnel WID Updater", "All Pylon HGT Updater", "All Dam WOC Updater", "Building in BUA Scaler", "Database Feature Report", "Source Analysis Report")

#-----------------------------------
# bool_dict[tool_names.var] to get tool boolean
bool_dict = OrderedDict([
	(tool_names.loc, False),
	(tool_names.disable, False),
	(tool_names.vogon, False),
	(tool_names.repair, False),
	(tool_names.fcode, False),
	(tool_names.defaults, False),
	(tool_names.metrics, False),
	(tool_names.ufi, False),
	(tool_names.hydro, False),
	(tool_names.trans, False),
	(tool_names.util, False),
	(tool_names.defbridge, False),
	(tool_names.defpylong, False),
	(tool_names.defdam, False),
	(tool_names.explode, False),
	(tool_names.dups, False),
	(tool_names.allbridge, False),
	(tool_names.allpylong, False),
	(tool_names.alldam, False),
	(tool_names.building, False),
	(tool_names.fcount, False),
	(tool_names.vsource, False)
])
for key in (key for key in bool_dict.keys() if key in tool_list): bool_dict[key] = True # Iterate generator of tools in tool_list and set True



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



'''
╔═══════════════════╗
║ General Functions ║
╚═══════════════════╝
'''
#----------------------------------------------------------------------
# Explicit is better than implicit
# Lambda function works better than "if not fieldname:", which can falsely catch 0.
#if not populated(row[0])
populated = lambda x: x is not None and str(x).strip() != '' and x != -999999 # Function that returns boolean of if input field is populated or empty or default
not_null = lambda x: x is not None
is_null = lambda x: x is None # A bit redundant

#-----------------------------------
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
	oops("\n\n***Failed to run {0}.***\n".format(tool_name))
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
		oops("Tool Warnings:")
		oops("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		oops(warnings)
		oops("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	oops("Error Report:")
	oops("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	oops(python_errors)
	oops(arcpy_errors)
	oops("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	oops('                       ______\n                    .-"      "-.\n                   /            \\\n       _          |              |          _\n      ( \\         |,  .-.  .-.  ,|         / )\n       > "=._     | )(__/  \\__)( |     _.=" <\n      (_/"=._"=._ |/     /\\     \\| _.="_.="\\_)\n             "=._ (_     ^^     _)"_.="\n                 "=\\__|IIIIII|__/="\n                _.="| \\IIIIII/ |"=._\n      _     _.="_.="\\          /"=._"=._     _\n     ( \\_.="_.="     `--------`     "=._"=._/ )\n      > _.="                            "=._ <\n     (_/                                    \\_)\n')
	oops("Please rerun the tool.")
	oops("Go double check the tool outputs above for more information on where the tool failed.")
	oops("If the error persists, uncheck the {0} tool option before rerunning.\nEither the feature class is too big or something else has gone wrong.".format(tool_name))
	oops("Exiting tool.\n")
	sys.exit(0)
	#print(u'                 uuuuuuu\n             uu$$$$$$$$$$$uu\n          uu$$$$$$$$$$$$$$$$$uu\n         u$$$$$$$$$$$$$$$$$$$$$u\n        u$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$$$$$$$$$$$$$$$$$$$$u\n       u$$$$$$"   "$$$"   "$$$$$$u\n       "$$$$"      u$u       $$$$"\n        $$$u       u$u       u$$$\n        $$$u      u$$$u      u$$$\n         "$$$$uu$$$   $$$uu$$$$"\n          "$$$$$$$"   "$$$$$$$"\n            u$$$$$$$u$$$$$$$u\n             u$"|¨|¨|¨|¨|"$u\n  uuu        $$u|¯|¯|¯|¯|u$$       uuu\n u$$$$        $$$$$u$u$u$$$       u$$$$\n  $$$$$uu      "$$$$$$$$$"     uu$$$$$$\nu$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$\n$$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"\n """      ""$$$$$$$$$$$uu ""$"""\n           uuuu ""$$$$$$$$$$uuu\n  u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$\n  $$$$$$$$$$""""           ""$$$$$$$$$$$"\n   "$$$$$"                      ""$$$$""\n     $$$"                         $$$$"')

def runtime(start): # Time a process or code block
	# Add a start time variable and use this function when you want that timer to end
	# Returns string of formatted elapsed time between start and execution of this function
	#from datetime import datetime as dt
	#start = dt.now()
	time_delta = (dt.now() - start).total_seconds()
	h = int(time_delta/(60*60))
	m = int((time_delta%(60*60))/60)
	s = time_delta%60.
	#time_elapsed = "{}:{:>02}:{:>05.4f}".format(h, m, s) # 00:00:00.0000
	if h == 1:
		hour_grammar = "hour"
	else:
		hour_grammar = "hours"
	if m == 1:
		minute_grammar = "minute"
	else:
		minute_grammar = "minutes"
	if h and m and s:
			time_elapsed = "{} {} {} {} and {} seconds".format(h, hour_grammar, m, minute_grammar, round(s))
	elif not h and m and s:
		time_elapsed = "{} {} and {:.1f} seconds".format(m, minute_grammar, s)
	elif not h and not m and s:
		time_elapsed = "{:.3f} seconds".format(s)
	else:
		time_elapsed = 0
	return time_elapsed

def progress(tool_name, fc, option): # Looping Loading Progress Bar
	if option == 'start':
		#progress(tool_name, '', 'start')
		ap.SetProgressor("default", "Starting {0}".format(tool_name))
		time.sleep(0.6)
	elif option == 'next':
		#for oo in loop:
		#	progress(tool_name, fc, 'next')
		#	value = srow[0] # Tool logic here
		ap.SetProgressorLabel("Running {0} on {1}...".format(tool_name, fc))
	elif option == 'stop':
		#progress(tool_name, '', 'stop')
		ap.SetProgressorLabel("Completed {0}".format(tool_name))
		ap.ResetProgressor()

def newprogress(tool_name, fc, option, pos): # Step Progressor Percentage Progress Bar
	if option == 'start':
		#increment = progress(fc, 'start', 0)
		p = int(math.log10(fc_counts[fc]))
		if not p: p = 1
		increment = int(math.pow(10, p - 1))
		ap.SetProgressor("step", "Running {0} on {1}".format(tool_name, fc), 0, fc_counts[fc], increment)
		return increment
	elif option == 'next':
		# with ap.da.SearchCursor(fc, ['field']) as scursor:
		# 	for pos, srow in enumerate(scursor, 0):
		# 		if (pos % increment) == 0:
		# 			progress(fc, 'next', pos)
		# 		value = srow[0] # Tool logic here
		ap.SetProgressorPosition(pos)
	elif option == 'stop':
		#progress(fc, 'stop', 0)
		ap.SetProgressorPosition(fc_counts[fc])
		ap.ResetProgressor()

#-----------------------------------
def make_field_list(dsc): # Construct a list of proper feature class fields
	# Sanitizes Geometry fields to work on File Geodatabases or SDE Connections
	#field_list = make_field_list(describe_obj)
	fields = dsc.fields # List of all fc fields
	out_fields = [dsc.OIDFieldName, dsc.lengthFieldName, dsc.areaFieldName, 'shape', 'area', 'length'] # List Geometry and OID fields to be removed
	# Construct sanitized list of field names
	field_list = [field.name for field in fields if field.type not in ['Geometry'] and not any(substring in field.name.lower() for substring in out_fields if substring)]
	# Add ufi field to index[-3], OID@ token to index[-2], and Shape@ geometry token to index[-1]
	field_list.append('OID@')
	field_list.append('SHAPE@')
	return field_list

def replace_list_value(existing, new, llist):
	return list(map(lambda x: x.replace(existing, new), llist))

def existential_panic(fc, toolname): # If current fc is empty, proceed with caution. If it isn't in the dataset, add an error.
	#if fc not in featureclass:
	#	if existential_panic(fc, tool_names.xxx):
	#		return tool_variables
	#	else:
	#		pass or return tool_variables
	if fc in featurerecess: # List of feature classes that have 0 records
		greentext("\n~~~ {0} has no features. Moving on. ~~~\n".format(fc))
		return False
	if fc not in featureclass and fc not in featurerecess: # If fc is not in either list, then it doesn't exist in the dataset
		oops("\n*** {0} is missing from the TDS dataset. Failed to run {1}. ***\n".format(fc, toolname))
		return True

#-----------------------------------
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

#-----------------------------------
def get_count(fc): # Returns feature count
    results = int(ap.GetCount_management(fc).getOutput(0))
    return results

def format_count(count): # format counts with the right amount of spacing for output report
	cnt_str = str(count)
	end_spacing = ""
	if len(cnt_str) > 0:
		for i in range(7-len(cnt_str)):
			end_spacing += " "
	else:
		pass
	return end_spacing

def clear_cache(lyr_list):
	for lyr in lyr_list: arcdel(lyr)


'''
╔════════════════╗
║ Tool Functions ║
╚════════════════╝
'''
#----------------------------------------------------------------------
def create_fc_list():
	fc_list_start = dt.now()
	write("Constructing feature class list from provided dataset.")
	write("Only feature classes containing records will be processed.")
	if bool_dict[tool_names.loc]: # Only run on 25k_LOC feature classes
		write("Only loading 25k_LOC feature classes.")
		# 25k_LOC Feature Classes
		featureclass_loc = ['AeronauticPnt', 'AeronauticSrf', 'FacilityPnt', 'FacilitySrf', 'HydrographyCrv', 'HydrographyPnt', 'HydrographySrf', 'IndustryPnt', 'IndustrySrf', 'InformationSrf', 'MilitaryPnt', 'MilitarySrf', 'PortHarbourPnt', 'PortHarbourSrf', 'StoragePnt', 'StorageSrf', 'StructurePnt', 'StructureSrf', 'TransportationGroundCrv', 'TransportationGroundPnt', 'TransportationGroundSrf', 'TransportationWaterCrv', 'TransportationWaterPnt', 'TransportationWaterSrf', 'UtilityInfrastructureCrv', 'UtilityInfrastructurePnt', 'UtilityInfrastructureSrf']
		if bool_dict[tool_names.vogon]:
			featureclass_loc.remove('StructureSrf')
			featureclass_loc.remove('StructurePnt')
			greentext("StructureSrf and StructurePnt will be skipped in processing.")

		#featureclass = [fc for fc in featureclass if fc_exists(fc, 'Finishing Tool') and get_count(fc)]
		fc_counts = {}
		featurerecess = []
		for fc in featureclass_loc:
			count = get_count(fc)
			if count:
				fc_counts[fc] = count
				write("    - {0} {1} features".format(count, fc))
			else:
				featurerecess.append(fc)
				greentext("    > {0} has {1} features".format(fc, count))

		featureclass = fc_counts.keys()
		featureclass.sort()
		write("Loaded {0} of 55 TDSv7.1 feature classes in {1}".format(len(featureclass), runtime(fc_list_start)))
		return fc_counts, featureclass, featurerecess

	#featureclass = ap.ListFeatureClasses()
	#featureclass = [fc for fc in featureclass if get_count(fc)]
	#featureclass = [fc for fc in ap.ListFeatureClasses() if get_count(fc)]
	fc_counts = {}
	featurerecess = []
	for fc in sorted(ap.ListFeatureClasses()):
		if bool_dict[tool_names.vogon]:
			if 'StructurePnt' in fc:
				print("StructurePnt will be skipped in processing.")
				continue
			if 'StructureSrf' in fc:
				print("StructureSrf will be skipped in processing.")
				continue
		if 'MetadataSrf' in fc:
			print("MetadataSrf will be skipped in processing.")
			continue
		if 'ResourceSrf' in fc:
			print("ResourceSrf will be skipped in processing.")
			continue
		count = get_count(fc)
		if count:
			fc_counts[fc] = count
			write("    - {0} {1} features".format(count, fc))
		else:
			featurerecess.append(fc)
			greentext("    > {0} has {1} features".format(fc, count))

	# Formatting Feature Class list
	featureclass = fc_counts.keys()
	featureclass.sort()
	write("Loaded {0} of 55 TDSv7.1 feature classes in {1}".format(len(featureclass), runtime(fc_list_start)))
	return fc_counts, featureclass, featurerecess

def snowflake_protocol(): # Checking for CACI schema cz they're "special" and have to make everything so fucking difficult
	snowflake_start = dt.now()
	scale_field = 'scale'
	write("Checking for CACI custom schema...")
	for fc in featureclass:
		field_check = ap.ListFields(fc)
		field_check = [field.name for field in field_check if any([scale_field in field.name.lower()])]
		if field_check:
			greentext("Variant TDS schema identified in {0}\nSnowflake protocol activated for relevant tools.".format(runtime(snowflake_start)))
			return True, field_check
		else:
			write("Regular TDS schema identified in {0}".format(runtime(snowflake_start)))
			return False, scale_field

def disable_editor_tracking(gdb_name): # Automatically disables editor tracking for each feature class that doesn't already have it disabled
	disable_start = dt.now()
	write("Disabling Editor Tracking for {0}".format(gdb_name))
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
				greentext("Error disabling editor tracking for {0}. Please check the data manually and try again.".format(fc))
				pass
	if firstl:
		write("Editor Tracking has been disabled.")
	else:
		write("Editor Tracking has already been disabled.")
	write("Time to disable Editor Tracking: {0}".format(runtime(disable_start)))

def check_defense(in_out): # If any of the tools that require the Defense Mapping license are selected, check out the Defense license
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

def refresh_extent(): # Recalculate each feature class extent to minimize the dataset bounding polygon for data partitioning
	# refresh_extent_start = dt.now()
	write("Recalculating feature class extents...\nThis repairs discrepancies in data extent boundaries after spatial edits in the SDE.")
	# #for fc in featureclass: ap.RecalculateFeatureClassExtent_management(fc)
	# # Cheating this to save a good chunk of time by only refreshing the extent of metadata and resource surfaces
	# if ap.Exists('MetadataSrf'):
	# 	ap.RecalculateFeatureClassExtent_management('MetadataSrf')
	# if ap.Exists('ResourceSrf'):
	# 	ap.RecalculateFeatureClassExtent_management('ResourceSrf')
	# elif ap.Exists('HydrographyCrv'):
	# 	ap.RecalculateFeatureClassExtent_management('HydrographyCrv')
	# elif ap.Exists('TransportationGroundCrv'):
	# 	ap.RecalculateFeatureClassExtent_management('TransportationGroundCrv')
	# write("Spatial data extent fully recalculated in {0}".format(runtime(refresh_extent_start)))

def grid_chungus(): #Create fishnet grid to partition large datasets into chunks so our potatoes have a chance of doing geospatial processing
	chungus_start = dt.now()
	mem_fc = "in_memory\\the_grid"
	origin_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMin) # ESRI docs lie and say CreateFishnet uses a Point object like extent.lowerLeft
	y_axis_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperLeft
	corner_coord = '{0} {1}'.format(ap.env.extent.XMax, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperRight
	# y_axis──>┌──┐<──corner
	# origin──>└──┘
	write("Constructing fishnet over dataset for partitioning data into chunks.\nThis helps our potatoes handle the large scale geospatial databases we have to process.")
	#### Vertex Density Check to determine if a 2x2, 3x3, or larger should be used for really big honkin data
	#ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", "", "POLYGON")
	ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", cores, cores, corner_coord, "NO_LABELS", "", "POLYGON")
	write("Spatial data partitions constructed in {0}".format(runtime(chungus_start)))
	return mem_fc

#----------------------------------------------------------------------
def repair_geometry():
	repair_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.repair))
	for fc in featureclass:
		progress(tool_names.repair, fc, 'next')
		write("Repairing NULL geometries in {0}".format(fc))
		ap.RepairGeometry_management(fc, "DELETE_NULL")
		#ap.RepairBadGeometry_production(featureclass, 'REPAIR_ONLY', 'DELETE_NULL_GEOMETRY', '#') # Repair Bad Geometry Production Mapping tool
	greentext("{0} finished in {1}".format(tool_names.repair, runtime(repair_start)))

#-----------------------------------
def pop_fcode():
	fcode_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.fcode))
	fcode_total = 0
	fields = ['f_code', 'fcsubtype']
	for fc in featureclass:
		progress(tool_names.fcode, fc, 'next')
		fcode_count = 0
		try:
			with ap.da.UpdateCursor(fc, fields, where_scale) as ucursor:
				for urow in ucursor: # Checks if F_Code matches the FCSubtype value. Updates F_Code if they don't match assuming proper subtype
					if urow[0] != str(ad.sub2fcode_dict[urow[1]]): #dict_import
						urow[0] = str(ad.sub2fcode_dict[urow[1]]) #dict_import
						fcode_count += 1
						ucursor.updateRow(urow)
			write("Updated {0} {1} feature F_Codes".format(fcode_count, fc))
			fcode_total += fcode_count
		except:
			greentext("{0} does not contain F_codes.".format(fc))
	greentext("{0} F_Code errors fixed in {1}".format(fcode_total, runtime(fcode_start)))
	return fcode_total

#-----------------------------------
def populate_null(fc, field_list, default):
	#populate_null(fc, string_fields, <'noInformation' or -999999>)
	count = 0
	with ap.da.UpdateCursor(fc, field_list, where_scale) as ucursor:
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

def process_defaults(fc_list):
	defaults_start = dt.now()
	if fc_list == featureclass:
		write("\n--- {0} ---\n".format(tool_names.defaults))
	count_nulls = 0
	write("Constructing field type lists to match default values to domain definitions")
	for fc in fc_list:
		progress(tool_names.defaults, fc, 'next')
		out_fields = ['shape', 'area', 'length', 'created', 'edited', 'f_code', 'fcsubtype', 'ufi', 'version']
		in_types = ['Double', 'Integer', 'Single', 'SmallInteger']
		string_fields = [field.name for field in arcpy.ListFields(fc, None, 'String') if not any(substring in field.name.lower() for substring in out_fields)]
		number_fields = [field.name for field in arcpy.ListFields(fc) if field.type in in_types and not any(substring in field.name.lower() for substring in out_fields)]
		string_fields.sort()
		number_fields.sort()
		fc_nulls = 0
		write("Locating NULL text and numeric fields in {0}".format(fc))
		fc_nulls += populate_null(fc, string_fields, 'noInformation')
		fc_nulls += populate_null(fc, number_fields, -999999)
		if fc_nulls > 0:
			write("  - {0} NULL values populated".format(fc_nulls))
		count_nulls += fc_nulls
	greentext("{0} NULL values populated with defaults in {1}".format(count_nulls, runtime(defaults_start)))

#-----------------------------------
def calc_metrics():
	metrics_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.metrics))
	for fc in featureclass:
		progress(tool_names.metrics, fc, 'next')
		if 'InformationCrv' in fc:
			continue
		shape_type = ap.Describe(fc).shapeType # Polygon, Polyline, Point, Multipoint, MultiPatch
		if 'Polyline' in shape_type:
			write("Calculating Length field for {0}".format(fc))
			with ap.da.UpdateCursor(fc, ['LZN', 'SHAPE@'], where_scale) as ucursor:
				for urow in ucursor:
					urow[0] = int(round(urow[-1].getLength('PRESERVE_SHAPE')))
					ucursor.updateRow(urow)
		elif 'Polygon' in shape_type:
			write("Calculating Area field for {0}".format(fc))
			with ap.da.UpdateCursor(fc, ['ARA', 'SHAPE@'], where_scale) as ucursor:
				for urow in ucursor:
					urow[0] = int(round(urow[-1].getArea('PRESERVE_SHAPE')))
					ucursor.updateRow(urow)
	greentext("{0} finished in {1}".format(tool_names.metrics, runtime(metrics_start)))

#-----------------------------------
def update_ufi():
	ufi_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.ufi))
	ufi_total = 0
	for fc in featureclass:
		progress(tool_names.ufi, fc, 'next')
		ufi_fc_start = dt.now()
		write("Scanning {0} UFIs in {1}...".format(fc_counts[fc], fc))
		with ap.da.UpdateCursor(fc, 'ufi', where_scale) as ucursor:
			for urow in ucursor:
				urow[0] = str(uuid.uuid4())
				ucursor.updateRow(urow)
		ufi_total += fc_counts[fc]
		write("Updated UFIs in {0}".format(runtime(ufi_fc_start)))
	greentext("{0} total UFI values updated in {1}".format(ufi_total, runtime(ufi_start)))
	return ufi_total

#-----------------------------------
# def dangling_orphans():
# 	arcpy.DeleteDangles_production(inFeatures, "10 Feet", '#', 'NON_RECURSIVE', '45')
# 	arcpy.RemoveCutbacks_production(roads, minimum_angle, "SEQUENTIAL", '#', 'IGNORE_SNAPPED_POINTS', '#')

def snap_lines_to_srf(lines, srf):
	#tolerance = "0.1 Meters"
	tolerance = "0.05 Meters"
	#tolerance = "1 Meters"
	vertex_env = [srf, "VERTEX", tolerance] # Snap lines to the nearest srf vertex within 0.03m
	edge_env = [srf, "EDGE", "0.03 Meters"] # Snap remaining lines to the nearest srf edge within 0.03m
	write("Snapping line end nodes to rank 1 surface vertices rank 2 surface edges.")
	ap.Snap_edit(lines, [vertex_env, edge_env])
	write("Creating missing line-surface intersection vertices.")
	ap.Integrate_management([[srf, 1], [lines, 2]]) # Integrate lines to srfs with default domain tolerance to create intersection vertices in them without morphing them and creating potential errors.
	ap.RepairGeometry_management(srf, "DELETE_NULL")

def snap_points_to_lines(points, lines):
	#tolerance = "0.1 Meters"
	tolerance = "0.05 Meters"
	#tolerance = "1 Meters"
	end_env = [lines, "END", tolerance] # Snap points to the nearest line end node within 0.03m as priority over other vertices
	vertex_env = [lines, "VERTEX", "0.03 Meters"] # Snap points to the nearest line vertex within 0.03m
	edge_env = [lines, "EDGE", "0.03 Meters"] # Snap remaining points to the nearest line edge within 0.03m
	write("Snapping points to rank 1 line end nodes, rank 2 line vertices, and rank 3 line edges.")
	ap.Snap_edit(points, [end_env, vertex_env, edge_env])
	write("Creating missing point-line intersection vertices.")
	ap.Integrate_management([[lines, 1], [points, 2]]) # Integrate points to lines with default domain tolerance to create intersection vertices in the lines without morphing them and creating potential errors.
	ap.RepairGeometry_management(lines, "DELETE_NULL")
	ap.RepairGeometry_management(points, "DELETE_NULL")

def make_integrate_layers(name_list):
	# name_list = ['FeaturePnt', 'FeatureCrv', 'FeatureSrf', 'feat_pnt', 'feat_crv', 'feat_srf']
	if name_list[0] not in featureclass:
		if existential_panic(name_list[0], "Integrate and Repair"):
			return False
	if name_list[1] not in featureclass:
		if existential_panic(name_list[1], "Integrate and Repair"):
			return False
	if name_list[2] not in featureclass:
		if existential_panic(name_list[2], "Integrate and Repair"):
			return False

	write("Making {0}, {1}, and {2} feature layers".format(name_list[0], name_list[1], name_list[2]))
	if name_list[0] == 'UtilityInfrastructurePnt':
		make_lyr(name_list[0], name_list[3], "f_code = 'AT042' AND {0}".format(where_scale))
	else:
		make_lyr(name_list[0], name_list[3], where_scale)
	if name_list[1] == 'UtilityInfrastructureCrv':
		make_lyr(name_list[1], name_list[4], "f_code = 'AT005' AND {0}".format(where_scale))
	else:
		make_lyr(name_list[1], name_list[4], where_scale)
	make_lyr(name_list[2], name_list[5], where_scale)
	write("Repairing {0} lines and {1} polygons before Integration".format(name_list[1], name_list[2]))
	ap.RepairGeometry_management(name_list[4], "DELETE_NULL")
	ap.RepairGeometry_management(name_list[5], "DELETE_NULL")
	return True

def repair_and_clean(name_list):
	#name_list = ['FeaturePnt', 'FeatureCrv', 'FeatureSrf', 'feat_pnt', 'feat_crv', 'feat_srf', grid_lyr]
	write("Repairing {0} and {1} features after integration".format(name_list[1], name_list[2]))
	ap.RepairGeometry_management(name_list[4], "DELETE_NULL")
	ap.RepairGeometry_management(name_list[5], "DELETE_NULL")
	write("Clearing process cache")
	clear_cache([name_list[3], name_list[4], name_list[5], name_list[-1]])

def integrate_hydro():
	hydro_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.hydro))
	hydro_list = ['HydrographyPnt', 'HydrographyCrv', 'HydrographySrf', 'hydro_pnt', 'hydro_crv', 'hydro_srf', 'grid_lyr']
	hydro_pnt = hydro_list[3]
	hydro_crv = hydro_list[4]
	hydro_srf = hydro_list[5]
	grid_lyr = hydro_list[-1]
	hfeat_count = 0
	make_lyr(mem_grid, grid_lyr)
	if not make_integrate_layers(hydro_list):
		return hfeat_count

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
			ap.SetProgressorLabel("Processing Hydrography features in partition {0}...".format(row[0]))
			select = "OID = {}".format(row[0])
			select_by_att(grid_lyr, "NEW_SELECTION", select)
			select_by_loc(hydro_pnt, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(hydro_crv, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(hydro_srf, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			pnt_count = get_count(hydro_pnt)
			crv_count = get_count(hydro_crv)
			srf_count = get_count(hydro_srf)
			hfeat_count = hfeat_count + pnt_count + crv_count + srf_count
			write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(pnt_count, hydro_list[0], crv_count, hydro_list[1], srf_count, hydro_list[2], row[0]))
			if crv_count > 0 and srf_count > 0:
				snap_lines_to_srf(hydro_crv, hydro_srf)
			if pnt_count > 0 and crv_count > 0:
				snap_points_to_lines(hydro_pnt, hydro_crv)
			if not pnt_count and not srf_count and crv_count > 0:
				write("Only curves present in data. Integrating them alone.")
				ap.Integrate_management(hydro_crv, "0.01 Meters")

	repair_and_clean(hydro_list)
	greentext("{0} finished in {1}".format(tool_names.hydro, runtime(hydro_start)))
	return hfeat_count

def integrate_trans():
	trans_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.trans))
	trans_list = ['TransportationGroundPnt', 'TransportationGroundCrv', 'TransportationGroundSrf', 'trans_pnt', 'trans_crv', 'trans_srf', 'grid_lyr']
	trans_pnt = trans_list[3]
	trans_crv = trans_list[4]
	trans_srf = trans_list[5]
	grid_lyr = trans_list[-1]
	tfeat_count = 0
	make_lyr(mem_grid, grid_lyr)
	if not make_integrate_layers(trans_list):
		return tfeat_count

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
			ap.SetProgressorLabel("Processing Transportation features in partition {0}...".format(row[0]))
			select = "OID = {}".format(row[0])
			select_by_att(grid_lyr, "NEW_SELECTION", select)
			select_by_loc(trans_pnt, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(trans_crv, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(trans_srf, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
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
				ap.Integrate_management(trans_crv, "0.01 Meters")

	repair_and_clean(trans_list)
	greentext("{0} finished in {1}".format(tool_names.trans, runtime(trans_start)))
	return tfeat_count

def integrate_util():
	util_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.util))
	util_list = ['UtilityInfrastructurePnt', 'UtilityInfrastructureCrv', 'UtilityInfrastructureSrf', 'util_pnt', 'util_crv', 'util_srf', 'grid_lyr']
	util_pnt = util_list[3]
	util_crv = util_list[4]
	util_srf = util_list[5]
	grid_lyr = util_list[-1]
	ufeat_count = 0
	make_lyr(mem_grid, grid_lyr)
	if not make_integrate_layers(util_list):
		return ufeat_count

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
			ap.SetProgressorLabel("Processing Utility features in partition {0}...".format(row[0]))
			select = "OID = {}".format(row[0])
			select_by_att(grid_lyr, "NEW_SELECTION", select)
			select_by_loc(util_pnt, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(util_crv, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(util_srf, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
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
				ap.Integrate_management(util_crv, "0.01 Meters")

	repair_and_clean(util_list)
	greentext("{0} finished in {1}".format(tool_names.util, runtime(util_start)))
	return ufeat_count

def update_bridge_wid(defbridge, allbridge):
	bridge_start = dt.now()
	if defbridge: write("\n--- {0} ---\n".format(tool_names.defbridge))
	if allbridge: write("\n--- {0} ---\n".format(tool_names.allbridge))
	#~~~~~ Royal Decree Variables ~~~~~
	total_bridges = 0
	updated_bridge_wids = 0
	updated_bridge_ctuus = 0
	remaining_default_bridges = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	trans_crv = 'TransportationGroundCrv'
	bridge_crv_lyr = 'bridge_crv_lyr'
	roads_lyr = 'roads'
	cart_tracks_lyr = 'cart_tracks'
	rails_lyr = 'rails'

	if defbridge and trans_crv not in featureclass:
		if existential_panic(trans_crv, tool_names.defbridge):
			return total_bridges, updated_bridge_wids, updated_bridge_ctuus, remaining_default_bridges
		else:
			return total_bridges, updated_bridge_wids, updated_bridge_ctuus, remaining_default_bridges
	if allbridge and trans_crv not in featureclass:
		if existential_panic(trans_crv, tool_names.allbridge):
			return total_bridges, updated_bridge_wids, updated_bridge_ctuus, remaining_default_bridges
		else:
			return total_bridges, updated_bridge_wids, updated_bridge_ctuus, remaining_default_bridges

	# Pull width and geometry fields for Bridges, Roads, Cart Tracks, Railways, and Railway Sidetracks
	bridge_fields = ['WID', 'ZI026_CTUU', 'SHAPE@']
	road_fields = ['ZI016_WD1', 'ZI026_CTUU', 'SHAPE@']
	cart_track_fields = ['WID', 'ZI026_CTUU', 'SHAPE@']
	rail_fields = ['ZI017_GAW', 'ZI026_CTUU', 'SHAPE@']

	if defbridge: # Only checks Bridges and Tunnels with default WID against Trans features that have a populated width value
		# Convert the feature classes from the TDS into usable layers
		lyr_start = dt.now()
		write("Making feature layers...")
		make_lyr(trans_crv, bridge_crv_lyr, "F_CODE IN ('AQ040', 'AQ130') AND WID <= 0 AND {0}".format(where_scale))
		make_lyr(trans_crv, "road_crv_lyr", "F_CODE IN ('AP030') AND ZI016_WD1 > 0 AND {0}".format(where_scale))
		make_lyr(trans_crv, "cart_crv_lyr", "F_CODE IN ('AP010') AND WID > 0 AND {0}".format(where_scale))
		make_lyr(trans_crv, "rail_crv_lyr", "F_CODE IN ('AN010', 'AN050') AND ZI017_GAW > 0 AND {0}".format(where_scale))
		write("Successfully made the feature layers in {0}\n".format(runtime(lyr_start)))

	if allbridge: # Checks all Bridges and Tunnels against Trans features even if they don't have populated width values
		# Convert the feature classes from the TDS into usable layers
		lyr_start = dt.now()
		write("Making feature layers...")
		make_lyr(trans_crv, bridge_crv_lyr, "F_CODE IN ('AQ040', 'AQ130') AND {0}".format(where_scale))
		make_lyr(trans_crv, "road_crv_lyr", "F_CODE IN ('AP030') AND {0}".format(where_scale))
		make_lyr(trans_crv, "cart_crv_lyr", "F_CODE IN ('AP010') AND {0}".format(where_scale))
		make_lyr(trans_crv, "rail_crv_lyr", "F_CODE IN ('AN010', 'AN050') AND {0}".format(where_scale))
		write("Successfully made the feature layers in {0}\n".format(runtime(lyr_start)))

	# Select Trans features that share a curve with the Bridges/Tunnels above
	select_by_loc("road_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", bridge_crv_lyr, "", "NEW_SELECTION")
	select_by_loc("cart_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", bridge_crv_lyr, "", "NEW_SELECTION")
	select_by_loc("rail_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", bridge_crv_lyr, "", "NEW_SELECTION")
	# Make Trans layers for each type
	make_lyr("road_crv_lyr", roads_lyr)
	make_lyr("cart_crv_lyr", cart_tracks_lyr)
	make_lyr("rail_crv_lyr", rails_lyr)

	### bridge_crv_lyr - Bridges and Tunnels at user specified scale
	### roads - Roads at user specified scale that share a line segment with bridge_crv_lyr
	### cart_tracks - Cart Tracks at user specified scale that share a line segment with bridge_crv_lyr
	### rails - Railways and Railway Sidetracks at user specified scale that share a line segment with bridge_crv_lyr

	# Gets a count of selected Bridges, Roads, and Rails
	total_bridges = get_count(bridge_crv_lyr)
	select_by_att(bridge_crv_lyr, "NEW_SELECTION", "WID <= 0")
	total_default_bridges = get_count(bridge_crv_lyr)
	select_by_att(bridge_crv_lyr, "CLEAR_SELECTION")
	total_roads = get_count(roads_lyr)
	total_cart_tracks = get_count(cart_tracks_lyr)
	total_rails = get_count(rails_lyr)

	# Error handling. If 0 Bridges selected, the script breaks
	if not total_bridges:
		greentext("No Bridges or Tunnels found.")
		if defbridge: write("{0} finished in {1}".format(tool_names.defbridge, runtime(bridge_start)))
		if allbridge: write("{0} finished in {1}".format(tool_names.allbridge, runtime(bridge_start)))
		return total_bridges, updated_bridge_wids, updated_bridge_ctuus, remaining_default_bridges
	# Error handling. If no Roads or Rails to select against, likely something will break
	if not total_roads and not total_cart_tracks and not total_rails:
		greentext("{0} Bridges and Tunnels found.".format(total_bridges))
		greentext("** No underlying Roads, Cart Tracks, Railways, or Railway Sidetracks for Bridges and Tunnels. **\n** The Bridges and Tunnels are either not coincident or missing an underlying Transportation feature. **")
		if defbridge: write("{0} finished in {1}".format(tool_names.defbridge, runtime(bridge_start)))
		if allbridge: write("{0} finished in {1}".format(tool_names.allbridge, runtime(bridge_start)))
		return total_bridges, updated_bridge_wids, updated_bridge_ctuus, remaining_default_bridges

	# Announces the features found
	write("{0} Bridges and Tunnels found.".format(total_bridges))
	write("{0} of the Bridges and Tunnels have default WID = -999999.".format(total_default_bridges))
	write("{0} Roads share a line segment with the Bridges and Tunnels.".format(total_roads))
	write("{0} Cart Tracks share a line segment with the Bridges and Tunnels.".format(total_cart_tracks))
	write("{0} Railways and Railway Sidetracks share a line segment with the Bridges and Tunnels.".format(total_rails))
	write("These Bridges and Tunnels will have their width and CTUU compared against the underlying Transportation features and will be updated accordingly.\n")

	road_bridges_updated = 0
	cart_bridges_updated = 0
	rail_bridges_updated = 0
	if total_bridges: # Double check that there are Bridges/Tunnels to work on
		write("Primary Loop Engaged...")
		# Loop to update Bridge/Tunnel width and CTUU to it's corresponding Road width and CTUU
		if total_roads:
			ap.SetProgressorLabel("Updating WID and CTUU for Bridges and Tunnels on Roads...")
			with ap.da.UpdateCursor(bridge_crv_lyr, bridge_fields) as u_road_bridges: # UpdateCursor for Bridges/Tunnels with width, CTUU, and geometry
				for abridge in u_road_bridges:
					with ap.da.SearchCursor(roads_lyr, road_fields) as s_roads: # SearchCursor for roads with width, CTUU, and geometry
						for road in s_roads:
							if abridge[-1].overlaps(road[-1]) or abridge[-1].equals(road[-1]): # Check if Bridge/Tunnel shares curve with Road (if not working test contains\within)
								if abridge[0] < road[0]:
									abridge[0] = int(road[0]*1.5) # Sets current Bridge/Tunnel width to Road width * [factor]
									road_bridges_updated += 1
								if abridge[1] != road[1]:
									abridge[1] = road[1] # Sets current Bridge/Tunnel CTUU to match the Rail CTUU
									updated_bridge_ctuus += 1
					u_road_bridges.updateRow(abridge)
			write("{0} Bridges or Tunnels with WID less than Road WD1 were updated.".format(road_bridges_updated))

		# Loop to update Bridge/Tunnel width and CTUU to it's corresponding Cart Track width and CTUU
		if total_cart_tracks:
			ap.SetProgressorLabel("Updating WID and CTUU for Bridges and Tunnels on Cart Tracks...")
			with ap.da.UpdateCursor(bridge_crv_lyr, bridge_fields) as u_cart_bridges: # UpdateCursor for Bridges/Tunnels with width, CTUU, and geometry
				for abridge in u_cart_bridges:
					with ap.da.SearchCursor(cart_tracks_lyr, cart_track_fields) as s_cart_tracks: # SearchCursor for Cart Tracks with width, CTUU, and geometry
						for cart_track in s_cart_tracks:
							if abridge[-1].overlaps(cart_track[-1]) or abridge[-1].equals(cart_track[-1]): # Check if Bridge/Tunnel shares curve with Cart Track (if not working test contains\within)
								if abridge[0] < cart_track[0]:
									abridge[0] = int(cart_track[0]*1.5) # Sets current Bridge/Tunnel width to Cart Track width * [factor]
									cart_bridges_updated += 1
								if abridge[1] != cart_track[1]:
									abridge[1] = cart_track[1] # Sets current Bridge/Tunnel CTUU to match the Rail CTUU
									updated_bridge_ctuus += 1
					u_cart_bridges.updateRow(abridge)
			write("{0} Bridges or Tunnels with WID less than Cart Track WID were updated.".format(cart_bridges_updated))

		# Loop to update Bridge/Tunnel width and CTUU to it's corresponding Rail width and CTUU
		if total_rails:
			ap.SetProgressorLabel("Updating WID and CTUU for Bridges and Tunnels on Railways...")
			with ap.da.UpdateCursor(bridge_crv_lyr, bridge_fields) as u_rail_bridges: # UpdateCursor for Bridges/Tunnels with width, CTUU, and geometry
				for abridge in u_rail_bridges:
					with ap.da.SearchCursor(rails_lyr, rail_fields) as s_rails: # SearchCursor for Rails with width, CTUU, and geometry
						for rail in s_rails:
							if abridge[-1].overlaps(rail[-1]) or abridge[-1].equals(rail[-1]): # Check if Bridge/Tunnel shares curve with Rail (if not working test contains\within)
								if abridge[0] < rail[0]:
									abridge[0] = int(rail[0])+1 # Sets current Bridge/Tunnel width to integer rounded Rail gauge width + [value]
									rail_bridges_updated += 1
								if abridge[1] != rail[1]:
									abridge[1] = rail[1] # Sets current Bridge/Tunnel CTUU to match the Rail CTUU
									updated_bridge_ctuus += 1
					u_rail_bridges.updateRow(abridge)
			write("{0} Bridges or Tunnels with WID less than Railway or Railway Sidetrack GAW were updated.".format(rail_bridges_updated))
		write("{0} Bridges or Tunnels with CTUU not matching the underlying Transportation feature were updated.".format(updated_bridge_ctuus))
	write(" ")

	# Final messages of the state of the data after tool completion
	select_by_att(bridge_crv_lyr, "NEW_SELECTION", "WID <= 0")
	remaining_default_bridges = get_count(bridge_crv_lyr)
	select_by_att(bridge_crv_lyr, "CLEAR_SELECTION")
	updated_bridge_wids = road_bridges_updated + cart_bridges_updated + rail_bridges_updated

	if remaining_default_bridges > 0:
		greentext("** {0} Bridges or Tunnels remaining with default WID = -999999. **\n** The default Bridges and Tunnels are either not coincident or missing an underlying Transportation feature. **".format(remaining_default_bridges))
	greentext("{0} WID values and {1} CTUU values updated for Bridges and Tunnels in {2}".format(updated_bridge_wids, updated_bridge_ctuus, runtime(bridge_start)))

	return total_bridges, updated_bridge_wids, updated_bridge_ctuus, remaining_default_bridges

def update_pylong_hgt(defpylong, allpylong):
	pylong_start = dt.now()
	if defpylong: write("\n--- {0} ---\n".format(tool_names.defpylong))
	if allpylong: write("\n--- {0} ---\n".format(tool_names.allpylong))
	#~~~~~ Royal Decree Variables ~~~~~
	total_pylons = 0
	updated_pylon_hgts = 0
	updated_pylon_ctuus = 0
	remaining_default_pylons = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	util_pnt = 'UtilityInfrastructurePnt'
	util_crv = 'UtilityInfrastructureCrv'
	utility_pnt_lyr = 'utility_pnt_lyr'
	utility_crv_lyr = 'utility_crv_lyr'
	pylons_on_cables_lyr = 'pylons_on_cables'

	if defpylong and (util_pnt not in featureclass or util_crv not in featureclass):
		if existential_panic(util_pnt, tool_names.defpylong) or existential_panic(util_crv, tool_names.defpylong):
			return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons
		else:
			return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons
	if allpylong and (util_pnt not in featureclass or util_crv not in featureclass):
		if existential_panic(util_pnt, tool_names.allpylong) or existential_panic(util_crv, tool_names.allpylong):
			return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons
		else:
			return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons

	# if util_pnt not in featureclass or util_crv not in featureclass:
	# 	if ap.Exists(util_pnt) or ap.Exists(util_crv):
	# 		greentext("Either {0} or {1} has no features. Moving on.".format(util_pnt, util_crv))
	# 	else:
	# 		if defpylong: oops("\n*** Failed to run {0} ***".format(tool_names.defpylong))
	# 		if allpylong: oops("\n*** Failed to run {0} ***".format(tool_names.pylong))
	# 		oops("{0} or {1} feature class missing\n".format(util_pnt, util_crv))
	# 	return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons

	# Pull height, CTUU, and geometry fields
	util_fields = ['HGT', 'ZI026_CTUU', 'SHAPE@']

	if defpylong: # Only checks Pylons with default HGT against Cable features that have a populated HGT
		# Convert the feature classes from the TDS into usable layers
		lyr_start = dt.now()
		write("Making feature layers...")
		make_lyr(util_pnt, utility_pnt_lyr, "F_CODE = 'AT042' AND HGT <= 0 AND {0}".format(where_scale))
		make_lyr(util_crv, utility_crv_lyr, "F_CODE = 'AT005' AND HGT > 0 AND {0}".format(where_scale))
		write("Successfully made the feature layers in {0}\n".format(runtime(lyr_start)))

	if allpylong:
		# Convert the feature classes from the TDS into usable layers
		lyr_start = dt.now()
		write("Making feature layers...")
		make_lyr(util_pnt, utility_pnt_lyr, "F_CODE = 'AT042' AND {0}".format(where_scale))
		make_lyr(util_crv, utility_crv_lyr, "F_CODE = 'AT005' AND HGT > 0 AND {0}".format(where_scale))
		write("Successfully made the feature layers in {0}\n".format(runtime(lyr_start)))

	# Select Pylons that intersect the Cables
	select_by_loc(utility_pnt_lyr, "INTERSECT", utility_crv_lyr, "", "NEW_SELECTION")
	# Make these selections into layers
	make_lyr(utility_pnt_lyr, pylons_on_cables_lyr)
	select_by_att(utility_pnt_lyr, "CLEAR_SELECTION")

	### utility_pnt_lyr - Pylons at user specified scale
	### utility_crv_lyr - Cables with HGT greater than 0
	### pylons_on_cables - Pylons that intersect Cables

	# Gets a count of selected Pylons and Cables
	total_pylons = get_count(utility_pnt_lyr)
	total_cables = get_count(utility_crv_lyr)
	total_pylons_on_cables = get_count(pylons_on_cables_lyr)
	select_by_att(utility_pnt_lyr, "NEW_SELECTION", "HGT <= 0")
	total_default_pylons = get_count(utility_pnt_lyr)
	select_by_att(utility_pnt_lyr, "CLEAR_SELECTION")

	# Error handling. If 0 Pylons selected the script breaks
	if not total_pylons_on_cables:
		greentext("No Pylons intersecting Cables found.")
		if defpylong: write("{0} finished in {1}".format(tool_names.defpylong, runtime(pylong_start)))
		if allpylong: write("{0} finished in {1}".format(tool_names.allpylong, runtime(pylong_start)))
		return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons
	# Error handling. If no Cables to select against, likely something will break
	if not total_cables:
		greentext("No Cables with height values found.")
		if defpylong: write("{0} finished in {1}".format(tool_names.defpylong, runtime(pylong_start)))
		if allpylong: write("{0} finished in {1}".format(tool_names.allpylong, runtime(pylong_start)))
		return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons

	# Announces the features found
	write("{0} Pylons found.".format(total_pylons))
	write("{0} of the Pylons have default HGT = -999999.".format(total_default_pylons))
	write("{0} Cables with height values found.".format(total_cables))
	write("{0} Pylons are intersecting Cables.".format(total_pylons_on_cables))
	write("These Pylons will have their height and CTUU compared against the intersecting Cables and will be updated accordingly.\n")

	if total_pylons_on_cables: # Double check that there are intersecting Pylons to work on
		ap.SetProgressorLabel("Updating HGT and CTUU for Pylons on Cables...")
		write("Primary Loop Engaged...")
		# Loop to update Pylon HGT and CTUU to it's corresponding Cable HGT and CTUU
		with ap.da.UpdateCursor(pylons_on_cables_lyr, util_fields) as u_pylons_on_cables: # UpdateCursor for Pylons with height, CTUU, and geometry
			for pylon in u_pylons_on_cables:
				with ap.da.SearchCursor(utility_crv_lyr, util_fields) as s_cables: # SearchCursor for Cables with height, CTUU, and geometry
					for cable in s_cables:
						if not pylon[-1].disjoint(cable[-1]): # Check if Pylon intersects a Cable
							if pylon[0] != cable[0]:
								pylon[0] = cable[0] # Sets current Pylon HGT to intersecting Cable's HGT
								updated_pylon_hgts += 1
							if pylon[1] != cable[1]:
								pylon[1] = cable[1] # Sets current Pylon CTUU to intersecting Cable's CTUU
								updated_pylon_ctuus += 1
				u_pylons_on_cables.updateRow(pylon)
		write("{0} Pylons with HGT not matching intersecting Cable HGT were updated.".format(updated_pylon_hgts))
		write("{0} Pylons with CTUU not matching intersecting Cable CTUU were updated.".format(updated_pylon_ctuus))
		write("(Totals may vary if Pylons intersect multiple Cables.)")
	write(" ")

	# Final messages of the state of the data after tool completion
	select_by_att(utility_pnt_lyr, "NEW_SELECTION", "HGT <= 0")
	remaining_default_pylons = get_count(utility_pnt_lyr)
	select_by_att(utility_pnt_lyr, "CLEAR_SELECTION")

	if remaining_default_pylons > 0:
		greentext("** {0} Pylons remaining with default HGT = -999999. **\n** The default Pylons are not snapped, missing a Cable, or the underlying Cable doesn't have a height.".format(remaining_default_pylons))
	greentext("{0} HGT values and {1} CTUU values updated for Pylons in {2}".format(updated_pylon_hgts, updated_pylon_ctuus, runtime(pylong_start)))

	return total_pylons, updated_pylon_hgts, updated_pylon_ctuus, remaining_default_pylons

def populate_woc(defdam, alldam):
	dam_start = dt.now()
	if defdam: write("\n--- {0} ---\n".format(tool_names.defdam))
	if alldam: write("\n--- {0} ---\n".format(tool_names.alldam))
	#~~~~~ Royal Decree Variables ~~~~~
	total_dams = 0
	updated_dams = 0
	dams_without_trans = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	hydro_srf = "HydrographySrf"
	trans_crv = "TransportationGroundCrv"
	dams_lyr = "dams_lyr"
	trans_lyr = "trans_lyr"

	if defdam and (hydro_srf not in featureclass or trans_crv not in featureclass):
		if existential_panic(hydro_srf, tool_names.defdam) or existential_panic(trans_crv, tool_names.defdam):
			return total_dams, updated_dams, dams_without_trans
		else:
			return total_dams, updated_dams, dams_without_trans
	if alldam and (hydro_srf not in featureclass or trans_crv not in featureclass):
		if existential_panic(hydro_srf, tool_names.alldam) or existential_panic(trans_crv, tool_names.alldam):
			return total_dams, updated_dams, dams_without_trans
		else:
			return total_dams, updated_dams, dams_without_trans

	# if hydro_srf not in featureclass or trans_crv not in featureclass:
	# 	if ap.Exists(hydro_srf) or ap.Exists(trans_crv):
	# 		greentext("Either {0} or {1} has no features. Moving on.".format(hydro_srf, trans_crv))
	# 	else:
	# 		if defdam: oops("\n*** Failed to run {0} ***".format(tool_names.defdam))
	# 		if alldam: oops("\n*** Failed to run {0} ***".format(tool_names.alldam))
	# 		oops("{0} or {1} feature classes missing\n".format(hydro_srf, trans_crv))
	# 	return total_dams, updated_dams, dams_without_trans

	# Important values
	sub_field = "fcsubtype"
	sub_dam_s = 100330                # Dam_S
	sub_cart_track = 100150           # CartTrack_C
	sub_road = 100152                 # Road_C
	sub_railway = 100143              # Railway_C
	sub_railway_sidetrack = 100144    # Railway_Sidetrack_C

	# Define lists of fields for the process below.
	hydro_fields = ['WOC', 'TRS', 'SHAPE@']
	trans_fields = ['LTN', 'fcsubtype', 'ZI017_GAW', 'SHAPE@']

	# Preprocessing logic
	lyr_start = dt.now()
	write("Making feature layers...")
	if defdam:
		# fcsubtype = 100330 AND WOC < 0 AND zi026_ctuu >= scale
		dam_clause = """{0} = {1} AND {2} < 0 AND {3}""".format(field_delim(hydro_srf, sub_field), sub_dam_s, 'WOC', where_scale)
	if alldam:
		# fcsubtype = 100330 AND zi026_ctuu >= scale
		dam_clause = """{0} = {1} AND {2}""".format(field_delim(hydro_srf, sub_field), sub_dam_s, where_scale)

	# fcsubtype in (100150, 100152, 100143, 100144) AND ltn > 0 AND zi026_ctuu >= scale
	trans_clause = """{0} in ({1}, {2}, {3}, {4}) AND {5} > 0 AND {6}""".format(field_delim(trans_crv, sub_field), sub_cart_track, sub_road, sub_railway, sub_railway_sidetrack, 'ltn', where_scale)

	make_lyr(hydro_srf, dams_lyr, dam_clause)
	make_lyr(trans_crv, trans_lyr, trans_clause)
	write("Successfully made the feature layers in {0}\n".format(runtime(lyr_start)))

	# Define counter to report counts to user
	total_dams = get_count(dams_lyr)
	total_trans = get_count(trans_lyr)
	select_by_loc(trans_lyr, "INTERSECT", dams_lyr)
	total_trans_on_dams = get_count(trans_lyr)
	select_by_att(dams_lyr, "NEW_SELECTION", "WOC <= 0")
	total_default_woc = get_count(dams_lyr)
	select_by_att(dams_lyr, "CLEAR_SELECTION")
	select_by_att(dams_lyr, "NEW_SELECTION", "TRS NOT IN (8, 9, 12, 13)")
	total_default_trs = get_count(dams_lyr)
	select_by_att(dams_lyr, "CLEAR_SELECTION")

	# Error handling. If 0 Dams selected, the script breaks
	if not total_dams:
		greentext("No Dams found.")
		if defdam: write("{0} finished in {1}".format(tool_names.defdam, runtime(dam_start)))
		if alldam: write("{0} finished in {1}".format(tool_names.alldam, runtime(dam_start)))
		return total_dams, updated_dams, dams_without_trans
	if not total_trans_on_dams:
		greentext("{0} Dams found.".format(total_dams))
		greentext("No underlying Roads, Cart Tracks, Railways, or Railway Sidetracks for Dams.\nThe Dams are either not coincident or missing an underlying Transportation feature.")

	write("{0} Dam surfaces found".format(total_dams))
	write("{0} Trans curves found".format(total_trans))
	write("{0} of the Dams have default WOC.".format(total_default_woc))
	write("{0} of the Dams have default TRS.".format(total_default_trs))
	write("{0} Transportation features are intersecting Dams.".format(total_trans_on_dams))
	write("These Dams will have their Width of Crest and Transportation System compared against the intersecting Transportation features and will be updated accordingly.\n")

	total_car_intersects = 0
	total_train_intersects = 0
	total_updated_no_trans = 0
	if total_dams: # Double check that there are Dams to work on
		ap.SetProgressorLabel("Updating WOC and TRS on Dams...")
		write("\nPrimary Loop Engaged...")
		with ap.da.UpdateCursor(dams_lyr, hydro_fields) as dams: # [0]-WOC, [1]-TRS, [-1]-SHAPE@
			for dam in dams:
				with ap.da.SearchCursor(trans_lyr, trans_fields) as trans: # [0]-LTN, [1]-FCSubtype, [2]-ZI017_GAW, [-1]-SHAPE@
					for tran in trans:
						if not dam[-1].disjoint(tran[-1]): # if Dam geometry intersects Trans geometry
							if populated(dam[0]): # if Dam WOC is populated
								if not populated(dam[1]): # if Dam TRS is NOT populated
									if tran[1] == sub_cart_track or tran[1] == sub_road: # if FCSubtype is Cart Track or Road
										dam[1] = 13 # TRS = "Road"
										dams.updateRow(dam) # update current Dam record
										total_car_intersects += 1
										break
									elif tran[1] == sub_railway or tran[1] == sub_railway_sidetrack: # else if FCSubtype is Railway or Railway Sidetrack
										dam[1] = 12 # TRS = "Railway"
										dams.updateRow(dam) # update current Dam record
										total_train_intersects += 1
										break
								break
							# else if dam WOC is NOT populated
							elif tran[1] == sub_cart_track or (tran[1] == sub_road and tran[0] == 1): # else if FCSubtype is Cart Track or Road with 1 lane
								dam[0] = 5 # WOC = 5 meters
								dam[1] = 13 # TRS = "Road"
								dams.updateRow(dam) # update current Dam record
								total_car_intersects += 1
								break
							elif tran[1] == sub_railway or tran[1] == sub_railway_sidetrack: # else if FCSubtype is Railway or Railway Sidetrack
								dam[0] = round(tran[2] +2) # WOC = ZI017_GAW + 2 (rounded)
								dam[1] = 12 # TRS = "Railway"
								dams.updateRow(dam) # update current Dam record
								total_train_intersects += 1
								break
							else: # else FCSubtype must be Road with more than 1 lane
								dam[0] = tran[0] * 2.5 + 2 # WOC = LTN * 2.5 + 2
								dam[1] = 13 # TRS = "Road"
								dams.updateRow(dam) # update current Dam record
								total_car_intersects += 1
								break
						else: # else dam geometry does NOT intersect Trans geometry
							dams_without_trans += 1
							if not populated(dam[0]) or not populated(dam[1]):
								total_updated_no_trans += 1
							if not populated(dam[0]):
								dam[0] = 5 # WOC = 5 meters
								dams.updateRow(dam) # update current Dam record
							if not populated(dam[1]): # if TRS is NOT populated
								dam[1] = 8 # TRS = "No Transportation System"
								dams.updateRow(dam) # update current Dam record

	write("{0} Dam surfaces intersecting Roads and Cart Tracks were updated.".format(total_car_intersects))
	write("{0} Dam surfaces intersecting Railways and Railway Sidetracks were updated.".format(total_train_intersects))
	write("{0} Dam surfaces not intersecting any Transportation features.".format(dams_without_trans))
	write("{0} Dam surfaces with no Transportation System were updated.".format(total_updated_no_trans))

	select_by_att(dams_lyr, "NEW_SELECTION", "WOC <= 0")
	remaining_default_woc = get_count(dams_lyr)
	select_by_att(dams_lyr, "CLEAR_SELECTION")
	select_by_att(dams_lyr, "NEW_SELECTION", "TRS NOT IN (8, 9, 12, 13)")
	remaining_default_trs = get_count(dams_lyr)
	select_by_att(dams_lyr, "CLEAR_SELECTION")
	updated_dams = total_car_intersects + total_train_intersects + total_updated_no_trans

	if remaining_default_woc > 0:
		greentext("** {0} Dams remaining with default WOC. **\n** There may be geometry issues with these Dams. **".format(remaining_default_woc))
	if remaining_default_trs > 0:
		greentext("** {0} Dams remaining with default or nonstandard TRS. **\n** These Dams may be attributed with an uncommon Transportation System. **".format(remaining_default_trs))
	greentext("\n{0} WOC and TRS values updated for Dam surfaces in {1}".format(updated_dams, runtime(dam_start)))

	return total_dams, updated_dams, dams_without_trans

def buildings_in_buas():
	# Initialize task
	building_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.building))
	#~~~~~ Royal Decree Variables ~~~~~
	bua_count = 0
	total_2upscale = 0
	total_2descale = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	settlement_srf = 'SettlementSrf'
	structure_srf = 'StructureSrf'
	structure_pnt = 'StructurePnt'

	#if fc not in featureclass:
	#	if existential_panic(fc, tool_names.xxx):
	#		return tool_variables
	#	else:
	#		pass or return tool_variables

	if settlement_srf not in featureclass:
		if existential_panic(settlement_srf, tool_names.building):
			return bua_count, total_2upscale, total_2descale
		else:
			return bua_count, total_2upscale, total_2descale
	if structure_srf not in featureclass and structure_pnt not in featureclass:
		if existential_panic(structure_srf, tool_names.building) and existential_panic(structure_pnt, tool_names.building):
			return bua_count, total_2upscale, total_2descale
		else:
			return bua_count, total_2upscale, total_2descale

	# if not ap.Exists(settlement_srf): # Task can't run if SettlementSrf fc is missing
	# 	oops("\n*** Failed to run {0} ***".format(tool_names.building))
	# 	oops("SettlementSrf feature class missing\n")
	# 	return bua_count, total_2upscale, total_2descale
	# if not ap.Exists(structure_srf) and not ap.Exists(structure_pnt): # Task can't run if both StructureSrf and StructurePnt fcs are missing. Only one is fine.
	# 	oops("\n*** Failed to run {0} ***".format(tool_names.building))
	# 	oops("StructureSrf and StructurePnt feature classes missing\n")
	# 	return bua_count, total_2upscale, total_2descale

	# Intra-task variables
	total_2upscale_s = 0
	total_2descale_s = 0
	total_2upscale_p = 0
	total_2descale_p = 0
	update_field = 'ZI026_CTUU'
	bua_query = "F_CODE IN ('AL020') AND ZI026_CTUU >= 50000"
	building_query_2upscale = "F_CODE IN ('AL013') AND ZI026_CTUU < 50000"
	building_query_2descale = "F_CODE IN ('AL013') AND ZI026_CTUU >= 50000"
	#caci_ffn_query_2upscale = "FFN IN ({0}) OR HGT >= 46 OR LMC = 1001".format(", ".join(str(i) for i in ad.ffn_list_caci.values())) #dict_import
	#caci_ffn_query_2descale = "FFN NOT IN ({0}) AND HGT < 46 AND LMC <> 1001".format(", ".join(str(i) for i in ad.ffn_list_caci.values())) #dict_import
	ffn_query_2upscale = "FFN IN ({0}) OR HGT >= 46 OR LMC = 1001".format(", ".join(str(i) for i in ad.ffn_list_p10_combo.values())) #dict_import
	ffn_query_2descale = "FFN NOT IN ({0}) AND HGT < 46 AND LMC <> 1001".format(", ".join(str(i) for i in ad.ffn_list_p10_combo.values())) #dict_import

	#----------------------------------------------------------------------

	write("Retrieved Settlement and Structure feature classes")
	# Make layer of BUAs >= 50k
	make_lyr(settlement_srf, "buas", bua_query)
	#make_tbl("SettlementSrf", "buas", bua_query) # Cannot be used for geometry.
	write("Searching within BUAs")
	bua_count = get_count("buas")

	if not bua_count: # No BUAs to check against buildings. Wrap up task.
		greentext("\nNo BUAs found.")
		write("{0} finished in {1}".format(tool_names.building, runtime(building_start)))
		return bua_count, total_2upscale, total_2descale

	# Adam's original important ffn list for just building points: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
	write("Current project important Building FFNs list:")
	write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_p10_combo.items())) #dict_import
	write(" ")

	if ap.Exists(structure_srf): # Must check using Exists() in case both 'Skip Buildings' and 'Building in BUA Scaler' were checked
		if get_count(structure_srf): # If it exists, count the features. If there are more than 0, then continue with the task
			ap.SetProgressorLabel("Identifying important Building surfaces...")
			write("Identifying Building surfaces matching criteria...\n")
			if bool_dict[tool_names.vogon] and bool_dict[tool_names.disable]: # disable_editor_tracking() won't apply to StructureSrf and Pnt if Skip Buildings is checked. correct for that here.
				greentext("Disabling Editor Tracking for StructureSrf feature class.")
				ap.DisableEditorTracking_management(structure_srf)

			# Make layer of building surfaces < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr(structure_srf, "building_s_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_12.5k_within_2upscale", ffn_query_2upscale)

			# Make layer of building surfaces >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr(structure_srf, "building_s_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_50k+_within_2descale", ffn_query_2descale)

			total_2upscale_s = get_count("building_s_12.5k_within_2upscale")
			total_2descale_s = get_count("building_s_50k+_within_2descale")
			write("{0} below scale Building surfaces in {1} BUAs are important, tall, or interesting.\nThey will be scaled up.".format(total_2upscale_s, bua_count))
			write("{0} Building surfaces >= 50k in {1} BUAs are unimportant, short, and uninteresting.\nThey will be descaled.".format(total_2descale_s, bua_count))

			#-----------------------------------

			if total_2upscale_s:
				# Scale in important, tall, or landmark building surfaces within BUAs from below 50k to 250k (per PSG)
				ap.SetProgressorLabel("Upscaling important Building surfaces...")
				write("Setting below scale important, tall, or interesting Building surfaces to 250k...")
				with ap.da.UpdateCursor("building_s_12.5k_within_2upscale", update_field) as ucursor:
					for urow in ucursor:
						urow[0] = 250000
						ucursor.updateRow(urow)

			if total_2descale_s:
				# Descale unimportant, short, and uninteresting building surfaces within BUAs from 50k+ to 12.5k
				ap.SetProgressorLabel("Descaling unimportant Building surfaces...")
				write("Setting unimportant, short, and uninteresting Building surfaces to 12.5k...")
				with ap.da.UpdateCursor("building_s_50k+_within_2descale", update_field) as ucursor:
					for urow in ucursor:
						urow[0] = 12500
						ucursor.updateRow(urow)

			write(" ")

	if ap.Exists(structure_pnt):
		if get_count(structure_pnt): # If it exists, count the features. If there are more than 0, then continue with the task
			ap.SetProgressorLabel("Identifying important Building points...")
			write("Identifying Building points matching criteria...\n")
			if bool_dict[tool_names.vogon] and bool_dict[tool_names.disable]: # disable_editor_tracking() won't apply to StructureSrf and Pnt if Skip Buildings is checked. correct for that here.
				greentext("Disabling Editor Tracking for StructurePnt feature class.")
				ap.DisableEditorTracking_management(structure_pnt)

			# Make layer of building points < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr(structure_pnt, "building_p_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_12.5k_within_2upscale", ffn_query_2upscale)

			# Make layer of building points >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr(structure_pnt, "building_p_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_50k+_within_2descale", ffn_query_2descale)

			total_2upscale_p = get_count("building_p_12.5k_within_2upscale")
			total_2descale_p = get_count("building_p_50k+_within_2descale")
			write("{0} below scale Building points in {1} BUAs are important, tall, or interesting.\nThey will be scaled up.".format(total_2upscale_p, bua_count))
			write("{0} Building points >= 50k in {1} BUAs are unimportant, short, and uninteresting.\nThey will be descaled.".format(total_2descale_p, bua_count))

			#-----------------------------------

			if total_2upscale_p:
				# Scale in important, tall, or landmark building points within BUAs from below 50k to 50k
				ap.SetProgressorLabel("Upscaling important Building points...")
				write("Setting below scale important, tall, or interesting Building points to 50k...")
				with ap.da.UpdateCursor("building_p_12.5k_within_2upscale", update_field) as ucursor:
					for urow in ucursor:
						urow[0] = 50000
						ucursor.updateRow(urow)

			if total_2descale_p:
				# Descale unimportant, short, and uninteresting building points within BUAs from 50k+ to 12.5k
				ap.SetProgressorLabel("Descaling unimportant Building points...")
				write("Setting unimportant, short, and uninteresting Building points to 12.5k...")
				with ap.da.UpdateCursor("building_p_50k+_within_2descale", update_field) as ucursor:
					for urow in ucursor:
						urow[0] = 12500
						ucursor.updateRow(urow)

			write(" ")

	#----------------------------------------------------------------------

	# Count total buildings being upscaled and downscaled
	total_2upscale = total_2upscale_s + total_2upscale_p
	total_2descale = total_2descale_s + total_2descale_p

	# Clean up created layers
	clear_cache(["buas", "building_s_50k+", "building_s_50k+_within_2descale", "building_s_12.5k", "building_s_12.5k_within_2upscale"])

	write("{0} Building surfaces scaled to 250k.".format(total_2upscale_s))
	write("{0} Building surfaces scaled to 12.5k.".format(total_2descale_s))
	write("{0} Building points scaled to 50k.".format(total_2upscale_p))
	write("{0} Building points scaled to 12.5k.".format(total_2descale_p))
	greentext("\n{0} Buildings scaled up and {1} Buildings scaled down {2}".format(total_2upscale, total_2descale, runtime(building_start)))

	return bua_count, total_2upscale, total_2descale

def caci_swap():
	# Initialize task
	swap_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.swap))

	caci_schema, scale_name = snowflake_protocol() # Check for a CACI schema. Special actions are required for their custom nonsense.
	if not caci_schema:
		oops("CACI Swap Scale and CTUU was checked, but the provided TDS does not match CACI schema containing the 'Scale' field.\nCannot run CACI Swap Scale and CTUU")
		bool_dict[tool_names.swap] = False
		return
	else:
		greentext("CACI schema containing '{0}'' field identified".format(scale_name))

	featureclass_caci = featureclass
	if bool_dict[tool_names.vogon]:
		featureclass_caci.append('StructureSrf')
		featureclass_caci.append('StructurePnt')

	write("Swapping CTUU and Scale for {0}".format(gdb_name))
	write("\nNote: The SAX_RX9 field will be changed from <NULL> to 'Scale Swapped' after the first swap. It will flip back and forth in subsequent runs.\nIf the tool was aborted on a previous run for some reason, it will reset all feature classes to the dominant swap format to maintain internal consistency. It is still up to the user to know which format they were swapping from. (Either Scale->CTUU or CTUU->Scale) Check the tool output for more information on which feature classes were changed.\n")
	fields = ['zi026_ctuu', 'scale', 'swap', 'progress', 'sax_rx9']
	fields[1] = str(scale_name)

	write("\nChecking if any previous swaps were canceled. Please wait...")
	swap_fc = []
	none_fc = []
	empty_fc = featurerecess
	chk_fields = ['sax_rx9', 'scale']
	chk_fields[1] = str(scale_name)
	clean_proceed = False
	swap_dom = False
	none_dom = False
	for fc in featureclass_caci:
		if 'StructureSrf' in featureclass_caci or 'StructurePnt' in featureclass_caci:
			if not fc_counts[fc]:
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
	for fc in featureclass_caci:
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

	greentext("\n{0} finished in {1}".format(tool_names.swap, runtime(swap_start)))
	return



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



'''
╔══════════════════════════════════════╗
║ Title Formatting and Workspace Setup ║
╚══════════════════════════════════════╝
'''
#----------------------------------------------------------------------
# Sanitizing GDB name
gdb_name = re.findall(r"[\w']+", os.path.basename(os.path.split(TDS)[0]))[0]
rresults = os.path.split(os.path.split(TDS)[0])[0]


#----------------------------------------------------------------------
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

#-----------------------------------
# Report of requested tasks
write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

#-----------------------------------
# Easter Egg
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

if secret == 'Raven Queen':
	write(u"    |     As fortold by the ancient grimoires    {0}|".format(exs))
	write(u"    |      And she who guards the final veil     {0}|".format(exs))
	write(u"    |             ___                            {0}|".format(exs))
	write(u"    |            / _ \___ __  _____ ___          {0}|".format(exs))
	write(u"    |           / , _/ _ `/ |/ / -_) _ \         {0}|".format(exs))
	write(u"    |          /_/|_|\_,_/|___/\__/_//_/         {0}|".format(exs))
	write(u"    |            ____                            {0}|".format(exs))
	write(u"    |           / __ \__ _____ ___ ___           {0}|".format(exs))
	write(u"    |          / /_/ / // / -_) -_) _ \          {0}|".format(exs))
	write(u"    |          \___\_\_,_/\__/\__/_//_/          {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |        The following Finishing tasks       {0}|".format(exs))
	write(u"    |            shall meet their fate           {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))

#-----------------------------------
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
if bool_dict[tool_names.defbridge]:
	write(u"    |     - Default Bridge/Tunnel WID Updater    {0}|".format(exs))
if bool_dict[tool_names.defpylong]:
	write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
if bool_dict[tool_names.defdam]:
	write(u"    |     - Default Dam WOC Updater              {0}|".format(exs))
if bool_dict[tool_names.explode]:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
if bool_dict[tool_names.dups]:
	write(u"    |     - Delete Identical Features            {0}|".format(exs))
if bool_dict[tool_names.allbridge]:
	write(u"    |     - All Bridge/Tunnel WID Updater        {0}|".format(exs))
if bool_dict[tool_names.allpylong]:
	write(u"    |     - All Pylon HGT Updater                {0}|".format(exs))
if bool_dict[tool_names.alldam]:
	write(u"    |     - All Dam WOC Updater                  {0}|".format(exs))
if bool_dict[tool_names.building]:
	write(u"    |     - Building in BUA Scaler               {0}|".format(exs))
if bool_dict[tool_names.fcount]:
	write(u"    |     - Generate Feature Report              {0}|".format(exs))
if bool_dict[tool_names.vsource]:
	write(u"    |     - Generate Source Report               {0}|".format(exs))

#-----------------------------------
write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")


#----------------------------------------------------------------------
# refresh_extent() # Refreshes the extent polygon for the whole dataset
fc_counts, featureclass, featurerecess = create_fc_list() # Create the feature class list with the requested fcs
if bool_dict[tool_names.disable]:
	disable_editor_tracking(gdb_name) # Disables Editor Tracking for all feature classes
mem_grid = grid_chungus() # Create the extent polygon grid for partitioning the data
#check_defense('out') # Checks out the Defense Mapping extension. Only need for Calculate Metrics. Soon to be deprecated.
write("")



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



'''
╔════════════╗
║ Tool Tasks ║
╚════════════╝
'''
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Data Maintenance Tools Category   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Repair All NULL Geometry '''''''''
# Repairs all NULL geometries in each feature class
if bool_dict[tool_names.repair]:
	progress(tool_names.repair, '', 'start')
	try:
		repair_geometry()
	except ap.ExecuteError:
		writeresults(tool_names.repair)
	progress(tool_names.repair, '', 'stop')


#----------------------------------------------------------------------
''''''''' Populate F_Codes '''''''''
# Identifies bad F_Code/FCSubtype pairs and updates the F_Code value assuming correctly attributed FCSubtypes
# Refactored from John Jackson's Populate F_codes tool by Nat Cagle
if bool_dict[tool_names.fcode]:
	#~~~~~ Royal Decree Variables ~~~~~
	fcode_total = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.fcode, '', 'start')
	try:
		fcode_total = pop_fcode()
	except ap.ExecuteError:
		writeresults(tool_names.fcode)
	progress(tool_names.fcode, '', 'stop')


#----------------------------------------------------------------------
''''''''' Calculate Default Values '''''''''
# Calculates default values for all fields with NULL attributes
if bool_dict[tool_names.defaults]:
	progress(tool_names.defaults, '', 'start')
	try:
		process_defaults(featureclass)
	except ap.ExecuteError:
		writeresults(tool_names.defaults)
	progress(tool_names.defaults, '', 'stop')


#----------------------------------------------------------------------
''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields (LZN and ARA)
if bool_dict[tool_names.metrics]:
	progress(tool_names.metrics, '', 'start')
	try:
		calc_metrics()
	except ap.ExecuteError:
		writeresults(tool_names.metrics)
	progress(tool_names.metrics, '', 'stop')


#----------------------------------------------------------------------
''''''''' Update UFI Values '''''''''
# Iterate through all features and update the ufi field with uuid4 random values
if bool_dict[tool_names.ufi]:
	#~~~~~ Royal Decree Variables ~~~~~
	ufi_total = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.ufi, '', 'start')
	try:
		ufi_total = update_ufi()
		#Update UFI Values updated 0 invalid or missing UFI values in 0:20:9.3510
	except ap.ExecuteError:
		writeresults(tool_names.ufi)
	progress(tool_names.ufi, '', 'stop')



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Feature Specific Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Integrate and Repair Hydrography Features '''''''''
if bool_dict[tool_names.hydro]:
	#~~~~~ Royal Decree Variables ~~~~~
	hfeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.hydro, '', 'start')
	try:
		hfeat_count = integrate_hydro()
	except ap.ExecuteError:
		writeresults(tool_names.hydro)
	progress(tool_names.hydro, '', 'stop')


#----------------------------------------------------------------------
''''''''' Integrate and Repair TransportationGround Features '''''''''
if bool_dict[tool_names.trans]:
	#~~~~~ Royal Decree Variables ~~~~~
	tfeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.trans, '', 'start')
	try:
		tfeat_count = integrate_trans()
	except ap.ExecuteError:
		writeresults(tool_names.trans)
	progress(tool_names.trans, '', 'stop')


#----------------------------------------------------------------------
''''''''' Integrate and Repair UtilityInfrastructure Features '''''''''
if bool_dict[tool_names.util]:
	#~~~~~ Royal Decree Variables ~~~~~
	ufeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.util, '', 'start')
	try:
		ufeat_count = integrate_util()
	except ap.ExecuteError:
		writeresults(tool_names.util)
	progress(tool_names.util, '', 'stop')


#----------------------------------------------------------------------
''''''''' Default Bridge/Tunnel WID Updater '''''''''
# Checks for Bridges or Tunnels with WID <= Trans width or mismatched CTUUs and updates them to match the underlying Transportation feature
if bool_dict[tool_names.defbridge]:
	#~~~~~ Royal Decree Variables ~~~~~
	def_total_bridges = 0
	def_updated_bridge_wids = 0
	def_updated_bridge_ctuus = 0
	def_remaining_default_bridges = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.defbridge, '', 'start')
	try:
		def_total_bridges, def_updated_bridge_wids, def_updated_bridge_ctuus, def_remaining_default_bridges = update_bridge_wid(True, False)
	except ap.ExecuteError:
		writeresults(tool_names.defbridge)
	progress(tool_names.defbridge, '', 'stop')


#----------------------------------------------------------------------
''''''''' Default Pylon HGT Updater '''''''''
# Checks for Pylons with HGT or CTUU mismatched against intersecting Cables and updates them to match the intersecting Cable
if bool_dict[tool_names.defpylong]:
	#~~~~~ Royal Decree Variables ~~~~~
	def_total_pylons = 0
	def_updated_pylon_hgts = 0
	def_updated_pylon_ctuus = 0
	def_remaining_default_pylons = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.defpylong, '', 'start')
	try:
		def_total_pylons, def_updated_pylon_hgts, def_updated_pylon_ctuus, def_remaining_default_pylons = update_pylong_hgt(True, False)
	except ap.ExecuteError:
		writeresults(tool_names.defpylong)
	progress(tool_names.defpylong, '', 'stop')


#----------------------------------------------------------------------
''''''''' Default Dam WOC Updater '''''''''
# Iterate through Dam surfaces and compares against Trans curves. Updates the WOC and TRS if needed.
if bool_dict[tool_names.defdam]:
	#~~~~~ Royal Decree Variables ~~~~~
	def_total_dams = 0
	def_updated_dams = 0
	def_dams_without_trans = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.defdam, '', 'start')
	try:
		def_total_dams, def_updated_dams, def_dams_without_trans = populate_woc(True, False)
	except ap.ExecuteError:
		writeresults(tool_names.defdam)
	progress(tool_names.defdam, '', 'stop')



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Geometry Correction Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Hypernova Burst Multipart Features '''''''''
# Explodes all multipart features for an entire dataset
if bool_dict[tool_names.explode]:
	explode_start = dt.now()
	tool_name = 'Hypernova Burst Multipart Features'
	write("\n--- {0} ---\n".format(tool_name))
	progress(tool_names.explode, '', 'start')
	##### Multipart Search #####
	fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
	fc_multi_list = []
	total_multi = 0
	total_complex = 0
	# Identifying the true multipart features and separating from complex singlepart polygons flagged as multiparts
	for fc in featureclass:
		progress(tool_names.explode, fc, 'next')
		try:
			write("Searching for multipart features in {0}".format(fc))
			multipart = False # Assume the feature class doesn't have multiparts
			with ap.da.SearchCursor(fc, ['OID@', 'SHAPE@'], where_scale) as scursor:
				complex = 0 # Counts complex single part features
				for row in scursor: # For each feature in the fc
					shape = row[1] # Get SHAPE@ token to extract properties
					if shape is None: # Checks for NULL geometries
						greentext(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
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
			# Creates iterable list of feature classes that have multipart features
			fc_multi_list.append(fc)

	write(" ")
	if total_complex > 0:
		write("The {0} complex polygons found are single part polygons with complex interior holes that are more likely to become multipart features.".format(total_complex))
	write(" ")
	if fc_multi_list: # Only runs if fc_multi_list is not empty
		for fc in fc_multi_list:
			count = len(fc_multi[fc])
			total_multi += count
			greentext("{0} multipart features found in {1}".format(count, fc))
			#greentext("  OIDs - {0}".format(fc_multi[fc]))
		write(" ")

	##### Isolate, Explode, Replace #####
	in_class = "multi"
	out_class = "single"
	for fc in fc_multi_list:
		progress(tool_names.explode, fc, 'next')
		try:
			#sanitize feature class name from sde cz the sde always has to make things more difficult than they need to be...
			fc_parts = fc.split(".")
			if fc_parts[-1] in ad.fc_fields:  #dict_import
				fcr = fc_parts[-1]
			else:
				oops("** Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin. **")

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

			write("{0} multipart progenitor cores collapsing".format(fcr))
			multistart = dt.now()
			ap.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
			greentext("Hypernova burst detected after {0}".format(runtime(multistart)))

			write("Removing original multipart features")
			# Deletes features in fc that have OIDs flagged as multiparts
			with ap.da.UpdateCursor(fc, oid_field) as ucursor:
				for row in ucursor:
					if row[0] in oid_list:
						ucursor.deleteRow()

			write("Replacing with singlepart features")
			# Create search and insert cursor to insert new rows in fc from MultipartToSinglepart output out_class
			with ap.da.SearchCursor(out_class, fieldnames) as scursor:
				with ap.da.InsertCursor(fc, fieldnames) as icursor:
					for row in scursor:
						icursor.insertRow(row)

			write("Populating NULL fields with defaults and updating UFIs for the new single part features")
			query2 = "{0} IS NOT NULL".format(og_oid)
			make_lyr(fc, "exploded_features", query2)
			process_defaults(["exploded_features"])
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
		#ap.Delete_management(str(ap.env.workspace) + str("\\" + str(in_class)))
		#ap.Delete_management(str(ap.env.workspace) + str("\\" + str(out_class)))
		clear_cache([in_class, out_class, "exploded_features"])
	except:
		write("No in_class or out_class created. Or processing layers have already been cleaned up. Continuing...")
		pass
	progress(tool_names.explode, '', 'stop')
	greentext("{0} features exploded in {1}".format(total_multi, runtime(explode_start)))


#----------------------------------------------------------------------
''''''''' Delete Identical Features '''''''''
# Checks for features with identical geometry and PSG attribution and removes them
if bool_dict[tool_names.dups]:
	dups_start = dt.now()
	tool_name = 'Delete Identical Features'
	write("\n--- {0} ---\n".format(tool_name))
	progress(tool_names.dups, '', 'start')
	out_table = os.path.dirname(TDS) # Output directory for Find Identical # C:/Projects/njcagle/S1_C09C_20210427.gdb
	path = os.path.join(rresults, gdb_name) # Output dBASE table location # C:/Projects/njcagle/S1_C09C_20210427
	table_loc = "{0}.dbf".format(path) # C:/Projects/njcagle/R&D/__Thunderdome/S1_C09C_20210427.dbf
	write("Creating temporary output files:\n    - {0}.dbf\n    - {0}.dbf.xml\n    - {0}.cpg\n    - {0}.IN_FID.atx".format(gdb_name))
	dup_count = 0

	for fc in featureclass: # Loop feature classes and FindIdentical to get a count, then delete any found
		progress(tool_names.dups, fc, 'next')
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
	progress(tool_names.dups, '', 'stop')
	greentext("{0} duplicates removed in {1}".format(dup_count, runtime(dups_start)))

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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Preprocessing Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' All Bridge/Tunnel WID Updater '''''''''
# Checks for Bridges or Tunnels with WID <= Trans width or mismatched CTUUs and updates them to match the underlying Transportation feature
if bool_dict[tool_names.allbridge]:
	#~~~~~ Royal Decree Variables ~~~~~
	all_total_bridges = 0
	all_updated_bridge_wids = 0
	all_updated_bridge_ctuus = 0
	all_remaining_default_bridges = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.allbridge, '', 'start')
	try:
		all_total_bridges, all_updated_bridge_wids, all_updated_bridge_ctuus, all_remaining_default_bridges = update_bridge_wid(False, True)
	except ap.ExecuteError:
		writeresults(tool_names.allbridge)
	progress(tool_names.allbridge, '', 'stop')


#----------------------------------------------------------------------
''''''''' All Pylon HGT Updater '''''''''
# Checks for Pylons with HGT or CTUU mismatched against intersecting Cables and updates them to match the intersecting Cable
if bool_dict[tool_names.allpylong]:
	#~~~~~ Royal Decree Variables ~~~~~
	all_total_pylons = 0
	all_updated_pylon_hgts = 0
	all_updated_pylon_ctuus = 0
	all_remaining_default_pylons = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.allpylong, '', 'start')
	try:
		all_total_pylons, all_updated_pylon_hgts, all_updated_pylon_ctuus, all_remaining_default_pylons = update_pylong_hgt(False, True)
	except ap.ExecuteError:
		writeresults(tool_names.allpylong)
	progress(tool_names.allpylong, '', 'stop')


#----------------------------------------------------------------------
''''''''' All Dam WOC Updater '''''''''
# Iterate through Dam surfaces and compares against Trans curves. Updates the WOC and TRS if needed.
if bool_dict[tool_names.alldam]:
	#~~~~~ Royal Decree Variables ~~~~~
	all_total_dams = 0
	all_updated_dams = 0
	all_dams_without_trans = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.alldam, '', 'start')
	try:
		all_total_dams, all_updated_dams, all_dams_without_trans = populate_woc(False, True)
	except ap.ExecuteError:
		writeresults(tool_names.alldam)
	progress(tool_names.alldam, '', 'stop')


#----------------------------------------------------------------------
''''''''' Building in BUA Scaler '''''''''
# Descales buildings within BUAs that don't have important FFNs, have a height < 46m, and aren't navigation landmarks
# Scales in buildings within BUAs that do have important FFNs, have a height >= 46m, or are navigation landmarks
if bool_dict[tool_names.building]:
	#~~~~~ Royal Decree Variables ~~~~~
	bua_count = 0
	total_2upscale = 0
	total_2descale = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	progress(tool_names.building, '', 'start')
	try:
		bua_count, total_2upscale, total_2descale = buildings_in_buas()
	except ap.ExecuteError:
		writeresults(tool_names.building)
	progress(tool_names.building, '', 'stop')


#----------------------------------------------------------------------
''''''''' CACI Swap Scale and CTUU '''''''''
# Swaps the Scale field with the CTUU field so we can work normally with CACI data
# if bool_dict[tool_names.swap]:
# 	try:
# 		caci_swap()
# 	except ap.ExecuteError:
# 		writeresults(tool_names.swap)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Database Management Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Database Feature Report '''''''''
# Refactored from John Jackson's Feature_Itemized_Counter tool by Nat Cagle
while bool_dict[tool_names.fcount]:
	fcount_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.fcount))
	progress(tool_names.fcount, '', 'start')
	#~~~~~ Royal Decree Variables ~~~~~
	pnt_cnt = 0
	crv_cnt = 0
	srf_cnt = 0
	tots_f = 0
	hydro_cnt = 0
	trans_cnt = 0
	util_cnt = 0
	building_cnt = 0
	landcover_cnt = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# if not 'StructurePnt' in featureclass and ap.Exists('StructurePnt'):
	# 	featureclass.append(u'StructurePnt')
	# if not 'StructureSrf' in featureclass and ap.Exists('StructureSrf'):
	# 	featureclass.append(u'StructureSrf')
	featureclass_count = ap.ListFeatureClasses()
	featureclass_count.sort()

	# Define fields for Search Cursor
	fields = ["FCSubtype"]

	# Set up dictionary and exclusion list to track feature classes
	feat_dict = OrderedDict()
	exList = []
	# Retrieve date and time for output file label and report timestamp
	today = dt.now().date() # Same as datetime.date.today(), but datetime.datetime is already imported as dt. Keeping it simple. And shorten the import list
	time_stamp = dt.now().strftime("%Y_%m_%d_%H%M")
	current_time = dt.now().strftime("%H:%M:%S")
	# Define feature categories
	hydro_cat = 'Hydrography'
	trans_cat = 'Transportation'
	util_cat = 'Utility'
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
	write("Checking feature classes...")

	# Fill in dictionary with itemized feature subtype counts
	for i in featureclass_count:
		progress(tool_names.fcount, i, 'next')
		currFC = str(i)
		currShape = currFC[-3:]
		feat_dict[currFC]=[{},0]
		hydro_feat = False
		trans_feat = False
		util_feat = False
		if hydro_cat in currFC:
			hydro_feat = True
		if trans_cat in currFC:
			trans_feat = True
		if util_cat in currFC:
			util_feat = True
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
					if util_feat:
						util_cnt += 1

			except:
				# If FC does not have FCSubtype field put it on exclusion list
				write("**** {0} does not have required fields ****".format(currFC))
				exList.append(currFC)
				continue
		write("{0} features counted".format(currFC))
	progress(tool_names.fcount, '', 'stop')

	progress(tool_names.fcount, '', 'start')
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
							"Total Utility Features            :  ",str(util_cnt),"\n",
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

	progress(tool_names.fcount, '', 'stop')
	greentext("Feature Count Report created. File located in the same folder as the database:\n{0}\n".format(results))
	greentext("{0} finished in {1}".format(tool_names.fcount, runtime(fcount_start)))
	break


#----------------------------------------------------------------------
''''''''' Source Analysis Report '''''''''
# Refactored from John Jackson's Version_Source_Counter tool by Nat Cagle
while bool_dict[tool_names.vsource]:
	vsource_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.vsource))
	progress(tool_names.vsource, '', 'start')

	# if not 'StructurePnt' in featureclass and ap.Exists('StructurePnt'):
	# 	featureclass.append(u'StructurePnt')
	# if not 'StructureSrf' in featureclass and ap.Exists('StructureSrf'):
	# 	featureclass.append(u'StructureSrf')
	featureclass_source = ap.ListFeatureClasses()
	featureclass_source.sort()

	time_stamp = dt.now().strftime("%Y_%m_%d_%H%M")
	fields = ["Version","ZI001_SDP","ZI001_SDV","ZI001_SRT"]
	results_csv = "{0}\\{1}_Source_Count_{2}.csv".format(rresults, gdb_name, time_stamp)
	results_txt = "{0}\\{1}_Source_Count_{2}.txt".format(rresults, gdb_name, time_stamp)
	feat_dict = OrderedDict()
	write("Checking feature classes...")

	# Fill in dictionary with leveled counts: Version -> SDP -> SDV *optional SRT
	for i in featureclass_source:
		progress(tool_names.vsource, i, 'next')
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
	progress(tool_names.vsource, '', 'stop')

	progress(tool_names.vsource, '', 'start')
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

	progress(tool_names.vsource, '', 'stop')
	greentext("Source Analysis Reports created. Files located in the same folder as the database:\n{0}\n{1}\n".format(results_csv, results_txt))
	greentext("{0} finished in {1}".format(tool_names.vsource, runtime(vsource_start)))
	break



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



'''
╔═══════════════════════════════╗
║ Report Formatting and Wrap Up ║
╚═══════════════════════════════╝
'''
#----------------------------------------------------------------------
ap.SetProgressor("default", "Completed all specified Finishing tools. Please see output summary below.")
write("\n\nFreeing partition memory")
#check_defense('in') # Checks back in the Defense Mapping extension. Only need for Calculate Metrics. Soon to be deprecated.
arcdel("in_memory")

#----------------------------------------------------------------------
# Report of completed tasks
write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}{4}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

#-----------------------------------
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

if secret == 'Raven Queen':
	write(u"    |            The Matron of Ravens            {0}|".format(exs))
	write(u"    |     Goddess of death, fate, and winter     {0}|".format(exs))
	write(u"    |             ___                            {0}|".format(exs))
	write(u"    |            / _ \___ __  _____ ___          {0}|".format(exs))
	write(u"    |           / , _/ _ `/ |/ / -_) _ \         {0}|".format(exs))
	write(u"    |          /_/|_|\_,_/|___/\__/_//_/         {0}|".format(exs))
	write(u"    |            ____                            {0}|".format(exs))
	write(u"    |           / __ \__ _____ ___ ___           {0}|".format(exs))
	write(u"    |          / /_/ / // / -_) -_) _ \          {0}|".format(exs))
	write(u"    |          \___\_\_,_/\__/\__/_//_/          {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |       Reminds us to grieve the fallen      {0}|".format(exs))
	write(u"    |            But do not pity them            {0}|".format(exs))
	write(u"    |      Death is the natural end of life      {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))

#-----------------------------------
write(u"    |   =======  Processes  Completed  =======   {0}|".format(exs))
write(u"    |   {0}   {1}|".format(sspaces, exs))
if bool_dict[tool_names.loc]:
	write(u"    |     - Used 25k_LOC feature classes only    {0}|".format(exs))
if bool_dict[tool_names.vogon]:
	write(u"    |     - Buildings skipped                    {0}|".format(exs))
if bool_dict[tool_names.repair]:
	write(u"    |     - Repaired NULL Geometries             {0}|".format(exs))
if bool_dict[tool_names.fcode]:
	write(u"    |     - Populated F_Codes                    {0}|".format(exs))
	write(u"    |          {0} F_Code errors fixed       {1}{2}|".format(fcode_total, format_count(fcode_total), exs))
if bool_dict[tool_names.defaults]:
	write(u"    |     - Calculated Default Values            {0}|".format(exs))
if bool_dict[tool_names.metrics]:
	write(u"    |     - Calculated Metrics                   {0}|".format(exs))
if bool_dict[tool_names.ufi]:
	write(u"    |     - Updated UFI Values                   {0}|".format(exs))
	write(u"    |          {0} Invalid or missing UFIs   {1}{2}|".format(ufi_total, format_count(ufi_total), exs))
if bool_dict[tool_names.hydro] or bool_dict[tool_names.trans] or bool_dict[tool_names.util]:
	write(u"    |     - Integrated and Repaired:             {0}|".format(exs))
	if bool_dict[tool_names.hydro]:
		write(u"    |          {0} Hydro                     {1}{2}|".format(hfeat_count, format_count(hfeat_count), exs))
	if bool_dict[tool_names.trans]:
		write(u"    |          {0} Trans                     {1}{2}|".format(tfeat_count, format_count(tfeat_count), exs))
	if bool_dict[tool_names.util]:
		write(u"    |          {0} Utilities                 {1}{2}|".format(ufeat_count, format_count(ufeat_count), exs))
if bool_dict[tool_names.defbridge]:
	write(u"    |     - Default Bridge/Tunnel WID Updater    {0}|".format(exs))
	if not ap.Exists('TransportationGroundCrv'):
		oops(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		oops(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not def_total_bridges:
		greentext(u"    |          No Bridges or Tunnels found       {0}|".format(exs))
	else:
		write(u"    |          {0} WID values updated        {1}{2}|".format(def_updated_bridge_wids, format_count(def_updated_bridge_wids), exs))
		write(u"    |          {0} CTUU values updated       {1}{2}|".format(def_updated_bridge_ctuus, format_count(def_updated_bridge_ctuus), exs))
		write(u"    |          {0} Default WIDs still exist  {1}{2}|".format(def_remaining_default_bridges, format_count(def_remaining_default_bridges), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.defpylong]:
	write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
	if not ap.Exists('UtilityInfrastructurePnt') or not ap.Exists('UtilityInfrastructureCrv'):
		oops(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		oops(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not def_total_pylons:
		greentext(u"    |          No default pylons found           {0}|".format(exs))
	else:
		write(u"    |          {0} HGT values updated        {1}{2}|".format(def_updated_pylon_hgts, format_count(def_updated_pylon_hgts), exs))
		write(u"    |          {0} CTUU values updated       {1}{2}|".format(def_updated_pylon_ctuus, format_count(def_updated_pylon_ctuus), exs))
		write(u"    |          {0} Default HGTs still exist  {1}{2}|".format(def_remaining_default_pylons, format_count(def_remaining_default_pylons), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.defdam]:
	write(u"    |     - Default Dam WOC Updater              {0}|".format(exs))
	if not ap.Exists('HydrographySrf') or not ap.Exists('TransportationGroundCrv'):
		oops(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		oops(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not def_total_dams:
		greentext(u"    |          No Dam surfaces found             {0}|".format(exs))
	else:
		write(u"    |          {0} Dams' WOC or TRS updated  {1}{2}|".format(def_updated_dams, format_count(def_updated_dams), exs))
		write(u"    |          {0} Dams without Trans curves {1}{2}|".format(def_dams_without_trans, format_count(def_dams_without_trans), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.explode]:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
	write(u"    |          {0} Complex features found    {1}{2}|".format(total_complex, format_count(total_complex), exs))
	write(u"    |          {0} Features exploded         {1}{2}|".format(total_multi, format_count(total_multi), exs))
if bool_dict[tool_names.dups]:
	write(u"    |     - Deleted Identical Features           {0}|".format(exs))
	write(u"    |          {0} Duplicates found          {1}{2}|".format(dup_count, format_count(dup_count), exs))
if bool_dict[tool_names.allbridge]:
	write(u"    |     - All Bridge/Tunnel WID Updater        {0}|".format(exs))
	if not ap.Exists('TransportationGroundCrv'):
		oops(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		oops(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not all_total_bridges:
		greentext(u"    |          No Bridges or Tunnels found       {0}|".format(exs))
	else:
		write(u"    |          {0} WID values updated        {1}{2}|".format(all_updated_bridge_wids, format_count(all_updated_bridge_wids), exs))
		write(u"    |          {0} CTUU values updated       {1}{2}|".format(all_updated_bridge_ctuus, format_count(all_updated_bridge_ctuus), exs))
		write(u"    |          {0} Default WIDs still exist  {1}{2}|".format(all_remaining_default_bridges, format_count(all_remaining_default_bridges), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.allpylong]:
	write(u"    |     - All Pylon HGT Updater                {0}|".format(exs))
	if not ap.Exists('UtilityInfrastructurePnt') or not ap.Exists('UtilityInfrastructureCrv'):
		oops(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		oops(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not all_total_pylons:
		greentext(u"    |          No default pylons found           {0}|".format(exs))
	else:
		write(u"    |          {0} HGT values updated        {1}{2}|".format(all_updated_pylon_hgts, format_count(all_updated_pylon_hgts), exs))
		write(u"    |          {0} CTUU values updated       {1}{2}|".format(all_updated_pylon_ctuus, format_count(all_updated_pylon_ctuus), exs))
		write(u"    |          {0} Default HGTs still exist  {1}{2}|".format(all_remaining_default_pylons, format_count(all_remaining_default_pylons), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.alldam]:
	write(u"    |     - All Dam WOC Updater                  {0}|".format(exs))
	if not ap.Exists('HydrographySrf') or not ap.Exists('TransportationGroundCrv'):
		oops(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		oops(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not all_total_dams:
		greentext(u"    |          No Dam surfaces found             {0}|".format(exs))
	else:
		write(u"    |          {0} Dams' WOC or TRS updated  {1}{2}|".format(all_updated_dams, format_count(all_updated_dams), exs))
		write(u"    |          {0} Dams without Trans curves {1}{2}|".format(all_dams_without_trans, format_count(all_dams_without_trans), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.building]:
	write(u"    |     - Building in BUA Scaler               {0}|".format(exs))
	if not ap.Exists('SettlementSrf') or (not ap.Exists('StructureSrf') and not ap.Exists('StructurePnt')):
		oops(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		oops(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not bua_count:
		greentext(u"    |          No BUAs found                     {0}|".format(exs))
	else:
		write(u"    |          {0} Buildings upscaled        {1}{2}|".format(total_2upscale, format_count(total_2upscale), exs))
		write(u"    |          {0} Buildings descaled        {1}{2}|".format(total_2descale, format_count(total_2descale), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.fcount]:
	write(u"    |     - Feature Report generated             {0}|".format(exs))
	write(u"    |          {0} Point Features            {1}{2}|".format(pnt_cnt, format_count(pnt_cnt), exs))
	write(u"    |          {0} Curve Features            {1}{2}|".format(crv_cnt, format_count(crv_cnt), exs))
	write(u"    |          {0} Surface Features          {1}{2}|".format(srf_cnt, format_count(srf_cnt), exs))
	write(u"    |          {0} Total Features            {1}{2}|".format(tots_f, format_count(tots_f), exs))
	write(u"    |          {0} Hydrography Features      {1}{2}|".format(hydro_cnt, format_count(hydro_cnt), exs))
	write(u"    |          {0} Transportation Features   {1}{2}|".format(trans_cnt, format_count(trans_cnt), exs))
	write(u"    |          {0} Utility Features          {1}{2}|".format(util_cnt, format_count(util_cnt), exs))
	write(u"    |          {0} Buildings                 {1}{2}|".format(building_cnt, format_count(building_cnt), exs))
	write(u"    |          {0} Landcover Surfaces        {1}{2}|".format(landcover_cnt, format_count(landcover_cnt), exs))
	write(u"    |          Check the output for file path    {0}|".format(exs))
if bool_dict[tool_names.vsource]:
	write(u"    |     - Source Report generated              {0}|".format(exs))
	write(u"    |          Check the output for file path    {0}|".format(exs))

#-----------------------------------
# Easter Egg
if not bool_dict[tool_names.repair] and not bool_dict[tool_names.fcode] and not bool_dict[tool_names.defaults] and not bool_dict[tool_names.metrics] and not bool_dict[tool_names.ufi] and not bool_dict[tool_names.hydro] and not bool_dict[tool_names.trans] and not bool_dict[tool_names.util] and not bool_dict[tool_names.defbridge] and not bool_dict[tool_names.defpylong] and not bool_dict[tool_names.defdam] and not bool_dict[tool_names.explode] and not bool_dict[tool_names.dups] and not bool_dict[tool_names.allbridge] and not bool_dict[tool_names.allpylong] and not bool_dict[tool_names.alldam] and not bool_dict[tool_names.building] and not bool_dict[tool_names.fcount] and not bool_dict[tool_names.vsource]:
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	greentext(u"    |          {0}, click a check box        {1}{2}|".format(username, format_count(username), exs))
	greentext(u"    |          and stop being cheeky.            {0}|".format(exs))

#-----------------------------------
write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")

ap.ResetProgressor()
