import arcpy as ap
from arcpy import AddMessage as write
from datetime import datetime as dt
import os
from math import sqrt
import uuid

#----------------------------------------------------------------
#* Reporting class
# To track and report each of the processes performed
    #   Repair Null Geometry        --> (NullsFound, FeaturesUpdated)
    #   Populate Default Values     --> FeaturesUpdated
    #   Populate F Codes            --> FeaturesUpdated
    #   Calculate Metrics           --> FeaturesUpdated
    #   Update UFI                  --> FeaturesUpdated
    #   Explode Multiparts          --> (MultipartsFound, ExplodedFeaturesCount)
    #   Delete Identical Features   --> IdenticalFeatuersFound
    #   Integrate Features          --> FeaturesProcessed
class ProcessReport:
    def __init__(self, active_functions):
        if "Repair Null Geometry" in active_functions:
            self.repair_nulls = True
        else:
            self.repair_nulls = False
        if "Populate Default Values" in active_functions:
            self.pop_default = True
            self.null_count = 0
            self.default_count = 0
        else:
            self.pop_default = False
            self.default_count = None
            self.null_count = None
        if "Populate F_Codes" in active_functions:
            self.pop_fcode = True
            self.fcode_count = 0
        else:
            self.pop_fcode = False
            self.fcode_count = None
        if "Calculate Metrics" in active_functions:
            self.calc_metric = True
            self.calc_count = 0
        else:
            self.calc_metric = False
            self.calc_count = None
        if "Update UFI" in active_functions:
            self.ufi = True
            self.ufi_count = 0
        else:
            self.ufi = False
            self.ufi_count = None
        if "Explode Multiparts" in active_functions:
            self.explode = True
            self.multipart_count = 0
            self.explode_count = 0
        else:
            self.explode = False
            self.multipart_count = None
            self.explode_count = None
        if "Delete Identical Features" in active_functions:
            self.delete_ident = True
            self.ident_count = 0
        else:
            self.delete_ident = False
            self.ident_count = None
        
        self.integrate_hydro = "Integrate Hydro" in active_functions
        self.integrate_util = "Integrate Utilities" in active_functions
        self.integrate_trans = "Integrate Trans" in active_functions
        if self.integrate_hydro + self.integrate_util + self.integrate_trans:
            self.integrate = True
            self.integrate_count = 0
        else:
            self.integrate = False
            self.integrate_count = None
    
    def add_default_count(self, default_return):
        self.null_count += default_return[0]
        self.default_count += default_return[1]

    def add_fcode_count(self, fcode_return):
        self.fcode_count += fcode_return

    def add_calc_count(self, calc_return):
        self.calc_count += calc_return

    def add_ufi_count(self, ufi_return):
        self.ufi_count += ufi_return

    def add_explode_count(self, explode_return):
        self.multipart_count += explode_return[0]
        self.explode_count += explode_return[1]

    def add_delete_ident_count(self, delete_ident_return):
        self.ident_count += delete_ident_return

    def add_integrate_count(self, integrate_return):
        self.integrate_count += integrate_return
    
    def function_results(self, tool):
        if tool is None:
            return "Process Not Performed"
        else:
            return tool
    def function_used(self, function):
        if function:
            return "ON"
        else:
            return "OFF"

    def report_totals(self):
        output = self.function_results
        default = self.default_count
        null = self.null_count
        fcode = self.fcode_count
        calc = self.calc_count
        ufi = self.ufi_count
        multi = self.multipart_count
        explode = self.explode_count
        ident = self.ident_count
        integrate = self.integrate_count
        
        report = "\n\n\nThe Final Count:"\
                    "\n\tPopulate Default Values:"\
                    "\n\t\tNull Attributes Found: {0}"\
                    "\n\t\tFeatures Updated: {1}"\
                    "\n\tPopulate Fcode:"\
                    "\n\t\tFeatures Updated: {2}"\
                    "\n\tCalculate Metrics:"\
                    "\n\t\tFeatures Updated: {3}"\
                    "\n\tUpdate UFI:"\
                    "\n\t\tFeatures Updated: {4}"\
                    "\n\tExplode Multipart Features:"\
                    "\n\t\tMultiparts Found: {5}"\
                    "\n\t\tFeatures Created: {6}"\
                    "\n\tDelete Identical Features:"\
                    "\n\t\tIdentical Features Found: {7}"\
                    "\n\tIntegrate Features:"\
                    "\n\t\tFeatures Processed: {8}"\
                    .format(output(default), output(null), output(fcode), output(calc), output(ufi),\
                            output(multi), output(explode), output(ident), output(integrate))
        write(report)
    
    def report_function_status(self):
        func_status = self.function_used
        function_report = "\n\n\nProcesses:"\
                    "\n\tRepair Null Geometry: {0}"\
                    "\n\tPopulate Default Values: {1}"\
                    "\n\tPopulate Fcode: {2}"\
                    "\n\tCalculate Metrics: {3}"\
                    "\n\tUpdate UFI: {4}"\
                    "\n\tExplode Multipart Features: {5}"\
                    "\n\tDelete Identical Features: {6}"\
                    "\n\tIntegrate Features: {7}"\
                    "\n\t\tHydrography: {8}"\
                    "\n\t\tTransportationGround: {9}"\
                    "\n\t\tUtilityInfrastructure: {10}\n\n"\
                    .format(func_status(self.repair_nulls),func_status(self.pop_default), func_status(self.pop_fcode), func_status(self.calc_metric), func_status(self.ufi), func_status(self.explode),\
                            func_status(self.delete_ident), func_status(self.integrate), func_status(self.integrate_hydro), func_status(self.integrate_trans), func_status(self.integrate_util))
        write(function_report)

