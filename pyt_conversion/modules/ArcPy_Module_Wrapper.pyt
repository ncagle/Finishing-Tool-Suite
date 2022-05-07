import arcpy as ap
from arcpy import AddMessage as write
import inspect
import sys

# apipath = r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules"
# sys.path.insert(0, apipath)
# import Import_Me as im


def global_func():
	write("\nThis is printing from the global function outside the Tool classes.\n")

# ap.ImportToolbox(r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\ArcPy Modules.tbx")
ap.ImportToolbox(r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\Import_Me.pyt")


write("Cannot output a message from this part of the python toolox")


class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "ArcPy Module Wrapper"
		self.alias = "wrapper"

		# List of tool classes associated with this toolbox
		self.tools = [importmodules]


class importmodules(object):

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
		self.label = "Import Modules"
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

		# Second parameter
		param_1 = ap.Parameter(
			name = 'sinuosity_field',
			displayName = 'Sinuosity Field',
			parameterType = 'Optional',
			direction = 'Input',
			datatype = 'Field')
		param_1.value = "sinuosity"

		# Third parameter
		param_2 = ap.Parameter(
			name = 'out_features',
			displayName = 'Output Features',
			parameterType = 'Derived',
			direction = 'Output',
			datatype = 'GPFeatureLayer')
		param_2.parameterDependencies = [param_0.name]
		param_2.schema.clone = True

		params = [param_0, param_1, param_2]
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
		test_var = 'test_value\n'
		write(test_var)

		tempcode = ap.importme.modtool.__code__
		write(type(tempcode))
		write(tempcode)
		write(inspect.getsource(tempcode))
		#del arcpy.importme
		#del arcpy.modtool_importme
		#write(dir(arcpy))

		# from arcpy import toolbox_code
		# write(ap.toolbox_code.__file__)
		# tbxfile = r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\Import Me.pyt"
		# tbxfile2 = r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\ArcPy Modules.tbx"
		# output_file = r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\gen_tbx_output.py"
		# module_name = 'importme'
		# mycode = toolbox_code.generate_toolbox_module(tbxfile, output_file, True, True, False, module_name, True)
		# write(mycode)
		# code_for_toolbox(tbxfile, True, output_file, False, module_name, True)

		# from arcpy.geoprocessing._base import gp, gp_fixargs
		# gp.addToolbox(tbxfile, 'importme')
		# gp.addToolbox(tbxfile2, 'arcmods')
		# write(gp.modtool_importme(*gp_fixargs((), True)))
		# tempvar = gp.modtool_importme(*gp_fixargs((), True)).outputCount
		# write(type(tempvar))
		# write(tempvar)
		# write(gp.arcmagic_arcmods(*gp_fixargs((), True)).outputCount)
		#
		# from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
		# retval = convertArcObjectToPythonObject(gp.modtool_importme(*gp_fixargs((), True)))
		# write(type(retval))
		# write(retval)
		# return retval



		# ap.importme.modtool.func_code
		# 	def __init__(self):
		# 		self.age = 20  # instance attribute
		# ap.importme.modtool
		# ['__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__doc__', '__esri_toolname__', '__format__', '__get__', '__getattribute__', '__globals__', '__hash__', '__init__', '__module__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'func_closure', 'func_code', 'func_defaults', 'func_dict', 'func_doc', 'func_globals', 'func_name']
		# ap.importme.modtool.__init__
		# ['__call__', '__class__', '__cmp__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__name__', '__new__', '__objclass__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
		# <method-wrapper '__init__' of function object at 0x152FE530>
		# ap.importme.modtool.__init__.__objclass__
		# ['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
		# <type 'object'>
		# ap.importme.modtool.__init__.__self__
		# ['__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__doc__', '__esri_toolname__', '__format__', '__get__', '__getattribute__', '__globals__', '__hash__', '__init__', '__module__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'func_closure', 'func_code', 'func_defaults', 'func_dict', 'func_doc', 'func_globals', 'func_name']
		# <function modtool at 0x15BDCF70>



		# pytmodule2 = ap.ImportToolbox(r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\Import Me.pyt")
		# # sys.modules["pytmodule"] = importpyt
		# # import pytmodule
		# #del sys.modules["pytmodule"]
		# #write(sys.modules)
		#
		# #write(dir(arcpy))
		# write(dir(pytmodule2))
		# write("\npytmodule2 Student:")
		# write(inspect.getsource(pytmodule2.Student.func_code))
		# # pytmodule2 Student:
		# # 	def __init__(self):
		# # 		self.age = 20  # instance attribute
		#
		# write("\npytmodule2 new_mod:")
		# write(inspect.getsource(pytmodule2.new_mod.func_code))
		# # pytmodule2 new_mod:
		# # 	def write_info(self, name, var): # Write information for given variable
		# # 		#write_info('var_name', var)
		# # 		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		# # 		write("Debug info for {0}:".format(name))
		# # 		write("   Variable Type: {0}".format(type(var)))
		# # 		if type(var) is str or type(var) is unicode:
		# # 			write("   Assigned Value: '{0}'".format(var))
		# # 		else:
		# # 			write("   Assigned Value: {0}".format(var))
		# # 		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		#
		# write("\npytmodule2 modtool:")
		# write(inspect.getsource(pytmodule2.modtool.func_code))
		# # pytmodule2 modtool:
		# # 	@classmethod
		# # 	def write_info(self, name, var): # Write information for given variable
		# # 		#write_info('var_name', var)
		# # 		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		# # 		write("Debug info for {0}:".format(name))
		# # 		write("   Variable Type: {0}".format(type(var)))
		# # 		if type(var) is str or type(var) is unicode:
		# # 			write("   Assigned Value: '{0}'".format(var))
		# # 		else:
		# # 			write("   Assigned Value: {0}".format(var))
		# # 		write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		#
		# write(type(pytmodule2.Student))
		# write(dir(pytmodule2.Student))

		return

# 'Student_importme',
# 'Tool_importme',
# 'importme',
# 'modtool_importme',
# 'new_mod_importme',




# write(parameters)
# TDS = parameters[0]
# TDS_str = parameters[0].valueAsText
# write(TDS)
# write(TDS_str)


# content = dir(ap.arcmods.arcmagic)
# content = dir(ap)
# write(content)
# write(ap.arcmods.arcmagic)
# write("\n")
#write(inspect.getsource(ap.arcmods))
#write(type(ap)) #<type 'module'>
#write(type(ap.arcmods)) #<type 'module'>
#write(type(ap.arcmods.arcmagic)) #<type 'function'> <function arcmagic at 0x26E2EF70>



#arcmagic = arcmagic(13, 'Richie', 'Gold')
# write(ap.arcmods.arcmagic) # <function arcmagic at 0x15BF0030>
# write("run ap.arcmods.arcmagic()")
# ap.arcmods.arcmagic()
# write("done")
# holder = ap.arcmods.arcmagic().getOutput(0)
# write("past holder line")
# write(type(holder)) # <type 'unicode'>
# write("holder type: ".format(type(holder))) # holder type:
# write("holder: ".format(holder)) # holder:
# holder2 = ap.arcmods.arcmagic()
# write("past holder line") #
# write(type(holder2)) # '#'
# write("holder2 type: ".format(type(holder2))) # holder2 type:
# write("holder2: ".format(holder2)) # holder2:


# arcmagic = ap.GetParameter(3)
# write(type(arcmagic))
# write(arcmagic)
#
# write(arcmagic.age)
# write(arcmagic.name)
# write(arcmagic.color)
# write(arcmagic.tostring())
#
# c_sum = arcmagic.a_b(1,2)
# write(c_sum)
# arcmagic.write_info('pass variable from pyt execute() thru pseudo-module', test_var)
# arcmagic.write_info('TDS', TDS)
# arcmagic.write_info('TDS_str', TDS_str)


#ap.arcmagic_arcmods()



#write(dir(ap.importme.modtool))
#write(inspect.getsource(pytmodule))

# ap.importme.Student.func_dict
# ['__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values', 'viewitems', 'viewkeys', 'viewvalues']
# <type 'function'>
#['__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__doc__', '__esri_toolname__', '__format__', '__get__', '__getattribute__', '__globals__', '__hash__', '__init__', '__module__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'func_closure', 'func_code', 'func_defaults', 'func_dict', 'func_doc', 'func_globals', 'func_name']






r"""{'numpy.core.info': <module 'numpy.core.info' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\info.pyc'>,
'ctypes.os': None, 'gc': <module 'gc' (built-in)>,
'fnmatch': <module 'fnmatch' from 'C:\Python27\ArcGIS10.6\lib\fnmatch.pyc'>,
'logging.weakref': None, 'pprint': <module 'pprint' from 'C:\Python27\ArcGIS10.6\lib\pprint.pyc'>,
'unittest.sys': None, 'numpy.core.umath': <module 'numpy.core.umath' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\umath.pyd'>,
'arcpy.xml': None, 'string': <module 'string' from 'C:\Python27\ArcGIS10.6\lib\string.pyc'>,
'numpy.lib.arraysetops': <module 'numpy.lib.arraysetops' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\arraysetops.pyc'>,
'arcpy._base': <module 'arcpy._base' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\_base.pyc'>,
'encodings.utf_8': <module 'encodings.utf_8' from 'C:\Python27\ArcGIS10.6\lib\encodings\utf_8.pyc'>,
'xml.etree.warnings': None, 'xml.etree.sys': None, 'subprocess': <module 'subprocess' from 'C:\Python27\ArcGIS10.6\lib\subprocess.pyc'>,
'numpy.core.machar': <module 'numpy.core.machar' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\machar.pyc'>,
'unittest.StringIO': None, 'arcpy._ga': <module 'arcpy._ga' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\_ga.pyc'>,
'numpy.ma.extras': <module 'numpy.ma.extras' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\ma\extras.pyc'>,
'numpy.fft.fftpack_lite': <module 'numpy.fft.fftpack_lite' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\fft\fftpack_lite.pyd'>,
'shlex': <module 'shlex' from 'C:\Python27\ArcGIS10.6\lib\shlex.pyc'>,
'dis': <module 'dis' from 'C:\Python27\ArcGIS10.6\lib\dis.pyc'>,
'arcpy.ddd': <module 'arcpy.ddd' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\ddd.pyc'>,
'numpy.lib': <module 'numpy.lib' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\__init__.pyc'>,
'logging.threading': None, 'arcpy.numpy': None, 'arcpy.schematics': <module 'arcpy.schematics' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\schematics.pyc'>,
'arcpy.cartography': <module 'arcpy.cartography' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\cartography.pyc'>,
'abc': <module 'abc' from 'C:\Python27\ArcGIS10.6\lib\abc.pyc'>,
'arcpy.imp': None, 'arcpy.locale': None, 'numpy.lib.npyio': <module 'numpy.lib.npyio' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\npyio.pyc'>,
'numpy.lib._compiled_base': <module 'numpy.lib._compiled_base' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\_compiled_base.pyd'>,
'arcpy.utils': <module 'arcpy.utils' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\utils.pyc'>,
'ntpath': <module 'ntpath' from 'C:\Python27\ArcGIS10.6\lib\ntpath.pyc'>,
'arcpy.stpm': <module 'arcpy.stpm' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\stpm.pyc'>,
'arcpy.arcobjects.arcobjectconversion': <module 'arcpy.arcobjects.arcobjectconversion' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\arcobjects\arcobjectconversion.pyc'>,
'numpy.fft.helper': <module 'numpy.fft.helper' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\fft\helper.pyc'>,
'unittest.suite': <module 'unittest.suite' from 'C:\Python27\ArcGIS10.6\lib\unittest\suite.pyc'>,
'_ctypes': <module '_ctypes' from 'C:\Python27\ArcGIS10.6\DLLs\_ctypes.pyd'>,
'aviationois': <module 'aviationois' from 'C:\Program Files (x86)\ArcGIS\AviationCharting\Desktop10.6\ArcToolbox\Toolboxes\aviationois.pyc'>,
'xml.etree': <module 'xml.etree' from 'C:\Python27\ArcGIS10.6\lib\xml\etree\__init__.pyc'>,
'codecs': <module 'codecs' from 'C:\Python27\ArcGIS10.6\lib\codecs.pyc'>,
'arcpy.os': None, 'wikimapia_addin': <module 'wikimapia_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{42DE8BA3-5B9D-4AD6-B676-4D014CE12EAF}\wikimapia_addin.py'>,
'StringIO': <module 'StringIO' from 'C:\Python27\ArcGIS10.6\lib\StringIO.pyc'>,
'weakref': <module 'weakref' from 'C:\Python27\ArcGIS10.6\lib\weakref.pyc'>,
'numpy.core._internal': <module 'numpy.core._internal' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\_internal.pyc'>,
'xml.dom.xmlbuilder': <module 'xml.dom.xmlbuilder' from 'C:\Python27\ArcGIS10.6\lib\xml\dom\xmlbuilder.py'>,
'numpy.lib.arraypad': <module 'numpy.lib.arraypad' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\arraypad.pyc'>,
'xml.dom.expatbuilder': <module 'xml.dom.expatbuilder' from 'C:\Python27\ArcGIS10.6\lib\xml\dom\expatbuilder.py'>,
'arcpy.uuid': None, '_sre': <module '_sre' (built-in)>,
'logging.sys': None, 'arcpy.datetime': None, 'ctypes._ctypes': None, '_heapq': <module '_heapq' (built-in)>,
'arcpy.arcobjects.xml': None, 'numpy.lib.financial': <module 'numpy.lib.financial' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\financial.pyc'>,
'binascii': <module 'binascii' (built-in)>,
'tokenize': <module 'tokenize' from 'C:\Python27\ArcGIS10.6\lib\tokenize.pyc'>,
'numpy.polynomial.chebyshev': <module 'numpy.polynomial.chebyshev' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\chebyshev.pyc'>,
'cPickle': <module 'cPickle' (built-in)>,
'numpy.polynomial.hermite_e': <module 'numpy.polynomial.hermite_e' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\hermite_e.pyc'>,
'encodings.cp1252': <module 'encodings.cp1252' from 'C:\Python27\ArcGIS10.6\lib\encodings\cp1252.pyc'>,
'arcpy._graph': <module 'arcpy._graph' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\_graph.pyc'>,
'webbrowser': <module 'webbrowser' from 'C:\Python27\ArcGIS10.6\lib\webbrowser.pyc'>,
'numpy.testing.utils': <module 'numpy.testing.utils' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\testing\utils.pyc'>,
'numpy.core.fromnumeric': <module 'numpy.core.fromnumeric' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\fromnumeric.pyc'>,
'numpy.ctypeslib': <module 'numpy.ctypeslib' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\ctypeslib.pyc'>,
'arcpy.geoprocessing._base': <module 'arcpy.geoprocessing._base' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\geoprocessing\_base.pyc'>,
'encodings.aliases': <module 'encodings.aliases' from 'C:\Python27\ArcGIS10.6\lib\encodings\aliases.pyc'>,
'exceptions': <module 'exceptions' (built-in)>,
'sre_parse': <module 'sre_parse' from 'C:\Python27\ArcGIS10.6\lib\sre_parse.pyc'>,
'numpy.random.warnings': None, 'arcpy.cmanagers': <module 'arcpy.cmanagers' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\cmanagers\__init__.pyc'>,
'logging.cStringIO': None, 'arcpy.sa.CompoundParameter': <module 'arcpy.sa.CompoundParameter' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\sa\CompoundParameter.pyc'>,
'numpy.lib.polynomial': <module 'numpy.lib.polynomial' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\polynomial.pyc'>,
'numpy.compat': <module 'numpy.compat' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\compat\__init__.pyc'>,
'arcpy.glob': None, 'numbers': <module 'numbers' from 'C:\Python27\ArcGIS10.6\lib\numbers.pyc'>,
'numpy.core.records': <module 'numpy.core.records' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\records.pyc'>,
'_subprocess': <module '_subprocess' (built-in)>,
'strop': <module 'strop' (built-in)>,
'xml.etree.ElementPath': <module 'xml.etree.ElementPath' from 'C:\Python27\ArcGIS10.6\lib\xml\etree\ElementPath.pyc'>,
'numpy.core.numeric': <module 'numpy.core.numeric' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\numeric.pyc'>,
'CableBuilder_v3_3_addin': <module 'CableBuilder_v3_3_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{577795B4-DEB7-4AFF-A79D-E3F1D1DBC207}\CableBuilder_v3_3_addin.py'>,
'arcpy.arcobjects.mixins': <module 'arcpy.arcobjects.mixins' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\arcobjects\mixins.pyc'>,
'arcpy.toolbox_code': <module 'arcpy.toolbox_code' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\toolbox_code.py'>,
'csv': <module 'csv' from 'C:\Python27\ArcGIS10.6\lib\csv.pyc'>,
'ctypes.util': <module 'ctypes.util' from 'C:\Python27\ArcGIS10.6\lib\ctypes\util.pyc'>,
'numpy.lib.utils': <module 'numpy.lib.utils' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\utils.pyc'>,
'_elementtree': <module '_elementtree' from 'C:\Python27\ArcGIS10.6\DLLs\_elementtree.pyd'>,
'numpy.lib.arrayterator': <module 'numpy.lib.arrayterator' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\arrayterator.pyc'>,
'os.path': <module 'ntpath' from 'C:\Python27\ArcGIS10.6\lib\ntpath.pyc'>,
'arcpy.da': <module 'arcpy.da' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\da.pyc'>,
'_weakrefset': <module '_weakrefset' from 'C:\Python27\ArcGIS10.6\lib\_weakrefset.pyc'>,
'unittest.traceback': None, 'unittest.os': None, 'arcpy.sa.Functions': <module 'arcpy.sa.Functions' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\sa\Functions.pyc'>,
'functools': <module 'functools' from 'C:\Python27\ArcGIS10.6\lib\functools.pyc'>,
'arcpy.edit': <module 'arcpy.edit' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\edit.pyc'>,
'sysconfig': <module 'sysconfig' from 'C:\Python27\ArcGIS10.6\lib\sysconfig.pyc'>,
'numpy.core.numerictypes': <module 'numpy.core.numerictypes' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\numerictypes.pyc'>,
'numpy.polynomial.legendre': <module 'numpy.polynomial.legendre' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\legendre.pyc'>,
'uuid': <module 'uuid' from 'C:\Python27\ArcGIS10.6\lib\uuid.pyc'>,
'numpy.matrixlib.defmatrix': <module 'numpy.matrixlib.defmatrix' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\matrixlib\defmatrix.pyc'>,
'tempfile': <module 'tempfile' from 'C:\Python27\ArcGIS10.6\lib\tempfile.pyc'>,
'imp': <module 'imp' (built-in)>,
'production': <module 'production' from 'C:\Program Files (x86)\ArcGIS\EsriProductionMapping\Desktop10.6\ArcToolbox\Toolboxes\production.pyc'>,
'arcpy.arcobjects.collections': None, 'numpy.core.scalarmath': <module 'numpy.core.scalarmath' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\scalarmath.pyd'>,
'numpy.core': <module 'numpy.core' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\__init__.pyc'>,
'xml.dom.copy': None, 'numpy.linalg.info': <module 'numpy.linalg.info' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\linalg\info.pyc'>,
'unittest.functools': None, 'xml.etree._elementtree': None, 'unittest.util': <module 'unittest.util' from 'C:\Python27\ArcGIS10.6\lib\unittest\util.pyc'>,
'arcpy.re': None, 'numpy.lib._datasource': <module 'numpy.lib._datasource' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\_datasource.pyc'>,
'Default_Value_Phoenix_addin': <module 'Default_Value_Phoenix_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{640D378E-58AC-40EE-8380-AD2F4B68F553}\Default_Value_Phoenix_addin.py'>,
'token': <module 'token' from 'C:\Python27\ArcGIS10.6\lib\token.pyc'>,
'numpy.linalg._umath_linalg': <module 'numpy.linalg._umath_linalg' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\linalg\_umath_linalg.pyd'>,
'arcpy.time': <module 'arcpy.time' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\time.pyc'>,
'cStringIO': <module 'cStringIO' (built-in)>,
'numpy.polynomial': <module 'numpy.polynomial' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\__init__.pyc'>,
'numpy.add_newdocs': <module 'numpy.add_newdocs' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\add_newdocs.pyc'>,
'arcpy.na': <module 'arcpy.na' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\na.pyc'>,
'Nidavellirs_Swage_Block_Preprocessing_addin': <module 'Nidavellirs_Swage_Block_Preprocessing_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{70197455-2BAB-45BB-BCE6-2375CF090684}\Nidavellirs_Swage_Block_Preprocessing_addin.py'>,
'encodings': <module 'encodings' from 'C:\Python27\ArcGIS10.6\lib\encodings\__init__.pyc'>,
'gapy': <module 'gapy' from 'c:\program files (x86)\arcgis\desktop10.6\bin\gapy.pyd'>,
'arcpy.logging': None, 'numpy.lib.numpy': None, 'numpy.random.threading': None, 're': <module 're' from 'C:\Python27\ArcGIS10.6\lib\re.pyc'>,
'Deimos_2': <module 'Deimos_2' from 'c:\program files (x86)\arcgis\desktop10.6\Resources\Raster\Types\System\Deimos-2\Deimos_2.pyc'>,
'math': <module 'math' (built-in)>,
'arcpy.ga': <module 'arcpy.ga' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\ga.pyc'>,
'ctypes.struct': None, 'bathymetry': <module 'bathymetry' from 'C:\Program Files (x86)\ArcGIS\MaritimeBathymetry\Desktop10.6\ArcToolbox\Toolboxes\bathymetry.pyc'>,
'_locale': <module '_locale' (built-in)>,
'logging': <module 'logging' from 'C:\Python27\ArcGIS10.6\lib\logging\__init__.pyc'>,
'thread': <module 'thread' (built-in)>,
'traceback': <module 'traceback' from 'C:\Python27\ArcGIS10.6\lib\traceback.pyc'>,
'arcpy.types': None, 'IterativeSelfSelect_addin': <module 'IterativeSelfSelect_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{B4E85733-6C2F-414F-9F53-6BC7401A58DC}\IterativeSelfSelect_addin.py'>,
'_collections': <module '_collections' (built-in)>,
'numpy.random': <module 'numpy.random' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\random\__init__.pyc'>,
'numpy.lib.twodim_base': <module 'numpy.lib.twodim_base' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\twodim_base.pyc'>,
'arcpy.sa.ParameterClasses': <module 'arcpy.sa.ParameterClasses' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\sa\ParameterClasses.pyc'>,
'xml.parsers.pyexpat': None, 'ctypes.sys': None, 'posixpath': <module 'posixpath' from 'C:\Python27\ArcGIS10.6\lib\posixpath.pyc'>,
'numpy.core.arrayprint': <module 'numpy.core.arrayprint' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\arrayprint.pyc'>,
'arcpy.codecs': None, 'types': <module 'types' from 'C:\Python27\ArcGIS10.6\lib\types.pyc'>,
'numpy.lib.stride_tricks': <module 'numpy.lib.stride_tricks' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\stride_tricks.pyc'>,
'arcpy.textwrap': None, 'numpy.lib.scimath': <module 'numpy.lib.scimath' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\scimath.pyc'>,
'arcpy.arcobjects.arcpy': None, 'arcpy._management': <module 'arcpy._management' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\_management.pyc'>,
'_codecs': <module '_codecs' (built-in)>,
'numpy.__config__': <module 'numpy.__config__' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\__config__.pyc'>,
'arcpy.sa.types': None, 'numpy.lib.ufunclike': <module 'numpy.lib.ufunclike' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\ufunclike.pyc'>,
'copy': <module 'copy' from 'C:\Python27\ArcGIS10.6\lib\copy.pyc'>,
'arcgisscripting': <module 'arcgisscripting' from 'c:\program files (x86)\arcgis\desktop10.6\bin\arcgisscripting.pyd'>,
'hashlib': <module 'hashlib' from 'C:\Python27\ArcGIS10.6\lib\hashlib.pyc'>,
'keyword': <module 'keyword' from 'C:\Python27\ArcGIS10.6\lib\keyword.pyc'>,
'_csv': <module '_csv' (built-in)>,
'numpy.lib.nanfunctions': <module 'numpy.lib.nanfunctions' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\nanfunctions.pyc'>,
'unittest.weakref': None, 'arcpy.arcobjects.functools': None, '_weakref': <module '_weakref' (built-in)>,
'sre_compile': <module 'sre_compile' from 'C:\Python27\ArcGIS10.6\lib\sre_compile.pyc'>,
'_hashlib': <module '_hashlib' from 'C:\Python27\ArcGIS10.6\DLLs\_hashlib.pyd'>,
'numpy.lib.shape_base': <module 'numpy.lib.shape_base' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\shape_base.pyc'>,
'numpy._import_tools': <module 'numpy._import_tools' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\_import_tools.pyc'>,
'logging.collections': None, 'arcpy.sa.arcgisscripting': None, '__main__': <module '__main__' (built-in)>,
'numpy.fft.info': <module 'numpy.fft.info' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\fft\info.pyc'>,
'arcpy.sys': None, 'xml.etree.cElementTree': <module 'xml.etree.cElementTree' from 'C:\Python27\ArcGIS10.6\lib\xml\etree\cElementTree.pyc'>,
'unittest.result': <module 'unittest.result' from 'C:\Python27\ArcGIS10.6\lib\unittest\result.pyc'>,
'bz2': <module 'bz2' from 'C:\Python27\ArcGIS10.6\DLLs\bz2.pyd'>,
'encodings.codecs': None, 'arcpy.functools': None, 'xml.dom.minicompat': <module 'xml.dom.minicompat' from 'C:\Python27\ArcGIS10.6\lib\xml\dom\minicompat.py'>,
'unittest.difflib': None, 'arcpy.sa.datetime': None, 'numpy.lib.index_tricks': <module 'numpy.lib.index_tricks' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\index_tricks.pyc'>,
'warnings': <module 'warnings' from 'C:\Python27\ArcGIS10.6\lib\warnings.pyc'>,
'glob': <module 'glob' from 'C:\Python27\ArcGIS10.6\lib\glob.pyc'>,
'arcpy.keyword': None, 'future_builtins': <module 'future_builtins' (built-in)>,
'aviationmanagement': <module 'aviationmanagement' from 'C:\Program Files (x86)\ArcGIS\AviationCharting\Desktop10.6\ArcToolbox\Toolboxes\aviationmanagement.pyc'>,
'arcpy.arcgisscripting': None, '_io': <module '_io' (built-in)>,
'linecache': <module 'linecache' from 'C:\Python27\ArcGIS10.6\lib\linecache.pyc'>,
'arcpy._mapping': <module 'arcpy._mapping' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\_mapping.pyc'>,
'numpy.linalg.linalg': <module 'numpy.linalg.linalg' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\linalg\linalg.pyc'>,
'pytmodule': <module 'importme' (built-in)>,
'numpy.lib._iotools': <module 'numpy.lib._iotools' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\_iotools.pyc'>,
'random': <module 'random' from 'C:\Python27\ArcGIS10.6\lib\random.pyc'>,
'unittest.types': None, 'datetime': <module 'datetime' (built-in)>,
'logging.os': None, 'ctypes._endian': <module 'ctypes._endian' from 'C:\Python27\ArcGIS10.6\lib\ctypes\_endian.pyc'>,
'encodings.encodings': None, 'unittest.pprint': None, 'arcpy.management': <module 'arcpy.management' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\management.pyc'>,
'numpy.random.mtrand': <module 'numpy.random.mtrand' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\random\mtrand.pyd'>,
'xml': <module 'xml' from 'C:\Python27\ArcGIS10.6\lib\xml\__init__.pyc'>,
'numpy.linalg': <module 'numpy.linalg' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\linalg\__init__.pyc'>,
'pyexpat.errors': <module 'pyexpat.errors' (built-in)>,
'logging.thread': None, 'xml.etree.ElementTree': <module 'xml.etree.ElementTree' from 'C:\Python27\ArcGIS10.6\lib\xml\etree\ElementTree.pyc'>,
'arcpy.pprint': None, 'pythonaddins': <module 'pythonaddins' from 'c:\program files (x86)\arcgis\desktop10.6\bin\pythonaddins.pyd'>,
'numpy.lib._version': <module 'numpy.lib._version' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\_version.pyc'>,
'arcpy.itertools': None, 'numpy.version': <module 'numpy.version' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\version.pyc'>,
'numpy.lib.type_check': <module 'numpy.lib.type_check' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\type_check.pyc'>,
'unittest.re': None, 'threading': <module 'threading' from 'C:\Python27\ArcGIS10.6\lib\threading.pyc'>,
'pyexpat.model': <module 'pyexpat.model' (built-in)>,
'arcpy.collections': None, 'locale': <module 'locale' from 'C:\Python27\ArcGIS10.6\lib\locale.pyc'>,
'numpy.random.numpy': None, 'atexit': <module 'atexit' from 'C:\Python27\ArcGIS10.6\lib\atexit.pyc'>,
'defense': <module 'defense' from 'C:\Program Files (x86)\ArcGIS\EsriDefenseMapping\Desktop10.6\ArcToolbox\Toolboxes\defense.pyc'>,
'numpy.testing.decorators': <module 'numpy.testing.decorators' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\testing\decorators.pyc'>,
'Tamapgotchi_addin': <module 'Tamapgotchi_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{F4DAD37C-40A9-41D9-BAC6-E04A0AEEBB26}\Tamapgotchi_addin.py'>,
'ctypes.subprocess': None, 'unittest.case': <module 'unittest.case' from 'C:\Python27\ArcGIS10.6\lib\unittest\case.pyc'>,
'numpy.lib.info': <module 'numpy.lib.info' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\info.pyc'>,
'arcpy.warnings': None, 'xml.dom.domreg': <module 'xml.dom.domreg' from 'C:\Python27\ArcGIS10.6\lib\xml\dom\domreg.py'>,
'PyEditorDev_addin': <module 'PyEditorDev_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{B141CFD7-CBD7-4415-BA4B-5FF3D536A70B}\PyEditorDev_addin.py'>,
'unittest.signal': None, 'itertools': <module 'itertools' (built-in)>,
'numpy.fft.fftpack': <module 'numpy.fft.fftpack' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\fft\fftpack.pyc'>,
'opcode': <module 'opcode' from 'C:\Python27\ArcGIS10.6\lib\opcode.pyc'>,
'ctypes': <module 'ctypes' from 'C:\Python27\ArcGIS10.6\lib\ctypes\__init__.pyc'>,
'arcpy.mapping': <module 'arcpy.mapping' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\mapping.pyc'>,
'arcpy.arcobjects.operator': None, 'arcpy.analysis': <module 'arcpy.analysis' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\analysis.pyc'>,
'arcpy.geoprocessing.arcgisscripting': None, 'TeLEOS-1': <module 'TeLEOS-1' from 'c:\program files (x86)\arcgis\desktop10.6\Resources\Raster\Types\System\TeLEOS-1\TeLEOS-1.pyc'>,
'xml.parsers': <module 'xml.parsers' from 'C:\Python27\ArcGIS10.6\lib\xml\parsers\__init__.pyc'>,
'arcpy.geocoding': <module 'arcpy.geocoding' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\geocoding.pyc'>,
'unittest.collections': None, 'numpy.polynomial.laguerre': <module 'numpy.polynomial.laguerre' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\laguerre.pyc'>,
'sre_constants': <module 'sre_constants' from 'C:\Python27\ArcGIS10.6\lib\sre_constants.pyc'>,
'numpy.core._methods': <module 'numpy.core._methods' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\_methods.pyc'>,
'numpy.core.function_base': <module 'numpy.core.function_base' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\function_base.pyc'>,
'numpy.compat.py3k': <module 'numpy.compat.py3k' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\compat\py3k.pyc'>,
'arcpy.geoprocessing': <module 'arcpy.geoprocessing' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\geoprocessing\__init__.pyc'>,
'numpy': <module 'numpy' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\__init__.pyc'>,
'xml.dom.NodeFilter': <module 'xml.dom.NodeFilter' from 'C:\Python27\ArcGIS10.6\lib\xml\dom\NodeFilter.py'>,
'arcpy.md': <module 'arcpy.md' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\md.pyc'>,
'numpy.ma': <module 'numpy.ma' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\ma\__init__.pyc'>,
'arcpy.server': <module 'arcpy.server' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\server.pyc'>,
'logging.atexit': None, 'aviation': <module 'aviation' from 'C:\Program Files (x86)\ArcGIS\AviationCharting\Desktop10.6\ArcToolbox\Toolboxes\aviation.pyc'>,
'xml.etree.re': None, 'zlib': <module 'zlib' (built-in)>,
'arcpy.toolbox': <module 'arcpy.toolbox' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\toolbox.pyc'>,
'copy_reg': <module 'copy_reg' from 'C:\Python27\ArcGIS10.6\lib\copy_reg.pyc'>,
'site': <module 'site' from 'C:\Python27\ArcGIS10.6\lib\site.pyc'>,
'io': <module 'io' from 'C:\Python27\ArcGIS10.6\lib\io.pyc'>,
'pyexpat': <module 'pyexpat' from 'C:\Python27\ArcGIS10.6\DLLs\pyexpat.pyd'>,
'shutil': <module 'shutil' from 'C:\Python27\ArcGIS10.6\lib\shutil.pyc'>,
'encodings.utf_32_be': <module 'encodings.utf_32_be' from 'C:\Python27\ArcGIS10.6\lib\encodings\utf_32_be.pyc'>,
'UAF_python_scripting_addin': <module 'UAF_python_scripting_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{4161AB61-45E5-4F2B-A8FA-53D467B4AC94}\UAF_python_scripting_addin.py'>,
'unittest.time': None, 'numpy.polynomial.polyutils': <module 'numpy.polynomial.polyutils' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\polyutils.pyc'>,
'sys': <module 'sys' (built-in)>,
'numpy.compat._inspect': <module 'numpy.compat._inspect' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\compat\_inspect.pyc'>,
'arcpy.ta': <module 'arcpy.ta' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\ta.pyc'>,
'xml.dom.xml': None, 'arcpy.sa.Utils': <module 'arcpy.sa.Utils' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\sa\Utils.pyc'>,
'difflib': <module 'difflib' from 'C:\Python27\ArcGIS10.6\lib\difflib.pyc'>,
'unittest.warnings': None, 'heapq': <module 'heapq' from 'C:\Python27\ArcGIS10.6\lib\heapq.pyc'>,
'reviewer': <module 'reviewer' from 'C:\Program Files (x86)\ArcGIS\ArcGISDataReviewer\Desktop10.6\ArcToolbox\Toolboxes\reviewer.pyc'>,
'msvcrt': <module 'msvcrt' (built-in)>,
'arcpy.arcobjects.weakref': None, 'struct': <module 'struct' from 'C:\Python27\ArcGIS10.6\lib\struct.pyc'>,
'numpy.random.info': <module 'numpy.random.info' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\random\info.pyc'>,
'arcpy.arcobjects.arcobjects': <module 'arcpy.arcobjects.arcobjects' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\arcobjects\arcobjects.pyc'>,
'numpy.testing': <module 'numpy.testing' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\testing\__init__.pyc'>,
'collections': <module 'collections' from 'C:\Python27\ArcGIS10.6\lib\collections.pyc'>,
'unittest.main': <module 'unittest.main' from 'C:\Python27\ArcGIS10.6\lib\unittest\main.pyc'>,
'unittest': <module 'unittest' from 'C:\Python27\ArcGIS10.6\lib\unittest\__init__.pyc'>,
'arcpy.arcpy': None, 'zipimport': <module 'zipimport' (built-in)>,
'textwrap': <module 'textwrap' from 'C:\Python27\ArcGIS10.6\lib\textwrap.pyc'>,
'arcpy.arcobjects.itertools': None, 'signal': <module 'signal' (built-in)>,
'numpy.random.operator': None, 'numpy.core.multiarray': <module 'numpy.core.multiarray' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\multiarray.pyd'>,
'arcpy.gapy': None, 'numpy.ma.core': <module 'numpy.ma.core' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\ma\core.pyc'>,
'numpy.core.getlimits': <module 'numpy.core.getlimits' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\getlimits.pyc'>,
'xml.parsers.expat': <module 'xml.parsers.expat' from 'C:\Python27\ArcGIS10.6\lib\xml\parsers\expat.pyc'>,
'arcpy.geoprocessing.functools': None, 'logging.traceback': None, 'numpy.matrixlib': <module 'numpy.matrixlib' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\matrixlib\__init__.pyc'>,
'arcpy.arc': <module 'arcpy.arc' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\arc.pyc'>,
'mpl_toolkits': <module 'mpl_toolkits' (built-in)>,
'arcpy.geoprocessing.weakref': None, 'UserDict': <module 'UserDict' from 'C:\Python27\ArcGIS10.6\lib\UserDict.pyc'>,
'inspect': <module 'inspect' from 'C:\Python27\ArcGIS10.6\lib\inspect.pyc'>,
'BingGoogleMaps_addin': <module 'BingGoogleMaps_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{2F40D012-FFA9-4363-AF84-0ED1BD71D261}\BingGoogleMaps_addin.py'>,
'unittest.runner': <module 'unittest.runner' from 'C:\Python27\ArcGIS10.6\lib\unittest\runner.pyc'>,
'arcpy.arcobjects.re': None, 'unittest.loader': <module 'unittest.loader' from 'C:\Python27\ArcGIS10.6\lib\unittest\loader.pyc'>,
'_functools': <module '_functools' (built-in)>,
'arcpy.conversion': <module 'arcpy.conversion' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\conversion.pyc'>,
'numpy.core.memmap': <module 'numpy.core.memmap' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\memmap.pyc'>,
'arcgis': <module 'arcgis' (built-in)>,
'arcpy.arcobjects._base': <module 'arcpy.arcobjects._base' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\arcobjects\_base.pyc'>,
'numpy.linalg.lapack_lite': <module 'numpy.linalg.lapack_lite' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\linalg\lapack_lite.pyd'>,
'os': <module 'os' from 'C:\Python27\ArcGIS10.6\lib\os.pyc'>,
'arcpy.cmanagers.arcpy': None, '__future__': <module '__future__' from 'C:\Python27\ArcGIS10.6\lib\__future__.pyc'>,
'numpy.core.shape_base': <module 'numpy.core.shape_base' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\shape_base.pyc'>,
'__builtin__': <module '__builtin__' (built-in)>,
'arcpy.lr': <module 'arcpy.lr' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\lr.pyc'>,
'operator': <module 'operator' (built-in)>,
'errno': <module 'errno' (built-in)>,
'arcpy.operator': None, '_warnings': <module '_warnings' (built-in)>,
'arcpy.sa.arcpy': None, 'encodings.__builtin__': None, 'unittest.fnmatch': None, 'arcpy.arcobjects.os': None, 'arcpy.arcobjects.types': None, '_struct': <module '_struct' (built-in)>,
'arcpy': <module 'arcpy' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\__init__.pyc'>,
'numpy.fft': <module 'numpy.fft' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\fft\__init__.pyc'>,
'xml.dom.minidom': <module 'xml.dom.minidom' from 'C:\Python27\ArcGIS10.6\lib\xml\dom\minidom.py'>,
'arcpy.arcobjects': <module 'arcpy.arcobjects' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\arcobjects\__init__.pyc'>,
'logging.time': None, 'arcpy.cmanagers.EnvManager': <module 'arcpy.cmanagers.EnvManager' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\cmanagers\EnvManager.pyc'>,
'numpy.lib.function_base': <module 'numpy.lib.function_base' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\function_base.pyc'>,
'logging.warnings': None, 'logging.codecs': None, '_random': <module '_random' (built-in)>,
'numpy.polynomial._polybase': <module 'numpy.polynomial._polybase' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\_polybase.pyc'>,
'arcpy.fabric': <module 'arcpy.fabric' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\fabric.pyc'>,
'numpy.polynomial.hermite': <module 'numpy.polynomial.hermite' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\hermite.pyc'>,
'contextlib': <module 'contextlib' from 'C:\Python27\ArcGIS10.6\lib\contextlib.pyc'>,
'nautical': <module 'nautical' from 'C:\Program Files (x86)\ArcGIS\MaritimeCharting\Desktop10.6\ArcToolbox\Toolboxes\nautical.pyc'>,
'numpy.polynomial.polynomial': <module 'numpy.polynomial.polynomial' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\polynomial\polynomial.pyc'>,
'numpy.core._dotblas': <module 'numpy.core._dotblas' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\_dotblas.pyd'>,
'arcpy.sa': <module 'arcpy.sa' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\sa\__init__.pyc'>,
'numpy.core.defchararray': <module 'numpy.core.defchararray' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\core\defchararray.pyc'>,
'arcpy._na': <module 'arcpy._na' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\_na.pyc'>,
'_abcoll': <module '_abcoll' from 'C:\Python27\ArcGIS10.6\lib\_abcoll.pyc'>,
'arcpy.arcobjects.geometries': <module 'arcpy.arcobjects.geometries' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\arcobjects\geometries.pyc'>,
'nt': <module 'nt' (built-in)>,
'genericpath': <module 'genericpath' from 'C:\Python27\ArcGIS10.6\lib\genericpath.pyc'>,
'stat': <module 'stat' from 'C:\Python27\ArcGIS10.6\lib\stat.pyc'>,
'UpdateDataSourcePlugin_addin': <module 'UpdateDataSourcePlugin_addin' from 'C:\Users\njcagle\AppData\Local\ESRI\Desktop10.6\AssemblyCache\{71BE15AB-DEF4-4B8E-BDC8-C0F1270E4061}\UpdateDataSourcePlugin_addin.py'>,
'unittest.signals': <module 'unittest.signals' from 'C:\Python27\ArcGIS10.6\lib\unittest\signals.pyc'>,
'ctypes.ctypes': None, 'numpy.lib.format': <module 'numpy.lib.format' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\lib\format.pyc'>,
'numpy.testing.nosetester': <module 'numpy.testing.nosetester' from 'C:\Python27\ArcGIS10.6\lib\site-packages\numpy\testing\nosetester.pyc'>,
'xml.dom': <module 'xml.dom' from 'C:\Python27\ArcGIS10.6\lib\xml\dom\__init__.py'>,
'arcpy.inspect': None, 'arcpy.interop': <module 'arcpy.interop' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\interop.pyc'>,
'time': <module 'time' (built-in)>,
'arcpy.stats': <module 'arcpy.stats' from 'c:\program files (x86)\arcgis\desktop10.6\arcpy\arcpy\stats.pyc'>}"""



"""
write('\n__call__:')
write(arcpy.arcmods.arcmagic.__call__)
write('\n__class__:')
write(arcpy.arcmods.arcmagic.__class__)
write('\n__closure__:')
write(arcpy.arcmods.arcmagic.__closure__)
write('\n__code__:')
write(arcpy.arcmods.arcmagic.__code__)
write('\n__defaults__:')
write(arcpy.arcmods.arcmagic.__defaults__)
write('\n__delattr__:')
write(arcpy.arcmods.arcmagic.__delattr__)
write('\n__dict__:')
write(arcpy.arcmods.arcmagic.__dict__)
write('\n__doc__:')
write(arcpy.arcmods.arcmagic.__doc__)
write('\n__esri_toolname__:')
write(arcpy.arcmods.arcmagic.__esri_toolname__)
write('\n__format__:')
write(arcpy.arcmods.arcmagic.__format__)
write('\n__get__:')
write(arcpy.arcmods.arcmagic.__get__)
write('\n__getattribute__:')
write(arcpy.arcmods.arcmagic.__getattribute__)
write('\n__globals__:')
write(arcpy.arcmods.arcmagic.__globals__)
write('\n__hash__:')
write(arcpy.arcmods.arcmagic.__hash__)
write('\n__init__:')
write(arcpy.arcmods.arcmagic.__init__)
write('\n__module__:')
write(arcpy.arcmods.arcmagic.__module__)
write('\n__name__:')
write(arcpy.arcmods.arcmagic.__name__)
write('\n__new__:')
write(arcpy.arcmods.arcmagic.__new__)
write('\n__reduce__:')
write(arcpy.arcmods.arcmagic.__reduce__)
write('\n__reduce_ex__:')
write(arcpy.arcmods.arcmagic.__reduce_ex__)
write('\n__repr__:')
write(arcpy.arcmods.arcmagic.__repr__)
write('\n__setattr__:')
write(arcpy.arcmods.arcmagic.__setattr__)
write('\n__sizeof__:')
write(arcpy.arcmods.arcmagic.__sizeof__)
write('\n__str__:')
write(arcpy.arcmods.arcmagic.__str__)
write('\n__subclasshook__:')
write(arcpy.arcmods.arcmagic.__subclasshook__)
write('\nfunc_closure:')
write(arcpy.arcmods.arcmagic.func_closure)
write('\nfunc_code:')
write(arcpy.arcmods.arcmagic.func_code)
write('\nfunc_defaults:')
write(arcpy.arcmods.arcmagic.func_defaults)
write('\nfunc_dict:')
write(arcpy.arcmods.arcmagic.func_dict)
write('\nfunc_doc:')
write(arcpy.arcmods.arcmagic.func_doc)
write('\nfunc_globals:')
write(arcpy.arcmods.arcmagic.func_globals)
write('\nfunc_name:')
write(arcpy.arcmods.arcmagic.func_name)
write("\n")
write("\n")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

['__call__',
'__class__',
'__closure__',
'__code__',
'__defaults__',
'__delattr__',
'__dict__',
'__doc__',
'__esri_toolname__',
'__format__',
'__get__',
'__getattribute__',
'__globals__',
'__hash__',
'__init__',
'__module__',
'__name__',
'__new__',
'__reduce__',
'__reduce_ex__',
'__repr__',
'__setattr__',
'__sizeof__',
'__str__',
'__subclasshook__',
'func_closure',
'func_code',
'func_defaults',
'func_dict',
'func_doc',
'func_globals',
'func_name']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__call__:
	<method-wrapper '__call__' of function object at 0x15D09F70>

__class__:
	<type 'function'>

__closure__:

__code__:
	<code object arcmagic at 26E51800, file "C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\ArcPy Modules.tbx", line 21>

__defaults__:

__delattr__:
	<method-wrapper '__delattr__' of function object at 0x15D09F70>

__dict__:
	{'__esri_toolname__': 'arcmagic_arcmods'}

__doc__:
	arcmagic_arcmods()

__esri_toolname__:
	arcmagic_arcmods

__format__:
	<built-in method __format__ of function object at 0x15D09F70>

__get__:
	<method-wrapper '__get__' of function object at 0x15D09F70>

__getattribute__:
	<method-wrapper '__getattribute__' of function object at 0x15D09F70>

__globals__:
	{'fintools':          None,
	'arcapi':             None,
	'__all__':            None,
	'__builtins__':       {'bytearray':                  <type 'bytearray'>,
							'IndexError':                <type 'exceptions.IndexError'>,
							'all':                       <built-in function all>,
							'help':                      Type help() for interactive help, or help(object) for help about object.,
							'vars':                      <built-in function vars>,
							'SyntaxError':               <type 'exceptions.SyntaxError'>,
							'unicode':                   <type 'unicode'>,
							'UnicodeDecodeError':        <type 'exceptions.UnicodeDecodeError'>,
							'memoryview':                <type 'memoryview'>,
							'isinstance':                <built-in function isinstance>,
							'copyright':                 Copyright (c) 2001-2017 Python Software Foundation. All Rights Reserved.
															 Copyright (c) 2000 BeOpen.com. All Rights Reserved.
															 Copyright (c) 1995-2001 Corporation for National Research Initiatives. All Rights Reserved.
															 Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam. All Rights Reserved.,
							'NameError':                 <type 'exceptions.NameError'>,
							'BytesWarning':              <type 'exceptions.BytesWarning'>,
							'dict':                      <type 'dict'>,
							'input':                     <built-in function input>,
							'oct':                       <built-in function oct>,
							'bin':                       <built-in function bin>,
							'SystemExit':                <type 'exceptions.SystemExit'>,
							'StandardError':             <type 'exceptions.StandardError'>,
							'format':                    <built-in function format>,
							'repr':                      <built-in function repr>,
							'sorted':                    <built-in function sorted>,
							'False':                     False,
							'RuntimeWarning':            <type 'exceptions.RuntimeWarning'>,
							'list':                      <type 'list'>,
							'iter':                      <built-in function iter>,
							'reload':                    <built-in function reload>,
							'Warning':                   <type 'exceptions.Warning'>,
							'__package__':               None,
							'round':                     <built-in function round>,
							'dir':                       <built-in function dir>,
							'cmp':                       <built-in function cmp>,
							'set':                       <type 'set'>,
							'bytes':                     <type 'str'>,
							'reduce':                    <built-in function reduce>,
							'intern':                    <built-in function intern>,
							'issubclass':                <built-in function issubclass>,
							'Ellipsis':                  Ellipsis,
							'EOFError':                  <type 'exceptions.EOFError'>,
							'locals':                    <built-in function locals>,
							'BufferError':               <type 'exceptions.BufferError'>,
							'slice':                     <type 'slice'>,
							'FloatingPointError':        <type 'exceptions.FloatingPointError'>,
							'sum':                       <built-in function sum>,
							'getattr':                   <built-in function getattr>,
							'abs':                       <built-in function abs>,
							'exit':                      Use exit() or Ctrl-Z plus Return to exit,
							'print':                     <built-in function print>,
							'True':                      True,
							'FutureWarning':             <type 'exceptions.FutureWarning'>,
							'ImportWarning':             <type 'exceptions.ImportWarning'>,
							'None':                      None,
							'hash':                      <built-in function hash>,
							'ReferenceError':            <type 'exceptions.ReferenceError'>,
							'len':                       <built-in function len>,
							'credits':                   Thanks to CWI,
															 CNRI,
															 BeOpen.com,
															 Zope Corporation and a cast of thousands
															 for supporting Python development.  See www.python.org for more information.,
							'frozenset':                 <type 'frozenset'>,
							'__name__':                  '__builtin__',
							'ord':                       <built-in function ord>,
							'super':                     <type 'super'>,
							'TypeError':                 <type 'exceptions.TypeError'>,
							'license':                   Type license() to see the full license text,
							'KeyboardInterrupt':         <type 'exceptions.KeyboardInterrupt'>,
							'UserWarning':               <type 'exceptions.UserWarning'>,
							'filter':                    <built-in function filter>,
							'range':                     <built-in function range>,
							'staticmethod':              <type 'staticmethod'>,
							'SystemError':               <type 'exceptions.SystemError'>,
							'BaseException':             <type 'exceptions.BaseException'>,
							'pow':                       <built-in function pow>,
							'RuntimeError':              <type 'exceptions.RuntimeError'>,
							'float':                     <type 'float'>,
							'MemoryError':               <type 'exceptions.MemoryError'>,
							'StopIteration':             <type 'exceptions.StopIteration'>,
							'globals':                   <built-in function globals>,
							'divmod':                    <built-in function divmod>,
							'enumerate':                 <type 'enumerate'>,
							'apply':                     <built-in function apply>,
							'LookupError':               <type 'exceptions.LookupError'>,
							'open':                      <built-in function open>,
							'quit':                      Use quit() or Ctrl-Z plus Return to exit,
							'basestring':                <type 'basestring'>,
							'UnicodeError':              <type 'exceptions.UnicodeError'>,
							'zip':                       <built-in function zip>,
							'hex':                       <built-in function hex>,
							'long':                      <type 'long'>,
							'next':                      <built-in function next>,
							'ImportError':               <type 'exceptions.ImportError'>,
							'chr':                       <built-in function chr>,
							'xrange':                    <type 'xrange'>,
							'type':                      <type 'type'>,
							'__doc__':                   "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices.",
							'Exception':                 <type 'exceptions.Exception'>,
							'tuple':                     <type 'tuple'>,
							'UnicodeTranslateError':     <type 'exceptions.UnicodeTranslateError'>,
							'reversed':                  <type 'reversed'>,
							'UnicodeEncodeError':        <type 'exceptions.UnicodeEncodeError'>,
							'IOError':                   <type 'exceptions.IOError'>,
							'hasattr':                   <built-in function hasattr>,
							'delattr':                   <built-in function delattr>,
							'setattr':                   <built-in function setattr>,
							'raw_input':                 <built-in function raw_input>,
							'SyntaxWarning':             <type 'exceptions.SyntaxWarning'>,
							'compile':                   <built-in function compile>,
							'ArithmeticError':           <type 'exceptions.ArithmeticError'>,
							'str':                       <type 'str'>,
							'property':                  <type 'property'>,
							'GeneratorExit':             <type 'exceptions.GeneratorExit'>,
							'int':                       <type 'int'>,
							'__import__':                <built-in function __import__>,
							'KeyError':                  <type 'exceptions.KeyError'>,
							'coerce':                    <built-in function coerce>,
							'PendingDeprecationWarning': <type 'exceptions.PendingDeprecationWarning'>,
							'file':                      <type 'file'>,
							'EnvironmentError':          <type 'exceptions.EnvironmentError'>,
							'unichr':                    <built-in function unichr>,
							'id':                        <built-in function id>,
							'OSError':                   <type 'exceptions.OSError'>,
							'DeprecationWarning':        <type 'exceptions.DeprecationWarning'>,
							'min':                       <built-in function min>,
							'UnicodeWarning':            <type 'exceptions.UnicodeWarning'>,
							'execfile':                  <built-in function execfile>,
							'any':                       <built-in function any>,
							'complex':                   <type 'complex'>,
							'bool':                      <type 'bool'>,
							'ValueError':                <type 'exceptions.ValueError'>,
							'NotImplemented':            NotImplemented,
							'map':                       <built-in function map>,
							'buffer':                    <type 'buffer'>,
							'max':                       <built-in function max>,
							'object':                    <type 'object'>,
							'TabError':                  <type 'exceptions.TabError'>,
							'callable':                  <built-in function callable>,
							'ZeroDivisionError':         <type 'exceptions.ZeroDivisionError'>,
							'eval':                      <built-in function eval>,
							'__debug__':                 True,
							'IndentationError':          <type 'exceptions.IndentationError'>,
							'AssertionError':            <type 'exceptions.AssertionError'>,
							'classmethod':               <type 'classmethod'>,
							'UnboundLocalError':         <type 'exceptions.UnboundLocalError'>,
							'NotImplementedError':       <type 'exceptions.NotImplementedError'>,
							'AttributeError':            <type 'exceptions.AttributeError'>,
							'OverflowError':             <type 'exceptions.OverflowError'>,
							'WindowsError':              <type 'exceptions.WindowsError'>},
	'__package__':        None,
	'__pathname__':       None,
	'__alias__':          None,
	'arcmagic':           None,
	'__name__':           None,
	'__doc__':            None}

__hash__:
	<method-wrapper '__hash__' of function object at 0x15D09F70>

__init__:
	<method-wrapper '__init__' of function object at 0x15D09F70>

__module__:
	arcmods

__name__:
	arcmagic

__new__:
	<built-in method __new__ of type object at 0x54F90F70>

__reduce__:
	<built-in method __reduce__ of function object at 0x15D09F70>

__reduce_ex__:
	<built-in method __reduce_ex__ of function object at 0x15D09F70>

__repr__:
	<method-wrapper '__repr__' of function object at 0x15D09F70>

__setattr__:
	<method-wrapper '__setattr__' of function object at 0x15D09F70>

__sizeof__:
	<built-in method __sizeof__ of function object at 0x15D09F70>

__str__:
	<method-wrapper '__str__' of function object at 0x15D09F70>

__subclasshook__:
	<built-in method __subclasshook__ of type object at 0x54F90F70>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

func_closure:

func_code:
	<code object arcmagic at 26E51800,
	file "C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\ArcPy Modules.tbx",
	line 21>

func_defaults:

func_dict:
	{'__esri_toolname__': 'arcmagic_arcmods'}

func_doc:
	arcmagic_arcmods()

func_globals:
	{'fintools': None,
	'arcapi': None,
	'__all__': None,
	'__builtins__': {'bytearray': <type 'bytearray'>,
	'IndexError': <type 'exceptions.IndexError'>,
	'all': <built-in function all>,
	'help': Type help() for interactive help,
	or help(object) for help about object.,
	'vars': <built-in function vars>,
	'SyntaxError': <type 'exceptions.SyntaxError'>,
	'unicode': <type 'unicode'>,
	'UnicodeDecodeError': <type 'exceptions.UnicodeDecodeError'>,
	'memoryview': <type 'memoryview'>,
	'isinstance': <built-in function isinstance>,
	'copyright': Copyright (c) 2001-2017 Python Software Foundation. All Rights Reserved.
		Copyright (c) 2000 BeOpen.com. All Rights Reserved.
		Copyright (c) 1995-2001 Corporation for National Research Initiatives. All Rights Reserved.
		Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam. All Rights Reserved.,
	'NameError': <type 'exceptions.NameError'>,
	'BytesWarning': <type 'exceptions.BytesWarning'>,
	'dict': <type 'dict'>,
	'input': <built-in function input>,
	'oct': <built-in function oct>,
	'bin': <built-in function bin>,
	'SystemExit': <type 'exceptions.SystemExit'>,
	'StandardError': <type 'exceptions.StandardError'>,
	'format': <built-in function format>,
	'repr': <built-in function repr>,
	'sorted': <built-in function sorted>,
	'False': False,
	'RuntimeWarning': <type 'exceptions.RuntimeWarning'>,
	'list': <type 'list'>,
	'iter': <built-in function iter>,
	'reload': <built-in function reload>,
	'Warning': <type 'exceptions.Warning'>,
	'__package__': None,
	'round': <built-in function round>,
	'dir': <built-in function dir>,
	'cmp': <built-in function cmp>,
	'set': <type 'set'>,
	'bytes': <type 'str'>,
	'reduce': <built-in function reduce>,
	'intern': <built-in function intern>,
	'issubclass': <built-in function issubclass>,
	'Ellipsis': Ellipsis,
	'EOFError': <type 'exceptions.EOFError'>,
	'locals': <built-in function locals>,
	'BufferError': <type 'exceptions.BufferError'>,
	'slice': <type 'slice'>,
	'FloatingPointError': <type 'exceptions.FloatingPointError'>,
	'sum': <built-in function sum>,
	'getattr': <built-in function getattr>,
	'abs': <built-in function abs>,
	'exit': Use exit() or Ctrl-Z plus Return to exit,
	'print': <built-in function print>,
	'True': True,
	'FutureWarning': <type 'exceptions.FutureWarning'>,
	'ImportWarning': <type 'exceptions.ImportWarning'>,
	'None': None,
	'hash': <built-in function hash>,
	'ReferenceError': <type 'exceptions.ReferenceError'>,
	'len': <built-in function len>,
	'credits':     Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands for supporting Python development.  See www.python.org for more information.,
	'frozenset': <type 'frozenset'>,
	'__name__': '__builtin__',
	'ord': <built-in function ord>,
	'super': <type 'super'>,
	'TypeError': <type 'exceptions.TypeError'>,
	'license': Type license() to see the full license text,
	'KeyboardInterrupt': <type 'exceptions.KeyboardInterrupt'>,
	'UserWarning': <type 'exceptions.UserWarning'>,
	'filter': <built-in function filter>,
	'range': <built-in function range>,
	'staticmethod': <type 'staticmethod'>,
	'SystemError': <type 'exceptions.SystemError'>,
	'BaseException': <type 'exceptions.BaseException'>,
	'pow': <built-in function pow>,
	'RuntimeError': <type 'exceptions.RuntimeError'>,
	'float': <type 'float'>,
	'MemoryError': <type 'exceptions.MemoryError'>,
	'StopIteration': <type 'exceptions.StopIteration'>,
	'globals': <built-in function globals>,
	'divmod': <built-in function divmod>,
	'enumerate': <type 'enumerate'>,
	'apply': <built-in function apply>,
	'LookupError': <type 'exceptions.LookupError'>,
	'open': <built-in function open>,
	'quit': Use quit() or Ctrl-Z plus Return to exit,
	'basestring': <type 'basestring'>,
	'UnicodeError': <type 'exceptions.UnicodeError'>,
	'zip': <built-in function zip>,
	'hex': <built-in function hex>,
	'long': <type 'long'>,
	'next': <built-in function next>,
	'ImportError': <type 'exceptions.ImportError'>,
	'chr': <built-in function chr>,
	'xrange': <type 'xrange'>,
	'type': <type 'type'>,
	'__doc__': "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices.",
	'Exception': <type 'exceptions.Exception'>,
	'tuple': <type 'tuple'>,
	'UnicodeTranslateError': <type 'exceptions.UnicodeTranslateError'>,
	'reversed': <type 'reversed'>,
	'UnicodeEncodeError': <type 'exceptions.UnicodeEncodeError'>,
	'IOError': <type 'exceptions.IOError'>,
	'hasattr': <built-in function hasattr>,
	'delattr': <built-in function delattr>,
	'setattr': <built-in function setattr>,
	'raw_input': <built-in function raw_input>,
	'SyntaxWarning': <type 'exceptions.SyntaxWarning'>,
	'compile': <built-in function compile>,
	'ArithmeticError': <type 'exceptions.ArithmeticError'>,
	'str': <type 'str'>,
	'property': <type 'property'>,
	'GeneratorExit': <type 'exceptions.GeneratorExit'>,
	'int': <type 'int'>,
	'__import__': <built-in function __import__>,
	'KeyError': <type 'exceptions.KeyError'>,
	'coerce': <built-in function coerce>,
	'PendingDeprecationWarning': <type 'exceptions.PendingDeprecationWarning'>,
	'file': <type 'file'>,
	'EnvironmentError': <type 'exceptions.EnvironmentError'>,
	'unichr': <built-in function unichr>,
	'id': <built-in function id>,
	'OSError': <type 'exceptions.OSError'>,
	'DeprecationWarning': <type 'exceptions.DeprecationWarning'>,
	'min': <built-in function min>,
	'UnicodeWarning': <type 'exceptions.UnicodeWarning'>,
	'execfile': <built-in function execfile>,
	'any': <built-in function any>,
	'complex': <type 'complex'>,
	'bool': <type 'bool'>,
	'ValueError': <type 'exceptions.ValueError'>,
	'NotImplemented': NotImplemented,
	'map': <built-in function map>,
	'buffer': <type 'buffer'>,
	'max': <built-in function max>,
	'object': <type 'object'>,
	'TabError': <type 'exceptions.TabError'>,
	'callable': <built-in function callable>,
	'ZeroDivisionError': <type 'exceptions.ZeroDivisionError'>,
	'eval': <built-in function eval>,
	'__debug__': True,
	'IndentationError': <type 'exceptions.IndentationError'>,
	'AssertionError': <type 'exceptions.AssertionError'>,
	'classmethod': <type 'classmethod'>,
	'UnboundLocalError': <type 'exceptions.UnboundLocalError'>,
	'NotImplementedError': <type 'exceptions.NotImplementedError'>,
	'AttributeError': <type 'exceptions.AttributeError'>,
	'OverflowError': <type 'exceptions.OverflowError'>,
	'WindowsError': <type 'exceptions.WindowsError'>},
	'__package__': None,
	'__pathname__': None,
	'__alias__': None,
	'arcmagic': None,
	'__name__': None,
	'__doc__': None}

func_name:
	arcmagic
"""
