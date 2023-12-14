
import game_backend.classes.room_class as room_class
import game_backend.gl_backend_functions as gl


class Item:
    def __init__(self, name, gen_name) -> None:
        self.name = name
        self.gen_name = gen_name
        self.article = "the"
        self.can_hang = False
        self.item_actions = {
            'help' : self.show_all_actions,
            'inspect': self.inspect_item,
        }
    
    def show_all_actions(self):
        actions = {
            'print_all': [],
        }

        actions['print_all'].append(f"Available actions for this {self.gen_name}:")
        for key in self.item_actions:
            actions['print_all'].append(f"- {key}")

        return actions

    def inspect_item(self): 
        actions = {
            'print_all': [],
        }

        actions['print_all'].append(f"There does not appear to be anything special about this {self.gen_name}.")
        return actions
            

class Multi_Name_Item(Item):
    def __init__(self, name, gen_name, alternate_names) -> None:
        super().__init__(name, gen_name)
        self.alt_names = alternate_names 


#########################
#### Inventory Items #### 
#########################
    
class Inv_Item(Item):

    # name - visible name of item  !!!! must be 17 characters or less !!!!

    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.inv_space = 1
        self.article = "a"
        self.item_actions.update({
            'inspect': self.inspect_item,
            'pick up': self.pick_up_item,
            'drop': self.drop_item,
        })

    def __repr__(self) -> str:
        return f'{self.name}(basic)'

    def pick_up_item(self, player):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if self not in player.inv:
            if (len(player.inv) < player.inv_cap):               
                all_items_complex = []
                for base_storage in player.loc.storage_tree:
                    all_items_complex.extend(base_storage.build_contained_list(True))
                
                for item_loc in all_items_complex:
                    if isinstance(item_loc, tuple) and item_loc[0] == self:
                        item_loc[1].items.remove(self)
                        player.add_inventory(self)
                        actions['print_all'].append(f"You have taken the {item_loc[0].name} from the {item_loc[1].name} and added it to your inventory.")
                        return (None, None, actions)
                    
                actions['print_all'].append(f"You did not match anything ***")
                return (None, None, actions)
            else:
                actions['print_all'].append("Your inventory is full.")
                actions['print_all'].append("Would you like to remove an item from your inventory to make space for the " + self.name + "?")
                actions['ask_y_or_n'] = True
                return ("full_inv_drop_items", self, actions)
        else:
            actions['print_all'].append("You are already holding this item.")
            return (None, None, actions)

    def drop_item(self, loc, player):
        actions = {}
        if self in player.inv:
            player.sub_inventory(self)
            player.loc.add_item(self, loc)
            try:
                actions['print_all'] = [f"You have dropped the {self.name} to the {loc.name}."] 
            except AttributeError:
                # If the item is dropped with no location, it is dropped on the ground
                actions['print_all'] = [f"You have dropped the {self.name} on the ground."]
        else:
            actions['print_all'].append("You cannot drop this item because you are not holding it.") 
        return (None, None, actions)

    def move_item(self, new_location, player):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        for sc in player.loc.storage_containers:
            if self in sc.items:
                last_location = sc
                sc.items.remove(self)

        player.loc.add_item(self, new_location)
        if last_location != new_location:
            actions['print_all'] = [f"You have moved the {self.name} from the {last_location.name} to the {new_location.name}."] 
        else:
            actions['print_all'] = [f"The {self.name} is already on the {new_location.name}."] 
        return (None, None, actions)

class Quote_Note(Inv_Item):
    def __init__(self, name, gen_name, lines_list, author) -> None:
        super().__init__(name, gen_name)
        self.quote = lines_list
        self.author = author
    
    def format_quote(self):
        formatted_quote = []
        # length of text box: 52 characters
        for line in self.quote:
            formatted_quote.append([line, "quote"])
        
        formatted_quote.append([self.author, "quote"])
        return formatted_quote

    def inspect_item(self):
        actions = {
            'print_all': [],
        }
        actions["print_all"].append(f"The {self.gen_name} reads:")
        actions["print_all"].extend(self.format_quote()) 
        return actions 

class Hanging_Quote_Note(Quote_Note):
    def __init__(self, name, gen_name, lines_list, author) -> None:
        super().__init__(name, gen_name, lines_list, author)
        self.can_hang = True
        
        
###################
#### Interacts #### 
###################

class Interact(Item):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        
    def __repr__(self) -> str:
        return f'{self.name}(interact)'

