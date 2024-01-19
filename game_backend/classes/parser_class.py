
import re

class Parser:
    def __init__(self) -> None:
        self.player = None

        self.all_actions = {
            'pick up' : ["pick up", "pickup", "take", "retrieve", "get", "grab", "remove"],
            'drop' : ["drop", "place", "put down", "put", "move"], #set
            'inspect' : ["inspect", "look at", "examine", "check out", "search", "read"],
            'open' : ["open"],
            'close' : ["close", "shut"],
            'unlock' : ['unlock', 'unseal'],
            'lock' : ["lock", "seal"],
            'break':["break", "smash", "tear down", "destroy"],
            'go':["go", "walk", "enter", "travel", "exit", "leave"],
            'display':["display", "view", "show", "reveal"],
        }
        
        self.movement_dict = {
            "forward" : ["forward", "forwards", "straight", "front"],
            "backward" : ["backward", "backwards", "back", "behind"],
            "left" : ["left"],
            "right" : ["right"]}

        self.item_actions = ["help", "turn on", "turn off"] #"directions", "items", 


        
    def parse_input(self, player, str_input):
        return self.id_action_object(player, str_input)

    def update_gen_dict(self, dict, item):
        try:
            dict[item.gen_name].append(item)
        except KeyError:
            dict[item.gen_name] = [item] 

        return dict 

    def regex_search(self, search_word, full_string):
        return bool(re.search(r"\b" + re.escape(search_word) + r"\b", full_string))

                
    def id_action_object(self, player, str_input):
        
        str_input = " " + str_input 
        parsed_info = {
            "action" : [],
            "nearby_objects" : [],
            "nearby_gen_dict" : {},
            "directions" : [],
            "cheats" : [],
            "original_input" : str_input,
        }

        # Loop over actions and store matches in action_list
        
        for key, val in self.all_actions.items():
            for action in val:
                if self.regex_search(action, str_input.lower()):
                    parsed_info["action"].append(key)

        # Loop over item specific actions and store matches in action_list
        for action in self.item_actions:
            if self.regex_search(action, str_input.lower()):
                parsed_info["action"].append(action)


        # Build a dictionary of all items in the room and inventory and the room itself
        ## Items in the room
        room_flat_tree = player.loc.build_storage_flat_list(False)
        print(room_flat_tree)
        for item in room_flat_tree:
            if self.regex_search(item.name.lower(), str_input.lower()):
                parsed_info["nearby_objects"].append(item)
            
            if self.regex_search(item.gen_name.lower(), str_input.lower()):
                parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], item)
        
        ## Items in inventory
        for item in player.inv:
            if self.regex_search(item.name.lower(), str_input.lower()):
                parsed_info["nearby_objects"].append(item)

            if self.regex_search(item.gen_name.lower(), str_input.lower()):
                parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], item)
                

        ## The room itself
        if self.regex_search(player.loc.name.lower(), str_input.lower()) or self.regex_search("room", str_input.lower()):
            parsed_info["nearby_objects"].append(player.loc)

        for action in ["directions", "items"]:
            if self.regex_search(action, str_input.lower()):
                parsed_info["action"].append(action)

        ## Doors adjacent to the room
        door_gen_bool = False
        if self.regex_search("door", str_input.lower()):
            door_gen_bool = True

        for door_or_doors in player.loc.doors.values():
            if isinstance(door_or_doors, list):
                for door in door_or_doors:
                    if door != None and self.regex_search(door.name.lower(), str_input.lower()):
                        parsed_info["nearby_objects"].append(door)
                     
                    if door != None and door_gen_bool:
                        parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], door)
            else:
                if door_or_doors != None and self.regex_search(door_or_doors.name.lower(), str_input.lower()):
                    parsed_info["nearby_objects"].append(door_or_doors)
                if door_or_doors != None and door_gen_bool:
                        parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], door_or_doors)

        # Loop over directions both for movement and displays
        for key, val in self.movement_dict.items():
            for direction in val:
                if self.regex_search(direction, str_input.lower()):
                    parsed_info["directions"].append(key)
        for c_direction in ("south", "north", "east", "west"):
            if self.regex_search(c_direction, str_input.lower()):
                parsed_info["directions"].append("cardinal")
        for direction in (player.loc.north, player.loc.east, player.loc.south, player.loc.west):
            # Zero's indicate a wall - will not have a name attribute
            if not isinstance(direction, int):
                if isinstance(direction, list):
                    for room in direction:
                        if self.regex_search(room.name.lower(), str_input.lower()):
                            parsed_info["directions"].append(room)
                else:
                    if self.regex_search(direction.name.lower(), str_input.lower()):
                        parsed_info["directions"].append(direction)

        # Return values
        print(parsed_info)
        return parsed_info


