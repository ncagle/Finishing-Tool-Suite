'''
    Refactoring to put things into functions.
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Data Maintenance Tools Category   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Repair All NULL Geometry '''''''''
# Repairs all NULL geometries in each feature class
# rewrite with intersect geometry method to remove duplicate vertices and kickbacks


def process_repair(featureclass):
    tool_name = 'Repair All NULL Geometry'
    write("\n--- {0} ---\n".format(tool_name))
    for fc in featureclass:
        try:
            write("Repairing NULL geometries in {0}".format(fc))
            arcpy.RepairGeometry_management(fc, "DELETE_NULL")
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(arcpy.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)


''''''''' Populate F_Codes '''''''''
# John Jackson's Fcode tool refactored from standalone with included dictionaries instead of imported


def process_fcode(featureclass):
    tool_name = 'Populate F_Codes'
    write("\n--- {0} ---\n".format(tool_name))
    for fc in featureclass:
        try:
            try:
                fields = ['f_code', 'fcsubtype']
                write("Updating {0} Feature F_Codes".format(fc))
                with arcpy.da.UpdateCursor(fc, fields) as fcursor:
                    for row in fcursor:  # Checks if F_Code matches the FCSubtype value. Updates F_Code if they don't match assuming proper subtype
                        if row[0] != str(sub2fcode_dict[row[1]]):
                            row[0] = str(sub2fcode_dict[row[1]])
                            fcursor.updateRow(row)
            except:
                write("{0} does not contain F_codes.".format(fc))
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(arcpy.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)


''''''''' Calculate Default Values '''''''''
# Calculate default values for NULL attributes
# All or nothing. Functions on datasets not individual feature classes
# rewrite using domains and coded values thru cursors


def process_defaults():
    tool_name = 'Calculate Default Values'
    write("\n--- {0} ---\n".format(tool_name))
    write("Locating NULL fields")
    try:
        write("Assigning domain defaults from coded values...")
        arcpy.CalculateDefaultValues_defense(arcpy.env.workspace)
        write("Complete")
    except arcpy.ExecuteError:
        # if the code failed for the current fc, check the error
        error_count += 1
        write("\n***Failed to run {0}.***\n".format(tool_name))
        write("Error Report:")
        write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        write(arcpy.GetMessages())
        write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(
            tool_name))
        write("Exiting tool.\n")
        sys.exit(0)


''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
# Defense mapping version takes too long and crashes. just rewrite with manual calculations


def process_metrics(featureclass):
    tool_name = 'Calculate Metrics'
    write("\n--- {0} ---\n".format(tool_name))
    metric_type = 'LENGTH;WIDTH;AREA;ANGLE_OF_ORIENTATION'
    for fc in featureclass:
        try:
            write("Calculating AOO, ARA, LZN, and WID for {0}".format(fc))
            arcpy.CalculateMetrics_defense(
                fc, metric_type, "LZN", "WID", "ARA", "#", "#", "#")
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(arcpy.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)


''''''''' Update UFI Values '''''''''  # add functionality to only update blank fields
# Iterate through all features and update the ufi field with uuid4 random values


