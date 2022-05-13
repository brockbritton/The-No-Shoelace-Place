
from tkinter import E
import game_backend.classes.character_class as character_class
import game_backend.classes.item_class as item_class
import game_backend.classes.parser_class as parser_class
import game_backend.gl_backend_functions as gl
import game_backend.objects.rooms as room


class Game:

    def __init__(self) -> None:
        self.master_dest = None
        self.master_helper = None
        self.wait_for_frontend_input = {'build_multiple_choice': None}
        self.save_prints = []
        self.player1 = character_class.Character("Jay Doe")
        self.parser = parser_class.Parser()
        room.basement_set_door_dictionaries()
        room.ward_set_door_dictionaries()
    
    def __repr__(self) -> str:
        return f'Whole Game Object - player: {self.player1.name}'
        

    def get_ui_values(self, player, id):
        ui_values = {
            # id for html element : (current value, method of updating)
            "xp_value": player.xp,
            "day_value": player.calendar.days_list[-1].day_number,
            "turns_value": player.calendar.days_list[-1].turns_left,
            "room_value": player.loc.display_name,
            "health_value": player.health,
            "diagnosis_value": player.diagnosis,
            "meditation_lvl": player.abilities[0].lvl,
            "assertiveness_lvl": player.abilities[1].lvl,
            "pos_attitude_lvl": player.abilities[2].lvl,
            "opp_action_lvl": player.abilities[3].lvl,
            "catharsis_lvl":  player.abilities[4].lvl,
        }
        return ui_values[id]

    def start_game(self):
        actions = {
            'print_all': [],
            'update_inv_visual': [],
            'update_ui_values': [],
        }

        actions['print_all'].append("----Intro Paragraph----") 
        actions['print_all'].append("...")

        #Update inventory visual
        actions['update_inv_visual'] = self.player1.build_inv_str_list()
        

        actions['print_all'].append("Welcome " + self.player1.name + "!")
        
        actions['print_all'].append("----Secondary Intro Paragraph----")
        actions['print_all'].append("...")

        actions['print_all'].append("For help, use the game help button in the bottom right corner.")

        return_tuple = self.player1.loc.enter_room(self.player1)
        self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)
        
        if len(self.save_prints) == 0:
            self.save_prints.extend(actions['print_all'])

        if len(actions['update_ui_values']) > 0:
            values_to_update = []
            for id in actions['update_ui_values']:
                values_to_update.append([id, str(self.get_ui_values(self.player1, id))])
            actions['update_ui_values'] = values_to_update

        return actions

    def load_game(self):
        actions = {
            'load_prints': self.save_prints,
            'update_inv_visual': self.player1.build_inv_str_list(),
            'update_ui_values': ["xp_value", "day_value", "turns_value", "room_value", "health_value", "diagnosis_value", "meditation_lvl", "assertiveness_lvl", "pos_attitude_lvl", "opp_action_lvl", "catharsis_lvl"],
        }

        if len(actions['update_ui_values']) > 0:
            values_to_update = []
            for id in actions['update_ui_values']:
                values_to_update.append([id, str(self.get_ui_values(self.player1, id))])
            actions['update_ui_values'] = values_to_update

        return actions

    def organize_raw_input(self, frontend_input):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False,
            'rebuild_text_entry': False,
            'update_inv_visual': [],
            'update_ui_values': ["room_value"] ###keep empty 
        }

        # Save the player input as part as the saved prints
        self.save_prints.append("> " + frontend_input) ####doesnt work for multiple choice

        # Set a default return tuple if nothing connects
        return_tuple = (None, None, {})

        # waiting vars = self.wait_for_frontend_input['build_multiple_choice']
        # If there is a list of variables in waiting vars and the input is numeric, 
        # convert to integer so that the correct variable from waiting vars is accessed
        if frontend_input.isnumeric() and self.wait_for_frontend_input['build_multiple_choice'] != None:
            input_value = self.wait_for_frontend_input['build_multiple_choice'][int(frontend_input)]
            self.wait_for_frontend_input['build_multiple_choice'] = None

            # Match the destination to the input value
            # and execute the desired action
            print("matching destination")
            match self.master_dest:
                case "drop_gen_item": return_tuple = self.player1.drop_gen_item(input_value, self.master_helper) 
                case "add_inventory_choice": return_tuple = self.player1.add_inventory_choice(input_value, self.master_helper) 
                case "full_inv_drop_items": return_tuple = self.player1.full_inv_drop_items(input_value, self.master_helper) 
                case "drop_x_for_y": return_tuple = self.player1.drop_x_for_y(input_value, self.master_helper) 
                case "inspect_pb": return_tuple = self.player1.inspect_pb(input_value) 
                case "interact_pb": return_tuple = self.player1.interact_pb(input_value)
                case "deal_take_damage": return_tuple = self.player1.deal_take_damage(input_value, self.master_helper) 
                case "choose_fight_action": return_tuple = self.player1.choose_fight_action(input_value, self.master_helper) 
                case "open_door_key": return_tuple = self.player1.open_door_key(input_value, self.master_helper) 
                case "open_door_crowbar": return_tuple = self.player1.open_door_crowbar(input_value, self.master_helper) 
                case "choose_room": return_tuple = self.player1.choose_room(input_value, self.master_helper)
                case "open_electronic_door": return_tuple = self.player1.open_electronic_door(input_value, self.master_helper)
                case "drop_item": return_tuple = self.player1.drop_item_choice(input_value)
                case "enter_code": return_tuple = self.master_helper[2].enter_code(input_value, self.master_helper)
                case "execute_event": return_tuple = self.master_helper.execute_event(input_value)


        # Otherwise, just use the input as it was given
        else:
            print("parsing data - no destination")
            input_value = frontend_input.strip()

            # Begin parsing the input
            parsed_dict = self.parser.parse_input(self.player1, input_value)
            # Check the parsed dictionary for existing values
            for value in parsed_dict.values():
                if len(value) > 0:
                    return_tuple = self.evaluate_parsed_data(parsed_dict)
                    break
        
        # Update the game destination and helper for the next input
        # Also update the actions dict with the new value
        self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        
        if self.master_helper == "dead":
            #option to continue or quit to menu and start over
            #continue means new day and starting in room
            pass

        # If there is no destination for the next input,
        # then spend one turn of this day
        if self.master_dest == None:
            actions = gl.combine_dicts(actions, self.player1.calendar.use_turns(1))
            # If the remaining turns are at 1/3 or 2/3 of the max, offer an event
            if (self.player1.calendar.days_list[-1].turns_left == (self.player1.calendar.max_turns_daily // 3)) or (self.player1.calendar.days_list[-1].turns_left == ((self.player1.calendar.max_turns_daily * 2) // 3)): 
                #return_tuple = self.player1.calendar.calculate_next_activity().ask_event()
                #self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)
                ...
        
        # If there are frontend values to update, 
        # access the data found the gui_ui_values dict 
        # and add it to the actions dict being sent to the frontend
        if len(actions['update_ui_values']) > 0:
            values_to_update = []
            for id in actions['update_ui_values']:
                values_to_update.append([id, str(self.get_ui_values(self.player1, id))])
            actions['update_ui_values'] = values_to_update

        # If there are values to build a multiple choice option,
        # take the underlying values and place the in the waiting for the next frontend input
        # and take the display vales and place them in the actions dict
        if len(actions['build_multiple_choice']) != 0:
            self.wait_for_frontend_input['build_multiple_choice'] = actions['build_multiple_choice'][1] #values
            actions['build_multiple_choice'] = actions['build_multiple_choice'][0] #displays
        
        # ask_y_or_no is just a simplistic way to note 
        # to build a multiple choice
        elif actions['ask_y_or_n']:
            self.wait_for_frontend_input['build_multiple_choice'] = ["y", "n"] #values
            actions['build_multiple_choice'] = ["Yes", "No"] #displays
            actions.pop('ask_y_or_n')
        
        # Otherwise rebuild the text entry (no multiple choice buttons)
        else:
            actions['rebuild_text_entry'] = True

        # If the original user input did not trigger any aspects of the game,
        # then add a message to show players their input was not successful
        if len(actions['print_all']) == 0:
            actions['print_all'] = ["I don't understand."]

        # Save all text prints from this turn so re-loading is possible
        self.save_prints.extend(actions['print_all'])

        print()
        print("master return", self.master_dest)
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
        print(parsed_dict) 
        # If the parsed dictionary has an action
        if len(parsed_dict["action"]) > 0:
            if len(parsed_dict["action"]) == 1:
                # If there is an action and an object
                if len(parsed_dict["nearby_objects"]) == 1:
                    if parsed_dict["action"][0] == "pick up":
                        if isinstance(parsed_dict["nearby_objects"][0], item_class.Inv_Item):
                            if parsed_dict["nearby_objects"][0] not in self.player1.inv:
                                return_tuple = self.player1.pick_up_item(parsed_dict["nearby_objects"][0])
                                dest, helper, actions = gl.parse_tuples(return_tuple, actions)
                            else:
                                actions["print_all"].append("You are already holding this item.")

                        else:
                            actions['print_all'].append("You cannot pick up this item.")

                    elif parsed_dict["action"][0] == "drop":
                        if parsed_dict["nearby_objects"][0] in self.player1.inv:
                            return_tuple = self.player1.drop_item(parsed_dict["nearby_objects"][0], None) #need parsing for drop location
                            dest, helper, actions = gl.parse_tuples(return_tuple, actions)
                        else:
                            actions['print_all'].append("You cannot drop this item because you are not holding it.") 

                    elif parsed_dict["action"][0] == "inspect": #working
                        try:
                            actions = gl.combine_dicts(actions, parsed_dict["nearby_objects"][0].inspect_object())
                        except AttributeError:
                            actions['print_all'].append("You cannot inspect this item.")

                    elif parsed_dict["action"][0] == "open":
                        if True:
                            pass
                        else:
                            actions['print_all'].append("You cannot open this item")

                    elif parsed_dict["action"][0] == "unlock":
                        if True:
                            pass
                        else:
                            actions['print_all'].append("You cannot unlock this item")

                    elif parsed_dict["action"][0] == "lock":
                        if True:
                            pass
                        else:
                            actions['print_all'].append("You cannot lock this item")

                    elif parsed_dict["action"][0] == "interact":
                        if True:
                            pass
                        else:
                            actions['print_all'].append("You cannot interact with this item")

                    elif parsed_dict["action"][0] == "break":
                        if True:
                            pass
                        else:
                            actions['print_all'].append("You cannot break this item")
                
                # If an action and a direction, but no object
                elif len(parsed_dict["directions"]) == 1:
                    if parsed_dict["action"][0] == "go":
                        if parsed_dict["directions"][0] == "cardinal":
                            actions["print_all"].append("You don't know your cardinal directions in here.")
                        else: 
                            i = ["backward", "left", "right", "forward"].index(parsed_dict["directions"][0])
                            direction_choice = ["b", "l", "r", "f"][i]
                            blrf_dict = self.player1.check_blrf_directions()

                            next_rooms = [self.player1.loc.north, self.player1.loc.east, self.player1.loc.south, self.player1.loc.west]
                            i = ['n', 'e', 's', 'w'].index(blrf_dict[direction_choice])
                            return_tuple = self.player1.move_nesw(blrf_dict[direction_choice], next_rooms[i])
                            dest, helper = return_tuple[0], return_tuple[1]
                            actions = gl.combine_dicts(actions, return_tuple[2])

            else:
                # Print error message if there are multiple actions
                pass
                
        # If the parsed dictionary does not have an action
        # and does have a direction or a nearby object
        elif len(parsed_dict["directions"]) > 0 or len(parsed_dict["nearby_objects"]) > 0:
            if len(parsed_dict["directions"]) + len(parsed_dict["nearby_objects"]) == 1:
                if len(parsed_dict["directions"]) == 1:
                    if parsed_dict["directions"][0] == "cardinal":
                        actions["print_all"].append("You don't know your cardinal directions in here.")
                    else: 
                        actions['print_all'].append(self.player1.loc.print_directions(self.player1, parsed_dict["directions"][0]))
                elif len(parsed_dict["nearby_objects"]) == 1:
                    pass
            else:
                # Please refer to one object at a time
                pass
        # If the parsed dictionary does not have an action, or a direction, or a nearby object
        # and does have a special action
        elif len(parsed_dict["special_actions"]) > 0:
            for action in parsed_dict["special_actions"]:
                match action:
                    case "xd" : actions["print_all"].append(self.player1.loc.print_directions(self.player1, None))
                    case "xi" : actions["print_all"].append(self.player1.loc.xray_look_storage_units())



        return (dest, helper, actions)
    


        
