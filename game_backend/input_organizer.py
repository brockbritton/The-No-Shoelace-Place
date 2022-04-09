

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
    actions = gl.combine_dicts(actions, return_tuple[2])

    return_tuple = (return_tuple[0], return_tuple[1], actions)
    return return_tuple


def organize_raw_input(dest, line_input, help_var):

    return_tuple = (None, None, None)
    actions = {
        'print_all': [],
        'build_multiple_choice': [],
        'ask_y_or_n': False
        }
    if dest == None:
        parsed_values, print_list = input_parser.parse_input(player1, line_input)
        print(parsed_values, print_list)
        actions['print_all'].extend(print_list)
        parsed = False
        if not isinstance(parsed_values, bool):
            for value in parsed_values:
                if value != None:
                    parsed = True
                    #print("parser found data")
                    return_tuple = parser_class.organize_parsed_data(parsed_values, player1)
                    actions = gl.combine_dicts(actions, return_tuple[2])
                    return_tuple = (return_tuple[0], return_tuple[1], actions)
                    break
        else:
            parsed = True 

        if not parsed:
            return_tuple = main(line_input, help_var)
            actions = gl.combine_dicts(actions, return_tuple[2])
            return_tuple = (return_tuple[0], return_tuple[1], actions)
        
            
    elif dest == "drop_gen_item":
        return_tuple = player1.drop_gen_item(line_input, help_var) 

    elif dest == "add_inventory_choice":
        return_tuple = player1.add_inventory_choice(line_input, help_var) 

    elif dest == "full_inv_drop_items":
        return_tuple = player1.full_inv_drop_items(line_input, help_var) 

    elif dest == "drop_x_for_y":
        return_tuple = player1.drop_x_for_y(line_input, help_var) 

    elif dest == "inspect_pb":
        return_tuple = player1.inspect_pb(line_input) 

    elif dest == "interact_pb":
        return_tuple = player1.interact_pb(line_input) 

    elif dest == "deal_take_damage":
        return_tuple = player1.deal_take_damage(line_input, help_var) 

    elif dest == "choose_fight_action":
        return_tuple = player1.choose_fight_action(line_input, help_var) 

    elif dest == "open_door_key":
        return_tuple = player1.open_door_key(line_input, help_var) 

    elif dest == "open_door_crowbar": #x2
        return_tuple = player1.open_door_crowbar(line_input, help_var) 

    elif dest == "choose_room":
        return_tuple = player1.choose_room(line_input, help_var)

    elif dest == "open_electronic_door":
        return_tuple = player1.open_electronic_door(line_input, help_var)

    elif dest == "enter_code":
        master_return, help_var = help_var[2].enter_code(line_input, help_var)

    elif dest == "drop_item":
        return_tuple = player1.drop_item_choice(line_input)

    elif dest == "execute_event":
        master_return, help_var = help_var.execute_event(line_input)
        if isinstance(help_var, int):
            for i in range(0, help_var):
                # Updates the gui visual to show the decrease in turns
                player1.calendar.use_turns(1)

    else:
        actions['print_all'].append("We have an issue...")

    if help_var == "dead":
        #game over screen
        pass

    """
    if master_return == None and not isinstance(help_var, int):
        player1.calendar.use_turns(1)
        if player1.calendar.days_list[-1].turns_left == (player1.calendar.max_turns_daily // 3) or player1.calendar.days_list[-1].turns_left == ((player1.calendar.max_turns_daily * 2) // 3): 
            master_return, help_var = player1.calendar.calculate_next_activity().ask_event()
        else:
            master_return, help_var = None, None
    """

    print("master return", return_tuple[0])
    print("master helper", return_tuple[1])
    print()
    return return_tuple


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


