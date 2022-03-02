# -*- #################
# ====================== #
# Finishing Tool v8.4 beta #
# Nat Cagle 2022-01-13   #
# ====================== #
import arcpy
from arcpy import AddMessage as write
from datetime import datetime as dt
import uuid
import os
import sys
import time
import math

#            ________________________________
#           | Runs Populate FCode, Calculate |
#           | Default Values, Integrate and  |
#           | Repair for hydro, trans, and   |
#           | utilities, updates UFI values, |
#           | deletes identical features,    |
#           | calculates geometry metrics,   |
#           | repairs all NULL geometries,   |
#           | and explodes all multipart     |
#           | features.                      |
#      _    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#   __(.)< ‾
#~~~\___)~~~


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
} #fcodeDict as ld

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
} #fcsubDict as ld

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


# User parameters
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
error_count = 0
featureclass = arcpy.ListFeatureClasses()


# Sanitizing GDB name
tds_split = TDS.split("\\")
tds_split.pop()
gdb_file = tds_split.pop()
name_list = gdb_file.split(".")
name_list.pop()
gdb_name = name_list[0]


# Tool title with GDB name
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
# if explode:
# 	exl = "_______"
# 	exs = "       "
if len(gdb_name) > 38:
	extra = len(gdb_name) - 38
	# if explode:
	# 	if extra > 5:
	# 		exl = ""
	# 		exs = ""
	# 		for i in range(extra):
	# 			exl += "_"
	# 			exs += " "
	# 	else:
	# 		pass
	# else:
	for i in range(extra):
		exl += "_"
		exs += " "

write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}{4}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

# Report of requested tasks
write(u"    |   ==== Processes Initialized ====          {0}|".format(exs))
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
	# if len(exs) <= 7:
	# 	write(u"    |     - Hypernova Burst Multipart Features   |")
	# else:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")


# Formatting Feature Class list
if arcpy.Exists('MetadataSrf'):
	featureclass.remove('MetadataSrf')
	write('MetadataSrf removed')
else:
	write('MetadataSrf not present')
if arcpy.Exists('ResourceSrf'):
	featureclass.remove('ResourceSrf')
	write('ResourceSrf removed')
else:
	write('ResourceSrf not present')
if vogon:
	if arcpy.Exists('StructurePnt'):
		featureclass.remove('StructurePnt')
	if arcpy.Exists('StructureSrf'):
		featureclass.remove('StructureSrf')
	write("StructureSrf and StructurePnt will be skipped in processing")
featureclass.sort()
write("Loaded {0} feature classes".format(len(featureclass)))


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


########## Data Maintenance Tools Category ##########

''''''''' Repair All NULL Geometry '''''''''

##### check for duplicate vertices in tolerance

# Repairs all NULL geometries in each feature class
if repair:
	tool_name = 'Repair All NULL Geometry'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			write("Repairing NULL geometries in " + str(fc))
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


''''''''' Populate F_Codes '''''''''
# John Jackson's Fcode tool refactored from standalone with included dictionaries instead of imported
if fcode:
	tool_name = 'Populate F_Codes'
	write("\n--- {0} ---\n".format(tool_name))
	for fc in featureclass:
		try:
			try:
				fields = ["f_code", "fcsubtype"]
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


''''''''' Calculate Default Values '''''''''
# Calculate default values for NULL attributes
# All or nothing. Functions on datasets not individual feature classes
if defaults:
	tool_name = 'Calculate Default Values'
	write("\n--- {0} ---\n".format(tool_name))
	write("Locating NULL fields...")
	try:
		write('Assigning domain defaults')
		arcpy.CalculateDefaultValues_defense(arcpy.env.workspace)
		write('Complete')
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


''''''''' Calculate Metrics '''''''''
# Calculates the metric values of the specified fields
if metrics:
	tool_name = 'Calculate Metrics'
	write("\n--- {0} ---\n".format(tool_name))
	metric_type = 'LENGTH;WIDTH;AREA;ANGLE_OF_ORIENTATION'
	for fc in featureclass:
		try:
			arcpy.AddMessage("Calculating AOO, ARA, LZN, and WID for " + str(fc))
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


