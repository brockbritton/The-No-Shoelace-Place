

import game_backend.classes.character_class as character_class
import game_backend.classes.item_class as item_class
import game_backend.classes.parser_class as parser_class
import game_backend.classes.room_class as room_class
import game_backend.objects.rooms as rooms
import game_backend.gl_backend_functions as gl
 

class Game:

    def __init__(self) -> None:
        self.master_dest = None
        self.master_helper = None
        self.wait_for_frontend_input = {'build_multiple_choice': None}
        self.save_prints = []
        self.player1 = character_class.Character("John Doe")
        self.parser = parser_class.Parser()
        self.starting_pars = len(self.start_game()['print_all'])
        
        #Map collections
        self.ward_rooms = room_class.Ward_Room._ward_rooms_registry
        self.ward_doors = item_class.Ward_Lockable_Door._doors_registry
        self.basement_rooms = room_class.Basement_Room._basement_rooms_registry
        self.basement_doors = item_class.Basement_Lockable_Door._doors_registry

    def __repr__(self) -> str:
        return f'Whole Game Object - player: {self.player1.name}'
    
    def get_curr_ui_value(self, id):
        # must be called each time because the values change
        ## these can be added to in action  {option}_value
        match id:
            case "xp-value": return self.player1.xp
            case "day-value": return self.player1.calendar.days_list[-1].day_number
            case "turns-value": return self.player1.calendar.days_list[-1].turns_left
            case "room-value": return self.player1.loc.display_name
            case "health-value": return self.player1.health
            case "diagnosis-value": return self.player1.diagnosis
            case "meditation-lvl": return self.player1.abilities[0].lvl
            case "assertiveness-lvl": return self.player1.abilities[1].lvl
            case "pos-attitude-lvl": return self.player1.abilities[2].lvl
            case "opp-action-lvl": return self.player1.abilities[3].lvl
            case "catharsis-lvl": return self.player1.abilities[4].lvl

    def get_player_inventory(self):
        return self.player1.build_inv_str_list()
    
    def get_player_attr(self):
        return [self.player1.xp, self.player1.calendar.days_list[-1].day_number, self.player1.calendar.days_list[-1].turns_left, self.player1.loc.display_name, self.player1.health, self.player1.diagnosis]

    def get_player_skills_lvl(self):
        return [self.player1.abilities[0].lvl, self.player1.abilities[1].lvl, self.player1.abilities[2].lvl, self.player1.abilities[3].lvl, self.player1.abilities[4].lvl]

    def get_player_exploration_values(self):
        return [[len(room_class.Room._visited_rooms), len(room_class.Ward_Room._ward_rooms_registry)], [len(item_class.Quote_Note._read_quotes), len(item_class.Quote_Note._all_quotes_registry)], [len(item_class.Riddle_Box._solved_riddles), len(item_class.Riddle_Box._all_riddles_registry)]]

    def get_item_action_params(self, action, object):
        # must be called each time because the values change
        match action:
            case "pick up": return [self.player1]
            case "drop": return [None, self.player1]
            case "unlock": return [self.player1]
            case "lock": return [self.player1]
            case "break": return [self.player1]
            case "inspect":
                if isinstance(object, room_class.Room):
                    return [self.player1]
                
            case "help": return []
            case "directions":
                if isinstance(object, room_class.Room):
                    return [self.player1]

            
        return []

    def start_game(self):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'rebuild_text_entry': False,
        }

        actions['print_all'].append("Welcome to The No-Shoelace Place!") 
        actions['print_all'].append("This new place, also known as the Ward, is small but there is a lot to find, so I suggest that you spend some time exploring.")
        actions['print_all'].append("For help playing, click the menu button in the top right.")
        
        return_tuple = self.player1.loc.enter_room(self.player1)
        self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)
        
        if len(self.save_prints) == 0:
            self.save_prints.extend(actions['print_all'])

        #print(self.player1.loc.storage_tree[0].items)

        return actions 
 
    def load_game(self):
        actions = {
            'load_prints': self.save_prints,
        }

        if self.wait_for_frontend_input['build_multiple_choice'] != None:
            actions['build_multiple_choice'] = self.wait_for_frontend_input['build_multiple_choice'][0]

        return actions 
    
    def organize_raw_input(self, frontend_input):
        actions = {
            'print_all': [],
            'build_multiple_choice': [], 
            'ask_y_or_n': False, 
            'rebuild_text_entry': False,
        }

        # Set a default return tuple if nothing connects
        return_tuple = (None, None, {})

        # If there is a list of variables in waiting vars and the input is numeric, 
        # convert to integer so that the correct variable from waiting vars is accessed
        if isinstance(frontend_input, int) and self.wait_for_frontend_input['build_multiple_choice'] != None:
            input_value = self.wait_for_frontend_input['build_multiple_choice'][1][int(frontend_input)]
            self.save_prints.append("> " + self.wait_for_frontend_input['build_multiple_choice'][0][int(frontend_input)]) 
            self.wait_for_frontend_input['build_multiple_choice'] = None
            # Match the destination to the input value
            # and execute the desired action
            print("matching destination: " + self.master_dest)
            return_tuple = (None, None, actions)
            match self.master_dest:
                case "full_inv_drop_items": 
                    return_tuple = self.player1.full_inv_drop_items(input_value, self.master_helper) 
                case "drop_x_for_y": 
                    return_tuple = self.player1.multi_choice_drop_x_for_y(input_value, self.master_helper) 
                case "move_nesw": 
                    return_tuple = self.player1.move_nesw(self.master_helper[0], self.master_helper[1][self.master_helper[1].index(input_value)])
                case "enter_code": 
                    return_tuple = self.master_helper[2].enter_code(input_value, self.master_helper)
                case "execute_event": 
                    return_tuple = self.master_helper.execute_event(input_value, self.player1)
                    if isinstance(return_tuple[1], int):
                        # Use n-1 turns because below another turn will be used
                        actions = gl.combine_dicts(actions, self.player1.calendar.use_turns(return_tuple[1] - 1, self.player1))
                case "level_up_ability": 
                    for ability in self.player1.abilities:
                        if ability.name == self.master_helper[0].name:
                            index = self.player1.abilities.index(ability)
                    return_tuple = self.player1.abilities[index].upgrade_ability(input_value, self.master_helper[1:], self.player1)
                case "gen_name_request":
                    if input_value != "c":
                        self.master_helper[0]["nearby_objects"].append(input_value)
                        return_tuple = self.evaluate_parsed_data(self.master_helper[0])
                    else:  
                        actions["print_all"].append(f"You did not choose a {self.master_helper[1]} to specify.")
                        return_tuple = (None, None, actions)
                case "ask_solve_riddle":
                    if input_value == "y":
                        actions["print_all"].append("Please type your guess below:")
                        actions['rebuild_text_entry'] = True
                        return_tuple = ("solve_riddle", self.master_helper, actions)
                    else:
                        actions["print_all"].append("You chose not solve this riddle.")
                        return_tuple = (None, None, actions)
        # For when there is a fill in answer to a question
        elif isinstance(frontend_input, str) and self.master_dest != None: 
            match self.master_dest:
                case "solve_riddle":
                    return_tuple = self.master_helper.solve_item(frontend_input)
        # Otherwise, just use the input as it was given
        else:
            # Save the player input as part as the saved prints
            self.save_prints.append("> " + frontend_input) 

            # Begin parsing the input
            input_value = frontend_input.strip()
            parsed_dict = self.parser.parse_input(self.player1, input_value)

            # Check the parsed dictionary for existing values
            #print(parsed_dict.values())
            for value in parsed_dict.values():
                # If any value exists
                if len(value) > 0:
                    return_tuple = self.evaluate_parsed_data(parsed_dict)
                    break
        
        # Update the game destination and helper for the next input
        # from either the case destination or the evaluated parser data
        # Also update the actions dict with the new value
        self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        # If the original user input did not trigger any aspects of the game,
        # then add a message to show players their input was not successful
        if len(actions['print_all']) == 0:
            actions['print_all'] = ["I don't understand."]

        # If character health is at 0, end the game
        if self.master_helper == "dead":
            #option to continue or quit to menu and start over
            #continue means new day and starting in room
            pass

        # If there is no destination for the next input,
        # then spend one turn of this day
        if self.master_dest == None:
            actions = gl.combine_dicts(actions, self.player1.calendar.use_turns(1, self.player1))
            # If the remaining turns are at 1/3 or 2/3 of the max, offer an event
            if (self.player1.calendar.days_list[-1].turns_left == (self.player1.calendar.max_turns_daily // 3)) or (self.player1.calendar.days_list[-1].turns_left == ((self.player1.calendar.max_turns_daily * 2) // 3)): 
                return_tuple = self.player1.calendar.calculate_next_activity().ask_event()
                self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)
                

        # If there are values to build a multiple choice option,
        # take the underlying values and place the in the waiting for the next frontend input
        # and take the display vales and place them in the actions dict
        # --- displays : 0 | values : 1 ---
        if len(actions['build_multiple_choice']) != 0:
            self.wait_for_frontend_input['build_multiple_choice'] = actions['build_multiple_choice'] #displays and values 
            actions['build_multiple_choice'] = actions['build_multiple_choice'][0] #displays
        
        # ask_y_or_no is just a simplistic way to 
        # to build a multiple choice option of yes or no
        elif actions['ask_y_or_n']:
            self.wait_for_frontend_input['build_multiple_choice'] = [["Yes", "No"], ["y", "n"]] #displays and values
            actions['build_multiple_choice'] = ["Yes", "No"] #displays 
        
        # Otherwise rebuild the text entry (no multiple choice buttons)
        else:
            actions['rebuild_text_entry'] = True
        # Remove this useless key that doesn't need to be sent to the frontend 
        actions.pop('ask_y_or_n')
        
        if len(actions['print_all']) > 0:
            # Due to some prints being duplicated for no discernable reason, 
            # this searches the print statements to make sure there are no duplicates
            for i in range(0, len(actions['print_all']) - 1):
                if actions['print_all'][i] == actions['print_all'][i+1]:
                    actions['print_all'].remove(actions['print_all'][i])

            # Save all text prints from this turn so re-loading is possible
            self.save_prints.extend(actions['print_all'])

        print()
        print("master destination", self.master_dest)
        print("master helper", self.master_helper)
        print("master actions", actions)

        return actions


    def evaluate_parsed_data(self, parsed_dict): 
        dest, helper = None, None
        actions = {
            'print_all': [],
            'ask_y_or_n': False,
            'build_multiple_choice': [],
        }

        # The parsed dictionary is as follows:
        # Casting to give better variable type highlights
        actions_list = list(parsed_dict["action"])  #parsed actions
        nearby_objects = list(parsed_dict["nearby_objects"]) #parsed objects : inv objects, storage containers, doors, room,
        nearby_gen_dict = dict(parsed_dict["nearby_gen_dict"]) #general object names and objects for each
        directions = list(parsed_dict["directions"]) #parsed directions
        original_str = str(parsed_dict["original_input"]) #original input string by the user


        # First look at nearby objects 
        # If there is one nearby object and if there is also a nearby dict key
        # check if the key of the dict is in the name of the nearby object
        
        # If general names of items were parsed
        #print(nearby_gen_dict)
        if len(nearby_gen_dict) > 0:
            # If there is 1 general name
            if len(nearby_gen_dict) == 1 and len(next(iter(nearby_gen_dict.items()))[1]) == 1:
                only_gen_item = next(iter(nearby_gen_dict.items()))[1][0]
                if only_gen_item not in nearby_objects:
                    nearby_objects.append(only_gen_item)
            # If there is more than 1 general name 
            else:
                print("checking for general name items")
                low_index = len(original_str)
                if len(nearby_gen_dict) > 1:
                    #index the general names to know which comes first
                    #set the first gen name key value pair to the variables
                    for key in nearby_gen_dict:
                        check_index = original_str.find(key)
                        if check_index < low_index:
                            curr_gen_name = key
                            curr_gen_objects = nearby_gen_dict[key]
                            low_index = check_index

                else:
                    first_key_value = next(iter(nearby_gen_dict.items()))
                    curr_gen_name = first_key_value[0]
                    curr_gen_objects = first_key_value[1]
                
                gen_name_solved = False
                if len(nearby_objects) > 0:
                    #check to see if the nearby object contains the gen_name in the name
                    #loop through nearby objects and if one of them has the gen name of the first dictionary key
                    #check if the full string minus the name of the object deletes the first key (gen_name)
                    for item in nearby_objects:
                        if curr_gen_name in item.name.lower():
                            check_str = original_str.replace(item.name.lower(), "")
                            if curr_gen_name not in check_str:
                                gen_name_solved = True
                                break
                
                # if the general name is not in the nearby object name
                # build mc - request which object the user was referencing
                if not gen_name_solved:
                    if len(actions_list) == 1:
                        actions['print_all'].append(f"Which {curr_gen_name} would you like to {actions_list[0]}?")
                    else:
                        actions['print_all'].append(f"Which {curr_gen_name} do you mean?")

                    displays = []
                    for item in curr_gen_objects:
                        displays.append(item.name)
                    displays.append("cancel")
                    curr_gen_objects.append("c")
                    actions["build_multiple_choice"] = [displays, curr_gen_objects]
                    del parsed_dict["nearby_gen_dict"][curr_gen_name]
                    return ("gen_name_request", [parsed_dict, curr_gen_name], actions) 

        #############################

        # If the parsed dictionary has an action
        if len(actions_list) > 0:
            if len(actions_list) == 1:
                
                # If there is one action and one object
                if len(nearby_objects) == 1:
                    if actions_list[0] in nearby_objects[0].item_actions:
                        function_params = self.get_item_action_params(actions_list[0], nearby_objects[0])
                        return_data = nearby_objects[0].item_actions[actions_list[0]](*function_params)
                        if isinstance(return_data, tuple):
                            dest, helper, actions = gl.parse_tuples(return_data, actions)
                        elif isinstance(return_data, dict):
                            actions = gl.combine_dicts(actions, return_data)
                    else:
                        actions['print_all'].append(f"You cannot {actions_list[0]} this item.")
                    
                # For if there are cases when an action and multiple objects need to be parsed
                elif len(nearby_objects) > 1:
                    
                    # If one is a storage unit and one is an inv_item 
                    if actions_list[0] == "drop" and len(nearby_objects) == 2:
                        # Check for if one is a storage unit and one is an inv_item
                        if isinstance(nearby_objects[0], item_class.Storage_Unit) and isinstance(nearby_objects[1], item_class.Inv_Item):
                            move_item, storage_unit = nearby_objects[1], nearby_objects[0]
                        elif isinstance(nearby_objects[1], item_class.Storage_Unit) and isinstance(nearby_objects[0], item_class.Inv_Item):
                            move_item, storage_unit = nearby_objects[0], nearby_objects[1]
                        
                        ##print(type(move_item), type(storage_unit))
                        # Depending on the storage unit, check necessary item attributes and add to it if possible
                        if isinstance(storage_unit, item_class.Wall_Storage):
                            if move_item.can_hang:
                                if move_item in self.player1.inv:
                                    return_tuple = move_item.drop_item(storage_unit, self.player1) 
                                else:
                                    return_tuple = move_item.move_item(storage_unit, self.player1)
                                dest, helper, actions = gl.parse_tuples(return_tuple, actions) 
                            else:
                                actions['print_all'].append("You cannot hang this item on a wall.")
                        else:
                            # If the inv_item is in the player inventory, put it in the storage unit
                            if move_item in self.player1.inv:
                                return_tuple = move_item.drop_item(storage_unit, self.player1) 
                            # Otherwise, move the item from one storage unit to another
                            else:
                                return_tuple = move_item.move_item(storage_unit, self.player1) 

                            dest, helper, actions = gl.parse_tuples(return_tuple, actions) 
                
                # When there are no objects, and only a direction
                elif len(directions) == 1:
                    if actions_list[0] == "go":
                        
                        if directions[0] == "cardinal":
                            actions["print_all"].append("You don't know your cardinal directions in here.")
                        else: 
                            if isinstance(directions[0], room_class.Room):
                                # move to room by name -- not set up
                                pass
                            else:
                                i = ["backward", "left", "right", "forward"].index(directions[0])
                                direction_choice = ["b", "l", "r", "f"][i]
                                blrf_dict = self.player1.build_blrf_dict()

                                next_rooms = [self.player1.loc.north, self.player1.loc.east, self.player1.loc.south, self.player1.loc.west]
                                i = ['n', 'e', 's', 'w'].index(blrf_dict[direction_choice])
                                return_tuple = self.player1.move_nesw(blrf_dict[direction_choice], next_rooms[i])
                                dest, helper = return_tuple[0], return_tuple[1]
                                actions = gl.combine_dicts(actions, return_tuple[2])

                else:
                    if actions_list[0] == "go":
                        actions['print_all'].append(f"Where do you want to {actions_list[0]}?")
                    else:
                        actions['print_all'].append(f"What do you want to {actions_list[0]}?")
            else:
                # Print error message if there are multiple actions
                actions["print_all"].append("Please only use one action at a time.")
                
        # If the parsed dictionary does not have an action
        # and does have a direction or a nearby object
        elif len(directions) >= 1 or len(nearby_objects) >= 1:
            # If there is one direction or one nearby object
            if len(directions) + len(nearby_objects) == 1:
                if len(directions) == 1:
                    if directions[0] == "cardinal":
                        actions["print_all"].append("You don't know your cardinal directions in here.")
                    else: 
                        if isinstance(directions[0], room_class.Room):
                            # example: the library is to your left ##############
                            actions["print_all"].append(f"The {directions[0].name} is to your direction")
                        else:
                            actions['print_all'].append(self.player1.loc.print_directions(self.player1, directions[0]))
                elif len(nearby_objects) == 1:
                    function_params = self.get_item_action_params("inspect", nearby_objects[0])
                    actions = nearby_objects[0].item_actions["inspect"](*function_params)
            # If there are multiple directions and/or nearby objects
            else:
                # Please refer to one object at a time
                actions["print_all"].append("Please only refer to only one item at a time.")
        '''
        # If the parsed dictionary does not have an action, or a direction, or a nearby object
        # but does have a special action
        elif len(special_actions) > 0:
            for action in special_actions:
                match action:
                    case "xd" : actions["print_all"].append(self.player1.loc.print_directions(self.player1, None))
                    case "xi" : actions["print_all"].append(self.player1.loc.xray_look_storage_units())
        '''
        return (dest, helper, actions)

    def return_map_data(self):
        map_dict = {
            "ward-rooms" : [],
            "basement-rooms" : [],
            "ward-doors" : [],
            "basement-doors" : [],
            "current-room" : []
        }

        for room in self.ward_rooms:
            if room.visited:
                map_dict["ward-rooms"].append(True)
            else:
                map_dict["ward-rooms"].append(False)
        
        for door in self.ward_doors:
            if door.visited:
                map_dict["ward-doors"].append(True)
            else:
                map_dict["ward-doors"].append(False)

        for b_room in self.basement_rooms:
            if b_room.visited:
                map_dict["basement-rooms"].append(True)
            else:
                map_dict["basement-rooms"].append(False)
        
        for door in self.basement_doors:
            if door.visited:
                map_dict["basement-doors"].append(True)
            else:
                map_dict["basement-doors"].append(False)

        # self.player1.loc: 
        # looking for which room is current and what direction the player is facing

        return map_dict