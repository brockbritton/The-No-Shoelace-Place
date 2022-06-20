
import tnslp.game_backend.classes.room_class as room_class
import tnslp.game_backend.objects.items as item
import tnslp.game_backend.objects.npcs as npc

# Stairwells
ward_landing = room_class.Ward_Room(
    "Ward Landing", 
    "Stairs 1",
    "A dimly lit stairwell, leading to a floor below.", 
    "",
    None, 
    (None, None),
    None)

basement_landing = room_class.Basement_Room(
    "Basement Landing", #room name
    "Stairs B", #display name
    "", #description
    "", #room label or none
    None, #storage units or none
    (None, None),
    None #doors or none
    )

basement_to_ward_stairs = room_class.Stairwell("Stairs Up", "Stairs Up", "", ward_landing)
ward_to_basement_stairs = room_class.Stairwell("Stairs Down", "Stairs Down", "", basement_landing)


### Ward Rooms ###
# display names must be 11 characters or less

game_entrance = room_class.Ward_Room(
    "Game Entrance", #room name
    "Game Ent.", #display name
    "", #description
    "", #room label or none
    None, #extra storage units or none
    (None, None), #items for ground, walls
    None #doors or none
    )


admissions = room_class.Ward_Room(
    "Admissions", 
    "Admissions", 
    "A sparsely decorated room, a few chairs in the corner, and desks at which staff sit focused on their work", 
    "",
    None, 
    (None, None),
    [item.admissions_entrance, item.service_hallway_w, None, None])

service_hallway = room_class.Ward_Room(
    "Service Hallway", 
    "Serv. Hall", 
    "A clean hallway, clearly used purely for servicing the various rooms along the hall", 
    "",
    None, 
    (None, None),
    [None, item.service_hallway_e, item.outside_time_n, [None, item.service_hallway_w]])

outside_time = room_class.Ward_Room(
    "Outside Courtyard", 
    "Outside",
    "A brick courtyard, with walls twelve feet tall, and no way to climb them. A park bench sits off to one side with a large open space taking up the majority.", 
    "",
    [item.park_bench, item.toys_bag], 
    (None, None),
    [item.outside_time_n, None, None, None]) #adds happiness


utility_closet = room_class.Ward_Room(
    "Utility Closet", 
    "Utilities",
    "", 
    "",
    [item.uc_cleaning_shelf, item.uc_hygiene_shelf], 
    (None, None),
    None)

common_room = room_class.Ward_Room(
    "Common Room", 
    "Common Room", 
    "A common area filled with tables and chairs, with cabinets lining a few walls.", 
    "",
    [item.cr_art_table, item.cr_game_cabinets, item.cr_ping_pong_table], 
    (None, [item.doors_poster]),
    [[None, None, None], [None, item.ward_to_basement_door], [None, None], item.service_hallway_e])

tv_room = room_class.Ward_Room(
    "TV Room", 
    "TV Room", 
    "A small room with a few chairs facing a tv mounted on the far wall.", 
    "",
    [item.tv_coffee_table], 
    (None, None),
    None)

library = room_class.Ward_Room(
    "Library", 
    "Library", 
    "", 
    "",
    [item.lib_classic_bookshelf, item.lib_nf_bookshelf, item.lib_fant_bookshelf, item.lib_help_bookshelf], 
    (None, None),
    None)

staff_breakroom = room_class.Ward_Room(
    "Staff Breakroom", 
    "Staff Break",
    "", 
    "",
    None, 
    (None, None),
    None)

med_station = room_class.Ward_Room(
    "Medication Room", 
    "Meds Room", 
    "A window at which patients can receive medications.", 
    "",
    [item.mw_recycle_bin, item.mw_trash_bin],
    (None, None), 
    None)

bathroom_cr = room_class.Ward_Room(
    "Common Room Bathroom", 
    "CR Bathroom", 
    "A safety-proofed bathroom, with sloped handles and polished metal for mirrors.", 
    "",
    None, 
    (None, None),
    None)

blue_hallway = room_class.Ward_Room(
    "Blue Hallway", 
    "Blue Hall", 
    "A clean hallway with blue floor tiling.", 
    "",
    None, 
    (None, None),
    None)

kitchen = room_class.Ward_Room(
    "Servery", 
    "Servery", 
    "A small dining room, also used as a place to receive food at mealtimes.", 
    "",
    [item.serv_counter, item.serv_tableware_bin], 
    (None, None),
    None) #adds happiness

sensory_room = room_class.Ward_Room(
    "Sensory Room", 
    "Sensory", 
    "A well-decorated room, full of comfortable seating and pillows, along with toys and gadgets to keep patients busy.", 
    "",
    None, 
    (None, None),
    None)

linen_closet = room_class.Ward_Room(
    "Linens", 
    "Linens", 
    "", 
    "",
    [item.lr_bedding_shelf, item.lr_towels_shelf], 
    (None, None),
    None)

