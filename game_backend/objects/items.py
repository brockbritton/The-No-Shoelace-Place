
import game_backend.classes.item_class as item_class

# Ward Items
# name, desc, hidden_atr

id_bracelet = item_class.ID_Bracelet("id bracelet", "bracelet", "", None)

basement_key = item_class.Key("basement door key", "key", "", None)
cabinet_key = item_class.Key("ward keys", "key", "", None)
ward_doors_key = item_class.Key("ward security key", "key", "", None)

# Ward Doors
admissions_entrance = item_class.Keyable_Door("Admissions Exit Door", "door", None) 
service_hallway_w = item_class.Keyable_Door("Service Hallway W Door", "door", [ward_doors_key])
service_hallway_e = item_class.Keyable_Door("Service Hallway E Door", "door", [ward_doors_key])
outside_time_n = item_class.Keyable_Door("Outside Recreation Door", "door", [ward_doors_key])
ward_to_basement_door = item_class.Keyable_Door("Basement Door", "door", [basement_key])

# Ward Storage Containers
common_room_table = item_class.Storage_Spot("common room table", "table")
common_room_cabinets = item_class.Storage_Box("common room cabinet", "cabinet", True, [cabinet_key, ward_doors_key])
# Cabinets
# Drawers

#### Basement Items ####

power_room_key = item_class.Key("power room key", "key", "", None)
keycard = item_class.Keycard("basement keycard", "key", "", None)
crowbar = item_class.Crowbar("crowbar", "crowbar", "", None)

flashlight = item_class.Flashlight("flashlight", "flashlight", "", None)


utility_belt = item_class.Utility_Belt("utility belt", "belt", "", None) 
shotgun_shells = item_class.Shotgun_Shells("shotgun shells", "ammo", "", None) #currently useless

#### Basement Interacts ####

power_box = item_class.Power_Box("fuse box", "fuse box")

# Basement Doors
power_s_door = item_class.Door("Power Room Door", "door", [power_room_key])
high_security_door = item_class.Electronic_Door("High Security Door", "door", "2116", [keycard])

# Storage Containers
# Cabinets
# Drawers