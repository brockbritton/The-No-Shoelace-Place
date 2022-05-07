

import num2words as n2w

import game_backend.classes.item_class as item_class
import game_backend.objects.items as item


class Room:
    _room_registry = []

    def __init__(self, name, display_name, description) -> None:
        self.name = name
        self.display_name = display_name
        self.description = description
        
        self.storage_containers = [item_class.Storage_Spot("ground", "ground")]
        self.walls = [] ######
        self.storage_dict = {}
        self.interacts = []
        self.monsters = []
        self.doors = {}
        self.interacts = []
        self.has_doors = False
        self._room_registry.append(self)
        self.visited = False

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


    def set_demons(self, list):
        for i in list:
            self.monsters.append(i)

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

    def remove_item(self, item):
        for sc in self.storage_containers:
            if item in sc.items:
                sc.items.remove(item)

    def print_room_name(self):
        return ("You have now entered: " + self.name)

    def print_description(self):
        return ("Room Description: " + self.description)

    def switch_lights(self):
        if self.lights_on:
            self.lights_on = False
        else:
            self.lights_on = True

    def update_storage_dict(self):
        for sc in self.storage_containers:
            self.storage_dict[sc] = sc.items

    def print_directions(self, player, none_or_one): 
        #left, forward, right, back
        
        if player.last_loc != None:
            lfrb_rooms, lfrb_cardinality = self._find_positional_rooms(player)
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
                sentence = self._build_complicated_adjacent_rooms_sentence(all_sentence_parts[i], blrf_sentence_start[i])
                sentences.append(sentence)

            full_paragraph = " ".join(sentences)
            return full_paragraph
        
        else:
            i = ["left", "forward", "right", "backward"].index(none_or_one)
            all_sentence_parts = []
            blrf_sentence_start = ["To your left", "In front of you", "To your right", "Behind you"]
            
            sentence_parts = self._get_sentence_parts(lfrb_rooms[i], lfrb_cardinality[i])
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

    def _find_positional_rooms(self, player):
        # identify in what positional directions which real rooms are
        nesw_rooms = [self.north, self.east, self.south, self.west] 
        nesw_letters = ["n", "e", "s", "w"] 

        lfrb_rooms = []
        lfrb_cardinality = []
        last_room_index = self._find_back_index(player, nesw_rooms)
        
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
                                    room_states.append(("unlocked door visited", adjacent_room[x]))
                                else:
                                    room_states.append("unlocked door unknown")
                            else: 
                                #needs to be here
                                room_states.append("locked door") 

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
                            room_states.append(("unlocked door visited", adjacent_room))
                        else:
                            room_states.append("unlocked door unknown")
                    else: 
                        room_states.append("locked door")
                else: 
                    if adjacent_room.visited:
                        room_states.append(("visited room", adjacent_room))
                    else:
                        room_states.append("unknown room")
        else:
            room_states.append("wall")

        return room_states

    def _build_complicated_adjacent_rooms_sentence(self, room_states, sentence_start):
        if len(room_states) > 1:
            state_freq = {}
            state_rooms = {}
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

            sentence_guide = ["visited room", "unlocked door visited", "unlocked door unknown", "locked door", "unknown room"]
            sentence_parts = []
            sentence_parts.append(sentence_start)
            for i in range(0, len(sentence_guide)):
                if sentence_guide[i] in state_freq.keys():
                    if i == 0:
                        sentence_parts.append(f" is {state_rooms[sentence_guide[i]].pop(0).name}")
                    elif i == 1:
                        sentence_parts.append(f" is an unlocked door leading to {state_rooms[sentence_guide[i]].pop(0).name}")
                    else:
                        # build a sentence using the keys and values from above
                        value_text = n2w.num2words(state_freq[sentence_guide[i]])
                        vowels = ["a", "e", "i", "o", "u"]
                        if value_text == "one":
                            if sentence_guide[i][0] in vowels:
                                verb = "is an"
                            else:
                                verb = "is a"
                            plural = ""
                            piece = "an "
                        else: 
                            verb = (f"are {value_text}")
                            plural = "s"
                            piece = ""

                        if sentence_guide[i] == "unlocked door unknown":
                            sentence_parts.append(f"{verb} locked door{plural} leading to {piece}unknown room{plural}")
                        elif sentence_guide[i] == "locked door":
                            sentence_parts.append(f"{verb} locked door{plural}")
                        elif sentence_guide[i] == "unknown room":
                            sentence_parts.append(f"{verb} unknown room{plural}")
                        elif sentence_guide[i] == "wall":
                            sentence_parts.append(f"{verb} unknown room{plural}")
            
        else:
            sentence_parts = []
            sentence_parts.append(sentence_start)
            
            if isinstance(room_states[0], tuple): 
                if room_states[0][0] == "visited room":
                    sentence_parts.append(f" is {room_states[0][1].name}")
                elif room_states[0][0] == "unlocked door visited":
                    sentence_parts.append(f" is an unlocked door leading to {room_states[0][1].name}")
            else:
                if room_states[0] == "unlocked door unknown":
                    sentence_parts.append("is an unlocked door leading to an unknown room")
                elif room_states[0] == "locked door":
                    sentence_parts.append("is a locked door")
                elif room_states[0] == "unknown room":
                    sentence_parts.append("is an unknown room")
                elif room_states[0] == "wall":
                    sentence_parts.append("is a wall")

            
        if len(sentence_parts[1:]) == 1:
            full_sentence = " ".join(sentence_parts)
            full_sentence += "."

        else:
            full_sentence = ""
            for i in range(0, len(sentence_parts)):
                if i > 1:
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

                else:
                    if i == 0:
                        full_sentence += (f"{sentence_parts[i]}")
                    else:
                        full_sentence += (f" {sentence_parts[i]}")

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
    def __init__(self, name, display_name, description, door_label) -> None:
        super().__init__(name, display_name, description)
        self.label = door_label
        self.lights_on = True
    
    def __repr__(self) -> str:
        return f'{self.name}(ward room)'


class Basement_Room(Room):
    def __init__(self, name, display_name, description) -> None:
        super().__init__(name, display_name, description)
        self.lights_on = False
    
    def __repr__(self) -> str:
        return f'{self.name}(basement room)'

class Maze_Room(Room):
    def __init__(self, name, description) -> None:
        super().__init__(name, "unclear", description)
        self.lights_on = False

    def __repr__(self) -> str:
        return f'{self.name}(maze room)'

    def print_directions(self, player, none_or_one):
        if item.flashlight in player.inv:
            if item.flashlight.full_power:
                return super().print_directions(player, none_or_one)
            else:
                return "The flashlight's light is barely strong enough to see even a few steps."
        else:
            return "It is completely dark here. There is no light to see by."
        
        

