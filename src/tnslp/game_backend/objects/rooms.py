
import tnslp.game_backend.classes.room_class as room_class
import tnslp.game_backend.objects.items as item
import tnslp.game_backend.objects.npcs as npc

### Ward Rooms ###
# display names must be 11 characters or less

game_exit = room_class.Ward_Room(
    "Game Exit", #room name #add article "the"
    "Game Exit", #display name
    "No Room Description", #description
    None, #room label or none
    (None, None), #items for ground, walls - must be lists of items
    [None, item.admissions_exit_door, None, None] #doors or none
    )

admissions = room_class.Ward_Room(  
    "Admissions", 
    "Admissions", 
    "A sparsely decorated room, a few chairs in the corner, and desks at which staff sit focused on their work", 
    "",
    (None, None),
    [None, None, None, item.admissions_exit_door])

service_hallway = room_class.Ward_Room(
    "Service Hallway", #add article "the"
    "Serv. Hall", 
    "A clean hallway, clearly used purely for servicing the various rooms along the hall", 
    "",
    (None, None),
    [item.security_and_service_hallway_door, item.service_hallway_and_common_room_door, item.courtyard_and_service_hallway_door, [None, None]])

utility_closet = room_class.Ward_Room(
    "Utility Closet", #add article "the"
    "Utilities",
    "No Room Description", 
    "", 
    (None, [item.uc_cleaning_shelf, item.uc_hygiene_shelf]),
    None)

security_room = room_class.Ward_Room(
    "Security Unit", #add article "the"
    "Security", 
    "No Room Description", 
    "",
    (None, None),
    [None, item.security_and_red_hallway_door, item.security_and_service_hallway_door, None])

outside_time = room_class.Ward_Room(
    "Outside Courtyard", #add article "the"
    "Outside",
    "A brick courtyard, with walls twelve feet high, and no way to climb them. A park bench sits off to one side with a large open space taking up the majority.", 
    "", 
    ([item.park_bench, item.toys_bag], None),
    [item.courtyard_and_service_hallway_door, None, None, None]) 

common_room = room_class.Starting_Ward_Room(
    "Common Room", #add article "the"
    "Common Room", 
    "A common area filled with tables and chairs, with cabinets lining a few walls.", 
    "",
    ([item.cr_art_table, item.cr_game_cabinets, item.cr_ping_pong_table], [item.doors_poster]),
    [[None, item.common_room_and_staff_breakroom, item.common_room_and_medications], [None, item.common_room_and_ward_landing_door], [None, None], item.service_hallway_and_common_room_door])

tv_room = room_class.Ward_Room(
    "TV Room", #add article "the"
    "TV Room", 
    "A small room with a few chairs facing a tv mounted on the far wall.", 
    "",
    ([item.tv_coffee_table], None),
    None)


staff_breakroom = room_class.Ward_Room(
    "Staff Breakroom", #add article "the"
    "Staff Break",
    "No Room Description", 
    "", 
    (None, None),
    [None, None, item.common_room_and_staff_breakroom, None])

med_station = room_class.Ward_Room(
    "Medication Room", #add article "the"
    "Meds Room", 
    "A window at which patients can receive medications.", 
    "",
    ([item.mw_recycle_bin, item.mw_trash_bin], None), 
    [None, None, item.common_room_and_medications, None])

bathroom_cr = room_class.Ward_Room(
    "Common Room Bathroom", #add article "the"
    "CR Bathroom", 
    "A safety-proofed bathroom, with sloped handles and polished metal for mirrors.", 
    "", 
    (None, [item.faucets_poster]),
    None)

library = room_class.Ward_Room(
    "Library", #add article "the"
    "Library", 
    "No Room Description", 
    "",
    (None, [item.lib_classic_bookshelf, item.lib_nf_bookshelf, item.lib_fant_bookshelf, item.lib_help_bookshelf]),
    None)

blue_hallway = room_class.Ward_Room(
    "Blue Hallway", #add article "the"
    "Blue Hall", 
    "A clean hallway with blue floor tiling.", 
    "", 
    (None, None),
    None)

kitchen = room_class.Ward_Room(
    "Servery", #add article "the"
    "Servery", 
    "A small dining room, also used as a place to receive food at mealtimes.", 
    "", 
    ([item.serv_counter, item.serv_tableware_bin], None),
    None)

