# -*- coding: utf-8 -*-
#¸¸.·´¯`·.¸¸.·´¯`·.¸¸
# ║╚╔═╗╝║  │┌┘─└┐│  ▄█▀‾
# ====================== #
# Finishing Tool v9.8.5  #
# Nat Cagle 2022-07-12   #
# ====================== #

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
  - Rewrite Calculate Metrics with manual calculations. Defense mapping tool takes too long and crashes. Kristen is working on it.
  - For calculating line and polygon metrics, if area or length is tool small throw warning with output. (Don't remember what this means.)
  - Maybe a pandas dataframe to sort UFIs. Still takes a long time to run.
  - Test rewritten Find Identical code and replace existing
  - Check for empty fcs for each fc loop


####################################
- Bridge WID Updater now checks for Bridges with WID <= Trans WD1 and updates them dependent on the underlying Road or Rail.
- Pylon HGT Updater now checks Pylons against intersecting Cables with HGT mismatch and updates the Pylon HGT to match the Cable HGT.
####################################


####################################
# Check Maxar important FFN list
####################################


####################################
# Double check bridge counting and also default detection for Bridge WID Updater. Use J11A sub2 for testing.
####################################


####################################
# make intergration for roads to buas. run test on J11A versus delivery GAIT to see effect. maybe add to full v9.8 release before Maxar deliveries.
####################################


####################################
# check the time difference between v9.6.5 and 9.7
Integrate Hydro
 - v9.6.5  >  0:00:45.4060
 - v9.7    >  0:54:54.4410
 - v9.8    >  0:54:25.0000

Integrate Trans
 - v9.6.5  >  0:00:36.0000
 - v9.7    >  0:02:09.8600
 - v9.8    >  0:02:35.6000

Integrate Utilities
 - v9.6.5  >  0:00:22.2970
 - v9.7    >  0:00:51.9690
 - v9.8    >  0:00:57.3530
####################################


# !_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!

## runtime() - fix grammar for singular hour and minute outputs

## Update tool names
    |     - Bridge WID Updater                   |
    |     - Pylon HGT Updater                    |
    |     - Building in BUA Scaler               |

## check if this output needs to change. were they not present or removed in the creation of the list?
MetadataSrf not present
ResourceSrf not present

## if not caci schema and caci swap is checked, set caci swap to FALSE to skip it entirely
tell user in ***green*** that since the schema isn't caci format, caci swap won't be run

## add runtime() output for constructing fishnet. just for funsies

## update wording in Update UFI Values
Searching 216 UFIs in AeronauticPnt for **invalid** or missing values.

--- Hypernova Burst Multipart Features --- #### double check for explosions
#### remove periods from these outputs
HydrographyCrv multipart progenitor cores collapsing.
#### make green and remove double "seconds" and period
Hypernova burst detected after 2.015 seconds seconds.

5 multipart features found in HydrographyCrv
  OIDs - [12131, 13707, 16829, 17093, 17390]
1 multipart features found in TransportationGroundCrv
  OIDs - [81597]
2 multipart features found in VegetationSrf
  OIDs - [1018, 3503]


--- Bridge WID Updater --- #### double check output math
3703 default WID bridges found.
2764 bridges on roads updated.
939 bridges on railroads updated.
#### new line
58 bridges still have default WID.
#### add asterisks and tabs
 The default bridges are either not snapped or missing their underlying road or rail.
 Make sure the bridges have the correct TRS.
#### fix runtime output
3645 bridges updated with new WID values in 0


--- Pylon HGT Updater --- #### double check output math
6529 default value pylons found.
6525 of the intersecting cables don't have a height. These will be ignored.
6 pylons are intersecting a cable with a height value and will be updated.
#### double check recount variable
0 pylons still have default HGT.
#### add asterisks and tabs
 Consider running Integrate and Repair before trying again.
 The remaining pylons are not snapped, missing a cable, or the underlying cable doesn't have a height.
6 pylons updated with new HGT values in 7.623 seconds


--- Building in BUA Scaler --- #### double check that there were no BUAs. might be missing the check.
No BUAs found. #### new line after
#### make green
Building in BUA Scaler finished in 0.562 seconds


--- CACI Swap Scale and CTUU ---
#### check this is stated in royal decree outro
Provided TDS does not match CACI schema containing the 'Scale' field.
Cannot run CACI Swap Scale and CTUU


--- Database Feature Report ---
Checking feature classes...
#### remove new line
AeronauticPnt features counted
AeronauticSrf features counted
~
#### "File located in the same folder as the database"
Feature Count Report created. File located in database folder:
C:\Projects\njcagle\R&D\M2_G19A_20210119_Feature_Report_2022_07_18_1309.txt
#### new line
Database Feature Report finished in 16.856 seconds


--- Source Analysis Report ---
Checking feature classes...
#### remove new line
AeronauticPnt feature sources identified
AeronauticSrf feature sources identified
~
#### "File located in the same folder as the database"
Source Analysis Report created. File located in database folder:
#### double check output folder location vs what is being printed
C:\Projects\njcagle\R&D
#### new line
Source Analysis Report finished in 10.232 seconds



#### Beautify and format
Freeing partition memory

~~ Checking Defense Mapping Extension back in ~~

#### Make a dictionary of runtimes for each tool for royal decree outro
#### use old time format
    |     - Repaired NULL Geometries             |
    |          Time Elapsed: 00:00:00.000        |
    |     - Populated F_Codes                    |
    |          0 F_Code errors fixed             |
    |          Time Elapsed: 00:00:00.000        |
#### update wording
    |     - Updated UFI Values                   |
    |          190674 Invalid or missing UFIs    |
#### Hydrography Features, Transportation Features, Utility Features
#### double check math for total features for new version of integration.
#### should just be total number of features in pnt, crv, and srf fcs.
    |     - Integrated and Repaired:             |
    |          28599 Hydrography Features        |
    |          64839 Transportation Features     |
    |          59988 Utility Features            |

#### this output has different numbers than the tool
#### Update tool name
    |     - Bridge WID Updater                   |
    |          3645 Bridges updated              |
#### make green if not 0
    |          58 Defaults not updated           |
#### make green if not 0
    |          Check the output for more info    |
#### Update tool name
    |     - Pylon HGT Updater                    |
    |          6 Pylons updated                  |
#### make green if not 0
    |          0 Defaults not updated            |
#### make green if not 0
    |          Check the output for more info    |
#### Update tool name
    |     - Building in BUA Scaler               |
    |          No BUAs found                     |

#### update tool name
    |     - Feature *R*eport generated             |
    |          95741 Point Features              |
    |          146849 Curve Features             |
    |          260289 Surface Features           |
    |          502879 Total Features             |
    |          37426 Hydrography Features        |
    |          117104 Transportation Features    |
#### add total utility feature count
    |          0000000 Utility Features          |**
    |          244865 Buildings                  |
    |          6663 Landcover Surfaces           |
#### update wording
    |          Check the output for file path    |
#### update tool name
    |     - Source *R*eport generated              |
#### update wording
    |          Check the output for file path    |

# !_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!_!‾!


## Recent Changes
	Version 9.7
	- Rewrote UFI check for duplicate and NULL values specifically
	- Added 'Skip Buildings' option for data with too many buildings (does not apply to Feature Count Report)
	- Sorted tools into categories
	- Added Tunnels to Default Bridge WID Updater
	- CACI Swap Scale and CTUU populates the 'SAX_RX9' field with 'Scale Swapped' the first time the tool is run. It erases the field when the Scale field is swapped back. This only goes back and forth and is dependent on this version of the tool being run when we get the database from CACI.
	- Added an updated Database Feature Report that outputs in alphabetical order, sorts any empty feature classes, and added more general totals such as total Trans, Hydro, Buildings, and Landcover.
	- Added an updated Source Analysis Report that outputs in alphabetical order and creates a csv and txt file of the SRT data source, collection dates, and total counts
	- Added option to Disable Editor Tracking (default true)
	- More detailed error handling for geoprocessing failures. Now with noticeable skull to catch users' attention.

	Version 9.8
    - Added option to specify what scale to run the tools on.
        - This applies to the following tools:
	        - Populate F_Codes
	        - Calculate Default Values
	        - Calculate Metrics
	        - Update UFI Values
	        - Integrate Hydrography Features
	        - Integrate Transportation Features
	        - Integrate Utility Features
	        - Hypernova Burst Multipart Features
	        - Bridge WID Updater
	        - Pylon HGT Updater
	        - Building in BUA Scaler
    - Added option to run tools on only 25k_LOC feature classes.
    - Switched the order of Delete Identical Features and Hypernova Burst Multipart so that any overlapping or kickback multipart features are exploded first and then checked for duplicates and removed.
    - Limited Calculate Metrics to only look at ARA for Polygons and LZN for Polylines. (This was not standard for the Defense Mapping tool)
    - Removed layered integration and overhauled the logic behind Integration steps.
        - Refactored Integration and Repair steps as modular functions.
        - Integrate Hydrography Features includes points (VanishingPoints, NaturalPools, etc.)
        - Integrate Transportation Features includes points (Ford, Culvert, etc.)
        - Work backwards through the geometry hierarchy to minimize feature shift or disjoint. Lines->Surfaces then Points->Lines.
        - Incorporated incremental snapping with 0.03m tolerance.
            - Snap lines to the nearest surface vertex within 0.03m.
	        - Snap remaining lines to the nearest surface edge within 0.03m.
	        - Snap points to the nearest line end node within 0.03m as priority over other vertices.
	        - Snap remaining points to the nearest line vertex within 0.03m.
	        - Snap remaining points to the nearest line edge within 0.03m.
	    - Integrate lines->surfaces then points->lines with default domain tolerance (ESRI recommended) to create intersection vertices without morphing the features.
	    - This should help with these GAIT errors. Although the GAIT tolerance is 0.1m, so the snap tolerance may need to be modified for further accuracy.
	        - Line-Line Undershoot/Overshoot
	        - Line-Area Perimeter Undershoot
	        - Point-Line Undershoot/Overshoot
	        - Potentially others
    - Buildings in BUA Scaler has been completely refactored using more efficient logic.
        - Descales buildings within BUAs that don't have important FFNs (client dependent), have a height < 46m, and aren't navigation landmarks (LMC=True).
	    - Scales in buildings within BUAs that do have important FFNs (client dependent), have a height >= 46m, or are navigation landmarks (LMC=True).
	- Cleaned up tool outputs and format


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
    - Added a function to construct the fishnet grid for partitioning large datasets into chunks using the Extent environment variable. This is now feature class independent. It is the first step in fully partitioning entire datasets for massive geospatial processing on only a Dell Optiplex with 8GB of RAM and a Core i5.
    - Fixed comma tuple bug in Calculate Metrics.
    - Changed the output for Update UFI Values to more accurately show which one is actively being worked on. User reading comprehension leaves something to be desired.
    - Removed use of the Defense Mapping extension in Hypernova Burst Multipart Features when calculating new default values.
    - CACI Swap scale_name variable was missing a definition after the last update. Added a second return value from the snowflake_protocol function for whatever CACI's unique Scale field name happens to be for any given schema.
    - Repair All NULL Geometries, Populate F_Codes, Calculate Default Values, Calculate Metrics, Update UFI Values, Integrate Hydrography Features, Integrate Transportation Features, and Integrate Utility Features have been refactored into functions.
	- Updated function aliases in code as well as replaced redundant code with recently made functions.
	- create_fc_list() now runs get_count() for each feature class in the dataset at the start and constructs the list with only feature classes that have records.



Crevasse
A deep crack in ice.
Crevice
A narrow opening in rock.


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
def TDS_check(TDS):
	if not ap.Exists(TDS):
		ap.AddError('                       ______\n                    .-"      "-.\n                   /            \\\n       _          |              |          _\n      ( \\         |,  .-.  .-.  ,|         / )\n       > "=._     | )(__/  \\__)( |     _.=" <\n      (_/"=._"=._ |/     /\\     \\| _.="_.="\\_)\n             "=._ (_     ^^     _)"_.="\n                 "=\\__|IIIIII|__/="\n                _.="| \\IIIIII/ |"=._\n      _     _.="_.="\\          /"=._"=._     _\n     ( \\_.="_.="     `--------`     "=._"=._/ )\n      > _.="                            "=._ <\n     (_/                                    \\_)\n')
		ap.AddError("Dataset {0} does not exist.\nPlease double check that the file path is correct.\nExitting tool...\n".format(TDS))
		sys.exit(0)


#----------------------------------------------------------------------
### [0] TDS   (The standard Finishing process is checked by default)   (Tools are run in list order) - Feature Dataset
TDS = ap.GetParameterAsText(0)
TDS_check(TDS)
ap.env.workspace = TDS
ap.env.extent = TDS
ap.env.overwriteOutput = True
### [1] For Top-Secret Finishing Version, what is the name of our leader? (Chairman Bock)- String
secret = ap.GetParameterAsText(1) # Password for Finishing easter egg
### [2] Scale to run tool: ZI026_CTUU >= - String Value List
where_scale = "zi026_ctuu >= {0}".format(ap.GetParameterAsText(2))

#-----------------------------------
### [3] Options .............. String Value List
### Tool Processing Options:   ['Use 25k_LOC feature classes only', 'Disable Editor Tracking', 'Skip Buildings']
### [6] Maintenance .......... String Value List
### Data Maintenance Tools:    ['Repair All NULL Geometries', 'Populate F_Codes', 'Calculate Default Values', 'Calculate Metrics', 'Update UFI Values']
### [7] Integration .......... String Value List
### Integration Tools:         ['Integrate Hydrography Features', 'Integrate Transportation Features', 'Integrate Utility Features']
### [8] Geometry ............. String Value List
### Geometry Correction Tools: ['Hypernova Burst Multipart Features', 'Delete Identical Features']
### [9] Preprocessing ........ String Value List
### Preprocessing Tools:       ['Bridge WID Updater', 'Pylon HGT Updater', 'Building in BUA Scaler', 'CACI Swap Scale and CTUU']
### [10] Management .......... String Value List
### Database Management Tools: ['Database Feature Report', 'Source Analysis Report']
tool_list = ap.GetParameter(3) + ap.GetParameter(4) + ap.GetParameter(5) + ap.GetParameter(6) + ap.GetParameter(7) + ap.GetParameter(8)

#-----------------------------------
#autopcf = ap.GetParameter()
#hydrattr = ap.GetParameter()
#tranattr = ap.GetParameter()
#utilattr = ap.GetParameter()
#cultureattr = ap.GetParameter()
#landcover = ap.Getparameter()

#-----------------------------------
name_class = namedtuple("name_class", "loc disable vogon repair fcode defaults metrics ufi hydro trans util explode dups bridge pylong building swap fcount vsource")
# tool_names.var to get Tool Name
tool_names = name_class("Use 25k_LOC feature classes only", "Disable Editor Tracking", "Skip Buildings", "Repair All NULL Geometries", "Populate F_Codes", "Calculate Default Values", "Calculate Metrics", "Update UFI Values", "Integrate Hydrography Features", "Integrate Transportation Features", "Integrate Utility Features", "Hypernova Burst Multipart Features", "Delete Identical Features", "Bridge WID Updater", "Pylon HGT Updater", "Building in BUA Scaler", "CACI Swap Scale and CTUU", "Database Feature Report", "Source Analysis Report")

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
	(tool_names.explode, False),
	(tool_names.dups, False),
	(tool_names.bridge, False),
	(tool_names.pylong, False),
	(tool_names.building, False),
	(tool_names.swap, False),
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
	ap.AddError("Please rerun the tool.")
	ap.AddError("Go double check the tool outputs above for more information on where the tool failed.")
	ap.AddError("If the error persists, uncheck the {0} tool option before rerunning.\nEither the feature class is too big or something else has gone wrong.".format(tool_name))
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

# def fc_exists(fc, tool_name): # Check if feature class exists
# 	if ap.Exists(fc):
# 		return True
# 	else:
# 		write("{0} feature class missing\n{1} will skip steps involving {0}".format(fc, tool_name))
# 		return False

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
			ap.AddWarning("StructureSrf and StructurePnt will be skipped in processing.")

		#featureclass = [fc for fc in featureclass if fc_exists(fc, 'Finishing Tool') and get_count(fc)]
		featureclass = []
		for fc in featureclass_loc:
			count = get_count(fc)
			if count:
				featureclass.append(fc)
				write("    - {0} {1} features".format(count, fc))
			else:
				ap.AddWarning("    > {0} has {1} features".format(fc, count))

		featureclass.sort()
		fc_list_finish = dt.now()
		write("Loaded {0} of 55 TDSv7.1 feature classes in {1}".format(len(featureclass), runtime(fc_list_start, fc_list_finish)))
		return featureclass

	#featureclass = ap.ListFeatureClasses()
	#featureclass = [fc for fc in featureclass if get_count(fc)]
	#featureclass = [fc for fc in ap.ListFeatureClasses() if get_count(fc)]
	featureclass = []
	for fc in sorted(ap.ListFeatureClasses()):
		count = get_count(fc)
		if count:
			featureclass.append(fc)
			write("    - {0} {1} features".format(count, fc))
		else:
			ap.AddWarning("    > {0} has {1} features".format(fc, count))

	# Formatting Feature Class list
	if 'MetadataSrf' in featureclass:
		featureclass.remove('MetadataSrf')
		write("MetadataSrf removed")
	else:
		write("MetadataSrf has 0 features or is not present")
	if 'ResourceSrf' in featureclass:
		featureclass.remove('ResourceSrf')
		write("ResourceSrf removed")
	else:
		write("ResourceSrf has 0 features or is not present")
	if bool_dict[tool_names.vogon]:
		if 'StructureSrf' in featureclass:
			featureclass.remove('StructureSrf')
		if 'StructurePnt' in featureclass:
			featureclass.remove('StructurePnt')
		ap.AddWarning("StructureSrf and StructurePnt will be skipped in processing.")

	featureclass.sort()
	fc_list_finish = dt.now()
	write("Loaded {0} of 55 TDSv7.1 feature classes in {1}".format(len(featureclass), runtime(fc_list_start, fc_list_finish)))
	return featureclass

def snowflake_protocol(): # Checking for CACI schema cz they're "special" and have to make everything so fucking difficult
	snowflake_start = dt.now()
	scale_field = 'scale'
	write("Checking for CACI custom schema...")
	for fc in featureclass:
		fc_zero = get_count(fc)
		if fc_zero == 0:
			continue
		else:
			field_check = ap.ListFields(fc)
			field_check = [field.name for field in field_check if any([scale_field in field.name.lower()])]
			if field_check:
				snowflake_finish = dt.now()
				ap.AddWarning("Variant TDS schema identified in {0}\nSnowflake protocol activated for relevant tools.".format(runtime(snowflake_start, snowflake_finish)))
				return True, field_check
			else:
				snowflake_finish = dt.now()
				write("Regular TDS schema identified in {0}".format(runtime(snowflake_start, snowflake_finish)))
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
				ap.AddWarning("Error disabling editor tracking for {0}. Please check the data manually and try again.".format(fc))
				pass
	if firstl:
		write("Editor Tracking has been disabled.")
	else:
		write("Editor Tracking has already been disabled.")
	disable_finish = dt.now()
	write("Time to disable Editor Tracking: {0}".format(runtime(disable_start, disable_finish)))

def check_defense(in_out, metrics): # If any of the tools that require the Defense Mapping license are selected, check out the Defense license
	if metrics:
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
	# write("Spatial data extent fully recalculated in {0}".format(runtime(refresh_extent_start, dt.now())))

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
	ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", "", "POLYGON")
	chungus_finish = dt.now()
	write("Spatial data partitions constructed in {0}".format(runtime(chungus_start, chungus_finish)))
	return mem_fc

#----------------------------------------------------------------------
def repair_geometry():
	repair_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.repair))
	for fc in featureclass:
		write("Repairing NULL geometries in {0}".format(fc))
		ap.RepairGeometry_management(fc, "DELETE_NULL")
		#ap.RepairBadGeometry_production(featureclass, 'REPAIR_ONLY', 'DELETE_NULL_GEOMETRY', '#') # Repair Bad Geometry Production Mapping tool
	repair_finish = dt.now()
	ap.AddWarning("{0} finished in {1}".format(tool_names.repair, runtime(repair_start, repair_finish)))

