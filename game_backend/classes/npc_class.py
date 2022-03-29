
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

    def escape(self):
        while True:
            direction = random.randint(1,4)
            if direction == 1 and self.loc.north != 0:
                gui_npc.printtk("The " + self.species + " escaped to the north!")
                self.loc = self.loc.north
                break
            elif direction == 2 and self.loc.east != 0:
                gui_npc.printtk("The " + self.species + " escaped to the east!")
                self.loc = self.loc.east
                break
            elif direction == 3 and self.loc.south != 0:
                gui_npc.printtk("The " + self.species + " escaped to the south!")
                self.loc = self.loc.south
                break
            elif direction == 4 and self.loc.west != 0:
                gui_npc.printtk("The " + self.species + " escaped to the west!")
                self.loc = self.loc.west
                break

    def monst_take_turn(self):
        if self.health < self.max_health / 6 and self.health > 0:
            gui_npc.printtk("The " + self.species + " escaped") #its not actually moving?
            self.escape()
            return 0, "flee"
        else:
            damage = self.monst_deal_damage()
            if random.randint(0,6) == 0:
                affect = self.attribute
                if affect == "posion":
                    gui_npc.printtk("You have been poisoned!")
                if affect == "bleeding":
                    gui_npc.printtk("You are now bleeding!")
            else: 
                affect = None
            
            return damage, affect

class Depression(Demon):
    def __init__(self, name):
        super().__init__(name)
        self.past_tense_attack = []
        self.given_attacks = []


        

def set_npc_gui(gui_window):
    global gui_npc
    gui_npc = gui_window