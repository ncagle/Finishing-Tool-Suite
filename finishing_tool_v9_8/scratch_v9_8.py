
MakeFeatureLayer_management as make_lyr
SelectLayerByAttribute_management as select_by_att
SelectLayerByLocation_management as select_by_loc
Delete_management as arcdel

#----------------------------------------------------------------------



def fc_exists(fc, tool_name):
	if ap.Exists(fc):
		return True
	else:
		write("{0} feature class missing.\n{1} will skip steps involving {0} .".format(fc, tool_name))
		return False


''''''''' Building in BUA Descaler '''''''''
# Descales buildings within BUAs that don't have important FFNs, have a height < 46m, and aren't navigation landmarks
# Scales in buildings within BUAs that do have important FFNs, have a height >= 46m, or are navigation landmarks
while building:
	# Initialize task
	building_start = dt.now()
	tool_name = 'Building in BUA Descaler'
	write("\n--- {0} ---\n".format(tool_name))

	#~~~~~ Royal Decree Variables ~~~~~
	# Check that required feature classes exist
	bua_exist = fc_exists('SettlementSrf', tool_name) # Does SettlementSrf fc exist in the dataset
	building_s_exist = fc_exists('StructureSrf', tool_name) # Does StructureSrf fc exist in the dataset
	building_p_exist = fc_exists('StructurePnt', tool_name) # Does StructureSrf fc exist in the dataset
	bua_count = 0
	total_2upscale = 0
	total_2descale = 0
	if not bua_exist: # Task can't run if SettlementSrf fc is missing
		break
	if not building_s_exist and not building_p_exist: # Task can't run if both StructureSrf and StructurePnt fcs are missing. Only one is fine.
		break
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# Intra-task variables
	total_2upscale_s = 0
	total_2descale_s = 0
	total_2upscale_p = 0
	total_2descale_p = 0
	update_field = 'ZI026_CTUU'
	bua_query = "F_CODE = 'AL020' AND ZI026_CTUU >= 50000" # We don't need to worry about below scale BUAs, right?
	building_query_2upscale = "F_CODE = 'AL013' AND ZI026_CTUU < 50000"
	building_query_2descale = "F_CODE = 'AL013' AND ZI026_CTUU >= 50000"
	caci_ffn_query_2upscale = "FFN IN ({0}) OR HGT >= 46 OR LMC = 1001".format(", ".join(str(i) for i in ad.ffn_list_caci.values())) #dict_import
	caci_ffn_query_2descale = "FFN NOT IN ({0}) AND HGT < 46 AND LMC <> 1001".format(", ".join(str(i) for i in ad.ffn_list_caci.values())) #dict_import
	ffn_query_2upscale = "FFN IN ({0}) OR HGT >= 46 OR LMC = 1001".format(", ".join(str(i) for i in ad.ffn_list_all.values())) #dict_import
	ffn_query_2descale = "FFN NOT IN ({0}) AND HGT < 46 AND LMC <> 1001".format(", ".join(str(i) for i in ad.ffn_list_all.values())) #dict_import

	#----------------------------------------------------------------------

	write("Retrieved Settlement and Structure feature classes")
	# Make layer of BUAs >= 50k
	make_lyr("SettlementSrf", "buas", bua_query)
	#make_tbl("SettlementSrf", "buas", bua_query) # Cannot be used for geometry.
	write("Searching within BUAs")
	bua_count = get_count("buas")

	if not bua_count: # No BUAs to check against buildings. Wrap up task.
		write("\nNo BUAs found.")
		building_finish = dt.now()
		write("{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
		break

	if building_s_exist:
		# Adam's original important ffn list for just building points: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building surfaces matching criteria...\n")
		if caci_schema: # Snowflake Protocol
			write("CACI specific important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_caci.items())) #dict_import

			# Make layer of building surfaces < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_12.5k_within_2upscale", caci_ffn_query_2upscale)

			# Make layer of building surfaces >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_50k+_within_2descale", caci_ffn_query_2descale)

			# # Alternative solution
			# # This starts with a geometry comparison with all structure srfs against BUAs, not just buildings
			# # The current method makes a queries the buildings to limit the number of features before the geometry comparison
			# # That should be faster.
			# # Make layer of BUAs and layer of all building surfaces within those BUAs
			# make_lyr("SettlementSurfaces", "buas", bua_query)
			# make_lyr(
			# 	select_by_loc(
			# 		make_lyr("StructureSrf", "structure_s"),
			# 		"WITHIN", "buas", "", "NEW_SELECTION"),
			# 	"structure_s_within")
			# # Select building surfaces 50k and up that are within BUAs
			# # Make layer of important building surfaces to descale
			# make_lyr(
			# 	select_by_att("structure_s_within", "NEW_SELECTION", building_query_2descale),
			# 	"building_s_50k+_within_2descale", caci_ffn_query_2descale)
			# # Select below scale building surfaces that are within BUAs
			# # Make layer of important building surfaces to upscale
			# make_lyr(
			# 	select_by_att("structure_s_within", "NEW_SELECTION", building_query_2upscale),
			# 	"building_s_12.5k_within_2upscale", caci_ffn_query_2upscale)

		#-----------------------------------

		else:
			write("Current project important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_all.items())) #dict_import

			# Make layer of building surfaces < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_12.5k_within_2upscale", ffn_query_2upscale)

			# Make layer of building surfaces >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructureSrf", "building_s_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_s_50k+_within_2descale", ffn_query_2descale)

		total_2upscale_s = get_count("building_s_12.5k_within_2upscale")
		total_2descale_s = get_count("building_s_50k+_within_2descale")
		write("\n{0} below scale building surfaces in {1} BUAs are important, tall, or interesting.\nThey will be scaled up.".format(total_2upscale_s, bua_count))
		write("{0} building surfaces >= 50k in {1} BUAs are unimportant, short, and uninteresting.\nThey will be descaled.\n".format(total_2descale_s, bua_count))

		#-----------------------------------

		if total_2upscale_s:
			# Scale in important, tall, or landmark building surfaces within BUAs from below 50k to 250k (per PSG)
			write("Setting below scale important, tall, or landmark building surfaces to 250k...")
			with ap.da.UpdateCursor("building_s_12.5k_within_2upscale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 250000
					ucursor.updateRow(urow)

		if total_2descale_s:
			# Descale unimportant, short, and uninteresting building surfaces within BUAs from 50k+ to 12.5k
			write("Setting unimportant, short, and uninteresting building surfaces to 12.5k...")
			with ap.da.UpdateCursor("building_s_50k+_within_2descale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 12500
					ucursor.updateRow(urow)

		write("")

	if building_p_exist:
		# Adam's original important ffn list for just building points: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building points matching criteria...\n")
		if caci_schema: # Snowflake Protocol
			write("CACI specific important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_caci.items())) #dict_import

			# Make layer of building points < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_12.5k_within_2upscale", caci_ffn_query_2upscale)

			# Make layer of building points >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_50k+_within_2descale", caci_ffn_query_2descale)

		#-----------------------------------

		else:
			write("Current project important building FFNs list:")
			write("\n".join("{}: {}".format(k, v) for k, v in ad.ffn_list_all.items())) #dict_import

			# Make layer of building points < 50k, select the buildings within BUAs, and apply the important building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_12.5k", building_query_2upscale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_12.5k_within_2upscale", ffn_query_2upscale)

			# Make layer of building points >= 50k, select the buildings within BUAs, and apply the unimportant building query
			make_lyr(
				select_by_loc(
					make_lyr("StructurePnt", "building_p_50k+", building_query_2descale),
					"WITHIN", "buas", "", "NEW_SELECTION"),
				"building_p_50k+_within_2descale", ffn_query_2descale)

		total_2upscale_p = get_count("building_p_12.5k_within_2upscale")
		total_2descale_p = get_count("building_p_50k+_within_2descale")
		write("\n{0} below scale building points in {1} BUAs are important, tall, or interesting.\nThey will be scaled up.".format(total_2upscale_p, bua_count))
		write("{0} building points >= 50k in {1} BUAs are unimportant, short, and uninteresting.\nThey will be descaled.\n".format(total_2descale_p, bua_count))

		#-----------------------------------

		if total_2upscale_p:
			# Scale in important, tall, or landmark building points within BUAs from below 50k to 50k
			write("Setting below scale important, tall, or landmark building points to 50k...")
			with ap.da.UpdateCursor("building_p_12.5k_within_2upscale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 50000
					ucursor.updateRow(urow)

		if total_2descale_p:
			# Descale unimportant, short, and uninteresting building points within BUAs from 50k+ to 12.5k
			write("Setting unimportant, short, and uninteresting building points to 12.5k...")
			with ap.da.UpdateCursor("building_p_50k+_within_2descale", update_field) as ucursor:
				for urow in ucursor:
					urow[0] = 12500
					ucursor.updateRow(urow)
		write("")

	#----------------------------------------------------------------------

	# Count total buildings being upscaled and downscaled
	total_2upscale = total_2upscale_s + total_2upscale_p
	total_2descale = total_2descale_s + total_2descale_p

	# Clean up created layers
	for lyr in ["buas", "building_s_50k+", "building_s_50k+_within_2descale", "building_s_12.5k", "building_s_12.5k_within_2upscale"]: arcdel(lyr)

	write("{0} building surfaces scaled to 250k.".format(total_2upscale_s))
	write("{0} building surfaces scaled to 12500.".format(total_2descale_s))
	write("{0} building points scaled to 50000.".format(total_2upscale_p))
	write("{0} building points scaled to 12500.".format(total_2descale_p))
	building_finish = dt.now()
	write("\n{0} finished in {1}".format(tool_name, runtime(building_start, building_finish)))
	break










# Royal Decree update
#----------------------------------------------------------------------

	write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
	if not bua_exist or (not building_s_exist and not building_p_exist):
		write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif not bua_count:
		write(u"    |          No BUAs found                     {0}|".format(exs))
	else:
		write(u"    |          {0} Buildings upscaled        {1}{2}|".format(total_2upscale, format_count(total_2upscale), exs))
		write(u"    |          {0} Buildings descaled        {1}{2}|".format(total_2descale, format_count(total_2descale), exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))


#                           __                    __
#           __       __     \_\  __          __   \_\  __   __       __
#           \_\     /_/        \/_/         /_/      \/_/   \_\     /_/
#         .-.  \.-./  .-.   .-./  .-.   .-./  .-.   .-\   .-.  \.-./  .-.
# `.     //-\\_//-\\_//-\\_//-\\_//-\\_//-\\_// \\_//-\\_//-\\_//-\\_//-\\
# . `.__//   '-'   '-'\  '-'   '-'  /'-'   '-'\__'-'   '-'__/'-'   '-'\__
#  `.___/              \__       __/\          \_\       /_/           \_\
#                       \_\     /_/  \__
#                                     \_\


#Create Fishnet
mem_fc = "in_memory\\the_grid"
grid_lyr = "grid_lyr"
origin_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMin) # ESRI docs lie and say CreateFishnet uses a Point object like extent.lowerLeft
y_axis_coord = '{0} {1}'.format(ap.env.extent.XMin, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperLeft
corner_coord = '{0} {1}'.format(ap.env.extent.XMax, ap.env.extent.YMax) # ESRI docs lie and say CreateFishnet uses a Point object like extent.upperRight
# y_axis──>┌──┐<──corner
# origin──>└──┘
write("Constructing fishnet over dataset for partitioning data into chunks.\nThis helps our potatoes handle the large scale geospatial databases we have to process.")
ap.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", "", "POLYGON")
ap.MakeFeatureLayer_management(mem_fc, grid_lyr)


#----------------------------------------------------------------------
def clear_cache(lyr_list):
	for lyr in lyr_list: arcdel(lyr)
# Clean up created layers
clear_cache([hydro_pnt, hydro_crv, hydro_srf])


#----------------------------------------------------------------------
def integrate_hydro(tool_names, grid_lyr):
	hydro_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.hydro))
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
	hydro_finish = dt.now()
	write("{0} finished in {1}".format(tool_names.hydro, runtime(hydro_start, hydro_finish)))
	return hfeat_count


#----------------------------------------------------------------------
if bool_dict[tool_names.hydro]:
	#~~~~~ Royal Decree Variables ~~~~~
	hfeat_count = 0
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	try:
		hfeat_count = integrate_hydro(tool_names, grid_lyr)
	except ap.ExecuteError:
		writeresults(tool_names.hydro)



#----------------------------------------------------------------------
def integrate_trans(tool_names, grid_lyr):
	trans_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.trans))
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
	trans_finish = dt.now()
	write("{0} finished in {1}".format(tool_names.trans, runtime(trans_start, trans_finish)))
	return tfeat_count



#----------------------------------------------------------------------
def integrate_util(tool_names, grid_lyr):
	util_start = dt.now()
	write("\n--- {0} ---\n".format(tool_names.util))
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
	util_finish = dt.now()
	write("{0} finished in {1}".format(tool_names.util, runtime(util_start, util_finish)))
	return ufeat_count



#                           __                    __
#           __       __     \_\  __          __   \_\  __   __       __
#           \_\     /_/        \/_/         /_/      \/_/   \_\     /_/
#         .-.  \.-./  .-.   .-./  .-.   .-./  .-.   .-\   .-.  \.-./  .-.
# `.     //-\\_//-\\_//-\\_//-\\_//-\\_//-\\_// \\_//-\\_//-\\_//-\\_//-\\
# . `.__//   '-'   '-'\  '-'   '-'  /'-'   '-'\__'-'   '-'__/'-'   '-'\__
#  `.___/              \__       __/\          \_\       /_/           \_\
#                       \_\     /_/  \__
#                                     \_\



#----------------------------------------------------------------------
import arcpy as ap
from datetime import datetime as dt
ap.env.workspace = r'C:\Projects\njcagle\R&D\M1_H23C_50k_split_20210415.gdb\TDS'
ap.env.overwriteOutput = True
featureclass = ap.ListFeatureClasses()
featureclass.sort()

def runtime(start, finish): # Time a process or code block
	# Add a start and finish variable markers surrounding the code to be timed
	#from datetime import datetime as dt
	#start/finish = dt.now()
	# Returns string of formatted elapsed time between start and finish markers
	time_delta = (finish - start).total_seconds()
	h = int(time_delta/(60*60))
	m = int((time_delta%(60*60))/60)
	s = time_delta%60.
	#time_elapsed = "{}:{:>02}:{:>05.4f}".format(h, m, s) # 00:00:00.0000
	if h and m and s:
		time_elapsed = "{} hours {} minutes and {} seconds".format(h, m, round(s))
	elif not h and m and s:
		time_elapsed = "{} minutes and {:.1f} seconds".format(m, s)
	elif not h and not m and s:
		time_elapsed = "{:.3f} seconds".format(s)
	else:
		time_elapsed = 0
	return time_elapsed

def get_count(fc): # Returns feature count
    results = int(ap.GetCount_management(fc).getOutput(0))
    return results

start = dt.now()
for fc in featureclass:
    if fc.endswith('Pnt'):
        continue
	if not get_count(fc):
		continue

    print('adding field to {0}'.format(fc))
    try:
        ap.AddField_management(fc, 'vertex_count', "LONG")
    except:
        pass
    print('calculating vertex count for {0}'.format(fc))
    ap.CalculateField_management(fc, 'vertex_count', '!shape!.pointcount', "PYTHON")
    ap.MakeFeatureLayer_management(fc, 'curr_fc')
    print('selecting features larger than 10,000 vertices')
    ap.SelectLayerByAttribute_management('curr_fc', "NEW_SELECTION", 'vertex_count >= 10000')
    big_count = get_count('curr_fc')
    if not big_count:
        print("{0} has no big features".format(fc))
        try:
            print('removing new field\n')
            ap.DeleteField_management(fc, 'vertex_count')
            continue
        except:
            continue
    print('Dicing down to reasonable size')
    ap.Dice_management('curr_fc', str(fc) + '_diced', 10000)
    print('removing new field')
    ap.DeleteField_management(fc, 'vertex_count')
    print('Finished Dicing {0}\n'.format(fc))
print('finished in {0}'.format(runtime(start, dt.now())))





import arcpy as ap
def write(strink):
    print(strink)

ap.env.workspace = r'C:\Projects\njcagle\R&D\__Thunderdome\S2_J12A_multiparts.gdb\TDS'
featureclass = ap.ListFeatureClasses()
featureclass.sort()

def get_count(fc): # Returns feature count
    results = int(ap.GetCount_management(fc).getOutput(0))
    return results

for fc in featureclass:
    fc_count = get_count(fc)
    if not fc_count:
        write('{0} has 0 features. skipping.\n'.format(fc))
        continue
    write('Searching {0} features in {1}'.format(fc_count, fc))
    try:
        with ap.da.SearchCursor(fc, "*", 'HGT >= 46') as scursor:
            write('{0} has HGT field'.format(fc))
            count = 0
            for srow in scursor:
                count += 1
            write('{0}/{1} features matching HGT >= 46m\n'.format(count, fc_count))
    except:
        write("Query didn't apply to {0}\n".format(fc))
        continue


(¯`·.¸¸.·´¯`·.¸¸.·´¯`·.¸¸.·´¯`·.¸¸.·´¯`·.¸¸.·´¯)
 )                                            (
(           ~ Database  Guillotine ~           )
 )   Source: S2_J12A_multiparts               (
(    Output: J12A_Guillotine6                  )
 )   - Create new GDB based on source schema  (
(    - Cut features at AOI boundary            )
 )   - Query: HGT >= 46                       (
(    - Read all source feature classes         )
 )                                   _        (
(                                 __(.)<       )
(_.·´¯`·.¸¸.·´¯`·.¸¸.·´¯`·.¸¸.·´¯`\___)·´¯`·.¸_)





sdv_fields = ['sdv', 'OID@', 'SHAPE@'] #Source Date Value(SDV) field and the true centroid token of each feature to find which footprint it mostly overlaps
fc_fields = ['acc', 'ccn', 'sdp', 'srt', 'txt']
img_fields = ['Acquisitio', 'SHAPE@'] #Acquisition date for the imagery footprint polygons and the shape token for comparisons

# Need to impliment sdv value sanitation
''''''''' Blanket Feature Update Based on Absolutely Nothing '''''''''
for fc in featureclass:
	if not get_count(fc):
		continue

	write('\n== Searching {1} features for matching footprints. =='.format(fc))
	with ap.da.UpdateCursor(fc, sdv_fields) as ucursor: # ['sdv', 'OID@', 'SHAPE@']
		# For each feature in the feature class, blanket update the SDV field with the oldest imagery date cz fuck accuracy, we want consistency.
		count = 0
		unknown_err_list = []
		null_geom_list = []
		for urow in ucursor: # Iterate thru each feature in the fc
			# Checks shape for NULL geometries left over from Topology or bad data
			if urow[-1] is None:
				ap.AddError("*** WARNING ***")
				ap.AddError("NULL geometry found in {0} feature OID: {1}\nMake sure you have run the MGCP Finishing Tool.\nIf the problem persists, try running Repair Geometry manually and trying again.".format(fc, oid))
				null_geom_list.append(oid)
				continue
			sdv = urow[0]
			oid = urow[1]
			centroid = urow[-1].trueCentroid

			try:
				with ap.da.SearchCursor(img_foot, img_fields) as scursor: # ['Acquisitio', 'SHAPE@']
					for srow in scursor: # Iterate thru each imagery footprint polygon
						acquisition = srow[0]
						shape = srow[-1]
						if shape.contains(centroid): # If the current feature centroid is within this imagery footprint polygon
							cell_date = acquisition.strftime("%Y-%m-%d") # Assumes properly downloaded imagery footprint shapefile will have the Acquisition field as a date object
							if 'N_A' in sdv or not populated(sdv): # If the feature SDV field contains 'N_A' cz of some stupid analyst or is not populated
								urow[0] = cell_date
								count += 1
							elif populated(sdv): # If instead, the SDV field is populated with (hopefully) a date
								try:
									feat_date = datetime.strptime(sdv, "%Y-%m-%d") # Parse what should be a text field in this format
									if acquisition > feat_date:
										urow[0] = cell_date
										count += 1
								except: # The SDV fild has some oddball value or an incorrectly formatted date. Fuck it. Overwrite it.
									urow[0] = cell_date
									count += 1
									continue
			except:
				# If SDV is NULL or incorrect format, skip to next feature
				ap.AddError("Encountered a problem while applying the Imagery Footprint acquisition date to {0} feature OID: {1}. Possibly a NULL value in the imagery acquisition date or NULL geometry or attribute in the feature.\nPlease check the validity of the Imagery Footprint and try again.\n**If this problem persists, you may have to manually attribute the SDV of the {0} feature. Please attribute it with the oldest Acquisition field date in the Imagery Footprint that intersects it.".format(fc, oid))
				unknown_err_list.append(oid)
				continue

			ucursor.updateRow(urow)

	if count > 0:
		write('\nUpdated {0} SDV dates in {1}.'.format(count, fc))
	if len(unknown_err_list) > 0:
		ap.AddError("\n*** WARNING ***")
		ap.AddError("These {0} features failed to have their SDV updated. Further manual investigation may be required.\nCheck the Imagery Footprint Acquisition field and the individual feature attribute fields and geometry.".format(fc))
		ap.AddError(unknown_err_list)
	if len(null_geom_list) > 0:
		ap.AddError("\n*** WARNING ***")
		ap.AddError("These {0} features were flagged as having NULL geometry. If Repair Geometry has not fixed them, further manual investigation may be required.".format(fc))
		ap.AddError(null_geom_list)




corner = [19.000000000000, -8.000000000000]
... ws = arcpy.Point(corner[0], corner[1])
... wn = arcpy.Point(corner[0], corner[1]+1)
... en = arcpy.Point(corner[0]+1, corner[1]+1)
... es = arcpy.Point(corner[0]+1, corner[1])
... coords = [ws, wn, en, es, ws]
... #ptGeometry = arcpy.PointGeometry(point)
... #arcpy.Polygon(arcpy.Array(coords))
...
... # Create a feature class with a spatial reference of GCS WGS 1984
... result = arcpy.CreateFeatureclass_management(r'C:\Projects\njcagle\finishing\====== L3Harris_MGCP ======\E019S08_boogaloo\_E019S08_delivery_folder\E019S08\E019S08_MGCP_TRD4_5_1_sub1.gdb\MGCP_Metadata', "bs_skware", "POLYGON", spatial_reference=4326)
... #feature_class = result[0]
...
... with arcpy.da.InsertCursor("bs_skware", ["SHAPE@"]) as icursor:
...     icursor.insertRow([arcpy.Polygon(arcpy.Array(coords), arcpy.SpatialReference(4326))])
...
... arcpy.Append_management('bs_skware', 'Cell', 'NO_TEST','First','')





corner = [19.000000000000, -8.000000000000]
ws = arcpy.Point(corner[0], corner[1])
wn = arcpy.Point(corner[0], corner[1]+1)
en = arcpy.Point(corner[0]+1, corner[1]+1)
es = arcpy.Point(corner[0]+1, corner[1])
coords = [ws, wn, en, es, ws]

# Create a feature class with a spatial reference of GCS WGS 1984
arcpy.CreateFeatureclass_management(MGCP, "bs_skware", "POLYGON", spatial_reference=4326)

with arcpy.da.InsertCursor("bs_skware", ["SHAPE@"]) as icursor:
	icursor.insertRow([arcpy.Polygon(arcpy.Array(coords), arcpy.SpatialReference(4326))])

arcpy.Append_management('bs_skware', fc_cell, 'NO_TEST','First','')
arcpy.Delete_management('bs_skware')