class Openable_Interact(Interact):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.open = False
        self.item_actions.update({
            'open': self.open_item,
            'close': self.close_item,
        })

    def inspect_item(self): 
        actions = {
            'print_all': [],
        }
        
        if self.open:
            if len(self.items) == 0:
                sentence = f"There is nothing in the {self.name}."
            elif len(self.items) == 1:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}."
            elif len(self.items) == 2:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name} and {self.items[1].article} {self.items[1].name}."
            else:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}, "
                for i in range(1, len(self.items)-1):
                    sentence += f"{self.items[i].article} {self.items[i].name}, "
                sentence += f"and {self.items[-1].article} {self.items[-1].name}."

            actions['print_all'].append(sentence)
        else:
            actions['print_all'].append(f"The {self.name} is closed.")
        return actions 


    def open_item(self):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }

        if self.open:
            actions['print_all'].append(f"The {self.name} is already open.")
        else:
            actions['print_all'].append(f"You have opened the {self.name}.")
            self.open = True

        return (None, None, actions)

    def close_item(self): 
        
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }

        if self.open:
            actions['print_all'].append(f"You have closed the {self.name}.")
            self.open = False
        else:
            actions['print_all'].append(f"The {self.name} is already closed.")
        
        return (None, None, actions)
        
class Lockable_Interact(Openable_Interact):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name)
        self.locked = True
        self.broken = False
        if keys_list == None:
            self.compatible_keys = []
        else:
            self.compatible_keys = keys_list 
        self.key_unlock = True
        self.crowbar_unlock = True
        self.electronic_unlock = False 
        self.item_actions.update({
            'lock': self.lock_item,
            'unlock': self.unlock_item,
            'break': self.break_lock,
        })

    
    def unlock_item(self, player):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        if self.locked:
            unlocking_item = None
            crowbar_item = None
            for item in player.inv:
                if isinstance(item, Key):
                    if item in self.compatible_keys or item.name == "master key":
                        unlocking_item = item
                        break
                elif isinstance(item, Crowbar):
                    crowbar_item = item

            # Keep this after the loop because there may be a key in inv after crowbar
            if unlocking_item == None and self.crowbar_unlock and crowbar_item != None:
                actions['print_all'].append(f"You do not have anything that can unlock this item. Alternatively you could use your {crowbar_item.name} to break this {self.gen_name}. If you do so, you will be unable to lock {self.name} again.")
                return actions
            
            if unlocking_item != None:
                actions['print_all'].append(f"You have unlocked the {self.name} with the {unlocking_item.name}.")
                self.locked = False
            else:
                actions['print_all'].append(f"You do not have anything that can unlock the {self.name}.")
        else:
            actions['print_all'].append(f"The {self.name} is already unlocked.")

        return actions

    def lock_item(self, player):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        if not self.broken:
            if not self.locked:
                locking_item = None
                for item in player.inv:
                    if isinstance(item, Key):
                        if item in self.compatible_keys or item.name == "master key":
                            locking_item = item
                            break

                if locking_item != None:
                    if self.open:
                        actions['print_all'].append(f"You have closed and locked the {self.name} with the {locking_item.name}.")
                        self.open = False
                    else:
                        actions['print_all'].append(f"You have locked the {self.name} with the {locking_item.name}.")
                    self.locked = True
                else:
                    actions['print_all'].append(f"You do not have anything that can lock the {self.name}.")
                
            else:
                actions['print_all'].append(f"The {self.name} is already locked.")
        else:
            actions['print_all'].append(f"The lock on the {self.name} is broken. You cannot lock this {self.gen_name} anymore.")

        return actions

    def break_lock(self, player):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }

        for item in player.inv:
            if isinstance(item, Crowbar):
                if not self.broken:
                    actions["print_all"].append(f"You have broken the lock on the {self.name}, therefore permanently unlocking it.")
                    self.broken = True
                    self.locked = False
                else:
                    actions["print_all"].append(f"The lock is already broken on this {self.gen_name}. You cannot break it again.")
                return actions
        
        actions["print_all"].append(f"You do not have anything that can break this {self.gen_name}.")   
        return actions


    def open_item(self): 
        dest, helper = None, None
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }

        if self.locked:
            actions['print_all'].append(f"The {self.name} is locked.")

        else:
            return super().open_item()

        return (dest, helper, actions)
        
    def close_item(self): 
        return super().close_item()

class Storage_Unit(Interact):
    def __init__(self, name, gen_name, items_list) -> None:
        super().__init__(name, gen_name)
        if items_list == None:
            self.items = []
        else:
            self.items = items_list

    def __repr__(self) -> str:
        return f'{self.name}(storage unit)'

    def set_items(self, item_list):
        if item_list != None:
            for i in item_list:
                self.items.append(i)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)
    
    def build_contained_list(self, complex_bool):
        node_items = []
        node_items.append(self)
        if len(self.items) > 0:
            for i in range(0, len(self.items)):
                if issubclass(type(self.items[i]), Storage_Unit):
                    if (issubclass(type(self.items[i]), Openable_Interact) and self.items[i].open) or (not issubclass(type(self.items[i]), Openable_Interact)):
                        node_items.extend(self.items[i].build_contained_list(complex_bool))
                    else:
                        node_items.append((self.items[i], self)) if complex_bool else node_items.append(self.items[i])
                else:
                    node_items.append((self.items[i], self)) if complex_bool else node_items.append(self.items[i])

        return node_items

