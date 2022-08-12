
import random
import tnslp.game_backend.objects.abilities as ability


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
        self.health = self.base_health
        self.attacks = []

    def __repr__(self) -> str:
        return f'{self.name}(demon)'


class Depression_Demon(Demon):
    def __init__(self):
        super().__init__("Depression")
        self.attacks = [ability.pessimism, ability.lethargy, ability.disordered_eating, ability.concentration]

class Anxiety_Demon(Demon):
    def __init__(self):
        super().__init__("Anxiety")
        self.attacks = [ability.panic, ability.self_doubt, ability.insomnia, ability.avoidance]

class PTSD_Demon(Demon):
    def __init__(self):
        super().__init__("PTSD")
        self.attacks = [ability.trauma, ability.emotional_distress, ability.nightmares, ability.lethargy]

class Apathy_Demon(Demon):
    def __init__(self):
        super().__init__("Apathy")
        self.attacks = [ability.numbness, ability.passiveness, ability.dependence, ability.lethargy]

        
        

