
import game_backend.classes.room_class as room_class


class Item:

    def __init__(self, name, gen_name) -> None:
        self.name = name
        self.gen_name = gen_name
        self.inspect_bool = True

    
class Inv_Item(Item):

    # name - visible name of item  !!!! must be 17 characters or less !!!!
    # desc - description of item 
    # hidden_atr - either None ,or, list of [text description, class of interact]
    # craftable - either None ,or, list of [required second item class, result item class]
    def __init__(self, name, gen_name, desc, hidden_atr) -> None:
        super().__init__(name, gen_name)
        self.inv_space = 1
        self.desc = desc
        self.hidden_atr = hidden_atr  
        self.pick_up_bool = True
        self.interact_bool = False
        self.openable_bool = False
        self.lockable_bool = False
        self.breakable = False

    def __repr__(self) -> str:
        return f'{self.name}(inv item)'

    def select_inv_item(self):
        actions = {
            'print_all': [],
            'build_multiple_choice': None,
            'ask_y_or_n': False
        }
        actions['print_all'].append(f"You have selected the {self.name} from your inventory.")
        actions['print_all'].append("What would you like to do with it?")
        actions['build_multiple_choice'] = ["Inspect it", "Drop it"],[["inspect item", self], ["drop item", self]]
        return (None, None, actions)

    def inspect_item(self): 
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        actions['print_all'].append(self.desc)
        actions['print_all'].append("Item Description")

        if self.hidden_atr != None:
            pass # Edit for how the items have hidden attributes
        else:
            actions['print_all'].append("There does not seem to be anything special about this item.")

        return (None, None, actions)

class Key(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)

class Keycard(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)

class Plastic_Utensil(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)

class Flashlight(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)
        self.full_power = False

class Crowbar(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)

class ID_Bracelet(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)
        self.properties = ["name", "age", "gender", "diagnosis"]
        self.values = [None, None, None, None]

    def print_values(self):
        # How to visually print it all
        pass

class Shotgun_Shells(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)
        self.inv_space = 2

class Utility_Belt(Inv_Item):
    def __init__(self, name, gen_name , desc, hidden_atr):
        super().__init__(name, gen_name, desc, hidden_atr)
        self.inv_space = 0
        self.added_cap = 5 #added capacity to inv

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
        self.hidden_atr = None

    def __repr__(self) -> str:
        return f'{self.name}(interact item)'
    
class Power_Box(Interact):
    def __init__(self, name, gen_name):
        super().__init__(name, gen_name)

    def hit_switch(self):
        for r in room_class.Room._room_registry:
            r.switch_lights()


