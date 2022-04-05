

import random

from pkg_resources import to_filename

import game_backend.classes.room_class as room_class
import game_backend.classes.calendar_class as calendar_class
import game_backend.objects.items as item
import game_backend.objects.rooms as room
import game_backend.objects.abilities as ability


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
        
        to_print = []
        if choice.lower() == "y":
            if (len(self.inv) < self.inv_cap):
                to_print.append("You have added a " + item.name + " to your inventory.")
                self.add_inventory(item)
                self.loc.remove_item(item)
                return (None, None, to_print)
            else:
                 
                to_print.append("Your inventory is full.")
      
                to_print.append("Would you like to remove an item from your inventory to make space for the " + item.name + "?")
                #gui_char.ask_y_n()
                return ("full_inv_drop_items", item, to_print)

        elif choice.lower() == "n":
            to_print.append("You did not pick up the " + item.name)
            return (None, None, to_print)

    def pick_up_item(self, item):
        to_print = []
        if (len(self.inv) < self.inv_cap):
            to_print.append("You have added the " + item.name + " to your inventory.")
            self.add_inventory(item)
            self.loc.remove_item(item)
            return (None, None, to_print)
        else:
             
            to_print.append("Your inventory is full.")
            to_print.append("Would you like to remove an item from your inventory to make space for the " + item.name + "?")
            #gui_char.ask_y_n()
            return ("full_inv_drop_items", item, to_print)


    def sub_inventory(self, item):
        self.inv.remove(item)
        # update the inventory visual

    def drop_item(self, item, loc):
        self.loc.add_item(item, loc)
        self.sub_inventory(item)
        return None, None
                
    def enter_room(self): #####
        to_print = []
        to_print.append(self.loc.print_room_name())

        # Setting gui current room
        #gui_char.settk(gui_char.ps_curr_room_value, self.loc.name)

        if not self.loc.visited:
            # Updating XP for gui 
            #to_print.append(f"New Room Discovered! + {gui_char.xp_dict['new_room']}")
            to_print.append(f"New Room Discovered! + 10xp")
            #gui_char.settk(gui_char.xp_value, gui_char.gettk(gui_char.xp_value, 0) + gui_char.xp_dict['new_room'])
            self.loc.visited = True

        if self.loc.lights_on:
            to_print.append(self.loc.print_description())

        if not self.loc.lights_on:
            stumble = random.randint(1,12)
            if stumble == 1:
                self.health -= 5
                if self.health < 0:
                    self.health = 0
                to_print.append("In the dark, you stumbled and fell, scraping your hands on the rough ground.")
                to_print.append("Your health is now at: " + str(self.health)) 

                if self.health <= 0:
                    return (None, "dead", to_print)
            
        if len(self.loc.monsters) != 0:
            
            to_print.append("Look out! There's a " + self.loc.monsters[0].species + "!")
            #dest, helper = self.fighting_menu(self.loc.monsters[0])
            dest, helper = None, None
            return (dest, helper, to_print)

        if isinstance(self.loc, room_class.Basement_Room) and self.loc.lights_on and self.health != 0: 
            dest, helper = self.look_around()
            return (dest, helper, to_print)

        return (None, None, to_print)

    def look_around(self): #####
        to_print = []
        if not self.loc.lights_on:
            to_print.append(self.loc.print_description())
        else:
            to_print.append(self.loc.print_items_loc_desc())
        
        if len(self.loc.storage_containers) == 0 and len(self.loc.interacts) == 0:
            to_print.append("There is nothing here...")
            
        to_print.append(self.loc.print_directions(self, None))

        return (None, None, to_print)

    def check_accuracy(self):
        if self.loc.lights_on:
            return 0
        else: 
            return random.randint(0,3)

    def take_damage(self, damage, affect):
        self.health -= damage
        self.condition = affect

    def take_conditional_damage(self):
        to_print = []
        chance = random.randint(1, 6)
        if chance == 1:
            if self.condition == "poison":
                self.health -= random.randint(1,4)
                 
                to_print.append("Your poisoning has hurt you.")
                to_print.append("Your health is now at " + str(self.health) + " points")
                 
            elif self.condition == "bleeding":
                self.health -= random.randint(1,6)
                 
                to_print.append("Your bleeding has hurt you.")
                to_print.append("Your health is now at " + str(self.health) + " points.")
            return to_print
                 

    def display_fighting_options(self, flist):
        to_print = []
        to_print.append("Combat Options: ") #wrong word?
         
        for i in range(0, len(flist)): 
            to_print.append("\t" + str(i+1) + ".   " + str(flist[i]))
        return to_print

    def fighting_menu(self, monster): ###### NEEDS WORK #######
        to_print = []
        fighting = ["Attack", "Defend", "Heal"]

        if monster.nature == "passive":
            fighting.append("Escape")
            to_print.append("The " + monster.species + " is calmly sitting in the middle of the room")
        elif monster.nature == "aggresive":
            to_print.append("As you enter the room, the " + monster.species + " engages you immediately!")
        
        self.display_fighting_options(fighting)
        if self.condition == None:
            condition = "Healthy"
        else: 
            condition = self.condition

        to_print.append("Your Health: " + str(self.health) + "\t Your Condition: " + condition)
        to_print.append(monster.species + " Health: " + str(monster.health))

          
        to_print.append("Choose a combat action:")
        return ("choose_fight_action", [monster, fighting], to_print)
    
    def choose_room(self, choice, list):
        #list: d_choice, next_rooms (plural)
        room_index = list[1].index(choice)

        dest, helper = self.move_nesw(list[0], list[1][room_index])
        return dest, helper

    def move_nesw(self, d_choice, next_room):

        #from main - choice: 'n', 's', 'e', 'w'
        #next_room can be list
        to_print = []
        invalid_direction = ["You cannot go that way", "There is a wall in that direction", "It is not possible to go that way"]  
        
        if self.guided:
            to_print.append("You are currently being guided by hospital staff. You cannot move freely.")
            return (None, None, to_print)

        if isinstance(next_room, list):
            to_print.append("Please choose a room below:")

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

            #gui_char.build_multiple_choice(display_rooms, next_room)
            return ("choose_room", [d_choice, next_room], to_print)

        if self.loc.has_doors: #check where doors have already been unlocked
            
            if not isinstance(self.loc.doors[d_choice], list): 
                if self.loc.doors[d_choice] != None: 
                    
                    dest = self.loc.doors[d_choice].open_close_interact(self, "open")
                    if dest == "open_door":
                        self.last_loc = self.loc
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        return (enter_room_tuple[0], enter_room_tuple[1], to_print.extend(enter_room_tuple[2]))
                    return (dest, [next_room, d_choice, self.loc.doors[d_choice]], to_print)
        
                else:
                    if next_room == 0:
                        to_print.append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        self.last_loc = self.loc
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        return (enter_room_tuple[0], enter_room_tuple[1], to_print.extend(enter_room_tuple[2]))
            else:
                possible_rooms = self.loc.check_direction_next_room(d_choice)
                next_room_index = possible_rooms.index(next_room)
                if self.loc.doors[d_choice][next_room_index] != None: 
                    
                    dest = self.loc.doors[d_choice][next_room_index].open_close_interact(self, "open")
                    if dest == "open_door":
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        return (enter_room_tuple[0], enter_room_tuple[1], to_print.extend(enter_room_tuple[2]))
                    return (dest, [next_room, d_choice, self.loc.doors[d_choice][next_room_index]], to_print)
        
                else:
                    if next_room == 0:
                        to_print.append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        self.last_loc = self.loc
                        self.loc = next_room
                        enter_room_tuple = self.enter_room()
                        return (enter_room_tuple[0], enter_room_tuple[1], to_print.extend(enter_room_tuple[2]))

        else:
            if next_room == 0:
                to_print.append(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                return (None, None, to_print)
            else: 
                self.last_loc = self.loc
                self.loc = next_room
                enter_room_tuple = self.enter_room()
                return (enter_room_tuple[0], enter_room_tuple[1], to_print.extend(enter_room_tuple[2]))

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
        to_print = []
        to_print.append("You have dropped the " + item.name)
        self.loc.add_item(item, None)
        self.sub_inventory(item)

        return (None, None, to_print)

    def full_inv_drop_items(self, choice, item):
        ##expecting y or n
        to_print = []
        if choice.lower() == "y":
            to_print.append("Would you like to drop " + self.inv[0].name + " for " + item.name + "?")
            #gui_char.ask_y_n()
            return ("drop_x_for_y", [self.inv[0], item], to_print)

        else: 
            return (None, None, to_print)
            
    def drop_x_for_y(self, choice, list):
        #list inv_item, found_item 
        ##expecting y or n 
        to_print = []
        if choice.lower() == "y":
             
            to_print.append("You have dropped " + list[0].name + " for " + list[1].name)
            
            self.add_inventory(list[1])
            self.loc.remove_item(list[1])
            self.loc.add_item(list[0], None)
            self.sub_inventory(list[0])
            
            return (None, None, to_print)
        
        elif choice.lower() == "n":
            if self.inv.index(list[0]) + 1 == len(self.inv):
                to_print.append("You didn't drop anything or pick up " + self.loc.items[list[1]].name)
                return (None, None, to_print)
            else:
                next_item = self.inv[self.inv.index(list[0]) + 1]
    
                to_print.append("Would you like to drop " + next_item.name + " for " + list[1].name + "?")
                #gui_char.ask_y_n()
                return ("drop_x_for_y", [next_item, list[1]], to_print)     

    def inspect_pb(self, choice):
        ##expecting y or n
        to_print = []
        if choice.lower() == "y":
            to_print.append("There is a lever attached to the box.")
            to_print.append("There is an instruction label on the box,") 
            to_print.append("but the words have long since faded away.")
            to_print.append("Would you like to pull the lever?")
            #gui_char.ask_y_n()
            return ("interact_pb", None, to_print)
        elif choice.lower() == "n":
            to_print.append("You did not interact with the power box.")
            return (None, None, to_print)
        else:
            #gui_char.ask_y_n()
            return ("inspect_pb", None, to_print)
            
    def interact_pb(self, choice):
        #y or n
        to_print = []
        if choice.lower() == "y":
            index = self.loc.interacts.index(item.power_box)
             
            if self.loc.lights_on:
                self.loc.interacts[index].hit_switch()
                to_print.append("You pulled the lever and the room is plunged into darkness.")

            else: 
                self.loc.interacts[index].hit_switch()
                
                to_print.append("You pulled the lever and the bright florescent lights flooded the room.")
            
        elif choice.lower() == "n":
            to_print.append("You did not interact with the power box.")
        
        else:
            #gui_char.ask_y_n()
            return ("interact_pb", None, to_print)
            
        return (None, None, to_print)

    def inspect_comp(self, choice): #maybe make player have to plug it in
        to_print = []
        if choice.lower() == "y":
            to_print.append("There is a heavy layer of dust coating the screen.")
            to_print.append("Upon wiping it away, you notice a power button at the base.")
            to_print.append("Would you like to press the power button?")
            #gui_char.ask_y_n()
            return ("interact_comp", None, to_print)

        elif choice.lower() == "n":
            to_print.append("You did not interact with the computer.")
            return (None, None, to_print)
        else:
            #gui_char.ask_y_n()
            return ("inspect_comp", None, to_print)

    def choose_fight_action(self, choice, list): 
        # For battle step one
        pass
    
    def choose_ability(self, monster):
        # For battle
        pass

    def after_heal_combat(self, list):
        #list: state, monster
        to_print = []
        damage, affect = list[1].monst_take_turn()
        to_print.append("The " + list[1].species + " dealt " + str(damage) + " damage to you!")
         
        if affect == "flee":
            return (None, None, to_print)
        self.take_damage(damage, affect)
        
        if self.health <= 0: 
            to_print.append("You have died.") #how to end game
            return (None, "dead", to_print)

        else: 
            to_print.append("Choose a combat action:")
            return ("choose_fight_action", [list[1], ["Attack", "Defend", "Heal"]], to_print)

    def deal_take_damage(self, choice, list):
        #return "choose_fight_action", [list[3], ["Attack", "Defend", "Heal"]]
        pass

    def open_door_key(self, choice, list):

        #list: next_room, direction choice, door
        to_print = []
        if choice == 'y':
            list[2].locked = False
            list[2].open = True
        elif choice == 'n':
            to_print.append("The door is still locked.")
        else: 
            #gui_char.ask_y_n()
            return ("open_door_key", list, to_print)

        return_tuple = self.check_move_through_door(list)
        return (return_tuple[0], return_tuple[1], to_print.extend(return_tuple[2]))

    def open_door_crowbar(self, choice, list): 
        #list: next_room, direction choice, door, player
        to_print = []
        if choice == 'y':
            list[2].locked = False
            list[2].broken = True
            list[2].open = True
        elif choice == 'n':
            to_print.append("The door is still locked.")
        else:
            #gui_char.ask_y_n()
            return ("open_door_crowbar", list, to_print)
        
        return_tuple = self.check_move_through_door(list)
        return (return_tuple[0], return_tuple[1], to_print.extend(return_tuple[2]))

    def open_electronic_door(self, choice, list):
        #list: next_room, direction choice, door
        to_print = []
        if choice == '1':
            to_print.append("Ready for Code: ")
            list.append(self)
            return ("enter_code", list, to_print)

        elif choice == '2' and item.keycard in self.inv:
            to_print.append("You swiped your keycard and the door opened.")
            list[2].locked = False
            list[2].open = True
            return_tuple = self.check_move_through_door(list)
            return (return_tuple[0], return_tuple[1], to_print.extend(return_tuple[2]))

        else:
            to_print.append("Please enter a valid choice.")
            return ("open_electronic_door", list, to_print)

    def check_move_through_door(self, help_list): 
        #list: next_room, direction choice, door
          
        print(self.loc.doors)
        to_print = []
        if not isinstance(self.loc.doors[help_list[1]], list):
            if self.loc.doors[help_list[1]].open:
                self.last_loc = self.loc
                self.loc = help_list[0]
                return_tuple = self.enter_room()
                return return_tuple

            else:
                to_print.append("Try another way.")
                return_tuple = self.enter_room()
                return (return_tuple[0], return_tuple[1], to_print.extend(return_tuple[2]))
        else:
            i = self.loc.doors[help_list[1]].index(help_list[2])
            if self.loc.doors[help_list[1]][i].open:
                self.last_loc = self.loc
                self.loc = help_list[0]
                return_tuple = self.enter_room()
                return (return_tuple[0], return_tuple[1], to_print.extend(return_tuple[2]))

            else:
                to_print.append("Try another way.")
                return_tuple = self.enter_room()
                return (return_tuple[0], return_tuple[1], to_print.extend(return_tuple[2]))

    def drop_item_choice(self, choice):
            item_index = self.inv.index(choice)
            dest, helper = self.drop_item(item_index, None)
            #gui_char.update_inv_visual(self)
            return dest, helper

