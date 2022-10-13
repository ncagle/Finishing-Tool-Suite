import arcpy
import pythonaddins as adn
import sys
import os
import time

#            ___________________________
#           | Checks for pylons with    |
#           | default HGT (-999999)     |
#           | and updates them          |
#           | to match the intersecting |
#           | cable HGT.                |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~

def pylonhgt():

   # User input for if connecting to SDE
   # Take the TDS as the tool parameter || TDS workspace doesn't play nice with the SDE connection
   arcpy.env.workspace = arcpy.GetParameterAsText(0)
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


pylonhgt ()

# working inline

# with arcpy.da.UpdateCursor("UtilityInfrastructurePoints", ['HGT', 'SHAPE@', 'F_CODE']) as pylon:
#    for i in pylon:
#       print(i[0])
#       if i[2] == 'AT042':
#          with arcpy.da.SearchCursor("UtilityInfrastructureCurves", ['HGT', 'SHAPE@', 'F_CODE']) as cable:
#             for j in cable:
#                if j[2] == 'AT005':
#                   if not i[1].disjoint(j[1]):
#                      if i[0] < j[0]:
#                         i[0] = j[0]
#       pylon.updateRow(i)      
