import arcpy
import pythonaddins as adn
import sys
import os
import time

#            ___________________________
#           | Checks for bridges with   |
#           | default WID (-999999)     |
#           | and updates them          |
#           | to match the underlying   |
#           | road or rail WID.         |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~

def bridgewid():

   try:
      # Take the TDS as the tool parameter || TDS workspace doesn't play nice with the SDE connection
      # Changed to taking feature layers directly
      arcpy.env.workspace = arcpy.GetParameterAsText(0)
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

bridgewid ()