''''''''' Update UFI Values ''''''''' ##### add functionality to only update blank fields
# Iterate through all features and update the ufi field with uuid4 random values
if ufi:
	tool_name = 'Update UFI Values'
	write("\n--- {0} ---\n".format(tool_name))
	ufi_count = 0
	for fc in featureclass:
		try:
			with arcpy.da.SearchCursor(fc, 'ufi') as scursor:
				values = [row[0] for row in scursor]
			with arcpy.da.UpdateCursor(fc, 'ufi') as ucursor:
				for row in ucursor:
					if values.count(row[0]) > 1:
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					elif row[0] is None:
						row[0] = str(uuid.uuid4())
						ufi_count += 1
					ucursor.updateRow(row)
				write('Updated UFIs in {0}'.format(fc))
		# try:
		# 	with arcpy.da.UpdateCursor(fc, 'ufi') as ucursor:
		# 		for row in ucursor:
		# 			row[0] = str(uuid.uuid4())
		# 			ucursor.updateRow(row)
		# 		write('Updated UFIs in ' + fc + '.')
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


########## Feature Specific Tools Category ##########

''''''''' Integrate and Repair '''''''''
# User choice to Integrate and Repair Hydrography curves, TransportationGround curves, or Utility points and surfaces to curves
if hydro or trans or util:
	tool_name = 'Integrate and Repair'
	write("\n--- {0} ---\n".format(tool_name))
