

'''
    python_toolbox_name.pyt
    Author: username
    Revised: mm/dd/yyyy
    ---------------------------------------------------------------------------
    Python toolbox (.pyt) description and special instructions.
'''

# ==================== #
# Finishing Tool v6    #
# Nat Cagle 2021-10-04 #
# ==================== #
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
