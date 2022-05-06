
import game_backend.classes.room_class as room_class


class Item:
    def __init__(self, name, gen_name) -> None:
        self.name = name
        self.gen_name = gen_name
        self.inspect_bool = True

    def inspect_item(self): 
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
        self.pick_up_bool = True
        self.interact_bool = False
        self.openable_bool = False
        self.lockable_bool = False
        self.breakable = False

    def __repr__(self) -> str:
        return f'{self.name}(inv item)'

class Key(Inv_Item):
    def __init__(self, name, gen_name , desc):
        super().__init__(name, gen_name, desc)

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


###################
#### Interacts #### 
###################

class Interact(Item):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.pick_up_bool = False
        self.interact_bool = True
        self.openable_bool = False
        self.lockable_bool = False
        self.breakable = False

    def __repr__(self) -> str:
        return f'{self.name}(interact item)'
    
class Power_Box(Interact):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)

    def hit_switch(self):
        for r in room_class.Room._room_registry:
            r.switch_lights()

class Openable_Interact(Interact):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.open = False
        self.openable_bool = True

    def open_interact(self, player): #######
        # When door is open (and unlocked)
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        
        #check for items based on classes
        has_crowbar, has_keycard = False, False
        for i in player.inv:
            if isinstance(i, Crowbar):
                has_crowbar = True
            elif isinstance(i, Keycard):
                has_keycard = True

        if self.open:
            actions['print_all'].append(f"The {self.gen_name} here has already been opened")
            return ("open_door", actions)

        # When door is closed
        else:
            # When door is closed and locked
            if not self.open and self.locked:
                if self.keyable and self.locked:
                    actions['print_all'].append(f"There is a locked {self.gen_name} here.")
                    for k in self.compatible_keys:
                        if k in player.inv:
                            actions['print_all'].append(f"Would you like to open the {self.gen_name} with your key?")
                            actions['ask_y_or_n'] = True
                            return ("open_door_key", actions)
                if has_crowbar and self.crowbar_open:
                    actions['print_all'].append(f"Would you like to open the {self.gen_name} with your crowbar?")
                    actions['ask_y_or_n'] = True
                    return ("open_door_crowbar", actions)
                if not self.keyable and self.locked and self.crowbar_open:
                    actions['print_all'].append(f"The {self.gen_name} is locked, but the lock is broken.")
                    if has_crowbar:
                        actions['print_all'].append(f"Would you like to open the {self.gen_name} with your crowbar?")
                        actions['ask_y_or_n'] = True
                        return ("open_door_crowbar", actions)
                if self.locked and self.electronic_open:
                    actions['print_all'].append(f"There is a {self.gen_name} locked with an electronic pad here.")
                    actions['print_all'].append("It appears to need a keycard or code to open.")
                    actions['print_all'].append("")
                    if player.loc.lights_on:

                        if has_keycard:
                            actions['print_all'].append("With the power restored, you can now try entering a code, or a use your keycard.")
                            actions['print_all'].append("What would you like to do?")
                            actions['build_multiple_choice'] = [["Enter a Code", "Use a Keycard", "Cancel"], [1, 2, -1]]
                            
                        else: 
                            actions['print_all'].append("With the power restored, you can now try entering a code.")
                            actions['print_all'].append("What would you like to do?")
                            actions['build_multiple_choice'] = [["Enter a Code", "Cancel"], [1, -1]]

                        return ("open_electronic_door", actions)
                    else:
                        actions['print_all'].append("With no power, the keypad is useless")
                        if has_crowbar:
                            actions['print_all'].append(f"There does not appear to be any way to open the {self.gen_name} with a crowbar")
                        return (None, actions)
                
            # When door is closed and unlocked
            if not self.open and not self.locked:
                actions['print_all'].append(f"The {self.gen_name} is not locked.")
                actions['print_all'].append("Would you like to open it?")
                actions['ask_y_or_n'] = True
                return ("open_door", actions)

    def close_interact(self, player): ######## NEED WORK
        
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        
class Lockable_Interact(Interact):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name)
        self.compatible_keys = keys_list
        self.lockable_bool = True
        self.locked = True
        self.keyable = True
        self.crowbar_open = True
        self.electronic_open = False
        self.open = False
        self.openable_bool = True

    def unlock_interact(self, player):
        ...

    def lock_interact(self, player):
        ...

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

class Storage_Bin(Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.lockable_bool = False
        self.openable_bool = False

class Storage_Box(Openable_Interact, Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.lockable_bool = False
        self.openable_bool = True

class Storage_LockBox(Lockable_Interact, Openable_Interact, Storage_Unit):
    def __init__(self, name, gen_name, locked_bool, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.locked = locked_bool
      
class Door(Openable_Interact):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)
        self.lockable_bool = False
            
class Lockable_Door(Lockable_Interact, Door):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.keyable = True
