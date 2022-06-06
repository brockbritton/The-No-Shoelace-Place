
import tnslp.game_backend.classes.item_class as item_class

# Room Name #
    # Items - declare variables
    # Storage Units
        # Storage Unit 1.set_items(items)
        # Storage Unit 2.set_items(items)
    # Doors
   

# Ward Item

id_bracelet = item_class.ID_Bracelet("id bracelet", "bracelet") 

basement_key = item_class.Key("basement key", "key")
cabinet_key = item_class.Key("ward cabinet keys", "key")
ward_doors_key = item_class.Key("ward security key", "key")




##### Ward Rooms and Items #####
# Common Room #
    # Storage Units
cr_art_table = item_class.Storage_Spot("arts and crafts table", "table")
cr_game_cabinets = item_class.Storage_LockBox("game cabinet", "cabinet", True, [cabinet_key, ward_doors_key])
deck_of_cards = item_class.Deck_of_Cards("deck of cards", "box")
cr_ping_pong_table = item_class.Storage_Spot("ping pong table", "table")
cr_ping_pong_table.set_items([deck_of_cards])
    # Doors
ward_to_basement_door = item_class.Lockable_Door("Basement Door", "door", [basement_key])

# Library #
    # Storage Units
lib_nf_bookshelf = item_class.Storage_Spot("non-fiction bookshelf", "shelf")
lib_fant_bookshelf = item_class.Storage_Spot("fantasy bookshelf", "shelf")
lib_classic_bookshelf = item_class.Storage_Spot("classics bookshelf", "shelf")
lib_help_bookshelf = item_class.Storage_Spot("self-help bookshelf", "shelf")

# TV Room #
    # Storage Units
tv_coffee_table = item_class.Storage_Spot("coffee table", "table")

# Med Window #
    # Storage Units
mw_trash_bin = item_class.Storage_Bin("trash bin", "bin")
mw_recycle_bin = item_class.Storage_Bin("recycle bin", "bin")

# Servery #
    # Storage Units
serv_counter = item_class.Storage_Spot("servery counter", "counter")
serv_tableware_bin = item_class.Storage_Box("tableware box", "box")

# Linen Room #
    # Storage Units
lr_towels_shelf = item_class.Storage_Spot("scrubs shelf", "shelf")
lr_bedding_shelf = item_class.Storage_Spot("bedding shelf", "shelf")

# Service Hallway #
    # Storage Units
    # Doors
service_hallway_w = item_class.Lockable_Door("Service Hallway W Door", "door", [ward_doors_key])
service_hallway_e = item_class.Lockable_Door("Service Hallway E Door", "door", [ward_doors_key])

# Utility Closet #
    # Storage Units
uc_cleaning_shelf = item_class.Storage_Spot("cleaning supplies shelf", "shelf")
uc_hygiene_shelf = item_class.Storage_Spot("hygiene supplies shelf", "shelf")

# Patient Courtyard #
    # Storage Units
park_bench = item_class.Storage_Spot("park bench", "table")
toys_bag = item_class.Storage_Bin("toys bin", "bin")
    # Doors
outside_time_n = item_class.Lockable_Door("Outside Recreation Door", "door", [ward_doors_key])

# Admissions Office #
    # Storage Units
admissions_entrance = item_class.Lockable_Door("Admissions Exit Door", "door", None) 



#### Basement Items ####

power_room_key = item_class.Key("power room key", "key")
keycard = item_class.Keycard("basement keycard", "key")
crowbar = item_class.Crowbar("crowbar", "crowbar")

flashlight = item_class.Flashlight("flashlight", "flashlight")

#### Basement Interacts ####

power_box = item_class.Power_Box("fuse box", "fuse box")

# Basement Doors
power_room_door = item_class.Lockable_Door("Power Room Door", "door", [power_room_key])
high_security_door = item_class.Lockable_Door("High Security Door", "door", [keycard, "2525"])

# Storage Containers
# Cabinets
# Drawers