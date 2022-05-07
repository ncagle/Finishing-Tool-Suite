import arcpy as ap
from arcpy import AddMessage as write


# arcpath = r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules" #\ArcPy_Module_Wrapper.pyt"
# import sys
# sys.path.insert(0, arcpath)
# import ArcPy_Module_Wrapper

ap.ImportToolbox(r"C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\pyt_conversion\modules\ArcPy_Module_Wrapper.pyt")


# def arcmag():
# 	fc = ap.GetParameter(0)
#
# 	class FeatureClass(object):
# 		"""FeatureClass object"""
#
# 		#----------------------------------------------------------------------
# 		def __init__(self,path):
# 			"""Constructor for FeatureClass"""
# 			gdb_attributes_dict = {'fc_path': ap.Describe(path).catalogPath,
# 								   'fc_name': ap.Describe(path).file.split(".")[-1],
# 								   'shape_type': ap.Describe(path).shapeType, # Polygon, Polyline, Point, Multipoint, MultiPatch
# 								   'shape_field': ap.Describe(path).shapeFieldName,
# 								   'length_field': ap.Describe(path).lengthFieldName,
# 								   'area_field': ap.Describe(path).areaFieldName,
# 								   'oid_field': ap.Describe(path).OIDFieldName,
# 								   'has_spatial_index': ap.Describe(path).hasSpatialIndex
# 								   }
#
# 			out_fields = [self.oid_field, self.length_field, self.area_field, self.shape_field] # List Geometry and OID fields to be removed
# 			# Construct sanitized list of field names
# 			field_list = [field.name for field in ap.ListFields(path) if field.type not in ['Geometry'] and field.name not in out_fields]
# 			# Add OID@ token to index[-2] and Shape@ geometry token to index[-1]
# 			field_list.append('OID@')
# 			field_list.append('SHAPE@')
#
# 			for k,v in gdb_attributes_dict.iteritems():
# 				setattr(self, k, v)
#
# 			setattr(self,'TDS',os.path.dirname(self.fc_path))
# 			setattr(self,'fields',field_list)
# 			setattr(self,'fc_features',Features(self.fc_path,self.fields))
#
# 		#----------------------------------------------------------------------
# 		def __str__(self):
# 			return self.baseName
#
# 		@classmethod
# 		def write_info(name, var): # Write information for given variable
# 			#write_info('var_name', var)
# 			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 			write("Debug info for {0}:".format(name))
# 			write("   Variable Type: {0}".format(type(var)))
# 			if type(var) is str or type(var) is unicode:
# 				write("   Assigned Value: '{0}'".format(var))
# 			else:
# 				write("   Assigned Value: {0}".format(var))
# 			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



#def arcmagic(): # Script as function
def main():
	class Student(object): # Class definition in script
		name = 'Nat'
		color = 'Green'
		def __init__(self):
			self.age = 20  # instance attribute

		@classmethod
		def tostring(self): # var accessing class attributes
			print('Student Class Attributes: name =', self.name)

		@classmethod
		def a_b(self, a, b): # Class method to be called with arcmagic as pseudo-module
			c = a+b
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

	return Student()



if __name__ == '__main__':
	write(dir(ap.wrapper))
	write(dir(ap.wrapper.importmodules))

	# Call main function
	pseudo_module = main()
	write(type(pseudo_module)) #<instance> type in python2. Class needs to inherit from object
	write(pseudo_module)
	#write(main())

	# Set *output* for script, NOTICE the parameter index number of the parameter before the variable to return
	#arcpy.SetParameter(3, Student())
	arcpy.SetParameter(0, pseudo_module)

# if __name__ == '__main__':
# 	# Get *input* for script
# 	input_param = arcpy.GetParameterAsText(0) # Hopefully getting first parameter passed to arcmagic() function in pyt
#
# 	# Call main function
# 	pseudo_module = main(input_param)
# 	write(type(pseudo_module)) #<instance> type
# 	write(pseudo_module)
#
# 	# Set *output* for script, NOTICE the parameter index number of the parameter before the variable to return
# 	#arcpy.SetParameter(3, Student())
# 	arcpy.SetParameter(1, pseudo_module)
