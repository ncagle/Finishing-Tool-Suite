import arcpy as ap
from arcpy import AddMessage as write


class Student(object): # Class definition in script
	name = 'Nat'
	color = 'Green'
	def __init__(self):
		self.age = 20  # instance attribute

	@classmethod
	def a_b(self, a, b): # Class method to be called with arcmagic as pseudo-module
		c = a+b
		write("Outside Student class method a+b=c: {0}".format(c))
		return c

	@classmethod
	def write_info(self, name, var): # Write information for given variable
		#write_info('var_name', var)
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		write("Debug info for {0}:".format(name))
		write("   Variable Type: {0}".format(type(var)))
		if type(var) is str or type(var) is unicode:
			write("   Assigned Value: '{0}'".format(var))
		else:
			write("   Assigned Value: {0}".format(var))
		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


class new_mod(Student):
	x = Student()
	def __init__(self):
		self.y = 20

	@classmethod
	def extract_mod(self):
		obj_inst = self.x.a_b(1,2)
		return obj_inst


class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Import Me"
		self.alias = "importme"

		# List of tool classes associated with this toolbox
		self.tools = [modtool]


class modtool(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "ModTool"
		self.description = ""
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		params = None
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		write("This is the execute function of importme.")
		class Student(object): # Class definition in script
			name = 'Nat'
			color = 'Green'
			def __init__(self):
				self.age = 20  # instance attribute
				self.test = 'what the fuck'

			@classmethod
			def a_b(self, a, b): # Class method to be called with arcmagic as pseudo-module
				c = a+b
				write("class method inside tool execute a+b=c: {0}".format(c))
				return c

			@classmethod
			def write_info(self, name, var): # Write information for given variable
				#write_info('var_name', var)
				write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
				write("Debug info for {0}:".format(name))
				write("   Variable Type: {0}".format(type(var)))
				if type(var) is str or type(var) is unicode:
					write("   Assigned Value: '{0}'".format(var))
				else:
					write("   Assigned Value: {0}".format(var))
				write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

		write("Class Student definition made. returning Student object.")
