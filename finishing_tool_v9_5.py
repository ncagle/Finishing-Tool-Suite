# -*- coding: utf-8 -*-
# ====================== #
# Finishing Tool v9.6    #
# Nat Cagle 2022-03-16   #
# ====================== #
import arcpy
from arcpy import AddMessage as write
from datetime import datetime as dt
from collections import OrderedDict
import csv as cs
import uuid
import os
import sys
import time
import math

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


# To Do List:
#### 4 hashtags means things to be updated

# rewrite selections of default pylons and bridges and make new fc in memory for cursor
# in memory upgrade
# Defense mapping version takes too long and crashes. just rewrite with manual calculations
# Error handling for feature classes used in integration not present in database
# Error handling for featureclass <NoneType> has no attribute .sort(). Tell user that ArcMap has failed to interanlly update the location of the input TDS. Just restart ArcMap and try again.
# Pull local user profile name and add it to the "stop being cheeky" easter egg
# optional DisableEditorTracking_management (default true)

#####

# Toolbox is running slow when everything is imported. All in one script 3000 lines and growing.
# I didn't want the individual tools cz I wanted the entire workflow to be accessible from one window
# What if each of the categories does have it's own tool if it needs to be run in particular without all
# the other options. But then the main Finishing Tool Suite is a Workflow Wrapper.
# So it imports the toolbox of itself and then calls the other tools in the toolbox as they are checked.
# This way, it stays sleek. Roundabout way of having tools as functions split up and importing them while
# still keeping it all in one toolbox without extra files

#####

# Write information for given variable
def write_info(name,var): # write_info('var_name',var)
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	write("Debug info for {0}:".format(name))
	write("   Variable Type: {0}".format(type(var)))
	write("   Assigned Value: {0}".format(var))
	write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# Gets messages from the ArcGIS tools ran and sends messages to dialog
def writeresults():
    messages = arcpy.GetMessages(0)
    warnings = arcpy.GetMessages(1)
    errors = arcpy.GetMessages(2)
    write(messages)
    if len(warnings) > 0:
        write(warnings)
    if len(errors) > 0:
        write(errors)
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Global Dictionaries and Parameters #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Dictionary Definitions '''''''''
#Dictionaries that associate FCodes and FCSubtypes with respective labels
#Dicitionary names: fcode_dict, fcsub_dict, sub2fcode_dict, fc_fields_og, fc_fields
fcode_dict = { 'AB040' : 'AerationBasin',
              'AT011' : 'Aerial',
              'AT012' : 'AerialFarm',
              'GB230' : 'AircraftHangar',
              'AK164' : 'Amphitheatre',
              'AK030' : 'AmusementPark',
              'AK020' : 'AmusementParkAttraction',
              'ZD045' : 'AnnotatedLocation',
              'GB015' : 'Apron',
              'BH010' : 'Aqueduct',
              'BH116' : 'Aquifer',
              'AQ151' : 'Arcade',
              'AL012' : 'ArcheologicalSite',
              'DA005' : 'AsphaltLake',
              'AL142' : 'AstronomicalObservatory',
              'AJ085' : 'Barn',
              'BI045' : 'BasinGate',
              'AG050' : 'Billboard',
              'AC010' : 'BlastFurnace',
              'BH015' : 'Bog',
              'AA045' : 'Borehole',
              'EA031' : 'BotanicGarden',
              'ZB030' : 'BoundaryMonument',
              'AQ040' : 'Bridge',
              'AQ056' : 'BridgePier',
              'AQ045' : 'BridgeSpan',
              'AQ050' : 'BridgeSuperstructure',
              'AQ055' : 'BridgeTower',
              'EB070' : 'Brush',
              'AL013' : 'Building',
              'AL018' : 'BuildingSuperstructure',
              'AL020' : 'BuiltUpArea',
              'AT005' : 'Cable',
              'AT041' : 'Cableway',
              'AL025' : 'Cairn',
              'AI030' : 'Camp',
              'AK060' : 'CampSite',
              'BH020' : 'Canal',
              'EC010' : 'Cane',
              'SU004' : 'CantonmentArea',
              'AI020' : 'CaravanPark',
              'AP010' : 'CartTrack',
              'AL375' : 'Castle',
              'AL376' : 'CastleComplex',
              'AC020' : 'CatalyticCracker',
              'AQ063' : 'CausewayStructure',
              'DB028' : 'CaveChamber',
              'DB029' : 'CaveMouth',
              'AL030' : 'Cemetery',
              'AH070' : 'Checkpoint',
              'BI010' : 'Cistern',
              'EC040' : 'ClearedWay',
              'FA210' : 'ConservationArea',
              'FA012' : 'ContaminatedRegion',
              'AQ060' : 'ControlTower',
              'AF020' : 'Conveyor',
              'AD055' : 'CoolingFacility',
              'AF030' : 'CoolingTower',
              'AL175' : 'Courtyard',
              'AF040' : 'Crane',
              'BJ031' : 'Crevasse',
              'DB061' : 'Crevice',
              'EA010' : 'CropLand',
              'AQ062' : 'Crossing',
              'AQ065' : 'Culvert',
              'DB070' : 'Cut',
              'DB071' : 'CutLine',
              'BI020' : 'Dam',
              'GB050' : 'DefensiveRevetment',
              'DB080' : 'Depression',
              'EE030' : 'Desert',
              'AT010' : 'DishAerial',
              'AB000' : 'DisposalSite',
              'BH030' : 'Ditch',
              'AL060' : 'DragonsTeeth',
              'AK070' : 'DriveInTheatre',
              'BB090' : 'DryDock',
              'AD010' : 'ElectricPowerStation',
              'CA010' : 'ElevationContour',
              'DB090' : 'Embankment',
              'AH025' : 'EngineeredEarthwork',
              'AP033' : 'EngineeredTurnaroundSite',
              'AF060' : 'EngineTestCell',
              'DB100' : 'Esker',
              'AF050' : 'ExcavatingMachine',
              'AA010' : 'ExtractionMine',
              'AL010' : 'Facility',
              'AK090' : 'Fairground',
              'AL070' : 'Fence',
              'AQ070' : 'FerryCrossing',
              'AQ080' : 'FerryStation',
              'AL017' : 'FireHydrant',
              'FA015' : 'FiringRange',
              'BH051' : 'FishFarmFacility',
              'BI060' : 'FishLadder',
              'BB110' : 'FishWeir',
              'AL073' : 'Flagpole',
              'AF070' : 'FlarePipe',
              'BB199' : 'FloatingDryDock',
              'BI044' : 'FloodControlStructure',
              'BH070' : 'Ford',
              'EC015' : 'Forest',
              'EC060' : 'ForestClearing',
              'AH055' : 'FortifiedBuilding',
              'BH075' : 'Fountain',
              'AM075' : 'FuelStorageFacility',
              'AL080' : 'Gantry',
              'AP040' : 'Gate',
              'BI070' : 'GaugingStation',
              'DB110' : 'GeologicFault',
              'DB115' : 'GeothermalOutlet',
              'BJ030' : 'Glacier',
              'AK100' : 'GolfCourse',
              'AK101' : 'GolfDrivingRange',
              'AM030' : 'GrainElevator',
              'AM020' : 'GrainStorageStructure',
              'AK110' : 'Grandstand',
              'EB010' : 'Grassland',
              'AJ110' : 'Greenhouse',
              'BB005' : 'Harbour',
              'GB250' : 'HardenedAircraftShelter',
              'AD050' : 'HeatingFacility',
              'EA020' : 'Hedgerow',
              'GB030' : 'Helipad',
              'GB035' : 'Heliport',
              'AJ030' : 'HoldingPen',
              'EA055' : 'HopField',
              'AF080' : 'Hopper',
              'BD181' : 'Hulk',
              'BH077' : 'Hummock',
              'AL099' : 'Hut',
              'AC040' : 'HydrocarbonProdFacility',
              'AA052' : 'HydrocarbonsField',
              'BJ099' : 'IceCap',
              'BJ040' : 'IceCliff',
              'BJ060' : 'IcePeak',
              'AQ075' : 'IceRoute',
              'BJ065' : 'IceShelf',
              'AL270' : 'IndustrialFarm',
              'AC060' : 'IndustrialFurnace',
              'BH082' : 'InlandWaterbody',
              'AL011' : 'Installation',
              'SU030' : 'InstallationBoundary',
              'AL201' : 'InterestSite',
              'BA030' : 'Island',
              'GB005' : 'LandAerodrome',
              'IA040' : 'LandParcel',
              'DB211' : 'LandslideMass',
              'BH090' : 'LandSubjectToInundation',
              'BA010' : 'LandWaterBoundary',
              'GB040' : 'LaunchPad',
              'BC050' : 'Lighthouse',
              'AL110' : 'LightSupportStructure',
              'BC070' : 'LightVessel',
              'AB021' : 'LiquidDiffuser',
              'BI030' : 'Lock',
              'EE010' : 'LoggingSite',
              'AK121' : 'Lookout',
              'AL371' : 'ManorHouse',
              'AI021' : 'ManufacturedHomePark',
              'ED010' : 'Marsh',
              'AL130' : 'MemorialMonument',
              'SU001' : 'MilitaryInstallation',
              'AL065' : 'Minefield',
              'AM040' : 'MineralPile',
              'AA020' : 'MineShaftSuperstructure',
              'AL120' : 'MissileSite',
              'BH100' : 'Moat',
              'AQ110' : 'MooringMast',
              'BJ020' : 'Moraine',
              'AQ170' : 'MotorVehicleStation',
              'DB150' : 'MountainPass',
              'AM065' : 'MunitionStorageFacility',
              'ZD040' : 'NamedLocation',
              'BH170' : 'NaturalPool',
              'AL014' : 'NonBuildingStructure',
              'AA054' : 'NonWaterWell',
              'AD041' : 'NuclearReactorContainment',
              'EC020' : 'Oasis',
              'AG040' : 'OfficePark',
              'BD115' : 'OffshoreConstruction',
              'EA040' : 'Orchard',
              'AK080' : 'OutdoorTheatreScreen',
              'AL155' : 'OverheadObstruction',
              'AK120' : 'Park',
              'AQ141' : 'ParkingGarage',
              'AL140' : 'ParticleAccelerator',
              'BH110' : 'Penstock',
              'AK061' : 'PicnicSite',
              'AQ113' : 'Pipeline',
              'AL165' : 'PipelineCrossingPoint',
              'EA030' : 'PlantNursery',
              'BJ080' : 'PolarIce',
              'BB009' : 'Port',
              'AD030' : 'PowerSubstation',
              'AQ111' : 'PreparedWatercourseCross',
              'AL170' : 'PublicSquare',
              'AQ116' : 'PumpingStation',
              'AT042' : 'Pylon',
              'BH012' : 'QanatShaft',
              'AK130' : 'Racetrack',
              'AT045' : 'RadarStation',
              'AN010' : 'Railway',
              'AN050' : 'RailwaySidetrack',
              'AN085' : 'RailwaySignal',
              'AN075' : 'RailwayTurntable',
              'AN060' : 'RailwayYard',
              'AL195' : 'Ramp',
              'BH120' : 'Rapids',
              'AB010' : 'RecyclingSite',
              'AL180' : 'RetailStand',
              'BH135' : 'RiceField',
              'AA040' : 'Rig',
              'BH140' : 'River',
              'AP030' : 'Road',
              'AP020' : 'RoadInterchange',
              'AQ135' : 'RoadsideRestArea',
              'DB160' : 'RockFormation',
              'AN076' : 'Roundhouse',
              'AL200' : 'Ruins',
              'GB055' : 'Runway',
              'BH160' : 'Sabkha',
              'BH155' : 'SaltEvaporator',
              'BH150' : 'SaltFlat',
              'DB170' : 'SandDunes',
              'AK161' : 'Scoreboard',
              'GB070' : 'SeaplaneRun',
              'AL105' : 'Settlement',
              'AC030' : 'SettlingPond',
              'AC507' : 'SewageTreatmentPlant',
              'AL208' : 'ShantyTown',
              'AQ118' : 'SharpCurve',
              'AA011' : 'ShearWall',
              'AL019' : 'Shed',
              'BI006' : 'ShipElevator',
              'AM011' : 'ShippingContainer',
              'BB241' : 'Shipyard',
              'AG030' : 'ShoppingComplex',
              'BB081' : 'ShorelineConstruction',
              'BB082' : 'ShorelineRamp',
              'AQ035' : 'Sidewalk',
              'AK150' : 'SkiJump',
              'AK155' : 'SkiRun',
              'BI040' : 'SluiceGate',
              'BB201' : 'SmallCraftFacility',
              'AF010' : 'Smokestack',
              'BD140' : 'Snag',
              'BJ100' : 'SnowIceField',
              'DA010' : 'SoilSurfaceRegion',
              'AD025' : 'SolarFarm',
              'AD020' : 'SolarPanel',
              'AL351' : 'SpaceFacility',
              'BH165' : 'Spillway',
              'AK040' : 'SportsGround',
              'CA030' : 'SpotElevation',
              'AJ080' : 'Stable',
              'AK160' : 'Stadium',
              'AQ150' : 'Stair',
              'AQ120' : 'SteepGrade',
              'DB010' : 'SteepTerrainFace',
              'GB045' : 'Stopway',
              'AM010' : 'StorageDepot',
              'AM070' : 'StorageTank',
              'AQ114' : 'StormDrain',
              'AQ161' : 'StreetLamp',
              'AQ162' : 'StreetSign',
              'BD100' : 'StructuralPile',
              'AM060' : 'SurfaceBunker',
              'ZB050' : 'SurveyPoint',
              'ED020' : 'Swamp',
              'AK170' : 'SwimmingPool',
              'AP056' : 'TankCrossing',
              'AM071' : 'TankFarm',
              'AP055' : 'TankTrail',
              'GB075' : 'Taxiway',
              'FA100' : 'TestSite',
              'AL510' : 'TetheredBalloon',
              'EB020' : 'Thicket',
              'BA040' : 'TidalWater',
              'AL036' : 'Tomb',
              'AL241' : 'Tower',
              'AQ160' : 'TrafficLight',
              'AP050' : 'Trail',
              'FA165' : 'TrainingSite',
              'AQ068' : 'TransportationBlock',
              'AQ125' : 'TransportationStation',
              'AQ059' : 'TransRouteCharacterChange',
              'AL211' : 'TransRouteProtectStruct',
              'EC005' : 'Tree',
              'BJ110' : 'Tundra',
              'AQ130' : 'Tunnel',
              'AQ095' : 'TunnelMouth',
              'AH060' : 'UndergroundBunker',
              'AL250' : 'UndergroundDwelling',
              'AQ115' : 'UtilityCover',
              'BH145' : 'VanishingPoint',
              'AP041' : 'VehicleBarrier',
              'AQ140' : 'VehicleLot',
              'BI005' : 'VesselLift',
              'EA050' : 'Vineyard',
              'ZD020' : 'VoidCollectionArea',
              'DB190' : 'VolcanicDyke',
              'DB180' : 'Volcano',
              'AL260' : 'Wall',
              'AB507' : 'WasteHeap',
              'GB065' : 'WaterAerodrome',
              'BH180' : 'Waterfall',
              'BI050' : 'WaterIntakeTower',
              'ZD070' : 'WaterMeasurementLocation',
              'AJ055' : 'WaterMill',
              'BH065' : 'WaterRace',
              'AM080' : 'WaterTower',
              'BH040' : 'WaterTreatmentBed',
              'BH230' : 'WaterWell',
              'BH220' : 'Waterwork',
              'AD060' : 'WindFarm',
              'AJ050' : 'Windmill',
              'AJ051' : 'WindTurbine',
              'AK180' : 'Zoo'
}