#----------------------------------------------------------------
#* Helper Functions
def get_featureclasses(skip=[], fc_list=[]):
    list_fcs = ap.ListFeatureClasses
    if not fc_list:
        fc_list = sorted(fc for fc in list_fcs() if fc not in skip)
    elif skip:
        for featureclass in skip:
            fc_list.remove(featureclass)
    return fc_list

def get_featureclass_fields(featureclass):
    desc = ap.Describe
    fields_set = set(field.name for field in desc(featureclass).fields)
    return fields_set

def get_field_type_map(featureclass):
    desc = ap.Describe
    field_type_map = {field.name: field.type for field in desc(featureclass).fields}
    return field_type_map


def get_count(featureclass):
    search = ap.da.SearchCursor
    with search(featureclass, ["OID@"]) as cursor:
        count = sum(1 for row in cursor)
    return count

def get_geometry_type(featureclass):
    desc = ap.Describe
    feature_geometry_type = desc(featureclass).ShapeType
    return feature_geometry_type

def validate_featureclass_presence(featureclass):
    fc_set = get_featureclasses()
    write("Looking for {0} in Dataset".format(featureclass))
    if featureclass in fc_set:
        write("Featureclass found")
        return True
    else:
        write("Featureclass missing. AAAAHHH!!!!")
        return False

def get_default_values(featureclass):
    list_subtypes = ap.da.ListSubtypes
    fc_subtypes_dict = list_subtypes(featureclass)
    fcsubtypes_list = fc_subtypes_dict.keys()
    exclusion_set = {'F_CODE', 'FCSUBTYPE', 'Version'}

    default_values_dict = {subtype: \
                            {field: fc_subtypes_dict[subtype]['FieldValues'][field][0] \
                            for field in fc_subtypes_dict[subtype]['FieldValues'].keys() \
                                if fc_subtypes_dict[subtype]['FieldValues'][field][0] != None}\
                            for subtype in fcsubtypes_list}
    simple_default_values_dict = {}
    for subtype in fcsubtypes_list:
        for field in default_values_dict[subtype].keys():
            if field in exclusion_set:
                continue
            simple_default_values_dict.setdefault(field, default_values_dict[subtype][field])
    

    return simple_default_values_dict

def get_fcsubtype_fcode_values(featureclass):
    list_subtypes = ap.da.ListSubtypes

    fcsubtypes_dict = list_subtypes(featureclass)

    fcsubtype_fcode_dict = {subtype: fcsubtypes_dict[subtype]['FieldValues']['F_CODE'][0] \
                            for subtype in fcsubtypes_dict.keys()}
    
    return fcsubtype_fcode_dict

def check_set_spatial_reference(grid_layer, tds_data): #uwu
    desc = ap.Describe
    apply_projection = ap.DefineProjection_management
    write("Checking Spatial Reference...")
    dvof_desc = desc(grid_layer)
    tds_desc = desc(tds_data)
    grid_sr = dvof_desc.spatialReference
    tds_sr = tds_desc.spatialReference

    if grid_sr.name != tds_sr.name:
        write("Applying {} projection to Grid Layer...".format(tds_sr.name))
        apply_projection(grid_layer, tds_sr)
    else:
        write("Grid Layer and TDS projection match confirmed: {}".format(tds_sr.name))