if hydro:
	tool_name = 'Hydrography Curves'
	fc = 'HydrographyCrv'
	write("- - - - - - - - - - - - - - - - - - - - - - ")
	write(" ~ {0} ~ ".format(tool_name))
	write("Making {0} feature layers".format(fc))
	arcpy.MakeFeatureLayer_management(fc, "hc")
	arcpy.SelectLayerByAttribute_management("hc", "NEW_SELECTION", "zi026_ctuu >= 50000")
	arcpy.MakeFeatureLayer_management("hc", "hc_scale")
	write("Repairing {0} lines before Integration".format(fc))
	arcpy.RepairGeometry_management("hc_scale", "DELETE_NULL")
	hfeat_count = 0
	if not large:
		try:
			hfeat_count = int(arcpy.GetCount_management("hc_scale").getOutput(0))
			write("Integrating {0} {1} features".format(hfeat_count, fc))
			arcpy.Integrate_management('hc_scale', "0.06 Meters")
			arcpy.Integrate_management('hc_scale', "0.03 Meters")
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
			mem_fc = "in_memory\\{0}_grid".format(fc)
			rectangle = "in_memory\\rectangle"
			write("Defining partition envelope")
			arcpy.MinimumBoundingGeometry_management(fc, rectangle, "RECTANGLE_BY_AREA", "ALL", "", "")
			with arcpy.da.SearchCursor(rectangle, ['SHAPE@']) as scursor:
				for row in scursor:
					shape = row[0]
					origin_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMin)
					y_axis_coord = '{0} {1}'.format(shape.extent.XMin, shape.extent.YMax)
					corner_coord = '{0} {1}'.format(shape.extent.XMax, shape.extent.YMax)
			write("Constructing fishnet")
			arcpy.CreateFishnet_management(mem_fc, origin_coord, y_axis_coord, "", "", "2", "2", corner_coord, "NO_LABELS", fc, "POLYGON")
			#arcpy.CreateFishnet_management(out_feature_class="in_memory/hydro_grid", origin_coord="30 19.9999999997", y_axis_coord="30 29.9999999997", cell_width="", cell_height="", number_rows="2", number_columns="2", corner_coord="36.00000000003 24", labels="NO_LABELS", template="C:/Projects/njcagle/finishing/=========Leidos_247=========/J05B/TDSv7_1_J05B_JANUS_DO247_sub1_pre.gdb/TDS/HydrographyCrv", geometry_type="POLYGON")
			arcpy.MakeFeatureLayer_management(mem_fc, "hgrid")
			with arcpy.da.SearchCursor("hgrid", ['OID@']) as scursor:
				for row in scursor:
					select = "OID = {}".format(row[0])
					arcpy.SelectLayerByAttribute_management("hgrid", "NEW_SELECTION", select)
					arcpy.SelectLayerByLocation_management("hc_scale", "INTERSECT", "hgrid","","NEW_SELECTION")
					feat_count = int(arcpy.GetCount_management("hc_scale").getOutput(0))
					write("Integrating {0} {1} features in partition {2}".format(feat_count, fc, row[0]))
					arcpy.Integrate_management("hc_scale", "0.06 Meters")
					arcpy.Integrate_management("hc_scale", "0.03 Meters")
					hfeat_count += feat_count
			write("Freeing partition memory")
			arcpy.Delete_management("in_memory")
			arcpy.Delete_management("hgrid")
		except arcpy.ExecuteError:
			# if the code failed for the current fc, check the error
			error_count += 1
			write("\n***Failed to run {0}.***".format(tool_name))
			write(arcpy.GetMessages())
			write("\nData too dense to be run in partitions. Integrating {0} in this database exceeds our current equipment limitations.".format(fc))
			write("To continue running tool, uncheck {0} before running again.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)
	write("Repairing {0} lines after Integration".format(fc))
	arcpy.RepairGeometry_management("hc_scale", "DELETE_NULL")
	write("Clearing process cache")
	arcpy.Delete_management("hc")
	arcpy.Delete_management("hc_scale")
	write("- - - - - - - - - - - - - - - - - - - - - - \n")

if trans:
	tool_name = 'Transportation Points and Curves'
	fc1 = 'TransportationGroundPnt'
	fc2 = 'TransportationGroundCrv'
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
			write("Integrating {0} {1} features and {2} Culvert points.".format(feat_count, fc2, cul_count))
			if cul_count > 0:
				arcpy.Integrate_management("tgp_scale 2;tgc_scale 1", "0.06 Meters")
				arcpy.Integrate_management("tgp_scale 2;tgc_scale 1", "0.03 Meters")
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
					write("Integrating {0} {1} features and {2} Culvert points in partition {3}".format(feat_count, fc2, pcul_count, row[0]))
					tfeat_count = tfeat_count + feat_count + pcul_count
					if pcul_count > 0:
						arcpy.Integrate_management("tgp_scale 2;tgc_scale 1", "0.06 Meters")
						arcpy.Integrate_management("tgp_scale 2;tgc_scale 1", "0.03 Meters")
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
	write("- - - - - - - - - - - - - - - - - - - - - - \n")

if util:
	tool_name = 'Utility Points, Lines, and Surfaces'
	fc1 = 'UtilityInfrastructurePnt'
	fc2 = 'UtilityInfrastructureCrv'
	fc3 = 'UtilityInfrastructureSrf'
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
			write("Integrating {0} {1} features, {2} {3} features, and {4} {5} features".format(feat_count1, fc1, feat_count2, fc2, feat_count3, fc3))
			arcpy.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.06 Meters")
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
					write("Integrating {0} {1} features, {2} {3} features, and {4} {5} features in partition {6}".format(feat_count1, fc1, feat_count2, fc2, feat_count3, fc3, row[0]))
					arcpy.Integrate_management("up_scale 2;uc_scale 1;us_scale 3", "0.06 Meters")
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
	write("- - - - - - - - - - - - - - - - - - - - - - \n")


########## Geometry Correction Tools Category ##########

''''''''' Delete Identical Features '''''''''
# Checks for features with identical geometry and PSG attribution and removes them
if dups:
	tool_name = 'Delete Identical Features'
	write("\n--- {0} ---\n".format(tool_name))
	# Set the output directory for the FindIdentical tool
	out_table = os.path.dirname(arcpy.env.workspace)
	# Precreate the path for the output dBASE table
	path = out_table.split(".")
	path.pop()
	table_loc = path[0] + str(".dbf")
	write("Creating temporary output file: " + str(table_loc))
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
			error_count += 1
			os.remove(table_loc)
			os.remove(table_loc + str(".xml"))
			os.remove(path[0] + str(".cpg"))
			os.remove(path[0] + str(".IN_FID.atx"))
			arcpy.RefreshCatalog(out_table)
			write("\n***Failed to run {0}.***\n".format(tool_name))
			write("Error Report:")
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write(arcpy.GetMessages())
			write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			write("\nPlease rerun the tool, but uncheck the {0} tool option. Either the feature class is too big or something else has gone wrong. Large data handling for tools other than Integration will be coming in a future update.".format(tool_name))
			write("Exiting tool.\n")
			sys.exit(0)

	# Clean up before next process
	os.remove(table_loc)
	os.remove(table_loc + str(".xml"))
	os.remove(path[0] + str(".cpg"))
	os.remove(path[0] + str(".IN_FID.atx"))
	arcpy.RefreshCatalog(out_table)


''''''''' Hypernova Burst Multipart Features '''''''''
# Explodes multipart features for an entire dataset
if explode:
	tool_name = 'Hypernova Burst Multipart Features'
	write("\n--- {0} ---\n".format(tool_name))
	##### Multipart Search #####
	fc_multi = {} # Create empty dictionary to house lists of mulitpart features and their feature classes
	fc_multi_list = []
	total_multi = 0
	for fc in featureclass:
		try:
			write("Searching for multiparts in " + str(fc))
			multipart = False # Assume the feature class doesn't have multiparts
			with arcpy.da.SearchCursor(fc, ['OID@', 'SHAPE@']) as scursor:
				complex = 0 # Counts complex single part features. Mainly for debugging. Might remain in final
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
				if multipart is True:
					count = len(fc_multi[fc])
					write("*** " + str(count) + " true multipart features found in " + str(fc) + " ***")
				elif complex > 0:
					write(str(complex) + " complex polygons found in " + str(fc))
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
	if complex > 0:
		write("The complex polygons found are single part polygons with complex interior holes that are more likely to become multipart features.")
	write(" ")
	if fc_multi_list: # Only runs if fc_multi_list is not empty
		for fc in fc_multi_list:
			count = len(fc_multi[fc])
			total_multi += count
			write(str(count) + " multipart features found in " + str(fc))
			write("  OIDs - " + str(fc_multi[fc]))
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
				write('Error: Unknown Feature Class name found. If running on SDE, the aliasing may have changed. Contact SDE Admin.')


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
			query = str(oid_field) + " in ({})".format(oid_list_str) # Formats the query from the above variables as: OBJECTID in (1, 2, 3)

			# Create a new feature class to put the multipart features in to decrease processing time. fields based on original fc template
			arcpy.CreateFeatureclass_management(arcpy.env.workspace, in_class, fc_geom, fc, "", "", arcpy.env.workspace)

			# Add multipart features to new feature class based on OID
			with arcpy.da.SearchCursor(fc, fieldnames, query) as scursor: # Search current fc using fc_fields with OID@ and "oidid" prepended as [0,1] respectively. Queries for only OIDs in the multipart oid_list.
				with arcpy.da.InsertCursor(in_class, fieldnames) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
					for row in scursor: # For each feature in the current fc
						if row[0] in oid_list: # If the OID is in the oid_list of multipart features. Redundant since the scursor is queried for multipart OIDs, but meh
							icursor.insertRow(row) # Insert that feature row into the temp feature class, in_class "multi"

			write(str(fcr) + " multipart progenitor cores collapsing.")
			before_process = dt.now().time()
			arcpy.MultipartToSinglepart_management(in_class, out_class) # New feature class output of just the converted single parts
			after_process = dt.now().time()
			date = dt.now().date()
			datetime1 = dt.combine(date, after_process)
			datetime2 = dt.combine(date, before_process)
			time_delta = datetime1 - datetime2
			time_elapsed = str(time_delta.total_seconds())
			write("Hypernova burst detected after " + time_elapsed + " seconds.")

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

	write("All multipart feature have acheived supernova!")

	try:
		arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(in_class)))
		arcpy.Delete_management(str(arcpy.env.workspace) + str("\\" + str(out_class)))
		arcpy.Delete_management("curr_fc")
	except:
		write("No in_class or out_class created. Or processing layers have already been cleaned up. Continuing...")
		pass


