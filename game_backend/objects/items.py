
import game_backend.classes.item_class as item_class

# Room Name #
    # Items - declare variables
    # Storage Units
        # Storage Unit 1.set_items(items)
        # Storage Unit 2.set_items(items)
    # Doors

#More Items:
# power_room_key
# crowbar, keycard
# antidote
# compass
# bandages

### Character Starting Items ###
id_bracelet = item_class.ID_Bracelet("id bracelet", "bracelet") 

### All Keys ###
master_key = item_class.Key("master key", "key")
security_key = item_class.Key("security key", "key")
ward_doors_key = item_class.Key("ward doors key", "key")
patient_key = item_class.Key("patient key", "key")
rec_key = item_class.Key("rec key", "key")

### All Posters ###
friends_poster = item_class.Hanging_Quote_Note("friends poster", 
    "poster", 
    ["\"Why did you do all this for me?\"",
        "he asked. \"I don't deserve it.\"",
        "\"I've never done anything for you.\"",
        "\"You have been my friend\", replied Charlotte.",
        "\"That in itself is a tremendous thing.\""],
    "E.B. White, Charlotte's Web")

stories_poster = item_class.Hanging_Quote_Note("stories poster",
    "poster",
    ["\"Do you have a magic spell to return someone to life?\" she said.",
        "\"No,\" the witch said, \"I'm sorry.\"",
        "\"Oh.\"",
        "\"Why don't you tell me about them?\"",
        "\"Will that bring them back?\"",
        "\"For us. For a little while. Stories are a different kind of magic.\""],
    "James Miller, A Small Fiction")

doors_poster = item_class.Hanging_Quote_Note("doors poster",
    "poster",
    ["In the universe,",
    "there are things that are known,", 
    "and things that are unknown,", 
    "and in between,",
    "there are doors."],
    "William Blake")

frienship_poster = item_class.Hanging_Quote_Note("friendship poster",
    "poster",
    ["There are good ships,",
    "and there are wood ships,",
    "and ships that sail the sea.",
    "But the best ships are frienships,",
    "and may they always be."],
    "Old Maritime Blessing")

monsters_poster = item_class.Hanging_Quote_Note("monsters poster",
    "poster",
    ["Whoever fights monsters should see to it that in the process he does not become a monster.",
    "And if you gaze long enough into an abyss, the abyss will gaze back into you."],
    "Friedrich Nietzsche")

oxygen_poster = item_class.Hanging_Quote_Note("oxygen poster",
    "poster",
    ["Freedom is the oxygen of the soul."],
    "Moshe Dayan")

alone_poster = item_class.Hanging_Quote_Note("alone poster",
    "poster",
    ["It's beautiful to be alone,",
    "To be alone does not mean to be lonely.", 
    "It means the mind is not influenced and comtaminated by society."],
    "Jiddu Krishnamurti")

hope_poster = item_class.Hanging_Quote_Note("hope poster",
    "poster",
    ["Once you choose hope, anything's possible."],
    "Christopher Reeve")

faucets_poster = item_class.Hanging_Quote_Note("faucets poster",
    "poster",
    ["Feelings",
    "are not like faucets", 
    "you can turn on and off."],
    "Richard Lessor")

## All Riddle Containers ##
friendship_note = item_class.Quote_Note(
    "chess note", 
    "note", 
    ["No one ever won a game by resigning."],
    "Savielly Tartakower"),
friendship_riddle = item_class.Riddle_Box(
    "Riddle 1", 
    "Riddle", 
    [friendship_note], 
    ["In adventures and journeys, we make our way,",
    "Side by side, we seize each day.",
    "A loyal partner through thick and thin,",
    "Together we conquer, never giving in.",
    "A steadfast companion, a source of elation.",
    "What am I, this trusted relation?"],
    ["friend", "friends", "friendship"]
)

################################
##### Ward Rooms and Items #####
################################

