
import re
import the_no_shoelace_place.classes.item_class as item_class

class Parser:
    def __init__(self) -> None:

        self.player = None
        
        pick_up_keys = {'pick up':["pick up", "take", "retrieve", "get", "grab", "remove"]}
        drop_keys = {'drop':["drop", "place", "put down", "put", "insert", "set"]}
        inspect_keys = {'inspect':["inspect", "look at", "examine", "read", "check out", "search"]}
        open_keys = {'open':["open"]}
        unlock_keys = {'unlock':['unlock', 'unseal']}
        close_keys = {'close':["close", "shut"]}
        lock_keys = {'lock':["lock", "seal"]}
        interact_keys = {'interact':["interact", "pull", "push"]}
        break_keys = {'break':["break", "smash", "tear down", "rip off", "damage"]}
        move_keys = {'go':["go", "move", "walk", "turn"]}
        display_keys = {'display':["display", "view", "show", "reveal"]}

        self.movement_dict = {
            "forward" : ["forward", "forwards", "straight", "front "],
            "backward" : ["backward", "backwards", "back", "behind"],
            "left" : ["left"],
            "right" : ["right"]}

        self.all_actions = [pick_up_keys, drop_keys, inspect_keys, open_keys, unlock_keys,
            close_keys, lock_keys, interact_keys, break_keys, move_keys, display_keys]
        
    def parse_input(self, player, str_input):
        self.update_player(player)

        if self.check_for_bans(str_input):
            return False

        return self.id_action_object(player, str_input)

    def update_player(self, player):
        self.player = player

    def check_for_bans(self, str):
        # when ready switch print to printtk
        if ' and ' in str:
            gui_parser.printtk("Please enter a single action at a time, avoiding using conjuntions.")
            return True
        elif ' or ' in str:
            gui_parser.printtk("Please enter specific commands, avoiding using conjuntions.")
        
        return False
                
    def id_action_object(self, player, str_input):
        str_input = " " + str_input 

        # Loop over actions and store matches in action_list
        actions_list = []
        for action in self.all_actions:
            for key, val in action.items():
                for phrase in val:
                    if re.search(r'\b' + phrase + r'\b', str_input.lower()):
                        actions_list.append(key)

        if len(actions_list) > 1:
            gui_parser.printtk("Please enter a single verb at a time.")
            return False
        else:
            if len(actions_list) == 1:
                parsed_action = actions_list[0]
            else:
                parsed_action = None

        # Loop over items and store matches in a list
        room_possible_items = {}
        for sc in player.loc.storage_containers:
            room_possible_items[sc] = sc.items

        obj_loc_tuples = []
        for loc, items_list in room_possible_items.items():
            for item in items_list:
                if item.name.lower() in str_input.lower():
                    obj_loc_tuples.append((item, loc))

        # Loop over inv items too
        for item in player.inv:
            if item.name.lower() in str_input.lower():
                obj_loc_tuples.append((item, player.inv))

        if len(obj_loc_tuples) > 1:
            gui_parser.printtk("Please include only one object at a time.")
            return False
        else:
            if len(obj_loc_tuples) == 1:
                parsed_obj_loc = obj_loc_tuples[0]
            else:
                parsed_obj_loc = None

        # Loop over storage locations
        item_storage_locations = {} 
        if parsed_action == 'drop':
            item_storage_locations['drop'] = []
            for sc in player.loc.storage_containers:
                if sc.name.lower() in str_input.lower():
                    item_storage_locations['drop'].append(sc)

        if len(item_storage_locations.keys()) == 0:
            item_storage_locations = None
        
        # Loop over doors and openable storage units
        doors = []
        for door_or_list in player.loc.doors.values():
            if isinstance(door_or_list, list):
                for door in door_or_list:
                    if door != None:
                        doors.append(door)
            else:
                if door_or_list != None:
                    doors.append(door_or_list)

        openable_items = {}
        for verb in ("open", "unlock", "close", "lock"):
            if parsed_action == verb:
                openable_items[verb] = []
                for sc in player.loc.storage_containers:
                    if sc.name.lower() in str_input.lower() and isinstance(sc, item_class.Storage_Box):
                        openable_items[verb].append(sc)
                for door in doors:
                    if door.name.lower() in str_input.lower():
                        openable_items[verb].append(door)

        if len(openable_items.keys()) == 0:
            openable_items = None

        
        direction_tuple = None
        for key, val in self.movement_dict.items():
            for direction in val:
                if direction in str_input.lower():
                    if parsed_action == "go":
                        direction_tuple = ("go", key)
                    else:
                        direction_tuple = (None, key)


        display_option_tuple = None
        if parsed_action == "display":
            for display_opt in ("items", "directions"):
                if display_opt in str_input.lower():
                    display_option_tuple = (parsed_action, display_opt)
        else:
            for display_opt in ("items", "directions"):
                if display_opt in str_input.lower():
                    display_option_tuple = (None, display_opt)
        
        # Return values
        return_tuple = (parsed_action, parsed_obj_loc, 
            item_storage_locations, openable_items, 
            direction_tuple, display_option_tuple)
        return return_tuple