fcsub_dict = { 100010 : 'AerationBasin',
              100201 : 'Aerial',
              100202 : 'AerialFarm',
              100456 : 'AircraftHangar',
              100074 : 'Amphitheatre',
              100054 : 'AmusementPark',
              100053 : 'AmusementParkAttraction',
              100476 : 'AnnotatedLocation',
              100438 : 'Apron',
              100295 : 'Aqueduct',
              154640 : 'Aquifer',
              100192 : 'Arcade',
              100082 : 'ArcheologicalSite',
              100356 : 'AsphaltLake',
              100111 : 'AstronomicalObservatory',
              100691 : 'Barn',
              131206 : 'BasinGate',
              121638 : 'Billboard',
              100012 : 'BlastFurnace',
              100296 : 'Bog',
              100696 : 'Borehole',
              100383 : 'BotanicGarden',
              100465 : 'BoundaryMonument',
              100161 : 'Bridge',
              100165 : 'BridgePier',
              100162 : 'BridgeSpan',
              100163 : 'BridgeSuperstructure',
              100164 : 'BridgeTower',
              100390 : 'Brush',
              100083 : 'Building',
              100087 : 'BuildingSuperstructure',
              100089 : 'BuiltUpArea',
              100199 : 'Cable',
              100206 : 'Cableway',
              100091 : 'Cairn',
              100041 : 'Camp',
              100057 : 'CampSite',
              100297 : 'Canal',
              100393 : 'Cane',
              170162 : 'CantonmentArea',
              100040 : 'CaravanPark',
              100150 : 'CartTrack',
              100128 : 'Castle',
              132642 : 'CastleComplex',
              100013 : 'CatalyticCracker',
              130381 : 'CausewayStructure',
              154959 : 'CaveChamber',
              154961 : 'CaveMouth',
              100092 : 'Cemetery',
              100039 : 'Checkpoint',
              100329 : 'Cistern',
              100396 : 'ClearedWay',
              100417 : 'ConservationArea',
              100409 : 'ContaminatedRegion',
              100167 : 'ControlTower',
              100026 : 'Conveyor',
              100697 : 'CoolingFacility',
              100028 : 'CoolingTower',
              100688 : 'Courtyard',
              100029 : 'Crane',
              100342 : 'Crevasse',
              100365 : 'Crevice',
              100380 : 'CropLand',
              100168 : 'Crossing',
              100170 : 'Culvert',
              100366 : 'Cut',
              192101 : 'CutLine',
              100330 : 'Dam',
              100446 : 'DefensiveRevetment',
              100367 : 'Depression',
              100403 : 'Desert',
              100200 : 'DishAerial',
              100007 : 'DisposalSite',
              100298 : 'Ditch',
              100096 : 'DragonsTeeth',
              100059 : 'DriveInTheatre',
              100233 : 'DryDock',
              100018 : 'ElectricPowerStation',
              100353 : 'ElevationContour',
              100368 : 'Embankment',
              132596 : 'EngineeredEarthwork',
              179969 : 'EngineeredTurnaroundSite',
              100031 : 'EngineTestCell',
              100369 : 'Esker',
              100030 : 'ExcavatingMachine',
              100001 : 'ExtractionMine',
              100080 : 'Facility',
              100061 : 'Fairground',
              100098 : 'Fence',
              100172 : 'FerryCrossing',
              100174 : 'FerryStation',
              100086 : 'FireHydrant',
              100410 : 'FiringRange',
              191951 : 'FishFarmFacility',
              100338 : 'FishLadder',
              100236 : 'FishWeir',
              100099 : 'Flagpole',
              100032 : 'FlarePipe',
              100243 : 'FloatingDryDock',
              131207 : 'FloodControlStructure',
              100302 : 'Ford',
              130380 : 'Forest',
              100398 : 'ForestClearing',
              132626 : 'FortifiedBuilding',
              100303 : 'Fountain',
              100141 : 'FuelStorageFacility',
              100101 : 'Gantry',
              100154 : 'Gate',
              100339 : 'GaugingStation',
              100370 : 'GeologicFault',
              100371 : 'GeothermalOutlet',
              100341 : 'Glacier',
              100062 : 'GolfCourse',
              100063 : 'GolfDrivingRange',
              100134 : 'GrainElevator',
              100133 : 'GrainStorageStructure',
              100064 : 'Grandstand',
              100387 : 'Grassland',
              100052 : 'Greenhouse',
              100222 : 'Harbour',
              100457 : 'HardenedAircraftShelter',
              100023 : 'HeatingFacility',
              100381 : 'Hedgerow',
              100441 : 'Helipad',
              100442 : 'Heliport',
              100043 : 'HoldingPen',
              100386 : 'HopField',
              100033 : 'Hopper',
              100279 : 'Hulk',
              100304 : 'Hummock',
              100103 : 'Hut',
              100015 : 'HydrocarbonProdFacility',
              100006 : 'HydrocarbonsField',
              100348 : 'IceCap',
              100343 : 'IceCliff',
              100344 : 'IcePeak',
              100173 : 'IceRoute',
              100345 : 'IceShelf',
              100129 : 'IndustrialFarm',
              100016 : 'IndustrialFurnace',
              130384 : 'InlandWaterbody',
              100081 : 'Installation',
              180061 : 'InstallationBoundary',
              100117 : 'InterestSite',
              100217 : 'Island',
              100436 : 'LandAerodrome',
              100458 : 'LandParcel',
              100379 : 'LandslideMass',
              100307 : 'LandSubjectToInundation',
              100212 : 'LandWaterBoundary',
              100443 : 'LaunchPad',
              100253 : 'Lighthouse',
              100105 : 'LightSupportStructure',
              100256 : 'LightVessel',
              100009 : 'LiquidDiffuser',
              100331 : 'Lock',
              100401 : 'LoggingSite',
              100066 : 'Lookout',
              180086 : 'ManorHouse',
              133168 : 'ManufacturedHomePark',
              100399 : 'Marsh',
              100108 : 'MemorialMonument',
              100462 : 'MilitaryInstallation',
              100097 : 'Minefield',
              100136 : 'MineralPile',
              100003 : 'MineShaftSuperstructure',
              100106 : 'MissileSite',
              100309 : 'Moat',
              100177 : 'MooringMast',
              100340 : 'Moraine',
              100197 : 'MotorVehicleStation',
              100372 : 'MountainPass',
              100138 : 'MunitionStorageFacility',
              100475 : 'NamedLocation',
              100320 : 'NaturalPool',
              100084 : 'NonBuildingStructure',
              155023 : 'NonWaterWell',
              100022 : 'NuclearReactorContainment',
              100394 : 'Oasis',
              100035 : 'OfficePark',
              100272 : 'OffshoreConstruction',
              100384 : 'Orchard',
              100060 : 'OutdoorTheatreScreen',
              100112 : 'OverheadObstruction',
              100065 : 'Park',
              100190 : 'ParkingGarage',
              100110 : 'ParticleAccelerator',
              100310 : 'Penstock',
              100058 : 'PicnicSite',
              100179 : 'Pipeline',
              100113 : 'PipelineCrossingPoint',
              100382 : 'PlantNursery',
              100347 : 'PolarIce',
              100223 : 'Port',
              100021 : 'PowerSubstation',
              100178 : 'PreparedWatercourseCross',
              100114 : 'PublicSquare',
              100182 : 'PumpingStation',
              100558 : 'Pylon',
              131749 : 'QanatShaft',
              100069 : 'Racetrack',
              100207 : 'RadarStation',
              100143 : 'Railway',
              100144 : 'RailwaySidetrack',
              100149 : 'RailwaySignal',
              100146 : 'RailwayTurntable',
              100145 : 'RailwayYard',
              100115 : 'Ramp',
              100311 : 'Rapids',
              100008 : 'RecyclingSite',
              100689 : 'RetailStand',
              100313 : 'RiceField',
              100004 : 'Rig',
              100314 : 'River',
              100152 : 'Road',
              100151 : 'RoadInterchange',
              100188 : 'RoadsideRestArea',
              100373 : 'RockFormation',
              100147 : 'Roundhouse',
              100116 : 'Ruins',
              100448 : 'Runway',
              100318 : 'Sabkha',
              100317 : 'SaltEvaporator',
              100316 : 'SaltFlat',
              100374 : 'SandDunes',
              121747 : 'Scoreboard',
              100453 : 'SeaplaneRun',
              100104 : 'Settlement',
              100014 : 'SettlingPond',
              134665 : 'SewageTreatmentPlant',
              100118 : 'ShantyTown',
              100183 : 'SharpCurve',
              100002 : 'ShearWall',
              100088 : 'Shed',
              132749 : 'ShipElevator',
              100132 : 'ShippingContainer',
              100245 : 'Shipyard',
              100034 : 'ShoppingComplex',
              100231 : 'ShorelineConstruction',
              100232 : 'ShorelineRamp',
              100159 : 'Sidewalk',
              100072 : 'SkiJump',
              100073 : 'SkiRun',
              100334 : 'SluiceGate',
              100244 : 'SmallCraftFacility',
              100025 : 'Smokestack',
              100277 : 'Snag',
              100349 : 'SnowIceField',
              100358 : 'SoilSurfaceRegion',
              100020 : 'SolarFarm',
              100019 : 'SolarPanel',
              100126 : 'SpaceFacility',
              100319 : 'Spillway',
              100055 : 'SportsGround',
              100355 : 'SpotElevation',
              100049 : 'Stable',
              154703 : 'Stadium',
              100191 : 'Stair',
              100185 : 'SteepGrade',
              100362 : 'SteepTerrainFace',
              100444 : 'Stopway',
              100131 : 'StorageDepot',
              100139 : 'StorageTank',
              100180 : 'StormDrain',
              100195 : 'StreetLamp',
              100196 : 'StreetSign',
              100271 : 'StructuralPile',
              100137 : 'SurfaceBunker',
              177997 : 'SurveyPoint',
              100400 : 'Swamp',
              100077 : 'SwimmingPool',
              180006 : 'TankCrossing',
              100140 : 'TankFarm',
              179906 : 'TankTrail',
              100454 : 'Taxiway',
              100414 : 'TestSite',
              100130 : 'TetheredBalloon',
              100388 : 'Thicket',
              100218 : 'TidalWater',
              100094 : 'Tomb',
              100122 : 'Tower',
              100194 : 'TrafficLight',
              100156 : 'Trail',
              100416 : 'TrainingSite',
              100171 : 'TransportationBlock',
              100186 : 'TransportationStation',
              131083 : 'TransRouteCharacterChange',
              130921 : 'TransRouteProtectStruct',
              100392 : 'Tree',
              100350 : 'Tundra',
              100187 : 'Tunnel',
              100176 : 'TunnelMouth',
              100038 : 'UndergroundBunker',
              100123 : 'UndergroundDwelling',
              100181 : 'UtilityCover',
              100315 : 'VanishingPoint',
              100155 : 'VehicleBarrier',
              100189 : 'VehicleLot',
              100328 : 'VesselLift',
              100385 : 'Vineyard',
              100473 : 'VoidCollectionArea',
              100377 : 'VolcanicDyke',
              100375 : 'Volcano',
              100124 : 'Wall',
              177962 : 'WasteHeap',
              100452 : 'WaterAerodrome',
              100321 : 'Waterfall',
              100337 : 'WaterIntakeTower',
              164755 : 'WaterMeasurementLocation',
              100046 : 'WaterMill',
              131810 : 'WaterRace',
              100142 : 'WaterTower',
              100299 : 'WaterTreatmentBed',
              100326 : 'WaterWell',
              100325 : 'Waterwork',
              100687 : 'WindFarm',
              100044 : 'Windmill',
              100045 : 'WindTurbine',
              100078 : 'Zoo'
}

sub2fcode_dict = {100185 : 'AQ120',
                 100162 : 'AQ045',
                 100344 : 'BJ060',
                 100401 : 'EE010',
                 100417 : 'FA210',
                 100161 : 'AQ040',
                 100295 : 'BH010',
                 131749 : 'BH012',
                 100296 : 'BH015',
                 100307 : 'BH090',
                 131207 : 'BI044',
                 154703 : 'AK160',
                 100097 : 'AL065',
                 100031 : 'AF060',
                 177997 : 'ZB050',
                 100074 : 'AK164',
                 100372 : 'DB150',
                 100465 : 'ZB030',
                 100015 : 'AC040',
                 100314 : 'BH140',
                 100691 : 'AJ085',
                 100104 : 'AL105',
                 100179 : 'AQ113',
                 100049 : 'AJ080',
                 100156 : 'AP050',
                 100002 : 'AA011',
                 100223 : 'BB009',
                 100176 : 'AQ095',
                 100143 : 'AN010',
                 100329 : 'BI010',
                 100343 : 'BJ040',
                 100130 : 'AL510',
                 100212 : 'BA010',
                 180086 : 'AL371',
                 132642 : 'AL376',
                 100060 : 'AK080',
                 100319 : 'BH165',
                 100128 : 'AL375',
                 180061 : 'SU030',
                 100218 : 'BA040',
                 100438 : 'GB015',
                 100072 : 'AK150',
                 100687 : 'AD060',
                 100163 : 'AQ050',
                 100113 : 'AL165',
                 100164 : 'AQ055',
                 100165 : 'AQ056',
                 100320 : 'BH170',
                 100380 : 'EA010',
                 131083 : 'AQ059',
                 100272 : 'BD115',
                 100453 : 'GB070',
                 100414 : 'FA100',
                 100183 : 'AQ118',
                 100321 : 'BH180',
                 100367 : 'DB080',
                 100178 : 'AQ111',
                 100177 : 'AQ110',
                 100105 : 'AL110',
                 130921 : 'AL211',
                 133168 : 'AI021',
                 100040 : 'AI020',
                 177962 : 'AB507',
                 100182 : 'AQ116',
                 132626 : 'AH055',
                 100043 : 'AJ030',
                 100055 : 'AK040',
                 100140 : 'AM071',
                 100396 : 'EC040',
                 100132 : 'AM011',
                 100331 : 'BI030',
                 100689 : 'AL180',
                 100399 : 'ED010',
                 100124 : 'AL260',
                 100061 : 'AK090',
                 131810 : 'BH065',
                 100023 : 'AD050',
                 100436 : 'GB005',
                 100697 : 'AD055',
                 100110 : 'AL140',
                 100318 : 'BH160',
                 100133 : 'AM020',
                 164755 : 'ZD070',
                 100096 : 'AL060',
                 100016 : 'AC060',
                 100362 : 'DB010',
                 100271 : 'BD100',
                 100452 : 'GB065',
                 100001 : 'AA010',
                 100188 : 'AQ135',
                 100368 : 'DB090',
                 100058 : 'AK061',
                 100339 : 'BI070',
                 100349 : 'BJ100',
                 100304 : 'BH077',
                 100303 : 'BH075',
                 100041 : 'AI030',
                 100034 : 'AG030',
                 100385 : 'EA050',
                 100342 : 'BJ031',
                 100390 : 'EB070',
                 100232 : 'BB082',
                 100022 : 'AD041',
                 100194 : 'AQ160',
                 100053 : 'AK020',
                 100345 : 'BJ065',
                 100195 : 'AQ161',
                 100136 : 'AM040',
                 100350 : 'BJ110',
                 100181 : 'AQ115',
                 100009 : 'AB021',
                 100115 : 'AL195',
                 100126 : 'AL351',
                 100033 : 'AF080',
                 192101 : 'DB071',
                 100222 : 'BB005',
                 100202 : 'AT012',
                 100201 : 'AT011',
                 100200 : 'AT010',
                 100108 : 'AL130',
                 100134 : 'AM030',
                 100186 : 'AQ125',
                 100374 : 'DB170',
                 100190 : 'AQ141',
                 100476 : 'ZD045',
                 100446 : 'GB050',
                 100355 : 'CA030',
                 100448 : 'GB055',
                 100475 : 'ZD040',
                 100233 : 'BB090',
                 154640 : 'BH116',
                 100054 : 'AK030',
                 100310 : 'BH110',
                 100338 : 'BI060',
                 100392 : 'EC005',
                 100092 : 'AL030',
                 100159 : 'AQ035',
                 100299 : 'BH040',
                 100365 : 'DB061',
                 100028 : 'AF030',
                 100021 : 'AD030',
                 100316 : 'BH150',
                 100279 : 'BD181',
                 100045 : 'AJ051',
                 100044 : 'AJ050',
                 100398 : 'EC060',
                 132749 : 'BI006',
                 100069 : 'AK130',
                 100353 : 'CA010',
                 100400 : 'ED020',
                 100116 : 'AL200',
                 100117 : 'AL201',
                 100035 : 'AG040',
                 180006 : 'AP056',
                 100118 : 'AL208',
                 100473 : 'ZD020',
                 100014 : 'AC030',
                 100199 : 'AT005',
                 130384 : 'BH082',
                 100373 : 'DB160',
                 100151 : 'AP020',
                 191951 : 'BH051',
                 100174 : 'AQ080',
                 100152 : 'AP030',
                 179969 : 'AP033',
                 100253 : 'BC050',
                 100341 : 'BJ030',
                 100337 : 'BI050',
                 100094 : 'AL036',
                 100256 : 'BC070',
                 100309 : 'BH100',
                 100111 : 'AL142',
                 100026 : 'AF020',
                 100089 : 'AL020',
                 100384 : 'EA040',
                 100172 : 'AQ070',
                 100366 : 'DB070',
                 100091 : 'AL025',
                 100019 : 'AD020',
                 100144 : 'AN050',
                 100020 : 'AD025',
                 100315 : 'BH145',
                 100387 : 'EB010',
                 100106 : 'AL120',
                 100065 : 'AK120',
                 100066 : 'AK121',
                 100010 : 'AB040',
                 132596 : 'AH025',
                 121638 : 'AG050',
                 100154 : 'AP040',
                 100347 : 'BJ080',
                 121747 : 'AK161',
                 100394 : 'EC020',
                 100317 : 'BH155',
                 100086 : 'AL017',
                 100297 : 'BH020',
                 100084 : 'AL014',
                 100083 : 'AL013',
                 100082 : 'AL012',
                 100081 : 'AL011',
                 100080 : 'AL010',
                 100131 : 'AM010',
                 100409 : 'FA012',
                 100088 : 'AL019',
                 100123 : 'AL250',
                 100410 : 'FA015',
                 100087 : 'AL018',
                 100371 : 'DB115',
                 100112 : 'AL155',
                 100192 : 'AQ151',
                 100370 : 'DB110',
                 100012 : 'AC010',
                 100155 : 'AP041',
                 100243 : 'BB199',
                 131206 : 'BI045',
                 100325 : 'BH220',
                 100334 : 'BI040',
                 100038 : 'AH060',
                 100180 : 'AQ114',
                 100231 : 'BB081',
                 100189 : 'AQ140',
                 100313 : 'BH135',
                 100171 : 'AQ068',
                 100358 : 'DA010',
                 100064 : 'AK110',
                 100030 : 'AF050',
                 100018 : 'AD010',
                 100462 : 'SU001',
                 100444 : 'GB045',
                 100348 : 'BJ099',
                 100443 : 'GB040',
                 170162 : 'SU004',
                 100456 : 'GB230',
                 100245 : 'BB241',
                 100381 : 'EA020',
                 100298 : 'BH030',
                 100326 : 'BH230',
                 100457 : 'GB250',
                 100277 : 'BD140',
                 100386 : 'EA055',
                 100046 : 'AJ055',
                 100150 : 'AP010',
                 100008 : 'AB010',
                 100375 : 'DB180',
                 100122 : 'AL241',
                 100138 : 'AM065',
                 100393 : 'EC010',
                 100013 : 'AC020',
                 100062 : 'AK100',
                 100063 : 'AK101',
                 100369 : 'DB100',
                 130380 : 'EC015',
                 100052 : 'AJ110',
                 100167 : 'AQ060',
                 130381 : 'AQ063',
                 100168 : 'AQ062',
                 100170 : 'AQ065',
                 100137 : 'AM060',
                 100403 : 'EE030',
                 100057 : 'AK060',
                 100217 : 'BA030',
                 100147 : 'AN076',
                 100146 : 'AN075',
                 100311 : 'BH120',
                 100244 : 'BB201',
                 100149 : 'AN085',
                 100454 : 'GB075',
                 100029 : 'AF040',
                 100356 : 'DA005',
                 100441 : 'GB030',
                 100696 : 'AA045',
                 100442 : 'GB035',
                 100302 : 'BH070',
                 100103 : 'AL099',
                 100004 : 'AA040',
                 100458 : 'IA040',
                 100078 : 'AK180',
                 100382 : 'EA030',
                 100383 : 'EA031',
                 100340 : 'BJ020',
                 100003 : 'AA020',
                 154961 : 'DB029',
                 154959 : 'DB028',
                 100073 : 'AK155',
                 100129 : 'AL270',
                 100328 : 'BI005',
                 100007 : 'AB000',
                 100377 : 'DB190',
                 100388 : 'EB020',
                 100077 : 'AK170',
                 100197 : 'AQ170',
                 100379 : 'DB211',
                 100098 : 'AL070',
                 100099 : 'AL073',
                 100059 : 'AK070',
                 100688 : 'AL175',
                 100330 : 'BI020',
                 100141 : 'AM075',
                 100114 : 'AL170',
                 179906 : 'AP055',
                 100139 : 'AM070',
                 100173 : 'AQ075',
                 100025 : 'AF010',
                 100236 : 'BB110',
                 100196 : 'AQ162',
                 100032 : 'AF070',
                 100145 : 'AN060',
                 100187 : 'AQ130',
                 100142 : 'AM080',
                 100207 : 'AT045',
                 100006 : 'AA052',
                 155023 : 'AA054',
                 100206 : 'AT041',
                 100558 : 'AT042',
                 100101 : 'AL080',
                 100039 : 'AH070',
                 100416 : 'FA165',
                 134665 : 'AC507',
                 100191 : 'AQ150'
}

