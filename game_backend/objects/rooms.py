
import game_backend.classes.room_class as room_class
import game_backend.objects.items as item
import game_backend.objects.npcs as npc

### Ward Rooms ###

game_entrance = room_class.Ward_Room("Game Entrance", "", "")

admissions = room_class.Ward_Room("Admissions", 
    "A sparsely decorated room, a few chairs in the corner, and desks at which staff sit focused on their work", 
    "")
service_hallway = room_class.Ward_Room("Service Hallway", 
    "A clean hallway, clearly used purely for servicing the various rooms along the hall", 
    "")
outside_time = room_class.Ward_Room("Outside Time", 
    "A brick courtyard, with walls twelve feet tall, and no way to climb them. A park bench sits off to one side with a large open space taking up the majority.", 
    "") #adds happiness
utility_closet = room_class.Ward_Room("Utility Closet", 
    "", 
    "")

common_room = room_class.Ward_Room("Common Room", 
    "A common area filled with tables and chairs, with cabinets lining a few walls.", 
    "")
tv_room = room_class.Ward_Room("TV Room", 
    "A small room with a few chairs facing a tv mounted on the far wall.", 
    "")
library = room_class.Ward_Room("Library", 
    "", 
    "")
staff_breakroom = room_class.Ward_Room("Staff Breakroom", 
    "", 
    "")
med_station = room_class.Ward_Room("Med Station", 
    "A window at which patients can receive medications.", 
    "")
ward_stairs = room_class.Ward_Room("Stairs Level One", 
    "A dimly lit stairwell, leading to a floor below.", 
    "")
bathroom_cr = room_class.Ward_Room("CR Bathroom", 
    "A safety-proofed bathroom, with sloped handles and polished metal for mirrors.", 
    "")

blue_hallway = room_class.Ward_Room("Blue Hallway", 
    "A clean hallway with blue floor tiling.", 
    "")
kitchen = room_class.Ward_Room("Servery", 
    "A small dining room, also used as a place to receive food at mealtimes.", 
    "") #adds happiness
sensory_room = room_class.Ward_Room("Sensory Room", 
    "A well-decorated room, full of comfortable seating and pillows, along with toys and gadgets to keep patients busy.", 
    "")
linen_closet = room_class.Ward_Room("Linen Closet", 
    "", 
    "")

red_hallway = room_class.Ward_Room("Red Hallway", 
    "A clean hallway with red floor tiling", 
    "")
pat_room_202 = room_class.Ward_Room("Room 201", 
    "A common patient room with two beds.", 
    "") #randomize player room
pat_room_204 = room_class.Ward_Room("Room 202", 
    "A common patient room with two beds.", 
    "")
pat_room_201 = room_class.Ward_Room("Room 203", 
    "A common patient room with two beds.", 
    "")
pat_room_203 = room_class.Ward_Room("Room 204", 
    "A common patient room with two beds.", 
    "")
bathroom_p = room_class.Ward_Room("Patient Bathroom", 
    "A small bathroom for patient use.", 
    "")


admissions.set_coordinates(game_entrance, service_hallway, 0, 0)
service_hallway.set_coordinates(0, common_room, outside_time, [utility_closet, admissions])
utility_closet.set_coordinates(0, service_hallway, 0, 0)
outside_time.set_coordinates(service_hallway, 0, 0, 0)

common_room.set_coordinates([tv_room, staff_breakroom, med_station], [blue_hallway, ward_stairs], [library, bathroom_cr], service_hallway) ###
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




#Set interacts in rooms
common_room.set_storage_units([item.common_room_cabinets, item.common_room_table])

#Set items in storage units
common_room.storage_containers[0].set_items([item.flashlight])
item.common_room_cabinets.set_items([item.shotgun_shells])
item.common_room_table.set_items([item.power_room_key])


#Set monsters/npc's in rooms