class Storage_Spot(Storage_Unit):
    def __init__(self, name, gen_name, item_list) -> None:
        super().__init__(name, gen_name, item_list)
        self.storage_type = "on"

    def inspect_item(self): 
        actions = {
            'print_all': [],
        }
        
        if len(self.items) == 0:
            sentence = f"There is nothing on the {self.name}."
        elif len(self.items) == 1:
            sentence = f"On the {self.name} is {self.items[0].article} {self.items[0].name}."
        elif len(self.items) == 2:
            sentence = f"On the {self.name} is {self.items[0].article} {self.items[0].name} and {self.items[1].article} {self.items[1].name}."
        else:
            sentence = f"On the {self.name} is {self.items[0].article} {self.items[0].name}, "
            for i in range(1, len(self.items)-1):
                sentence += f"{self.items[i].article} {self.items[i].name}, "
            sentence += f"and {self.items[-1].article} {self.items[-1].name}."

        actions['print_all'].append(sentence)
        return actions

class Wall_Storage(Storage_Spot):
    def __init__(self, name, gen_name, item_list) -> None:
        super().__init__(name, gen_name, item_list)

class Floor_Storage(Storage_Spot):
    def __init__(self, name, gen_name, item_list) -> None:
        super().__init__(name, gen_name, item_list)
    
class Storage_Bin(Storage_Unit):
    def __init__(self, name, gen_name, item_list) -> None:
        super().__init__(name, gen_name, item_list)
        self.storage_type = "in"

    def inspect_item(self): 
        actions = {
            'print_all': [],
        }

        if len(self.items) == 0:
            sentence = f"There is nothing in the {self.name}."
        elif len(self.items) == 1:
            sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}."
        elif len(self.items) == 2:
            sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name} and {self.items[1].article} {self.items[1].name}."
        else:
            sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}, "
            for i in range(1, len(self.items)-1):
                sentence += f"{self.items[i].article} {self.items[i].name}, "
            sentence += f"and {self.items[-1].article} {self.items[-1].name}."

        actions['print_all'].append(sentence)
        return actions 

class Storage_Box(Storage_Unit, Openable_Interact):
    def __init__(self, name, gen_name, item_list) -> None:
        super().__init__(name, gen_name, item_list)
        self.open = False
    
class Storage_LockBox(Lockable_Interact, Storage_Box):
    def __init__(self, name, gen_name, locked_bool, keys_list, item_list) -> None:
        super(Lockable_Interact, self).__init__(name, gen_name, keys_list)
        super(Storage_Box, self).__init__(name, gen_name, item_list)
        self.locked = locked_bool

    def inspect_item(self): 
        actions = {
            'print_all': [],
        }
        if self.open:
            if len(self.items) == 0:
                sentence = f"There is nothing in the {self.name}."
            elif len(self.items) == 1:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}."
            elif len(self.items) == 2:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name} and {self.items[1].article} {self.items[1].name}."
            else:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}, "
                for i in range(1, len(self.items)-1):
                    sentence += f"{self.items[i].article} {self.items[i].name}, "
                sentence += f"and {self.items[-1].article} {self.items[-1].name}."

            actions['print_all'].append(sentence)
        else:
            if self.locked:
                actions['print_all'].append(f"The {self.name} is closed and locked.")
            else:
                actions['print_all'].append(f"The {self.name} is closed but unlocked.")
        return actions
          
class Door(Openable_Interact):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)
        self.can_lock_unlock = False
            
class Lockable_Door(Lockable_Interact, Door):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.visited = False
        self.keyable = True

class Ward_Lockable_Door(Lockable_Door):
    _doors_registry = []
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self._doors_registry.append(self)

class Basement_Lockable_Door(Lockable_Door):
    _doors_registry = []
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self._doors_registry.append(self)

class Electronic_Door(Lockable_Interact, Door):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.keyable = False

    def unlock_item(self, player):
        #unlock using code or keyard also opens door
        ...

    def close_item(self):
        #closing door also locks it again
        ...

class Hanging_Wall_Item(Interact):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.can_hang = True

