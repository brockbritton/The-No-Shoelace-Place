
import random


class NPC:
    def __init__(self, name) -> None:
        self.name = name

    def set_location(self, loc):
        self.loc = loc


class Demon(NPC):

    def __init__(self, name) -> None:
        super().__init__(name)
        self.name = name
        self.base_health = 100
        self.curr_health = self.base_health
        self.past_tense_attack = []
        self.given_attacks = []

    def __repr__(self) -> str:
        return f'{self.name}(demon)'


    def monst_deal_damage(self):
        return self.level * random.randint(1, 5)

    def monst_take_damage(self, damage):
        self.health -= damage


    def monst_take_turn(self):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        if self.health < self.max_health / 6 and self.health > 0:
            actions['print_all'].append("The " + self.species + " escaped") #its not actually moving?
            self.escape() #depreciated
            return (0, "flee", actions)
        else:
            damage = self.monst_deal_damage()
            if random.randint(0,6) == 0:
                affect = self.attribute
                if affect == "posion":
                    actions['print_all'].append("You have been poisoned!")
                if affect == "bleeding":
                    actions['print_all'].append("You are now bleeding!")
            else: 
                affect = None
            
            return (damage, affect, actions)

class Depression(Demon):
    def __init__(self, name):
        super().__init__(name)
        self.past_tense_attack = []
        self.given_attacks = []

