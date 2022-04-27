

import game_backend.objects.items as item
import game_backend.classes.item_class as item_class
import num2words as n2w

class Room:
    _room_registry = []

    def __init__(self, name, description) -> None:
        self.description = description
        self.name = name
        self.storage_containers = [item_class.Storage_Spot("ground", "ground")]
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

    def set_storage_units(self, list):
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

    def print_one_direction(self, room_obj, str_letter): ##more params?
        ...
            
    def print_directions(self, player, none_or_one): ####### ugh
        direct_list = ["n", "e", "s", "w"]
        
        blrf_rooms_list = [self.north, self.east, self.south, self.west]
        blrf_direct_list = []

        print("Current Location:", self.name)
        
        if player.last_loc != None:
            for r in blrf_rooms_list:
                if isinstance(r, list):
                    for x in r:
                        if x == player.last_loc:
                            last_room_index = blrf_rooms_list.index(r)

                elif r == player.last_loc:
                    last_room_index = blrf_rooms_list.index(r)

                #can also be 0 - for wall

            blrf_direct_list.append(direct_list[last_room_index]) #back


            if last_room_index + 1 > 3: #left
                blrf_direct_list.append(direct_list[0])
            else:
                blrf_direct_list.append(direct_list[last_room_index + 1])

            if last_room_index - 1 < 0: #right
                blrf_direct_list.append(direct_list[3])
            else:
                blrf_direct_list.append(direct_list[last_room_index - 1])

            if last_room_index + 2 > 3: #forward
                blrf_direct_list.append(direct_list[last_room_index - 2])
            else:
                blrf_direct_list.append(direct_list[last_room_index + 2])

        else: 
            blrf_direct_list = ["n", "e", "w", "s"]
            last_room_index = 0
        
        behind = blrf_rooms_list[last_room_index]

        # forward
        if last_room_index + 2 > 3:
            forward = blrf_rooms_list[last_room_index - 2]
        else:
            forward = blrf_rooms_list[last_room_index + 2]
        
        # left
        if last_room_index + 1 > 3:
            left = blrf_rooms_list[0]
        else:
            left = blrf_rooms_list[last_room_index + 1]

        # right
        if last_room_index - 1 < 0:
            right = blrf_rooms_list[3]
        else:
            right = blrf_rooms_list[last_room_index - 1]
        
        blrf_rooms = [behind, left, right, forward]

        sentences = []
        blrf_directions = ["Behind you", "To your left", "To your right", "In front of you"]
        for i in range(0, len(blrf_rooms)):

            if blrf_rooms[i] != 0: 
                if isinstance(blrf_rooms[i], list): 
                    room_states = []
                    for x in (range(0, len(blrf_rooms[i]))):
                        if direct_list[i] in self.doors:
                            if self.doors[blrf_direct_list[i]] != None and self.doors[blrf_direct_list[i]][x] != None:
                                
                                if not self.doors[blrf_direct_list[i]][x].locked:
                                    if blrf_rooms[i][x].visited:
                                        room_states.append(("unlocked door visited", blrf_rooms[i][x]))
                                    else:
                                        room_states.append("unlocked door unknown")
                                else: 
                                    #needs to be here
                                    room_states.append("locked door") 

                            else:
                                if blrf_rooms[i][x].visited:
                                    room_states.append(("visited room", blrf_rooms[i][x]))
                                else:
                                    room_states.append("unknown room")

                        # Repeated due to if a door doesnt exist in this direction
                        else: 
                            if blrf_rooms[i][x].visited:
                                room_states.append(("visited room", blrf_rooms[i][x]))
                            else:
                                room_states.append("unknown room")
                    
                    sentences.append(room_states)

                # If there is only one room in a certain direction
                else: 
                    if self.has_doors and self.doors[blrf_direct_list[i]] != None: #

                        if not self.doors[blrf_direct_list[i]].locked:
                            if blrf_rooms[i].visited:
                                sentences.append(blrf_directions[i] + " there is an unlocked door that leads to the " + blrf_rooms[i].name)
                            else:
                                sentences.append(blrf_directions[i] + " there is an unlocked door that leads to an unknown room.")
                        else: 
                            sentences.append(blrf_directions[i] + " there is a locked door")
                    else: 
                        if blrf_rooms[i].visited:
                            sentences.append(blrf_directions[i] + " is " + blrf_rooms[i].name)
                        else:
                            sentences.append(blrf_directions[i] +  " is an unknown room")
            else:
                sentences.append(blrf_directions[i] + " there is a wall")
        
        paragraph_parts = self._build_complicated_adjacent_rooms_sentence(sentences)
        if none_or_one == None:
            full_paragraph = " ".join(paragraph_parts)
            return full_paragraph
        elif none_or_one == "backward":
            return paragraph_parts[0]
        elif none_or_one == "left":
            return paragraph_parts[1]
        elif none_or_one == "right":
            return paragraph_parts[2]
        elif none_or_one == "forward":
            return paragraph_parts[3]

        
    def _build_complicated_adjacent_rooms_sentence(self, room_states):
        blrf_directions = ["Behind you", "To your left", "To your right", "In front of you"]
        all_parts = []
        for i in range(0, len(room_states)):
            if isinstance(room_states[i], list):
                state_freq = {}
                state_rooms = {}
                for state in room_states[i]:
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

                paragraph_guide = ["visited room", "unlocked door visited", "unlocked door unknown", "locked door", "unknown room"]
                paragraph_parts = []
                paragraph_parts.append(blrf_directions[i])
                for i in range(0, len(paragraph_guide)):
                    if paragraph_guide[i] in state_freq.keys():
                        if i == 0:
                            paragraph_parts.append(f" is {state_rooms[paragraph_guide[i]].pop(0).name}")
                        elif i == 1:
                            paragraph_parts.append(f" is an unlocked door leading to {state_rooms[paragraph_guide[i]].pop(0).name}")
                        else:
                            # build a sentence using the keys and values from above
                            value_text = n2w.num2words(state_freq[paragraph_guide[i]])
                            vowels = ["a", "e", "i", "o", "u"]
                            if value_text == "one":
                                if paragraph_guide[i][0] in vowels:
                                    verb = "is an"
                                else:
                                    verb = "is a"
                                plural = ""
                                piece = "an "
                            else: 
                                verb = (f"are {value_text}")
                                plural = "s"
                                piece = ""

                            if paragraph_guide[i] == "unlocked door unknown":
                                paragraph_parts.append(f"{verb} locked door{plural} leading to {piece}unknown room{plural}")
                            elif paragraph_guide[i] == "locked door":
                                paragraph_parts.append(f"{verb} locked door{plural}")
                            elif paragraph_guide[i] == "unknown room":
                                paragraph_parts.append(f"{verb} unknown room{plural}")
                all_parts.append(paragraph_parts)
            
            else:
                all_parts.append(room_states[i])

            all_sentences = []
            for parts_set in all_parts:
                if isinstance(parts_set, list):
                    if len(parts_set[1:]) == 1:
                        full_sentence = " ".join(parts_set)
                        full_sentence += "."
                        all_sentences.append(full_sentence)
                    else:
                        full_sentence = ""
                        for i in range(0, len(parts_set)):
                            if i > 1:
                                if "is" in parts_set[i]:
                                    parts_set[i] = parts_set[i].replace("is ", "")
                                elif "are" in parts_set[i]:
                                    parts_set[i] = parts_set[i].replace("are ", "")
                                
                                # between the 2nd and 2nd to last item
                                if i > 1 and i < len(parts_set) - 1:
                                    full_sentence += (f", {parts_set[i]}")
                                
                                # the last item
                                elif i == len(parts_set) - 1:
                                    full_sentence += (f" and {parts_set[i]}.")

                            else:
                                if i == 0:
                                    full_sentence += (f"{parts_set[i]}")
                                else:
                                    full_sentence += (f" {parts_set[i]}")
 
                        all_sentences.append(full_sentence)

                else:
                    parts_set += "."
                    all_sentences.append(parts_set)
        
        return all_sentences
                    

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
    def __init__(self, name, description, door_label) -> None:
        super().__init__(name, description)
        self.label = door_label
        self.lights_on = True
    
    def __repr__(self) -> str:
        return f'{self.name}(ward room)'


class Basement_Room(Room):
    def __init__(self, name, description) -> None:
        super().__init__(name, description)
        self.lights_on = False
    
    def __repr__(self) -> str:
        return f'{self.name}(basement room)'

class Maze_Room(Room):
    def __init__(self, name, description) -> None:
        super().__init__(name, description)
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
        
        