#-----------------------------------
def pop_fcode():
	fcode_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.fcode))
	fcode_total = 0
	fields = ['f_code', 'fcsubtype']
	for fc in featureclass:
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
			ap.AddWarning("{0} does not contain F_codes.".format(fc))
	fcode_finish = dt.now()
	ap.AddWarning("{0} F_Code errors fixed in {1}".format(fcode_total, runtime(fcode_start, fcode_finish)))
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
	defaults_finish = dt.now()
	ap.AddWarning("{0} NULL values populated with defaults in {1}".format(count_nulls, runtime(defaults_start, defaults_finish)))

#-----------------------------------
def calc_metrics():
	metrics_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.metrics))
	for fc in featureclass:
		shape_type = ap.Describe(fc).shapeType # Polygon, Polyline, Point, Multipoint, MultiPatch
		if shape_type == 'Polyline':
			make_lyr(fc, 'fc_lyr', where_scale)
			write("Calculating Length field for {0}".format(fc))
			ap.CalculateMetrics_defense('fc_lyr', 'LENGTH', "LZN", "#", "#", "#", "#", "#")
			arcdel('fc_lyr')
		elif shape_type == 'Polygon':
			make_lyr(fc, 'fc_lyr', where_scale)
			write("Calculating Area field for {0}".format(fc))
			ap.CalculateMetrics_defense('fc_lyr', 'AREA', "#", "#", "ARA", "#", "#", "#")
			arcdel('fc_lyr')
	metrics_finish = dt.now()
	ap.AddWarning("{0} finished in {1}".format(tool_names.metrics, runtime(metrics_start, metrics_finish)))

