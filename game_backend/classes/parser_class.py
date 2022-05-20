
import re


class Parser:
    def __init__(self) -> None:
        self.player = None
        pick_up_keys = {'pick up':["pick up", "take", "retrieve", "get", "grab", "remove"]}
        drop_keys = {'drop':["drop", "place", "put down", "put", "insert", "set"]}
        inspect_keys = {'inspect':["inspect", "look at", "examine", "read", "check out", "search"]}
        open_keys = {'open':["open"]}
        close_keys = {'close':["close", "shut"]}
        unlock_keys = {'unlock':['unlock', 'unseal']}
        lock_keys = {'lock':["lock", "seal"]}
        break_keys = {'break':["break", "smash", "tear down", "rip off", "damage", "destroy"]}
        move_keys = {'go':["go", "move", "walk", "turn"]}
        display_keys = {'display':["display", "view", "show", "reveal"]}

        self.movement_dict = {
            "forward" : ["forward", "forwards", "straight", "front "],
            "backward" : ["backward", "backwards", "back", "behind"],
            "left" : ["left"],
            "right" : ["right"]}

        self.all_actions = [pick_up_keys, drop_keys, inspect_keys, open_keys, unlock_keys,
            close_keys, lock_keys, break_keys, move_keys, display_keys]
        
    def parse_input(self, player, str_input):
        self.update_player(player)
        return self.id_action_object(player, str_input)

    def update_player(self, player):
        self.player = player
                
    def id_action_object(self, player, str_input):
        
        str_input = " " + str_input 
        parsed_info = {
            "action" : [],
            "nearby_objects" : [],
            "directions" : [],
            "special_actions" : []
        }

        # Loop over actions and store matches in action_list
        for action in self.all_actions:
            for key, val in action.items():
                for phrase in val:
                    if re.search(r'\b' + phrase + r'\b', str_input.lower()):
                        parsed_info["action"].append(key)

        # Build a dictionary of all items in the room and inventory and the room itself
        ## Items in storage units in the room
        for sc in player.loc.storage_containers:
            if sc.name.lower() in str_input.lower():
                parsed_info["nearby_objects"].append(sc)
            for item in sc.items:
                if item.name.lower() in str_input.lower():
                    parsed_info["nearby_objects"].append(item)
        ## Items in inventory
        for item in player.inv:
            if item.name.lower() in str_input.lower():
                parsed_info["nearby_objects"].append(item)
        ## The room itself
        if player.loc.name.lower() in str_input.lower() or "room" in str_input.lower():
            parsed_info["nearby_objects"].append(player.loc)

        ## Doors adjacent to the room
        #### It is not good to have the door name since thats not yet visibly available to the player
        for door_or_doors in player.loc.doors.values():
            if isinstance(door_or_doors, list):
                for door in door_or_doors:
                    if door != None and door.name.lower() in str_input.lower():
                        parsed_info["nearby_objects"].append(door)
            else:
                if door != None and door.name.lower() in str_input.lower():
                    parsed_info["nearby_objects"].append(door)

        # Loop over directions both for movement and displays
        for key, val in self.movement_dict.items():
            for direction in val:
                if direction in str_input.lower():
                    parsed_info["directions"].append(key)
        for direction in ("south", "north", "east", "west"):
            if direction in str_input.lower():
                parsed_info["directions"].append("cardinal")

        # Check for special actions
        # xi : items in room
        # xd : directions
        # xw : items on walls
        for special in ("xi", "xd", "xw"):
            if special in str_input.lower():
                parsed_info["special_actions"].append(special)
        
        # Return values
        return parsed_info


