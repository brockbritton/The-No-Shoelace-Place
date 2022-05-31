import random


class Ability:

    def __init__(self, display_name, base_damage, conditions_list) -> None:
        self.name = display_name
        self.damage = base_damage
        self.affects = conditions_list
        self.lvl = 0

    def __repr__(self) -> str:
        return f'{self.name}(ability)'



class Coping_Skill(Ability):
    def __init__(self, display_name, base_healing, possible_condition, lvl_ui_value) -> None:
        super().__init__(display_name, None, possible_condition)
        self.base_healing = base_healing
        self.lvl_ui_value = lvl_ui_value
        self.lvl_xp_reqs = {
            1: 100, 
            2: 200,
            3: 300,
            4: 400,
            5: 500,
        }

    def upgrade_ability(self, helper_list, player): 
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False,
            'update_ui_values': [],
        }
        self.lvl += 1
        if self.damage != None:
            self.damage *= self.lvl
        if isinstance(self.affects, list):
            for c in self.affects:
                #c.upgrade_condition()  #this is a condition
                pass
        
        player.earn_xp(-1 * helper_list[0])
        if self.lvl == 1:
            actions['print_all'].append(f"You have learned {self.name}!")
        else:
            actions['print_all'].append(f"You have leveled up {self.name} to level {self.lvl}!")
        actions['update_ui_values'] = ["xp_value", self.lvl_ui_value]

        return (None, None, actions)


class Demon_Skill(Ability):
    def __init__(self, display_name, base_damage, possible_condition) -> None:
        super().__init__(display_name, base_damage, possible_condition)
        self.lvl = 3
