

import tnslp.game_backend.classes.character_class as character_class
import tnslp.game_backend.classes.item_class as item_class
import tnslp.game_backend.classes.parser_class as parser_class
import tnslp.game_backend.gl_backend_functions as gl
import tnslp.game_backend.objects.rooms as room
import tnslp.game_backend.objects.items as item


class Game:

    def __init__(self) -> None:
        self.master_dest = None
        self.master_helper = None
        self.wait_for_frontend_input = {'build_multiple_choice': None}
        self.save_prints = []
        self.player1 = character_class.Character("Jay Doe")
        self.parser = parser_class.Parser()
        self.item_actions_params = {
            'pick up': ['player'],
            'drop': [None, 'player'],
            'unlock': ['player'],
            'lock': ['player'],

        }
    
    def __repr__(self) -> str:
        return f'Whole Game Object - player: {self.player1.name}'

    def get_curr_ui_value(self, id):
        # must be called each time because the values change
        match id:
            case "xp_value": return self.player1.xp
            case "day_value": return self.player1.calendar.days_list[-1].day_number
            case "turns_value": return self.player1.calendar.days_list[-1].turns_left
            case "room_value": return self.player1.loc.display_name
            case "health_value": return self.player1.health
            case "diagnosis_value": return self.player1.diagnosis
            case "meditation_lvl": return self.player1.abilities[0].lvl
            case "assertiveness_lvl": return self.player1.abilities[1].lvl
            case "pos_attitude_lvl": return self.player1.abilities[2].lvl
            case "opp_action_lvl": return self.player1.abilities[3].lvl
            case "catharsis_lvl": return self.player1.abilities[4].lvl

    def start_game(self):
        actions = {
            'print_all': [],
            'update_inv_visual': [],
            'update_ui_values': [
                "xp_value", 
                "day_value", 
                "turns_value", 
                "room_value", 
                "health_value", 
                "diagnosis_value", 
                "meditation_lvl", 
                "assertiveness_lvl", 
                "pos_attitude_lvl", 
                "opp_action_lvl", 
                "catharsis_lvl"
                ],
        }

        actions['print_all'].append("As you open your eyes, you find yourself laying on a bed in a non descript bedroom.") 
        actions['print_all'].append("A person on the bed next to you welcomes you to this new place, and suggests that you spend some time exploring as there's a lot to find.")
        actions['print_all'].append("For help playing, use the game help button in the bottom right corner.")
        
        return_tuple = self.player1.loc.enter_room(self.player1)
        self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)
        actions['update_inv_visual'] = self.player1.build_inv_str_list()
        
        if len(self.save_prints) == 0:
            self.save_prints.extend(actions['print_all'])

        if len(actions['update_ui_values']) > 0:
            values_to_update = []
            for id in actions['update_ui_values']:
                values_to_update.append([id, str(self.get_curr_ui_value(id))])
            actions['update_ui_values'] = values_to_update
        #print("start game actions", actions)
        return actions

    def load_game(self):
        actions = {
            'load_prints': self.save_prints,
            'update_inv_visual': self.player1.build_inv_str_list(),
            'update_ui_values': [
                "xp_value", 
                "day_value", 
                "turns_value", 
                "room_value", 
                "health_value", 
                "diagnosis_value", 
                "meditation_lvl", 
                "assertiveness_lvl", 
                "pos_attitude_lvl", 
                "opp_action_lvl", 
                "catharsis_lvl"],
        }

        if len(actions['update_ui_values']) > 0:
            values_to_update = []
            for id in actions['update_ui_values']:
                values_to_update.append([id, str(self.get_curr_ui_value(id))])
            actions['update_ui_values'] = values_to_update

        return actions

    def organize_raw_input(self, frontend_input):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False,
            'rebuild_text_entry': False,
            'update_inv_visual': [],
            'update_ui_values': [] ###keep list empty 
        }


        

        # Set a default return tuple if nothing connects
        return_tuple = (None, None, {})

        # waiting vars = self.wait_for_frontend_input['build_multiple_choice']
        # If there is a list of variables in waiting vars and the input is numeric, 
        # convert to integer so that the correct variable from waiting vars is accessed
        if frontend_input.isnumeric() and self.wait_for_frontend_input['build_multiple_choice'] != None:
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
                case "ask_unlock_item": 
                    return_tuple = self.master_helper.ask_unlock_item(input_value, self.player1)
                case "level_up_ability": 
                    for ability in self.player1.abilities:
                        if ability.name == self.master_helper[0].name:
                            index = self.player1.abilities.index(ability)
                    return_tuple = self.player1.abilities[index].upgrade_ability(input_value, self.master_helper[1:], self.player1)
                    

            
        # Otherwise, just use the input as it was given
        else:
            # Save the player input as part as the saved prints
            self.save_prints.append("> " + frontend_input) 

            # Begin parsing the input
            input_value = frontend_input.strip()
            parsed_dict = self.parser.parse_input(self.player1, input_value)
            print("parsed data:", parsed_dict)
            # Check the parsed dictionary for existing values
            for value in parsed_dict.values():
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
                ...
        
        # If there are frontend values to update, 
        # access the data found the gui_ui_values dict 
        # and add it to the actions dict being sent to the frontend
        if len(actions['update_ui_values']) > 0:
            values_to_update = []
            for id in actions['update_ui_values']:
                values_to_update.append([id, str(self.get_curr_ui_value(id))])
            actions['update_ui_values'] = values_to_update

        # If there are values to build a multiple choice option,
        # take the underlying values and place the in the waiting for the next frontend input
        # and take the display vales and place them in the actions dict
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
            'update_inv_visual': [],
            'update_ui_values': []
        }

        # The parsed dictionary is as follows:
        """ 
        parsed_info = {
            "action" : [], #parsed actions : 
            "nearby_objects" : [], #parsed objects : inv objects, storage containers, doors, room, 
            "directions" : [], #parsed directions
            "special_actions" : []
        }
        """

        # If the parsed dictionary has an action
        if len(parsed_dict["action"]) > 0:
            if len(parsed_dict["action"]) == 1:
                # If there is one action and one object
                if len(parsed_dict["nearby_objects"]) == 1:
                    if parsed_dict["action"][0] in parsed_dict["nearby_objects"][0].item_actions:
                        function_params = []
                        # if the action requires function parameters
                        try:
                            for param in self.item_actions_params[parsed_dict["action"][0]]:
                                if param == 'player':
                                    function_params.append(self.player1)
                                else:
                                    function_params.append(param)

                            return_data = parsed_dict["nearby_objects"][0].item_actions[parsed_dict["action"][0]](*function_params)
                        except KeyError:
                            return_data = parsed_dict["nearby_objects"][0].item_actions[parsed_dict["action"][0]]()
                        
                        if isinstance(return_data, tuple):
                            dest, helper, actions = gl.parse_tuples(return_data, actions)
                        elif isinstance(return_data, dict):
                            actions = gl.combine_dicts(actions, return_data)
                    else:
                        actions['print_all'].append(f"You cannot {parsed_dict['action'][0]} this item.")
                    
                
                # For if there are cases when an action and multiple objects need to be parsed
                elif len(parsed_dict["nearby_objects"]) > 1:
                    # If one is a storage unit and one is an inv_item
                    if parsed_dict["action"][0] == "drop" and len(parsed_dict["nearby_objects"]) == 2:
                        # Check for if one is a storage unit and one is an inv_item
                        if isinstance(parsed_dict["nearby_objects"][0], item_class.Storage_Unit) and isinstance(parsed_dict["nearby_objects"][1], item_class.Inv_Item):
                            move_item, storage_unit = parsed_dict["nearby_objects"][1], parsed_dict["nearby_objects"][0]
                        elif isinstance(parsed_dict["nearby_objects"][1], item_class.Storage_Unit) and isinstance(parsed_dict["nearby_objects"][0], item_class.Inv_Item):
                            move_item, storage_unit = parsed_dict["nearby_objects"][0], parsed_dict["nearby_objects"][1]
                        
                        # Depending on the storage unit, check necessary item attributes and add to it if possible
                        if isinstance(storage_unit, item_class.Storage_Wall):
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
                elif len(parsed_dict["directions"]) == 1:
                    if parsed_dict["action"][0] == "go":
                        if parsed_dict["directions"][0] == "cardinal":
                            actions["print_all"].append("You don't know your cardinal directions in here.")
                        else: 
                            i = ["backward", "left", "right", "forward"].index(parsed_dict["directions"][0])
                            direction_choice = ["b", "l", "r", "f"][i]
                            blrf_dict = self.player1.build_blrf_dict()

                            next_rooms = [self.player1.loc.north, self.player1.loc.east, self.player1.loc.south, self.player1.loc.west]
                            i = ['n', 'e', 's', 'w'].index(blrf_dict[direction_choice])
                            return_tuple = self.player1.move_nesw(blrf_dict[direction_choice], next_rooms[i])
                            dest, helper = return_tuple[0], return_tuple[1]
                            actions = gl.combine_dicts(actions, return_tuple[2])

            else:
                # Print error message if there are multiple actions
                actions["print_all"].append("Please only use one action at a time.")
                
        # If the parsed dictionary does not have an action
        # and does have a direction or a nearby object
        elif len(parsed_dict["directions"]) >= 1 or len(parsed_dict["nearby_objects"]) >= 1:
            # If there is one direction or one nearby object
            if len(parsed_dict["directions"]) + len(parsed_dict["nearby_objects"]) == 1:
                if len(parsed_dict["directions"]) == 1:
                    if parsed_dict["directions"][0] == "cardinal":
                        actions["print_all"].append("You don't know your cardinal directions in here.")
                    else: 
                        actions['print_all'].append(self.player1.loc.print_directions(self.player1, parsed_dict["directions"][0]))
                elif len(parsed_dict["nearby_objects"]) == 1:
                    actions = gl.combine_dicts(actions, parsed_dict["nearby_objects"][0].inspect_item())
            # If there are multiple directions and/or nearby objects
            else:
                # Please refer to one object at a time
                actions["print_all"].append("Please only refer to only one item at a time.")
        # If the parsed dictionary does not have an action, or a direction, or a nearby object
        # but does have a special action
        elif len(parsed_dict["special_actions"]) > 0:
            for action in parsed_dict["special_actions"]:
                match action:
                    case "xd" : actions["print_all"].append(self.player1.loc.print_directions(self.player1, None))
                    case "xi" : actions["print_all"].append(self.player1.loc.xray_look_storage_units())

        return (dest, helper, actions)



        
