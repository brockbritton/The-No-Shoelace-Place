
import game_backend.classes.ability_class as ability_class

#### Conditions for Abilities ####
negate_stat_changes = 0
healing = 0 # Healing
boost_attack = 0 # Multiplier Boost
attack_first = 0

reduce_attack = 0
lose_turn = 0
fatigue = 0
double_attack = 0
extra_turn = 0
defenseless = 0
attack_last = 0

#### Character Attacks / Abilities ####
catharsis = ability_class.Coping_Skill("Catharsis", 20, None)
meditation = ability_class.Coping_Skill("Meditation", 0, [negate_stat_changes, healing])
assertiveness = ability_class.Coping_Skill("Assert Yourself", 10, [attack_first])
opposite_action = ability_class.Coping_Skill("Opposite Action", None, [attack_last, double_attack])
pos_attitude = ability_class.Coping_Skill("Stay Positive", 5, [boost_attack])


#### Demon Attacks / Abilities ####

## Depression Demon ##
pessimism = ability_class.Demon_Skill("Pessimism", 5, [reduce_attack]) # recurring damage
lethargy = ability_class.Demon_Skill("Lethargy", 0, [fatigue])
disordered_eating = ability_class.Demon_Skill("Disordered Eating", 25, [reduce_attack])
concentration = ability_class.Demon_Skill("Lack of Concentration", 10, [lose_turn]) 

## Anxiety Demon ##
panic = ability_class.Demon_Skill("Self Doubt", 15, [double_attack])  
self_doubt = ability_class.Demon_Skill("Self Doubt", 20, [reduce_attack])
insomnia = ability_class.Demon_Skill("Insomnia", 10, [extra_turn]) # recurring damage
avoidance = ability_class.Demon_Skill("Avoidance", 0, [lose_turn])

## PTSD Demon ##
trauma = ability_class.Demon_Skill("Trauma", 30, None)
emotional_distress = ability_class.Demon_Skill("Emotional Distress", 5, [reduce_attack]) ##
nightmares = ability_class.Demon_Skill("Nightmares", 30, None) #requires the attacked to to be asleep #is recurring while the attacked stays asleep
lethargy = ability_class.Demon_Skill("Lethargy", 0, [fatigue])  

## Apathy Demon ##
lethargy = ability_class.Demon_Skill("Lethargy", 0, [fatigue]) 
numbness = ability_class.Demon_Skill("Numbness", 15, [reduce_attack, negate_stat_changes]) 
passiveness = ability_class.Demon_Skill("Passiveness", 20, [defenseless]) 
dependence = ability_class.Demon_Skill("Dependence", 10, [attack_last]) 