class Openable_Interact(Interact):
    
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name)
        self.open = False
        self.locked = True
        self.broken = False
        self.crowbar_open = True
        self.keyable = True
        self.compatible_keys = keys_list
        self.electronic_open = False
        self.openable_bool = True
        self.lockable_bool = True
        

    def open_close_interact(self, player, act):
        # act: "open" or "close"
        if isinstance(self, Door):
            interact_str = "door"
        elif isinstance(self, Cabinet):
            interact_str = "cabinet"
        elif isinstance(self, Drawers):
            interact_str = "drawer"

        if act == "open":
            return self.open_interact(player, interact_str)
        elif act == "close":
            return self.close_interact(player, interact_str)

    def open_interact(self, player, gen_str): #######
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
            actions['print_all'].append(f"The {gen_str} here has already been opened")
            return ("open_door", actions)

        # When door is closed
        else:
            # When door is closed and locked
            if not self.open and self.locked:
                if self.keyable and self.locked:
                    actions['print_all'].append(f"There is a locked {gen_str} here.")
                    for k in self.compatible_keys:
                        if k in player.inv:
                            actions['print_all'].append(f"Would you like to open the {gen_str} with your key?")
                            actions['ask_y_or_n'] = True
                            return ("open_door_key", actions)
                if has_crowbar and self.crowbar_open:
                    actions['print_all'].append(f"Would you like to open the {gen_str} with your crowbar?")
                    actions['ask_y_or_n'] = True
                    return ("open_door_crowbar", actions)
                if not self.keyable and self.locked and self.crowbar_open:
                    actions['print_all'].append(f"The {gen_str} is locked, but the lock is broken.")
                    if has_crowbar:
                        actions['print_all'].append(f"Would you like to open the {gen_str} with your crowbar?")
                        actions['ask_y_or_n'] = True
                        return ("open_door_crowbar", actions)
                if self.locked and self.electronic_open:
                    actions['print_all'].append(f"There is a {gen_str} locked with an electronic pad here.")
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
                            actions['print_all'].append(f"There does not appear to be any way to open the {gen_str} with a crowbar")
                        return (None, actions)
                
            # When door is closed and unlocked
            if not self.open and not self.locked:
                actions['print_all'].append(f"The {gen_str} is not locked.")
                actions['print_all'].append("Would you like to open it?")
                actions['ask_y_or_n'] = True
                return ("open_door", actions)

    def close_interact(self, player, gen_str): ######## NEED WORK
        
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

        # When door is open (and unlocked)
        if self.open:
            # Write something different
            pass

        # When door is closed
        else:
            # When door is closed and locked
            if not self.open and self.locked:
                if self.keyable and self.locked:
                    actions['print_all'].append(f"There is a locked {gen_str} here.")
                    for k in self.compatible_keys:
                        if k in player.inv:
                            
                            return ("dest", actions)
                if has_crowbar and self.crowbar_open:
                    
                    actions['ask_y_or_n'] = True
                    return ("dest", actions)
                if not self.keyable and self.locked and self.crowbar_open:
                    actions['print_all'].append(f"The {gen_str} is locked, but the lock is broken.")
                    if has_crowbar:
                        
                        actions['ask_y_or_n'] = True
                        return ("dest", actions)
                if self.locked and self.electronic_open:
                    actions['print_all'].append(f"There is a {gen_str} locked with an electronic pad here.")
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

                        return ("dest", actions)
                    else:
                        actions['print_all'].append("With no power, the keypad is useless")
                        if has_crowbar:
                            actions['print_all'].append(f"There does not appear to be any way to open the {gen_str} with a crowbar")
                        return ("dest", actions)
                
            # When door is closed and unlocked
            if not self.open and not self.locked:
                actions['print_all'].append(f"The {gen_str} is not locked.")
                actions['print_all'].append("Would you like to open it?")
                actions['ask_y_or_n'] = True
                return ("dest", actions)

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
        

class Storage_Box(Openable_Interact, Storage_Unit):
    def __init__(self, name, gen_name, locked_bool, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.locked = locked_bool



class Cabinet(Storage_Box):
    def __init__(self, name, gen_name, locked_bool, keys_list):
        super().__init__(name, gen_name, locked_bool, keys_list)
        self.locked = locked_bool

class Drawers(Storage_Box):
    def __init__(self, name, gen_name, locked_bool, keys_list):
        super().__init__(name, gen_name, locked_bool, keys_list)
        self.locked = locked_bool
      
class Door(Openable_Interact):
    def __init__(self, name, gen_name, keys_list):
        super().__init__(name, gen_name, keys_list)
        self.electronic_open = False
            
class Keyable_Door(Door):
    def __init__(self, name, gen_name, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.keyable = True

class Electronic_Door(Door):
    def __init__(self, name, gen_name, code, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.keyable = False
        self.electronic_open = True
        self.crowbar_open = False
        self.code = code 
        self.crowbar_open = False
        self.electronic_open = True

    def enter_code(self, choice, list): #should be accept code but whatever
        #list: next_room, direction choice, door, player
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        
        if choice == 'q':
            actions['print_all'].append("You are no longer attempting codes. ")
            return (None, None, actions)
        elif not choice.isnumeric(): #make it so it can only enter numbers? using tkinter validate
            actions['print_all'].append("Please enter only numbers")
            return ("enter_code", list, actions)
        elif len(choice) < 1:
            actions['print_all'].append("Please enter a code before submitting!")
            return ("enter_code", list, actions)

        elif len(choice) > 6:
            actions['print_all'].append("Please enter a code no longer than 6 numbers!")
            return ("enter_code", list, actions)

        if self.code == choice:
            self.open = True
            actions['print_all'].append("The door hisses, sliding into the wall revealing the Control Room!")
            list[2].locked = False
            list[2].open = True
            return (None, None, actions)
    
        else:
            actions['print_all'].append("The code did not open the door.")
            actions['print_all'].append("Continue trying or enter 'q' to quit:")
            return ("enter_code", list, actions)