fc_fields_og = { 'AeronauticCrv' : ['F_CODE','FCSUBTYPE','AXS','PCF','SBB','TXP','ZI005_FNA','ZI006_MEM','ZI019_ASP','ZI019_ASP2','ZI019_ASP3','ZI019_ASU','ZI019_ASU2','ZI019_ASU3','ZI019_ASX','ZI019_SFS','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'AeronauticPnt' : ['F_CODE','FCSUBTYPE','APT','APT2','APT3','AXS','FFN','FFN2','FFN3','FPT','HAF','HGT','LMC','MCC','MCC2','MCC3','PCF','PEC','TRS','TRS2','TRS3','ZI005_FNA','ZI006_MEM','ZI019_ASP','ZI019_ASP2','ZI019_ASP3','ZI019_ASU','ZI019_ASU2','ZI019_ASU3','ZI019_ASX','ZI019_SFS','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'AeronauticSrf' : ['F_CODE','FCSUBTYPE','APT','APT2','APT3','APU','APU2','APU3','ASU','ASU2','ASU3','AXS','FFN','FFN2','FFN3','FPT','HAF','HGT','LMC','MCC','MCC2','MCC3','PCF','PEC','SBB','TRS','TRS2','TRS3','TXP','ZI005_FNA','ZI006_MEM','ZI019_ASP','ZI019_ASP2','ZI019_ASP3','ZI019_ASU','ZI019_ASU2','ZI019_ASU3','ZI019_ASX','ZI019_SFS','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'AgriculturePnt' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI013_CSP','ZI013_CSP2','ZI013_CSP3','ZI013_PIG','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'AgricultureSrf' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI013_CSP','ZI013_CSP2','ZI013_CSP3','ZI013_PIG','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'BoundaryPnt' : ['F_CODE','FCSUBTYPE','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'CultureCrv' : ['F_CODE','FCSUBTYPE','HGT','LMC','PCF','SSC','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'CulturePnt' : ['F_CODE','FCSUBTYPE','HGT','LMC','PCF','SSC','TTY','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI037_REL','ZI001_SRT','Shape','Version'],
              'CultureSrf' : ['F_CODE','FCSUBTYPE','CAM','HGT','LMC','PCF','SSC','TTY','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI037_REL','ZI037_RFA','ZI001_SRT','Shape','Version'],
              'FacilityPnt' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI037_REL','ZI037_RFA','ZI001_SRT','Shape','Version'],
              'FacilitySrf' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI037_REL','ZI037_RFA','ZI001_SRT','Shape','Version'],
              'HydroAidNavigationPnt' : ['F_CODE','FCSUBTYPE','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'HydroAidNavigationSrf' : ['F_CODE','FCSUBTYPE','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'HydrographyCrv' : ['F_CODE','FCSUBTYPE','ATC','CDA','CWT','DFT','DFU','FCS','HGT','LMC','LOC','MCC','MCC2','MCC3','NVS','PCF','RLE','SBB','TID','TRS','TRS2','TRS3','WCC','WOC','ZI005_FNA','ZI006_MEM','ZI024_HYP','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'HydrographyPnt' : ['F_CODE','FCSUBTYPE','AZC','DFT','DFU','DMD','DOF','FCS','HGT','IWT','LMC','MCC','MCC2','MCC3','MNS','OCS','PCF','TID','TRS','TRS2','TRS3','WOC','WST','ZI005_FNA','ZI006_MEM','ZI024_HYP','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'HydrographySrf' : ['F_CODE','FCSUBTYPE','ATC','AZC','CDA','CWT','DFT','DFU','DMD','FCS','HGT','INU','IWT','LMC','LOC','MCC','MCC2','MCC3','MNS','NVS','OCS','PCF','RLE','SBB','TID','TRS','TRS2','TRS3','WCC','WOC','ZI005_FNA','ZI006_MEM','ZI024_HYP','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'IndustryCrv' : ['F_CODE','FCSUBTYPE','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'IndustryPnt' : ['F_CODE','FCSUBTYPE','CRA','CRM','FFN','FFN2','FFN3','HGT','LMC','LOC','PBY','PBY2','PBY3','PCF','PPO','PPO2','PPO3','RIP','SRL','TRS','TRS2','TRS3','ZI005_FNA','ZI006_MEM','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'IndustrySrf' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','LOC','PBY','PBY2','PBY3','PCF','PPO','PPO2','PPO3','SRL','ZI005_FNA','ZI006_MEM','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'InformationCrv' : ['F_CODE','FCSUBTYPE','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'InformationPnt' : ['F_CODE','FCSUBTYPE','NLT','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'InformationSrf' : ['F_CODE','FCSUBTYPE','VCA','VCA2','VCA3','VCT','VCT2','VCT3','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'MilitaryCrv' : ['F_CODE','FCSUBTYPE','EET','HGT','LMC','MCC','MCC2','MCC3','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'MilitaryPnt' : ['F_CODE','FCSUBTYPE','CAA','FFN','FFN2','FFN3','HGT','LMC','MCC','MCC2','MCC3','PCF','PPO','PPO2','PPO3','RLE','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'MilitarySrf' : ['F_CODE','FCSUBTYPE','CAA','EET','FFN','FFN2','FFN3','HGT','LMC','MCC','MCC2','MCC3','PCF','PPO','PPO2','PPO3','RLE','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'PhysiographyCrv' : ['F_CODE','FCSUBTYPE','AZC','FIC','GFT','HGT','LMC','MCC','MCC2','MCC3','PCF','TRS','TRS2','TRS3','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'PhysiographyPnt' : ['F_CODE','FCSUBTYPE','GOT','HGT','LMC','MCC','MCC2','MCC3','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'PhysiographySrf' : ['F_CODE','FCSUBTYPE','FIC','GOT','HGT','LMC','MCC','MCC2','MCC3','PCF','SAD','SDO','SDT','SIC','TRS','TRS2','TRS3','TSM','TSM2','TSM3','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'PortHarbourCrv' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','MCC','MCC2','MCC3','PCF','PWC','WLE','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'PortHarbourPnt' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','MCC','MCC2','MCC3','PCF','TID','ZI005_FNA','ZI006_MEM','ZI025_WLE','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'PortHarbourSrf' : ['F_CODE','FCSUBTYPE','FFN','FFN2','FFN3','HGT','LMC','MCC','MCC2','MCC3','PCF','PWC','TID','WLE','ZI005_FNA','ZI006_MEM','ZI025_WLE','ZI026_CTUU','ZI001_SRT','SHAPE_Area','Shape','Version'],
              'RecreationCrv' : ['F_CODE','FCSUBTYPE','AMA','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'RecreationPnt' : ['F_CODE','FCSUBTYPE','AMA','FFN','FFN2','FFN3','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'RecreationSrf' : ['F_CODE','FCSUBTYPE','AMA','FFN','FFN2','FFN3','HGT','LMC','PCF','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'SettlementPnt' : ['F_CODE','FCSUBTYPE','BAC','FFN','FFN2','FFN3','LMC','PCF','ZI005_FNA','ZI005_FNA2','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'SettlementSrf' : ['F_CODE','FCSUBTYPE','BAC','FFN','FFN2','FFN3','LMC','PCF','ZI005_FNA','ZI005_FNA2','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'StoragePnt' : ['F_CODE','FCSUBTYPE','CBP','FFN','FFN2','FFN3','HGT','LMC','LUN','PCF','PPO','PPO2','PPO3','SPT','SSC','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'StorageSrf' : ['F_CODE','FCSUBTYPE','CBP','FFN','FFN2','FFN3','HGT','LMC','LUN','PCF','PPO','PPO2','PPO3','SPT','SSC','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'StructureCrv' : ['F_CODE','FCSUBTYPE','BSU','HGT','LMC','PCF','WTI','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'StructurePnt' : ['F_CODE','FCSUBTYPE','BSU','CRM','FFN','FFN2','FFN3','HGT','LMC','PCF','RLE','TOS','TTC','TTC2','TTC3','ZI005_FNA','ZI006_MEM','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI037_REL','ZI037_RFA','ZI001_SRT','Shape','Version'],
              'StructureSrf' : ['F_CODE','FCSUBTYPE','BSU','FFN','FFN2','FFN3','HGT','LMC','PCF','RLE','TOS','TTC','TTC2','TTC3','ZI005_FNA','ZI006_MEM','ZI014_PPO','ZI014_PPO2','ZI014_PPO3','ZI026_CTUU','ZI037_REL','ZI037_RFA','Shape','Version'],
              'TransportationGroundCrv' : ['F_CODE','FCSUBTYPE','ACC','BOT','BSC','BSC2','BSC3','CAT','CWT','FCO','FFN','FFN2','FFN3','GTC','HGT','LOC','LTN','MCC','MCC2','MCC3','MES','ONE','OWO','PCF','RFD','RIN_ROI','RIN_ROI2','RIN_ROI3','RIN_RTN','RIN_RTN2','RIN_RTN3','RLE','ROR','RRC','RRC2','RRC3','RSA','RTA','RTY','RWC','SBB','SEP','TRA','TRP','TRS','TRS2','TRS3','TST','WLE','ZI005_FNA','ZI006_MEM','ZI016_ROC','ZI016_WD1','ZI016_WTC','ZI017_GAW','ZI017_RGC','ZI017_RIR','ZI017_RRA','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'TransportationGroundPnt' : ['F_CODE','FCSUBTYPE','BOT','BSC','BSC2','BSC3','CWT','DGC','FFN','FFN2','FFN3','GTC','HGT','LMC','MCC','MCC2','MCC3','MES','PCF','PYM','RFD','RIN_ROI','RIN_ROI2','RIN_ROI3','RIN_RTN','RIN_RTN2','RIN_RTN3','TRP','TRS','TRS2','TRS3','ZI005_FNA','ZI006_MEM','ZI016_ROC','ZI016_WTC','ZI017_GAW','ZI017_RGC','ZI017_RRA','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'TransportationGroundSrf' : ['F_CODE','FCSUBTYPE','BOT','BSC','BSC2','BSC3','DGC','FFN','FFN2','FFN3','HGT','LMC','LTN','MCC','MCC2','MCC3','PCF','RFD','TRA','TRP','TRS','TRS2','TRS3','VET','WLE','ZI005_FNA','ZI006_MEM','ZI016_ROC','ZI017_GAW','ZI017_RGC','ZI017_RRA','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'TransportationWaterCrv' : ['F_CODE','FCSUBTYPE','CDA','CWT','FER','HGT','LMC','LOC','PCF','RLE','SBB','TRS','TRS2','TRS3','ZI005_FNA','ZI006_MEM','ZI024_HYP','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'TransportationWaterPnt' : ['F_CODE','FCSUBTYPE','HGT','LMC','PCF','TRS','TRS2','TRS3','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'TransportationWaterSrf' : ['F_CODE','FCSUBTYPE','CDA','CWT','HGT','LMC','LOC','PCF','RLE','SBB','TRS','TRS2','TRS3','ZI005_FNA','ZI006_MEM','ZI024_HYP','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'UtilityInfrastructureCrv' : ['F_CODE','FCSUBTYPE','CAB','CAB2','CAB3','CST','CWT','HGT','LOC','OWO','PCF','PLT','PLT2','PLT3','PPO','PPO2','PPO3','RLE','RTA','SPT','TST','ZI005_FNA','ZI006_MEM','ZI020_GE4','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'UtilityInfrastructurePnt' : ['F_CODE','FCSUBTYPE','AT005_CAB','AT005_CAB2','AT005_CAB3','HGT','LMC','PCF','POS','POS2','POS3','PPO','PPO2','PPO3','SRL','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI032_PYC','ZI032_PYM','ZI032_TOS','ZI001_SRT','Shape','Version'],
              'UtilityInfrastructureSrf' : ['F_CODE','FCSUBTYPE','HGT','LMC','PCF','POS','POS2','POS3','PPO','PPO2','PPO3','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'VegetationCrv' : ['F_CODE','FCSUBTYPE','DMT','LMC','SBC','TRE','ZI005_FNA','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'VegetationPnt' : ['F_CODE','FCSUBTYPE','HGT','LMC','TRE','ZI006_MEM','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'VegetationSrf' : ['F_CODE','FCSUBTYPE','DMT','HGT','LMC','SBC','TID','TRE','VEG','VSP','VSP2','VSP3','ZI005_FNA','ZI006_MEM','ZI024_HYP','ZI026_CTUU','ZI001_SRT','Shape','Version'],
              'MetadataSrf' : ['F_CODE','FCSUBTYPE','MDE','RCG','ZI001_SRT','Shape','Version'],
              'ResourceSrf' : ['F_CODE','FCSUBTYPE','AVA','CID','CPS','DQS','ETS','ETZ','EVA','HVA','HZD','MDE','MEM','RCG','RTL','VDT','Shape','Version']
}

fc_fields = { 'AeronauticCrv' : ['f_code','fcsubtype','ara','axs','lzn','pcf','sbb','txp','zi005_fna','zi006_mem','zi019_asp','zi019_asp2','zi019_asp3','zi019_asu','zi019_asu2','zi019_asu3','zi019_asx','zi019_sfs','zi026_ctuu','zi001_srt','shape@','version'],
              'AeronauticPnt' : ['f_code','fcsubtype','apt','apt2','apt3','ara','axs','ffn','ffn2','ffn3','fpt','haf','hgt','lmc','mcc','mcc2','mcc3','pcf','pec','trs','trs2','trs3','zi005_fna','zi006_mem','zi019_asp','zi019_asp2','zi019_asp3','zi019_asu','zi019_asu2','zi019_asu3','zi019_asx','zi019_sfs','zi026_ctuu','zi001_srt','shape@','version'],
              'AeronauticSrf' : ['f_code','fcsubtype','apt','apt2','apt3','apu','apu2','apu3','ara','asu','asu2','asu3','axs','ffn','ffn2','ffn3','fpt','haf','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','pec','sbb','trs','trs2','trs3','txp','wid','zi005_fna','zi006_mem','zi019_asp','zi019_asp2','zi019_asp3','zi019_asu','zi019_asu2','zi019_asu3','zi019_asx','zi019_sfs','zi026_ctuu','zi001_srt','shape@','version'],
              'AgriculturePnt' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','pcf','zi005_fna','zi006_mem','zi013_csp','zi013_csp2','zi013_csp3','zi013_pig','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'AgricultureSrf' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi013_csp','zi013_csp2','zi013_csp3','zi013_pig','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'BoundaryPnt' : ['f_code','fcsubtype','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'CultureCrv' : ['f_code','fcsubtype','ara','hgt','lmc','lzn','pcf','ssc','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'CulturePnt' : ['f_code','fcsubtype','ara','hgt','lmc','pcf','ssc','tty','zi005_fna','zi006_mem','zi026_ctuu','zi037_rel','zi001_srt','shape@','version'],
              'CultureSrf' : ['f_code','fcsubtype','ara','cam','hgt','lmc','lzn','pcf','ssc','tty','wid','zi005_fna','zi006_mem','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'FacilityPnt' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','pcf','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'FacilitySrf' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'HydroAidNavigationPnt' : ['f_code','fcsubtype','ara','hgt','lmc','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'HydroAidNavigationSrf' : ['f_code','fcsubtype','ara','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'HydrographyCrv' : ['f_code','fcsubtype','aoo','ara','atc','cda','cwt','dft','dfu','fcs','hgt','lmc','loc','lzn','mcc','mcc2','mcc3','nvs','pcf','rle','sbb','tid','trs','trs2','trs3','wcc','wid','woc','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'HydrographyPnt' : ['f_code','fcsubtype','aoo','azc','dft','dfu','dmd','dof','fcs','hgt','iwt','lmc','mcc','mcc2','mcc3','mns','ocs','pcf','tid','trs','trs2','trs3','woc','wst','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'HydrographySrf' : ['f_code','fcsubtype','aoo','ara','atc','azc','cda','cwt','dft','dfu','dmd','fcs','hgt','inu','iwt','lmc','loc','lzn','mcc','mcc2','mcc3','mns','nvs','ocs','pcf','rle','sbb','tid','trs','trs2','trs3','wcc','wid','woc','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'IndustryCrv' : ['f_code','fcsubtype','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'IndustryPnt' : ['f_code','fcsubtype','cra','crm','ffn','ffn2','ffn3','hgt','lmc','loc','pby','pby2','pby3','pcf','ppo','ppo2','ppo3','rip','srl','trs','trs2','trs3','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'IndustrySrf' : ['f_code','fcsubtype','ara','ffn','ffn2','ffn3','hgt','lmc','loc','lzn','pby','pby2','pby3','pcf','ppo','ppo2','ppo3','srl','wid','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi001_srt','shape@','version'],
              'InformationCrv' : ['f_code','fcsubtype','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'InformationPnt' : ['f_code','fcsubtype','nlt','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'InformationSrf' : ['f_code','fcsubtype','ara','lzn','vca','vca2','vca3','vct','vct2','vct3','wid','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'MilitaryCrv' : ['f_code','fcsubtype','eet','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'MilitaryPnt' : ['f_code','fcsubtype','caa','ffn','ffn2','ffn3','hgt','lmc','mcc','mcc2','mcc3','pcf','ppo','ppo2','ppo3','rle','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'MilitarySrf' : ['f_code','fcsubtype','ara','caa','eet','ffn','ffn2','ffn3','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','ppo','ppo2','ppo3','rle','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PhysiographyCrv' : ['f_code','fcsubtype','azc','fic','gft','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','trs','trs2','trs3','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PhysiographyPnt' : ['f_code','fcsubtype','aoo','got','hgt','lmc','mcc','mcc2','mcc3','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PhysiographySrf' : ['f_code','fcsubtype','aoo','ara','fic','got','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','sad','sdo','sdt','sic','trs','trs2','trs3','tsm','tsm2','tsm3','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PortHarbourCrv' : ['f_code','fcsubtype','ffn','ffn2','ffn3','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','pwc','wle','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'PortHarbourPnt' : ['f_code','fcsubtype','ffn','ffn2','ffn3','hgt','lmc','mcc','mcc2','mcc3','pcf','tid','zi005_fna','zi006_mem','zi025_wle','zi026_ctuu','zi001_srt','shape@','version'],
              'PortHarbourSrf' : ['f_code','fcsubtype','ffn','ffn2','ffn3','hgt','lmc','lzn','mcc','mcc2','mcc3','pcf','pwc','tid','wid','wle','zi005_fna','zi006_mem','zi025_wle','zi026_ctuu','zi001_srt','shape@','version'],
              'RecreationCrv' : ['f_code','fcsubtype','ama','hgt','lmc','lzn','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'RecreationPnt' : ['f_code','fcsubtype','ama','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'RecreationSrf' : ['f_code','fcsubtype','ama','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'SettlementPnt' : ['f_code','fcsubtype','bac','ffn','ffn2','ffn3','lmc','pcf','zi005_fna','zi005_fna2','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'SettlementSrf' : ['f_code','fcsubtype','ara','bac','ffn','ffn2','ffn3','lmc','lzn','pcf','wid','zi005_fna','zi005_fna2','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StoragePnt' : ['f_code','fcsubtype','cbp','ffn','ffn2','ffn3','hgt','lmc','lun','pcf','ppo','ppo2','ppo3','spt','ssc','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StorageSrf' : ['f_code','fcsubtype','ara','cbp','ffn','ffn2','ffn3','hgt','lmc','lun','lzn','pcf','ppo','ppo2','ppo3','spt','ssc','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StructureCrv' : ['f_code','fcsubtype','bsu','hgt','lmc','lzn','pcf','wti','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'StructurePnt' : ['f_code','fcsubtype','bsu','crm','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','rle','tos','ttc','ttc2','ttc3','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','zi001_srt','shape@','version'],
              'StructureSrf' : ['f_code','fcsubtype','ara','bsu','ffn','ffn2','ffn3','hgt','lmc','lzn','pcf','rle','tos','ttc','ttc2','ttc3','wid','zi005_fna','zi006_mem','zi014_ppo','zi014_ppo2','zi014_ppo3','zi026_ctuu','zi037_rel','zi037_rfa','shape@','version'],
              'TransportationGroundCrv' : ['f_code','fcsubtype','acc','bot','bsc','bsc2','bsc3','cat','cwt','fco','ffn','ffn2','ffn3','gtc','hgt','loc','ltn','lzn','mcc','mcc2','mcc3','mes','one','owo','pcf','rfd','rin_roi','rin_roi2','rin_roi3','rin_rtn','rin_rtn2','rin_rtn3','rle','ror','rrc','rrc2','rrc3','rsa','rta','rty','rwc','sbb','sep','tra','trp','trs','trs2','trs3','tst','wid','wle','zi005_fna','zi006_mem','zi016_roc','zi016_wd1','zi016_wtc','zi017_gaw','zi017_rgc','zi017_rir','zi017_rra','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationGroundPnt' : ['f_code','fcsubtype','bot','bsc','bsc2','bsc3','cwt','dgc','ffn','ffn2','ffn3','gtc','hgt','lmc','mcc','mcc2','mcc3','mes','pcf','pym','rfd','rin_roi','rin_roi2','rin_roi3','rin_rtn','rin_rtn2','rin_rtn3','trp','trs','trs2','trs3','wid','zi005_fna','zi006_mem','zi016_roc','zi016_wtc','zi017_gaw','zi017_rgc','zi017_rra','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationGroundSrf' : ['f_code','fcsubtype','ara','bot','bsc','bsc2','bsc3','dgc','ffn','ffn2','ffn3','hgt','lmc','ltn','lzn','mcc','mcc2','mcc3','pcf','rfd','tra','trp','trs','trs2','trs3','vet','wid','wle','zi005_fna','zi006_mem','zi016_roc','zi017_gaw','zi017_rgc','zi017_rra','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationWaterCrv' : ['f_code','fcsubtype','aoo','cda','cwt','fer','hgt','lmc','loc','lzn','pcf','rle','sbb','trs','trs2','trs3','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationWaterPnt' : ['f_code','fcsubtype','aoo','hgt','lmc','pcf','trs','trs2','trs3','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'TransportationWaterSrf' : ['f_code','fcsubtype','aoo','ara','cda','cwt','hgt','lmc','loc','lzn','pcf','rle','sbb','trs','trs2','trs3','wid','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'UtilityInfrastructureCrv' : ['f_code','fcsubtype','cab','cab2','cab3','cst','cwt','hgt','loc','lzn','owo','pcf','plt','plt2','plt3','ppo','ppo2','ppo3','rle','rta','spt','tst','zi005_fna','zi006_mem','zi020_ge4','zi026_ctuu','zi001_srt','shape@','version'],
              'UtilityInfrastructurePnt' : ['f_code','fcsubtype','at005_cab','at005_cab2','at005_cab3','hgt','lmc','pcf','pos','pos2','pos3','ppo','ppo2','ppo3','srl','zi005_fna','zi006_mem','zi026_ctuu','zi032_pyc','zi032_pym','zi032_tos','zi001_srt','shape@','version'],
              'UtilityInfrastructureSrf' : ['f_code','fcsubtype','ara','hgt','lmc','lzn','pcf','pos','pos2','pos3','ppo','ppo2','ppo3','wid','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'VegetationCrv' : ['f_code','fcsubtype','dmt','lmc','lzn','sbc','tre','zi005_fna','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'VegetationPnt' : ['f_code','fcsubtype','hgt','lmc','tre','zi006_mem','zi026_ctuu','zi001_srt','shape@','version'],
              'VegetationSrf' : ['f_code','fcsubtype','ara','dmt','hgt','lmc','lzn','sbc','tid','tre','veg','vsp','vsp2','vsp3','wid','zi005_fna','zi006_mem','zi024_hyp','zi026_ctuu','zi001_srt','shape@','version'],
              'MetadataSrf' : ['f_code','fcsubtype','mde','rcg','zi001_srt','shape@','version'],
              'ResourceSrf' : ['f_code','fcsubtype','ava','cid','cps','dqs','ets','etz','eva','hva','hzd','mde','mem','rcg','rtl','vdt','shape@','version']
}

# Important FFN List from Leidos
ffn_list_all = OrderedDict([
                ('    Public Administration', 808),
				('        - Government', 811),
				('            > National Government', 814),
				('            > Subnational Government', 813),
				('            > Local Government', 812),
				('            > Executive Activities', 818),
				('            > Legislative Activities', 819),
				('            > Civil Activities', 822),
				('            > Capitol', 817),
				('            > Palace', 815),
				('            > Polling Station', 821),
				('        - Diplomacy', 825),
				('            > Consul', 828),
				('            > Diplomatic Mission', 826),
				('            > Embassy', 827),
				('        - Defence Activities', 835),
				('            > Armory', 836),
				('            > Maritime Defense', 829),
				('            > Military Recruitment', 838),
				('            > Military Reserve Activities', 837),
				('    Public Order, Safety and Security Services', 830),
				('        - Public Order', 831),
				('            > Immigration Control', 842),
				('            > Imprisonment', 843),
				('            > Judicial Activities', 840),
				('            > Juvenile Corrections', 844),
				('            > Law Enforcement', 841),
				('        - Safety', 832),
				('            > Firefighting', 845),
				('            > Rescue and Paramedical Services', 846),
				('            > Emergency Operations', 847),
				('            > Emergency Relief Services', 888),
				('            > Civil Intelligence', 848),
				('            > CBRNE Civilian Support', 839),
				('        - Security Services', 833),
				('            > Guard', 781),
				('            > Security Enforcement', 780),
				('    Education', 850),
				('        - Primary Education', 851),
				('        - Secondary Education', 852),
				('        - Higher Education', 855),
				('        - Vocational Education', 857),
				('    Human Health Activities', 860),
				('        - In-patient Care', 861),
				('            > Intermediate Care', 871),
				('            > Psychiatric In-patient Care', 873),
				('            > Residential Care', 875),
				('        - Out-patient Care', 862),
				('            > Urgent Medical Care', 863),
				('        - Human Tissue Repository', 864),
				('        - Leprosy Care', 866),
				('        - Public Health Activities', 865),
				('    Cultural, Arts, and Entertainment', 890),
				('        - Aquarium', 906),
				('        - Auditorium', 892),
				('        - Botanical and/or Zoological Reserve Activities', 907),
				('        - Cinema', 594),
				('        - Library', 902),
				('        - Museum', 905),
				('        - Night Club', 895),
				('        - Opera House', 894),
				('        - Theatre', 891),
				('    Utilities', 350),
				('        - Power Generation', 351),
				('        - Climate Control', 352),
				('            > Cooling', 355),
				('            > Heating', 356),
				('        - Water Supply', 360),
				('            > Water Collection', 361),
				('            > Water Treatment', 362),
				('            > Water Distribution', 363),
				('        - Sewerage', 370),
				('            > Sewerage Screening', 372),
				('            > Restroom', 382),
				('        - Waste Treatment and Disposal', 383),
				('        - Materials Recovery', 385),
				('    Transport', 480),
				('        - Transportation Hub', 489),
				('            > Station', 482),
				('            > Stop', 483),
				('            > Terminal', 481),
				('            > Transfer Hub', 484),
				('        - Railway Transport', 490),
				('            > Railway Passenger Transport', 491),
				('        - Pedestrian Transport', 494),
				('        - Road Transport', 495),
				('            > Road Freight Transport', 497),
				('            > Road Passenger Transport', 496),
				('        - Pipeline Transport', 500),
				('            > Pumping', 501),
				('        - Water Transport', 505),
				('            > Inland Waters Transport', 507),
				('            > Canal Transport', 508),
				('            > Harbour Control', 513),
				('            > Port Control', 510),
				('            > Maritime Pilotage', 511),
				('            > Pilot Station', 512),
				('        - Air Transport', 520),
				('            > Air Traffic Control', 525),
				('        - Mail and Package Transport', 541),
				('            > Postal Activities', 540),
				('            > Courier Activities', 545),
				('        - Transportation Support', 529),
				('            > Navigation', 488),
				('            > Signalling', 486),
				('            > Transport System Maintenance', 487),
				('            > Warehousing and Storage', 530),
				('            > Cargo Handling', 536),
				('            > Motor Vehicle Parking', 535),
				('            > Inspection', 539),
				('            > Customs Checkpoint', 537),
				('            > Inspection Station', 538),
				('            > Hotel', 551),
				('            > Resort', 552),
				('            > Radio Broadcasting', 601),
				('            > Television Broadcasting', 604),
				('        - Refugee Shelter', 883),
				('    Religious Activities', 930),
				('        - Place of Worship', 931),
				('        - Islamic Prayer Hall', 932),
				('    Meeting Place', 970),
				('        - Community Centre', 893),
				('        - Convention Centre', 579)
])

ffn_list_caci = OrderedDict([
 				('    Public Administration', 808),
				('        - Government', 811),
				('            > National Government', 814),
				('            > Subnational Government', 813),
				('            > Local Government', 812),
				('            > Executive Activities', 818),
				('            > Legislative Activities', 819),
				('            > Civil Activities', 822),
				('            > Capitol', 817),
				('            > Palace', 815),
				('            > Polling Station', 821),
				('        - Diplomacy', 825),
				('            > Consul', 828),
				('            > Diplomatic Mission', 826),
				('            > Embassy', 827),
				('        - Defence Activities', 835),
				('            > Armory', 836),
				('            > Maritime Defense', 829),
				('            > Military Recruitment', 838),
				('            > Military Reserve Activities', 837),
				('    Education', 850),
				('        - Primary Education', 851),
				('        - Secondary Education', 852),
				('        - Higher Education', 855),
				('        - Vocational Education', 857),
				('    Human Health Activities', 860),
				('        - In-patient Care', 861),
				('            > Intermediate Care', 871),
				('            > Psychiatric In-patient Care', 873),
				('            > Residential Care', 875),
				('        - Out-patient Care', 862),
				('            > Urgent Medical Care', 863),
				('        - Human Tissue Repository', 864),
				('        - Leprosy Care', 866),
				('        - Public Health Activities', 865),
				('    Religious Activities', 930),
				('        - Place of Worship', 931),
				('        - Islamic Prayer Hall', 932)
])


''''''''' User Parameters '''''''''
TDS = arcpy.GetParameterAsText(0)
arcpy.env.workspace = TDS
workspace = os.path.dirname(arcpy.env.workspace)
arcpy.env.overwriteOutput = True
vogon = arcpy.GetParameter(1) # Skips large building datasets
repair = arcpy.GetParameter(2)
fcode = arcpy.GetParameter(3)
defaults = arcpy.GetParameter(4)
metrics = arcpy.GetParameter(5)
ufi = arcpy.GetParameter(6)
large = arcpy.GetParameter(7) # Running chunk processing for integrating large datasets
hydro = arcpy.GetParameter(8)
trans = arcpy.GetParameter(9)
util = arcpy.GetParameter(10)
dups = arcpy.GetParameter(11)
explode = arcpy.GetParameter(12)
bridge = arcpy.GetParameter(13)
pylong = arcpy.GetParameter(14)
building = arcpy.GetParameter(15) # Be sure to add Structure Srf and Pnt back if vogon is checked
swap = arcpy.GetParameter(16)
fcount = arcpy.GetParameter(17)
vsource = arcpy.GetParameter(18)
#sdepull = arcpy.GetParameter(19)
#dataload = arcpy.GetParameter(20)
secret = arcpy.GetParameter(19) ### update index as needed
error_count = 0
featureclass = arcpy.ListFeatureClasses()

# argv = tuple(ap.GetParameterAsText(i)
# for i in range(ap.GetArgumentCount()))



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Title Formatting and Workspace Setup #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Sanitizing GDB name
tds_split = TDS.split("\\")
tds_split.pop()
rresults = tds_split
gdb_file = tds_split.pop()
name_list = gdb_file.split(".")
name_list.pop()
gdb_name = name_list[0]
#rresults.pop()
rresults = "\\".join(rresults)


# Tool title with GDB name formatting
write("")
slines = u"______________________________________"
sspaces = u"                                      "
exl = ""
exs = ""
exgl = "" # odd left dominant
exgr = ""
range_len = 38 - len(gdb_name)
if range_len > 0:
	if (range_len % 2) == 0:
		rn0 = range_len/2
		for i in range(int(rn0)):
			exgl += " "
			exgr += " "
	else:
		rn1 = int(float(range_len)/2)
		for i in range(rn1):
			exgl += " "
		rn2 = rn1 + 1
		for i in range(int(rn2)):
			exgr += " "
if len(gdb_name) > 38:
	extra = len(gdb_name) - 38

	for i in range(extra):
		exl += "_"
		exs += " "


# Report of requested tasks
write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

if secret:
	write(u"    |          By order of the Liberator         {0}|".format(exs))
	write(u"    |        The leader of the free people       {0}|".format(exs))
	write(u"    |      _______        _                      {0}|".format(exs))
	write(u"    |     / ___/ /  ___ _(_)_____ _  ___ ____    {0}|".format(exs))
	write(u"    |    / /__/ _ \/ _ `/ / __/  ' \/ _ `/ _ \   {0}|".format(exs))
	write(u"    |    \___/_//_/\_,_/_/_/ /_/_/_/\_,_/_//_/   {0}|".format(exs))
	write(u"    |               ___           __             {0}|".format(exs))
	write(u"    |              / _ )___  ____/ /__           {0}|".format(exs))
	write(u"    |             / _  / _ \/ __/  '_/           {0}|".format(exs))
	write(u"    |            /____/\___/\__/_/\_\            {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |        The following Finishing tasks       {0}|".format(exs))
	write(u"    |              shall be executed             {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))

write(u"    |   ======  Processes  Initialized  ======   {0}|".format(exs))
write(u"    |   {0}   {1}|".format(sspaces, exs))
if repair:
	write(u"    |     - Repair All NULL Geometries           {0}|".format(exs))
if fcode:
	write(u"    |     - Populate F_Codes                     {0}|".format(exs))
if defaults:
	write(u"    |     - Calculate Default Values             {0}|".format(exs))
if metrics:
	write(u"    |     - Calculate Metrics                    {0}|".format(exs))
if ufi:
	write(u"    |     - Update UFI Values                    {0}|".format(exs))
if hydro or trans or util:
	write(u"    |     - Integrate and Repair:                {0}|".format(exs))
	if large:
		write(u"    |        ~ Large Dataset ~                   {0}|".format(exs))
	if hydro:
		write(u"    |          Hydro                             {0}|".format(exs))
	if trans:
		write(u"    |          Trans                             {0}|".format(exs))
	if util:
		write(u"    |          Utilities                         {0}|".format(exs))
if dups:
	write(u"    |     - Delete Identical Features            {0}|".format(exs))
if explode:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
if bridge:
	write(u"    |     - Default Bridge WID Updater           {0}|".format(exs))
if pylong:
	write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
if building:
	write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
if swap:
	write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
if fcount:
	write(u"    |     - Generate Feature Report              {0}|".format(exs))
if vsource:
	write(u"    |     - Generate Source Report               {0}|".format(exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")


# Formatting Feature Class list
if arcpy.Exists('MetadataSrf'):
	featureclass.remove('MetadataSrf')
	write("MetadataSrf removed")
else:
	write("MetadataSrf not present")
if arcpy.Exists('ResourceSrf'):
	featureclass.remove('ResourceSrf')
	write("ResourceSrf removed")
else:
	write("ResourceSrf not present")
if vogon:
	if arcpy.Exists('StructurePnt'):
		featureclass.remove('StructurePnt')
	if arcpy.Exists('StructureSrf'):
		featureclass.remove('StructureSrf')
	write("StructureSrf and StructurePnt will be skipped in processing")
featureclass.sort()
write("Loaded {0} of 55 TDSv7.1 feature classes".format(len(featureclass)))


# Checking for CACI schema cz they're "special" and have to make everything so fucking difficult
caci_schema = False
scale_name = 'scale'
for fc in featureclass:
	fc_zero = int(arcpy.GetCount_management(fc).getOutput(0))
	if fc_zero == 0:
		continue
	else:
		field_check = arcpy.ListFields(fc)
		for f in field_check:
			if f == 'scale' or f == 'SCALE' or f == 'Scale' or f == 'sCaLe':
				scale_name = f
		field_check = [x.name.lower() for x in field_check]
		#field_check = [x.decode('utf-8').lower() for x in field_check]
		for f in field_check:
			if f == 'scale' or f == 'SCALE' or f == 'Scale' or f == 'sCaLe':
				caci_schema = True
		if caci_schema:
			write("Variant TDS schema identified\nSnowflake protocol activated for relevant tools")
		break


# Automatically disables editor tracking for each feature class that doesn't already have it disabled
write("\nDisabling Editor Tracking for {0}".format(gdb_name))
firstl = False
for fc in featureclass:
	desc = arcpy.Describe(fc)
	if desc.editorTrackingEnabled:
		try:
			arcpy.DisableEditorTracking_management(fc)
			if not firstl:
				write("\n")
				firstl = True
			write("{0} - Disabled".format(fc))
		except:
			write("Error disabling editor tracking for {0}. Please check the data manually and try again.".format(fc))
			pass
if firstl:
	write("\n")
write("Editor Tracking has been disabled.")


# If any of the tools that require the Defense Mapping license are selected, check out the Defense license
if defaults or metrics or explode:
	no_defense = False
	class LicenseError(Exception):
		pass
	if arcpy.CheckExtension("defense") == "Available":
		write("\n*Checking out Defense Mapping Extension*\n")
		arcpy.CheckOutExtension("defense")
	else:
		write("Defense Mapping license is unavailable")
		no_defense = True
		raise LicenseError



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Data Maintenance Tools Category   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Repair All NULL Geometry '''''''''
# Repairs all NULL geometries in each feature class
#### rewrite with intersect geometry method to remove duplicate vertices and kickbacks
# if input_shp is None:
# write("{0} feature OID: {1} found with NULL geometry. Skipping transfer.".format(fc_strip, srow[-2]))
# continue
while repair:
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
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	break


''''''''' Populate F_Codes '''''''''
# John Jackson's Fcode tool refactored from standalone with included dictionaries instead of imported
while fcode:
	tool_name = 'Populate F_Codes'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			try:
				fields = ['f_code', 'fcsubtype']
				write("Updating {0} Feature F_Codes".format(fc))
				with arcpy.da.UpdateCursor(fc, fields) as fcursor:
					for row in fcursor: # Checks if F_Code matches the FCSubtype value. Updates F_Code if they don't match assuming proper subtype
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
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	break


''''''''' Calculate Default Values '''''''''
# Calculate default values for NULL attributes
# All or nothing. Functions on datasets not individual feature classes
#### rewrite using domains and coded values thru cursors
while defaults:
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
		write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
		write("Exiting tool.\n")
		sys.exit(0)
	break


''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
#### Defense mapping version takes too long and crashes. just rewrite with manual calculations
# for line and polygon metrics, if area or length is tool small throw warning with output.
while metrics:
	tool_name = 'Calculate Metrics'
	write("\n--- {0} ---\n".format(tool_name))
	metric_type = 'LENGTH;WIDTH;AREA;ANGLE_OF_ORIENTATION'
	for fc in featureclass:
		try:
			write("Calculating AOO, ARA, LZN, and WID for {0}".format(fc))
			arcpy.CalculateMetrics_defense(fc, metric_type, "LZN", "WID", "ARA", "#", "#", "#")
		except arcpy.ExecuteError:
			# if the code failed for the current fc, check the error
			error_count += 1
			write("\n***Failed to run {0}.***\n".format(tool_name))
			write("Error Report:")
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write(arcpy.GetMessages())
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	break


''''''''' Update UFI Values ''''''''' ##### add functionality to only update blank fields
# Iterate through all features and update the ufi field with uuid4 random values
while ufi:
	tool_name = 'Update UFI Values'
	write("\n--- {0} ---\n".format(tool_name))
	ufi_count = 0
	# Explicit is better than implicit
	# Lambda function works better than "if not fieldname:", which can falsely catch 0.
	populated = lambda x: x is not None and str(x).strip() != '' # Function that returns boolean of if input field is populated or empty

	for fc in featureclass:
		try:
			with arcpy.da.SearchCursor(fc, 'ufi') as scursor:
				values = [row[0] for row in scursor]
			with arcpy.da.UpdateCursor(fc, 'ufi') as ucursor:
				for row in ucursor:
					if not populated(row[0]):
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					elif len(row[0]) != 36: # 36 character random alphanumeric string
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
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Feature Specific Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Integrate and Repair '''''''''
### Add integration of hydro VanishingPoints and NaturalPools
### Major rework of logic behind integrate step.
### Potentially do away with Integrate and make a few tools that just do the major things we need integrate to do
###   - Run snap tool with low tolerance for helping keep certain features coincident.
###   - Make a tool to add vertices at all feature intersections that don't have one already.
###      This is one of the main things we use integrate for, but it might be a tall order
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
	arcpy.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "zi026_ctuu >= 50000")
	arcpy.SelectLayerByAttribute_management("hs", "NEW_SELECTION", "zi026_ctuu >= 50000")
	arcpy.MakeFeatureLayer_management("hc", "hc_scale")
	srf_count = int(arcpy.GetCount_management("hs").getOutput(0))
	if srf_count > 0:
		arcpy.MakeFeatureLayer_management("hs", "hs_scale")
	write("Repairing {0} lines before Integration".format(fc1))
	arcpy.RepairGeometry_management("hc_scale", "DELETE_NULL")
	hfeat_count = 0
	if not large:
		try:
			feat_count = int(arcpy.GetCount_management("hc_scale").getOutput(0))
			write("Integrating {0} {1} features and \n            {2} {3} features...".format(feat_count, fc1, srf_count, fc2))
			if srf_count > 0:
				arcpy.Integrate_management("hc_scale 1;hs_scale 2", "0.03 Meters")
			else:
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
			write("\nPlease rerun the tool, but make sure the 'Process Large Feature Class' option is checked under {0}.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	if large:
		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(fc1)
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			arcpy.MinimumBoundingGeometry_management(fc1, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with arcpy.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			arcpy.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc1, "POLYGON")
			#arcpy.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			arcpy.MakeFeatureLayer_management(mem_fc, "hgrid")
			with arcpy.da.SearchCursor("hgrid", ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					arcpy.SelectLayerByAttribute_management("hgrid", "NEW_SELECTION", select)
					if srf_count > 0:
						arcpy.SelectLayerByLocation_management("hs_scale", "INTERSECT", "hgrid","","NEW_SELECTION")
						ssrf_count = int(arcpy.GetCount_management("hs_scale").getOutput(0))
					else:
						ssrf_count = 0
					arcpy.SelectLayerByLocation_management("hc_scale", "INTERSECT", "hgrid","","NEW_SELECTION")
					feat_count = int(arcpy.GetCount_management("hc_scale").getOutput(0))
					write("Integrating {0} {1} features and\n            {2} {3} features in partition {4}...".format(feat_count, fc1, ssrf_count, fc2, row[0]))
					hfeat_count = hfeat_count + feat_count + ssrf_count
					if ssrf_count > 0:
						arcpy.Integrate_management("hc_scale 1;hs_scale 2", "0.03 Meters")
					elif feat_count > 0:
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
			write("\nData too dense to be run in partitions. Integrating {0} in this database exceeds our current equipment limitations.".format(fc1))
			write("To continue running tool, uncheck {0} before running again.".format(tool_name))
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
	arcpy.SelectLayerByAttribute_management("tgp", "NEW_SELECTION", "f_code = 'AQ065' AND zi026_ctuu >= 50000")
	cul_count = int(arcpy.GetCount_management("tgp").getOutput(0))
	arcpy.SelectLayerByAttribute_management("tgc", "NEW_SELECTION", "zi026_ctuu >= 50000")
	if cul_count > 0:
		arcpy.MakeFeatureLayer_management("tgp", "tgp_scale")
	arcpy.MakeFeatureLayer_management("tgc", "tgc_scale")
	write("Repairing {0} lines before Integration".format(fc2))
	arcpy.RepairGeometry_management("tgc_scale", "DELETE_NULL")
	tfeat_count = 0
	if not large:
		try:
			feat_count = int(arcpy.GetCount_management("tgc_scale").getOutput(0))
			write("Integrating {0} {1} features and\n            {2} Culvert points...".format(feat_count, fc2, cul_count))
			if cul_count > 0:
				arcpy.Integrate_management("tgp_scale 2;tgc_scale 1", "0.03 Meters")
			else:
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
			write("\nPlease rerun the tool, but make sure the 'Process Large Feature Class' option is checked under {0}.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	if large:
		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(fc2)
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			arcpy.MinimumBoundingGeometry_management(fc2, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with arcpy.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			arcpy.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc2, "POLYGON")
			#arcpy.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			arcpy.MakeFeatureLayer_management(mem_fc, "tgrid")
			with arcpy.da.SearchCursor("tgrid", ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					arcpy.SelectLayerByAttribute_management("tgrid", "NEW_SELECTION", select)
					if cul_count > 0:
						arcpy.SelectLayerByLocation_management("tgp_scale", "INTERSECT", "tgrid","","NEW_SELECTION")
						pcul_count = int(arcpy.GetCount_management("tgp_scale").getOutput(0))
					else:
						pcul_count = 0
					arcpy.SelectLayerByLocation_management("tgc_scale", "INTERSECT", "tgrid","","NEW_SELECTION")
					feat_count = int(arcpy.GetCount_management("tgc_scale").getOutput(0))
					write("Integrating {0} {1} features and\n            {2} Culvert points in partition {3}...".format(feat_count, fc2, pcul_count, row[0]))
					tfeat_count = tfeat_count + feat_count + pcul_count
					if pcul_count > 0:
						arcpy.Integrate_management("tgp_scale 2;tgc_scale 1", "0.03 Meters")
					elif feat_count > 0:
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
			write("\nData too dense to be run in partitions. Integrating {0} in this database exceeds our current equipment limitations.".format(fc2))
			write("To continue running tool, uncheck {0} before running again.".format(tool_name))
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
	arcpy.SelectLayerByAttribute_management("up", "NEW_SELECTION", "zi026_ctuu >= 50000")
	arcpy.SelectLayerByAttribute_management("uc", "NEW_SELECTION", "zi026_ctuu >= 50000")
	arcpy.SelectLayerByAttribute_management("us", "NEW_SELECTION", "zi026_ctuu >= 50000")
	arcpy.MakeFeatureLayer_management("up", "up_scale")
	arcpy.MakeFeatureLayer_management("uc", "uc_scale")
	arcpy.MakeFeatureLayer_management("us", "us_scale")
	write("Repairing {0} lines and {1} polygons before Integration".format(fc2, fc3))
	arcpy.RepairGeometry_management("uc_scale", "DELETE_NULL")
	arcpy.RepairGeometry_management("us_scale", "DELETE_NULL")
	ufeat_count = 0
	if not large:
		try:
			feat_count1 = int(arcpy.GetCount_management("up_scale").getOutput(0))
			feat_count2 = int(arcpy.GetCount_management("uc_scale").getOutput(0))
			feat_count3 = int(arcpy.GetCount_management("us_scale").getOutput(0))
			write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features...".format(feat_count1, fc1, feat_count2, fc2, feat_count3, fc3))
			arcpy.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.03 Meters")
			ufeat_count = feat_count1 + feat_count2 + feat_count3
		except arcpy.ExecuteError:
			# if the code failed for the current fc, check the error
			error_count += 1
			write("\n***Failed to run {0}.***\n".format(tool_name))
			write("Error Report:")
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write(arcpy.GetMessages())
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write("\nPlease rerun the tool, but make sure the 'Process Large Feature Class' option is checked under {0}.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	if large:
		try:
			#Create Fishnet
			write("Processing large feature class. Partitioning data in chunks to process.")
			mem_fc = "in_memory\\{0}_grid".format(fc2)
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			arcpy.MinimumBoundingGeometry_management(fc2, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with arcpy.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			arcpy.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc2, "POLYGON")
			#arcpy.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			arcpy.MakeFeatureLayer_management(mem_fc, "ugrid")
			with arcpy.da.SearchCursor("ugrid", ['OID@']) as scursor:
				##### Add check for any 0 count features selected in each loop that might default to all features instead of 0 in current partition
				for row in scursor:
					select = "OID = {}".format(row[0])
					arcpy.SelectLayerByAttribute_management("ugrid", "NEW_SELECTION", select)
					arcpy.SelectLayerByLocation_management("up_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
					arcpy.SelectLayerByLocation_management("uc_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
					arcpy.SelectLayerByLocation_management("us_scale", "INTERSECT", "ugrid", "", "NEW_SELECTION")
					feat_count1 = int(arcpy.GetCount_management("up_scale").getOutput(0))
					feat_count2 = int(arcpy.GetCount_management("uc_scale").getOutput(0))
					feat_count3 = int(arcpy.GetCount_management("us_scale").getOutput(0))
					ufeat_count = ufeat_count + feat_count1 + feat_count2 + feat_count3
					write("Integrating {0} {1} features,\n            {2} {3} features, and\n            {4} {5} features in partition {6}...".format(feat_count1, fc1, feat_count2, fc2, feat_count3, fc3, row[0]))
					arcpy.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.03 Meters")
			write("Freeing partition memory")
			arcpy.Delete_management("in_memory")
			arcpy.Delete_management("ugrid")
		except arcpy.ExecuteError:
			# if the code failed for the current fc, check the error
			error_count += 1
			write("\n***Failed to run {0}.***".format(tool_name))
			write(arcpy.GetMessages())
			write("\nData too dense to be run in partitions. Integrating Utilities in this database exceeds our current equipment limitations.")
			write("To continue running tool, uncheck {0} before running again.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	write("Repairing {0} lines and {1} polygons after Integration".format(fc2, fc3))
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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Geometry Correction Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Delete Identical Features '''''''''
# Checks for features with identical geometry and PSG attribution and removes them
#### Test rewritten find identical code and replace existing
while dups:
	tool_name = 'Delete Identical Features'
	write("\n--- {0} ---\n".format(tool_name))
	# Set the output directory for the FindIdentical tool
	out_table = os.path.dirname(arcpy.env.workspace)
	# Precreate the path for the output dBASE table
	path = out_table.split(".")
	path.pop()
	table_loc = path[0] + str(".dbf")
	write("Creating temporary output file: {0}".format(table_loc))
	dup_count = 0


# ##### check Shape vs shape@ and add xy-tolerance to find and delete identical
# #search cursor with shape@ and oid@ check each shape against the others. if they match, store the oid in list.
# #new cursor. check matching shapes. if the other fields match, delete the one with the higher oid value
# 	for fc in featureclass:
# 		try:
# 			prev_check = []
# 			dup_oids = []
# 			lap_fields = ['SHAPE@XY', 'OID@']
#
# 			with arcpy.da.SearchCursor(fc, lap_fields) as scursor:
# 				with arcpy.da.SearchCursor(fc, lap_fields) as tcursor:
# 					for row in scursor:
# 						icursor.insertRow(row)
# 			atuple = ptGeometry.angleAndDistanceTo(ptGeometry2, "GEODESIC")
# 			atuple == (angle in degrees, distance in meters)


	# Loop feature classes and FindIdentical to get a count, then delete any found
	# ARA and other metric fields included
	for fc in featureclass:
		try:
			dick = fc_fields_og[fc]
			arcpy.FindIdentical_management(fc, out_table, dick, "", "", output_record_option="ONLY_DUPLICATES")
			rows = int(arcpy.management.GetCount(table_loc).getOutput(0))
			write("Found " + str(rows) + " duplicate " + str(fc) + " features.")
			if rows > 0:
				arcpy.DeleteIdentical_management(fc, fc_fields_og[fc])
				write("Deleted " + str(rows) + " duplicate " + str(fc) + " features.")
				dup_count += rows
		except arcpy.ExecuteError:
			# if the code failed for the current fc, check the error
			#error_count += 1
			try:
				os.remove(table_loc)
				os.remove(table_loc + str(".xml"))
				os.remove(path[0] + str(".cpg"))
				os.remove(path[0] + str(".IN_FID.atx"))
			except:
				pass
			arcpy.RefreshCatalog(out_table)
			write("\n***Failed to run {0} on {1}.***\n".format(tool_name, fc))
			write("Error Report:")
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write(arcpy.GetMessages())
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write_info("out_table", out_table)
			write_info("path", path)
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)

	# Clean up before next process
	os.remove(table_loc)
	os.remove(table_loc + str(".xml"))
	os.remove(path[0] + str(".cpg"))
	os.remove(path[0] + str(".IN_FID.atx"))
	arcpy.RefreshCatalog(out_table)
	break


''''''''' Hypernova Burst Multipart Features '''''''''
# Explodes multipart features for an entire dataset
while explode:
	tool_name = 'Hypernova Burst Multipart Features'
	write("\n--- {0} ---\n".format(tool_name))
	##### Multipart Search #####
	fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
	fc_multi_list = []
	total_multi = 0
	total_complex = 0
	for fc in featureclass:
		try:
			write("Searching for multiparts in {0}".format(fc))
			multipart = False # Assume the feature class doesn't have multiparts
			with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as scursor:
				complex = 0 # Counts complex single part features
				for row in scursor: # For each feature in the fc
					shape = row[1] # Get SHAPE@ token to extract properties
					if shape is None: # Checks for NULL geometries
						write(" *** Found a feature with NULL geometry. Be sure Repair Geometry has been run. *** ")
						continue
					elif shape.isMultipart is True: # Does the feature have the isMultipart flag
						shape_type = str(shape.type) # Gets the geometry type of the feature
						if shape_type == 'polygon': # If the feature is a polygon, it may be a complex single part feature with interior rings
							if shape.partCount > 1: # If the number of geometric parts is more than one, then it is a true multipart feature
								if multipart is False: # And if that multipart feature is the first in the fc
									fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
									multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
								elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
									fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
								continue # Moves on to the next feature row in the search loop
							else: # If the part count is not greater than 1, then it is a complex single part feature with interior rings
								complex += 1
								continue # Moves on to the next feature row in the search loop
						else: # Non-polygon feature geometries do not have the isMultipart flaw since they have fewer dimensions. Simply proceed as normal
							if multipart is False: # And if that multipart feature is the first in the fc
								fc_multi[fc] = [row[0]] # Create a dictionary key of the feature class with a value of the first mutlipart oid in a list
								multipart = True # Mark the current fc as having multipart features and that the initial feature dictionary has been created
							elif multipart is True: # If a multipart feature has already been found and the initial dictionary key is set up
								fc_multi[fc].append(row[0]) # Append the new multipart feature oid to the value list for the current feature class key in the dictionary
				if complex > 0:
					total_complex += complex
					write("{0} complex polygons found in {1}".format(complex, fc))
				if multipart is True:
					count = len(fc_multi[fc])
					write("*** " + str(count) + " true multipart features found in " + str(fc) + " ***")
				else:
					write("No multiparts found")

		except arcpy.ExecuteError:
			# if the code failed for the current fc, check the error
			error_count += 1
			write("\n***Failed to run {0}.***\n".format(tool_name))
			write("Error Report:")
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write(arcpy.GetMessages())
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
		if multipart is True:
			fc_multi_list.append(fc) # Creates iterable list of feature classes that have multipart features

	write(" ")
	if total_complex > 0:
		write("The {0} complex polygons found are single part polygons with complex interior holes that are more likely to become multipart features.".format(total_complex))
	write(" ")
	if fc_multi_list: # Only runs if fc_multi_list is not empty
		for fc in fc_multi_list:
			count = len(fc_multi[fc])
			total_multi += count
			write("{0} multipart features found in {1}".format(count, fc))
			write("  OIDs - {0}".format(fc_multi[fc]))
		write(" ")

	##### Isolate, Explode, Replace #####
	in_class = "multi"
	out_class = "single"
	for fc in fc_multi_list:
		try:
			#sanitize feature class name from sde cz the sde always has to make things more difficult than they need to be...
			fc_parts = fc.split(".")
			if fc_parts[-1] in fc_fields:
				fcr = fc_parts[-1]
			else:
				write("Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin.")

			# Variables
			oid_list = fc_multi[fc]
			og_oid = "oidid"
			fc_geom = arcpy.Describe(fc).shapeType
			oid_field = arcpy.Describe(fc).OIDFieldName # Get the OID field name. Not necessary for every loop, but simple enough to just put here.
			# Adds a field to the current fc that stores the original OID for identification after exploding.
			arcpy.AddField_management(fc, og_oid, "double")
			with arcpy.da.UpdateCursor(fc, [oid_field, og_oid]) as ucursor:
				for row in ucursor:
					if row[0] in oid_list:
						row[1] = row[0]
						ucursor.updateRow(row)
			#arcpy.CalculateField_management(fc, og_oid, "!" + oid_field + "!", "PYTHON")
			fieldnames = fc_fields[fcr]
			fieldnames.insert(0, og_oid)
			fieldnames.insert(0, oid_field)
			oid_list_str = str(fc_multi[fc]) # Convert the list to a string and remove the []
			oid_list_str = oid_list_str[1:-1]
			query = "{0} in ({1})".format(oid_field, oid_list_str) # Formats the query from the above variables as: OBJECTID in (1, 2, 3)

			# Create a new feature class to put the multipart features in to decrease processing time. fields based on original fc template
			arcpy.CreateFeatureclass_management(arcpy.env.workspace, in_class, fc_geom, fc, "", "", arcpy.env.workspace)

			# Add multipart features to new feature class based on OID
			with arcpy.da.SearchCursor(fc, fieldnames, query) as scursor: # Search current fc using fc_fields with OID@ and "oidid" prepended as [0,1] respectively. Queries for only OIDs in the multipart oid_list.
				with arcpy.da.InsertCursor(in_class, fieldnames) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
					for row in scursor: # For each feature in the current fc
						if row[0] in oid_list: # If the OID is in the oid_list of multipart features. Redundant since the scursor is queried for multipart OIDs, but meh
							icursor.insertRow(row) # Insert that feature row into the temp feature class, in_class "multi"

			write("{0} multipart progenitor cores collapsing.".format(fcr))
			before_process = dt.now().time()
			arcpy.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
			after_process = dt.now().time()
			date = dt.now().date()
			datetime1 = dt.combine(date, after_process)
			datetime2 = dt.combine(date, before_process)
			time_delta = datetime1 - datetime2
			time_elapsed = str(time_delta.total_seconds())
			write("Hypernova burst detected after {0} seconds.".format(time_elapsed))

			write("Removing original multipart features.")
			# Deletes features in fc that have OIDs flagged as multiparts
			with arcpy.da.UpdateCursor(fc, oid_field) as ucursor:
				for row in ucursor:
					if row[0] in oid_list:
						ucursor.deleteRow()

			write("Replacing with singlepart features.")
			# Create search and insert cursor to insert new rows in fc from MultipartToSinglepart output out_class
			with arcpy.da.SearchCursor(out_class, fieldnames) as scursor:
				with arcpy.da.InsertCursor(fc, fieldnames) as icursor:
					for row in scursor:
						icursor.insertRow(row)

			write("Populating NULL fields with defaults and updating UFIs for the new single part features.")
			query2 = "{0} IS NOT NULL".format(og_oid)
			arcpy.MakeFeatureLayer_management(fc, "curr_fc", query2)
			arcpy.CalculateDefaultValues_defense("curr_fc")
			write("NULL fields populated with default values")
			with arcpy.da.UpdateCursor(fc, 'ufi', query2) as ucursor:
				for row in ucursor:
					row[0] = str(uuid.uuid4())
					ucursor.updateRow(row)
			arcpy.DeleteField_management(fc, og_oid)
			write("UFI values updated")
			write(" ")

		except arcpy.ExecuteError:
			# if the code failed for the current fc, check the error
			error_count += 1
			write("\n***Failed to run {0}.***\n".format(tool_name))
			write("Error Report:")
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write(arcpy.GetMessages())
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)

	if fc_multi_list:
		write("All multipart feature have acheived supernova!")

	try:
		arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(in_class)))
		arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(out_class)))
		arcpy.Delete_management("curr_fc")
	except:
		write("No in_class or out_class created. Or processing layers have already been cleaned up. Continuing...")
		pass
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Preprocessing Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Default Bridge WID Updater '''''''''
# Checks for bridges with default WID (-999999) and updates them to match the underlying road or rail WID
while bridge:
	bridge_err = False
	no_def_bridge = False
	bridge_count = 0
	total_rem_b = 0
	tool_name = 'Default Bridge WID Updater'
	write("\n--- {0} ---\n".format(tool_name))
	if not arcpy.Exists('TransportationGroundCrv'):
		write("TransportationGroundCrv feature class missing./nCannot run Default Bridge WID Updater.")
		bridge_err = True
		break
	break

while bridge: # Needs updating from management geoprocessing to cursors
	if bridge_err:
		break
	# Pull width and geometry fields for bridges
	fieldsB = ['WID', 'SHAPE@']
	# Pull width and geometry fields for roads
	fieldsR = ['ZI016_WD1', 'SHAPE@']
	# Pull width and geometry fields for rails and sidetracks
	fieldsRR = ['ZI017_GAW', 'SHAPE@']

	# Convert the feature classes from the TDS into usable layers
	write("Making feature layers...")
	arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "bridge_crv_lyr")
	arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "road_crv_lyr")
	arcpy.MakeFeatureLayer_management("TransportationGroundCrv", "rail_crv_lyr")
	write("Successfully made the feature layers!")

	# Select road bridges with default (-999999) width
	arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130')")
	arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 13")
	# Make road bridges with default (-999999) width into layer
	arcpy.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeR")

	# Select rail bridges with default (-999999) width
	arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AQ040', 'AQ130')")
	arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999 AND TRS = 12")
	# Make rail bridges with default (-999999) width into layer
	arcpy.MakeFeatureLayer_management("bridge_crv_lyr", "fc_bridgeRR")

	# Select roads that share curve with the default width bridges above
	arcpy.SelectLayerByAttribute_management("road_crv_lyr", "NEW_SELECTION", "F_CODE = 'AP030'")
	arcpy.SelectLayerByLocation_management("road_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "fc_bridgeR", "", "SUBSET_SELECTION")
	# Make roads that share curve with default width bridges into layer
	arcpy.MakeFeatureLayer_management("road_crv_lyr", "fc_road")

	# Select rails that share curve with the default width bridges above
	arcpy.SelectLayerByAttribute_management("rail_crv_lyr", "NEW_SELECTION", "F_CODE IN ('AN010', 'AN050')")
	arcpy.SelectLayerByLocation_management("rail_crv_lyr", "SHARE_A_LINE_SEGMENT_WITH", "fc_bridgeRR", "", "SUBSET_SELECTION")
	# Make rails that share curve with default width bridges into layer
	arcpy.MakeFeatureLayer_management("rail_crv_lyr", "fc_rail")

	# Gets a count of selected bridges, roads, and rails
	fc_bridgeR_total = int(arcpy.management.GetCount("fc_bridgeR").getOutput(0))
	fc_bridgeRR_total = int(arcpy.management.GetCount("fc_bridgeRR").getOutput(0))
	total_bridges = fc_bridgeR_total + fc_bridgeRR_total
	total_roads = int(arcpy.management.GetCount("fc_road").getOutput(0))
	total_rails = int(arcpy.management.GetCount("fc_rail").getOutput(0))

	# Error handling. If 0 bridges selected the script hangs.
	if total_bridges == 0:
		write("No default bridges found.")
		no_def_bridge = True
		break
	# Error handling. If no roads or rails to select against, likely something will break.
	if total_roads == 0 and total_rails == 0:
		write("{0} default WID bridges found.".format(total_bridges))
		write("No underlying roads or rails for default bridges. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.")
		bridge_err = True
		break

	# Announces the total default bridges found.
	write("{0} default WID bridges found.".format(total_bridges))

	# Start an edit session. Must provide the workspace.
	edit = arcpy.da.Editor(workspace)
	# Edit session is started without an undo/redo stack for versioned data
	edit.startEditing(False, True) # For second argument, use False for unversioned data

	countR = 0
	if fc_bridgeR_total > 0:
		edit.startOperation() # Start an edit operation for road bridges
		# Loop to update bridge width to it's corresponding road width
		with arcpy.da.UpdateCursor("fc_bridgeR", fieldsB) as bridgeR: # UpdateCursor for bridges with width and geometry
			for i in bridgeR:
				with arcpy.da.SearchCursor("fc_road", fieldsR) as road: # SearchCursor for roads with width and geometry
					for j in road:
						if i[1].within(j[1]): # Check if bridge shares curve with road(if not working test contains\within)
							if i[0] < j[0]:
								i[0] = int(j[0]*1.5) # Sets current bridge width to road width * [factor]
				bridgeR.updateRow(i)
				countR += 1
		edit.stopOperation() # Stop the edit operation
	write("{0} bridges on roads updated.".format(countR))

	countRR = 0
	if fc_bridgeRR_total > 0:
		edit.startOperation() # Start an edit operation for rail bridges
		# Loop to update bridge width to it's corresponding rail width
		with arcpy.da.UpdateCursor("fc_bridgeRR", fieldsB) as bridgeRR: # UpdateCursor for bridges with width and geometry
			for i in bridgeRR:
				with arcpy.da.SearchCursor("fc_rail", fieldsRR) as rail: # SearchCursor for rails with width and geometry
					for j in rail:
						if i[1].within(j[1]): # Check if bridge shares curve with rail(if not working test contains\within)
							if i[0] < j[0]:
								i[0] = int(j[0])+1 # Sets current bridge width to integer rounded rail gauge width + [value]
				bridgeRR.updateRow(i)
				countRR += 1
		edit.stopOperation() # Stop the edit operation
	write("{0} bridges on railroads updated.".format(countRR))

	# Stop the edit session and save the changes
	try:
		edit.stopEditing(True)
	except:
		write("First attempt to save failed. Checking for updated SDE version. Trying again in 5 seconds. Please hold...")
		time.sleep(5)
		edit.stopEditing(True)

	# Select any remaining bridges with default (-999999) width
	arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "NEW_SELECTION", "F_CODE = 'AQ040'")
	arcpy.SelectLayerByAttribute_management("bridge_crv_lyr", "SUBSET_SELECTION", "WID = -999999")
	# Make these selections into a new layer and get a count
	arcpy.MakeFeatureLayer_management("bridge_crv_lyr", "bridges_rem")
	total_rem_b = int(arcpy.management.GetCount("bridges_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	bridge_count = (countR + countRR) - total_rem_b
	write("Updated {0} bridges with new WID values.".format(bridge_count))
	if total_rem_b > 0:
		write("{0} bridges still have default WID. \n The default bridges are either not snapped or missing their underlying road or rail. \n Make sure the bridges have the correct TRS.".format(total_rem_b))
	break


''''''''' Default Pylon HGT Updater '''''''''
# Checks for pylons with default HGT (-999999) and updates them to match the intersecting cable HGT
while pylong:
	pylong_err = False
	no_def_pylon = False
	lecount = 0
	total_rem_p = 0
	tool_name = 'Default Pylon HGT Updater'
	write("\n--- {0} ---\n".format(tool_name))
	if not arcpy.Exists('UtilityInfrastructurePnt') or not arcpy.Exists('UtilityInfrastructureCrv'):
		write("UtilityInfrastructurePnt or UtilityInfrastructureCrv feature classes missing./nCannot run Default Pylon HGT Updater.")
		pylong_err = True
		break
	break

while pylong: # Needs updating from management geoprocessing to cursors
	if pylong_err:
		break
	# Pull height and geometry fields
	fields = ['HGT', 'SHAPE@']

	# Convert the feature classes from the TDS into usable layers
	write("Making feature layers...")
	arcpy.MakeFeatureLayer_management("UtilityInfrastructurePnt", "utility_pnt_lyr")
	arcpy.MakeFeatureLayer_management("UtilityInfrastructureCrv", "utility_crv_lyr")
	write("Successfully made the feature layers!")

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

	# Gets a count of selected pylons and cables
	total_pylons = int(arcpy.management.GetCount("fc_pylon_total").getOutput(0))
	total_cables = int(arcpy.management.GetCount("fc_cable_total").getOutput(0))
	usable_pylons = int(arcpy.management.GetCount("fc_pylon").getOutput(0))
	usable_cables = int(arcpy.management.GetCount("fc_cable").getOutput(0))

	# Error handling. If 0 pylons selected the script hangs.
	if total_pylons == 0:
		write("No default pylons found.")
		no_def_pylon = True
		break
	# Error handling. If no cables to select against, likely something will break.
	if total_cables == 0:
		write("{0} default value pylons found.".format(total_pylons))
		write("No intersecting cables for default pylons. \n Try running Integrate and Repair then try again. \n The default pylons are either not snapped or missing a cable.")
		pylong_err = True
		break

	# Announces the total default pylons found.
	no_hgt_cable = total_cables - usable_cables
	y = total_pylons - usable_pylons
	y = str(y)
	write("{0} default value pylons found.".format(total_pylons))
	write("{0} of the intersecting cables don't have a height. These will be ignored.".format(no_hgt_cable))
	write("{0} pylons are intersecting a cable with a height value and will be updated.".format(usable_pylons))

	# Loop to update pylon height to it's corresponding cable height
	with arcpy.da.UpdateCursor("fc_pylon", fields) as pylon: # UpdateCursor for pylons with height and geometry
		for i in pylon:
			with arcpy.da.SearchCursor("fc_cable", fields) as cable: # SearchCursor for cables with height and geometry
				for j in cable:
					if not i[1].disjoint(j[1]): # Check if pylon intersects a cable
						if i[0] < j[0]:
							i[0] = j[0] # Sets current pylon HGT to intersecting cable's HGT
			pylon.updateRow(i)
			lecount += 1

	# Select any remaining pylons with default (-999999) height
	arcpy.SelectLayerByAttribute_management("fc_pylon", "NEW_SELECTION", "F_CODE = 'AT042'")
	arcpy.SelectLayerByAttribute_management("fc_pylon", "SUBSET_SELECTION", "HGT = -999999")
	# Make these selections into a new layer and get a count
	arcpy.MakeFeatureLayer_management("fc_pylon", "pylons_rem")
	total_rem_p = int(arcpy.management.GetCount("pylons_rem").getOutput(0))
	# Final messages of the state of the data after tool completion
	lecount = lecount - total_rem_p
	write("Updated {0} pylons with new HGT values.".format(lecount))
	write("{0} pylons still have default HGT. \n Consider running Integrate and Repair before trying again. \n The remaining pylons are not snapped, missing a cable, or the underlying cable doesn't have a height.".format(total_rem_p))
	break


''''''''' Building in BUA Descaler '''''''''
# Descales buildings within BUAs that don't have important FFNs
while building:
	building_err = False
	no_bua = False
	no_bua_buildings = False
	total_non_imp = 0
	tool_name = 'Building in BUA Descaler'
	write("\n--- {0} ---\n".format(tool_name))
	if not arcpy.Exists('SettlementSrf'):
		write("SettlementSrf feature class missing./nCannot run Building in BUA Descaler.")
		building_err = True
		break
	if not arcpy.Exists('StructureSrf') and not arcpy.Exists('StructurePnt'):
		write("StructureSrf and StructurePnt feature classes missing./nCannot run Building in BUA Descaler.")
		building_err = True
		break
	break

while building: # Needs updating from management geoprocessing to cursors
	if building_err:
		break
	# Make initial layers from the workspace
	srf_exist = False
	pnt_exist = False
	import_ffn_s = 0
	import_ffn_p = 0
	non_import_count_s = 0
	non_import_count_p = 0
	fields = 'ZI026_CTUU'
	caci_query = "FFN IN ({0})".format(", ".join(str(i) for i in ffn_list_caci.values()))
	other_query = "FFN IN ({0})".format(", ".join(str(i) for i in ffn_list_all.values()))

	if caci_schema:
		write("CACI specific important building FFNs list:")
		write("\n".join("{}: {}".format(k, v) for k, v in ffn_list_caci.items()))
	else:
		write("Current project important building FFNs list:")
		write("\n".join("{}: {}".format(k, v) for k, v in ffn_list_all.items()))

	# Make layer of BUAs
	write("\nRetrieved feature classes containing BUAs and Buildings")
	write("Selecting BUAs")
	arcpy.MakeFeatureLayer_management("SettlementSrf", "settlement_srf")
	arcpy.SelectLayerByAttribute_management("settlement_srf", "NEW_SELECTION", "F_CODE = 'AL020'")
	arcpy.MakeFeatureLayer_management("settlement_srf", "buas")
	write("Searching within BUAs")

	if arcpy.Exists('StructureSrf'):
		# Make layer of building surfaces
		arcpy.MakeFeatureLayer_management("StructureSrf", "structure_srf")
		arcpy.SelectLayerByAttribute_management("structure_srf", "NEW_SELECTION", "F_CODE = 'AL013'")
		arcpy.MakeFeatureLayer_management("structure_srf", "building_srf")
		# Layer of building surfaces within BUAs
		arcpy.SelectLayerByLocation_management ("building_srf", "WITHIN", "buas", "", "NEW_SELECTION")
		arcpy.MakeFeatureLayer_management("building_srf", "bua_building_s")
		# Select important building surfaces and switch selection
		# Adam's original list: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building surfaces matching criteria...")
		if caci_schema:
			arcpy.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", caci_query)
		else:
			arcpy.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", other_query)
		import_ffn_s = int(arcpy.GetCount_management("bua_building_s").getOutput(0))
		arcpy.SelectLayerByAttribute_management("bua_building_s", "SWITCH_SELECTION")
		arcpy.MakeFeatureLayer_management("bua_building_s", "non_import_s")
		non_import_count_s = int(arcpy.GetCount_management("non_import_s").getOutput(0))

	if arcpy.Exists('StructurePnt'):
		# Make layer of building points
		arcpy.MakeFeatureLayer_management("StructurePnt", "structure_pnt")
		arcpy.SelectLayerByAttribute_management("structure_pnt", "NEW_SELECTION", "F_CODE = 'AL013'")
		arcpy.MakeFeatureLayer_management("structure_pnt", "building_pnt")
		# Layer of building points within BUAs
		arcpy.SelectLayerByLocation_management ("building_pnt", "WITHIN", "buas", "", "NEW_SELECTION")
		arcpy.MakeFeatureLayer_management("building_pnt", "bua_building_p")
		# Select important building points and switch selection
		# Adam's original list: (850, 851, 852, 855, 857, 860, 861, 871, 873, 875, 862, 863, 864, 866, 865, 930, 931)
		write("Identifying building points matching criteria...")
		if caci_schema:
			arcpy.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", caci_query)
		else:
			arcpy.SelectLayerByAttribute_management("bua_building_s", "NEW_SELECTION", other_query)
		import_ffn_p = int(arcpy.GetCount_management("bua_building_p").getOutput(0))
		arcpy.SelectLayerByAttribute_management("bua_building_p", "SWITCH_SELECTION")
		arcpy.MakeFeatureLayer_management("bua_building_p", "non_import_p")
		non_import_count_p = int(arcpy.GetCount_management("non_import_p").getOutput(0))

	# Count buildings and buas in selections
	bua_count = int(arcpy.GetCount_management("buas").getOutput(0))
	total_import = import_ffn_s + import_ffn_p
	total_non_imp = non_import_count_s + non_import_count_p

	# End script if there are no BUAs or no buildings inside them
	if bua_count == 0:
		write("\nNo BUAs found.")
		no_bua = True
		break
	if total_non_imp == 0:
		write("\nNo buildings without important FFNs found in BUAs.")
		no_bua_buildings = True
		break

	write("\n{0} buildings with important FFNs found in {1} total BUAs.".format(total_import, bua_count))

	# Descale selected, non-important buildings within BUAs to CTUU 12500
	write("Descaling unimportant building surfaces...")
	with arcpy.da.UpdateCursor("non_import_s", fields) as cursor_s:
		for row in cursor_s:
			row[0] = 12500
			cursor_s.updateRow(row)

	write("Descaling unimportant building points...")
	with arcpy.da.UpdateCursor("non_import_p", fields) as cursor_p:
		for row in cursor_p:
			row[0] = 12500
			cursor_p.updateRow(row)

	write("\n{0} building surfaces descaled to CTUU 12500.".format(non_import_count_s))
	write("{0} building points descaled to CTUU 12500.".format(non_import_count_p))
	break


''''''''' CACI Swap Scale and CTUU '''''''''
# Swaps the Scale field with the CTUU field so we can work normally with CACI data
while swap:
	tool_name = 'CACI Swap Scale and CTUU'
	write("\n--- {0} ---\n".format(tool_name))
	if not caci_schema:
		write("Provided TDS does not match CACI schema containing the 'Scale' field.\nCannot run CACI Swap Scale and CTUU")
		break
	if caci_schema:
		write("CACI schema containing 'Scale' field identified")
	featureclass = arcpy.ListFeatureClasses()
	if arcpy.Exists('MetadataSrf'):
		featureclass.remove('MetadataSrf')
		write("MetadataSrf removed")
	else:
		write("MetadataSrf not present")
	if arcpy.Exists('ResourceSrf'):
		featureclass.remove('ResourceSrf')
		write("ResourceSrf removed")
	else:
		write("ResourceSrf not present")
	featureclass.sort()
	break

while swap:
	if not caci_schema:
		break
	write("Swapping CTUU and Scale for {0}".format(gdb_name))
	write("\nNote: The SAX_RX9 field will be changed from <NULL> to 'Scale Swapped' after the first swap. It will flip back and forth in subsequent runs.\nIf the tool was aborted on a previous run for some reason, it will reset all feature classes to the dominant swap format to maintain internal consistency. It is still up to the user to know which format they were swapping from. (Either Scale->CTUU or CTUU->Scale) Check the tool output for more information on which feature classes were changed.\n")
	fields = ['zi026_ctuu', 'scale', 'swap', 'progress', 'sax_rx9']
	fields[1] = str(scale_name)

	# Explicit is better than implicit
	populated = lambda x: x is not None and str(x).strip() != '' # Finds empty fields. See UFI process

	write("\nChecking if any previous swaps were canceled. Please wait...")
	swap_fc = []
	none_fc = []
	empty_fc = []
	chk_fields = ['sax_rx9', 'scale']
	chk_fields[1] = str(scale_name)
	clean_proceed = False
	swap_dom = False
	none_dom = False
	for fc in featureclass:
		fc_zero = int(arcpy.GetCount_management(fc).getOutput(0))
		if fc_zero == 0:
			empty_fc.append(str(fc))
			continue
		# field_check = arcpy.ListFields(fc)
		# partialchk = False
		# swapchk = False
		# for f in field_check:
		# 	if f.name == "progress":
		# 		partialchk = True
		# 	if f.name == "swap":
		# 		swapchk = True
		# 		break
		# if swapchk:
		# 	continue
		with arcpy.da.SearchCursor(fc, chk_fields) as scursor:
			for row in scursor:
				if not populated(row[0]):
					if not populated(row[1]):
						continue
					none_fc.append(str(fc))
					break
				if row[0] == 'Scale Swapped':
					if not populated(row[1]):
						continue
					swap_fc.append(str(fc))
					break
	if len(swap_fc) == 0 or len(none_fc) == 0:
		clean_proceed = True
	elif len(swap_fc) > len(none_fc):
		swap_dom = True
	elif len(swap_fc) < len(none_fc):
		none_dom = True
	if not clean_proceed:
		write("\n***Previous run was flagged. Resetting feature classes to previous format.***\n")
		if swap_dom:
			write("Majority of feature classes tagged as 'Scale Swapped'. Updating the following feature classes to match:")
			write("\n".join(i for i in none_fc) + "\n")
		if none_dom:
			write("Majority of feature classes /not/ tagged as 'Scale Swapped'. Updating the following feature classes to match:")
			write("\n".join(i for i in swap_fc) + "\n")
	if clean_proceed:
		write("Previous swaps finished properly. Continuing...\n")

	# Swippity Swappity Loop
	for fc in featureclass:
		if swap_dom and fc in swap_fc:
			continue
		if none_dom and fc in none_fc:
			continue
		if clean_proceed and fc in empty_fc:
			write("*Feature Class {0} is empty*".format(fc))
			continue
		elif fc in empty_fc:
			continue
		#write("swap_dom: {0}\nnone_dom: {1}".format(swap_dom, none_dom)) ###
		write("Swapping CTUU and Scale fields for {0} features".format(fc))
		field_check = arcpy.ListFields(fc)
		partialchk = False
		swapchk = False
		for f in field_check:
			if f.name == "progress":
				partialchk = True
			if f.name == "swap":
				swapchk = True
		if not partialchk:
			arcpy.AddField_management(fc, "progress", "TEXT", 9) # Creates temporary progress field
		if not swapchk:
			arcpy.AddField_management(fc, "swap", "LONG", 9) # Creates temporary swap field
		with arcpy.da.UpdateCursor(fc, fields) as ucursor: # Update cursor to juggle values
			for row in ucursor:
				if row[3] == 'y' or row[3] == 'x':
					continue
				# Functions as three ring puzzle
				row[2] = row[1] #swap = scale
				row[1] = row[0] #scale = ctuu
				row[0] = row[2] #ctuu = swap
				row[3] = 'y' #mark row as swapped in previous run that crashed or canceled
				if not populated(row[4]):
					row[4] = 'Scale Swapped'
				elif row[4] == 'Scale Swapped':
					row[4] = None
				swap_tag = row[4]
				ucursor.updateRow(row)
			write("    SAX_RX9 field value after swap: {0}".format(swap_tag))
			if partialchk and not clean_proceed:
				write("Resetting partial feature class to dominant format.")
				for row in ucursor:
					if swap_dom and not populated(row[4]):
						row[2] = row[1] #swap = scale
						row[1] = row[0] #scale = ctuu
						row[0] = row[2] #ctuu = swap
						row[3] = 'x' #mark row as swapped in previous run that crashed or canceled
						row[4] = 'Scale Swapped'
					if none_dom and row[4] == 'Scale Swapped':
						row[2] = row[1] #swap = scale
						row[1] = row[0] #scale = ctuu
						row[0] = row[2] #ctuu = swap
						row[3] = 'x' #mark row as swapped in previous run that crashed or canceled
						row[4] = None

		# Deletes temporary swap field
		arcpy.DeleteField_management(fc, "swap")
		arcpy.DeleteField_management(fc, "progress")
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Database Management Tools Category #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

''''''''' Database Feature Report '''''''''
# Refactored from John Jackson's Feature_Itemized_Counter.py by Nat Cagle
while fcount:
	tool_name = 'Database Feature Report'
	write("\n--- {0} ---\n".format(tool_name))
	# Define counters for shape feature counts and total feature count
	pnt_cnt = 0
	crv_cnt = 0
	srf_cnt = 0
	tots_f = 0
	hydro_cnt = 0
	trans_cnt = 0
	building_cnt = 0
	landcover_cnt = 0
	break

while fcount:
	gdb_name_full = TDS.split('\\')[-2]
	# Define fields for Search Cursor
	fields = ["FCSubtype"]
	if not 'StructurePnt' in featureclass:
		featureclass.append('StructurePnt')
	if not 'StructureSrf' in featureclass:
		featureclass.append('StructureSrf')
	# Set up dictionary and exclusion list to track feature classes
	feat_dict = OrderedDict()
	exList = []
	# Retrieve date and time for output file label and report timestamp
	today = dt.now().date() #datetime.date.today()
	time_stamp = dt.now().strftime("%Y_%m_%d_%H%M")
	current_time = dt.now().strftime("%H:%M:%S")
	# Define feature categories
	hydro_cat = 'Hydrography'
	trans_cat = 'Transportation'
	building_sub = 100083
	landcover_list = [ 100295, #'Aqueduct'
						100296, #'Bog'
						100089, #'BuiltUpArea'
						100297, #'Canal'
						100393, #'Cane'
						100329, #'Cistern'
						100396, #'ClearedWay'
						100380, #'CropLand'
						100403, #'Desert'
						100298, #'Ditch'
						100001, #'ExtractionMine'
						130380, #'Forest'
						100341, #'Glacier'
						100387, #'Grassland'
						100386, #'HopField'
						130384, #'InlandWaterbody'
						100399, #'Marsh'
						100340, #'Moraine'
						100320, #'NaturalPool'
						100384, #'Orchard'
						100313, #'RiceField'
						100314, #'River'
						100318, #'Sabkha'
						100316, #'SaltFlat'
						100374, #'SandDunes'
						100349, #'SnowIceField'
						100358, #'SoilSurfaceRegion'
						100400, #'Swamp'
						100388, #'Thicket'
						100218, #'TidalWater'
						100350, #'Tundra'
						100385, #'Vineyard'
						100473, #'VoidCollectionArea'
	]

	# Create report output file path
	results = "{0}\\{1}_Feature_Report_{2}.txt".format(rresults, gdb_name, time_stamp)
	write("Checking feature classes...\n")

	# Fill in dictionary with itemized feature subtype counts
	for i in featureclass:
		currFC = str(i)
		currShape = currFC[-3:]
		feat_dict[currFC]=[{},0]
		hydro_feat = False
		trans_feat = False
		if hydro_cat in currFC:
			hydro_feat = True
		elif trans_cat in currFC:
			trans_feat = True
		with arcpy.da.SearchCursor(i,fields) as vCursor:
			try:
				# Iterate through features in Feature Class
				for j in vCursor:
					curr_sub = int(j[0])
					# Counting Feature Subtypes
					if fcsub_dict[int(j[0])] not in feat_dict[currFC][0]:
						feat_dict[str(i)][0][fcsub_dict[int(j[0])]] = 1
					else:
						feat_dict[currFC][0][fcsub_dict[int(j[0])]] += 1
					# Count Feature Class total features
					feat_dict[currFC][1] += 1
					# Count Database total features
					tots_f += 1
					# Counting based on shape type
					if currShape == 'Srf':
						srf_cnt += 1
						if any(int(substring) == int(curr_sub) for substring in landcover_list):
							landcover_cnt += 1
					elif currShape == 'Crv':
						crv_cnt += 1
					else:
						pnt_cnt += 1
					# Counting specific categories
					if int(curr_sub) == int(building_sub):
						building_cnt += 1
					if hydro_feat:
						hydro_cnt += 1
					if trans_feat:
						trans_cnt += 1

			except:
				# If FC does not have FCSubtype field put it on exclusion list
				write("**** {0} does not have required fields ****".format(currFC))
				exList.append(currFC)
				continue
		write("{0} features counted".format(currFC))

	# Setup and write results to text file
	write("\nWriting report to TXT file...\n")
	with open(results,'w') as txt_file:
		line = []
		txt_file.write("Feature Count Report for TPC: {0}\n".format(gdb_name_full))
		txt_file.write("Report created: {0} at time: {1}\n\n\n".format(today, current_time))
		txt_file.writelines(["Point Features  :  ",str(pnt_cnt),"\n",
							"Curve Features  :  ",str(crv_cnt),"\n",
							"Surface Features:  ",str(srf_cnt),"\n",
							"Total Features  :  ",str(tots_f),"\n\n",
							"Total Hydrography Features        :  ",str(hydro_cnt),"\n",
							"Total Transportation Features     :  ",str(trans_cnt),"\n",
							"Total Building Surfaces and Points:  ",str(building_cnt),"\n",
							"Total Landcover Surfaces          :  ",str(landcover_cnt),"\n\n\n"])
		header = ['Feature Class'.ljust(25), 'Subtype'.center(25), 'Feature Count\n'.rjust(8),'\n\n']
		txt_file.writelines(header)
		for fKey in feat_dict:
			# Check exclusion list
			if fKey in exList:
				txt_file.writelines([fKey.ljust(25),
									'******** Feature Class does not contain subtypes ********','\n\n'])
				continue
			# Print Subtype list with individual counts
			if feat_dict[fKey][1] != 0:
				# Print Feature Class with count
				txt_file.writelines([fKey.ljust(25),'--------- Total Features: ',
									str(feat_dict[fKey][1]),' ---------','\n\n'])
				for sKey in feat_dict[fKey][0]:
					line = [''.ljust(25),sKey.center(25),str(feat_dict[fKey][0][sKey]).rjust(8)+'\n']
					txt_file.writelines(line)
				txt_file.write('\n\n')
		txt_file.write("\nEmpty Feature Classes:\n\n")
		for fKey in feat_dict:
			# Check exclusion list
			if fKey in exList:
				continue
			if feat_dict[fKey][1] == 0:
				txt_file.write("{0}\n".format(fKey))

	write("Feature Count Report created. File located in database folder:\n{0}".format(results))
	break


''''''''' Source Analysis Report '''''''''
# Refactored from John Jackson's Version_Source_Counter.py by Nat Cagle
while vsource:
	tool_name = 'Source Analysis Report'
	write("\n--- {0} ---\n".format(tool_name))
	break

while vsource:
	time_stamp = dt.now().strftime("%Y_%m_%d_%H%M")
	gdb_name_full = TDS.split('\\')[-2]
	fields = ["Version","ZI001_SDP","ZI001_SDV","ZI001_SRT"]
	results_csv = "{0}\\{1}_Source_Count_{2}.csv".format(rresults, gdb_name, time_stamp)
	results_txt = "{0}\\{1}_Source_Count_{2}.txt".format(rresults, gdb_name, time_stamp)
	feat_dict = OrderedDict()
	write("Checking feature classes...\n")

	# Fill in dictionary with leveled counts: Version -> SDP -> SDV *optional SRT
	for i in featureclass:
		feat_dict[str(i)]=OrderedDict()
		with arcpy.da.SearchCursor(i,fields) as vCursor:
			try:
				for j in vCursor:
					if str(j[0]) not in feat_dict[str(i)]:
						feat_dict[str(i)][str(j[0])]={str(j[1]):{str(j[2]):1}}

					elif str(j[1]) not in feat_dict[str(i)][str(j[0])]:
						feat_dict[str(i)][str(j[0])][str(j[1])] = {str(j[2]):1}
					elif str(j[2]).strip() not in feat_dict[str(i)][str(j[0])][str(j[1])]:
						feat_dict[str(i)][str(j[0])][str(j[1])][str(j[2]).strip()] = 1
					else:
						feat_dict[str(i)][str(j[0])][str(j[1])][str(j[2]).strip()] += 1
			except:
				write("**** {0} does not have required fields ****".format(i))
		write("{0} feature sources identified".format(i))

	# Set up and write dictionary out to CSV
	write("\nWriting report to CSV and TXT file...\n")
	with open(results_csv,'wb') as csvFile:
		writer = cs.writer(csvFile, delimiter=',')
		line = []
		header = ['Feature Class', 'Version', 'Description (SDP)', 'Source Date','Feature Count']
		writer.writerow(header)
		for fKey in feat_dict:
			if feat_dict[fKey]: # Only writes output if it exists
				writer.writerow([fKey,None,None,None,None])
				for vKey in feat_dict[fKey]:
					for sKey in feat_dict[fKey][vKey]:
						for dKey in feat_dict[fKey][vKey][sKey]:
							line = [None,vKey,sKey,dKey,feat_dict[fKey][vKey][sKey][dKey]]
							writer.writerow(line)

	# Set up and write dictionary out to TXT
	with open(results_txt,'w') as txt_file:
		line = []
		txt_file.write("Source Report for TPC: {0}\nScroll right for all information.\n**For an ordered view, see accompanying .csv file\n\n".format(gdb_name_full))
		header = ['Feature Class'.ljust(25), 'Version'.center(14), 'Description (SDP)'.ljust(65), 'Source Date'.center(16),'Feature Count\n\n'.rjust(8)]
		txt_file.writelines(header)
		for fKey in feat_dict:
			if feat_dict[fKey]:
				txt_file.write(fKey+'\n')
				for vKey in feat_dict[fKey]:
					for sKey in feat_dict[fKey][vKey]:
						for dKey in feat_dict[fKey][vKey][sKey]:
							line = [''.ljust(25),vKey.center(14),sKey.ljust(65),dKey.center(16),str(feat_dict[fKey][vKey][sKey][dKey]).rjust(8)+'\n']
							txt_file.writelines(line)

	write("Source Analysis Report created. File located in database folder:\n{0}".format(rresults))
	break



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Report Formatting and Wrap Up #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

if defaults or metrics or explode:
	if not no_defense:
		write("\n~~ Checking Defense Mapping Extension back in ~~\n")
		arcpy.CheckInExtension("defense")


# Report of completed tasks
def format_count(count):
	cnt_str = str(count)
	end_spacing = ""
	if len(cnt_str) > 0:
		for i in range(7-len(cnt_str)):
			end_spacing += " "
	else:
		pass
	return end_spacing

write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}{4}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

# Easter Egg
if secret:
	write(u"    |        Our great and powerful leader       {0}|".format(exs))
	write(u"    |         The kind-hearted and caring        {0}|".format(exs))
	write(u"    |      _______        _                      {0}|".format(exs))
	write(u"    |     / ___/ /  ___ _(_)_____ _  ___ ____    {0}|".format(exs))
	write(u"    |    / /__/ _ \/ _ `/ / __/  ' \/ _ `/ _ \   {0}|".format(exs))
	write(u"    |    \___/_//_/\_,_/_/_/ /_/_/_/\_,_/_//_/   {0}|".format(exs))
	write(u"    |               ___           __             {0}|".format(exs))
	write(u"    |              / _ )___  ____/ /__           {0}|".format(exs))
	write(u"    |             / _  / _ \/ __/  '_/           {0}|".format(exs))
	write(u"    |            /____/\___/\__/_/\_\            {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |             Thanks you for your            {0}|".format(exs))
	write(u"    |             outstanding service            {0}|".format(exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |   {0}   {1}|".format(sspaces, exs))

write(u"    |   =======  Processes  Completed  =======   {0}|".format(exs))
write(u"    |   {0}   {1}|".format(sspaces, exs))
if vogon:
    write(u"    |     - Buildings skipped                    {0}|".format(exs))
if repair:
	write(u"    |     - Repaired NULL Geometries             {0}|".format(exs))
if fcode:
	write(u"    |     - Populated F_Codes                    {0}|".format(exs))
if defaults:
	write(u"    |     - Calculated Default Values            {0}|".format(exs))
if metrics:
	write(u"    |     - Calculated Metrics                   {0}|".format(exs))
if ufi:
	f_ufi_count = format_count(ufi_count)
	write(u"    |     - Updated UFI Values                   {0}|".format(exs))
	write(u"    |          {0} Duplicate or blank UFIs   {1}{2}|".format(ufi_count, f_ufi_count, exs))
if hydro or trans or util:
	write(u"    |     - Integrated and Repaired:             {0}|".format(exs))
	if large:
		write(u"    |        ~ Large Dataset ~                   {0}|".format(exs))
	if hydro:
		f_hfeat_count = format_count(hfeat_count)
		write(u"    |          {0} Hydro                     {1}{2}|".format(hfeat_count, f_hfeat_count, exs))
	if trans:
		f_tfeat_count = format_count(tfeat_count)
		write(u"    |          {0} Trans                     {1}{2}|".format(tfeat_count, f_tfeat_count, exs))
	if util:
		f_ufeat_count = format_count(ufeat_count)
		write(u"    |          {0} Utilities                 {1}{2}|".format(ufeat_count, f_ufeat_count, exs))
if dups:
	f_dup_count = format_count(dup_count)
	write(u"    |     - Deleted Identical Features           {0}|".format(exs))
	write(u"    |          {0} Duplicates found          {1}{2}|".format(dup_count, f_dup_count, exs))
if explode:
	f_complex_count = format_count(total_complex)
	f_multi_count = format_count(total_multi)
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
	write(u"    |          {0} Complex features found    {1}{2}|".format(total_complex, f_complex_count, exs))
	write(u"    |          {0} Features exploded         {1}{2}|".format(total_multi, f_multi_count, exs))
if bridge:
	f_bridge_count = format_count(bridge_count)
	f_total_rem_b = format_count(total_rem_b)
	write(u"    |     - Default Bridge WID Updater           {0}|".format(exs))
	if bridge_err:
		write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif no_def_bridge:
		write(u"    |          No default bridges found          {0}|".format(exs))
	else:
		write(u"    |          {0} Bridges updated           {1}{2}|".format(bridge_count, f_bridge_count, exs))
		write(u"    |          {0} Defaults not updated      {1}{2}|".format(total_rem_b, f_total_rem_b, exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if pylong:
	f_lecount = format_count(lecount)
	f_total_rem_p = format_count(total_rem_p)
	write(u"    |     - Default Pylon HGT Updater            {0}|".format(exs))
	if pylong_err:
		write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif no_def_pylon:
		write(u"    |          No default pylons found           {0}|".format(exs))
	else:
		write(u"    |          {0} Pylons updated            {1}{2}|".format(lecount, f_lecount, exs))
		write(u"    |          {0} Defaults not updated      {1}{2}|".format(total_rem_p, f_total_rem_p, exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if building:
	f_total_non = format_count(total_non_imp)
	write(u"    |     - Building in BUA Descaler             {0}|".format(exs))
	if building_err:
		write(u"    |       !!! The tool did not finish !!!      {0}|".format(exs))
		write(u"    |       !!! Please check the output !!!      {0}|".format(exs))
	elif no_bua:
		write(u"    |          No BUAs found                     {0}|".format(exs))
	elif no_bua_buildings:
		write(u"    |          No un-important buildings found   {0}|".format(exs))
	else:
		write(u"    |          {0} Buildings descaled        {1}{2}|".format(total_non_imp, f_total_non, exs))
		write(u"    |          Check the output for more info    {0}|".format(exs))
if swap:
	write(u"    |     - CACI Swap Scale and CTUU             {0}|".format(exs))
if fcount:
	f_pnt_cnt = format_count(pnt_cnt)
	f_crv_cnt = format_count(crv_cnt)
	f_srf_cnt = format_count(srf_cnt)
	f_tots_f = format_count(tots_f)
	f_hydro_cnt = format_count(hydro_cnt)
	f_trans_cnt = format_count(trans_cnt)
	f_building_cnt = format_count(building_cnt)
	f_landcover_cnt = format_count(landcover_cnt)
	write(u"    |     - Feature report generated             {0}|".format(exs))
	write(u"    |          {0} Point Features            {1}{2}|".format(pnt_cnt, f_pnt_cnt, exs))
	write(u"    |          {0} Curve Features            {1}{2}|".format(crv_cnt, f_crv_cnt, exs))
	write(u"    |          {0} Surface Features          {1}{2}|".format(srf_cnt, f_srf_cnt, exs))
	write(u"    |          {0} Total Features            {1}{2}|".format(tots_f, f_tots_f, exs))
	write(u"    |          {0} Hydrography Features      {1}{2}|".format(hydro_cnt, f_hydro_cnt, exs))
	write(u"    |          {0} Transportation Features   {1}{2}|".format(trans_cnt, f_trans_cnt, exs))
	write(u"    |          {0} Buildings                 {1}{2}|".format(building_cnt, f_building_cnt, exs))
	write(u"    |          {0} Landcover Surfaces        {1}{2}|".format(landcover_cnt, f_landcover_cnt, exs))
	write(u"    |          Check the output for more info    {0}|".format(exs))
if vsource:
	write(u"    |     - Source report generated              {0}|".format(exs))
	write(u"    |          Check the output for more info    {0}|".format(exs))

# Easter Egg
if not vogon and not repair and not fcode and not defaults and not metrics and not ufi and not large and not hydro and not trans and not util and not dups and not explode and not bridge and not pylong and not building and not swap and not fcount and not vsource:
	write(u"    |   {0}   {1}|".format(sspaces, exs))
	write(u"    |       Kristen, click a check box and       {0}|".format(exs))
	write(u"    |             stop being cheeky.             {0}|".format(exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")
