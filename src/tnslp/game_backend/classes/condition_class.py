
import random


class Condition:
    def __init__(self, name, odds, recurring, lvl) -> None:
        self.name = name
        self.lvl = lvl #turns are equal to lvl
        self.odds = odds
        self.recur = recurring
    
    def __repr__(self) -> str:
        return f'{self.name}(condition)'


    def upgrade_condition(self):
        self.lvl += 1

    def check_condition_hit(self):
        check = random.randint(0, self.odds)
        if check == 0:
            return True
        else:
            return False

class HP_Condition(Condition):
    # base hp damage or heal, "heal" or "damage"
    def __init__(self, name, odds, recurring, hp, action, lvl) -> None:
        super().__init__(name, odds, recurring, lvl)
        self.affected_hp = hp
        self.action = action

    def execute(self):
        if not self.recur:
            return self.action, self.affected_hp * self.lvl
        else:
            # action, [hp mod, turns]
            return self.action, [self.affected_hp * self.lvl, self.lvl]

class Percent_Modifier(Condition):
    def __init__(self, name, odds, recurring, perc, lvl, to_mod) -> None:
        super().__init__(name, odds, recurring, lvl)
        # above 100 is increase, below 100 is decrease
        # add 10 to the perc to upgrade
        self.perc = perc
        self.modify = to_mod

    def execute(self):
        if not self.recur:
            if self.perc > 1.0:
                return self.modify, self.perc + (.1 * self.lvl)
            elif self.perc < 1.0:
                return self.modify, self.perc - (.1 * self.lvl)
        else:
            # whats being modded, [new perc, turns]
            if self.perc > 1.0:
                return self.modify, [self.perc + (.1 * self.lvl), self.lvl]
            elif self.perc < 1.0:
                return self.modify, [self.perc - (.1 * self.lvl), self.lvl]

class Mod_Attack_Seq(Condition):
    def __init__(self, name, odds, recurring, action, lvl) -> None:
        super().__init__(name, odds, recurring, lvl)
        # action = attack_first, lose_turn, extra_turn, attack_last
        self.action = action

    def execute(self):
        if not self.recur:
            return self.action
        else:
            # whats being modded, [new perc, turns]
           return self.action, self.lvl

class Negate_Mods(Condition):
    def __init__(self, name, odds, recurring, lvl, negate_list) -> None:
        super().__init__(name, odds, recurring, lvl)
        self.negated = negate_list

    def execute(self):
        if not self.recur:
            return self.negated
        else:
            # whats being modded, [new perc, turns]
           return self.negated, self.lvl

    
