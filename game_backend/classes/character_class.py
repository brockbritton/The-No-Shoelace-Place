

import random

import game_backend.classes.room_class as room_class
import game_backend.classes.calendar_class as calendar_class
import game_backend.objects.items as item
import game_backend.objects.rooms as room
import game_backend.objects.abilities as ability
import game_backend.gl_backend_functions as gl



class Character:

    def __init__(self, name) -> None:
        self.name = name
        self.loc = room.common_room #starting location
        self.last_loc = None

        self.inv = [item.id_bracelet, item.basement_key, item.crowbar, item.keycard]
        #self.inv = []
        self.inv_cap = 6 #current inventory capacity - maybe just keep it set
        self.inv_cap_start = 6 #starting inventory capacity

        self.health = 65 #starting / current player health
        self.full_health = 100 #starting player health
        self.condition = None

        #self.calendar = calendar_class.Calendar()
        #self.abilities = [ability.catharsis, ability.assertiveness, ability.pos_attitude, ability.meditation, ability.opposite_action]

        self.guided = False #for outside time or from admissions to common room

    def __repr__(self) -> str:
        return f'{self.name}(character)'

    def add_inventory(self, item):
        self.inv.append(item)
        #update the inventory visual

    def add_inventory_choice(self, choice, item): ##unneeded?
        
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice.lower() == "y":
            if (len(self.inv) < self.inv_cap):
                actions['print_all'].append("You have added a " + item.name + " to your inventory.")
                self.add_inventory(item)
                self.loc.remove_item(item)
                return (None, None, actions)
            else:
                 
                actions['print_all'].append("Your inventory is full.")
      
                actions['print_all'].append("Would you like to remove an item from your inventory to make space for the " + item.name + "?")
                actions['ask_y_or_n'] = True
                return ("full_inv_drop_items", item, actions)

        elif choice.lower() == "n":
            actions['print_all'].append("You did not pick up the " + item.name)
            return (None, None, actions)

    def pick_up_item(self, item):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if (len(self.inv) < self.inv_cap):
            actions['print_all'].append("You have added the " + item.name + " to your inventory.")
            self.add_inventory(item)
            self.loc.remove_item(item)
            return (None, None, actions)
        else:
             
            actions['print_all'].append("Your inventory is full.")
            actions['print_all'].append("Would you like to remove an item from your inventory to make space for the " + item.name + "?")
            actions['ask_y_or_n'] = True
            return ("full_inv_drop_items", item, actions)


    def sub_inventory(self, item):
        self.inv.remove(item)
        # update the inventory visual

    def drop_item(self, item, loc):
        self.loc.add_item(item, loc)
        self.sub_inventory(item)
        return None, None
                
    def enter_room(self): #####
        actions = {
            'print_all': [],
        }
        actions['print_all'].append(self.loc.print_room_name())

        # Setting gui current room
        #gui_char.settk(gui_char.ps_curr_room_value, self.loc.name)

        if not self.loc.visited:
            # Updating XP for gui 
            #actions['print_all'].append(f"New Room Discovered! + {gui_char.xp_dict['new_room']}")
            actions['print_all'].append(f"New Room Discovered! + 10xp")
            #gui_char.settk(gui_char.xp_value, gui_char.gettk(gui_char.xp_value, 0) + gui_char.xp_dict['new_room'])
            self.loc.visited = True

        if self.loc.lights_on:
            actions['print_all'].append(self.loc.print_description())

        if not self.loc.lights_on:
            stumble = random.randint(1,12)
            if stumble == 1:
                self.health -= 5
                if self.health < 0:
                    self.health = 0
                actions['print_all'].append("In the dark, you stumbled and fell, scraping your hands on the rough ground.")
                actions['print_all'].append("Your health is now at: " + str(self.health)) 

                if self.health <= 0:
                    return (None, "dead", actions)
            
        if len(self.loc.monsters) != 0:
            
            actions['print_all'].append("Look out! There's a " + self.loc.monsters[0].species + "!")
            #dest, helper = self.fighting_menu(self.loc.monsters[0])
            dest, helper = None, None
            return (dest, helper, actions)

        if isinstance(self.loc, room_class.Basement_Room) and self.loc.lights_on and self.health != 0: 
            dest, helper = self.look_around()
            return (dest, helper, actions)

        return (None, None, actions)

    def look_around(self): #####
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if not self.loc.lights_on:
            actions['print_all'].append(self.loc.print_description())
        else:
            actions['print_all'].append(self.loc.print_items_loc_desc())
        
        if len(self.loc.storage_containers) == 0 and len(self.loc.interacts) == 0:
            actions['print_all'].append("There is nothing here...")
            
        actions['print_all'].append(self.loc.print_directions(self, None))

        return (None, None, actions)

    def check_accuracy(self):
        if self.loc.lights_on:
            return 0
        else: 
            return random.randint(0,3)

    def take_damage(self, damage, affect):
        self.health -= damage
        self.condition = affect

    def take_conditional_damage(self):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        chance = random.randint(1, 6)
        if chance == 1:
            if self.condition == "poison":
                self.health -= random.randint(1,4)
                 
                actions['print_all'].append("Your poisoning has hurt you.")
                actions['print_all'].append("Your health is now at " + str(self.health) + " points")
                 
            elif self.condition == "bleeding":
                self.health -= random.randint(1,6)
                 
                actions['print_all'].append("Your bleeding has hurt you.")
                actions['print_all'].append("Your health is now at " + str(self.health) + " points.")
            return actions['print_all']
                 

    def display_fighting_options(self, flist):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        actions['print_all'].append("Combat Options: ") #wrong word?
         
        for i in range(0, len(flist)): 
            actions['print_all'].append("\t" + str(i+1) + ".   " + str(flist[i]))
        return actions['print_all']

    def fighting_menu(self, monster): ###### NEEDS WORK #######
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        fighting = ["Attack", "Defend", "Heal"]

        if monster.nature == "passive":
            fighting.append("Escape")
            actions['print_all'].append("The " + monster.species + " is calmly sitting in the middle of the room")
        elif monster.nature == "aggresive":
            actions['print_all'].append("As you enter the room, the " + monster.species + " engages you immediately!")
        
        self.display_fighting_options(fighting)
        if self.condition == None:
            condition = "Healthy"
        else: 
            condition = self.condition

        actions['print_all'].append("Your Health: " + str(self.health) + "\t Your Condition: " + condition)
        actions['print_all'].append(monster.species + " Health: " + str(monster.health))

          
        actions['print_all'].append("Choose a combat action:")
        return ("choose_fight_action", [monster, fighting], actions)
    
    def choose_room(self, choice, list):
        #list: d_choice, next_rooms (plural)
        room_index = list[1].index(choice)

        dest, helper = self.move_nesw(list[0], list[1][room_index])
        return dest, helper

    def move_nesw(self, d_choice, next_room):
        #from main - choice: 'n', 's', 'e', 'w'
        #next_room can be list
        actions = {
            'print_all': [],
            'ask_y_or_n': False
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
                        display_rooms.append(next_room[i].name)

                elif next_room[i].visited:
                    display_rooms.append(next_room[i].name)
                else:
                    display_rooms.append("Unknown Room")

            actions['build_multiple_choice'] = (display_rooms, next_room)
            return ("choose_room", [d_choice, next_room], actions)

        if self.loc.has_doors: #check where doors have already been unlocked
            
            if not isinstance(self.loc.doors[d_choice], list): 
                if self.loc.doors[d_choice] != None: 
                    
                    dest = self.loc.doors[d_choice].open_close_interact(self, "open")
                    if dest == "open_door":
                        self.last_loc = self.loc
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)
                    return (dest, [next_room, d_choice, self.loc.doors[d_choice]], actions)
        
                else:
                    if next_room == 0:
                        actions['print_all'].append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        self.last_loc = self.loc
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)
            else:
                possible_rooms = self.loc.check_direction_next_room(d_choice)
                next_room_index = possible_rooms.index(next_room)
                if self.loc.doors[d_choice][next_room_index] != None: 
                    
                    dest = self.loc.doors[d_choice][next_room_index].open_close_interact(self, "open")
                    if dest == "open_door":
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)
                    return (dest, [next_room, d_choice, self.loc.doors[d_choice][next_room_index]], actions)
        
                else:
                    if next_room == 0:
                        actions['print_all'].append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        self.last_loc = self.loc
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        actions = gl.combine_dicts(actions, enter_room_tuple[2])
                        return (enter_room_tuple[0], enter_room_tuple[1], actions)

        else:
            if next_room == 0:
                actions['print_all'].append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                return (None, None, actions)
            else: 
                self.last_loc = self.loc
                self.loc = next_room
                enter_room_tuple = self.enter_room()
                actions = gl.combine_dicts(actions, enter_room_tuple[2])
                return (enter_room_tuple[0], enter_room_tuple[1], actions)

    def check_blrf_directions(self):
        rooms_list = [self.loc.north, self.loc.east, self.loc.south, self.loc.west]
        direct_list = ["n", "e", "s", "w"]
        if self.last_loc == None:
            print("Last Location M: None")
        else: 
            print("Last Location M:", self.last_loc.name)
        
        if self.last_loc != None:
            for r in rooms_list:
                    if isinstance(r, list):
                        for x in r:
                            if x == self.last_loc:
                                last_room_index = rooms_list.index(r)
                                #second = r.index(x)
                                #issue because its two indexes?
                    elif r == self.last_loc:
                        last_room_index = rooms_list.index(r)

                    #can also be 0 - for wall     
            
            nesw_direct_list = []

            nesw_direct_list.append(direct_list[last_room_index]) #back

            if last_room_index + 1 > 3: #left
                nesw_direct_list.append(direct_list[0])
            else:
                nesw_direct_list.append(direct_list[last_room_index + 1])

            
            if last_room_index - 1 < 0: #right
                nesw_direct_list.append(direct_list[3])
            else:
                nesw_direct_list.append(direct_list[last_room_index - 1])

            if last_room_index + 2 > 3: #forward
                nesw_direct_list.append(direct_list[last_room_index - 2])
            else:
                nesw_direct_list.append(direct_list[last_room_index + 2])

        else: 
            nesw_direct_list = ["n", "e", "w", "s"]
            last_room_index = 0

        blrf_direct_list = ["b", "l", "r", "f"]
        blrf_dict = {}
        for i in range(0, len(direct_list)):
            blrf_dict[blrf_direct_list[i]] = nesw_direct_list[i]
        return blrf_dict

    

    def drop_gen_item(self, choice, item):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        actions['print_all'].append("You have dropped the " + item.name)
        self.loc.add_item(item, None)
        self.sub_inventory(item)

        return (None, None, actions)

    def full_inv_drop_items(self, choice, item):
        ##expecting y or n
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice.lower() == "y":
            actions['print_all'].append("Would you like to drop " + self.inv[0].name + " for " + item.name + "?")
            actions['ask_y_or_n'] = True
            return ("drop_x_for_y", [self.inv[0], item], actions)

        else: 
            return (None, None, actions)
            
    def drop_x_for_y(self, choice, list):
        #list inv_item, found_item 
        ##expecting y or n 
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice.lower() == "y":
             
            actions['print_all'].append("You have dropped " + list[0].name + " for " + list[1].name)
            
            self.add_inventory(list[1])
            self.loc.remove_item(list[1])
            self.loc.add_item(list[0], None)
            self.sub_inventory(list[0])
            
            return (None, None, actions)
        
        elif choice.lower() == "n":
            if self.inv.index(list[0]) + 1 == len(self.inv):
                actions['print_all'].append("You didn't drop anything or pick up " + self.loc.items[list[1]].name)
                return (None, None, actions)
            else:
                next_item = self.inv[self.inv.index(list[0]) + 1]
    
                actions['print_all'].append("Would you like to drop " + next_item.name + " for " + list[1].name + "?")
                actions['ask_y_or_n'] = True
                return ("drop_x_for_y", [next_item, list[1]], actions)     

    def inspect_pb(self, choice):
        ##expecting y or n
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice.lower() == "y":
            actions['print_all'].append("There is a lever attached to the box.")
            actions['print_all'].append("There is an instruction label on the box,") 
            actions['print_all'].append("but the words have long since faded away.")
            actions['print_all'].append("Would you like to pull the lever?")
            actions['ask_y_or_n'] = True
            return ("interact_pb", None, actions)
        elif choice.lower() == "n":
            actions['print_all'].append("You did not interact with the power box.")
            return (None, None, actions)
        else:
            actions['ask_y_or_n'] = True
            return ("inspect_pb", None, actions)
            
    def interact_pb(self, choice):
        #y or n
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice.lower() == "y":
            index = self.loc.interacts.index(item.power_box)
             
            if self.loc.lights_on:
                self.loc.interacts[index].hit_switch()
                actions['print_all'].append("You pulled the lever and the room is plunged into darkness.")

            else: 
                self.loc.interacts[index].hit_switch()
                
                actions['print_all'].append("You pulled the lever and the bright florescent lights flooded the room.")
            
        elif choice.lower() == "n":
            actions['print_all'].append("You did not interact with the power box.")
        
        else:
            actions['ask_y_or_n'] = True
            return ("interact_pb", None, actions)
            
        return (None, None, actions)

    def inspect_comp(self, choice): #maybe make player have to plug it in
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice.lower() == "y":
            actions['print_all'].append("There is a heavy layer of dust coating the screen.")
            actions['print_all'].append("Upon wiping it away, you notice a power button at the base.")
            actions['print_all'].append("Would you like to press the power button?")
            actions['ask_y_or_n'] = True
            return ("interact_comp", None, actions)

        elif choice.lower() == "n":
            actions['print_all'].append("You did not interact with the computer.")
            return (None, None, actions)
        else:
            actions['ask_y_or_n'] = True
            return ("inspect_comp", None, actions)

    def choose_fight_action(self, choice, list): 
        # For battle step one
        pass
    
    def choose_ability(self, monster):
        # For battle
        pass

    def after_heal_combat(self, list):
        #list: state, monster
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        damage, affect = list[1].monst_take_turn()
        actions['print_all'].append("The " + list[1].species + " dealt " + str(damage) + " damage to you!")
         
        if affect == "flee":
            return (None, None, actions)
        self.take_damage(damage, affect)
        
        if self.health <= 0: 
            actions['print_all'].append("You have died.") #how to end game
            return (None, "dead", actions)

        else: 
            actions['print_all'].append("Choose a combat action:")
            return ("choose_fight_action", [list[1], ["Attack", "Defend", "Heal"]], actions)

    def deal_take_damage(self, choice, list):
        #return "choose_fight_action", [list[3], ["Attack", "Defend", "Heal"]]
        pass

    def open_door_key(self, choice, list):

        #list: next_room, direction choice, door
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice == 'y':
            list[2].locked = False
            list[2].open = True
        elif choice == 'n':
            actions['print_all'].append("The door is still locked.")
        else: 
            #gui_char.ask_y_n()
            return ("open_door_key", list, actions)

        return_tuple = self.check_move_through_door(list)
        return (return_tuple[0], return_tuple[1], actions['print_all'].extend(return_tuple[2]))

    def open_door_crowbar(self, choice, list): 
        #list: next_room, direction choice, door, player
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice == 'y':
            list[2].locked = False
            list[2].broken = True
            list[2].open = True
        elif choice == 'n':
            actions['print_all'].append("The door is still locked.")
        else:
            actions['ask_y_or_n'] = True
            return ("open_door_crowbar", list, actions)
        
        return_tuple = self.check_move_through_door(list)
        return (return_tuple[0], return_tuple[1], actions['print_all'].extend(return_tuple[2]))

    def open_electronic_door(self, choice, list):
        #list: next_room, direction choice, door
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if choice == '1':
            actions['print_all'].append("Ready for Code: ")
            list.append(self)
            return ("enter_code", list, actions)

        elif choice == '2' and item.keycard in self.inv:
            actions['print_all'].append("You swiped your keycard and the door opened.")
            list[2].locked = False
            list[2].open = True
            return_tuple = self.check_move_through_door(list)
            return (return_tuple[0], return_tuple[1], actions['print_all'].extend(return_tuple[2]))

        else:
            actions['print_all'].append("Please enter a valid choice.")
            return ("open_electronic_door", list, actions)

    def check_move_through_door(self, help_list): 
        #list: next_room, direction choice, door
          
        print(self.loc.doors)
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if not isinstance(self.loc.doors[help_list[1]], list):
            if self.loc.doors[help_list[1]].open:
                self.last_loc = self.loc
                self.loc = help_list[0]
                return_tuple = self.enter_room()
                return return_tuple

            else:
                actions['print_all'].append("Try another way.")
                return_tuple = self.enter_room()
                return (return_tuple[0], return_tuple[1], actions['print_all'].extend(return_tuple[2]))
        else:
            i = self.loc.doors[help_list[1]].index(help_list[2])
            if self.loc.doors[help_list[1]][i].open:
                self.last_loc = self.loc
                self.loc = help_list[0]
                return_tuple = self.enter_room()
                return (return_tuple[0], return_tuple[1], actions['print_all'].extend(return_tuple[2]))

            else:
                actions['print_all'].append("Try another way.")
                return_tuple = self.enter_room()
                return (return_tuple[0], return_tuple[1], actions['print_all'].extend(return_tuple[2]))

    def drop_item_choice(self, choice):
            item_index = self.inv.index(choice)
            dest, helper = self.drop_item(item_index, None)
            #gui_char.update_inv_visual(self)
            return dest, helper