sensory_room = room_class.Ward_Room(
    "Sensory Room", #add article "the"
    "Sensory", 
    "A well-decorated room, full of comfortable seating and pillows, along with toys and gadgets to keep patients busy.", 
    "",
    (None, None),
    None)

linen_closet = room_class.Ward_Room(
    "Linen Closet", #add article "the"
    "Linens", 
    "No Room Description", 
    "", 
    (None, [item.lr_bedding_shelf, item.lr_towels_shelf]),
    None)

red_hallway = room_class.Ward_Room(
    "Red Hallway", #add article "the"
    "Red Hall", 
    "A clean hallway with red floor tiling", 
    "",
    (None, None),
    [[None, None], None, [None, None, None], item.security_and_red_hallway_door])

pat_room_101 = room_class.Ward_Room(
    "Patient Room 101", 
    "Room 101", 
    "A common patient room with two beds.", 
    "",
    (None, None), 
    None)

pat_room_103 = room_class.Ward_Room(
    "Patient Room 103", 
    "Room 103", 
    "A common patient room with two beds.", 
    "",
    (None, None),
    None)

bathroom_p = room_class.Ward_Room(
    "Patient Bathroom", #add article "the"
    "P. Bathroom", 
    "A small bathroom for patient use.", 
    "",
    (None, None),
    None)

pat_room_102 = room_class.Ward_Room(
    "Patient Room 102", 
    "Room 102", 
    "A common patient room with two beds.", 
    "",
    (None, None),
    None) #randomize player room

pat_room_104 = room_class.Ward_Room(
    "Patient Room 104", 
    "Room 104", 
    "A common patient room with two beds.", 
    "", 
    (None, None),
    None)


######################    
### Basement Rooms ###
######################   

basement_lobby = room_class.Basement_Room(
    "Basement Lobby", #add article "the"
    "B. Lobby", 
    "No Room Description",
    "",
    (None, None),
    None)

old_nurses_station = room_class.Basement_Room(
    "Old Nursing Station", #add article "the"
    "B. Nursing",  
    "No Room Description", 
    "",
    (None, None),
    None)

old_med_window = room_class.Basement_Room(
    "Old Medication Window", #add article "the"
    "B. Meds", 
    "No Room Description",
    "",
    (None, None),
    None)

old_medical_storage = room_class.Basement_Room(
    "Old Medical Storage", #add article "the"
    "Med. Storage", 
    "No Room Description",
    "",
    (None, None),
    None)

sedation_room = room_class.Basement_Room(
    "Sedation Room", #add article "the"
    "Sedation",
    "No Room Description",
    "",
    (None, None),
    None)

residential_hallway = room_class.Basement_Room(
    "Residential Hallway", #add article "the"
    "Res. Hall", 
    "No Room Description",
    "",
    (None, None),
    None)

old_residential_bedroom = room_class.Basement_Room(
    "Old Residential Bedroom", #add article "the"
    "Res. Bed.", 
    "No Room Description",
    "",
    (None, None),
    None)

power_room = room_class.Basement_Room(
    "Power Room", #add article "the"
    "Power Room", 
    "No Room Description",
    "",
    (None, None),
    [None, item.power_room_door, None, None])

waiting_room = room_class.Basement_Room(
    "Waiting Room", #add article "the"
    "Wait Room", 
    "No Room Description",
    "",
    (None, None),
    None)

old_therapy_room = room_class.Basement_Room(
    "Old Therapy Room", #add article "the"
    "Therapy R.", 
    "No Room Description",
    "",
    (None, None),
    None)

clinical_hallway = room_class.Basement_Room(
    "Clinical Hallway", #add article "the"
    "Clin. Hall", 
    "No Room Description",
    "",
    (None, None),
    None)

straightjacket_storage = room_class.Basement_Room(
    "Straightjacket Storage", 
    "SJ Storage", 
    "No Room Description",
    "",
    (None, None),
    None)

tanning_bed_cell = room_class.Basement_Room(
    "Confinement", 
    "Confinement", 
    "No Room Description",
    "",
    (None, None),
    None)

high_security_area = room_class.Basement_Room(
    "High Security Wing", #add article "the"
    "High Sec.", 
    "No Room Description",
    "",
    (None, None),
    None)

shock_therapy_room = room_class.Basement_Room(
    "Shock Therapy Room", #add article "the"
    "Shk. Therapy",
    "No Room Description",
    "",
    (None, None),
    None)

### Basement / Maze:Boiler Rooms ? ###

