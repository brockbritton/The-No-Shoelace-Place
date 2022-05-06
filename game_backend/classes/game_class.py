
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

        return_tuple = self.player1.enter_room()
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
            parsed_values, print_list = self.parser.parse_input(self.player1, input_value)
            actions['print_all'].extend(print_list)

            # If a boolean were returned, an errorneous input was given
            # Otherwise, check for existence of parsed values
            if not isinstance(parsed_values, bool):
                for value in parsed_values:
                    if value != None:
                        return_tuple = self.organize_parsed_data(parsed_values, self.player1)
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


    def organize_parsed_data(self, parsed_tuple, player): 
        dest, helper = None, None
        actions = {
            'print_all': [],
            'ask_y_or_n': False,
            'build_multiple_choice': [],
            'update_inv_visual': [],
            'update_ui_values': []
        }
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
        print(parsed_tuple)


        # If there is no verb and one object - inspect object
        if (action == None or action == 'inspect') and object_loc_tuple != None:
            if isinstance(object_loc_tuple[0], item_class.Inv_Item):
                actions = gl.combine_dicts(actions, object_loc_tuple[0].inspect_item())
            else:
                actions['print_all'].append("You can only inspect items at this time.")
        
            
        elif direction_tuple != None:
            # Move a certain direction
            if direction_tuple[0] == "go":
                i = ["backward", "left", "right", "forward"].index(direction_tuple[1])
                direction_choice = ["b", "l", "r", "f"][i]
                blrf_dict = player.check_blrf_directions()

                next_rooms = [player.loc.north, player.loc.east, player.loc.south, player.loc.west]
                i = ['n', 'e', 's', 'w'].index(blrf_dict[direction_choice])
                return_tuple = player.move_nesw(blrf_dict[direction_choice], next_rooms[i])
                dest, helper = return_tuple[0], return_tuple[1]
                actions = gl.combine_dicts(actions, return_tuple[2])

            # Printing adjacent rooms for a certain direction
            # direction_tuple[0] == None
            else:
                actions['print_all'].append(player.loc.print_directions(player, direction_tuple[1]))


        elif display_option_tuple != None:
            if display_option_tuple[1] == 'items':
                actions['print_all'].append(player.loc.print_items_loc_desc())

            elif display_option_tuple[1] == 'directions':
                actions['print_all'].append(player.loc.print_directions(player, None))

        # If there is one action and one object
        elif action != None and object_loc_tuple != None:
            
            if action == "pick up":
                if object_loc_tuple[0].pick_up_bool:
                    if isinstance(object_loc_tuple[1], item_class.Storage_Unit):
                        return_tuple = player.pick_up_item(object_loc_tuple[0])
                        dest, helper, = return_tuple[0], return_tuple[1]
                        actions = gl.combine_dicts(actions, return_tuple[2])
                    elif isinstance(object_loc_tuple[1], list):
                        actions['print_all'].append("This item is already in your inventory.")
                else:
                    actions['print_all'].append("You cannot pick up this item.")

            elif action == "drop":
                if object_loc_tuple[0] in player.inv:
                    if storage_locations == None or 'drop' not in storage_locations.keys():
                        return_tuple = player.drop_item(object_loc_tuple[0], None) 
                        dest, helper, = return_tuple[0], return_tuple[1]
                        actions = gl.combine_dicts(actions, return_tuple[2])
                        actions['print_all'].append(f"You have dropped the {object_loc_tuple[0].name} on the ground.")
                    else:
                        if 'drop' in storage_locations.keys():
                            if len(storage_locations['drop']) == 1:
                                return_tuple = player.drop_item(object_loc_tuple[0], storage_locations['drop'][0])
                                dest, helper, = return_tuple[0], return_tuple[1]
                                actions = gl.combine_dicts(actions, return_tuple[2])
                                actions['print_all'].append(f"You have dropped the {object_loc_tuple[0].name} to the {storage_locations['drop'][0].name}.")
                            else:
                                return_tuple = player.drop_item(object_loc_tuple[0], None) 
                                dest, helper, = return_tuple[0], return_tuple[1]
                                actions = gl.combine_dicts(actions, return_tuple[2])
                                actions['print_all'].append(f"You have dropped the {object_loc_tuple[0].name} on the ground.")
                else:
                    actions['print_all'].append("You cannot drop this item beacuse you are not holding it.")

            elif action == "inspect":
                if object_loc_tuple[0].inspect_bool:
                    pass
                else:
                    actions['print_all'].append("You cannot inspect this item.")

            elif action == "open":
                if object_loc_tuple[0].openable_bool:
                    pass
                else:
                    actions['print_all'].append("You cannot open this item")

            elif action == "unlock":
                if object_loc_tuple[0].lockable_bool:
                    pass
                else:
                    actions['print_all'].append("You cannot unlock this item")

            elif action == "lock":
                if object_loc_tuple[0].lockable_bool:
                    pass
                else:
                    actions['print_all'].append("You cannot lock this item")

            elif action == "interact":
                if object_loc_tuple[0].interact_bool:
                    pass
                else:
                    actions['print_all'].append("You cannot interact with this item")

            elif action == "break":
                if object_loc_tuple[0].breakable:
                    pass
                else:
                    actions['print_all'].append("You cannot break this item")
        
        
        return (dest, helper, actions)
    


        
