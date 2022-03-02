import arcpy
import pythonaddins as adn

#            ___________________________
#           | Runs Calculate Default    |
#           | Value, Integrate, and     |
#           | Repair on the proper      |
#           | features for finishing.   |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~

# Script arguments
arcpy.env.workspace = arcpy.GetParameterAsText(0)

arcpy.MakeFeatureLayer_management("HydrographyCrv", "hc")
arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "tg")
arcpy.MakeFeatureLayer_management("UtilityInfrastructurePnt", "up")
arcpy.MakeFeatureLayer_management("UtilityInfrastructureCrv", "uc")
arcpy.MakeFeatureLayer_management("UtilityInfrastructureSrf", "us")
    
# Process: Calculate Default Values
arcpy.CalculateDefaultValues_defense(arcpy.env.workspace)

# Process: Select Data
#arcpy.SelectData_management(TDS, "HydrographyCrv")
arcpy.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("hc", "ihydro_crv")

# Process: Integrate
arcpy.Integrate_management("ihydro_crv", "0.03 Meters")

# Process: Select Data (2)
#arcpy.SelectData_management(TDS, "TransportationGroundCrv")
arcpy.SelectLayerByAttribute_management("tg", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("tg", "itrans_crv")

# Process: Integrate (2)
arcpy.Integrate_management("itrans_crv", "0.03 Meters")

# Process: Select Data (3)
#arcpy.SelectData_management(TDS, "UtilityInfrastructurePnt")
arcpy.SelectLayerByAttribute_management("up", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("up", "iutility_pnt")

# Process: Select Data (4)
#arcpy.SelectData_management(TDS, "UtilityInfrastructureCrv")
arcpy.SelectLayerByAttribute_management("uc", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("uc", "iutility_crv")

# Process: Select Data (8)
#arcpy.SelectData_management(TDS, "UtilityInfrastructureSrf")
arcpy.SelectLayerByAttribute_management("us", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("us", "iutility_srf")

# Process: Integrate (3)
arcpy.Integrate_management("iutility_pnt 2;iutility_crv 1;iutility_srf 3", "0.03 Meters")

# Process: Select Data (5)
#arcpy.SelectData_management(TDS, "HydrographyCrv")
arcpy.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("hc", "rhydro_crv")

# Process: Repair Geometry
arcpy.RepairGeometry_management("rhydro_crv", "DELETE_NULL")

# Process: Select Data (6)
#arcpy.SelectData_management(TDS, "TransportationGroundCrv")
arcpy.SelectLayerByAttribute_management("tg", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("tg", "rtrans_crv")

# Process: Repair Geometry (2)
arcpy.RepairGeometry_management("rtrans_crv", "DELETE_NULL")

# Process: Select Data (7)
#arcpy.SelectData_management(TDS, "UtilityInfrastructureCrv")
arcpy.SelectLayerByAttribute_management("uc", "NEW_SELECTION", "")
arcpy.MakeFeatureLayer_management("uc", "rutility_crv")

# Process: Repair Geometry (3)
arcpy.RepairGeometry_management("rutility_crv", "DELETE_NULL")