def runtime(start): # Time a process or code block
    # Add a start time variable and use this function when you want that timer to end
    # Returns string of formatted elapsed time between start and execution of this function
    #from datetime import datetime as dt
    #start = dt.now()
    now = dt.now
    time_delta = (now() - start).total_seconds()
    h = int(time_delta/(60*60))
    m = int((time_delta%(60*60))/60)
    s = time_delta%60.
    #time_elapsed = "{}:{:>02}:{:>05.4f}".format(h, m, s) # 00:00:00.0000
    if h == 1:
        hour_grammar = "hour"
    else:
        hour_grammar = "hours"
    if m == 1:
        minute_grammar = "minute"
    else:
        minute_grammar = "minutes"
    if h and m and s:
            time_elapsed = "{} {} {} {} and {} seconds".format(h, hour_grammar, m, minute_grammar, round(s))
    elif not h and m and s:
        time_elapsed = "{} {} and {:.1f} seconds".format(m, minute_grammar, s)
    elif not h and not m and s:
        time_elapsed = "{:.3f} seconds".format(s)
    else:
        time_elapsed = 0
    return time_elapsed

#----------------------------------------------------------------
#* Primary Functions

#** Preliminary
def disable_editor_tracking(gdb_name): # Automatically disables editor tracking for each feature class that doesn't already have it disabled
    now = dt.now
    disable_editor = ap.DisableEditorTracking_management
    greentext = ap.AddWarning
    desc = ap.Describe

    disable_start = now()
    
    featureclass_set = get_featureclasses()
    write("Disabling Editor Tracking for {0}".format(gdb_name))
    firstl = False
    for fc in featureclass_set:
        fc_desc = desc(fc)
        if fc_desc.editorTrackingEnabled:
            try:
                disable_editor(fc)
                if not firstl:
                    write("\n")
                    firstl = True
                write("{0} - Disabled".format(fc))
            except:
                greentext("Error disabling editor tracking for {0}. Please check the data manually and try again.".format(fc))
                pass
    if firstl:
        write("Editor Tracking has been disabled.")
    else:
        write("Editor Tracking has already been disabled.")
    write("Time to disable Editor Tracking: {0}".format(runtime(disable_start)))