def process_ufi(featureclass):
    tool_name = 'Update UFI Values'
    write("\n--- {0} ---\n".format(tool_name))
    ufi_count = 0
    # Explicit is better than implicit
    # Lambda function works better than "if not fieldname:", which can falsely catch 0.
    # Function that returns boolean of if input field is populated or empty
    def populated(x): return x is not None and str(x).strip() != ''

    for fc in featureclass:
        try:
            with arcpy.da.SearchCursor(fc, 'ufi') as scursor:
                values = [row[0] for row in scursor]
            with arcpy.da.UpdateCursor(fc, 'ufi') as ucursor:
                for row in ucursor:
                    if not populated(row[0]):
                        row[0] = str(uuid.uuid4())
                        ufi_count += 1
                    elif values.count(row[0]) > 1:
                        row[0] = str(uuid.uuid4())
                        ufi_count += 1
                    ucursor.updateRow(row)
                write("Updated UFIs in {0}".format(fc))
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(arcpy.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Feature Specific Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


''''''''' Integrate and Repair '''''''''
# User choice to Integrate and Repair Hydrography curves, TransportationGround curves, or Utility points and surfaces to curves
if hydro or trans or util:
    tool_name = 'Integrate and Repair'
    write("\n--- {0} ---\n".format(tool_name))
while hydro:
    tool_name = 'Hydrography Curves'
    fc1 = 'HydrographyCrv'
    fc2 = 'HydrographySrf'
    if not arcpy.Exists(fc1):
        write("**HydrographyCrv feature class not found\n  To run Integrate, copy an empty Hydro curve feature class from a blank schema into this dataset and run the tool again.")
        break
    if not arcpy.Exists(fc2):
        write("**HydrographySrf feature class not found\n  To run Integrate, copy an empty Hydro surface feature class from a blank schema into this dataset and run the tool again.")
        break
    write("- - - - - - - - - - - - - - - - - - - - - - ")
    write(" ~ {0} ~ ".format(tool_name))
    write("Making {0} and {1} feature layers".format(fc1, fc2))
    arcpy.MakeFeatureLayer_management(fc1, "hc")
    arcpy.MakeFeatureLayer_management(fc2, "hs")
    arcpy.SelectLayerByAttribute_management(
        "hc", "NEW_SELECTION", "zi026_ctuu >= 50000")
    arcpy.SelectLayerByAttribute_management(
        "hs", "NEW_SELECTION", "zi026_ctuu >= 50000")
    arcpy.MakeFeatureLayer_management("hc", "hc_scale")
    srf_count = int(arcpy.GetCount_management("hs").getOutput(0))
    if srf_count > 0:
        arcpy.MakeFeatureLayer_management("hs", "hs_scale")
    write("Repairing {0} lines before Integration".format(fc1))
    arcpy.RepairGeometry_management("hc_scale", "DELETE_NULL")
    hfeat_count = 0
    if not large:
        try:
            feat_count = int(arcpy.GetCount_management(
                "hc_scale").getOutput(0))
            write("Integrating {0} {1} features and \n            {2} {3} features...".format(
                feat_count, fc1, srf_count, fc2))
            if srf_count > 0:
                arcpy.Integrate_management(
                    "hc_scale 1;hs_scale 2", "0.06 Meters")
                arcpy.Integrate_management(
                    "hc_scale 1;hs_scale 2", "0.03 Meters")
            else:
                arcpy.Integrate_management('hc_scale', "0.06 Meters")
                arcpy.Integrate_management('hc_scale', "0.03 Meters")
            hfeat_count = feat_count + srf_count
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(arcpy.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but make sure the 'Process Large Feature Class' option is checked under {0}.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)
    if large:
        try:
            # Create Fishnet
            write(
                "Processing large feature class. Partitioning data in chunks to process.")
            mem_fc = "in_memory\\{0}_grid".format(fc1)
            rectangle = "in_memory\\rectangle"
            write("Defining partition envelope")
            arcpy.MinimumBoundingGeometry_management(
                fc1, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
            with arcpy.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
                for row in scursor:
                    shape = row[0]
                    origin_coord = '{0} {1}'.format(
                        shape.extent.XMin, shape.extent.YMin)
                    y_axis_coord = '{0} {1}'.format(
                        shape.extent.XMin, shape.extent.YMax)
                    corner_coord = '{0} {1}'.format(
                        shape.extent.XMax, shape.extent.YMax)
            write("Constructing fishnet")
            arcpy.CreateFishnet_management(
                mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc1, "POLYGON")
            #arcpy.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
            arcpy.MakeFeatureLayer_management(mem_fc, "hgrid")
            with arcpy.da.SearchCursor("hgrid", ['OID@']) as scursor:
                for row in scursor:
                    select = "OID = {}".format(row[0])
                    arcpy.SelectLayerByAttribute_management(
                        "hgrid", "NEW_SELECTION", select)
                    if srf_count > 0:
                        arcpy.SelectLayerByLocation_management(
                            "hs_scale", "INTERSECT", "hgrid", "", "NEW_SELECTION")
                        ssrf_count = int(arcpy.GetCount_management(
                            "hs_scale").getOutput(0))
                    else:
                        ssrf_count = 0
                    arcpy.SelectLayerByLocation_management(
                        "hc_scale", "INTERSECT", "hgrid", "", "NEW_SELECTION")
                    feat_count = int(arcpy.GetCount_management(
                        "hc_scale").getOutput(0))
                    write("Integrating {0} {1} features and\n            {2} {3} features in partition {4}...".format(
                        feat_count, fc1, ssrf_count, fc2, row[0]))
                    hfeat_count = hfeat_count + feat_count + ssrf_count
                    if ssrf_count > 0:
                        arcpy.Integrate_management(
                            "hc_scale 1;hs_scale 2", "0.06 Meters")
                        arcpy.Integrate_management(
                            "hc_scale 1;hs_scale 2", "0.03 Meters")
                    elif feat_count > 0:
                        arcpy.Integrate_management('hc_scale', "0.06 Meters")
                        arcpy.Integrate_management('hc_scale', "0.03 Meters")
                    else:
                        continue
            write("Freeing partition memory")
            arcpy.Delete_management("in_memory")
            arcpy.Delete_management("hgrid")
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***".format(tool_name))
            write(arcpy.GetMessages())
            write(
                "\nData too dense to be run in partitions. Integrating {0} in this database exceeds our current equipment limitations.".format(fc1))
            write("To continue running tool, uncheck {0} before running again.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)
    write("Repairing {0} and {1} features after Integration".format(fc1, fc2))
    arcpy.RepairGeometry_management("hc_scale", "DELETE_NULL")
    arcpy.RepairGeometry_management("hs_scale", "DELETE_NULL")
    write("Clearing process cache")
    arcpy.Delete_management("hc")
    arcpy.Delete_management("hc_scale")
    arcpy.Delete_management("hs")
    arcpy.Delete_management("hs_scale")
    if trans or util:
        write("- - - - - - - - - - - - - - - - - - - - - -\n")
    else:
        write("- - - - - - - - - - - - - - - - - - - - - -")
    break

while trans:
    tool_name = 'Transportation Points and Curves'
    fc1 = 'TransportationGroundPnt'
    fc2 = 'TransportationGroundCrv'
    if not arcpy.Exists(fc1):
        fc1 = fc2
    if not arcpy.Exists(fc2):
        write("**TransportationGroundCrv feature class not found\n  To run Integrate, copy an empty Trans curve feature class from a blank schema into this dataset and run the tool again.")
        break
    write("- - - - - - - - - - - - - - - - - - - - - - ")
    write(" ~ {0} ~ ".format(tool_name))
    write("Making {0} and {1} feature layers".format(fc1, fc2))
    arcpy.MakeFeatureLayer_management(fc1, "tgp")
    arcpy.MakeFeatureLayer_management(fc2, "tgc")
    arcpy.SelectLayerByAttribute_management(
        "tgp", "NEW_SELECTION", "f_code = 'AQ065' AND zi026_ctuu >= 50000")
    cul_count = int(arcpy.GetCount_management("tgp").getOutput(0))
    arcpy.SelectLayerByAttribute_management(
        "tgc", "NEW_SELECTION", "zi026_ctuu >= 50000")
    if cul_count > 0:
        arcpy.MakeFeatureLayer_management("tgp", "tgp_scale")
    arcpy.MakeFeatureLayer_management("tgc", "tgc_scale")
    write("Repairing {0} lines before Integration".format(fc2))
    arcpy.RepairGeometry_management("tgc_scale", "DELETE_NULL")
    tfeat_count = 0
    if not large:
        try:
            feat_count = int(arcpy.GetCount_management(
                "tgc_scale").getOutput(0))
            write("Integrating {0} {1} features and\n            {2} Culvert points...".format(
                feat_count, fc2, cul_count))
            if cul_count > 0:
                arcpy.Integrate_management(
                    "tgp_scale 2;tgc_scale 1", "0.06 Meters")
                arcpy.Integrate_management(
                    "tgp_scale 2;tgc_scale 1", "0.03 Meters")
            else:
                arcpy.Integrate_management("tgc_scale", "0.06 Meters")
                arcpy.Integrate_management("tgc_scale", "0.03 Meters")
            tfeat_count = feat_count + cul_count
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(arcpy.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but make sure the 'Process Large Feature Class' option is checked under {0}.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)
    if large:
        try:
            # Create Fishnet
            write(
                "Processing large feature class. Partitioning data in chunks to process.")
            mem_fc = "in_memory\\{0}_grid".format(fc2)
            rectangle = "in_memory\\rectangle"
            write("Defining partition envelope")
            arcpy.MinimumBoundingGeometry_management(
                fc2, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
            with arcpy.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
                for row in scursor:
                    shape = row[0]
                    origin_coord = '{0} {1}'.format(
                        shape.extent.XMin, shape.extent.YMin)
                    y_axis_coord = '{0} {1}'.format(
                        shape.extent.XMin, shape.extent.YMax)
                    corner_coord = '{0} {1}'.format(
                        shape.extent.XMax, shape.extent.YMax)
            write("Constructing fishnet")
            arcpy.CreateFishnet_management(
                mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc2, "POLYGON")
            #arcpy.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
            arcpy.MakeFeatureLayer_management(mem_fc, "tgrid")
            with arcpy.da.SearchCursor("tgrid", ['OID@']) as scursor:
                for row in scursor:
                    select = "OID = {}".format(row[0])
                    arcpy.SelectLayerByAttribute_management(
                        "tgrid", "NEW_SELECTION", select)
                    if cul_count > 0:
                        arcpy.SelectLayerByLocation_management(
                            "tgp_scale", "INTERSECT", "tgrid", "", "NEW_SELECTION")
                        pcul_count = int(arcpy.GetCount_management(
                            "tgp_scale").getOutput(0))
                    else:
                        pcul_count = 0
                    arcpy.SelectLayerByLocation_management(
                        "tgc_scale", "INTERSECT", "tgrid", "", "NEW_SELECTION")
                    feat_count = int(arcpy.GetCount_management(
                        "tgc_scale").getOutput(0))
                    write("Integrating {0} {1} features and\n            {2} Culvert points in partition {3}...".format(
                        feat_count, fc2, pcul_count, row[0]))
                    tfeat_count = tfeat_count + feat_count + pcul_count
                    if pcul_count > 0:
                        arcpy.Integrate_management(
                            "tgp_scale 2;tgc_scale 1", "0.06 Meters")
                        arcpy.Integrate_management(
                            "tgp_scale 2;tgc_scale 1", "0.03 Meters")
                    elif feat_count > 0:
                        arcpy.Integrate_management("tgc_scale", "0.06 Meters")
                        arcpy.Integrate_management("tgc_scale", "0.03 Meters")
                    else:
                        continue
            write("Freeing partition memory")
            arcpy.Delete_management("in_memory")
            arcpy.Delete_management("tgrid")
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***".format(tool_name))
            write(arcpy.GetMessages())
            write(
                "\nData too dense to be run in partitions. Integrating {0} in this database exceeds our current equipment limitations.".format(fc2))
            write("To continue running tool, uncheck {0} before running again.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)
    write("Repairing {0} lines after Integration".format(fc2))
    arcpy.RepairGeometry_management("tgc_scale", "DELETE_NULL")
    write("Clearing process cache")
    arcpy.Delete_management("tgp")
    arcpy.Delete_management("tgc")
    arcpy.Delete_management("tgp_scale")
    arcpy.Delete_management("tgc_scale")
    if util:
        write("- - - - - - - - - - - - - - - - - - - - - -\n")
    else:
        write("- - - - - - - - - - - - - - - - - - - - - -")
    break

while util:
    tool_name = 'Utility Points, Lines, and Surfaces'
    fc1 = 'UtilityInfrastructurePnt'
    fc2 = 'UtilityInfrastructureCrv'
    fc3 = 'UtilityInfrastructureSrf'
    if not arcpy.Exists(fc1):
        write("**UtilityInfrastructurePnt feature class not found\n  To run Integrate, copy an empty Utility point feature class from a blank schema into this dataset and run the tool again.")
        break
    if not arcpy.Exists(fc2):
        write("**UtilityInfrastructureCrv feature class not found\n  To run Integrate, copy an empty Utility curve feature class from a blank schema into this dataset and run the tool again.")
        break
    if not arcpy.Exists(fc3):
        write("**UtilityInfrastructureSrf feature class not found\n  To run Integrate, copy an empty Utility surface feature class from a blank schema into this dataset and run the tool again.")
        break
    write("- - - - - - - - - - - - - - - - - - - - - - ")
    write(" ~ {0} ~ ".format(tool_name))
    write("Making {0}, {1}, and {2} feature layers".format(fc1, fc2, fc3))
    arcpy.MakeFeatureLayer_management(fc1, "up")
    arcpy.MakeFeatureLayer_management(fc2, "uc")
    arcpy.MakeFeatureLayer_management(fc3, "us")
    arcpy.SelectLayerByAttribute_management(
        "up", "NEW_SELECTION", "zi026_ctuu >= 50000")
    arcpy.SelectLayerByAttribute_management(
        "uc", "NEW_SELECTION", "zi026_ctuu >= 50000")
    arcpy.SelectLayerByAttribute_management(
        "us", "NEW_SELECTION", "zi026_ctuu >= 50000")
    arcpy.MakeFeatureLayer_management("up", "up_scale")
    arcpy.MakeFeatureLayer_management("uc", "uc_scale")
    arcpy.MakeFeatureLayer_management("us", "us_scale")
    write(
        "Repairing {0} lines and {1} polygons before Integration".format(fc2, fc3))
    arcpy.RepairGeometry_management("uc_scale", "DELETE_NULL")
    arcpy.RepairGeometry_management("us_scale", "DELETE_NULL")
    ufeat_count = 0
    if not large:
        try:
            feat_count1 = int(arcpy.GetCount_management(
                "up_scale").getOutput(0))
            feat_count2 = int(arcpy.GetCount_management(
                "uc_scale").getOutput(0))
            feat_count3 = int(arcpy.GetCount_management(
                "us_scale").getOutput(0))
            write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features...".format(
                feat_count1, fc1, feat_count2, fc2, feat_count3, fc3))
            arcpy.Integrate_management(
                "up_scale 2;uc_scale 1;us_scale 3", "0.06 Meters")
            arcpy.Integrate_management(
                "up_scale 2;uc_scale 1;us_scale 3", "0.03 Meters")
            ufeat_count = feat_count1 + feat_count2 + feat_count3
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***\n".format(tool_name))
            write("Error Report:")
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write(arcpy.GetMessages())
            write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            write("\nPlease rerun the tool, but make sure the 'Process Large Feature Class' option is checked under {0}.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)
    if large:
        try:
            # Create Fishnet
            write(
                "Processing large feature class. Partitioning data in chunks to process.")
            mem_fc = "in_memory\\{0}_grid".format(fc2)
            rectangle = "in_memory\\rectangle"
            write("Defining partition envelope")
            arcpy.MinimumBoundingGeometry_management(
                fc2, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
            with arcpy.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
                for row in scursor:
                    shape = row[0]
                    origin_coord = '{0} {1}'.format(
                        shape.extent.XMin, shape.extent.YMin)
                    y_axis_coord = '{0} {1}'.format(
                        shape.extent.XMin, shape.extent.YMax)
                    corner_coord = '{0} {1}'.format(
                        shape.extent.XMax, shape.extent.YMax)
            write("Constructing fishnet")
            arcpy.CreateFishnet_management(
                mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc2, "POLYGON")
            #arcpy.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
            arcpy.MakeFeatureLayer_management(mem_fc, "ugrid")
            with arcpy.da.SearchCursor("ugrid", ['OID@']) as scursor:
                # Add check for any 0 count features selected in each loop that might default to all features instead of 0 in current partition
                for row in scursor:
                    select = "OID = {}".format(row[0])
                    arcpy.SelectLayerByAttribute_management(
                        "ugrid", "NEW_SELECTION", select)
                    arcpy.SelectLayerByLocation_management(
                        "up_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
                    arcpy.SelectLayerByLocation_management(
                        "uc_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
                    arcpy.SelectLayerByLocation_management(
                        "us_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
                    feat_count1 = int(arcpy.GetCount_management(
                        "up_scale").getOutput(0))
                    feat_count2 = int(arcpy.GetCount_management(
                        "uc_scale").getOutput(0))
                    feat_count3 = int(arcpy.GetCount_management(
                        "us_scale").getOutput(0))
                    ufeat_count = ufeat_count + feat_count1 + feat_count2 + feat_count3
                    write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(
                        feat_count1, fc1, feat_count2, fc2, feat_count3, fc3, row[0]))
                    arcpy.Integrate_management(
                        "up_scale 2;uc_scale 1;us_scale 3", "0.06 Meters")
                    arcpy.Integrate_management(
                        "up_scale 2;uc_scale 1;us_scale 3", "0.03 Meters")
            write("Freeing partition memory")
            arcpy.Delete_management("in_memory")
            arcpy.Delete_management("ugrid")
        except arcpy.ExecuteError:
            # if the code failed for the current fc, check the error
            error_count += 1
            write("\n***Failed to run {0}.***".format(tool_name))
            write(arcpy.GetMessages())
            write("\nData too dense to be run in partitions. Integrating Utilities in this database exceeds our current equipment limitations.")
            write("To continue running tool, uncheck {0} before running again.".format(
                tool_name))
            write("Exiting tool.\n")
            sys.exit(0)
    write(
        "Repairing {0} lines and {1} polygons after Integration".format(fc2, fc3))
    arcpy.RepairGeometry_management("uc_scale", "DELETE_NULL")
    arcpy.RepairGeometry_management("us_scale", "DELETE_NULL")
    write("Clearing process cache")
    arcpy.Delete_management("up")
    arcpy.Delete_management("uc")
    arcpy.Delete_management("us")
    arcpy.Delete_management("up_scale")
    arcpy.Delete_management("uc_scale")
    arcpy.Delete_management("us_scale")
    write("- - - - - - - - - - - - - - - - - - - - - -")
    break
