
import re

class Parser:
    def __init__(self) -> None:
        self.player = None

        self.all_actions = {
            'pick up' : ["pick up", "pickup", "take", "retrieve", "get", "grab", "remove"],
            'drop' : ["drop", "place", "put down", "put", "set", "move"],
            'inspect' : ["inspect", "look at", "examine", "read", "check out", "search"],
            'open' : ["open"],
            'close' : ["close", "shut"],
            'unlock' : ['unlock', 'unseal'],
            'lock' : ["lock", "seal"],
            'break':["break", "smash", "tear down", "rip off", "damage", "destroy"],
            'go':["go", "walk", "turn", "enter", "travel", "exit", "leave"],
            'display':["display", "view", "show", "reveal"],
            'help':["help", "?"]
        }
        
        self.movement_dict = {
            "forward" : ["forward", "forwards", "straight", "front"],
            "backward" : ["backward", "backwards", "back", "behind"],
            "left" : ["left"],
            "right" : ["right"]}

        self.special_actions = ["sleep", "sit", "rooms", "items"]


        
    def parse_input(self, player, str_input):
        return self.id_action_object(player, str_input)

    def update_gen_dict(self, dict, item):
        try:
            dict[item.gen_name].append(item)
        except KeyError:
            dict[item.gen_name] = [item]

        return dict

                
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
            for phrase in val:
                # use regex here?
                if phrase in str_input.lower():
                    parsed_info["action"].append(key)

        # Loop over item specific actions and store matches in action_list
        for action in self.special_actions:
            if re.search(r'\b' + action + r'\b', str_input.lower()):
                parsed_info["action"].append(action)

        # Build a dictionary of all items in the room and inventory and the room itself
        ## Items in storage units in the room
        for sc in player.loc.storage_containers:
            if sc.name.lower() in str_input.lower():
                parsed_info["nearby_objects"].append(sc)
            
            if sc.gen_name.lower() in str_input.lower():
                parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], sc)
            
            contents = sc.build_flat_list_of_contents(False)
            for item in contents:
                if item.name.lower() in str_input.lower():
                    parsed_info["nearby_objects"].append(item)
                
                if item.gen_name.lower() in str_input.lower():
                    parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], item)
                
        ## Items in inventory
        for item in player.inv:
            if item.name.lower() in str_input.lower():
                parsed_info["nearby_objects"].append(item)

            if item.gen_name.lower() in str_input.lower():
                parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], item)
                

        ## The room itself
        if player.loc.name.lower() in str_input.lower() or "room" in str_input.lower():
            parsed_info["nearby_objects"].append(player.loc)

        ## Doors adjacent to the room
        door_gen_bool = False
        if "door" in str_input.lower():
            door_gen_bool = True

        for door_or_doors in player.loc.doors.values():
            if isinstance(door_or_doors, list):
                for door in door_or_doors:
                    if door != None and door.name.lower() in str_input.lower():
                        parsed_info["nearby_objects"].append(door)
                     
                    if door != None and door_gen_bool:
                        parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], door)
            else:
                if door_or_doors != None and door_or_doors.name.lower() in str_input.lower():
                    parsed_info["nearby_objects"].append(door_or_doors)
                if door_or_doors != None and door_gen_bool:
                        parsed_info["nearby_gen_dict"] = self.update_gen_dict(parsed_info["nearby_gen_dict"], door_or_doors)

        # Loop over directions both for movement and displays
        for key, val in self.movement_dict.items():
            for direction in val:
                if direction in str_input.lower():
                    parsed_info["directions"].append(key)
        for direction in ("south", "north", "east", "west"):
            if direction in str_input.lower():
                parsed_info["directions"].append("cardinal")
        for direction in (player.loc.north, player.loc.east, player.loc.south, player.loc.west):
            # Zero's indicate a wall - will not have a name attribute
            if not isinstance(direction, int):
                if isinstance(direction, list):
                    for room in direction:
                        if room.name.lower() in str_input.lower():
                            parsed_info["directions"].append(room)
                else:
                    if direction.name.lower() in str_input.lower():
                        parsed_info["directions"].append(direction)

        # Check for special actions
        # xi : items in room
        # xd : directions
        for cheat in ("xi", "xd", "cheatcode:Asher"):
            if cheat in str_input.lower():
                parsed_info["cheats"].append(cheat)
        
        # Return values
        return parsed_info


