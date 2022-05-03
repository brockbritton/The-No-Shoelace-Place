
import game_backend.classes.item_class as item_class

# Ward Items
# name, desc, hidden_atr

id_bracelet = item_class.ID_Bracelet("id bracelet", "bracelet", "")

basement_key = item_class.Key("basement door key", "key", "")
cabinet_key = item_class.Key("ward keys", "key", "")
ward_doors_key = item_class.Key("ward security key", "key", "")

##### Ward Doors
admissions_entrance = item_class.Keyable_Door("Admissions Exit Door", "door", None) 
service_hallway_w = item_class.Keyable_Door("Service Hallway W Door", "door", [ward_doors_key])
service_hallway_e = item_class.Keyable_Door("Service Hallway E Door", "door", [ward_doors_key])
outside_time_n = item_class.Keyable_Door("Outside Recreation Door", "door", [ward_doors_key])
ward_to_basement_door = item_class.Keyable_Door("Basement Door", "door", [basement_key])

##### Ward Storage Containers
# Common Room
cr_art_table = item_class.Storage_Spot("arts and crafts table", "table")
cr_game_cabinets = item_class.Storage_Box("game cabinet", "cabinet", True, [cabinet_key, ward_doors_key])
cr_ping_pong_table = item_class.Storage_Spot("ping pong table", "table")

# Library
lib_nf_bookshelf = item_class.Storage_Spot("non-fiction bookshelf", "shelf")
lib_fant_bookshelf = item_class.Storage_Spot("fantasy bookshelf", "shelf")
lib_classic_bookshelf = item_class.Storage_Spot("classics bookshelf", "shelf")
lib_help_bookshelf = item_class.Storage_Spot("self-help bookshelf", "shelf")

# TV Room
tv_coffee_table = item_class.Storage_Spot("coffee table", "table")

# Med Window
mw_trash_bin = item_class.Storage_Box("trash can", "trash can", False, [])
mw_recycle_bin = item_class.Storage_Box("recycle bin", "recycle bin", False, [])

# Servery
serv_counter = item_class.Storage_Spot("servery counter", "counter")
serv_tableware_bin = item_class.Storage_Box("tableware box", "box", False, [])

# Linen Room
lr_towels_shelf = item_class.Storage_Spot("scrubs shelf", "shelf")
lr_bedding_shelf = item_class.Storage_Spot("bedding shelf", "shelf")

# Utility Closet
uc_cleaning_shelf = item_class.Storage_Spot("cleaning supplies shelf", "shelf")
uc_hygiene_shelf = item_class.Storage_Spot("hygiene supplies shelf", "shelf")

# Patient Courtyard
park_bench = item_class.Storage_Spot("park bench", "table")
toys_bag = item_class.Storage_Box("toys box", "box ", False, [])


#### Basement Items ####

power_room_key = item_class.Key("power room key", "key", "")
keycard = item_class.Keycard("basement keycard", "key", "")
crowbar = item_class.Crowbar("crowbar", "crowbar", "")

flashlight = item_class.Flashlight("flashlight", "flashlight", "")

#### Basement Interacts ####

power_box = item_class.Power_Box("fuse box", "fuse box")

# Basement Doors
power_room_door = item_class.Door("Power Room Door", "door", [power_room_key])
high_security_door = item_class.Electronic_Door("High Security Door", "door", "2116", [keycard])

# Storage Containers
# Cabinets
# Drawers