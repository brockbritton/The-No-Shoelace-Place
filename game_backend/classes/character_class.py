

import random

import the_no_shoelace_place.classes.room_class as room_class
import the_no_shoelace_place.classes.calendar_class as calendar_class
import the_no_shoelace_place.objects.game_objects.items as item
import the_no_shoelace_place.objects.game_objects.rooms as room
import the_no_shoelace_place.objects.game_objects.abilities as ability


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

        self.calendar = calendar_class.Calendar()
        self.abilities = [ability.catharsis, ability.assertiveness, ability.pos_attitude, ability.meditation, ability.opposite_action]

        self.guided = False #for outside time or from admissions to common room

    def __repr__(self) -> str:
        return f'{self.name}(character)'

    def add_inventory(self, item):
        self.inv.append(item)
        gui_char.update_inv_visual(self)

    def add_inventory_choice(self, choice, item): ##unneeded?
        ##expecting y or n
        if choice.lower() == "y":
            if (len(self.inv) < self.inv_cap):
                gui_char.printtk("You have added a " + item.name + " to your inventory.")
                self.add_inventory(item)
                self.loc.remove_item(item)
                return "main", None
            else:
                gui_char.printtk("")
                gui_char.printtk("Your inventory is full.")
      
                gui_char.printtk("Would you like to remove an item from your inventory to make space for the " + item.name + "?")
                gui_char.ask_y_n()
                return "full_inv_drop_items", item

        elif choice.lower() == "n":
            gui_char.printtk("You did not pick up the " + item.name)
            return "main", None

    def pick_up_item(self, item):
        if (len(self.inv) < self.inv_cap):
            gui_char.printtk("You have added the " + item.name + " to your inventory.")
            self.add_inventory(item)
            self.loc.remove_item(item)
            return "main", None
        else:
            gui_char.printtk("")
            gui_char.printtk("Your inventory is full.")
    
            gui_char.printtk("Would you like to remove an item from your inventory to make space for the " + item.name + "?")
            gui_char.ask_y_n()
            return "full_inv_drop_items", item


    def sub_inventory(self, item):
        self.inv.remove(item)
        gui_char.update_inv_visual(self)

    def drop_item(self, item, loc):
        self.loc.add_item(item, loc)
        self.sub_inventory(item)
        return "main", None

    def check_inventory(self, items_list):
        bool_list = []
        for i in range(0, len(items_list)):
            bool_list.append(False)

        for item in self.inv:
            for o_item in items_list:
                if item.name == o_item.name:
                    index = items_list.index(o_item)
                    bool_list[index] = True 

        return bool_list
                
    def enter_room(self): #####
        self.loc.print_room_name()

        # Setting gui current room
        gui_char.settk(gui_char.ps_curr_room_value, self.loc.name)

        if not self.loc.visited:
            # Updating XP for gui 
            gui_char.printtk(f"New Room Discovered! + {gui_char.xp_dict['new_room']}")
            gui_char.settk(gui_char.xp_value, gui_char.gettk(gui_char.xp_value, 0) + gui_char.xp_dict['new_room'])
            self.loc.visited = True

        if self.loc.lights_on:
            gui_char.printtk("")
            self.loc.print_description()

        if not self.loc.lights_on:
            stumble = random.randint(1,12)
            if stumble == 1:
                self.health -= 5
                if self.health < 0:
                    self.health = 0
                gui_char.printtk("In the dark, you stumbled and fell, scraping your hands on the rough ground.")
                gui_char.printtk("Your health is now at: " + str(self.health)) 

                if self.health <= 0:
                    gui_char.printtk("")
                    return "main", "dead"
            
        if len(self.loc.monsters) != 0:
            
            gui_char.printtk("Look out! There's a " + self.loc.monsters[0].species + "!")
            dest, helper = self.fighting_menu(self.loc.monsters[0])
            return dest, helper

        if isinstance(self.loc, room_class.Basement_Room) and self.loc.lights_on and self.health != 0: 
            dest, helper = self.look_around()
            return dest, helper

        return None, None

    def look_around(self): #####

        if not self.loc.lights_on:
            self.loc.print_description()
            gui_char.printtk("")
        else:
            self.loc.print_items_loc_desc()
        
        if len(self.loc.storage_containers) == 0 and len(self.loc.interacts) == 0:
            gui_char.printtk("There is nothing here...")
            
        
        self.loc.print_directions(self)

        return None, None

    def view_health(self):
        gui_char.printtk("")
        gui_char.printtk("Your current health: " + str(self.health))
        if self.condition == None:
            gui_char.printtk("Your current condition: Healthy")
        else: 
            gui_char.printtk("You current condition: " + self.condition + "ed")

    def check_accuracy(self):
        if self.loc.lights_on:
            return 0
        else: 
            return random.randint(0,3)

    def take_damage(self, damage, affect):
        self.health -= damage
        self.condition = affect

    def take_conditional_damage(self):
        
        chance = random.randint(1, 6)
        if chance == 1:
            if self.condition == "poison":
                self.health -= random.randint(1,4)
                gui_char.printtk("")
                gui_char.printtk("Your poisoning has hurt you.")
                gui_char.printtk("Your health is now at " + str(self.health) + " points")
                gui_char.printtk("")
            elif self.condition == "bleeding":
                self.health -= random.randint(1,6)
                gui_char.printtk("")
                gui_char.printtk("Your bleeding has hurt you.")
                gui_char.printtk("Your health is now at " + str(self.health) + " points.")
                gui_char.printtk("")

    def display_fighting_options(self, flist):
        gui_char.printtk("Combat Options: ") #wrong word?
        gui_char.printtk("")
        for i in range(0, len(flist)): 
            gui_char.printtk("\t" + str(i+1) + ".   " + str(flist[i]))

    def fighting_menu(self, monster): ###### NEEDS WORK #######
        fighting = ["Attack", "Defend", "Heal"]

        if monster.nature == "passive":
            fighting.append("Escape")
            gui_char.printtk("The " + monster.species + " is calmly sitting in the middle of the room")
        elif monster.nature == "aggresive":
            gui_char.printtk("As you enter the room, the " + monster.species + " engages you immediately!")
        
        
        gui_char.printtk("") 
        self.display_fighting_options(fighting)
        if self.condition == None:
            condition = "Healthy"
        else: 
            condition = self.condition

        gui_char.printtk("") 
        gui_char.printtk("Your Health: " + str(self.health) + "\t Your Condition: " + condition)
        gui_char.printtk(monster.species + " Health: " + str(monster.health))

        gui_char.printtk("") 
        gui_char.printtk("Choose a combat action:")
        return "choose_fight_action", [monster, fighting]
    
    def choose_room(self, choice, list):
        #list: d_choice, next_rooms (plural)
        room_index = list[1].index(choice)

        dest, helper = self.move_nesw(list[0], list[1][room_index])
        return dest, helper

    def move_nesw(self, d_choice, next_room):

        #from main - choice: 'n', 's', 'e', 'w'
        #next_room can be list
        
        invalid_direction = ["You cannot go that way", "There is a wall in that direction", "It is not possible to go that way"]  
        
        if self.guided:
            gui_char.printtk("You are currently being guided by hospital staff. You cannot move freely.")
            return None, None

        if isinstance(next_room, list):
            gui_char.printtk("Please choose a room below:")

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

            gui_char.build_multiple_choice(display_rooms, next_room)
            return "choose_room", [d_choice, next_room]

        if self.loc.has_doors: #check where doors have already been unlocked
            
            if not isinstance(self.loc.doors[d_choice], list): 
                if self.loc.doors[d_choice] != None: 
                    
                    dest = self.loc.doors[d_choice].open_close_interact(self, "open")
                    if dest == "open_door":
                        self.last_loc = self.loc
                        self.loc = next_room
                        dest, helper = self.enter_room()
                        return dest, helper
                    return dest, [next_room, d_choice, self.loc.doors[d_choice]]
        
                else:
                    if next_room == 0:
                        gui_char.printtk(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        self.last_loc = self.loc
                        self.loc = next_room
                        dest, helper = self.enter_room()
                        return dest, helper
            else:
                possible_rooms = self.loc.check_direction_next_room(d_choice)
                next_room_index = possible_rooms.index(next_room)
                if self.loc.doors[d_choice][next_room_index] != None: 
                    
                    dest = self.loc.doors[d_choice][next_room_index].open_close_interact(self, "open")
                    if dest == "open_door":
                        self.loc = next_room
                        dest, helper = self.enter_room()
                        return dest, helper
                    return dest, [next_room, d_choice, self.loc.doors[d_choice][next_room_index]]
        
                else:
                    if next_room == 0:
                        gui_char.printtk(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                    else: 
                        self.last_loc = self.loc
                        self.loc = next_room
                        dest, helper = self.enter_room()
                        return dest, helper

        else:
            if next_room == 0:
                gui_char.printtk(invalid_direction[random.randint(0, len(invalid_direction)-1)])
                return "main", None
            else: 
                self.last_loc = self.loc
                self.loc = next_room
                dest, helper = self.enter_room()
                return dest, helper

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
        
        if choice != "y" and choice != "n":
            gui_char.ask_y_n()
            return "drop_gen_item", item
        else: 
            gui_char.printtk("You have dropped the " + item.name)
            self.loc.add_item(item, None)
            self.sub_inventory(item)

            
        return "main", None

    def full_inv_drop_items(self, choice, item):
        ##expecting y or n
        if choice.lower() == "y":
            gui_char.printtk("")
            gui_char.printtk("Would you like to drop " + self.inv[0].name + " for " + item.name + "?")
            gui_char.ask_y_n()
            return "drop_x_for_y", [self.inv[0], item]

        else: 
            return "main", None
            
    def drop_x_for_y(self, choice, list):
        #list inv_item, found_item 
        ##expecting y or n 

        if choice.lower() == "y":
            gui_char.printtk("")
            gui_char.printtk("You have dropped " + list[0].name + " for " + list[1].name)
            
            self.add_inventory(list[1])
            self.loc.remove_item(list[1])
            self.loc.add_item(list[0], None)
            self.sub_inventory(list[0])
            
            return "main", None
        
        elif choice.lower() == "n":
            if self.inv.index(list[0]) + 1 == len(self.inv):
                gui_char.printtk("You didn't drop anything or pick up " + self.loc.items[list[1]].name)
                return "main", None
            else:
                next_item = self.inv[self.inv.index(list[0]) + 1]
    
                gui_char.printtk("")
                gui_char.printtk("Would you like to drop " + next_item.name + " for " + list[1].name + "?")
                gui_char.ask_y_n()
                return "drop_x_for_y", [next_item, list[1]]     

    def inspect_pb(self, choice):
        ##expecting y or n
        if choice.lower() == "y":
            gui_char.printtk("")
            gui_char.printtk("There is a lever attached to the box.")
            gui_char.printtk("There is an instruction label on the box,") 
            gui_char.printtk("but the words have long since faded away.")
            gui_char.printtk("Would you like to pull the lever?")
            gui_char.ask_y_n()
            return "interact_pb"
        elif choice.lower() == "n":
            gui_char.printtk("You did not interact with the power box.")
            return "main"
        else:
            gui_char.ask_y_n()
            return "inspect_pb"
            
    def interact_pb(self, choice):
        #y or n
        if choice.lower() == "y":
            index = self.loc.interacts.index(item.power_box)
            gui_char.printtk("")
            if self.loc.lights_on:
                self.loc.interacts[index].hit_switch()
                gui_char.printtk("You pulled the lever and the room is plunged into darkness.")

            else: 
                self.loc.interacts[index].hit_switch()
                
                gui_char.printtk("You pulled the lever and the bright florescent lights flooded the room.")
            
        elif choice.lower() == "n":
            gui_char.printtk("You did not interact with the power box.")
        
        else:
            gui_char.ask_y_n()
            return "interact_pb"
            
        return "main"

    def inspect_comp(self, choice): #maybe make player have to plug it in
        if choice.lower() == "y":
            gui_char.printtk("")
            gui_char.printtk("There is a heavy layer of dust coating the screen.")
            gui_char.printtk("Upon wiping it away, you notice a power button at the base.")
            gui_char.printtk("Would you like to press the power button?")
            gui_char.ask_y_n()
            return "interact_comp"

        elif choice.lower() == "n":
            gui_char.printtk("You did not interact with the computer.")
            return "main"
        else:
            gui_char.ask_y_n()
            return "inspect_comp"

    def choose_fight_action(self, choice, list): 
        # For battle step one
        pass
    
    def choose_ability(self, monster):
        # For battle
        pass

    def after_heal_combat(self, list):
        #list: state, monster
        damage, affect = list[1].monst_take_turn()
        gui_char.printtk("The " + list[1].species + " dealt " + str(damage) + " damage to you!")
        gui_char.printtk("")
        if affect == "flee":
            return "main", None
        self.take_damage(damage, affect)
        if self.health <= 0: 
            gui_char.printtk("You have died.") #how to end game
            return "main", "dead"

        else: 
            gui_char.printtk("Choose a combat action:")
            return "choose_fight_action", [list[1], ["Attack", "Defend", "Heal"]]

    def deal_take_damage(self, choice, list):
        #return "choose_fight_action", [list[3], ["Attack", "Defend", "Heal"]]
        pass

    def open_door_key(self, choice, list):

        #list: next_room, direction choice, door

        if choice == 'y':
            list[2].locked = False
            list[2].open = True
        elif choice == 'n':
            gui_char.printtk("The door is still locked.")
        else: 
            gui_char.ask_y_n()
            return "open_door_key", list

        dest, helper = self.check_move_through_door(list)
        return dest, helper

    def open_door_crowbar(self, choice, list): 
        #list: next_room, direction choice, door, player
        if choice == 'y':
            list[2].locked = False
            list[2].broken = True
            list[2].open = True
        elif choice == 'n':
            gui_char.printtk("The door is still locked.")
        else:
            gui_char.ask_y_n()
            return "open_door_crowbar", list
        
        dest, helper = self.check_move_through_door(list)
        return dest, helper

    def open_electronic_door(self, choice, list):
        #list: next_room, direction choice, door
        if choice == '1':
            gui_char.printtk("Ready for Code: ")
            list.append(self)
            return "enter_code", list

        elif choice == '2' and item.keycard in self.inv:
            gui_char.printtk("You swiped your keycard and the door opened.")
            list[2].locked = False
            list[2].open = True
            dest, helper = self.check_move_through_door(list)
            return dest, helper

        else:
            gui_char.printtk("Please enter a valid choice.")
            return "open_electronic_door", list

    def check_move_through_door(self, help_list): 
        #list: next_room, direction choice, door
        gui_char.printtk("") 
        print(self.loc.doors)
        if not isinstance(self.loc.doors[help_list[1]], list):
            if self.loc.doors[help_list[1]].open:
                self.last_loc = self.loc
                self.loc = help_list[0]
                dest, helper = self.enter_room()
                return dest, helper

            else:
                gui_char.printtk("Try another way.")
                gui_char.printtk("")
                dest, helper = self.enter_room()
                return dest, helper
        else:
            i = self.loc.doors[help_list[1]].index(help_list[2])
            if self.loc.doors[help_list[1]][i].open:
                self.last_loc = self.loc
                self.loc = help_list[0]
                dest, helper = self.enter_room()
                return dest, helper

            else:
                gui_char.printtk("Try another way.")
                gui_char.printtk("")
                dest, helper = self.enter_room()
                return dest, helper

    def drop_item_choice(self, choice):

            item_index = self.inv.index(choice)
            
            dest, helper = self.drop_item(item_index)
            gui_char.update_inv_visual(self)
            return dest, helper


#general func

def set_char_gui(gui_window):
    global gui_char
    gui_char = gui_window
