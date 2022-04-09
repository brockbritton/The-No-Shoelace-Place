
import random
import game_backend.objects.events as event


class Calendar:
    def __init__(self) -> None:
        self.days_list = []
        self.max_turns_daily = 15
        self.activities_offered = []
        self.next_day()

    def __repr__(self) -> str:
        return f'(calendar)'


    def next_day(self):
        # Player stats values are updated on initialized Day object
        new_day = _Day(self.max_turns_daily, len(self.days_list))
        self.days_list.append(new_day)

    def use_turns(self, num):
        actions = {
            'print_all': [],
            'build_multiple_choice': [],
            'ask_y_or_n': False
        }
        self.days_list[-1].turns_left -= num
        if self.days_list[-1].turns_left == 0:
            actions['print_all'].append("The old day is ending...")
            self.next_day()
            actions['print_all'].append("The new day is beginning...")

        else:
            #gui_cal.settk(gui_cal.turns_value, gui_cal.gettk(gui_cal.turns_value, 0) - num)
            pass

        return actions


    def calculate_next_activity(self):
        all_groups = [event.meditation_group, event.catharsis_group, event.assert_group, event.opp_action_group, event.pos_attitude_group]
        all_guides = [event.guide_to_outside]
        if random.randint(0, 2) == 3: 
            # should be == 0, not building guides right now
            self.activities_offered.append((all_guides[0], None))
            return all_guides[0]
        else:
            if len(self.activities_offered) < 5:
                for act in all_groups:
                    if act not in self.activities_offered:
                        self.activities_offered.append((act, None))
                        return act
            else:
                act_dict = {}
                for act in self.activities_offered:
                    if act not in act_dict.keys():
                        act_dict[act] = 1
                    else:
                        act_dict[act] += 1

                act_num = random.randint(0, len(self.activities_offered) - 1)
                curr_act = 0
                for act in act_dict:
                    if curr_act + (len(self.activities_offered) - act_dict[act]) >= act_num:
                        self.activities_offered.append((act, None))
                        return act
                    

class _Day:
    def __init__(self, turns, day) -> None:
        self.day_number = day
        self.turns_left = turns
        #gui_cal.settk(gui_cal.day_value, day)
        #gui_cal.settk(gui_cal.turns_value, turns)
        self.activity1 = None
        self.activity2 = None


