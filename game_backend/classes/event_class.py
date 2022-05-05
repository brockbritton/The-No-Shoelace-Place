
class Event:

    def __init__(self, name, turns) -> None:
        self.name = name 
        self.turns = turns

    def execute_event(self, y_or_n):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        if y_or_n == "y":
            actions['print_all'].extend(self.describe_event())
            return (None, self.turns, actions)
        else:
            actions['print_all'].append("You did not attend this event")
            return (None, None, actions)

    def describe_event(self):
        return ["This is a test description of an event"]
        
        
class Coping_Skill_Group(Event):
    def __init__(self, name, ability) -> None:
        super().__init__(name, 3)
        self.affected_ability = ability
    
    def __repr__(self) -> str:
        return f'{self.name}(coping skill group)'


    def ask_event(self):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }

        actions['print_all'].append(f"There is a {self.name} coping skills group starting soon. Would you like to attend?")
        actions['ask_y_or_n'] = True
        return ("execute_event", self, actions)

    def describe_event(self):
        phrases = []
        phrases.append(f"In attending the {self.name} coping skills group,")
        if self.affected_ability.lvl == 5:
            phrases.append(f"you reviewed many ideas and philosophies, but you have already learned all you can about the skill of {self.affected_ability.name}.")
        else:
            self.affected_ability.lvl += 1
            if self.affected_ability.lvl == 1:
                # print: You have learned the skill of self.affected_ability.name
                phrases.append(f"you have learned the skill of {self.affected_ability.name}.")

            else:
                phrases.append(f"you have learned more about the skill of {self.affected_ability.name}.")
        
        return (" ".join(phrases))
            

class Guided_Path(Event):
    def __init__(self, name, moves, room_path, optional_bool) -> None:
        super().__init__(name, moves)
        self.room_path = room_path
        self.optional = optional_bool
        self.start = self.room_path[0]
        self.end = self.room_path[-1]

    def __repr__(self) -> str:
        return f'{self.name}(guided path)'

    def ask_event(self):
        # to be built later
        pass

    def describe_event(self):
        # Print description of rooms through self.start and self.end
        pass



    

