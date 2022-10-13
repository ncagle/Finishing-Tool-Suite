import arcpy
import pythonaddins as adn
import sys
import os
import time
import fcfields
import labelDict as ld

#            ___________________________
#           | Runs the pre-processing   |
#           | tools on a database in    |
#           | the proper sequence.      |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~

TDS = arcpy.GetParameterAsText(0)

def bridgewid(TDS):

   try:
      # Take the TDS as the tool parameter || TDS workspace doesn't play nice with the SDE connection
      # Changed to taking feature layers directly
      arcpy.env.workspace = TDS
      workspace = os.path.dirname(arcpy.env.workspace)


      arcpy.AddMessage("Working local...")

      # Pull width and geometry fields for bridges
      fieldsB = ['WID', 'SHAPE@']
      # Pull width and geometry fields for roads
      fieldsR = ['ZI016_WD1', 'SHAPE@']
      # Pull width and geometry fields for rails and sidetracks
      fieldsRR = ['ZI017_GAW', 'SHAPE@']

      # Have to convert the feature classes from the TDS into usable layers to please the capricious, fastidious ArcPy gods
      # When run locally the function can just take the actual name of the layer like it should cz that makes sense
      arcpy.AddMessage("Making feature layers...")
      arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "bridge_crv_lyr")
      arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "road_crv_lyr")
      arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "rail_crv_lyr")
      arcpy.AddMessage("Successfully made the feature layers!")
         
   except:
      arcpy.AddMessage("Double check alias names of features.")

      
   # Select road bridges with default (-999999) width
   arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE = 'AQ040'")
   arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 13")

   # Make road bridges with default (-999999) width into layer
   arcpy.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeR")
   arcpy.GetMessages()

   # Select rail bridges with default (-999999) width
   arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE = 'AQ040'")
   arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 12")

   # Make rail bridges with default (-999999) width into layer
   arcpy.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeRR")
   arcpy.GetMessages()

   # Select roads that share curve with the default width bridges above
   arcpy.SelectLayerByAttribute_management("road_crv_lyr", "NEW_SELECTION", "F_CODE = 'AP030'")
   arcpy.SelectLayerByLocation_management("road_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "fc_bridgeR", "", "SUBSET_SELECTION")

   # Make roads that share curve with default width bridges into layer
   arcpy.MakeFeatureLayer_management("road_crv_lyr", "fc_road")
   arcpy.GetMessages()
   
   # Select rails that share curve with the default width bridges above
   arcpy.SelectLayerByAttribute_management("rail_crv_lyr", "NEW_SELECTION", "F_CODE = 'AN010' OR F_CODE = 'AN050'")
   arcpy.SelectLayerByLocation_management("rail_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "fc_bridgeRR", "", "SUBSET_SELECTION")

   # Make rails that share curve with default width bridges into layer
   arcpy.MakeFeatureLayer_management("rail_crv_lyr", "fc_rail")
   arcpy.GetMessages()

   # Gets a count of selected bridges, roads, and rails
   fc_bridgeR_total = int(arcpy.management.GetCount("fc_bridgeR").getOutput(0))
   fc_bridgeRR_total = int(arcpy.management.GetCount("fc_bridgeRR").getOutput(0))
   total_bridges = fc_bridgeR_total + fc_bridgeRR_total
   total_roads = int(arcpy.management.GetCount("fc_road").getOutput(0))
   total_rails = int(arcpy.management.GetCount("fc_rail").getOutput(0))
   
   # Error handling. If 0 bridges selected the script hangs. Requires exit.
   if total_bridges == 0:
      arcpy.AddMessage("No default bridges found.")
      return
   # Error handling. If no roads or rails to select against, likely something will break. So preemptively adding an exit.
   if total_roads == 0 and total_rails == 0:
      total_bridges = str(total_bridges)
      arcpy.AddMessage(total_bridges + " default value bridges found.")
      arcpy.AddMessage("No underlying roads or rails for default bridges. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.")
      return

   # Announces the total default bridges found.
   total_bridges = str(total_bridges)
   arcpy.AddMessage(total_bridges + " default value bridges found.")

   # Start an edit session. Must provide the workspace.
   edit = arcpy.da.Editor(workspace)
   # Edit session is started without an undo/redo stack for versioned data
   # (for second argument, use False for unversioned data)
   edit.startEditing(False, True)
   arcpy.GetMessages()

   countR = 0
   if fc_bridgeR_total > 0:
      # Start an edit operation for road bridges
      edit.startOperation()
      # Loop to update bridge width to it's corresponding road width
      with arcpy.da.UpdateCursor("fc_bridgeR", fieldsB) as bridgeR:    # UpdateCursor for bridges with width and geometry
         for i in bridgeR:
            with arcpy.da.SearchCursor("fc_road", fieldsR) as road:    # SearchCursor for roads with width and geometry
               for j in road:
                  if i[1].within(j[1]):   # Check if bridge shares curve with road(if not working test contains\within)
                     if i[0] < j[0]:
                        i[0] = j[0]*1.5    # Sets current bridge width to road width * [factor]
                        #arcpy.AddMessage("Wide boy fixed")
            bridgeR.updateRow(i)
            countR += 1
         arcpy.GetMessages()

      # Stop the edit operation.
      edit.stopOperation()
   arcpy.AddMessage(str(countR) + " bridges on roads updated.")

   countRR = 0
   if fc_bridgeRR_total > 0:
      # Start an edit operation for rail bridges
      edit.startOperation()
      # Loop to update bridge width to it's corresponding rail width
      with arcpy.da.UpdateCursor("fc_bridgeRR", fieldsB) as bridgeRR:    # UpdateCursor for bridges with width and geometry
         for i in bridgeRR:
            with arcpy.da.SearchCursor("fc_rail", fieldsRR) as rail:    # SearchCursor for rails with width and geometry
               for j in rail:
                  if i[1].within(j[1]):   # Check if bridge shares curve with rail(if not working test contains\within)
                     if i[0] < j[0]:
                        i[0] = int(j[0])+1    # Sets current bridge width to integer rounded rail gauge width + [value]
                        #arcpy.AddMessage("Wide boy fixed")
            bridgeRR.updateRow(i)
            countRR += 1
         arcpy.GetMessages()

      # Stop the edit operation.
      edit.stopOperation()
   arcpy.AddMessage(str(countRR) + " bridges on railroads updated.")
   
   # Stop the edit session and save the changes
   try:
      edit.stopEditing(True)
      arcpy.GetMessages()
   except:
      arcpy.AddMessage("First attempt to save failed. Checking for updated SDE version. Trying again in 5 seconds. Please hold...")
      time.sleep(5)
      edit.stopEditing(True)

   # Select any remaining bridges with default (-999999) width
   arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE = 'AQ040'")
   arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999")
   # Make these selections into a new layer and get a count
   arcpy.MakeFeatureLayer_management("bridge_crv_lyr", "bridges_rem")
   total_rem = int(arcpy.management.GetCount("bridges_rem").getOutput(0))
   # Final messages of the state of the data after tool completion
   count = (countR + countRR) - total_rem
   count = str(count)
   arcpy.AddMessage("Updated " + count + " bridges with new WID values.")
   if total_rem == 0:
      return
   elif total_rem > 0:
      total_rem = str(total_rem)
      arcpy.AddMessage(total_rem + " bridges still have default WID. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.")

################################################

def buildingdescale(TDS):
    
    arcpy.env.workspace = TDS
    arcpy.env.overwriteOutput = True

    # Make initial layers from the workspace
    fields = 'ZI026_CTUU'
    arcpy.MakeFeatureLayer_management("SettlementSrf", "settlement_srf")
    #arcpy.MakeFeatureLayer_management("StructureSrf", "structure_srf")
    arcpy.MakeFeatureLayer_management("StructurePnt", "structure_pnt")

    # Make layer of BUAs
    arcpy.SelectLayerByAttribute_management("settlement_srf", "NEW_SELECTION", "F_CODE = 'AL020'")
    arcpy.MakeFeatureLayer_management("settlement_srf", "buas")
    # Make layer of building surfaces
    #arcpy.SelectLayerByAttribute_management("structure_srf", "NEW_SELECTION", "F_CODE = 'AL013'")
    #arcpy.MakeFeatureLayer_management("structure_srf", "building_srf")
    # Make layer of building points
    arcpy.SelectLayerByAttribute_management("structure_pnt", "NEW_SELECTION", "F_CODE = 'AL013'")
    arcpy.MakeFeatureLayer_management("structure_pnt", "building_pnt")
    # Layer of building surfaces within BUAs
    #arcpy.SelectLayerByLocation_management ("building_srf", "WITHIN", "buas", "", "NEW_SELECTION")
    #arcpy.MakeFeatureLayer_management("building_srf", "bua_building_s")
    # Layer of building points within BUAs
    arcpy.SelectLayerByLocation_management ("building_pnt", "WITHIN", "buas", "", "NEW_SELECTION")
    arcpy.MakeFeatureLayer_management("building_pnt", "bua_building_p")
    # Select non important building surfaces
    #arcpy.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", "FFN IN (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)")
    #arcpy.SelectLayerByAttribute_management("bua_building_s", "SWITCH_SELECTION")
    #arcpy.MakeFeatureLayer_management("bua_building_s", "non_import_s")
    # Select non important building points
    arcpy.SelectLayerByAttribute_management("bua_building_p", "NEW_SELECTION", "FFN IN (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)")
    arcpy.SelectLayerByAttribute_management("bua_building_p", "SWITCH_SELECTION")
    arcpy.MakeFeatureLayer_management("bua_building_p", "non_import_p")

    # Count buildings and buas in selections
    bua_count = int(arcpy.GetCount_management("buas").getOutput(0))
    #non_import_count_s = int(arcpy.GetCount_management("non_import_s").getOutput(0))
    non_import_count_p = int(arcpy.GetCount_management("non_import_p").getOutput(0))
    #total_buildings = non_import_count_s + non_import_count_p

    # End script if there are no BUAs or no buildings inside them
    if bua_count == 0:
        arcpy.AddMessage("No BUAs found.")
        return
    elif non_import_count_p == 0:
        arcpy.AddMessage("No buildings in BUAs found.")
        return

    arcpy.AddMessage(str(non_import_count_p) + " buildings found. Descaling...")

    with arcpy.da.UpdateCursor("non_import_p", fields) as cursor_p:
        for row in cursor_p:
            row[0] = 12500
            cursor_p.updateRow(row)

    arcpy.AddMessage(str(non_import_count_p) + " buildings descaled to CTUU 12500.")

################################################

def calcmetrics(TDS):
    arcpy.env.workspace = TDS
    featureclass = arcpy.ListFeatureClasses()
    metric_type = 'LENGTH;WIDTH;AREA;ANGLE_OF_ORIENTATION'

    for fc in featureclass:
        arcpy.AddMessage("Calculating AOO, ARA, LZN, and WID for " + str(fc))
        arcpy.defense.CalculateMetrics(fc, metric_type, "LZN", "WID", "ARA", "#", "", 0.03)

################################################

def deleteidentical(TDS):
    arcpy.env.workspace = TDS
    arcpy.env.overwriteOutput = True

    # Pull in feature classes from TDS
    featureclass = arcpy.ListFeatureClasses()

    # Set the output directory for the FindIdentical tool
    out_table = os.path.dirname(arcpy.env.workspace)
    # Precreate the path for the output dBASE table
    path = out_table.split(".")
    path.pop()
    table_loc = path[0] + str(".dbf")
    arcpy.AddMessage("Creating temporary output file: " + str(table_loc))

    # Loop feature classes and FindIdentical to get a count, then delete any found
    for fc in featureclass:
        dick = fcfields.fc_fields[fc]
        arcpy.FindIdentical_management(fc, out_table, dick, "", "", output_record_option="ONLY_DUPLICATES")
        rows = int(arcpy.management.GetCount(table_loc).getOutput(0))
        arcpy.AddMessage("Found " + str(rows) + " duplicate " + str(fc) + " features.")
        if rows > 0:
            arcpy.DeleteIdentical_management(fc, fcfields.fc_fields[fc])
            arcpy.AddMessage("Deleted " + str(rows) + " duplicate " + str(fc) + " features.")

    # Clean up before next process
    del table_loc

################################################

def finishingtools(TDS):
   arcpy.env.workspace = TDS

   arcpy.MakeFeatureLayer_management("HydrographyCrv", "hc")
   arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "tg")
   arcpy.MakeFeatureLayer_management("UtilityInfrastructurePnt", "up")
   arcpy.MakeFeatureLayer_management("UtilityInfrastructureCrv", "uc")
   arcpy.MakeFeatureLayer_management("UtilityInfrastructureSrf", "us")


   # Calculate Default Values
   arcpy.AddMessage("Calculating Default Values")
   arcpy.CalculateDefaultValues_defense(arcpy.env.workspace)


   # Repairing before Integration
   arcpy.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("hc", "rhydro_crv1")
   arcpy.RepairGeometry_management("rhydro_crv1", "DELETE_NULL")

   arcpy.SelectLayerByAttribute_management("tg", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("tg", "rtrans_crv1")
   arcpy.RepairGeometry_management("rtrans_crv1", "DELETE_NULL")


   arcpy.SelectLayerByAttribute_management("uc", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("uc", "rutility_crv1")
   arcpy.RepairGeometry_management("rutility_crv1", "DELETE_NULL")


   # Integrating Hydro curves
   arcpy.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("hc", "ihydro_crv")
   arcpy.AddMessage("Integrating Hydro")
   arcpy.Integrate_management("ihydro_crv", "0.03 Meters")

   # Integrating Trans curves
   arcpy.SelectLayerByAttribute_management("tg", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("tg", "itrans_crv")
   arcpy.AddMessage("Integrating Trans")
   arcpy.Integrate_management("itrans_crv", "0.03 Meters")

   # Integrating Utility surfaces and points to curves
   arcpy.SelectLayerByAttribute_management("up", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("up", "iutility_pnt")
   arcpy.SelectLayerByAttribute_management("uc", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("uc", "iutility_crv")
   arcpy.SelectLayerByAttribute_management("us", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("us", "iutility_srf")
   arcpy.AddMessage("Integrating Utility")
   arcpy.Integrate_management("iutility_pnt 2;iutility_crv 1;iutility_srf 3", "0.03 Meters")


   # Post Integration Repair
   arcpy.AddMessage("Repairing Lines")
   arcpy.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("hc", "rhydro_crv")
   arcpy.RepairGeometry_management("rhydro_crv", "DELETE_NULL")

   arcpy.SelectLayerByAttribute_management("tg", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("tg", "rtrans_crv")
   arcpy.RepairGeometry_management("rtrans_crv", "DELETE_NULL")

   arcpy.SelectLayerByAttribute_management("uc", "NEW_SELECTION", "")
   arcpy.MakeFeatureLayer_management("uc", "rutility_crv")
   arcpy.RepairGeometry_management("rutility_crv", "DELETE_NULL")
   
################################################

def populatefcode(TDS):
    arcpy.env.workspace = TDS
    workspace = arcpy.env.workspace


    fcList = arcpy.ListFeatureClasses()
    sub2Fcode = ld.sub2FcodeDict



    for fc in fcList:
        try:
            with arcpy.da.UpdateCursor(fc, ["f_code", "fcsubtype"]) as fCursor:
                for i in fCursor:
                    if i[0] != str(sub2Fcode[i[1]]):
                        i[0] = str(sub2Fcode[i[1]])
                        fCursor.updateRow(i)
            arcpy.AddMessage(str(fc)+" Features updated")
        except:
            arcpy.AddMessage(str(fc)+" does not contain F_codes.")

################################################

def pylonhgt(TDS):

   # User input for if connecting to SDE
   # Take the TDS as the tool parameter || TDS workspace doesn't play nice with the SDE connection
   arcpy.env.workspace = TDS
   workspace = os.path.dirname(arcpy.env.workspace)

   arcpy.AddMessage("Working local...")

   # Pull height and geometry fields
   fields = ['HGT', 'SHAPE@']

   # Have to convert the feature classes from the TDS into usable layers to please the capricious, fastidious ArcPy gods
   # When run locally the function can just take the actual name of the layer like it should cz that makes sense
   arcpy.AddMessage("Making feature layers...")
   arcpy.MakeFeatureLayer_management("UtilityInfrastructurePnt", "utility_pnt_lyr")
   arcpy.MakeFeatureLayer_management("UtilityInfrastructureCrv", "utility_crv_lyr")
   arcpy.AddMessage("Successfully made the feature layers!")

   
   # Select pylons with default (-999999) height
   arcpy.SelectLayerByAttribute_management("utility_pnt_lyr", "NEW_SELECTION", "F_CODE = 'AT042'")
   arcpy.SelectLayerByAttribute_management("utility_pnt_lyr", "SUBSET_SELECTION", "HGT = -999999")
   arcpy.MakeFeatureLayer_management("utility_pnt_lyr", "fc_pylon_total")
   # Select cables that intersect the default height pylons above and removes any with default height
   arcpy.SelectLayerByAttribute_management("utility_crv_lyr", "NEW_SELECTION", "F_CODE = 'AT005'")
   arcpy.SelectLayerByLocation_management("utility_crv_lyr", "INTERSECT", "utility_pnt_lyr", "", "SUBSET_SELECTION")
   arcpy.MakeFeatureLayer_management("utility_pnt_lyr", "fc_cable_total")
   arcpy.SelectLayerByAttribute_management("utility_crv_lyr", "REMOVE_FROM_SELECTION", "HGT = -999999")
   # Select only the default pylons that intersect cables to speed up run time
   arcpy.SelectLayerByLocation_management("utility_pnt_lyr", "INTERSECT", "utility_crv_lyr", "", "SUBSET_SELECTION")

   # Make these selections into layers
   arcpy.MakeFeatureLayer_management("utility_pnt_lyr", "fc_pylon")
   arcpy.MakeFeatureLayer_management("utility_crv_lyr", "fc_cable")
   arcpy.GetMessages()

   # Gets a count of selected pylons and cables
   total_pylons = int(arcpy.management.GetCount("fc_pylon_total").getOutput(0))
   total_cables = int(arcpy.management.GetCount("fc_cable_total").getOutput(0))
   usable_pylons = int(arcpy.management.GetCount("fc_pylon").getOutput(0))
   usable_cables = int(arcpy.management.GetCount("fc_cable").getOutput(0))

   
   # Error handling. If 0 pylons selected the script hangs. Requires exit.
   if total_pylons == 0:
      arcpy.AddMessage("No default pylons found.")
      return
   # Error handling. If no cables to select against, likely something will break. So preemptively adding an exit.
   if total_cables == 0:
      total_pylons = str(total_pylons)
      arcpy.AddMessage(total_pylons + " default value pylons found.")
      arcpy.AddMessage("No intersecting cables for default pylons. \n Try running Integrate and Repair then try again. \n The default pylons are either not snapped or missing a cable.")
      return


   # Announces the total default pylons found.
   x = total_cables - usable_cables
   x = str(x)
   y = total_pylons - usable_pylons
   y = str(y)
   total_pylons = str(total_pylons)
   usable_pylons = str(usable_pylons)
   arcpy.AddMessage(total_pylons + " default value pylons found.")
   arcpy.AddMessage(x + " of the intersecting cables don't have a height. These will be ignored.")
   arcpy.AddMessage(usable_pylons + " pylons are intersecting a cable with a height value and will be updated.")


   # Loop to update pylon height to it's corresponding cable height
   with arcpy.da.UpdateCursor("fc_pylon", fields) as pylon:    # UpdateCursor for pylons with height and geometry
      lecount = 0
      for i in pylon:
         with arcpy.da.SearchCursor("fc_cable", fields) as cable:    # SearchCursor for cables with height and geometry
            for j in cable:
               if not i[1].disjoint(j[1]):   # Check if pylon intersects a cable
                  if i[0] < j[0]:
                     i[0] = j[0]    # Sets current pylon HGT to intersecting cable's HGT
                     #arcpy.AddMessage("Tall boy fixed")
         pylon.updateRow(i)
         lecount += 1
      arcpy.GetMessages()


   # Select any remaining pylons with default (-999999) height
   arcpy.SelectLayerByAttribute_management("fc_pylon", "NEW_SELECTION", "F_CODE = 'AT042'")
   arcpy.SelectLayerByAttribute_management("fc_pylon", "SUBSET_SELECTION", "HGT = -999999")
   # Make these selections into a new layer and get a count
   arcpy.MakeFeatureLayer_management("fc_pylon", "pylons_rem")
   total_rem = int(arcpy.management.GetCount("pylons_rem").getOutput(0))
   # Final messages of the state of the data after tool completion
   lecount = lecount - total_rem
   total_rem = str(total_rem)
   lecount = str(lecount)
   arcpy.AddMessage("Updated " + lecount + " pylons with new HGT values.")
   arcpy.AddMessage(total_rem + " pylons still have default HGT. \n Consider running Integrate and Repair before trying again. \n The remaining pylons are not snapped, missing a cable, or the underlying cable doesn't have a height.")

################################################

arcpy.AddMessage("Running Populate F_CODE")
populatefcode(TDS)
arcpy.AddMessage("Running Finishing Tools")
finishingtools(TDS)
arcpy.AddMessage("Running Delete Identical")
deleteidentical(TDS)
arcpy.AddMessage("Running Calculate Metrics")
calcmetrics(TDS)
arcpy.AddMessage("Running Bridge Default WID Updater")
bridgewid(TDS)
arcpy.AddMessage("Running Pylon Default HGT Updater")
pylonhgt(TDS)
arcpy.AddMessage("Running Building in BUA Descaler")
buildingdescale(TDS)