def grid_chungus(cores): #Create fishnet grid to partition large datasets into chunks so our potatoes have a chance of doing geospatial processing
    now = dt.now
    desc = ap.Describe
    make_fishnet = ap.CreateFishnet_management
    make_layer = ap.MakeFeatureLayer_management
    chungus_start = now()
    tds = ap.env.workspace
    # Set the Arc environment
    ap.env.extent = tds
    extent_template = tds
    mem_fc = "in_memory\\the_grid"
    origin_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMin) # ESRI docs lie and say CreateFishnet uses a Point object like extent.lowerLeft
    y_axis_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperLeft
    corner_coord = '{0} {1}'.format(ap.env.extent.XMax, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperRight
    # y_axis──>┌──┐<──corner
    # origin──>└──┘
    write("Constructing fishnet over dataset for partitioning data into chunks.\nThis helps our potatoes handle the large scale geospatial databases we have to process.")
    #### Vertex Density Check to determine if a 2x2, 3x3, or larger should be used for really big honkin data
    #ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", "", "POLYGON")
    make_fishnet(mem_fc, origin_coord, y_axis_coord, "0", "0", cores, cores, corner_coord=corner_coord, labels="NO_LABELS",template=extent_template, geometry_type="POLYGON")
    write("Spatial data partitions constructed in {0}".format(runtime(chungus_start)))
    check_set_spatial_reference(mem_fc, tds)
    grid_layer = make_layer(mem_fc, "temp_grid_layer")
    grid_sr = desc(grid_layer).spatialReference.name
    write("\nGrid Layer Created with {} Spatial Reference\n".format(grid_sr))
    return grid_layer

def make_scaled_layers(featureclass_list, scale):
    make_layer = ap.MakeFeatureLayer_management
    delim = ap.AddFieldDelimiters

    layers_dict = {}

    for featureclass in featureclass_list:
        write("\nScaling {}".format(featureclass))
        try:
            scale_query = """{0} >= {1}""".format(delim(featureclass, "ZI026_CTUU"), scale)
            layer_name = "{}_layer".format(featureclass)
            fc_layer = make_layer(featureclass, layer_name, scale_query)
            fc_count = get_count(fc_layer)
            if fc_count > 0:
                write("\tFeatures in scale: {}".format(fc_count))
                layers_dict.setdefault(featureclass, fc_layer)
            else:
                write("\tNo Features Present. Skipping...")
                continue
        except:
            write("\tSkipping {} Features".format(featureclass))
            continue
    
    return layers_dict

def delete_scaled_layers(layers_dict):
    arc_del = ap.Delete_management
    for featureclass in layers_dict.keys():
        arc_del(layers_dict[featureclass])
    del layers_dict
#----------------------------------------------------------------
#** Conditioning Functions
def populate_nulls_with_defaults(featureclass):
    update = ap.da.UpdateCursor
    default_values_dict = get_default_values(featureclass)
    # write(default_values_dict)
    fields = default_values_dict.keys()
    null_counter = 0
    updated_feature_counter = 0
    row_updated = False

    with update(featureclass, fields) as cursor:
        for row in cursor:
            for index, value in enumerate(fields):
                if row[index] is None:
                    row[index] = default_values_dict[value]
                    null_counter += 1
                    updated_feature_counter += 1
                    row_updated = True
            if row_updated:
                cursor.updateRow(row)
                row_updated = False
    
    return (null_counter, updated_feature_counter)


def populate_fcodes(featureclass):
    update = ap.da.UpdateCursor

    fcsubtype_fcode_dict = get_fcsubtype_fcode_values(featureclass)
    fields = ['FCSUBTYPE', 'F_CODE']
    features_updated = 0

    with update(featureclass, fields) as cursor:
        for row in cursor:
            try:
                proper_fcode = fcsubtype_fcode_dict[row[0]]
            except:
                write("FCSUBTYPE {0} does not belong in {1} Featureclass. Please Correct in data.".format(row[0], featureclass))
                continue
            if row[1] != proper_fcode:
                row[1] = proper_fcode
                features_updated += 1
                cursor.updateRow(row)
    return features_updated

def calculate_metrics(featureclass, scale_where_clause=None):
    # Set tool start time
    # now = dt.now
    # tool_start = now()

    # Set Variables
    # tool_name = "Calculate Metrics"
    curve_fields = ['LZN', 'SHAPE@']
    surface_fields = ['ARA', 'SHAPE@']
    feature_update_count = 0
    update = ap.da.UpdateCursor

    # Check ShapeType of featureclass
    featureclass_geometry = get_geometry_type(featureclass)
    write("\tUpdating geometry metric for {} features.".format(featureclass_geometry))
    
    # Check for appropriate fields, 
    # if not present then skip to next featureclass
    if featureclass_geometry == 'Polyline':
        if curve_fields[0] not in get_featureclass_fields(featureclass):
            return 0
        else:
            with update(featureclass, curve_fields, scale_where_clause) as cursor:
                for row in cursor:
                    row[0] = round(row[-1].getLength('PRESERVE_SHAPE'))
                    feature_update_count+=1
                    cursor.updateRow(row)
    elif featureclass_geometry == 'Polygon':
        if surface_fields[0] not in get_featureclass_fields(featureclass):
            return 0
        else:
            with update(featureclass, surface_fields, scale_where_clause) as cursor:
                for row in cursor:
                    row[0] = round(row[-1].getArea('PRESERVE_SHAPE'))
                    feature_update_count+=1
                    cursor.updateRow(row)
    # greentext("{0} finished in {1}".format(tool_name, runtime(tool_start)))
    return feature_update_count


def update_ufi(featureclass):
    update = ap.da.UpdateCursor

    ufi_total = 0

    with update(featureclass, ['UFI']) as cursor:
        for row in cursor:
            row[0] = str(uuid.uuid4())
            ufi_total+=1
            cursor.updateRow(row)
    
    return ufi_total


def integrate_theme(theme_type, grid_layer=None, scale=-999999):
    now = dt.now
    select_by_att = ap.SelectLayerByAttribute_management
    select_by_loc = ap.SelectLayerByLocation_management
    greentext = ap.AddWarning
    repair = ap.RepairGeometry_management
    delim = ap.AddFieldDelimiters
    integrate = ap.Integrate_management
    arc_del = ap.Delete_management
    desc = ap.Describe

    # timing start
    run_start = now()

    # Set up variables
    
    theme_point_layer = "".join([theme_type,"Pnt_layer"])
    theme_curve_layer = "".join([theme_type,"Crv_layer"])
    theme_surface_layer = "".join([theme_type,"Srf_layer"])

    # track features integrated
    features_processed_count = 0

    # Create layers for integration
    # Validate that layers are sucessfully made and features present
    if not create_thematic_layers(theme_type, scale):
        write("One or more expected Featureclasses not present...")
        return features_processed_count
    
    # Store total feature counts
    theme_point_total = get_count(theme_point_layer)
    theme_curve_total = get_count(theme_curve_layer)
    theme_surface_total = get_count(theme_surface_layer)

    write("Total features for {}:\n".format(theme_type))
    write("\t\tPoint Features: {0}\n\t\tLine Features: {1}\n\t\tSurface Features: {2}\n".format(theme_point_total, theme_curve_total, theme_surface_total))

    # Check for grid layer
    # if grid layer not present
    # integrate over entire database
    # else 
    # divide features by tile and integrate over each tile

    if not grid_layer:
        write("They've hacked the grid! RUN!!!")
        return features_processed_count
    else:
        search = ap.da.SearchCursor

        grid_oid_field = desc(grid_layer).OIDFieldName
        with search(grid_layer, [grid_oid_field]) as cursor:
            grid_tiles = [row[0] for row in cursor]
        
        write("Using Partition Grid...")
        # integrate each tile separately to conserve memory
        for tile in grid_tiles:
            # select tile in grid layer
            tile_start = now()
            tile_query = "{0} = {1}".format(delim(grid_layer, grid_oid_field), tile)
            select_by_att(grid_layer, "NEW_SELECTION", tile_query)

            # Make Selections based on location in tile
            select_by_loc(theme_point_layer, "INTERSECT", grid_layer, "", "NEW_SELECTION")
            select_by_loc(theme_curve_layer, "INTERSECT", grid_layer, "", "NEW_SELECTION")
            select_by_loc(theme_surface_layer, "INTERSECT", grid_layer, "", "NEW_SELECTION")

            # Get feature counts for current tile
            theme_point_count = get_count(theme_point_layer)
            theme_curve_count = get_count(theme_curve_layer)
            theme_surface_count = get_count(theme_surface_layer)
            write("\nFeatures intersecting Partiton {}:".format(tile))
            write("\t{0} Point features: {1}\n\t{0} Line features: {2}\n\t{0} Surface features:{3}\n".format(theme_type, theme_point_count, theme_curve_count, theme_surface_count))
            
            if not (theme_point_count + theme_curve_count + theme_surface_count):
                write("No Features present in this grid. Skipping....")
                # Clear selections before next loop
                select_by_att(grid_layer, "CLEAR_SELECTION")
                select_by_att(theme_point_layer, "CLEAR_SELECTION")
                select_by_att(theme_curve_layer, "CLEAR_SELECTION")
                select_by_att(theme_surface_layer, "CLEAR_SELECTION")
                greentext("\t\tTile {0} integrated in {1}".format(tile, runtime(tile_start)))
                continue
            if (theme_surface_count * theme_curve_count):
                write("\tIntegrating lines to surfaces...")
                integrate_mixed_geometries(theme_surface_layer,theme_curve_layer)
                repair(theme_surface_layer, "DELETE_NULL")
                repair(theme_curve_layer, "DELETE_NULL")
                features_processed_count += (theme_surface_count + theme_curve_count)
            if (theme_point_count * theme_curve_count):
                write("\tIntegrating points to lines...")
                integrate_mixed_geometries(theme_curve_layer, theme_point_layer)
                repair(theme_point_layer, "DELETE_NULL")
                repair(theme_curve_layer, "DELETE_NULL")
                features_processed_count += (theme_curve_count + theme_point_count)
            if (not (theme_point_count + theme_surface_count) and theme_curve_count):
                write("\t\tNo points or surfaces detected, only integrating curves")
                integrate(theme_curve_layer, "0.01 Meters")
                repair(theme_curve_layer, "DELETE_NULL")
                features_processed_count += theme_curve_count
            
            # Clear selections before next loop
            select_by_att(grid_layer, "CLEAR_SELECTION")
            select_by_att(theme_point_layer, "CLEAR_SELECTION")
            select_by_att(theme_curve_layer, "CLEAR_SELECTION")
            select_by_att(theme_surface_layer, "CLEAR_SELECTION")
            greentext("\t\tTile {0} integrated in {1}".format(tile, runtime(tile_start)))

        arc_del(theme_point_layer)
        arc_del(theme_curve_layer)
        arc_del(theme_surface_layer)
        greentext("\t{0} finished in {1}".format(" ".join(["Integrate", theme_type]), runtime(run_start)))
        return features_processed_count

# Creates working layers of a single theme in TDS data
def create_thematic_layers(theme, scale=-999999):
    make_layer = ap.MakeFeatureLayer_management
    repair = ap.RepairGeometry_management
    delim = ap.AddFieldDelimiters

    # Saftey Check: 
    # Make sure each of the feature classes in the theme are present in the working environment
    theme_point_fc = "".join([theme,"Pnt"])
    theme_curve_fc = "".join([theme,"Crv"])
    theme_surface_fc = "".join([theme,"Srf"])
    if not validate_featureclass_presence(theme_point_fc) or \
        not validate_featureclass_presence(theme_curve_fc) or \
        not validate_featureclass_presence(theme_surface_fc):
        return False

    # create scale query
    scale_query = """{0} >= {1}""".format(delim(theme_curve_fc, "ZI026_CTUU"), scale)
    # Create layers based on scale and (optional) feature type limitations
    theme_point_layer = "".join([theme,"Pnt_layer"])
    theme_curve_layer = "".join([theme,"Crv_layer"])
    theme_surface_layer = "".join([theme,"Srf_layer"])

    make_layer(theme_point_fc, theme_point_layer, scale_query)
    make_layer(theme_curve_fc, theme_curve_layer, scale_query)
    make_layer(theme_surface_fc, theme_surface_layer, scale_query)

    # Perform a preemptive RepairGeometry on curves and surfaces
    repair(theme_curve_layer, "DELETE_NULL")
    repair(theme_surface_layer, "DELETE_NULL")
    # Return True to validate successful layer creation
    return True

# Nat's logic of using Snap_edits to adjust features 
# then Integrate to create vertex points at intersections.
# This version is a generalized one from the methods in Finsihing Tool 9.8.8
def integrate_mixed_geometries(rank_1_features, rank_2_features):
    # use Snap to grab unsnapped features that are just outside of the integrate tolerance
    snap = ap.Snap_edit
    integrate = ap.Integrate_management
    snap_tolerance = "0.05 METERS"
    end_snap_environment = [rank_1_features, "END", snap_tolerance]
    vertex_snap_environment = [rank_1_features, "VERTEX", snap_tolerance]
    edge_snap_environment = [rank_1_features, "EDGE", snap_tolerance]

    if get_geometry_type(rank_1_features) == "Polyline":
        snapping_environment = [end_snap_environment, vertex_snap_environment, edge_snap_environment]
    else:
        snapping_environment = [vertex_snap_environment, edge_snap_environment]


    snap(rank_2_features, snapping_environment)

    # Integrate features based on ranking
    integrate_rankings = [[rank_1_features, 1], [rank_2_features, 2]]
    # cluster_tolerance = "0.01 METERS" # previously used, not recommended by ESRI
    integrate(integrate_rankings)

def explode_multipart_features_v2(featureclass):
    # Arcpy tools to use
    search = ap.da.SearchCursor
    desc = ap.Describe
    add_delim = ap.AddFieldDelimiters
    make_layer = ap.MakeFeatureLayer_management
    copy_features = ap.CopyFeatures_management
    multipart_to_singlepart = ap.MultipartToSinglepart_management
    delete_features = ap.DeleteFeatures_management
    append_features = ap.Append_management
    arc_del = ap.Delete_management
    greentext = ap.AddWarning
    repair = ap.RepairGeometry_management   #! Possible delete if using attribute conditioners

    now = dt.now

    # Temp locations for explodeing multiparts
    temp_multipart_fc = "in_memory//{}_multiparts".format(featureclass)
    temp_singlepart_fc = "in_memory//{}_singleparts".format(featureclass)
    multipart_layer_name = "{}_multipart_layer".format(featureclass)
    # Tracking data for finding multiparts
    multipart_oid_list = []
    complex_feature_count = 0

    # write("\n***Searching for multiparts in {}***".format(featureclass))
    start_explode = now()

    # Fields for finding multiparts
    check_fields = ["OID@", "SHAPE@"]

    # Find true multiparts
    with search(featureclass, check_fields) as scursor:
        for feature in scursor:
            shape = feature[-1]

            # Double check for lingering nulls
            if shape is None:
                # Leave a message
                continue
            elif shape.isMultipart:
                if shape.partCount > 1:
                    # True multipart
                    multipart_oid_list.append(feature[0])
                else:
                    # Mislabelled complex feature
                    complex_feature_count += 1
    
    # if the check list is empty, then move on otherwise continue with explode
    if not multipart_oid_list:
        write("\tNo multiparts found in {}".format(featureclass))
        return (0, 0)
    
    #* if it moves past this point then there are multiparts in the featureclass

    # Copy identified features to temp featureclass
    oid_field_name = desc(featureclass).OIDFieldName
    if len(multipart_oid_list) > 1:
        oid_query = """{0} in {1}""".format(add_delim(featureclass,oid_field_name), tuple(multipart_oid_list))
    else:
        oid_query = """{0} = {1}""".format(add_delim(featureclass, oid_field_name), multipart_oid_list[0])

    multipart_layer = make_layer(featureclass, multipart_layer_name, oid_query)
    copy_features(multipart_layer, temp_multipart_fc)

    # Get the count of all multipart features
    multipart_feature_count = get_count(multipart_layer)
    write("\t{} Multiparts found\n\tExploding....".format(multipart_feature_count))
    
    # Explode the temp multipart featureclass
    multipart_to_singlepart(temp_multipart_fc, temp_singlepart_fc)

    #? Apply attribution conditioning??
    repair(temp_singlepart_fc, "DELETE_NULL")

    # Get the count of all single part features
    singlepart_feature_count = get_count(temp_singlepart_fc)
    write("\t{} Singlepart features from explosion".format(singlepart_feature_count))

    # Delete Multipart Features from original featureclass
    #? Use the multipart layer from above???
    write("\tRemoving original multipart features.")
    delete_features(multipart_layer)

    #? Maybe get multipart_layer count as a check
    # post_delete_count = get_count(multipart_layer)
    # write("\tDebug: Checking count after delete: {}".format(post_delete_count))

    # Copy features from temp Singlepart featureclass into original featureclass
    write("\tCopying in correct features...")
    append_features(temp_singlepart_fc, featureclass, "NO_TEST")

    # Clean up the memory space
    arc_del(temp_multipart_fc)
    arc_del(temp_singlepart_fc)
    arc_del(multipart_layer)

    # greentext("{0} {1} multiparts exploded into {2} features in {3}".format(multipart_feature_count, featureclass, singlepart_feature_count, runtime(start_explode)))
    return (multipart_feature_count, singlepart_feature_count)

def delete_identical_features(featureclass):
    desc = ap.Describe
    find_identical = ap.FindIdentical_management
    delete_identical = ap.DeleteIdentical_management
    arc_del = ap.Delete_management
    # Check for identical features
    find_identical_table = "in_memory//{}_FI".format(featureclass)
    fc_desc = desc(featureclass)
    oid_field_name = fc_desc.OIDFieldName
    exclude_fields = set([oid_field_name, 'LZN', 'ARA', 'UFI', 'GlobalID', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date', 'SHAPE_Length', 'SHAPE_Area'])
    check_fields = [field.name for field in fc_desc.fields if field.name not in exclude_fields]

    # write("\nChecking for identical features in {}".format(featureclass))
    # write("\tFields to compare: {}".format(check_fields))

    find_identical(featureclass, find_identical_table, check_fields, output_record_option="ONLY_DUPLICATES")

    identical_count = get_count(find_identical_table)

    write("\t{} Identical features found".format(identical_count))
    arc_del(find_identical_table)

    # if identicals found: 
    # use delete identical
    if identical_count:
        write("\tDeleting identical features...")
        delete_identical(featureclass, check_fields)
    
    # double check
    # find_identical(featureclass, find_identical_table, check_fields, output_record_option="ONLY_DUPLICATES")
    # identical_count = get_count(find_identical_table)
    # write("\tVerifying Identical Features Deleted\n\t{} Identical Features Found".format(identical_count))
    # arc_del(find_identical_table)
    # if identical_count:
        # write("\tDeleting remaining identical features...")
        # delete_identical(featureclass, check_fields)

    return identical_count

#----------------------------------------------------------------
def main(*argv):
    now = dt.now
    greentext = ap.AddWarning
    
    # Get Parameters
    tds = argv[0]
    scale = int(argv[1])
    cores = str(int(sqrt(int(argv[2]))))
    options = set([opt.strip("\'") for opt in argv[3].split(';')])
    primary_functions = set([func.strip("\'") for func in argv[4].split(';')])
    
    process = ProcessReport(primary_functions)
    
    # Set Environment
    ap.env.workspace = tds
    write("Options: {0}\nProcesses: {1}".format(options, primary_functions))
    process.report_function_status()
    
    # Options: 
    #   Disable Editor Tracking
    #   Skip Buildings
    if "Disable Editor Tracking" in options:
        gdb_name = os.path.split(os.path.dirname(tds))[-1]
        disable_editor_tracking(gdb_name)
    
    if "Skip Buildings" in options:
        skip_fc_list = ["StructurePnt", "StructureCrv", "StructureSrf"]
        featureclass_list = get_featureclasses(skip_fc_list)
    else:
        featureclass_list = get_featureclasses()
    
    # Create Scaled Layers
    write("\nScaling data: CTUU >= {}".format(scale))
    scaled_layers = make_scaled_layers(featureclass_list, scale)


    # Primary Functions:
    #   Repair Null Geometry
    #   Populate Default Values
    #   Populate F Codes
    #   Calculate Metrics
    #   Update UFI
    #   Explode Multiparts
    #   Delete Identical Features
    write("\n***Beginning Data Conditioning***")
    primary_functions_start = now()
    
    for featureclass in sorted(scaled_layers.keys()):
        fc_start = now()
        fc_layer = scaled_layers[featureclass]
        write("\nConditioning {} features".format(featureclass))
        if process.repair_nulls:
            repair = ap.RepairGeometry_management
            repair(fc_layer, "DELETE_NULL")
            write("\tIntial Repair complete")
        
        if process.explode:
            explode_counts = explode_multipart_features_v2(fc_layer)
            process.add_explode_count(explode_counts)
        
        if process.pop_default:
            null_results = populate_nulls_with_defaults(fc_layer)
            process.add_default_count(null_results)
            write("\t{0} nulls populated in {1} features.".format(null_results[0], null_results[1]))
        
        if process.pop_fcode:
            fcodes_populated = populate_fcodes(fc_layer)
            process.add_fcode_count(fcodes_populated)
            write("\t{0} F_CODEs populated.".format(fcodes_populated))
        
        if process.calc_metric:
            metrics_updated = calculate_metrics(fc_layer)
            process.add_calc_count(metrics_updated)
            write("\t{} feature metrics updated.".format(metrics_updated))
        
        if process.ufi:
            ufis_updated = update_ufi(fc_layer)
            process.add_ufi_count(ufis_updated)
            write("\t{0} UFIs updated.".format(ufis_updated))
        
        if process.delete_ident:
            write("\tScanning for Identical Features...")
            identical_count = delete_identical_features(fc_layer)
            process.add_delete_ident_count(identical_count)
        
        greentext("{0} conditioning finished in {1}".format(fc_layer, runtime(fc_start)))
        write("_____________________________________")
    greentext("\n\nDatabase Primary Conditioning completed in {}".format(runtime(primary_functions_start)))

    # Clean up memory
    write("\nClearing working memory....\n")
    delete_scaled_layers(scaled_layers)
    
    # Integrate Themes:
    #    Integrate Hydrography
    #    Integrate TransportationGround
    #    Integrate UtilityInformation
    if process.integrate:
        integrate_start = now()
        integrate_themes = []
        if process.integrate_hydro:
            integrate_themes.append("Hydrography")
        if process.integrate_trans:
            integrate_themes.append("TransportationGround")
        if process.integrate_util:
            integrate_themes.append("UtilityInfrastructure")
        write("\nPreparing to Integrate: {}".format(integrate_themes))
        grid_layer = grid_chungus(cores)
        for theme in integrate_themes:
            write("\n***Integrating {} Features***".format(theme))
            integrate_count = integrate_theme(theme, grid_layer, scale)
            process.add_integrate_count(integrate_count)
        greentext("\nTotal Integration completed in {}".format(runtime(integrate_start)))

    
    # Report Processing Totals
    process.report_totals()


if __name__=='__main__':
    ap.env.overwriteOutput = True
    ap.env.XYResolution = "0.00000000001 DecimalDegrees"
    ap.env.XYTolerance = "0.000000008983153 DecimalDegrees"
    argv = tuple(ap.GetParameterAsText(i)
            for i in range(ap.GetArgumentCount()))
    start = dt.now()
    main(*argv)
    write(dt.now() - start)