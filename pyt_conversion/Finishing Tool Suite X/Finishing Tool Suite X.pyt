import arcpy as ap
from arcpy import AddMessage as write
import arcmagic

def global_func():
	write("\nThis is printing from the global function outside the Tool classes.\n")


class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Finishing Tool Suite X"
		self.alias = "phoenix"

		# List of tool classes associated with this toolbox
		self.tools = [FinishingTools, PreprocessingTools]


class FinishingTools(object):
	class ToolValidator(object):
		"""Class for validating a tool's parameter values and controlling
		the behavior of the tool's dialog."""

		def __init__(self, parameters):
			"""Setup arcpy and the list of tool parameters."""
			self.params = parameters

		def initializeParameters(self):
			"""Refine the properties of a tool's parameters.  This method is
			called when the tool is opened."""
			self.params[0].category = "1 Data Maintenance Tools"
			return

		def updateParameters(self):
			"""Modify the values and properties of parameters before internal
			validation is performed.  This method is called whenever a parameter
			has been changed."""
			return

		def updateMessages(self):
			"""Modify the messages created by internal validation for each tool
			parameter.  This method is called after internal validation."""
			return

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Finishing Tools"
		self.description = ""
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		# First parameter
		param_0 = ap.Parameter(
			name = 'TDS',
			displayName = 'TDS   (The standard Finishing process is checked by default)   (Tools are run in list order)',
			parameterType = 'Optional',
			direction = 'Input',
			datatype = 'Feature Dataset')

		# # Second parameter
		# param_1 = ap.Parameter(
		# 	name = 'sinuosity_field',
		# 	displayName = 'Sinuosity Field',
		# 	parameterType = 'Optional',
		# 	direction = 'Input',
		# 	datatype = 'Field')
		# param_1.value = "sinuosity"
		#
		# # Third parameter
		# param_2 = ap.Parameter(
		# 	name = 'out_features',
		# 	displayName = 'Output Features',
		# 	parameterType = 'Derived',
		# 	direction = 'Output',
		# 	datatype = 'GPFeatureLayer')
		# param_2.parameterDependencies = [param_0.name]
		# param_2.schema.clone = True

		params = [param_0] #, param_1, param_2]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		validator = getattr(self, 'ToolValidator', None)
		if validator:
			return validator(parameters).updateParameters()

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		validator = getattr(self, 'ToolValidator', None)
		if validator:
			return validator(parameters).updateMessages()

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		global_func()
		test_var = 'testicles'
		arcmagic.write_info('test_var', test_var)
		return

class PreprocessingTools(object):
	class ToolValidator(object):
		"""Class for validating a tool's parameter values and controlling
		the behavior of the tool's dialog."""

		def __init__(self, parameters):
			"""Setup arcpy and the list of tool parameters."""
			self.params = parameters

		def initializeParameters(self):
			"""Refine the properties of a tool's parameters.  This method is
			called when the tool is opened."""
			self.params[0].category = "1 Data Maintenance Tools"
			return

		def updateParameters(self):
			"""Modify the values and properties of parameters before internal
			validation is performed.  This method is called whenever a parameter
			has been changed."""
			return

		def updateMessages(self):
			"""Modify the messages created by internal validation for each tool
			parameter.  This method is called after internal validation."""
			return

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Preprocessing Tools"
		self.description = ""
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		# First parameter
		param_0 = ap.Parameter(
			name = 'TDS',
			displayName = 'TDS   (The standard Finishing process is checked by default)   (Tools are run in list order)',
			parameterType = 'Optional',
			direction = 'Input',
			datatype = 'Feature Dataset')

		# # Second parameter
		# param_1 = ap.Parameter(
		# 	name = 'sinuosity_field',
		# 	displayName = 'Sinuosity Field',
		# 	parameterType = 'Optional',
		# 	direction = 'Input',
		# 	datatype = 'Field')
		# param_1.value = "sinuosity"
		#
		# # Third parameter
		# param_2 = ap.Parameter(
		# 	name = 'out_features',
		# 	displayName = 'Output Features',
		# 	parameterType = 'Derived',
		# 	direction = 'Output',
		# 	datatype = 'GPFeatureLayer')
		# param_2.parameterDependencies = [param_0.name]
		# param_2.schema.clone = True

		params = [param_0] #, param_1, param_2]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		validator = getattr(self, 'ToolValidator', None)
		if validator:
			return validator(parameters).updateParameters()

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		validator = getattr(self, 'ToolValidator', None)
		if validator:
			return validator(parameters).updateMessages()

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		global_func()
		return
