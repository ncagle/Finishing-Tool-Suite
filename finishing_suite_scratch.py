

'''
    python_toolbox_name.pyt
    Author: username
    Revised: mm/dd/yyyy
    ---------------------------------------------------------------------------
    Python toolbox (.pyt) description and special instructions.
'''

# ====================== #
# Finishing Tool Scratch #
# Nat Cagle 2022-03-01   #
# ====================== #
import arcpy
from arcpy import AddMessage as write
from datetime import datetime as dt
import uuid
import os
import sys
import time
import math

#            ________________________________
#           | Runs Populate FCode, Calculate |
#           | Default Values, Integrate and  |
#           | Repair for hydro, trans, and   |
#           | utilities, updates UFI values, |
#           | deletes identical features,    |
#           | calculates geometry metrics,   |
#           | repairs all NULL geometries,   |
#           | and explodes all multipart     |
#           | features.                      |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~



"""
This is general testing ground and scratch code.
I was using it to fiddle with progressors and migrating to a python toolbox.
~NJC
"""



def make_param(disp_name, p_name, data_type, default_val=None, p_type='Required', p_dir='Input'):
    ''' Global function to create new parameters for a tool. Avoid a lot of
        repetitive code with this. '''
    param = arcpy.Parameter(
        displayName=disp_name,
        name=p_name,
        datatype=data_type,
        parameterType=p_type,
        direction=p_dir
    )
    param.value = default_val
    return param


class Toolbox(object):
    def __init__(self):
        ''' Define the toolbox (the name of the toolbox is the name of the .pyt
            file). '''
        self.label = 'Finishing Suite'
        self.alias = 'finishingsuite'

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Finishing(object):
    def __init__(self):
        ''' Define the tool (tool name is the name of the class). '''
        self.label = 'Finishing Suite v8'
        self.description = 'The collection of Finishing tools and processes.'
        self.category = ''  # Optionally place tool in a named toolset within toolbox
        self.canRunInBackground = False
        self.parameters = [
            # make_param('Output Geodatabase', 'out_gdb', 'DEWorkspace', r'C:\WorkSpace\Temp\temp.gdb'),
            # make_param('Input Layer', 'in_lyr', 'GPFeatureLayer'),
            # make_param('Input Field', 'in_field', 'Field'),
            # ...
        ]

    def getParameterInfo(self):
        ''' Return parameter list defined in tool's __init__ method. Can set
            any additional proprieties, such as filters, for parameters here.
            Just reference them using their index in the parameter list. '''
        # self.parameters[0].filter.list = ['Local Database']
        # self.parameters[2].parameterDependencies = [self.parameters[1].name]
        # ...
        return self.parameters

    def isLicensed(self):
        ''' Set whether tool is licensed to execute. '''
        return True

    def updateParameters(self, parameters):
        ''' Modify the values and properties of parameters before internal
            validation is performed. This method is called whenever a parameter
            has been changed. '''
        return

    def updateMessages(self, parameters):
        ''' Modify the messages created by internal validation for each tool
            parameter. This method is called after internal validation. '''
        return

    def execute(self, parameters, messages):
        ''' The source code of the tool. '''
        return












'''
Demonstrates a step progressor by looping through records
on a table. Use a table with 10,000 or so rows - smaller tables
just whiz by.
   1 = table name
   2 = field on the table
'''

import arcpy
import time
import math

try:
    inTable = arcpy.GetParameterAsText(0)
    inField = 'OID@'

    # Determine number of records in table
    #
    record_count = int(arcpy.GetCount_management(inTable).getOutput(0))
    if record_count == 0:
        raise ValueError("{0} has no records to count".format(inTable))

    arcpy.AddMessage("Number of rows = {0}\n".format(record_count))

    # Method 1: Calculate and use a suitable base 10 increment
    # ===================================

    p = int(math.log10(record_count))
    if not p:
        p = 1
    increment = int(math.pow(10, p - 1))

    arcpy.SetProgressor(
        "step", "Incrementing by {0} on {1}".format(increment, inTable),
        0, record_count, increment)

    beginTime = time.clock()
    with arcpy.da.SearchCursor(inTable, [inField]) as cursor:
        for i, row in enumerate(cursor, 0):
            if (i % increment) == 0:
                arcpy.SetProgressorPosition(i)
            fieldValue = row[0]

    arcpy.SetProgressorPosition(i)
    arcpy.AddMessage("Method 1")
    arcpy.AddMessage("\tIncrement = {0}".format(increment))
    arcpy.AddMessage("\tElapsed time: {0}\n".format(time.clock() - beginTime))

    # Method 2: let's just move in 10 percent increments
    # ===================================
    increment = int(record_count / 10.0)
    arcpy.SetProgressor(
        "step", "Incrementing by {0} on {1}".format(increment, inTable),
        0, record_count, increment)

    beginTime = time.clock()
    with arcpy.da.SearchCursor(inTable, [inField]) as cursor:
        for i, row in enumerate(cursor, 0):
            if (i % increment) == 0:
                arcpy.SetProgressorPosition(i)
            fieldValue = row[0]

    arcpy.SetProgressorPosition(i)
    arcpy.AddMessage("Method 2")
    arcpy.AddMessage("\tIncrement = {0}".format(increment))
    arcpy.AddMessage("\tElapsed time: {0}\n".format(time.clock() - beginTime))

    # Method 3: use increment of 1
    # ===================================
    increment = 1
    arcpy.SetProgressor("step",
                        "Incrementing by 1 on {0}".format(inTable),
                        0, record_count, increment)

    beginTime = time.clock()
    with arcpy.da.SearchCursor(inTable, [inField]) as cursor:
        for row in cursor:
            arcpy.SetProgressorPosition()
            fieldValue = row[0]

    arcpy.SetProgressorPosition(record_count)
    arcpy.ResetProgressor()
    arcpy.AddMessage("Method 3")
    arcpy.AddMessage("\tIncrement = {0}".format(increment))
    arcpy.AddMessage("\tElapsed time: {0}\n".format(time.clock() - beginTime))

    arcpy.AddMessage("Pausing for a moment to allow viewing...")
    time.sleep(2.0)  # Allow viewing of the finished progressor