if defaults or metrics or explode:
	if not no_defense:
		write("\n~~ Checking Defense Mapping Extension back in ~~\n")
		arcpy.CheckInExtension("defense")


# Report of completed tasks
def format_count(count):
	cnt_str = str(count)
	if len(cnt_str) > 0:
		for i in range(7-len(cnt_str)):
			cnt_str += " "
	else:
		pass
	return cnt_str

write(u"   _____{0}{3}__\n / \\    {1}{4}  \\\n|   |   {1}{4}   |\n \\_ |   {1}{4}   |\n    |   {5}{2}{6}{4}   |\n    |   {1}{4}   |".format(slines, sspaces, gdb_name, exl, exs, exgl, exgr))

write(u"    |   ===== Processes Completed =====          {0}|".format(exs))
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
	write(u"    |          {0} Duplicate or blank UFIs   {1}|".format(f_ufi_count, exs))
if hydro or trans or util:
	write(u"    |     - Integrated and Repaired:             {0}|".format(exs))
	if large:
		write(u"    |        ~ Large Dataset ~                   {0}|".format(exs))
	if hydro:
		f_hfeat_count = format_count(hfeat_count)
		write(u"    |          {0} Hydro                     {1}|".format(f_hfeat_count, exs))
	if trans:
		f_tfeat_count = format_count(tfeat_count)
		write(u"    |          {0} Trans                     {1}|".format(f_tfeat_count, exs))
	if util:
		f_ufeat_count = format_count(ufeat_count)
		write(u"    |          {0} Utilities                 {1}|".format(f_ufeat_count, exs))
