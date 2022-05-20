
import game_backend.classes.room_class as room_class
import game_backend.gl_backend_functions as gl


class Item:
    def __init__(self, name, gen_name) -> None:
        self.name = name
        self.gen_name = gen_name
        self.article = "a"
        self.can_inspect = True

    def inspect_object(self): 
        actions = {
            'print_all': [],
        }

        actions['print_all'].append(f"There does not appear to be anything special about this {self.gen_name}.")
        return actions

    
class Inv_Item(Item):

    # name - visible name of item  !!!! must be 17 characters or less !!!!
    # desc - description of item 

    def __init__(self, name, gen_name, desc) -> None:
        super().__init__(name, gen_name)
        self.inv_space = 1
        self.desc = desc  
        self.can_pick_up = True
        self.can_interact = False
        self.can_open_close = False
        self.can_lock_unlock = False
        self.can_break = False

    def __repr__(self) -> str:
        return f'{self.name}(inv item)'

class Key(Inv_Item):
    def __init__(self, name, gen_name , desc):
        super().__init__(name, gen_name, desc)



###################
#### Interacts #### 
###################

class Interact(Item):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.can_pick_up = False
        self.can_interact = True
        self.can_open_close = False
        self.can_lock_unlock = False
        self.can_break = False

    def __repr__(self) -> str:
        return f'{self.name}(interact item)'

class Openable_Interact(Interact):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.open = False
        self.can_open_close = True

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
        
        return actions
        
class Lockable_Interact(Openable_Interact):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name)
        self.locked = True
        self.can_lock_unlock = True
        self.compatible_keys = keys_list # list keys in most general effectiveness to most specific effectiveness
        self.key_unlock = True
        self.crowbar_unlock = True
        self.electronic_unlock = False 
    
    def unlock_item(self, player):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        if self.locked:
            unlocking_item = None
            for item in self.compatible_keys:
                if item in player.inv:
                    unlocking_item = item
                    break
            if unlocking_item == None and self.crowbar_unlock:
                for item in player.inv:
                    if isinstance(item, Crowbar):
                        unlocking_item = item
            
            if unlocking_item != None:
                if isinstance(unlocking_item, Crowbar):
                    actions['print_all'].append(f"You have broken open the {self.name} with the {unlocking_item.name}.")
                else:
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
        if not self.locked:
            locking_item = None
            for item in self.compatible_keys:
                if item in player.inv:
                    locking_item = item
                    break
            if locking_item != None:
                actions['print_all'].append(f"You have locked the {self.name} with the {locking_item.name}.")
                self.locked = True
            else:
                actions['print_all'].append(f"You do not have anything that can lock the {self.name}.")
            
        else:
            actions['print_all'].append(f"The {self.name} is already locked.")

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
            actions['print_all'].append(f"Would you like to try to unlock the {self.name}?")
            dest, helper = "ask_unlock_item", self
            actions['ask_y_or_n'] = True

        else:
            actions = gl.parse_tuples(super().open_item(), actions)

        return (dest, helper, actions)
        
    def close_item(self): 
        return super().close_item


class Storage_Unit(Interact):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.items = []

    def set_items(self, item_list):
        for i in item_list:
            self.items.append(i)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

class Storage_Spot(Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)

    def inspect_object(self): 
        actions = {
            'print_all': [],
        }
        if len(self.items) == 0:
            actions['print_all'].append(f"There is nothing on the {self.name}.")
        else:
            actions['print_all'].append(f"There is something on the {self.name}: {self.items}.")
        return actions

class Storage_Bin(Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.can_lock_unlock = False
        self.can_open_close = False

    def inspect_object(self): 
        actions = {
            'print_all': [],
        }
        if len(self.items) == 0:
            actions['print_all'].append(f"There is nothing in the {self.name}.")
        else:
            actions['print_all'].append(f"There is something in the {self.name}: {self.items}.")
        return actions

class Storage_Box(Openable_Interact, Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.can_lock_unlock = False
        self.can_open_close = True
    
    def inspect_object(self): 
        actions = {
            'print_all': [],
        }
        if self.open:
            if len(self.items) == 0:
                actions['print_all'].append(f"There is nothing in the {self.name}.")
            else:
                actions['print_all'].append(f"There is something in the {self.name}: {self.items}.")
        else:
            actions['print_all'].append(f"The {self.name} is closed.")
        return actions

class Storage_LockBox(Lockable_Interact, Openable_Interact, Storage_Unit):
    def __init__(self, name, gen_name, locked_bool, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.locked = locked_bool

    def inspect_object(self): 
        actions = {
            'print_all': [],
        }
        if self.open:
            if len(self.items) == 0:
                actions['print_all'].append(f"There is nothing in the {self.name}.")
            else:
                actions['print_all'].append(f"There is something in the {self.name}: {self.items}.")
        else:
            if self.locked:
                actions['print_all'].append(f"The {self.name} is closed and locked.")
            else:
                actions['print_all'].append(f"The {self.name} is closed.")
        return actions
    
      
class Door(Openable_Interact):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)
        self.can_lock_unlock = False
            
class Lockable_Door(Lockable_Interact, Door):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.keyable = True


#############################################
##### Individual Inventory Item Classes #####
#############################################

class Keycard(Inv_Item):
    def __init__(self, name, gen_name , desc):
        super().__init__(name, gen_name, desc)

class Plastic_Utensil(Inv_Item):
    def __init__(self, name, gen_name , desc):
        super().__init__(name, gen_name, desc)

class Flashlight(Inv_Item):
    def __init__(self, name, gen_name , desc):
        super().__init__(name, gen_name, desc)
        self.full_power = False

class Crowbar(Inv_Item):
    def __init__(self, name, gen_name , desc):
        super().__init__(name, gen_name, desc)

class ID_Bracelet(Inv_Item):
    def __init__(self, name, gen_name , desc):
        super().__init__(name, gen_name, desc)
        self.properties = ["name", "age", "gender", "diagnosis"]
        self.values = [None, None, None, None]

    def print_values(self):
        # How to visually print it all
        pass

class Deck_of_Cards(Inv_Item, Storage_Box):
    def __init__(self, name, gen_name, desc) -> None:
        super().__init__(name, gen_name, desc)
        self.items = []
        for i in (("\u2660", "spades"), ("\u2665", "hearts"), ("\u2666", "diamonds"), ("\u2663", "clubs")):
            for j in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"):
                self.items.append(Suit_Card(j, i[1], i[0]))
    
    def inspect_object(self):
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
        super().__init__(f"{number} {suit_display}", "card", "a cool card")
        self.suit = suit_display
        self.suit_name = suit_name
        self.number = number
    
    def __repr__(self) -> str:
        return f'{self.number}{self.suit}'
    
    def inspect_object(self):
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
        for r in room_class.Room._room_registry:
            r.switch_lights()

    def inspect_object(self):
        actions = {
            'print_all': [],
        }
        #custom commands dict for every item: here would be pull or push
        actions['print_all'].append("There is a lever attached to the box.") 
        actions['print_all'].append("There is an instruction label on the box, but the words have long since faded away.") 

        return actions