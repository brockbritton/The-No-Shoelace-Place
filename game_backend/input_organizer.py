

import game_backend.classes.character_class as character_class
import game_backend.classes.item_class as item_class
import game_backend.classes.parser_class as parser_class
import game_backend.objects.rooms as room
import game_backend.gl_backend_functions as gl

from flask import session

def create_character():
    try:
        if session['player1'] is not None:
            print("character exists")

    except KeyError:
        session['player1'] = character_class.Character("Jay Doe")
        print("character now exists")
    

#start game and handle input
def start_game():
    actions = {
        'print_all': [],
        'update_inv_visual': [],
        'update_ui_values': {}
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

    global input_parser
    
    # Check if player1 exists in session
    create_character()
    input_parser = parser_class.Parser()
    
    #Update inventory visual
    actions['update_inv_visual'] = session['player1'].build_inv_str_list()
    

    actions['print_all'].append("Welcome " + session['player1'].name + "!")
    
    actions['print_all'].append("----Secondary Intro Paragraph----")
    actions['print_all'].append("...")

    actions['print_all'].append("For help, use the game help button in the bottom right corner.")

    return_tuple = session['player1'].enter_room()
    master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)
    if len(session['save_prints']) == 0:
        session['save_prints'].extend(actions['print_all'])

    return actions

def load_game():
    actions = {
        'load_prints': session['save_prints'],
        'update_inv_visual': session['player1'].build_inv_str_list(),
        'update_ui_values': {}
    }

    return actions

def organize_raw_input(frontend_input):
    global master_helper, master_dest, wait_for_frontend_input
    print(session)
    print(type(session['player1']))
    actions = {
        'print_all': [],
        'build_multiple_choice': [],
        'ask_y_or_n': False,
        'rebuild_text_entry': False,
        'update_inv_visual': []
    }

    session['save_prints'].append("> " + frontend_input)

    if frontend_input.isnumeric() and wait_for_frontend_input['build_multiple_choice'] != None:
        input_value = wait_for_frontend_input['build_multiple_choice'][int(frontend_input)]
        wait_for_frontend_input['build_multiple_choice'] = None
    else:
        input_value = frontend_input.strip()

    ### parsing begins ###
    if master_dest == None:
        parsed_values, print_list = input_parser.parse_input(session['player1'], input_value)
        actions['print_all'].extend(print_list)
        parsed = False
        if not isinstance(parsed_values, bool):
            for value in parsed_values:
                if value != None:
                    parsed = True
                    #print("parser found data")
                    return_tuple = parser_class.organize_parsed_data(parsed_values, session['player1'])
                    master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)
                    break
        else:
            # error in user input rules, skip parsing
            parsed = True 
        

    elif master_dest == "drop_gen_item":
        return_tuple = session['player1'].drop_gen_item(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "add_inventory_choice":
        return_tuple = session['player1'].add_inventory_choice(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "full_inv_drop_items":
        return_tuple = session['player1'].full_inv_drop_items(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "drop_x_for_y":
        return_tuple = session['player1'].drop_x_for_y(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "inspect_pb":
        return_tuple = session['player1'].inspect_pb(input_value) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "interact_pb":
        return_tuple = session['player1'].interact_pb(input_value)
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions) 

    elif master_dest == "deal_take_damage":
        return_tuple = session['player1'].deal_take_damage(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "choose_fight_action":
        return_tuple = session['player1'].choose_fight_action(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "open_door_key":
        return_tuple = session['player1'].open_door_key(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "open_door_crowbar": #x2
        return_tuple = session['player1'].open_door_crowbar(input_value, master_helper) 
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "choose_room":
        return_tuple = session['player1'].choose_room(input_value, master_helper)
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "open_electronic_door":
        return_tuple = session['player1'].open_electronic_door(input_value, master_helper)
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "enter_code":
        master_return, master_helper = master_helper[2].enter_code(input_value, master_helper)
        ###???

    elif master_dest == "drop_item":
        return_tuple = session['player1'].drop_item_choice(input_value)
        master_dest, master_helper, actions = gl.parse_tuples(return_tuple, actions)

    elif master_dest == "execute_event":
        master_return, master_helper = master_helper.execute_event(input_value) ###???
        if isinstance(master_helper, int):
            for i in range(0, master_helper):
                # Updates the gui visual to show the decrease in turns
                session['player1'].calendar.use_turns(1)

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

    if actions['print_all'] == []:
        actions['print_all'] = ["Excuse me?"]

    session['save_prints'].extend(actions['print_all'])

    print()
    print("master return", master_dest)
    print("master helper", master_helper)
    print("master actions", actions)

    return actions