class Riddle_Box(Storage_LockBox):
    def __init__(self, name, gen_name, item_list, riddle_lines, answer_array) -> None:
        super().__init__(name, gen_name, True, [], item_list)
        self.riddle = riddle_lines
        self.answers = answer_array
        self.item_actions.update({
            'solve': self.prompt_solve_item,
        })

    def inspect_item(self):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        } 
        if self.open:
            actions["print_all"].append(f"{self.name} is solved. To read the riddle again, 'read {self.name}'")
            if len(self.items) == 0:
                sentence = f"There is nothing in the {self.name}."
            elif len(self.items) == 1:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}."
            elif len(self.items) == 2:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name} and {self.items[1].article} {self.items[1].name}."
            else:
                sentence = f"In the {self.name} is {self.items[0].article} {self.items[0].name}, "
                for i in range(1, len(self.items)-1):
                    sentence += f"{self.items[i].article} {self.items[i].name}, "
                sentence += f"and {self.items[-1].article} {self.items[-1].name}."

            actions['print_all'].append(sentence)
            return (None, None, actions)
        else:
            actions["print_all"].append(f"{self.name} goes as follows:")
            for line in self.riddle:
                actions["print_all"].append([line, "riddle"])
            actions["print_all"].append("Would you like to solve the riddle?")
            actions['ask_y_or_n'] = True
            return ("ask_solve_riddle", self, actions)


    def prompt_solve_item(self):
        actions = {
            'print_all': []
        }  

    def solve_item(self, guess_str):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        } 
        if guess_str in self.answers:
            actions['print_all'].append(f"Correct! You have solved {self.name}!")
            actions['print_all'].append("With a hiss, a small hatch opens, revealing a box in the wall.")
            self.locked = False
            self.open = True
            return (None, None, actions)
        else:
            actions['print_all'].append(f"Incorrect. You have not yet solved {self.name}!")
            actions['print_all'].append(f"Would you like to try again?")
            actions['ask_y_or_n'] = True
            return ("ask_solve_riddle", self, actions)

class Riddle_Door(Interact):
    def __init__(self, name, gen_name, item_list, riddle_lines, answer_array) -> None:
        super().__init__(name, gen_name, True, None, item_list)
        self.riddle = riddle_lines
        self.answers = answer_array
        self.item_actions.update({
            'solve': self.solve_item,
        })
        del self.item_actions['break']


#############################################
##### Individual Inventory Item Classes #####
#############################################

class Basic_Item(Inv_Item):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)

class Key(Inv_Item):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)

class Keycard(Inv_Item):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)

class Flashlight(Inv_Item):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)
        self.full_power = False

class Crowbar(Inv_Item):
    # Necessary to be able to use the crowbar to open/close doors
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)


class ID_Bracelet(Inv_Item):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)
        self.properties = ["name", "age", "gender", "diagnosis"]
        self.values = [None, None, None, None]

    def inspect_item(self):
        actions = {
            'print_all': [],
        }
        actions['print_all'].append(f"The following data is printed on the bracelet:")
        # How to visually print it all
        for i in range(0, len(self.properties)):
            if self.values[i] is not None:
                actions['print_all'].append(f"{self.properties[i]}: {self.values[i]}")
            else:
                actions['print_all'].append(f"{self.properties[i]}: unknown")

        return actions

        
class Deck_of_Cards(Storage_Box, Inv_Item):
    def __init__(self, name, gen_name) -> None:
        all_cards = []
        for i in (("\u2660", "spades"), ("\u2665", "hearts"), ("\u2666", "diamonds"), ("\u2663", "clubs")):
            for j in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"):
                all_cards.append(Suit_Card(j, i[1], i[0]))
        super().__init__(name, gen_name, None)
        
    
    def inspect_item(self):
        actions = {
            'print_all': [],
        }

        if self.open:
            if len(self.items) == 0:
                actions['print_all'].append(f"There is nothing in the {self.name}.")
            else:
                #how to show which cards are in the box
                actions['print_all'].append(f"There is something in the {self.name}: {self.items}.") 
        else:
            actions['print_all'].append(f"The {self.name} is closed.")
        return actions

class Suit_Card(Inv_Item):
    def __init__(self, number, suit_name, suit_display) -> None:
        super().__init__(f"{number} {suit_display}", "card")
        self.suit = suit_display
        self.suit_name = suit_name
        self.number = number
    
    def __repr__(self) -> str:
        return f'{self.number}{self.suit}'
    
    def inspect_item(self):
        actions = {
            'print_all': [],
        }

        actions['print_all'].append(f"There does not appear to be anything special about the {self.name}.")
        return actions

class Power_Box(Interact):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)
        self.special_commands = ["pull", "push"]

    def hit_switch(self):
        for room in room_class.Room._room_registry:
            room.switch_lights()

    def inspect_item(self):
        actions = {
            'print_all': [],
        }
        #custom commands dict for every item: here would be pull or push
        actions['print_all'].append("There is a lever attached to the box.") 
        actions['print_all'].append("There is an instruction label on the box, but the words have long since faded away.") 

        return actions

class Chess_Set(Storage_Box):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name, [
            Quote_Note("chess note", 
                "note", 
                ["No one ever won a game by resigning."],
                "Savielly Tartakower"),
            Basic_Item("chess board", "board"),
        ])

        