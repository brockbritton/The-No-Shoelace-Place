
class Event:

    def __init__(self, name, turns) -> None:
        self.name = name 
        self.turns_spent = turns

    def __repr__(self) -> str:
        return f'{self.name}(event)'
        
        
class Coping_Skill_Group(Event):
    def __init__(self, name, ability) -> None:
        super().__init__(name, 3)
        self.affected_ability = ability
    
    def ask_event(self):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }

        actions['print_all'].append(f"There is a {self.name} coping skills group starting soon. Would you like to attend?")
        actions['ask_y_or_n'] = True
        return ("execute_event", self, actions)

    def execute_event(self, y_or_n, player):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        if y_or_n == "y":
            for ability in player.abilities:
                if ability.name == self.affected_ability.name:
                    player_ability = player.abilities[player.abilities.index(ability)]
            if player_ability.lvl == 5:
                actions['print_all'].append(f"You reviewed many ideas and philosophies, but you have already learned all you can {player_ability.name}.")
                return (None, self.turns_spent, actions)
            else:
                req_xp = player_ability.lvl_xp_reqs[player_ability.lvl + 1]
                if player.xp >= req_xp:
                    if player_ability.lvl == 0:
                        actions['print_all'].append(f"Would you like to use {req_xp} experience to learn {player_ability.name}?")
                    else:
                        actions['print_all'].append(f"Would you like to use {req_xp} experience to level up {player_ability.name}?")
                    actions['ask_y_or_n'] = True
                    return ("level_up_ability", [player_ability, req_xp, self.turns_spent], actions)
                else:
                    if player_ability.lvl == 0:
                        actions['print_all'].append(f"Unfortunately you do not have enough experience to learn {player_ability.name}?")
                    else:
                        actions['print_all'].append(f"Unfortunately you do not have enough experience to level up {player_ability.name}?")
                    return (None, self.turns_spent, actions)
 
        else:
            actions['print_all'].append("You did not attend this event")
            return (None, None, actions)
            

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

    def execute_event(self, y_or_n):
        # to be built later
        pass


    