except Exception as e:
    arcpy.AddError(e[0])










# Add causes and potential solutions to error log if necessary
if error_count != 0:
	write("\n\n\n\#\#\# Causes and Potential Solutions \#\#\#\n")
	write("999999 Errors:")
	write("ESRI Support defines the cause of this error as 'Something unexpected', which is incredibly helpful.")
	write("\t- There may be NULL geometry, short segments, self intersections, or other geometry problems in the feature class. This is a common cause.")
	write("\t\tIf you haven't already, try running the Repair Geometry tool from the XXX toolbox on the problem feature class.")
	write("\t- Check that the name of the input TDS is only alphanumeric and doesn't start with a number. (weird legacy ArcMap requirements)")
	write("\t- Make sure you have permissions to access the TDS you are working with. Always work with local copies, not files on the Q: or T:")
	write("\t- The feature class may be too big. This is a common problem for us working on limited hardware.")
	write("\t\tYou can try running the tool on a computer with more RAM. But our computers may not be capable.")
	write("\t\tYou could pull the problem feature class out of the GDB break it into smaller chunks. This is time consuming though and may not be enough.")
	write("\t- ArcMap may not be properly cleaning up its temp files. Try going to %localappdata%\\temp in the file explorer and deleteing everything in the folder.\n")
	write("999998 Errors:")
	write("This is 999999's drunk uncle. Similar to the previous error, but with ArcMap denying any and all responsibility.")
	write("\t- ESRI considers this a general 'operating system error' that could be 'various error conditions.'")
	write("\t- The main reason for this error is usually a feature class being too big.")
	write("\t- Some of the other solutions above might help if nothing else does.\n")
	write("If an error mentions Topology or the Topoengine, this is ArcMap scapegoating. These are also usually geometry or size issues. Same as above.\n")
	write("If the error is something other than these, the could be any number of causes. You can google the error or message Nat with a screenshot.\n\n")
	write("For more information, check out this article.\nDeath, Taxes and the Esri ArcGIS 999999 Error\nhttps://gisgeography.com/esri-arcgis-999999-error/")












''''''''' Mass Merge GDBs '''''''''
if merge:
	"""
	A tool to merge one or more geodatabases of matching schema into a single
	geodatabase. Source and target geodatabases can be local (file) geodatabases or
	ArcSDE database connections. Any datasets or feature classes that do not match
	the target schema will be ignored. Duplicate data will be persisted if present
	(duplicate features will not be removed).
	Adapted from http://projects.sarasafavi.com/mergegeodatabases through the
	Internet Archive Wayback Machine circa 2014
	"""

	import arcpy
	import os
	import time
	from arcpy import AddMessage as write

	START = time.time()

	#### SET THESE VARIABLES BEFORE USING ####
	model_path = arcpy.GetParameterAsText(0) # path to target geodatabase - schema should match that of input geodatabase(s)
	paths_list = arcpy.GetParameterAsText(1) # list of (str) paths to input geodatabase(s)
	paths_to_load = paths_list.split(";")
	write(paths_to_load)

	def list_layers(gdb):
		"""
			Creates a list of feature classes in current workspace with full paths
			(including path to parent geodatabase). Returns list of layers.
		"""
		write("\nGenerating layer list...")
		arcpy.env.workspace = gdb
		lyrs = []
		for ds in arcpy.ListDatasets():
			for fc in arcpy.ListFeatureClasses(feature_dataset = ds):
				fullpath = os.path.join(gdb, ds, fc)
				lyrs.append(fullpath)
		return lyrs

	if __name__ == "__main__":
		for gdb in paths_to_load:
			arcpy.env.workspace = gdb

			write("***Beginning processing for {0}***".format(gdb))
			lyrs = list_layers(gdb)

			for lyr in lyrs:
				fc = os.path.basename(lyr)
				ds = os.path.basename(os.path.dirname(lyr))
					# if no dataset (i.e., fc is in root of geodatabase) then
					# ds = empty string
				target = os.path.join(model_path, ds, fc)
					# if ds = '' then join correctly ignores

				try:
				# append lyr to model_path/<ds>/<fc>
					arcpy.Append_management(lyr, target)
					write("Appended: {0}".format(target))
					with open ("appended_layers.txt", "a") as txt:
						txt.write("{0}\n".format(lyr))
				except arcpy.ExecuteError as e:
					if "000732" in e:
						pass
						# target does not contain this feature class name
						# TODO copy entire source layer to target?
					else:
						# log failed attempts to append (e.g., non-matching schemas)
						with open ("append_errors.txt", "a") as txt:
							txt.write("***Failed to append {0}\n\t{1}\n".format(lyr, e))
					write(e)
					pass

		END = time.time()
		write("***Processing complete: time elapsed = {0} seconds***".format(END-START))









