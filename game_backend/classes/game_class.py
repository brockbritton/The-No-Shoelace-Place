
import game_backend.classes.character_class as character_class
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

        self.save_prints.append("> " + frontend_input) ####doesnt work for multiple choice

        if frontend_input.isnumeric() and self.wait_for_frontend_input['build_multiple_choice'] != None:
            print("convert to int")
            input_value = self.wait_for_frontend_input['build_multiple_choice'][int(frontend_input)]
            self.wait_for_frontend_input['build_multiple_choice'] = None
        else:
            print("stay as str")
            input_value = frontend_input.strip()

        ### parsing begins ###
        if self.master_dest == None:
            parsed_values, print_list = self.parser.parse_input(self.player1, input_value)
            actions['print_all'].extend(print_list)
            parsed = False
            if not isinstance(parsed_values, bool):
                for value in parsed_values:
                    if value != None:
                        parsed = True
                        #print("parser found data")
                        return_tuple = parser_class.organize_parsed_data(parsed_values, self.player1)
                        self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)
                        break
            else:
                # error in user input rules, skip parsing
                parsed = True 
            

        elif self.master_dest == "drop_gen_item":
            return_tuple = self.player1.drop_gen_item(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "add_inventory_choice":
            return_tuple = self.player1.add_inventory_choice(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "full_inv_drop_items":
            return_tuple = self.player1.full_inv_drop_items(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "drop_x_for_y":
            return_tuple = self.player1.drop_x_for_y(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "inspect_pb":
            return_tuple = self.player1.inspect_pb(input_value) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "interact_pb":
            return_tuple = self.player1.interact_pb(input_value)
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions) 

        elif self.master_dest == "deal_take_damage":
            return_tuple = self.player1.deal_take_damage(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "choose_fight_action":
            return_tuple = self.player1.choose_fight_action(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "open_door_key":
            return_tuple = self.player1.open_door_key(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "open_door_crowbar": #x2
            return_tuple = self.player1.open_door_crowbar(input_value, self.master_helper) 
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "choose_room":
            return_tuple = self.player1.choose_room(input_value, self.master_helper)
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "open_electronic_door":
            return_tuple = self.player1.open_electronic_door(input_value, self.master_helper)
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "enter_code":
            self.master_dest, self.master_helper = self.master_helper[2].enter_code(input_value, self.master_helper)
            ###???

        elif self.master_dest == "drop_item":
            return_tuple = self.player1.drop_item_choice(input_value)
            self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)

        elif self.master_dest == "execute_event":
            self.master_dest, self.master_helper = self.master_helper.execute_event(input_value) ###???
            if isinstance(self.master_helper, int):
                actions = gl.combine_dicts(actions, self.player1.calendar.use_turns(self.master_helper))

        else:
            print("We have a destination issue...")

        if self.master_helper == "dead":
            #game over screen
            pass

        # Using turns and potential to ask events
        if self.master_dest == None:
            actions = gl.combine_dicts(actions, self.player1.calendar.use_turns(1))
            if (self.player1.calendar.days_list[-1].turns_left == (self.player1.calendar.max_turns_daily // 3)) or (self.player1.calendar.days_list[-1].turns_left == ((self.player1.calendar.max_turns_daily * 2) // 3)): 
                pass
                #return_tuple = self.player1.calendar.calculate_next_activity().ask_event()
                #self.master_dest, self.master_helper, actions = gl.parse_tuples(return_tuple, actions)
            else:
                self.master_dest, self.master_helper = None, None
        
        
        if len(actions['update_ui_values']) > 0:
            values_to_update = []
            for id in actions['update_ui_values']:
                values_to_update.append([id, str(self.get_ui_values(self.player1, id))])
            actions['update_ui_values'] = values_to_update

        
        if len(actions['build_multiple_choice']) != 0:
            self.wait_for_frontend_input['build_multiple_choice'] = actions['build_multiple_choice'][1] #values
            actions['build_multiple_choice'] = actions['build_multiple_choice'][0] #displays
        
        elif actions['ask_y_or_n']:
            self.wait_for_frontend_input['build_multiple_choice'] = ["y", "n"] #values
            actions['build_multiple_choice'] = ["Yes", "No"] #displays
            actions.pop('ask_y_or_n')
        
        else:
            actions['rebuild_text_entry'] = True

        if len(actions['print_all']) == 0:
            actions['print_all'] = ["I don't understand."]

        #Save text prints from this term so loading is possible
        self.save_prints.extend(actions['print_all'])

        print()
        print("master return", self.master_dest)
        print("master helper", self.master_helper)
        print("master actions", actions)

        return actions


        