# General Function
def organize_parsed_data(parsed_tuple, player): 
    dest, helper = None, None
    
    #   actions_list (verbs), 
    action = parsed_tuple[0]
    #   obj_loc_tuples (objects and their current locations), 
    object_loc_tuple = parsed_tuple[1]
    #   item_storage_locations (places to store objects if necessary verbs were parsed), 
    storage_locations = parsed_tuple[2]
    #   openable_items (objects that can be opened/closed, locked/unlocked if verbs were parsed)
    openable_items = parsed_tuple[3]
    #   movement direction (if a movement verb is parsed)
    direction_tuple = parsed_tuple[4]
    #   option for displaying (like items or directions)
    display_option_tuple = parsed_tuple[5]


    # If there is no verb and one object - inspect object
    if action == None and object_loc_tuple != None:
        if isinstance(object_loc_tuple[0], item_class.Inv_Item):
            dest, helper = object_loc_tuple[0].inspect_item()
        elif isinstance(object_loc_tuple[0], item_class.Storage_Unit):
            #print contents of storage spot
            pass
        else:
            gui_parser.printtk("This is an item.")

    
    elif direction_tuple != None:
        # Move a certain direction
        if direction_tuple[0] == "go":
            i = ["backward", "left", "right", "forward"].index(direction_tuple[1])
            direction_choice = ["b", "l", "r", "f"][i]
            blrf_dict = player.check_blrf_directions()

            next_rooms = [player.loc.north, player.loc.east, player.loc.south, player.loc.west]
            i = ['n', 'e', 's', 'w'].index(blrf_dict[direction_choice])
            dest, helper = player.move_nesw(blrf_dict[direction_choice], next_rooms[i])
        # Printing adjacent rooms for a certain direction
        # direction_tuple[0] == None
        else:
            gui_parser.printtk("Print adjacent rooms in a direction")


    elif display_option_tuple != None:
        if display_option_tuple[1] == 'items':
            player.loc.print_items_loc_desc()

        elif display_option_tuple[1] == 'directions':
            player.loc.print_all_directions(player, None)

    # If there is one action and one object
    elif action != None and object_loc_tuple != None:
        
        if action == "pick up":
            if object_loc_tuple[0].pick_up_bool:
                if isinstance(object_loc_tuple[1], item_class.Storage_Unit):
                    dest, helper = player.pick_up_item(object_loc_tuple[0])
                elif isinstance(object_loc_tuple[1], list):
                    gui_parser.printtk("This item is already in your inventory.")
            else:
                gui_parser.printtk("You cannot pick up this item.")

        elif action == "drop":
            if object_loc_tuple[0] in player.inv:
                if storage_locations == None or 'drop' not in storage_locations.keys():
                    dest, helper = player.drop_item(object_loc_tuple[0], None) 
                    gui_parser.printtk(f"You have dropped the {object_loc_tuple[0].name} on the ground.")
                else:
                    if 'drop' in storage_locations.keys():
                        dest, helper = player.drop_item(object_loc_tuple[0], storage_locations['drop'][0])
                        gui_parser.printtk(f"You have dropped the {object_loc_tuple[0].name} to the {storage_locations['drop'][0].name}.")
    
            else:
                gui_parser.printtk("You cannot drop this item beacuse you are not holding it.")

        elif action == "inspect":
            if object_loc_tuple[0].inspect_bool:
                pass
            else:
                gui_parser.printtk("You cannot inspect this item.")

        elif action == "open":
            if object_loc_tuple[0].openable_bool:
                pass
            else:
                gui_parser.printtk("You cannot open this item")

        elif action == "unlock":
            if object_loc_tuple[0].lockable_bool:
                pass
            else:
                gui_parser.printtk("You cannot unlock this item")

        elif action == "lock":
            if object_loc_tuple[0].lockable_bool:
                pass
            else:
                gui_parser.printtk("You cannot lock this item")

        elif action == "interact":
            if object_loc_tuple[0].interact_bool:
                pass
            else:
                gui_parser.printtk("You cannot interact with this item")

        elif action == "break":
            if object_loc_tuple[0].breakable:
                pass
            else:
                gui_parser.printtk("You cannot break this item")
    
    
    return dest, helper
    


def set_parser_gui(gui_window):
    global gui_parser
    gui_parser = gui_window