def ward_set_door_dictionaries():
    admissions.create_door_dict([item.admissions_entrance, item.service_hallway_w, None, None])
    service_hallway.create_door_dict([None, item.service_hallway_e, item.outside_time_n, [None, item.service_hallway_w]])
    outside_time.create_door_dict([item.outside_time_n, None, None, None])
    common_room.create_door_dict([[None, None, None], [None, item.ward_to_basement_door], [None, None], item.service_hallway_e]) ###
    

######################    
### Basement Rooms ###
######################    

# Rooms (name, description)
basement_stairs = room_class.Basement_Room("Stairs Level B", "")
basement_landing = room_class.Basement_Room("Basement Landing", "")
old_nurses_station = room_class.Basement_Room("Old Nursing Station", "")
old_med_window = room_class.Basement_Room("Old Med Window", "")
old_medical_storage = room_class.Basement_Room("Old Medical Storage", "")

sedation_room = room_class.Basement_Room("Sedation Room", "")
residential_hallway = room_class.Basement_Room("Residential Hallway", "")
old_residential_bedroom = room_class.Basement_Room("Old Residential Bedroom", "")

maze_int1 = room_class.Maze_Room("A Dark Intersection", "")
maze_south_end1 = room_class.Maze_Room("A Dead End", "")
maze_north_end1 = room_class.Maze_Room("A Dead End", "")
maze_int2 = room_class.Maze_Room("A Dark Intersection", "")
maze_int3 = room_class.Maze_Room("A Dark Intersection", "")
maze_west_end1 = room_class.Maze_Room("A Dead End", "")
maze_int4 = room_class.Maze_Room("A Dark Intersection", "")
maze_east_end1 = room_class.Maze_Room("A Dead End", "")
maze_int5 = room_class.Maze_Room("A Dark Intersection", "")
maze_north_end2 = room_class.Maze_Room("A Dead End", "")
maze_int6 = room_class.Maze_Room("A Dark Intersection", "")
maze_east_end2 = room_class.Maze_Room("A Dead End", "")

power_room = room_class.Basement_Room("", "")

waiting_room = room_class.Basement_Room("", "")
old_therapy_room = room_class.Basement_Room("", "")
clinical_hallway = room_class.Basement_Room("", "")
straightjacket_storage = room_class.Basement_Room("", "")
tanning_bed_cell = room_class.Basement_Room("", "")

high_security_area = room_class.Basement_Room("", "")
plexiglass_cell = room_class.Basement_Room("", "")
shock_therapy_room = room_class.Basement_Room("", "")

####
basement_landing.set_coordinates(residential_hallway, basement_stairs, waiting_room, [old_nurses_station, old_med_window])
old_nurses_station.set_coordinates(old_med_window, basement_landing, 0, old_medical_storage)
old_med_window.set_coordinates(0, basement_landing, old_nurses_station, 0)
old_medical_storage.set_coordinates(0, old_nurses_station, 0, 0)

residential_hallway.set_coordinates(old_residential_bedroom, sedation_room, basement_landing, maze_int1)
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

waiting_room.set_coordinates(basement_landing, 0, old_therapy_room, clinical_hallway)
clinical_hallway.set_coordinates(0, waiting_room, [straightjacket_storage, tanning_bed_cell], high_security_area)
old_therapy_room.set_coordinates(waiting_room, 0, 0, 0)
straightjacket_storage.set_coordinates(clinical_hallway, 0, 0, 0)
tanning_bed_cell.set_coordinates(clinical_hallway, 0, 0, 0)

high_security_area.set_coordinates(shock_therapy_room, clinical_hallway, 0, plexiglass_cell)
plexiglass_cell.set_coordinates(0, high_security_area, 0, 0)
shock_therapy_room.set_coordinates(0, 0, high_security_area, 0)



#Set items in rooms
# revolver, power_room_key
# shotgun_shells, crowbar, keycard
# utility_belt, bandages
# bandages, antidote
# antidote
# compass
# bandages

#Set interacts in rooms
power_room.set_interacts([item.power_box])

#Set monsters npc's in rooms


#create door dictionaries
def basement_set_door_dictionaries():
    power_room.create_door_dict([None, None, item.power_s_door, None])