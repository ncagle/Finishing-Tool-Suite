import arcpy
import os

#            ___________________________
#           | Calculates ARA, LZN, WID, |
#           | and AOO for required      |
#           | features.                 |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~

arcpy.env.workspace = arcpy.GetParameterAsText(0)
featureclass = arcpy.ListFeatureClasses()
metric_type = 'LENGTH;WIDTH;AREA;ANGLE_OF_ORIENTATION'

for fc in featureclass:
    arcpy.AddMessage("Calculating AOO, ARA, LZN, and WID for " + str(fc))
    arcpy.defense.CalculateMetrics(fc, metric_type, "LZN", "WID", "ARA", "#", "", 0.03)
