
import tnslp.game_backend.classes.room_class as room_class
import tnslp.game_backend.gl_backend_functions as gl


class Item:
    def __init__(self, name, gen_name) -> None:
        self.name = name
        self.gen_name = gen_name
        self.article = "the"
        self.item_actions = {
            'inspect': self.inspect_item,
        }

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
        return f'{self.name}(inv item)'

    def pick_up_item(self, player):
        actions = {
            'print_all': [],
            'ask_y_or_n': False
        }
        if self not in player.inv:
            if (len(player.inv) < player.inv_cap):
                actions['print_all'].append("You have added the " + self.name + " to your inventory.")
                actions['update_inv_visual'] = player.add_inventory(self)
                for sc in player.loc.storage_containers:
                    contents = sc.build_flat_list_of_contents(True)
                    for item_loc in contents:
                        if item_loc[0] == self:
                            item_loc[1].items.remove(self)
                            break
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
            actions['update_inv_visual'] = player.sub_inventory(self)
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
        return f'{self.name}(interact item)'

class Openable_Interact(Interact):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        self.open = False
        self.item_actions.update({
            'open': self.open_item,
            'close': self.close_item,
        })


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
        self.compatible_keys = keys_list # list keys in most general effectiveness to most specific effectiveness
        self.key_unlock = True
        self.crowbar_unlock = True
        self.electronic_unlock = False 
        self.item_actions.update({
            'lock': self.lock_item,
            'unlock': self.unlock_item,
        })

    
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

    def ask_unlock_item(self, choice, player):
        actions = {}

        if choice == 'y':
            actions = self.unlock_item(player)
        elif choice == 'n':
            actions['print_all'] = [f"You did not try to unlock the {self.name}."]

        return (None, None, actions)

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
            return super().open_item()

        return (dest, helper, actions)
        
    def close_item(self): 
        return super().close_item()

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

    def build_flat_list_of_contents(self, more_info):
        flat_list = []
        for item in self.items:
            if more_info:
                if isinstance(item, Storage_Unit):
                    flat_list.append((item, self))
                    flat_list.extend(item.build_flat_list_of_contents(more_info))
                else:
                    flat_list.append((item, self))
            else:
                if isinstance(item, Storage_Unit):
                    flat_list.append(item)
                    flat_list.extend(item.build_flat_list_of_contents(more_info))
                else:
                    flat_list.append(item)
        return flat_list

class Storage_Spot(Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
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

class Storage_Wall(Storage_Spot):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
    
class Storage_Bin(Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
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

class Storage_Box(Openable_Interact, Storage_Unit):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
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

class Storage_LockBox(Lockable_Interact, Storage_Box):
    def __init__(self, name, gen_name, locked_bool, keys_list) -> None:
        super().__init__(name, gen_name, keys_list)
        self.locked = locked_bool

    def inspect_item(self): 
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

        

class Deck_of_Cards(Inv_Item, Storage_Box):
    def __init__(self, name, gen_name) -> None:
        super().__init__(name, gen_name)
        for i in (("\u2660", "spades"), ("\u2665", "hearts"), ("\u2666", "diamonds"), ("\u2663", "clubs")):
            for j in ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"):
                self.items.append(Suit_Card(j, i[1], i[0]))
    
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
        for r in room_class.Room._room_registry:
            r.switch_lights()

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
        super().__init__(name, gen_name)
        self.items = [
            Quote_Note("chess note", 
                "note", 
                ["No one ever won a game by resigning."],
                "Savielly Tartakower"),
            Basic_Item("chess board", "board"),
        ]

        