#-----------------------------------
def update_ufi():
	ufi_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.ufi))
	ufi_total = 0
	for fc in featureclass:
		write("Searching {0} UFIs in {1} for invalid or missing values.".format(get_count(fc), fc))
		ufi_count = 0
		with ap.da.SearchCursor(fc, 'ufi', where_scale) as scursor:
			values = [srow[0] for srow in scursor]
		with ap.da.UpdateCursor(fc, 'ufi', where_scale) as ucursor:
			for urow in ucursor:
				if not populated(urow[0]):
					urow[0] = str(uuid.uuid4())
					ufi_count += 1
				elif len(urow[0]) != 36: # 36 character random alphanumeric string
					urow[0] = str(uuid.uuid4()) # GOTOHELL-FUCK-COCK-PISS-MOTHERFUCKER and LEONARDO-EATS-FROG-EGGS-DISGUSTINGLY are valid XD
					ufi_count += 1
				elif values.count(urow[0]) > 1:
					urow[0] = str(uuid.uuid4())
					ufi_count += 1
				ucursor.updateRow(urow)
			if ufi_count:
				write("  - {0} UFIs updated".format(ufi_count))
			ufi_total += ufi_count
	ufi_finish = dt.now()
	ap.AddWarning("{0} invalid or missing UFI values updated in {1}".format(ufi_total, runtime(ufi_start, ufi_finish)))
	return ufi_total

