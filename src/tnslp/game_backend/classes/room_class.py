

import random
import num2words as n2w
import tnslp.game_backend.classes.item_class as item_class
import tnslp.game_backend.classes.npc_class as npc_class
import tnslp.game_backend.gl_backend_functions as gl


class Room:
    _all_rooms_registry = []
    def __init__(self, name, display_name, description, room_label, floor_wall_items, doors) -> None:
        self.name = name
        self.display_name = display_name
        self.description = description
        self.label = room_label
        self.doors = {}
        self.has_doors = False
        if doors != None: 
            self.create_door_dict(doors)
        self._all_rooms_registry.append(self)
        self.storage_containers = [item_class.Storage_Spot("ground", "ground"), item_class.Storage_Wall("wall", "walls")]
        for i in range(0, len(floor_wall_items)):
            if floor_wall_items[i] != None:
                self.storage_containers[i].set_items(floor_wall_items[i])
        
        self.storage_dict = {}
        self._all_rooms_registry.append(self)
        self.visited = False
        self.item_actions = {
            'help' : self.show_all_actions,
            'inspect': self.inspect_room,
            'items': self.show_items,
            'rooms': self.show_directions,
        }

    def show_all_actions(self):
        actions = {
            'print_all': [],
        }

        actions['print_all'].append("Available actions for this room:")
        for key in self.item_actions:
            actions['print_all'].append(f"- {key}")


        return actions

    def inspect_room(self, player):
        actions = {
            'print_all': [],
        }

        actions['print_all'].append(self.description)

        return actions

    def show_items(self):
        actions = {
            'print_all': [],
        }
        if len(self.storage_containers) > 0:
            actions['print_all'].append(self.look_storage_units())

        return actions

    def show_directions(self, player):
        actions = {
            'print_all': [],
        }
        
        actions['print_all'].append(self.print_directions(player, None))

        return actions

    def look_storage_units(self):
        sc_dict = {
            True: [],
            False: []
        }

        for sc in self.storage_containers: 
            sc_dict[(len(sc.items) > 0)].append(sc)

        full_sentence = ""
        for key, value in sc_dict.items():
            if len(value) > 0:
                sentence = ""
                if key:
                    sentence += "There are items stored on or within "
                    conjoiner = "and"
                else:
                    sentence += "There are no items stored on or within "
                    conjoiner = "or"

                if len(value) == 1:
                    sentence += f"{value[0].article} {value[0].name}."
                elif len(value) == 2:
                    sentence += f"{value[0].article} {value[0].name} {conjoiner} {value[1].article} {value[1].name}."
                else:
                    for i in range(0, len(value)-1):
                        sentence += f"{value[i].article} {value[i].name}, "
                    sentence += f"{conjoiner} {value[-1].article} {value[-1].name}."
                    
                full_sentence += (sentence + " ")
        return full_sentence

    def xray_look_storage_units(self):
        # Storage_Spot, Storage_Bin, Storage_Box, Storage_LockBox 
        sentences = ""
        for sc in self.storage_containers:
            sentences +=  (f"{sc.name}: {sc.items}. ")

        return sentences

    def set_coordinates(self, n, e, s, w):
        self.north = n
        self.east = e
        self.south = s
        self.west = w

    def check_direction_next_room(self, string):
        if string == "n":
            return self.north
        elif string == "e":
            return self.east
        elif string == "s":
            return self.south
        elif string == "w":
            return self.west

    def add_storage_units(self, list):
        for i in list:
            self.storage_containers.append(i)

    def set_interacts(self, list):
        for i in list:
            self.interacts.append(i)

    def create_door_dict(self, door_list):
        direct_list = ["n", "e", "s", "w"]
        for i in range(0, len(door_list)):
            self.doors[direct_list[i]] = door_list[i]
        self.has_doors = True

    def add_item(self, item, spot):
        if spot == None:
            self.storage_containers[0].items.append(item)
        else:
            spot.items.append(item)

    def switch_lights(self):
        if self.lights_on:
            self.lights_on = False
        else:
            self.lights_on = True

    def update_storage_dict(self):
        for sc in self.storage_containers:
            self.storage_dict[sc] = sc.items

    def enter_room(self, player):
        actions = {
            'print_all': [],
        }
        if self != player.loc:
            player.last_loc = player.loc
        else:
            player.last_loc = None
        player.loc = self

        if not self.visited:
            # Updating XP for gui 
            actions['print_all'].append(f"New Room Discovered! +{player.xp_dict['new_room']}xp")
            actions['print_all'].append(f"You are now in {self.name}.")
            actions["print_all"].append(self.description)
            player.earn_xp(10)
            self.visited = True
        else:
            actions['print_all'].append(f"You are now in {self.name}.")

        
        for direction in self.doors.values():
            if isinstance(direction, list):
                for door in direction:
                    if isinstance(door, item_class.Lockable_Door) and not door.visited:
                        door.visited = True
            else:
                if isinstance(direction, item_class.Lockable_Door) and not direction.visited:
                    direction.visited = True

        if not self.lights_on:
            #some check about having full battery flashlight
            stumble = random.randint(1,12)
            if stumble == 1:
                actions['print_all'].append("In the dark, you stumbled and fell, scraping your hands on the rough ground.")
                player.health -= 5
                if player.health <= 0:
                    player.health = 0
                    return (None, "dead", actions)
                
        return (None, None, actions)

    def print_directions(self, player, none_or_one): 
        #left, forward, right, back
        if player.last_loc != None:
            lfrb_rooms, lfrb_cardinality = self.find_positional_rooms(player)
        else:
            lfrb_rooms = [self.east, self.south, self.west, self.north] 
            lfrb_cardinality = ["e", "s", "w", "n"]

        if none_or_one == None:
            all_sentence_parts = []
            blrf_sentence_start = ["To your left", "In front of you", "To your right", "Behind you"]
            for i in range(0, len(lfrb_rooms)):
                sentence_parts = self._get_sentence_parts(lfrb_rooms[i], lfrb_cardinality[i])
                all_sentence_parts.append(sentence_parts)
            
            sentences = []
            for i in range(0, len(all_sentence_parts)):
                ##### Break is below
                sentence = self._build_complicated_adjacent_rooms_sentence(all_sentence_parts[i], blrf_sentence_start[i])
                sentences.append(sentence)

            full_paragraph = " ".join(sentences)
            return full_paragraph
        
        else:
            i = ["left", "forward", "right", "backward"].index(none_or_one)
            all_sentence_parts = []
            blrf_sentence_start = ["To your left", "In front of you", "To your right", "Behind you"]
            
            sentence_parts = self._get_sentence_parts(lfrb_rooms[i], lfrb_cardinality[i])
            print(sentence_parts)
            ##### Break is below
            sentence = self._build_complicated_adjacent_rooms_sentence(sentence_parts, blrf_sentence_start[i])

            return sentence
       
    def _find_back_index(self, player, blfr_rooms):
        for r in blfr_rooms:
            if isinstance(r, list):
                for x in r:
                    if x == player.last_loc:
                        return blfr_rooms.index(r)

            elif r == player.last_loc:
                return blfr_rooms.index(r)

    def find_positional_rooms(self, player):
        # identify in what positional directions which real rooms are
        nesw_rooms = [self.north, self.east, self.south, self.west] 
        nesw_letters = ["n", "e", "s", "w"] 

        lfrb_rooms = []
        lfrb_cardinality = []
        last_room_index = self._find_back_index(player, nesw_rooms)
        if last_room_index == None:
            last_room_index = 0
        
        for i in range(1, 4):
            if last_room_index + i > 3:
                lfrb_rooms.append(nesw_rooms[(last_room_index + i) - 4])
                lfrb_cardinality.append(nesw_letters[(last_room_index + i) - 4])

            else:
                lfrb_rooms.append(nesw_rooms[last_room_index + i])
                lfrb_cardinality.append(nesw_letters[last_room_index + i])

        lfrb_rooms.append(nesw_rooms[last_room_index])
        lfrb_cardinality.append(nesw_letters[last_room_index])

        return lfrb_rooms, lfrb_cardinality

    def _get_sentence_parts(self, adjacent_room, direction_cardinality):
        room_states = []
        if adjacent_room != 0: 
            if isinstance(adjacent_room, list): 
                for x in (range(0, len(adjacent_room))):
                    if direction_cardinality in self.doors: #?
                        if self.doors[direction_cardinality] != None and self.doors[direction_cardinality][x] != None:
                            if not self.doors[direction_cardinality][x].locked:
                                if adjacent_room[x].visited:
                                    room_states.append(("door visited", (self.doors[direction_cardinality][x], adjacent_room[x])))
                                else:
                                    room_states.append(("door unknown", self.doors[direction_cardinality][x]))
                            else: 
                                if adjacent_room[x].visited:
                                    room_states.append(("door visited", (self.doors[direction_cardinality][x], adjacent_room[x])))
                                else:
                                    room_states.append(("door unknown", self.doors[direction_cardinality][x]))
                                
                        else:
                            if adjacent_room[x].visited:
                                room_states.append(("visited room", adjacent_room[x]))
                            else:
                                room_states.append("unknown room")

                    # Repeated due to if a door doesnt exist in this direction
                    else: 
                        if adjacent_room[x].visited:
                            room_states.append(("visited room", adjacent_room[x]))
                        else:
                            room_states.append("unknown room")

            # If there is only one room in a certain direction
            else: 
                if self.has_doors and self.doors[direction_cardinality] != None: #
                    if not self.doors[direction_cardinality].locked:
                        if adjacent_room.visited:
                            room_states.append(("door visited", (self.doors[direction_cardinality], adjacent_room)))
                        else:
                            room_states.append(("door unknown", self.doors[direction_cardinality]))
                    else: 
                        if adjacent_room.visited:
                            room_states.append(("door visited", (self.doors[direction_cardinality], adjacent_room)))
                        else:
                            room_states.append(("door unknown", self.doors[direction_cardinality]))
                                
                else: 
                    if adjacent_room.visited:
                        room_states.append(("visited room", adjacent_room))
                    else:
                        room_states.append("unknown room")
        else:
            room_states.append("wall")

        return room_states

    def _build_complicated_adjacent_rooms_sentence(self, room_states, sentence_start):
        state_freq = {}
        state_rooms = {}
        print()
        print(sentence_start)
        print("all room states:", room_states)
        for state in room_states:
            if isinstance(state, tuple):
                if state[0] not in state_freq.keys():
                    state_freq[state[0]] = 1
                    state_rooms[state[0]] = [state[1]]
                else:
                    state_freq[state[0]] += 1
                    state_rooms[state[0]].append(state[1])
            else:
                if state not in state_freq.keys():
                    state_freq[state] = 1
                else:
                    state_freq[state] += 1

        
        print("room freq:", state_freq)
        print("helper data:", state_rooms)

        sentence_guide = [
            "visited room", 
            "door visited", 
            "door unknown", 
            "unknown room",
            "wall"
            ]
        sentence_parts = []
        sentence_parts.append(sentence_start)
        for adj_type in sentence_guide:
            if adj_type in state_freq.keys():
                if adj_type in ["unknown room", "wall"]:
                    # build a sentence using the keys and values from above
                    freq_text = n2w.num2words(state_freq[adj_type])
                    vowels = ["a", "e", "i", "o", "u"]
                    if freq_text == "one":
                        if adj_type[0] in vowels:
                            verb_value = "is an"
                        else:
                            verb_value = "is a"
                        plural = ""
                    else: 
                        verb_value = (f"are {freq_text}")
                        plural = "s"
                    sentence_parts.append(f"{verb_value} {adj_type}{plural}")

                else:
                    while len(state_rooms[adj_type]) > 0:
                        if adj_type == "visited room":
                            sentence_parts.append(f"is {state_rooms[adj_type].pop(0).name}")
                        elif adj_type == "door visited":
                            helper_tuple = state_rooms[adj_type].pop(0)
                            if helper_tuple[0].locked:
                                locked_unlocked = "locked"
                            else:
                                locked_unlocked = "unlocked"
                            sentence_parts.append(f"is {helper_tuple[0].name} ({locked_unlocked}) leading to {helper_tuple[1].name}")
                        elif adj_type == "door unknown":
                            door = state_rooms[adj_type].pop(0)
                            if door.locked:
                                locked_unlocked = "locked"
                            else:
                                locked_unlocked = "unlocked"
                            sentence_parts.append(f"is {door.name} ({locked_unlocked}) leading to an unknown room") ###need door name
                            

        
        if len(sentence_parts[1:]) == 1:
            full_sentence = " ".join(sentence_parts)
            full_sentence += "."

        else:
            full_sentence = ""
            for i in range(0, len(sentence_parts)):
                if i == 0:
                    full_sentence += (f"{sentence_parts[i]}")
                elif i == 1:
                    full_sentence += (f" {sentence_parts[i]}")
                else:
                    if "is" in sentence_parts[i]:
                        sentence_parts[i] = sentence_parts[i].replace("is ", "")
                    elif "are" in sentence_parts[i]:
                        sentence_parts[i] = sentence_parts[i].replace("are ", "")
                    
                    # between the 2nd and 2nd to last item
                    if i > 1 and i < len(sentence_parts) - 1:
                        full_sentence += (f", {sentence_parts[i]}")
                    
                    # the last item
                    elif i == len(sentence_parts) - 1:
                        full_sentence += (f" and {sentence_parts[i]}.")

        return full_sentence
                    
    def print_items_loc_desc(self):
        paragraph_parts = []
        for sc in self.storage_containers:
            if isinstance(sc, item_class.Storage_Box):
                if sc.locked:
                    paragraph_parts.append((f"The {sc.name} is locked."))
                else:
                    paragraph_parts.append(self.build_container_sentence(sc))

            elif isinstance(sc, item_class.Storage_Spot):
                if len(sc.items) == 0:
                    paragraph_parts.append((f"There is nothing on the {sc.name}."))
                else:
                    paragraph_parts.append(self.build_container_sentence(sc))

        full_paragraph = " ".join(paragraph_parts)
        
        return full_paragraph

    def build_container_sentence(self, container):
        sentence_parts = []
        contain_type = "" 
        lock_type = ""

        if isinstance(container, item_class.Storage_Box):
            contain_type = "contains"
            if container.locked:
                lock_type = " locked"
            else:
                lock_type = " unlocked"
                
        elif isinstance(container, item_class.Storage_Spot):
            contain_type = "has"
            lock_type = ""

        if len(container.items) == 0:
            sentence_parts.append((f"The{lock_type} {container.name} is empty."))
        elif len(container.items) == 1:
            sentence_parts.append((f"The{lock_type} {container.name} {contain_type} a {container.items[0].name}."))
        elif len(container.items) == 2:
            sentence_parts.append((f"The{lock_type} {container.name} {contain_type} a {container.items[0].name} and a {container.items[1].name}."))
        else:
            sentence_parts.append((f"The{lock_type} {container.name} {contain_type}"))
            for i in range(0, len(container.items)):
                if i < len(container.items) - 1:
                    sentence_parts.append((f"a {container.items[i].name},"))
                else:
                    sentence_parts.append((f"and a {container.items[i].name}."))
        
        full_sentence = " ".join(sentence_parts)
        return full_sentence

