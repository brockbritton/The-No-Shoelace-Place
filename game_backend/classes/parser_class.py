
import re

import game_backend.classes.item_class as item_class
import game_backend.gl_backend_functions as gl


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
        display_keys = {'display':["display", "view", "show", "reveal", "look at"]}

        self.movement_dict = {
            "forward" : ["forward", "forwards", "straight", "front "],
            "backward" : ["backward", "backwards", "back", "behind"],
            "left" : ["left"],
            "right" : ["right"]}

        self.all_actions = [pick_up_keys, drop_keys, inspect_keys, open_keys, unlock_keys,
            close_keys, lock_keys, interact_keys, break_keys, move_keys, display_keys]
        
    def parse_input(self, player, str_input):
        self.update_player(player)

        print_list = self.check_for_bans(str_input)
        if len(print_list) != 0:
            return False, print_list
        else:
            tuples, print_list = self.id_action_object(player, str_input, print_list)
            return tuples, print_list

    def update_player(self, player):
        self.player = player

    def check_for_bans(self, str):
        to_print = []
        if ' and ' in str:
            to_print.append("Please enter a single action at a time, avoiding using conjuntions.")
        elif ' or ' in str:
            to_print.append("Please enter specific commands, avoiding using conjuntions.")
        return to_print
                
    def id_action_object(self, player, str_input, to_print):
        
        str_input = " " + str_input 
        # Loop over actions and store matches in action_list
        actions_list = []
        for action in self.all_actions:
            for key, val in action.items():
                for phrase in val:
                    if re.search(r'\b' + phrase + r'\b', str_input.lower()):
                        actions_list.append(key)

        if len(actions_list) > 1:
            to_print.append("Please enter a single verb at a time.")
            return False, to_print
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

        print(obj_loc_tuples)
        if len(obj_loc_tuples) > 1:
            to_print.append("Please include only one object at a time.")
            return False, to_print
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
        return return_tuple, to_print