red_hallway = room_class.Ward_Room(
    "Red Hallway", 
    "Red Hall", 
    "A clean hallway with red floor tiling", 
    "",
    None, 
    (None, None),
    None)

pat_room_202 = room_class.Ward_Room(
    "Room 202", 
    "Room 202", 
    "A common patient room with two beds.", 
    "",
    None, 
    (None, None),
    None) #randomize player room

pat_room_204 = room_class.Ward_Room(
    "Room 204", 
    "Room 204", 
    "A common patient room with two beds.", 
    "",
    None, 
    (None, None),
    None)

pat_room_201 = room_class.Ward_Room(
    "Room 201", 
    "Room 201", 
    "A common patient room with two beds.", 
    "",
    None, 
    (None, None),
    None)

pat_room_203 = room_class.Ward_Room(
    "Room 203", 
    "Room 203", 
    "A common patient room with two beds.", 
    "",
    None, 
    (None, None),
    None)

bathroom_p = room_class.Ward_Room(
    "Patient Bathroom", 
    "P. Bathroom", 
    "A small bathroom for patient use.", 
    "",
    None, 
    (None, None),
    None)

######################    
### Basement Rooms ###
######################   

basement_lobby = room_class.Basement_Room(
    "Basement Lobby", 
    "B. Lobby", 
    "",
    "",
    None,
    (None, None),
    None)

old_nurses_station = room_class.Basement_Room(
    "Old Nursing Station", 
    "Nursing", 
    "",
    "",
    None,
    (None, None),
    None)

old_med_window = room_class.Basement_Room(
    "Old Medication Window", 
    "B. Meds", 
    "",
    "",
    None,
    (None, None),
    None)

old_medical_storage = room_class.Basement_Room(
    "Old Medical Storage", 
    "Med. Storage", 
    "",
    "",
    None,
    (None, None),
    None)

sedation_room = room_class.Basement_Room(
    "Sedation Room", 
    "Sedation",
    "",
    "",
    None,
    (None, None),
    None)

residential_hallway = room_class.Basement_Room(
    "Residential Hallway", 
    "Res. Hall", 
    "",
    "",
    None,
    (None, None),
    None)

old_residential_bedroom = room_class.Basement_Room(
    "Old Residential Bedroom", 
    "Res. Bed.", 
    "",
    "",
    None,
    (None, None),
    None)

power_room = room_class.Basement_Room(
    "Power Room", 
    "Power Room", 
    "",
    "",
    None,
    (None, None),
    [None, item.power_room_door, None, None])

waiting_room = room_class.Basement_Room(
    "Waiting Room", 
    "Waiting R.", 
    "",
    "",
    None,
    (None, None),
    None)

old_therapy_room = room_class.Basement_Room(
    "Old Therapy Room", 
    "Therapy R.", 
    "",
    "",
    None,
    (None, None),
    None)

clinical_hallway = room_class.Basement_Room(
    "Clinical Hallway", 
    "Clin. Hall", 
    "",
    "",
    None,
    (None, None),
    None)

straightjacket_storage = room_class.Basement_Room(
    "Straightjacket Storage", 
    "SJ Storage", 
    "",
    "",
    None,
    (None, None),
    None)

tanning_bed_cell = room_class.Basement_Room(
    "Confinement", 
    "Confinement", 
    "",
    "",
    None,
    (None, None),
    None)

high_security_area = room_class.Basement_Room(
    "High Security Wing", 
    "High Sec.", 
    "",
    "",
    None,
    (None, None),
    None)

shock_therapy_room = room_class.Basement_Room(
    "Shock Therapy Room", 
    "Shk. Therapy",
    "",
    "",
    None,
    (None, None),
    None)

####################################    
### Basement / Maze:Boiler Rooms ###
####################################

maze_int1 = room_class.Maze_Room(
    "A Dark Intersection", 
    "",
    (None, None),
    None)

maze_south_end1 = room_class.Maze_Room(
    "A Dead End", 
    "",
    (None, None),
    None)

maze_north_end1 = room_class.Maze_Room(
    "A Dead End", 
    "",
    (None, None),
    None)

maze_int2 = room_class.Maze_Room(
    "A Dark Intersection", 
    "",
    (None, None),
    None)

maze_int3 = room_class.Maze_Room(
    "A Dark Intersection", 
    "",
    (None, None),
    None)

maze_west_end1 = room_class.Maze_Room(
    "A Dead End", 
    "",
    (None, None),
    None)

maze_int4 = room_class.Maze_Room(
    "A Dark Intersection", 
    "",
    (None, None),
    None)

maze_east_end1 = room_class.Maze_Room(
    "A Dead End", 
    "",
    (None, None),
    None)

maze_int5 = room_class.Maze_Room(
    "A Dark Intersection", 
    "",
    (None, None),
    None)

maze_north_end2 = room_class.Maze_Room(
    "A Dead End", 
    "",
    (None, None),
    None)

