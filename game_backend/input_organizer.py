

import game_backend.classes.character_class as character_class
import game_backend.classes.item_class as item_class
import game_backend.classes.parser_class as parser_class
import game_backend.objects.rooms as room
import game_backend.gl_backend_functions as gl


#start game and handle input
def start_game():
    actions = {
        'print_all': [],
    }

    room.basement_stairs.set_coordinates(room.ward_stairs, 0, 0, room.basement_landing)
    room.ward_stairs.set_coordinates(room.basement_stairs, 0, 0, room.common_room)

    room.basement_set_door_dictionaries()
    room.ward_set_door_dictionaries()

    global master_dest, master_helper
    master_dest, master_helper = None, None

    global wait_for_frontend_input
    wait_for_frontend_input = {
        'build_multiple_choice': None,
    }

    actions['print_all'].append("----Intro Paragraph----") 
    actions['print_all'].append("...")

    global player1
    player1 = character_class.Character("Jay Doe")
    #gui.update_inv_visual(player1)
    global input_parser
    input_parser = parser_class.Parser()

    actions['print_all'].append("Welcome " + player1.name + "!")
    
    actions['print_all'].append("----Secondary Intro Paragraph----")
    actions['print_all'].append("...")

    actions['print_all'].append("Enter 'commands' to display all commands or 'help' for more information: ")

    return_tuple = player1.enter_room()
    actions = parse_tuples(return_tuple, actions)

    return actions


def organize_raw_input(frontend_input):
    global master_helper, master_dest, wait_for_frontend_input
    actions = {
        'print_all': [],
        'build_multiple_choice': [],
        'ask_y_or_n': False,
        'rebuild_text_input': False
    }

    if frontend_input.isnumeric() and wait_for_frontend_input['build_multiple_choice'] != None:
        input_value = wait_for_frontend_input['build_multiple_choice'][int(frontend_input)]
        wait_for_frontend_input['build_multiple_choice'] = None
    else:
        input_value = frontend_input.strip()

    ### parsing begins ###
    if master_dest == None:
        parsed_values, print_list = input_parser.parse_input(player1, input_value)
        print(parsed_values, print_list)
        actions['print_all'].extend(print_list)
        parsed = False
        if not isinstance(parsed_values, bool):
            for value in parsed_values:
                if value != None:
                    parsed = True
                    #print("parser found data")
                    return_tuple = parser_class.organize_parsed_data(parsed_values, player1)
                    actions = parse_tuples(return_tuple, actions)
                    break
        else:
            parsed = True 

        if not parsed:
            return_tuple = main(input_value, master_helper)
            actions = parse_tuples(return_tuple, actions)
        

    elif master_dest == "drop_gen_item":
        return_tuple = player1.drop_gen_item(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "add_inventory_choice":
        return_tuple = player1.add_inventory_choice(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "full_inv_drop_items":
        return_tuple = player1.full_inv_drop_items(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "drop_x_for_y":
        return_tuple = player1.drop_x_for_y(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "inspect_pb":
        return_tuple = player1.inspect_pb(input_value) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "interact_pb":
        return_tuple = player1.interact_pb(input_value)
        actions = parse_tuples(return_tuple, actions) 

    elif master_dest == "deal_take_damage":
        return_tuple = player1.deal_take_damage(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "choose_fight_action":
        return_tuple = player1.choose_fight_action(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "open_door_key":
        return_tuple = player1.open_door_key(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "open_door_crowbar": #x2
        return_tuple = player1.open_door_crowbar(input_value, master_helper) 
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "choose_room":
        return_tuple = player1.choose_room(input_value, master_helper)
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "open_electronic_door":
        return_tuple = player1.open_electronic_door(input_value, master_helper)
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "enter_code":
        master_return, master_helper = master_helper[2].enter_code(input_value, master_helper)
        ###???

    elif master_dest == "drop_item":
        return_tuple = player1.drop_item_choice(input_value)
        actions = parse_tuples(return_tuple, actions)

    elif master_dest == "execute_event":
        master_return, master_helper = master_helper.execute_event(input_value) ###???
        if isinstance(master_helper, int):
            for i in range(0, master_helper):
                # Updates the gui visual to show the decrease in turns
                player1.calendar.use_turns(1)

    else:
        actions['print_all'].append("We have an issue...")

    if master_helper == "dead":
        #game over screen
        pass

    """
    if master_return == None and not isinstance(master_helper, int):
        player1.calendar.use_turns(1)
        if player1.calendar.days_list[-1].turns_left == (player1.calendar.max_turns_daily // 3) or player1.calendar.days_list[-1].turns_left == ((player1.calendar.max_turns_daily * 2) // 3): 
            master_return, master_helper = player1.calendar.calculate_next_activity().ask_event()
        else:
            master_return, master_helper = None, None
    """

    
    if len(actions['build_multiple_choice']) != 0:
        wait_for_frontend_input['build_multiple_choice'] = actions['build_multiple_choice'][1] #values
        actions['build_multiple_choice'] = actions['build_multiple_choice'][0] #displays
       
    elif actions['ask_y_or_n']:
        wait_for_frontend_input['build_multiple_choice'] = ["y", "n"] #values
        actions['build_multiple_choice'] = ["Yes", "No"] #displays
        actions.pop('ask_y_or_n')
    
    else:
        actions['rebuild_text_entry'] = True

    print()
    print("master return", master_dest)
    print("master helper", master_helper)
    print("master actions", actions)

    return actions


def main(choice, helper): 
    return_tuple = (None, None, None)
    actions = {
        'print_all': []
    }
    #this is for when an item is selected from the inventory and selected to be dropped
    if choice == 'drop item':
        if isinstance(helper, item_class.Item):
            return_tuple = player1.drop_item_choice(helper)
        else:
            # if using the command line a player wants to drop an item
            pass

    elif choice == 'inspect item':
        if isinstance(helper, item_class.Item):
            return_tuple = helper.inspect_item()
            actions = gl.combine_dicts(actions, return_tuple[2])
        else:
            # If a player wants to inspect an item either available in the room or in their inventory
            pass

    return (return_tuple[1], return_tuple[2], actions)


def parse_tuples(tuple_list, old_action_dict):
    global master_dest, master_helper
    master_dest, master_helper = tuple_list[0], tuple_list[1]
    new_action_dict = gl.combine_dicts(old_action_dict, tuple_list[2])
    return new_action_dict