# Common Room #
deck_of_cards = item_class.Deck_of_Cards("deck of cards", "box")
chess_set = item_class.Chess_Set("chess set", "box")
    # Storage Units
cr_art_table = item_class.Storage_Spot("arts and crafts table", "table", [security_key])
cr_game_cabinets = item_class.Storage_Box("game cabinet", "cabinet", [chess_set, deck_of_cards])
cr_ping_pong_table = item_class.Storage_Spot("ping pong table", "table", None)
    # Doors
common_room_and_ward_landing_door = item_class.Ward_Lockable_Door("Door W1-B", "door", None)
common_room_and_staff_breakroom = item_class.Ward_Lockable_Door("Door W4", "door", None)
common_room_and_medications = item_class.Ward_Lockable_Door("Door W6", "door", None)

# Library #
    # Storage Units
lib_nf_bookshelf = item_class.Storage_Spot("non-fiction bookshelf", "shelf", None)
lib_fant_bookshelf = item_class.Storage_Spot("fantasy bookshelf", "shelf", None)
lib_classic_bookshelf = item_class.Storage_Spot("classics bookshelf", "shelf", None)
lib_help_bookshelf = item_class.Storage_Spot("self-help bookshelf", "shelf", None)

# TV Room #
    # Storage Units
tv_coffee_table = item_class.Storage_Spot("coffee table", "table", None)

# Med Window #
    # Storage Units
mw_trash_bin = item_class.Storage_Bin("trash bin", "bin", None)
mw_recycle_bin = item_class.Storage_Bin("recycle bin", "bin", None)

# Servery #
    # Storage Units
serv_counter = item_class.Storage_Spot("servery counter", "counter", None)
serv_tableware_bin = item_class.Storage_Box("tableware box", "box", None)

# Linen Room #
    # Storage Units
lr_towels_shelf = item_class.Storage_Spot("scrubs shelf", "shelf", None)
lr_bedding_shelf = item_class.Storage_Spot("bedding shelf", "shelf", None)

# Service Hallway #
    # Storage Units
    # Doors
service_hallway_and_common_room_door = item_class.Ward_Lockable_Door("Door S4", "door", None)

# Security Unit #
    # Storage Units
    # Doors
security_and_red_hallway_door = item_class.Ward_Lockable_Door("Door S6", "door", None)
security_and_service_hallway_door = item_class.Ward_Lockable_Door("Door S3", "door", None)

# Utility Closet #
    # Storage Units
uc_cleaning_shelf = item_class.Storage_Spot("cleaning supplies shelf", "shelf", None)
uc_hygiene_shelf = item_class.Storage_Spot("hygiene supplies shelf", "shelf", None)

# Patient Courtyard #
    # Storage Units
park_bench = item_class.Storage_Spot("park bench", "table", None)
toys_bag = item_class.Storage_Bin("toys bin", "bin", None)
    # Doors
courtyard_and_service_hallway_door = item_class.Ward_Lockable_Door("Door S9", "door", None)

# Admissions Office #
    # Storage Units
admissions_exit_door = item_class.Ward_Lockable_Door("Door M7", "door", None) 




##########################
##### Basement Items #####
##########################

power_room_key = item_class.Key("power room key", "key")
keycard = item_class.Keycard("basement keycard", "key")
crowbar = item_class.Crowbar("crowbar", "crowbar")

flashlight = item_class.Flashlight("flashlight", "flashlight")

#### Basement Interacts ####

power_box = item_class.Power_Box("fuse box", "fuse box")

# Basement Doors
power_room_door = item_class.Basement_Lockable_Door("Power Room Door", "door", [power_room_key])
high_security_door = item_class.Basement_Lockable_Door("Door J331", "door", [keycard, "2525"])
build_end_door = item_class.Basement_Lockable_Door("Build 1.0 End Door", "door", None)

# Storage Containers
# Cabinets
# Drawers