if dups:
	f_dup_count = format_count(dup_count)
	write(u"    |     - Deleted Identical Features           {0}|".format(exs))
	write(u"    |          {0} Duplicates found          {1}|".format(f_dup_count, exs))
if explode:
	f_multi_count = format_count(total_multi)
	# if len(exs) <= 7:
	# 	write(u"    |     - Hypernova Burst Multipart Features   |")
	# else:
	write(u"    |     - Hypernova Burst Multipart Features   {0}|".format(exs))
	write(u"    |          {0} Features exploded         {1}|".format(f_multi_count, exs))

write(u"    |                              {0}      _       |\n    |                              {0}   __(.)<     |\n    |                              {0}~~~\\___)~~~   |".format(exs))
write(u"    |   {0}{2}___|___\n    |  /{1}{3}      /\n    \\_/_{0}{2}_____/".format(slines, sspaces, exl, exs))
write("\n")


# Easter Egg
if not vogon and not repair and not fcode and not defaults and not metrics and not ufi and not large and not hydro and not trans and not util and not dups and not explode:
	write("Kristen, click a check box and stop being cheeky.\n")

# Add causes and potential solutions to error log if necessary
if error_count != 0:
	write("\n\n\n\#\#\# Causes and Potential Solutions \#\#\#\n")
	write("999999 Errors:")
	write("The infamous 999999 error... ArcMap's equivalent of a *shrug*")
	write("ESRI Support defines the cause of this error as 'Something unexpected', which is incredibly helpful.")
	write("\t- There may be NULL geometry, short segments, self intersections, or other geometry problems in the feature class. This is a common cause.")
	write("\t\tIf you haven't already, try running the Repair Geometry tool from the XXX toolbox on the problem feature class.")
	write("\t- Check that the name of the input TDS is only alphanumeric and doesn't start with a number. (weird legacy ArcMap requirements)")
	write("\t- Make sure you have permissions to access the TDS you are working with. Always work with local copies, not files on the Q: or T:")
	write("\t- The feature class may be too big. This is a common problem for us working on limited hardware.")
	write("\t\tYou can try running the tool on a computer with more RAM. But our computers may not be capable.")
	write("\t\tYou could pull the problem feature class out of the GDB break it into smaller chunks. This is time consuming though and may not be enough.")
	write("\t- ArcMap may not be properly cleaning up its temp files. Try going to %localappdata%\\temp in the file explorer and deleteing everything in the folder.\n")
	write("999998 Errors:")
	write("This is 999999's drunk uncle. Similar to the previous error, but with ArcMap denying any and all responsibility.")
	write("\t- ESRI considers this a general 'operating system error' that could be 'various error conditions.'")
	write("\t- The main reason for this error is usually a feature class being too big.")
	write("\t- Some of the other solutions above might help if nothing else does.\n")
	write("If an error mentions Topology or the Topoengine, this is ArcMap scapegoating. These are also usually geometry or size issues. Same as above.\n")
	write("If the error is something other than these, the could be any number of causes. You can google the error or message Nat with a screenshot.\n\n")
	write("For more information, check out this article.\nDeath, Taxes and the Esri ArcGIS 999999 Error\nhttps://gisgeography.com/esri-arcgis-999999-error/")





