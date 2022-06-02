
import random

import game_backend.objects.events as event


class Calendar:
    def __init__(self) -> None:
        self.days_list = []
        self.max_turns_daily = 30
        self.activities_offered = []
        self.next_day()

    def __repr__(self) -> str:
        return f'(calendar)'

    def next_day(self):
        # Player stats values are updated on initialized Day object
        new_day = _Day(self.max_turns_daily, len(self.days_list))
        self.days_list.append(new_day)

    def _get_curr_day_data(self):
        #return current day, turns left
        return self.days_list[-1].day_number, self.days_list[-1].turns_left

    def use_turns(self, num):
        actions = {
            'print_all': [],
            'update_ui_values': [],
        }
        self.days_list[-1].turns_left -= num
        if self.days_list[-1].turns_left == 0: 
            actions['print_all'].append("The old day is ending...")
            self.next_day()
            actions['update_ui_values'].append("day_value")
            actions['print_all'].append("The new day is beginning...")

        actions['update_ui_values'].append("turns_value")
        return actions


    def calculate_next_activity(self):
        all_groups = [event.meditation_group, event.catharsis_group, event.assert_group, event.opp_action_group, event.pos_attitude_group]
        all_guides = [event.guide_to_outside]
        if random.randint(0, 2) == 3:
            # should be == 0, not building guides right now
            self.activities_offered.append(all_guides[0])
            return all_guides[0]
        else:
            return all_groups[random.randint(0, len(all_groups) - 1)]
            

class _Day:
    def __init__(self, turns, day) -> None:
        self.day_number = day
        self.turns_left = turns
        self.activity1 = None
        self.activity2 = None

    def __repr__(self) -> str:
        return f'(day)'