maze_int6 = room_class.Maze_Room(
    "A Dark Intersection", 
    "",
    (None, None),
    [None, None, None, item.power_room_door])

maze_east_end2 = room_class.Maze_Room(
    "A Dead End", 
    "",
    (None, None),
    None)

########################################   
### Basement / Plexiglass Final Room ###
########################################

plexiglass_cell = room_class.Final_Room(
    "Plexiglass Cell", #name
    "", #display name 
    "", #description
    "", #room label
    None #doors
    )


## Landing Coordinates ##
basement_landing.set_coordinates(basement_to_ward_stairs, 0, 0, basement_lobby)
ward_landing.set_coordinates(ward_to_basement_stairs, 0, 0, common_room)

## Ward Coordinates ##

admissions.set_coordinates(game_entrance, service_hallway, 0, 0)
service_hallway.set_coordinates(0, common_room, outside_time, [utility_closet, admissions])
utility_closet.set_coordinates(0, service_hallway, 0, 0)
outside_time.set_coordinates(service_hallway, 0, 0, 0)

common_room.set_coordinates([tv_room, staff_breakroom, med_station], [blue_hallway, ward_landing], [library, bathroom_cr], service_hallway) ###
tv_room.set_coordinates(0, 0, common_room, 0)
staff_breakroom.set_coordinates(0, med_station, common_room, 0)
med_station.set_coordinates(0, 0, common_room, staff_breakroom)
library.set_coordinates(common_room, 0, 0, 0)
bathroom_cr.set_coordinates(common_room, 0, 0, 0)

blue_hallway.set_coordinates(red_hallway, [kitchen, sensory_room], 0, [common_room, linen_closet])
kitchen.set_coordinates(0, 0, 0, blue_hallway)
sensory_room.set_coordinates(0, 0, 0, blue_hallway)
linen_closet.set_coordinates(0, blue_hallway, 0, 0)

red_hallway.set_coordinates(0, [pat_room_204, pat_room_202], blue_hallway, [pat_room_201, pat_room_203, bathroom_p])
bathroom_p.set_coordinates(0, red_hallway, 0, 0)
pat_room_201.set_coordinates(0, red_hallway, 0, 0)
pat_room_203.set_coordinates(0, red_hallway, 0, 0)
pat_room_202.set_coordinates(0, 0, 0, red_hallway)
pat_room_204.set_coordinates(0, 0, 0, red_hallway)

## Basement Coordinates ##

basement_lobby.set_coordinates(residential_hallway, basement_landing, waiting_room, [old_nurses_station, old_med_window])
old_nurses_station.set_coordinates(old_med_window, basement_lobby, 0, old_medical_storage)
old_med_window.set_coordinates(0, basement_lobby, old_nurses_station, 0)
old_medical_storage.set_coordinates(0, old_nurses_station, 0, 0)

residential_hallway.set_coordinates(old_residential_bedroom, sedation_room, basement_lobby, maze_int1)
sedation_room.set_coordinates(0, 0, 0, residential_hallway)
old_residential_bedroom.set_coordinates(0, 0, residential_hallway, 0)

maze_int1.set_coordinates(maze_north_end1, residential_hallway, maze_south_end1, maze_int2)
maze_south_end1.set_coordinates(maze_int1, 0, 0, 0)
maze_north_end1.set_coordinates(0, 0, maze_int1, 0)
maze_int2.set_coordinates(maze_int3, maze_int1, maze_int3, 0)
maze_int3.set_coordinates(maze_int2, 0, 0, maze_west_end1)
maze_west_end1.set_coordinates(0, maze_int3, 0, 0)
maze_int4.set_coordinates(0, maze_east_end1, maze_int3, maze_int5)
maze_east_end1.set_coordinates(0, 0, 0, maze_int4)
maze_int5.set_coordinates(maze_north_end2, maze_int4, maze_int6, 0)
maze_north_end2.set_coordinates(0, 0, maze_int5, 0)
maze_int6.set_coordinates(maze_int5, maze_east_end2, 0, power_room)
maze_east_end2.set_coordinates(0, 0, 0, maze_int6)

power_room.set_coordinates(0, maze_int6, 0, 0)

waiting_room.set_coordinates(basement_lobby, 0, old_therapy_room, clinical_hallway)
clinical_hallway.set_coordinates(0, waiting_room, [straightjacket_storage, tanning_bed_cell], high_security_area)
old_therapy_room.set_coordinates(waiting_room, 0, 0, 0)
straightjacket_storage.set_coordinates(clinical_hallway, 0, 0, 0)
tanning_bed_cell.set_coordinates(clinical_hallway, 0, 0, 0)

high_security_area.set_coordinates(shock_therapy_room, clinical_hallway, 0, plexiglass_cell)
shock_therapy_room.set_coordinates(0, 0, high_security_area, 0)
plexiglass_cell.set_coordinates(0, high_security_area, 0, 0)