#-----------------------------------
# def dangling_orphans():
# 	arcpy.DeleteDangles_production(inFeatures, "10 Feet", '#', 'NON_RECURSIVE', '45')
# 	arcpy.RemoveCutbacks_production(roads, minimum_angle, "SEQUENTIAL", '#', 'IGNORE_SNAPPED_POINTS', '#')

def snap_lines_to_srf(lines, srf):
	vertex_env = [srf, "VERTEX", "0.03 Meters"] # Snap lines to the nearest srf vertex within 0.03m
	edge_env = [srf, "EDGE", "0.03 Meters"] # snap remaining lines to the nearest srf edge within 0.03m
	write("Snapping line end nodes to rank 1 surface vertices rank 2 surface edges.")
	ap.Snap_edit(lines, [vertex_env, edge_env])
	write("Creating missing line-surface intersection vertices.")
	ap.Integrate_management([[srf, 1], [lines, 2]]) # Integrate lines to srfs with default domain tolerance to create intersection vertices in them without morphing them and creating potential errors.
	ap.RepairGeometry_management(srf, "DELETE_NULL")

def snap_points_to_lines(points, lines):
	end_env = [lines, "END", "0.03 Meters"] # Snap points to the nearest line end node within 0.03m as priority over other vertices
	vertex_env = [lines, "VERTEX", "0.03 Meters"] # Snap points to the nearest line vertex within 0.03m
	edge_env = [lines, "EDGE", "0.03 Meters"] # snap remaining points to the nearest line edge within 0.03m
	write("Snapping points to rank 1 line end nodes, rank 2 line vertices, and rank 3 line edges.")
	ap.Snap_edit(points, [end_env, vertex_env, edge_env])
	write("Creating missing point-line intersection vertices.")
	ap.Integrate_management([[lines, 1], [points, 2]]) # Integrate points to lines with default domain tolerance to create intersection vertices in the lines without morphing them and creating potential errors.
	ap.RepairGeometry_management(points, "DELETE_NULL")
	ap.RepairGeometry_management(lines, "DELETE_NULL")

def make_integrate_layers(name_list):
	#name_list = ['FeaturePnt', 'FeatureCrv', 'FeatureSrf', 'feat_pnt', 'feat_crv', 'feat_srf']
	if name_list[0] not in featureclass:
		if ap.Exists(name_list[0]):
			pass
		else:
			ap.AddError("** {0} feature class not found\n  To run Integrate, copy an empty {0} feature class from a blank schema into this dataset and run the tool again. **".format(name_list[0]))
			writeresults("Integrate and Repair")
	if name_list[1] not in featureclass:
		if ap.Exists(name_list[1]):
			pass
		else:
			ap.AddError("** {0} feature class not found\n  To run Integrate, copy an empty {0} feature class from a blank schema into this dataset and run the tool again. **".format(name_list[1]))
			writeresults("Integrate and Repair")
	if name_list[2] not in featureclass:
		if ap.Exists(name_list[2]):
			pass
		else:
			ap.AddError("** {0} feature class not found\n  To run Integrate, copy an empty {0} feature class from a blank schema into this dataset and run the tool again. **".format(name_list[2]))
			writeresults("Integrate and Repair")

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
	make_integrate_layers(hydro_list)

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
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
				ap.Integrate_management(hydro_crv, "0.02 Meters")

	repair_and_clean(hydro_list)
	hydro_finish = dt.now()
	ap.AddWarning("{0} finished in {1}".format(tool_names.hydro, runtime(hydro_start, hydro_finish)))
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
	make_integrate_layers(trans_list)

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
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
				ap.Integrate_management(trans_crv, "0.02 Meters")

	repair_and_clean(trans_list)
	trans_finish = dt.now()
	ap.AddWarning("{0} finished in {1}".format(tool_names.trans, runtime(trans_start, trans_finish)))
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
	make_integrate_layers(util_list)

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
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
				ap.Integrate_management(util_crv, "0.02 Meters")

	repair_and_clean(util_list)
	util_finish = dt.now()
	ap.AddWarning("{0} finished in {1}".format(tool_names.util, runtime(util_start, util_finish)))
	return ufeat_count

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
if bool_dict[tool_names.explode]:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
if bool_dict[tool_names.dups]:
	write(u"    |     - Delete Identical Features            {0}|".format(exs))
if bool_dict[tool_names.bridge]:
	write(u"    |     - Bridge WID Updater                   {0}|".format(exs))
if bool_dict[tool_names.pylong]:
	write(u"    |     - Pylon HGT Updater                    {0}|".format(exs))
if bool_dict[tool_names.building]:
	write(u"    |     - Building in BUA Scaler               {0}|".format(exs))
if bool_dict[tool_names.swap]:
	write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
if bool_dict[tool_names.fcount]:
	write(u"    |     - Generate Feature Report              {0}|".format(exs))
if bool_dict[tool_names.vsource]:
	write(u"    |     - Generate Source Report               {0}|".format(exs))

#-----------------------------------
write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")


#----------------------------------------------------------------------
#refresh_extent() # Refreshes the extent polygon for the whole dataset
featureclass = create_fc_list() # Create the feature class list with the requested fcs
caci_schema, scale_name = snowflake_protocol() # Check for a CACI schema. Special actions are required for their custom nonsense.
if bool_dict[tool_names.swap] and not caci_schema:
	bool_dict[tool_names.swap] = False
	ap.AddError("CACI Swap Scale and CTUU was checked, but a CACI schema was not identified.\n** CACI Swap Scale and CTUU will be skipped **")
if bool_dict[tool_names.disable]:
	disable_editor_tracking(gdb_name) # Disables Editor Tracking for all feature classes
mem_grid = grid_chungus() # Create the extent polygon grid for partitioning the data
check_defense('out', bool_dict[tool_names.metrics]) # Checks out the Defense Mapping extension. Only need for Calculate Metrics. Soon to be deprecated.
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
	try:
		repair_geometry()
	except ap.ExecuteError:
		writeresults(tool_names.repair)


#----------------------------------------------------------------------
''''''''' Populate F_Codes '''''''''
# Identifies bad F_Code/FCSubtype pairs and updates the F_Code value assuming correctly attributed FCSubtypes
# Refactored from John Jackson's Populate F_codes tool by Nat Cagle
if bool_dict[tool_names.fcode]:
	#~~~~~ Royal Decree Variables ~~~~~
	fcode_total = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		fcode_total = pop_fcode()
	except ap.ExecuteError:
		writeresults(tool_names.fcode)


#----------------------------------------------------------------------
''''''''' Calculate Default Values '''''''''
# Calculates default values for all fields with NULL attributes
if bool_dict[tool_names.defaults]:
	try:
		process_defaults(featureclass)
	except ap.ExecuteError:
		writeresults(tool_names.defaults)


#----------------------------------------------------------------------
''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields (LZN and ARA)
if bool_dict[tool_names.metrics]:
	try:
		calc_metrics()
	except ap.ExecuteError:
		writeresults(tool_names.metrics)