class Ward_Room(Room):
    _ward_rooms_registry = []
    # room name, display name, description, room label, storage units, doors
    def __init__(self, name, display_name, description, room_label, storage_units, floor_wall_items, doors) -> None:
        super().__init__(name, display_name, description, room_label, floor_wall_items, doors)
        self.lights_on = True
        self._ward_rooms_registry.append(self)
        if storage_units != None:
            self.add_storage_units(storage_units)
        
        
    def __repr__(self) -> str:
        return f'{self.name}(ward room)'


class Starting_Ward_Room(Ward_Room):
    def __init__(self, name, display_name, description, room_label, storage_units, floor_wall_items, doors) -> None:
        super().__init__(name, display_name, description, room_label, storage_units, floor_wall_items, doors)
        self.visited = False
        if self.has_doors:
            for direction in self.doors.values():
                if isinstance(direction, list):
                    for door in direction:
                        if isinstance(door, item_class.Lockable_Door) and not door.visited:
                            door.visited = True
                else:
                    if isinstance(direction, item_class.Lockable_Door) and not direction.visited:
                        direction.visited = True


class Basement_Room(Room):
    _basement_rooms_registry = []
    def __init__(self, name, display_name, description, room_label, storage_units, floor_wall_items, doors) -> None:
        super().__init__(name, display_name, description, room_label, floor_wall_items, doors)
        self.lights_on = False
        self._basement_rooms_registry.append(self)
        if storage_units != None:
            self.add_storage_units(storage_units)

    
    def __repr__(self) -> str:
        return f'{self.name}(basement room)'