#     del row,scursor
# onside=ShapeMake(shp,-angle)
# extent=onside.extent
# origPoint='%s %s' %(extent.XMin,extent.YMin)
# yPoint='%s %s' %(extent.XMin,extent.YMax)
# endPoint='%s %s' %(extent.XMax,extent.YMax)
# arcpy.CreateFishnet_management(tempf, origPoint,yPoint,
#                                "0", "0", nRows, nCols,endPoint,
#                                "NO_LABELS", "", "POLYGON")


# if hydro:
# 	tool_name = 'Integrate and Repair Hydro'
# 	fc = 'HydrographyCrv'
# 	try:
# 		# mem_fc = "in_memory\\{0}".format(fc)
# 		# # Create a new feature class to put the multipart features in to decrease processing time
# 		# arcpy.CreateFeatureclass_management(arcpy.env.workspace, in_class, fc_geom, fc, "", "", arcpy.env.workspace)
# 		#
# 		# # Add multipart features to new feature class based on OID
# 		# oid_list = fc_multi[fc]
# 		# with arcpy.da.SearchCursor(fc, sfields, query) as scursor: # Search current fc using fc_fields with OID@ prepended as [0]
# 		# 	with arcpy.da.InsertCursor(in_class, sfields) as icursor: # Insert cursor for the newly created feature class with the same fields as scursor
# 		# 		for row in scursor: # For each feature in the current fc
# 		# 			#write("if {0} in {1}:".format(row[0], oid_list))
# 		# 			if row[0] in oid_list:
# 		# 				#write("true. doing icursor.insertRow(row)")
# 		# 				icursor.insertRow(row)
# 		write("- - - - - - - - - - - - - - - - - - - - - - ")
# 		write("Repairing Hydro lines before Integration")
# 		arcpy.RepairGeometry_management(fc, "DELETE_NULL")
# 		write("Integrating Hydro")
# 		arcpy.Integrate_management(fc, "0.03 Meters")
# 		write("Repairing Hydro lines after Integration")
# 		write("- - - - - - - - - - - - - - - - - - - - - - ")
# 		arcpy.RepairGeometry_management(fc, "DELETE_NULL")
#
# ########
# 	except arcpy.ExecuteError:
# 		# if the code failed for the current fc, check the error
# 		error_count += 1
# 		write("\n***Failed to run {0} on {1}.".format(tool_name, fc))
# 		write("See potential solutions at the end of the script.")
# 		write(arcpy.GetMessages())
# 		write("Continuing to next process.\n")
# 		pass
# ########
#
# if trans:
# 	tool_name = 'Integrate and Repair Trans'
# 	try:
# 		write("- - - - - - - - - - - - - - - - - - - - - - ")
# 		write("Repairing Trans lines before Integration")
# 		arcpy.RepairGeometry_management('TransportationGroundCrv', "DELETE_NULL")
# 		write("Integrating Trans")
# 		arcpy.Integrate_management('TransportationGroundCrv', "0.03 Meters")
# 		write("Repairing Trans lines after Integration")
# 		write("- - - - - - - - - - - - - - - - - - - - - - ")
# 		arcpy.RepairGeometry_management('TransportationGroundCrv', "DELETE_NULL")
# 	except arcpy.ExecuteError as e:
# 		# if the code failed for the current fc, check the error
# 		if "999999" in e:
# 			error_count += 1
# 			write("The infamous 999999 error... ArcMap's equivalent of a *shrug*")
# 			write("See potential solutions at the end of the script.")
# 			write("***Failed to run {0} on {1}.\n\t{1}\n".format(tool_name, fc, e))
# 			pass
# 		if "999998" in e:
# 			error_count += 1
# 			write("The 999998 error is a general operating system error")
# 			write("See potential solutions at the end of the script.")
# 			write("***Failed to run {0} on {1}.\n\t{1}\n".format(tool_name, fc, e))
# 			pass
# 		else:
# 			# log other errors
# 			error_count += 1
# 			write("***Failed to run {0} on {1}.\n\t{1}\n".format(tool_name, fc, e))
# 		write(e)
# 		write("Continuing to next feature class.")
# 		pass
#
# if util:
# 	tool_name = 'Integrate and Repair Utility'
# 	try:
# 		write("- - - - - - - - - - - - - - - - - - - - - - ")
# 		write("Repairing Utility lines before Integration")
# 		arcpy.RepairGeometry_management('UtilityInfrastructureCrv', "DELETE_NULL")
# 		write("Integrating Utilities")
# 		arcpy.Integrate_management("UtilityInfrastructurePnt 2;UtilityInfrastructureCrv 1;UtilityInfrastructureSrf 3", "0.03 Meters")
# 		write("Repairing Utility lines after Integration")
# 		write("- - - - - - - - - - - - - - - - - - - - - - ")
# 		arcpy.RepairGeometry_management('UtilityInfrastructureCrv', "DELETE_NULL")
# 	except arcpy.ExecuteError as e:
# 		# if the code failed for the current fc, check the error
# 		if "999999" in e:
# 			error_count += 1
# 			write("The infamous 999999 error... ArcMap's equivalent of a *shrug*")
# 			write("See potential solutions at the end of the script.")
# 			write("***Failed to run {0} on {1}.\n\t{1}\n".format(tool_name, fc, e))
# 			pass
# 		if "999998" in e:
# 			error_count += 1
# 			write("The 999998 error is a general operating system error")
# 			write("See potential solutions at the end of the script.")
# 			write("***Failed to run {0} on {1}.\n\t{1}\n".format(tool_name, fc, e))
# 			pass
# 		else:
# 			# log other errors
# 			error_count += 1
# 			write("***Failed to run {0} on {1}.\n\t{1}\n".format(tool_name, fc, e))
# 		write(e)
# 		write("Continuing to next feature class.")
# 		pass



