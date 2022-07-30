
#-----------------------------------
def repair_and_clean(name_list):
	write("Repairing {0} and {1} features after integration".format(name_list[1], name_list[2]))
	ap.RepairGeometry_management(name_list[4], "DELETE_NULL")
	ap.RepairGeometry_management(name_list[5], "DELETE_NULL")
	write("Clearing process cache")
	clear_cache([name_list[3], name_list[4], name_list[5]])

#-----------------------------------
def integrate_hydro(grid_lyr):
	hydro_list = ['HydrographyPnt', 'HydrographyCrv', 'HydrographySrf', 'hydro_pnt', 'hydro_crv', 'hydro_srf']
	hydro_pnt = hydro_list[3]
	hydro_crv = hydro_list[4]
	hydro_srf = hydro_list[5]
	hfeat_count = 0
	make_integrate_layers(hydro_list)

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
			select = "OID = {}".format(row[0])
			select_by_att(grid_lyr, "NEW_SELECTION", select)
			select_by_loc(hydro_pnt, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(hydro_crv, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(hydro_srf, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			pnt_count = get_count(hydro_pnt)
			crv_count = get_count(hydro_crv)
			srf_count = get_count(hydro_srf)
			hfeat_count = hfeat_count + pnt_count + crv_count + srf_count
			write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(pnt_count, hydro_list[0], crv_count, hydro_list[1], srf_count, hydro_list[2], row[0]))
			if crv_count > 0 and srf_count > 0:
				snap_lines_to_srf(hydro_crv, hydro_srf)
			if pnt_count > 0 and crv_count > 0:
				snap_points_to_lines(hydro_pnt, hydro_crv)
			if pnt_count == 0 and srf_count == 0 and crv_count > 0:
				ap.Integrate_management(hydro_crv, "0.02 Meters")

	repair_and_clean(hydro_list)
	return hfeat_count

#-----------------------------------
def integrate_trans(grid_lyr):
	trans_list = ['TransportationGroundPnt', 'TransportationGroundCrv', 'TransportationGroundSrf', 'trans_pnt', 'trans_crv', 'trans_srf']
	trans_pnt = trans_list[3]
	trans_crv = trans_list[4]
	trans_srf = trans_list[5]
	tfeat_count = 0
	make_integrate_layers(trans_list)

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
			select = "OID = {}".format(row[0])
			select_by_att(grid_lyr, "NEW_SELECTION", select)
			select_by_loc(trans_pnt, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(trans_crv, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(trans_srf, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			pnt_count = get_count(trans_pnt)
			crv_count = get_count(trans_crv)
			srf_count = get_count(trans_srf)
			tfeat_count = tfeat_count + pnt_count + crv_count + srf_count
			write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(pnt_count, trans_list[0], crv_count, trans_list[1], srf_count, trans_list[2], row[0]))
			if crv_count > 0 and srf_count > 0:
				snap_lines_to_srf(trans_crv, trans_srf)
			if pnt_count > 0 and crv_count > 0:
				snap_points_to_lines(trans_pnt, trans_crv)
			if pnt_count == 0 and srf_count == 0 and crv_count > 0:
				ap.Integrate_management(trans_crv, "0.02 Meters")

	repair_and_clean(trans_list)
	return tfeat_count

#-----------------------------------
def integrate_util(grid_lyr):
	util_list = ['UtilityInfrastructurePnt', 'UtilityInfrastructureCrv', 'UtilityInfrastructureSrf', 'util_pnt', 'util_crv', 'util_srf']
	util_pnt = util_list[3]
	util_crv = util_list[4]
	util_srf = util_list[5]
	ufeat_count = 0
	make_integrate_layers(util_list)

	write("Partitioning large feature class into chunks for processing")
	with ap.da.SearchCursor(grid_lyr, ['OID@']) as scursor:
		for row in scursor:
			select = "OID = {}".format(row[0])
			select_by_att(grid_lyr, "NEW_SELECTION", select)
			select_by_loc(util_pnt, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(util_crv, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			select_by_loc(util_srf, "INTERSECT", grid_lyr, "", "NEW_SELECTION")
			pnt_count = get_count(util_pnt)
			crv_count = get_count(util_crv)
			srf_count = get_count(util_srf)
			ufeat_count = ufeat_count + pnt_count + crv_count + srf_count
			write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(pnt_count, util_list[0], crv_count, util_list[1], srf_count, util_list[2], row[0]))
			if crv_count > 0 and srf_count > 0:
				snap_lines_to_srf(util_crv, util_srf)
			if pnt_count > 0 and crv_count > 0:
				snap_points_to_lines(util_pnt, util_crv)
			if pnt_count == 0 and srf_count == 0 and crv_count > 0:
				ap.Integrate_management(util_crv, "0.02 Meters")

	repair_and_clean(util_list)
	return ufeat_count



#----------------------------------------------------------------------
#Create Fishnet
mem_fc = "in_memory\\the_grid"
grid_lyr = "grid_lyr"
origin_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMin) # ESRI docs lie and say CreateFishnet uses a Point object like extent.lowerLeft
y_axis_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperLeft
corner_coord = '{0} {1}'.format(ap.env.extent.XMax, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperRight
# y_axis──>┌──┐<──corner
# origin──>└──┘
write("Constructing fishnet over dataset for partitioning data into chunks.\nThis helps our potatoes handle the large scale geospatial databases we have to process.")
#### Vertex Density Check to determine if a 2x2, 3x3, or larger should be used for really big honkin data
ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", "", "POLYGON")
make_lyr(mem_fc, grid_lyr)


#-----------------------------------
if bool_dict[tool_names.hydro]:
	#~~~~~ Royal Decree Variables ~~~~~
	hfeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		hfeat_count = integrate_hydro(grid_lyr)
	except ap.ExecuteError:
		writeresults(tool_names.hydro)


#-----------------------------------
if bool_dict[tool_names.trans]:
	#~~~~~ Royal Decree Variables ~~~~~
	tfeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		tfeat_count = integrate_trans(grid_lyr)
	except ap.ExecuteError:
		writeresults(tool_names.trans)


#-----------------------------------
if bool_dict[tool_names.util]:
	#~~~~~ Royal Decree Variables ~~~~~
	ufeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		ufeat_count = integrate_util(grid_lyr)
	except ap.ExecuteError:
		writeresults(tool_names.util)



"""
MetadataSrf removed
ResourceSrf removed
Loaded 53 of 55 TDSv7.1 feature classes in 0:00:2.2050
Checking for CACI custom schema
Regular TDS schema identified in 0:00:0.8120
Recalculating feature class extents finished in 0:00:26.6520
Constructing fishnet over dataset for partitioning data into chunks.
This helps our potatoes handle the large scale geospatial databases we have to process.

--- Integrate Hydrography Features ---

Making HydrographyPnt, HydrographyCrv, and HydrographySrf feature layers
Repairing HydrographyCrv lines and HydrographySrf polygons before Integration
Partitioning large feature class into chunks for processing
Integrating 0 HydrographyPnt features,
            0 HydrographyCrv features, and
            71 HydrographySrf features in partition 1...
Integrating 0 HydrographyPnt features,
            0 HydrographyCrv features, and
            1 HydrographySrf features in partition 2...
Integrating 25714 HydrographyPnt features,
            2835 HydrographyCrv features, and
            1571 HydrographySrf features in partition 3...
Integrating 76 HydrographyPnt features,
            188 HydrographyCrv features, and
            146 HydrographySrf features in partition 4...
Repairing HydrographyCrv and HydrographySrf features after integration
Clearing process cache
Integrate Hydrography Features finished in 0:03:18.2480

--- Integrate Transportation Features ---

Making TransportationGroundPnt, TransportationGroundCrv, and TransportationGroundSrf feature layers
Repairing TransportationGroundCrv lines and TransportationGroundSrf polygons before Integration
Partitioning large feature class into chunks for processing
Integrating 167 TransportationGroundPnt features,
            4631 TransportationGroundCrv features, and
            235 TransportationGroundSrf features in partition 4...
Repairing TransportationGroundCrv and TransportationGroundSrf features after integration
Clearing process cache
Integrate Transportation Features finished in 0:01:32.2480

--- Integrate Utility Features ---

Making UtilityInfrastructurePnt, UtilityInfrastructureCrv, and UtilityInfrastructureSrf feature layers
Repairing UtilityInfrastructureCrv lines and UtilityInfrastructureSrf polygons before Integration
Partitioning large feature class into chunks for processing
Integrating 1709 UtilityInfrastructurePnt features,
            131 UtilityInfrastructureCrv features, and
            31 UtilityInfrastructureSrf features in partition 4...
Repairing UtilityInfrastructureCrv and UtilityInfrastructureSrf features after integration
Clearing process cache
Integrate Utility Features finished in 0:00:20.6170
"""
