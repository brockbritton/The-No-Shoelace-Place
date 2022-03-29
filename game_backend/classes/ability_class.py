import random


class Ability:

    def __init__(self, display_name, base_damage, conditions_list) -> None:
        self.name = display_name
        self.damage = base_damage
        self.affect = conditions_list
        self.lvl = 0

    def __repr__(self) -> str:
        return f'{self.name}(ability)'


    def upgrade_ability(self): 
        self.lvl += 1
        self.damage *= self.lvl
        for c in self.affect:
            c.upgrade_condition()  #this is a condition


class Coping_Skill(Ability):
    def __init__(self, display_name, base_healing, possible_condition) -> None:
        super().__init__(display_name, None, possible_condition)
        self.base_healing = base_healing

    def level_up(self, multiplier):
        self.damage = self.damage * multiplier
        self.effect_turns = self.effect_turns * multiplier


class Demon_Skill(Ability):
    def __init__(self, display_name, base_damage, possible_condition) -> None:
        super().__init__(display_name, base_damage, possible_condition)
        self.lvl = 3
