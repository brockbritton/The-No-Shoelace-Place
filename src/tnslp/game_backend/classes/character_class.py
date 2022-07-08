

import random

import tnslp.game_backend.classes.calendar_class as calendar_class
import tnslp.game_backend.gl_backend_functions as gl
import tnslp.game_backend.objects.abilities as ability
import tnslp.game_backend.objects.items as item


class Character:

    def __init__(self, name) -> None:
        self.name = name
        self.loc = None
        self.last_loc = None

        self.inv = [item.id_bracelet, item.basement_key, item.crowbar]
        #self.inv = []
        self.inv_cap = 6 #current inventory capacity - maybe just keep it set
        self.inv_cap_start = 6 #starting inventory capacity

        self.health = 65 #starting / current player health
        self.full_health = 100 #maximum player health
        self.diagnosis = None

        self.xp = 150
        self.xp_dict = {
            'new_room': 10,
            'new_item': 5,
            'easter_egg': 100,
            'new_door_unlocked': 50,
        }

        self.calendar = calendar_class.Calendar(self)
        self.abilities = [ability.meditation, ability.assertiveness, ability.pos_attitude, ability.opposite_action, ability.catharsis]

        self.guided = False #for outside time or from admissions to common room

    def __repr__(self) -> str:
        return f'{self.name}(character)'

    def build_inv_str_list(self):
        strings = []
        for item in self.inv:
            strings.append(item.name)
        if len(strings) < 6:
            for i in range(6 - len(strings)):
                strings.append("")
        return strings

    def earn_xp(self, amount):
        self.xp += amount
        return "xp_value"

    def gain_health(self, hp):
        self.health += hp
        if hp > 0:
            message = f"You have gained {hp} health."
        else:
            message = f"You have lost {hp} health."
        
        return ("health_value", message)

    def add_inventory(self, item):
        self.inv.append(item)
        return self.build_inv_str_list()

    def sub_inventory(self, item):
        self.inv.remove(item)
        return self.build_inv_str_list()
        
    def full_inv_drop_items(self, choice, item_to_pick_up):
        actions = {
            'print_all': [],
            'build_multiple_choice': []
        }
        if choice.lower() == "y":
            actions['print_all'].append(f"Please choose an item to drop in place of the {item_to_pick_up.name}:")
            actions['build_multiple_choice'] = [[], []]
            for item in self.inv:
                actions['build_multiple_choice'][0].append(item.name)
                actions['build_multiple_choice'][1].append(item)
            actions['build_multiple_choice'][0].append("cancel")
            actions['build_multiple_choice'][1].append("cancel")
            return ("drop_x_for_y", item_to_pick_up, actions)

        else: 
            return (None, None, actions)
            
    def multi_choice_drop_x_for_y(self, item_to_drop, item_to_pick_up):
        #list inv_item, found_item 
        ##expecting y or n 
        actions = {
            'print_all': [],
            'ask_y_or_n': False,
            'update_inv_visual': [],
        }
        if item_to_drop != "cancel":
            return_tuple1 = item_to_drop.drop_item(None, self) 

            item_to_pick_up_loc = None
            for sc in self.loc.storage_containers:
                if item_to_pick_up_loc == None:
                    for tup in sc.build_flat_list_of_contents(True):
                        if tup[0] == item_to_pick_up:
                            item_to_pick_up_loc = tup[1]
                            break
                else:
                    break
            
            return_tuple2 = item_to_pick_up.pick_up_item(self, item_to_pick_up_loc)
            actions = gl.combine_dicts(actions, return_tuple1[2])
            actions = gl.combine_dicts(actions, return_tuple2[2])
            # This solves the problem of two different lists being built and combined
            actions["update_inv_visual"] = self.build_inv_str_list()
            
        else:
            actions['print_all'].append(f"You chose to not pick up the {item_to_pick_up.name}.")

        return (None, None, actions)
    
    def take_damage(self, damage, affect):
        self.health -= damage
        self.condition = affect

    def move_nesw(self, d_choice, next_room):
        #from main - choice: 'n', 's', 'e', 'w'
        #next_room can be list
        actions = {
            'print_all': [],
            'ask_y_or_n': False,
            'build_multiple_choice': [],
            'update_ui_values': []
        }
        invalid_direction = ["You cannot go that way", "There is a wall in that direction", "It is not possible to go that way"]  
        
        if self.guided:
            actions['print_all'].append("You are currently being guided by hospital staff. You cannot move freely.")
            return (None, None, actions)

        if isinstance(next_room, list):
            actions['print_all'].append("Please choose a room below:")

            display_rooms = [] #check for doors too
            for i in range(0, len(next_room)):
                if self.loc.has_doors and self.loc.doors[d_choice][i] != None:
                    if self.loc.doors[d_choice][i].locked:
                        display_rooms.append("Locked Door")
                    else:
                        if next_room[i].visited:
                            display_rooms.append(f"Unlocked Door: {next_room[i].name}")
                        else:
                            display_rooms.append(f"Unlocked Door: Unknown Room")

                elif next_room[i].visited:
                    display_rooms.append(next_room[i].name)
                else:
                    display_rooms.append("Unknown Room")

            actions['build_multiple_choice'] = [display_rooms, next_room]
            return ("move_nesw", [d_choice, next_room], actions)

        if self.loc.has_doors: #also check where doors have already been unlocked
            
            if not isinstance(self.loc.doors[d_choice], list): 
                if self.loc.doors[d_choice] != None: 
                    dest, helper, actions_open_close = self.loc.doors[d_choice].open_item()
                    actions = gl.combine_dicts(actions, actions_open_close)
                    if self.loc.doors[d_choice].open:
                        enter_room_tuple = next_room.enter_room(self)
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)
                    return (dest, helper, actions)
        
                else:
                    if next_room == 0:
                        actions['print_all'].append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        enter_room_tuple = next_room.enter_room(self)
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)
            else:
                possible_rooms = self.loc.check_direction_next_room(d_choice)
                next_room_index = possible_rooms.index(next_room)
                if self.loc.doors[d_choice][next_room_index] != None: 
                    
                    dest, helper, actions_open_close = self.loc.doors[d_choice][next_room_index].open_item()
                    actions = gl.combine_dicts(actions, actions_open_close)
                    if self.loc.doors[d_choice][next_room_index].open:
                        enter_room_tuple = next_room.enter_room(self)
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)
                    return (dest, helper, actions)
        
                else:
                    if next_room == 0:
                        actions['print_all'].append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        enter_room_tuple = next_room.enter_room(self)
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)

        else:
            if next_room == 0:
                actions['print_all'].append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                return (None, None, actions)
            else: 
                enter_room_tuple = next_room.enter_room(self)
                actions = gl.combine_dicts(actions, enter_room_tuple[2])
                return (enter_room_tuple[0], enter_room_tuple[1], actions)

    def build_blrf_dict(self):
        lfrb_cardinality = self.loc.find_positional_rooms(self)[1]

        lfrb_direct_list = ["l", "f", "r", "b"]
        lfrb_dict = {}
        for i in range(0, len(lfrb_cardinality)):
            lfrb_dict[lfrb_direct_list[i]] = lfrb_cardinality[i]

        return lfrb_dict