# # Tool title with GDB name
# write("\nRunning Finishing Tools on:\n")
# slines = u""
# sspaces = u""
# for i in range(len(gdb_name)):
# 	slines += u"_"
# 	sspaces += u" "
# write(u"   _____{0}__\n / \\    {1}  \\\n|   |   {1}   |\n \\_ |   {1}   |\n    |   {2}   |\n    |   {1}   |\n    |   {0}___|___\n    |  /{1}      /\n    \\_/_{0}_____/\n".format(slines, sspaces, gdb_name))

# # Report of requested tasks
# write("=== Processes Initialized ===\n")
# if repair:
# 	write("  - Repair Geometries")
# if fcode:
# 	write("  - Populate F_Codes")
# if defaults:
# 	write("  - Calculate Default Values")
# if metrics:
# 	write("  - Calculate Metrics")
# if ufi:
# 	write("  - Update UFI Values")
# if hydro or trans or util:
# 	write("  - Integrated and Repaired:")
# 	if large:
# 		write("      ~Large Dataset~")
# 	if hydro:
# 		write("       Hydro")
# 	if trans:
# 		write("       Trans")
# 	if util:
# 		write("       Utilities")
# if dups:
# 	write("  - Delete Identical Features")
# if explode:
# 	write("  - Hypernova Burst Multipart Features")
# write("\n")
#
# # Report of completed tasks
# write("=== Processes Completed ===\n")
# if repair:
# 	write("  - Repaired All NULL Geometries\n")
# if fcode:
# 	write("  - Populated F_Codes\n")
# if defaults:
# 	write("  - Calculated Default Values\n")
# if metrics:
# 	write("  - Calculated Metrics (AOO, ARA, LZN, and WID)\n")
# if ufi:
# 	write("  - Updated UFI Values\n")
# if hydro or trans or util:
# 	if large:
# 		write("  - Integrated and Repaired Large Dataset:")
# 	else:
# 		write("  - Integrated and Repaired:")
# 	if hydro:
# 		write("       Hydro\n")
# 	if trans:
# 		write("       Trans\n")
# 	if util:
# 		write("       Utilities\n")
# if dups:
# 	write("  - Deleted Identical Features\n")
# if explode:
# 	write("  - Hypernova Burst Multipart Features\n")

