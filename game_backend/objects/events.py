

import game_backend.classes.event_class as event_class
import game_backend.objects.rooms as room
import game_backend.objects.abilities as ability

guide_to_outside = event_class.Guided_Path("Guided Path to Outside", 5, [room.common_room, room.service_hallway, room.outside_time], True)
guide_to_cr = event_class.Guided_Path("Guided Path to Outside", 5, [room.outside_time, room.service_hallway, room.common_room], False)

meditation_group = event_class.Coping_Skill_Group("Meditation", ability.meditation)
catharsis_group = event_class.Coping_Skill_Group("Catharsis", ability.catharsis)
assert_group = event_class.Coping_Skill_Group("Assertiveness", ability.assertiveness)
opp_action_group = event_class.Coping_Skill_Group("Opposite Action", ability.opposite_action)
pos_attitude_group = event_class.Coping_Skill_Group("Positive Attitude", ability.pos_attitude)