def copy_fc(source, target, *args, **kwargs): #(s_f)ields, (s_q)uery, (t_f)ields, (t_q)uery
	# copy_fc(source_var, target_var, s_f=s_fields, s_q=s_query, t_f=t_fields, t_q=t_query)
    s_fields = kwargs.get('s_f', "'*'") # Default s_fields variable will be '*' for all fields
    s_query = kwargs.get('s_q', "''")
    t_fields = kwargs.get('t_f', "'*'") # Default t_fields variable will be '*' for all fields
    t_query = kwargs.get('t_q', "''")

	with arcpy.da.SearchCursor(source, s_fields, s_query) as scursor:
		with arcpy.da.InsertCursor(target, t_fields, t_query) as icursor:
			for row in scursor:
				icursor.insertRow(row)






# Conversion toolset
@gptooldoc('LoadData_production', None)
def LoadData(in_cross_reference=None, in_sources=None, in_target=None, in_dataset_map_defs=None, row_level_errors=None):
    """LoadData_production(in_cross_reference, in_sources;in_sources..., in_target, {in_dataset_map_defs;in_dataset_map_defs...}, {row_level_errors})

        Moves features from one schema to another by loading data from a
        source to a target workspace.  Data mapping rules described in a
        cross-reference database are applied during the load. All Esri Mapping
        and Charting solutions products install a cross-reference database
        that you can use. You can create a cross-reference database using the
        Create Cross-reference tool.Data that matches the schema defined in
        the cross-reference database
        for the source is appended to the target workspace. The cross-
        reference database contains a DatasetMapping table that lists pairs of
        source and target dataset names. Each source and target name pair can
        have a WHERE clause and a subtype. The WHERE clause defines a subset
        of features in the source to append to the target. Subtype identifies
        a subtype in the target feature class into which features are loaded.

     INPUTS:
      in_cross_reference (Workspace):
          The path to a cross-reference database. Cross-reference databases for
          each product specification reside in the <install location>\\SolutionNa
          me\\Desktop10.2\\[ProductName]\\[SpecificationName]\\DataConversion
          directory.
      in_sources (Workspace):
          A list of workspaces that contain the source features to load into the
          target workspace.
      in_target (Workspace):
          The target workspace that contains the schema referenced in the cross-
          reference database. Source features are loaded into this workspace.
      in_dataset_map_defs {String}:
          The source to target feature class mapping list. The format of this
          string is id | SourceDataset | TargetDataset | WhereClause | Subtype.
      row_level_errors {Boolean}:
          Indicates if the tool will log errors that occur while inserting new
          rows into feature classes and tables in the in_target parameter.

          * ROW_LEVEL_ERROR_LOGGING-Log errors that occur during individual row-
          level inserts. This is the default.

          * NO_ROW_LEVEL_ERROR_LOGGING-Do not log errors that occur during
          individual row-level inserts."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LoadData_production(*gp_fixargs((in_cross_reference, in_sources, in_target, in_dataset_map_defs, row_level_errors), True)))
        return retval
    except Exception as e:
        raise e






import arcpy
fcList = [a list of FCs that you want to merge together]
outputFC = r"C:\temp\test.gdb\merge"
for fc in fcList:
    if fcList.index(fc) == 0:
        arcpy.CopyFeatures_management(fc, outputFC)
        insertRows = arcpy.da.InsertCursor(outputFC, ["SHAPE@","*"])
    else:
        searchRows = arcpy.da.SearchCursor(fc, ["SHAPE@","*"])
        for searchRow in searchRows:
            insertRows.insertRow(searchRow)
        del searchRow, searchRows
    print "Appended " + str(fc) + "..."
del insertRows
Reply With Quote Reply With Quote Top Bottom








# Gets messages from the ArcGIS tools ran and sends messages to dialog
def writeresults():
    messages = GetMessages(0)
    warnings = GetMessages(1)
    errors = GetMessages(2)
    AddMessage(messages)
    if len(warnings) > 0:
        AddWarning(warnings)
    if len(errors) > 0:
        AddError(errors)
    return
