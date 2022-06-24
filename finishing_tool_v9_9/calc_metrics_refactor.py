# -*- coding: utf-8 -*-
#¸¸.·´¯`·.¸¸.·´¯`·.¸¸
#╔════════════════════════════╗#
#║ Calculate Metrics Refactor ║#
#║        Kristen Hall        ║#
#║   Last Edited 2022-06-24   ║#
#╚════════════════════════════╝#
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




''''''''' Useful Functions '''''''''
# Give the function a feature class variable and it will return the number of features
# Ex: trans_count = get_count(trans_fc)
def get_count(fc_layer):
    results = int(ap.GetCount_management(fc_layer).getOutput(0))
    return results

# Use this to output information about a variable when you run the tool in ArcMap
# It's just a nicely formatted way to check information about a variable when debugging
# Ex:
# In this code is the variable TDS.
# If I wanted to check that it had the right value when the tool is running, I'd use this function.
# The first value is what you want the output to call the variable
# The second value is the variable itself
# write_info('TDS_on_line_69', TDS)
# This is what would show up when you run the tool:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Debug info for TDS_on_line_69:
#    Variable Type: <type 'str'>
#    Assigned Value: 'C:\Projects\finishing\G08B\G08B_Req2_5.gdb\TDS'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def write_info(name, var):
	#write_info('var_name', var)
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	write("Debug info for {0}:".format(name))
	write("   Variable Type: {0}".format(type(var)))
	if type(var) is str or type(var) is unicode:
		write("   Assigned Value: '{0}'".format(var))
	else:
		write("   Assigned Value: {0}".format(var))
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# Function that returns boolean of if input field is populated or empty or default
populated = lambda x: x is not None and str(x).strip() != '' and x != -999999


#----------------------------------------------------------------------


''''''''' Variables '''''''''

TDS = ap.GetParameterAsText(0)
ap.env.workspace = TDS
# If any of the tools that require the Defense Mapping license are selected, check out the Defense license
check_defense('out', defaults, metrics, explode)


#----------------------------------------------------------------------


''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
## Only run on Polygon ARA and Polyline LZN

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




#----------------------------------------------------------------------

Giant UWU tool for kristen


|         | `.               .' |         |
|         |   `.           .'   |         |
|         |     `.   .   .'     |         |
`._______.'       `.' `.'       `._______.'




 _   ___      ___   _
| | | \ \ /\ / / | | |
| |_| |\ V  V /| |_| |
 \__,_| \_/\_/  \__,_|


 __    __   ___       ___   __    __
 ) )  ( (  (  (       )  )  ) )  ( (
( (    ) )  \  \  _  /  /  ( (    ) )
 ) )  ( (    \  \/ \/  /    ) )  ( (
( (    ) )    )   _   (    ( (    ) )
 ) \__/ (     \  ( )  /     ) \__/ (
 \______/      \_/ \_/      \______/


 __    __  ____    __    ____  __    __
|  |  |  | \   \  /  \  /   / |  |  |  |
|  |  |  |  \   \/    \/   /  |  |  |  |
|  |  |  |   \            /   |  |  |  |
|  `--'  |    \    /\    /    |  `--'  |
 \______/      \__/  \__/      \______/