#----------------------------------------------------------------------
''''''''' Update UFI Values '''''''''
# Iterate through all features and update the ufi field with uuid4 random values
if bool_dict[tool_names.ufi]:
	#~~~~~ Royal Decree Variables ~~~~~
	ufi_total = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		ufi_total = update_ufi()
		#Update UFI Values updated 0 invalid or missing UFI values in 0:20:9.3510
	except ap.ExecuteError:
		writeresults(tool_names.ufi)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Feature Specific Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Integrate and Repair Hydrography Features '''''''''
if bool_dict[tool_names.hydro]:
	#~~~~~ Royal Decree Variables ~~~~~
	hfeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		hfeat_count = integrate_hydro()
	except ap.ExecuteError:
		writeresults(tool_names.hydro)


#----------------------------------------------------------------------
''''''''' Integrate and Repair TransportationGround Features '''''''''
if bool_dict[tool_names.trans]:
	#~~~~~ Royal Decree Variables ~~~~~
	tfeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		tfeat_count = integrate_trans()
	except ap.ExecuteError:
		writeresults(tool_names.trans)


#----------------------------------------------------------------------
''''''''' Integrate and Repair UtilityInfrastructure Features '''''''''
if bool_dict[tool_names.util]:
	#~~~~~ Royal Decree Variables ~~~~~
	ufeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		ufeat_count = integrate_util()
	except ap.ExecuteError:
		writeresults(tool_names.util)



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
	##### Multipart Search #####
	fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
	fc_multi_list = []
	total_multi = 0
	total_complex = 0
	# Identifying the true multipart features and separating from complex singlepart polygons flagged as multiparts
	for fc in featureclass:
		try:
			write("Searching for multipart features in {0}".format(fc))
			multipart = False # Assume the feature class doesn't have multiparts
			with ap.da.SearchCursor(fc, ['OID@', 'SHAPE@'], where_scale) as scursor:
				complex = 0 # Counts complex single part features
				for row in scursor: # For each feature in the fc
					shape = row[1] # Get SHAPE@ token to extract properties
					if shape is None: # Checks for NULL geometries
						ap.AddWarning(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
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
			ap.AddWarning("{0} multipart features found in {1}".format(count, fc))
			#ap.AddWarning("  OIDs - {0}".format(fc_multi[fc]))
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
				ap.AddError("** Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin. **")

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
			multifinish = dt.now()
			ap.AddWarning("Hypernova burst detected after {0}".format(runtime(multistart, multifinish)))

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
	explode_finish = dt.now()
	ap.AddWarning("{0} features exploded in {1}".format(total_multi, runtime(explode_start, explode_finish)))


#----------------------------------------------------------------------
''''''''' Delete Identical Features '''''''''
# Checks for features with identical geometry and PSG attribution and removes them
if bool_dict[tool_names.dups]:
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
	ap.AddWarning("{0} duplicates removed in {1}".format(dup_count, runtime(dups_start, dups_finish)))

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
''''''''' Bridge WID Updater '''''''''
# Checks for bridges with WID <= Trans WD1 and updates them to match the underlying road or rail WID
while bool_dict[tool_names.bridge]:
	bridge_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.bridge))
	#~~~~~ Royal Decree Variables ~~~~~
	total_bridges = 0
	updated_bridges = 0
	remaining_default_bridges = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	if 'TransportationGroundCrv' not in featureclass:
		if ap.Exists('TransportationGroundCrv'):
			ap.AddWarning("TransportationGroundCrv has no features. Moving on.")
		else:
			ap.AddError("\n*** Failed to run {0} ***".format(tool_names.bridge))
			ap.AddError("TransportationGroundCrv feature class missing\n")
		break

	# Pull width and geometry fields for bridges
	bridge_fields = ['WID', 'ZI026_CTUU', 'SHAPE@']
	# Pull width and geometry fields for roads
	road_fields = ['ZI016_WD1', 'ZI026_CTUU', 'SHAPE@']
	# Pull width and geometry fields for cart tracks
	cart_track_fields = ['WID', 'ZI026_CTUU', 'SHAPE@']
	# Pull width and geometry fields for rails and sidetracks
	rail_fields = ['ZI017_GAW', 'ZI026_CTUU', 'SHAPE@']

	# Convert the feature classes from the TDS into usable layers
	write("Making feature layers...")
	make_lyr("TransportationGroundCrv", "bridge_crv_lyr", "F_CODE IN ('AQ040', 'AQ130') AND {0}".format(where_scale))
	make_lyr("TransportationGroundCrv", "road_crv_lyr", "F_CODE IN ('AP030') AND {0}".format(where_scale))
	make_lyr("TransportationGroundCrv", "cart_crv_lyr", "F_CODE IN ('AP010') AND {0}".format(where_scale))
	make_lyr("TransportationGroundCrv", "rail_crv_lyr", "F_CODE IN ('AN010', 'AN050') AND {0}".format(where_scale))
	write("Successfully made the feature layers!")

	# Select road bridges with default (-999999) width
	#select_by_att("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130') AND {0}".format(where_scale))
	#select_by_att("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 13")
	# Make road bridges with default (-999999) width into layer
	#make_lyr("bridge_crv_lyr", "road_cart_bridges", "WID = -999999 AND TRS = 13") #### remove default check to just search all bridges for values <= trans WD1
	#make_lyr("bridge_crv_lyr", "road_cart_bridges", "TRS = 13") #### remove default check to just search all bridges for values <= trans WD1

	# Select rail bridges with default (-999999) width
	#select_by_att("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130') AND {0}".format(where_scale))
	#select_by_att("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 12")
	# Make rail bridges with default (-999999) width into layer
	#make_lyr("bridge_crv_lyr", "rail_bridges", "WID = -999999 AND TRS = 12") #### remove default check to just search all bridges for values <= trans WD1
	#make_lyr("bridge_crv_lyr", "rail_bridges", "TRS = 12") #### remove default check to just search all bridges for values <= trans WD1

	# Select roads that share curve with the default width bridges above
	#select_by_att("road_crv_lyr", "NEW_SELECTION", "F_CODE = 'AP030' AND {0}".format(where_scale))
	select_by_loc("road_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "bridge_crv_lyr", "", "NEW_SELECTION")
	# Make roads that share curve with default width bridges into layer
	make_lyr("road_crv_lyr", "roads")

	select_by_loc("cart_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "bridge_crv_lyr", "", "NEW_SELECTION")
	make_lyr("cart_crv_lyr", "cart_tracks")

	# Select rails that share curve with the default width bridges above
	#select_by_att("rail_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AN010', 'AN050') AND {0}".format(where_scale))
	select_by_loc("rail_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "bridge_crv_lyr", "", "NEW_SELECTION")
	# Make rails that share curve with default width bridges into layer
	make_lyr("rail_crv_lyr", "rails")

	### road_cart_bridges - Bridges and Tunnels at user specified scale with default WID and TRS = Road
	### rail_bridges - Bridges and Tunnels at user specified scale with default WID and TRS = Rail
	### roads - Roads at user specified scale that share a line segment with road_cart_bridges
	### cart_tracks - Cart Tracks at user specified scale that share a line segment with road_cart_bridges
	### rails - Railways and Railway Sidetracks at user specified scale that share a line segment with rail_bridges

	# Gets a count of selected bridges, roads, and rails
	#road_cart_bridges_total = get_count("road_cart_bridges")
	#rail_bridges_total = get_count("rail_bridges")
	total_bridges = get_count("bridge_crv_lyr")
	select_by_att("bridge_crv_lyr", "NEW_SELECTION", "WID = -999999")
	total_default_bridges = get_count("bridge_crv_lyr")
	select_by_att("bridge_crv_lyr", "CLEAR_SELECTION")
	total_roads = get_count("roads")
	total_cart_tracks = get_count("cart_tracks")
	total_rails = get_count("rails")

	# Error handling. If 0 bridges selected the script hangs.
	if not total_bridges:
		ap.AddWarning("No bridges or tunnels found.")
		bridge_finish = dt.now()
		write("{0} finished in {1}".format(tool_names.bridge, runtime(bridge_start, bridge_finish)))
		break
	# Error handling. If no roads or rails to select against, likely something will break.
	if not total_roads and not total_cart_tracks and not total_rails:
		ap.AddWarning("{0} bridges and tunnels found.".format(total_bridges))
		ap.AddWarning("** No underlying Roads, Cart Tracks, Railways, or Railway Sidetracks for default bridges and tunnels. \n The default bridges and tunnels are either not snapped or missing their underlying Transportation feature. \n Make sure the bridges and tunnels have the correct TRS. **")
		bridge_err = True
		bridge_finish = dt.now()
		write("{0} finished in {1}".format(tool_names.bridge, runtime(bridge_start, bridge_finish)))
		break

	# Announces the total default bridges found.
	write("{0} total bridges and tunnels found.".format(total_bridges))
	write("{0} bridges and tunnels with default WID = -999999 found.\n".format(total_default_bridges))

	# Start an edit session. Must provide the workspace.
	#edit = ap.da.Editor(os.path.dirname(TDS))
	# Edit session is started without an undo/redo stack for versioned data
	#edit.startEditing(False, True) # For second argument, use False for unversioned data

	road_bridges_updated = 0
	cart_bridges_updated = 0
	rail_bridges_updated = 0
	if total_bridges > 0:
		#edit.startOperation() # Start an edit operation for road bridges
		# Loop to update bridge width to it's corresponding road width
		with ap.da.UpdateCursor("bridge_crv_lyr", bridge_fields) as u_road_bridges: # UpdateCursor for bridges with width and geometry
			for bridge in u_road_bridges:
				with ap.da.SearchCursor("roads", road_fields) as s_roads: # SearchCursor for roads with width and geometry
					for road in s_roads:
						#if bridge[-1].overlaps(road[-1]): # Check if bridge shares curve with road(if not working test contains\within)
						if bridge[-1].buffer(0.000031092503).contains(road[-1]): # Check if bridge shares curve with road(if not working test contains\within)
							if bridge[0] < road[0]:
								bridge[0] = int(road[0]*1.5) # Sets current bridge width to road width * [factor]
							if bridge[1] != road[1]:
								bridge[1] = road[1]
				u_road_bridges.updateRow(bridge)
				road_bridges_updated += 1
		#edit.stopOperation() # Stop the edit operation
		write("{0} Bridges or Tunnels with WID less than Road WD1 were updated.".format(road_bridges_updated))

		#edit.startOperation() # Start an edit operation for cart track bridges
		# Loop to update bridge width to it's corresponding cart track width
		with ap.da.UpdateCursor("bridge_crv_lyr", bridge_fields) as u_cart_bridges: # UpdateCursor for bridges with width and geometry
			for bridge in u_cart_bridges:
				with ap.da.SearchCursor("cart_tracks", cart_track_fields) as s_cart_tracks: # SearchCursor for cart tracks with width and geometry
					for cart_track in s_cart_tracks:
						#if bridge[-1].overlaps(cart_track[-1]): # Check if bridge shares curve with cart track(if not working test contains\within)
						if bridge[-1].buffer(0.000031092503).contains(cart_track[-1]): # Check if bridge shares curve with cart track(if not working test contains\within)
							if bridge[0] < cart_track[0]:
								bridge[0] = int(cart_track[0]*1.5) # Sets current bridge width to cart track width * [factor]
							if bridge[1] != cart_track[1]:
								bridge[1] = cart_track[1]
				u_cart_bridges.updateRow(bridge)
				cart_bridges_updated += 1
		#edit.stopOperation() # Stop the edit operation
		write("{0} Bridges or Tunnels with WID less than Cart Track WID were updated.".format(cart_bridges_updated))

		#edit.startOperation() # Start an edit operation for rail bridges
		# Loop to update bridge width to it's corresponding rail width
		with ap.da.UpdateCursor("bridge_crv_lyr", bridge_fields) as u_rail_bridges: # UpdateCursor for bridges with width and geometry
			for bridge in u_rail_bridges:
				with ap.da.SearchCursor("rails", rail_fields) as s_rails: # SearchCursor for rails with width and geometry
					for rail in s_rails:
						#if bridge[-1].overlaps(rail[-1]): # Check if bridge shares curve with rail(if not working test contains\within)
						if bridge[-1].buffer(0.000031092503).contains(rail[-1]): # Check if bridge shares curve with rail(if not working test contains\within)
							if bridge[0] < rail[0]:
								bridge[0] = int(rail[0])+1 # Sets current bridge width to integer rounded rail gauge width + [value]
							if bridge[1] != rail[1]:
								bridge[1] = rail[1]
				u_rail_bridges.updateRow(bridge)
				rail_bridges_updated += 1
		#edit.stopOperation() # Stop the edit operation
		write("{0} Bridges or Tunnels with WID less than Railway or Railway Sidetrack GAW were updated.".format(rail_bridges_updated))
	write("\n")

	# Stop the edit session and save the changes
	#try:
	#	edit.stopEditing(True)
	#except:
	#	write("First attempt to save failed. Checking for updated SDE version. Trying again in 5 seconds. Please hold...")
	#	time.sleep(5)
	#	edit.stopEditing(True)

	# Select any remaining bridges with default (-999999) width
	#select_by_att("bridge_crv_lyr", "NEW_SELECTION", "F_CODE = 'AQ040' AND {0}".format(where_scale))
	select_by_att("bridge_crv_lyr", "NEW_SELECTION", "WID = -999999")
	# Make these selections into a new layer and get a count
	#make_lyr("bridge_crv_lyr", "bridges_rem")
	remaining_default_bridges = get_count("bridge_crv_lyr")
	# Final messages of the state of the data after tool completion
	updated_bridges = road_bridges_updated + cart_bridges_updated + rail_bridges_updated
	if remaining_default_bridges > 0:
		ap.AddWarning("** {0} Bridges or Tunnels remaining with default WID = -99999. **\n** The default bridges and tunnels are either not snapped or missing their underlying road or rail. **\n** Make sure the bridges and tunnels have the correct TRS. **".format(remaining_default_bridges))
	bridge_finish = dt.now()
	ap.AddWarning("{0} bridges and tunnels updated with new WID values in {1}".format(updated_bridges, runtime(bridge_start, bridge_finish)))
	break


Making feature layers...
Successfully made the feature layers!
108 bridges and tunnels found.

106 Bridges or Tunnels on Roads updated.
97 Bridges or Tunnels on Cart Tracks updated.
2 Bridges or Tunnels on railroads updated.

** 102 bridges and tunnels still have default WID. **
** The default bridges and tunnels are either not snapped or missing their underlying road or rail. **
** Make sure the bridges and tunnels have the correct TRS. **
205 bridges and tunnels updated with new WID values in 1 minute and 34.7 seconds

    |          205 Bridges updated               |
    |          102 Default bridges remaining     |
    |          Check the output for more info    |




#----------------------------------------------------------------------
''''''''' Pylon HGT Updater '''''''''
# Checks for pylons with HGT mismatch against intersecting Cables and updates them to match the Cable HGT
while bool_dict[tool_names.pylong]:
	pylong_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.pylong))
	#~~~~~ Royal Decree Variables ~~~~~
	total_pylons = 0
	lecount = 0
	total_rem_p = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	if 'UtilityInfrastructurePnt' not in featureclass or 'UtilityInfrastructureCrv' not in featureclass:
		if ap.Exists() or ap.Exists():
			ap.AddWarning("Either UtilityInfrastructurePnt or UtilityInfrastructureCrv has no features. Moving on.")
		else:
			ap.AddError("\n*** Failed to run {0} ***".format(tool_names.pylong))
			ap.AddError("UtilityInfrastructurePnt or UtilityInfrastructureCrv feature class missing\n")
		break

	# Pull height and geometry fields
	fields = ['HGT', 'SHAPE@']

	# Convert the feature classes from the TDS into usable layers
	write("Making feature layers...")
	make_lyr("UtilityInfrastructurePnt", "utility_pnt_lyr")
	make_lyr("UtilityInfrastructureCrv", "utility_crv_lyr")
	write("Successfully made the feature layers!")

	# Select pylons with default (-999999) height
	select_by_att("utility_pnt_lyr", "NEW_SELECTION", "F_CODE = 'AT042' AND {0}".format(where_scale))
	select_by_att("utility_pnt_lyr", "SUBSET_SELECTION", "HGT = -999999")
	make_lyr("utility_pnt_lyr", "fc_pylon_total")
	# Select cables that intersect the default height pylons above and removes any with default height
	select_by_att("utility_crv_lyr", "NEW_SELECTION", "F_CODE = 'AT005' AND {0}".format(where_scale))
	select_by_loc("utility_crv_lyr", "INTERSECT", "utility_pnt_lyr", "", "SUBSET_SELECTION")
	make_lyr("utility_pnt_lyr", "fc_cable_total")
	select_by_att("utility_crv_lyr", "REMOVE_FROM_SELECTION", "HGT = -999999")
	# Select only the default pylons that intersect cables to speed up run time
	select_by_loc("utility_pnt_lyr", "INTERSECT", "utility_crv_lyr", "", "SUBSET_SELECTION")
	# Make these selections into layers
	make_lyr("utility_pnt_lyr", "fc_pylon")
	make_lyr("utility_crv_lyr", "fc_cable")

	# Gets a count of selected pylons and cables
	total_pylons = get_count("fc_pylon_total")
	total_cables = get_count("fc_cable_total")
	usable_pylons = get_count("fc_pylon")
	usable_cables = get_count("fc_cable")

	# Error handling. If 0 pylons selected the script hangs.
	if not total_pylons:
		ap.AddWarning("No default pylons found.")
		pylong_finish = dt.now()
		write("{0} finished in {1}".format(tool_names.pylong, runtime(pylong_start, pylong_finish)))
		break
	# Error handling. If no cables to select against, likely something will break.
	if not total_cables:
		ap.AddWarning("{0} default value pylons found.".format(total_pylons))
		ap.AddWarning("No intersecting cables for default pylons. \n Try running Integrate and Repair then try again. \n The default pylons are either not snapped or missing a cable.")
		pylong_err = True
		pylong_finish = dt.now()
		write("{0} finished in {1}".format(tool_names.pylong, runtime(pylong_start, pylong_finish)))
		break

	# Announces the total default pylons found.
	no_hgt_cable = total_cables - usable_cables
	y = str(total_pylons - usable_pylons)
	#y = str(y)
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
	select_by_att("fc_pylon", "NEW_SELECTION", "F_CODE = 'AT042' AND {0}".format(where_scale))
	select_by_att("fc_pylon", "SUBSET_SELECTION", "HGT = -999999")
	# Make these selections into a new layer and get a count
	make_lyr("fc_pylon", "pylons_rem")
	total_rem_p = get_count("pylons_rem")
	# Final messages of the state of the data after tool completion
	lecount = lecount - total_rem_p
	ap.AddWarning("{0} pylons still have default HGT. \n Consider running Integrate and Repair before trying again. \n The remaining pylons are not snapped, missing a cable, or the underlying cable doesn't have a height.".format(total_rem_p))
	pylong_finish = dt.now()
	ap.AddWarning("{0} pylons updated with new HGT values in {1}".format(lecount, runtime(pylong_start, pylong_finish)))
	break


#----------------------------------------------------------------------
''''''''' Building in BUA Scaler '''''''''
# Descales buildings within BUAs that don't have important FFNs, have a height < 46m, and aren't navigation landmarks
# Scales in buildings within BUAs that do have important FFNs, have a height >= 46m, or are navigation landmarks
while bool_dict[tool_names.building]:
	# Initialize task
	building_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.building))
	#~~~~~ Royal Decree Variables ~~~~~
	bua_count = 0
	total_2upscale = 0
	total_2descale = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	if not ap.Exists('SettlementSrf'): # Task can't run if SettlementSrf fc is missing
		ap.AddError("\n*** Failed to run {0} ***".format(tool_names.building))
		ap.AddError("SettlementSrf feature class missing\n")
		break
	if not ap.Exists('StructureSrf') and not ap.Exists('StructurePnt'): # Task can't run if both StructureSrf and StructurePnt fcs are missing. Only one is fine.
		ap.AddError("\n*** Failed to run {0} ***".format(tool_names.building))
		ap.AddError("StructureSrf and StructurePnt feature classes missing\n")
		break

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
		ap.AddWarning("\nNo BUAs found.")
		building_finish = dt.now()
		write("{0} finished in {1}".format(tool_names.building, runtime(building_start, building_finish)))
		break

	if ap.Exists('StructureSrf'):
		if bool_dict[tool_names.vogon] and bool_dict[tool_names.disable]: # disable_editor_tracking() won't apply to StructureSrf and Pnt if Skip Buildings is checked. correct for that here.
			ap.AddWarning("Disabling Editor Tracking for StructureSrf feature class.")
			ap.DisableEditorTracking_management('StructureSrf')

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

	if ap.Exists('StructurePnt'):
		if bool_dict[tool_names.vogon] and bool_dict[tool_names.disable]: # disable_editor_tracking() won't apply to StructureSrf and Pnt if Skip Buildings is checked. correct for that here.
			ap.AddWarning("Disabling Editor Tracking for StructurePnt feature class.")
			ap.DisableEditorTracking_management('StructurePnt')

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
	clear_cache(["buas", "building_s_50k+", "building_s_50k+_within_2descale", "building_s_12.5k", "building_s_12.5k_within_2upscale"])

	write("{0} building surfaces scaled to 250k.".format(total_2upscale_s))
	write("{0} building surfaces scaled to 12500.".format(total_2descale_s))
	write("{0} building points scaled to 50000.".format(total_2upscale_p))
	write("{0} building points scaled to 12500.".format(total_2descale_p))
	building_finish = dt.now()
	ap.AddWarning("\n{0} finished in {1}".format(tool_names.building, runtime(building_start, building_finish)))
	break


#----------------------------------------------------------------------
''''''''' CACI Swap Scale and CTUU '''''''''
# Swaps the Scale field with the CTUU field so we can work normally with CACI data
while bool_dict[tool_names.swap]:
	swap_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.swap))
	if caci_schema:
		ap.AddWarning("CACI schema containing 'Scale' field identified")
	else:
		ap.AddError("Provided TDS does not match CACI schema containing the 'Scale' field.\nCannot run CACI Swap Scale and CTUU")
		break

	caci_featureclass = featureclass
	if 'StructurePnt' not in caci_featureclass and ap.Exists('StructurePnt'):
		caci_featureclass.append(u'StructurePnt')
	if 'StructureSrf' not in caci_featureclass and ap.Exists('StructureSrf'):
		caci_featureclass.append(u'StructureSrf')
	caci_featureclass.sort()

	write("Swapping CTUU and Scale for {0}".format(gdb_name))
	write("\nNote: The SAX_RX9 field will be changed from <NULL> to 'Scale Swapped' after the first swap. It will flip back and forth in subsequent runs.\nIf the tool was aborted on a previous run for some reason, it will reset all feature classes to the dominant swap format to maintain internal consistency. It is still up to the user to know which format they were swapping from. (Either Scale->CTUU or CTUU->Scale) Check the tool output for more information on which feature classes were changed.\n")
	fields = ['zi026_ctuu', 'scale', 'swap', 'progress', 'sax_rx9']
	fields[1] = str(scale_name)

	# Explicit is better than implicit
	#populated = lambda x: x is not None and str(x).strip() != '' # Finds empty fields. See UFI process

	write("\nChecking if any previous swaps were canceled. Please wait...")
	swap_fc = []
	none_fc = []
	empty_fc = []
	chk_fields = ['sax_rx9', 'scale']
	chk_fields[1] = str(scale_name)
	clean_proceed = False
	swap_dom = False
	none_dom = False
	for fc in caci_featureclass:
		if not get_count(fc):
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
		ap.AddWarning("\n***Previous run was flagged. Resetting feature classes to previous format.***\n")
		if swap_dom:
			ap.AddWarning("Majority of feature classes tagged as 'Scale Swapped'. Updating the following feature classes to match:")
			ap.AddWarning("\n".join(i for i in none_fc) + "\n")
		if none_dom:
			ap.AddWarning("Majority of feature classes /not/ tagged as 'Scale Swapped'. Updating the following feature classes to match:")
			ap.AddWarning("\n".join(i for i in swap_fc) + "\n")
	if clean_proceed:
		write("Previous swaps finished properly. Continuing...\n")

	# Swippity Swappity Loop
	for fc in caci_featureclass:
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
	ap.AddWarning("{0} finished in {1}".format(tool_name, runtime(swap_start, swap_finish)))
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Database Management Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

#----------------------------------------------------------------------
''''''''' Database Feature Report '''''''''
# Refactored from John Jackson's Feature_Itemized_Counter tool by Nat Cagle
while bool_dict[tool_names.fcount]:
	fcount_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.fcount))
	#~~~~~ Royal Decree Variables ~~~~~
	pnt_cnt = 0
	crv_cnt = 0
	srf_cnt = 0
	tots_f = 0
	hydro_cnt = 0
	trans_cnt = 0
	building_cnt = 0
	landcover_cnt = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	if not 'StructurePnt' in featureclass and ap.Exists('StructurePnt'):
		featureclass.append(u'StructurePnt')
	if not 'StructureSrf' in featureclass and ap.Exists('StructureSrf'):
		featureclass.append(u'StructureSrf')
	featureclass.sort()

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

	ap.AddWarning("Feature Count Report created. File located in database folder:\n{0}".format(results))
	fcount_finish = dt.now()
	ap.AddWarning("{0} finished in {1}".format(tool_names.fcount, runtime(fcount_start, fcount_finish)))
	break


#----------------------------------------------------------------------
''''''''' Source Analysis Report '''''''''
# Refactored from John Jackson's Version_Source_Counter tool by Nat Cagle
while bool_dict[tool_names.vsource]:
	vsource_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.vsource))

	if not 'StructurePnt' in featureclass and ap.Exists('StructurePnt'):
		featureclass.append(u'StructurePnt')
	if not 'StructureSrf' in featureclass and ap.Exists('StructureSrf'):
		featureclass.append(u'StructureSrf')
	featureclass.sort()

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

	ap.AddWarning("Source Analysis Report created. File located in database folder:\n{0}".format(rresults))
	vsource_finish = dt.now()
	ap.AddWarning("{0} finished in {1}".format(tool_names.vsource, runtime(vsource_start, vsource_finish)))
	break



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



'''
╔═══════════════════════════════╗
║ Report Formatting and Wrap Up ║
╚═══════════════════════════════╝
'''
#----------------------------------------------------------------------
write("\nFreeing partition memory")
check_defense('in', bool_dict[tool_names.metrics]) # Checks back in the Defense Mapping extension. Only need for Calculate Metrics. Soon to be deprecated.
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
	write(u"    |          {0} Duplicate or blank UFIs   {1}{2}|".format(ufi_total, format_count(ufi_total), exs))
if bool_dict[tool_names.hydro] or bool_dict[tool_names.trans] or bool_dict[tool_names.util]:
	write(u"    |     - Integrated and Repaired:             {0}|".format(exs))
	if bool_dict[tool_names.hydro]:
		write(u"    |          {0} Hydro                     {1}{2}|".format(hfeat_count, format_count(hfeat_count), exs))
	if bool_dict[tool_names.trans]:
		write(u"    |          {0} Trans                     {1}{2}|".format(tfeat_count, format_count(tfeat_count), exs))
	if bool_dict[tool_names.util]:
		write(u"    |          {0} Utilities                 {1}{2}|".format(ufeat_count, format_count(ufeat_count), exs))
if bool_dict[tool_names.explode]:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
	write(u"    |          {0} Complex features found    {1}{2}|".format(total_complex, format_count(total_complex), exs))
	write(u"    |          {0} Features exploded         {1}{2}|".format(total_multi, format_count(total_multi), exs))
if bool_dict[tool_names.dups]:
	write(u"    |     - Deleted Identical Features           {0}|".format(exs))
	write(u"    |          {0} Duplicates found          {1}{2}|".format(dup_count, format_count(dup_count), exs))
if bool_dict[tool_names.bridge]:
	write(u"    |     - Bridge WID Updater                   {0}|".format(exs))
	if not ap.Exists('TransportationGroundCrv'):
		ap.AddError(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		ap.AddError(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not total_bridges:
		ap.AddWarning(u"    |          No default bridges found          {0}|".format(exs))
	else:
		write(u"    |          {0} Bridges updated           {1}{2}|".format(updated_bridges, format_count(updated_bridges), exs))
		write(u"    |          {0} Default bridges remaining {1}{2}|".format(remaining_default_bridges, format_count(remaining_default_bridges), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.pylong]:
	write(u"    |     - Pylon HGT Updater                    {0}|".format(exs))
	if not ap.Exists('UtilityInfrastructurePnt') or not ap.Exists('UtilityInfrastructureCrv'):
		ap.AddError(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		ap.AddError(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not total_pylons:
		ap.AddWarning(u"    |          No default pylons found           {0}|".format(exs))
	else:
		write(u"    |          {0} Pylons updated            {1}{2}|".format(lecount, format_count(lecount), exs))
		write(u"    |          {0} Defaults not updated      {1}{2}|".format(total_rem_p, format_count(total_rem_p), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.building]:
	write(u"    |     - Building in BUA Scaler               {0}|".format(exs))
	if not ap.Exists('SettlementSrf') or (not ap.Exists('StructureSrf') and not ap.Exists('StructurePnt')):
		ap.AddError(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		ap.AddError(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not bua_count:
		ap.AddWarning(u"    |          No BUAs found                     {0}|".format(exs))
	else:
		write(u"    |          {0} Buildings upscaled        {1}{2}|".format(total_2upscale, format_count(total_2upscale), exs))
		write(u"    |          {0} Buildings descaled        {1}{2}|".format(total_2descale, format_count(total_2descale), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.swap]:
	write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
if bool_dict[tool_names.fcount]:
	write(u"    |     - Feature report generated             {0}|".format(exs))
	write(u"    |          {0} Point Features            {1}{2}|".format(pnt_cnt, format_count(pnt_cnt), exs))
	write(u"    |          {0} Curve Features            {1}{2}|".format(crv_cnt, format_count(crv_cnt), exs))
	write(u"    |          {0} Surface Features          {1}{2}|".format(srf_cnt, format_count(srf_cnt), exs))
	write(u"    |          {0} Total Features            {1}{2}|".format(tots_f, format_count(tots_f), exs))
	write(u"    |          {0} Hydrography Features      {1}{2}|".format(hydro_cnt, format_count(hydro_cnt), exs))
	write(u"    |          {0} Transportation Features   {1}{2}|".format(trans_cnt, format_count(trans_cnt), exs))
	write(u"    |          {0} Buildings                 {1}{2}|".format(building_cnt, format_count(building_cnt), exs))
	write(u"    |          {0} Landcover Surfaces        {1}{2}|".format(landcover_cnt, format_count(landcover_cnt), exs))
	write(u"    |          Check the output for more info    {0}|".format(exs))
if bool_dict[tool_names.vsource]:
	write(u"    |     - Source report generated              {0}|".format(exs))
	write(u"    |          Check the output for more info    {0}|".format(exs))

#-----------------------------------
# Easter Egg
if not bool_dict[tool_names.loc] and not bool_dict[tool_names.disable] and not bool_dict[tool_names.vogon] and not bool_dict[tool_names.repair] and not bool_dict[tool_names.fcode] and not bool_dict[tool_names.defaults] and not bool_dict[tool_names.metrics] and not bool_dict[tool_names.ufi] and not bool_dict[tool_names.hydro] and not bool_dict[tool_names.trans] and not bool_dict[tool_names.util] and not bool_dict[tool_names.explode] and not bool_dict[tool_names.dups] and not bool_dict[tool_names.bridge] and not bool_dict[tool_names.pylong] and not bool_dict[tool_names.building] and not bool_dict[tool_names.swap] and not bool_dict[tool_names.fcount] and not bool_dict[tool_names.vsource]:
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	ap.AddWarning(u"    |       Kristen, click a check box and       {0}|".format(exs))
	ap.AddWarning(u"    |             stop being cheeky.             {0}|".format(exs))

#-----------------------------------
write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")