########################################   
### Basement / Plexiglass Final Room ###
########################################
"""
plexiglass_cell = room_class.Final_Room(
    "Plexiglass Cell", #name
    "Demon Cell", #display name 
    "No Room Description", #description
    "", #room label
    (None, None))
""" 

###################################
### Stair Landings / Stairwells ###
###################################

# Stairwells to connect the ward and basement
ward_landing = room_class.Ward_Room(
    "Ward Landing", #add article "the"
    "Stairs 1",
    "A dimly lit stairwell, leading to a floor below.", 
    "", 
    (None, None),
    [None, None, None, item.common_room_and_ward_landing_door])

basement_landing = room_class.Basement_Room(
    "Basement Landing", #room name #add article "the"
    "Stairs B", #display name
    "No Room Description", #description
    "", #room label or none
    (None, None),
    None #doors or none
    ) 

basement_to_ward_stairs = room_class.Stairwell("Stairs Up", "Stairs Up", "", ward_landing)
ward_to_basement_stairs = room_class.Stairwell("Stairs Down", "Stairs Down", "", basement_landing)


## Landing Coordinates ## 
basement_landing.set_coordinates(0, 0, basement_to_ward_stairs, basement_lobby)
ward_landing.set_coordinates(0, 0, ward_to_basement_stairs, common_room)

## Ward Coordinates ##

admissions.set_coordinates(0, service_hallway, 0, game_exit)
service_hallway.set_coordinates(security_room, common_room, outside_time, [utility_closet, admissions])
utility_closet.set_coordinates(0, service_hallway, 0, 0)
outside_time.set_coordinates(service_hallway, 0, 0, 0)
security_room.set_coordinates(0, red_hallway, service_hallway, 0)

common_room.set_coordinates([tv_room, staff_breakroom, med_station], [blue_hallway, ward_landing], [library, bathroom_cr], service_hallway)
tv_room.set_coordinates(0, 0, common_room, 0)
staff_breakroom.set_coordinates(0, med_station, common_room, 0)
med_station.set_coordinates(0, 0, common_room, staff_breakroom)
library.set_coordinates(common_room, 0, 0, 0)
bathroom_cr.set_coordinates(common_room, 0, 0, 0)

blue_hallway.set_coordinates(0, [linen_closet, sensory_room, kitchen], 0, [common_room, red_hallway])
kitchen.set_coordinates(0, 0, 0, blue_hallway)
sensory_room.set_coordinates(0, 0, 0, blue_hallway)
linen_closet.set_coordinates(0, 0, 0, blue_hallway)

red_hallway.set_coordinates([pat_room_103, pat_room_101], blue_hallway, [bathroom_p, pat_room_102, pat_room_104], security_room)
bathroom_p.set_coordinates(red_hallway, 0, 0, 0)
pat_room_102.set_coordinates(red_hallway, 0, 0, 0)
pat_room_104.set_coordinates(red_hallway, 0, 0, 0)
pat_room_101.set_coordinates(0, 0, red_hallway, 0)
pat_room_103.set_coordinates(0, 0, red_hallway, 0)


## Basement Coordinates ##

basement_lobby.set_coordinates(residential_hallway, basement_landing, waiting_room, [old_nurses_station, old_med_window])
old_nurses_station.set_coordinates(old_med_window, basement_lobby, 0, old_medical_storage)
old_med_window.set_coordinates(0, basement_lobby, old_nurses_station, 0)
old_medical_storage.set_coordinates(0, old_nurses_station, 0, 0)

residential_hallway.set_coordinates(old_residential_bedroom, sedation_room, basement_lobby, 0)
sedation_room.set_coordinates(0, 0, 0, residential_hallway)
old_residential_bedroom.set_coordinates(0, 0, residential_hallway, 0)

waiting_room.set_coordinates(basement_lobby, 0, old_therapy_room, clinical_hallway)
clinical_hallway.set_coordinates(0, waiting_room, [straightjacket_storage, tanning_bed_cell], high_security_area)
old_therapy_room.set_coordinates(waiting_room, 0, 0, 0)
straightjacket_storage.set_coordinates(clinical_hallway, 0, 0, 0)
tanning_bed_cell.set_coordinates(clinical_hallway, 0, 0, 0)

high_security_area.set_coordinates(shock_therapy_room, clinical_hallway, 0, 0)
shock_therapy_room.set_coordinates(0, 0, high_security_area, 0)
#plexiglass_cell.set_coordinates(0, high_security_area, 0, 0)