class Stairwell(Room):
    #self, name, display_name, description, room_label, floor_wall_items, doors
    def __init__(self, name, display_name, room_label, to_room) -> None:
        super().__init__(name, display_name, None, room_label, (None, None), None)
        self.to_room = to_room
        self.visited = True

    def enter_room(self, player):
        return self.to_room.enter_room(player)
    

class Final_Room(Room):
    #self, name, display_name, description, room_label, floor_wall_items, doors
    def __init__(self, name, display_name, description, room_label, doors) -> None:
        super().__init__(name, display_name, description, room_label, [None, None], doors)
        self.lights_on = False
        self.demon = npc_class.Depression_Demon()
    

    def __repr__(self) -> str:
        return f'{self.name}(final room)'

    def enter_room(self, player):
        actions = {
            'print_all': [],
            'build_multiple_choice': []
        }
        
        if not self.visited:
            # Updating XP for gui 
            actions['print_all'].append(f"New Room Discovered! +{player.xp_dict['new_room']}xp")
            player.earn_xp(10)
            self.visited = True

        actions['print_all'].append(f"You have now encountered your demon of {self.demon.name}. ")
        actions['print_all'].append("It has trapped you in this room. You cannot escape. It is time to face your demon!")

        player_avail_abilities = player.build_available_abilities_list()
        if len(player_avail_abilities) == 0:
            actions['print_all'].append(f"Unfortunately you have not learned any skills to fight your demon. The demon of {self.demon.name} has incapacitated you.")
            actions['print_all'].append("You have been returned to your room.")
            player.last_loc = None
            player.loc = player.personal_room
            enter_tuple = player.personal_room.enter_room(player)

            actions = gl.combine_dicts(actions, enter_tuple[2])
            return (enter_tuple[0], enter_tuple[1], actions)
            
        else:
            actions['print_all'].append("Please choose a skill to use against your demon:")
            displays = []
            for ability in player_avail_abilities:
                displays.append(ability.name)
            actions['build_multiple_choice'] = [displays, player_avail_abilities]
            return ("face_demon", None, actions)

class Maze_Room(Room):
    def __init__(self, name, display_name, description, room_label, floor_wall_items, doors) -> None:
        super().__init__(name, display_name, description, room_label, floor_wall_items, doors)