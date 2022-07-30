# -*- coding: utf-8 -*-
#¸¸.·´¯`·.¸¸.·´¯`·.¸¸
#╔════════════════════════════╗#
#║ Calculate Metrics Refactor ║#
#║        Kristen Hall        ║#
#║   Last Edited 2022-06-24   ║#
#╚════════════════════════════╝#
import arcpy as ap
from arcpy import AddMessage as write

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

# Function that returns True if x (a field) is populated and False if x (a field) is NULL, empty, or default
# Ex:
# if populated('HGT'):
#     write("HGT field has a value")
# if not populated('HGT'):
#     write("HGT field is NULL, empty, or -999999")
populated = lambda x: x is not None and str(x).strip() != '' and x != -999999


#----------------------------------------------------------------------


''''''''' Variables '''''''''
# These are the variables you'll probably need
TDS = ap.GetParameterAsText(0) # r'C:\Projects\njcagle\R&D\__Thunderdome\S2_J12A_multiparts.gdb\TDS'
ap.env.workspace = TDS
featureclass = ap.ListFeatureClasses() # ['AeronauticCrv', 'AeronauticPnt', 'AeronauticSrf', 'AgriculturePnt', 'AgricultureSrf', 'BoundaryPnt', 'CultureCrv', 'CulturePnt', 'CultureSrf', 'FacilityPnt', 'FacilitySrf', 'HydroAidNavigationPnt', 'HydroAidNavigationSrf', 'HydrographyCrv', 'HydrographyPnt', 'HydrographySrf', 'IndustryCrv', 'IndustryPnt', 'IndustrySrf', 'InformationCrv', 'InformationPnt', 'InformationSrf', 'MilitaryCrv', 'MilitaryPnt', 'MilitarySrf', 'PhysiographyCrv', 'PhysiographyPnt', 'PhysiographySrf', 'PortHarbourCrv', 'PortHarbourPnt', 'PortHarbourSrf', 'RecreationCrv', 'RecreationPnt', 'RecreationSrf', 'SettlementPnt', 'SettlementSrf', 'StoragePnt', 'StorageSrf', 'StructureCrv', 'StructurePnt', 'StructureSrf', 'TransportationGroundCrv', 'TransportationGroundPnt', 'TransportationGroundSrf', 'TransportationWaterCrv', 'TransportationWaterPnt', 'TransportationWaterSrf', 'UtilityInfrastructureCrv', 'UtilityInfrastructurePnt', 'UtilityInfrastructureSrf', 'VegetationCrv', 'VegetationPnt', 'VegetationSrf', 'MetadataSrf', 'ResourceSrf']


#----------------------------------------------------------------------


''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
## Only run on Polygon ARA and Polyline LZN


for fc in featureclass: # loop thru each fc in the featureclass list
	if get_count(fc) == 0: # If the fc doesn't have any features, skip it and move to the next one
		continue
	shape_type = ap.Describe(fc).shapeType # Gets the geometry type of the current fc. 'Polygon', 'Polyline', 'Point'
	if shape_type == 'Polyline':
		write("Calculating Length field for {0}".format(fc))
		ap.CalculateMetrics_defense(fc, 'LENGTH', "LZN", "#", "#", "#", "#", "#")
	elif shape_type == 'Polygon':
		write("Calculating Area field for {0}".format(fc))
		ap.CalculateMetrics_defense(fc, 'AREA', "#", "#", "ARA", "#", "#", "#")






#----------------------------------------------------------------------


Giant UWU tool for kristen

|         | `.               .' |         |
|         |   `.           .'   |         |
|         |     `.   .   .'     |         |
`._______.'       `.' `.'       `._______.'

print("|         | `.               .' |         |\n|         |   `.           .'   |         |\n|         |     `.   .   .'     |         |\n`._______.'       `.' `.'       `._______.'")


 _   ___      ___   _
| | | \ \ /\ / / | | |
| |_| |\ V  V /| |_| |
 \__,_| \_/\_/  \__,_|

print(" _   ___      ___   _\n| | | \ \ /\ / / | | |\n| |_| |\ V  V /| |_| |\n \__,_| \_/\_/  \__,_|")


 __    __   ___       ___   __    __
 ) )  ( (  (  (       )  )  ) )  ( (
( (    ) )  \  \  _  /  /  ( (    ) )
 ) )  ( (    \  \/ \/  /    ) )  ( (
( (    ) )    )   _   (    ( (    ) )
 ) \__/ (     \  ( )  /     ) \__/ (
 \______/      \_/ \_/      \______/

print(" __    __   ___       ___   __    __\n ) )  ( (  (  (       )  )  ) )  ( (\n( (    ) )  \  \  _  /  /  ( (    ) )\n ) )  ( (    \  \/ \/  /    ) )  ( (\n( (    ) )    )   _   (    ( (    ) )\n ) \__/ (     \  ( )  /     ) \__/ (\n \______/      \_/ \_/      \______/")


 __    __  ____    __    ____  __    __
|  |  |  | \   \  /  \  /   / |  |  |  |
|  |  |  |  \   \/    \/   /  |  |  |  |
|  |  |  |   \            /   |  |  |  |
|  `--'  |    \    /\    /    |  `--'  |
 \______/      \__/  \__/      \______/

print(" __    __  ____    __    ____  __    __\n|  |  |  | \   \  /  \  /   / |  |  |  |\n|  |  |  |  \   \/    \/   /  |  |  |  |\n|  |  |  |   \            /   |  |  |  |\n|  `--'  |    \    /\    /    |  `--'  |\n \______/      \__/  \__/      \______/")
