
import random
import game_backend.objects.events as event
import game_backend.objects.rooms as room


class Calendar:
    def __init__(self, player) -> None:
        self.days_list = []
        self.max_turns_daily = 12 #30
        self.activities_offered = []
        self.next_day(player)

    def __repr__(self) -> str:
        return '(calendar)'

    def next_day(self, player):
        # Player stats values are updated on initialized Day object
        new_day = _Day(self.max_turns_daily, len(self.days_list) + 1)
        self.days_list.append(new_day)
        player.loc = player.home_room

    def _get_curr_day_data(self):
        #return current day, turns left
        return self.days_list[-1].day_number, self.days_list[-1].turns_left

    def use_turns(self, num, player):
        actions = {
            'print_all': [],
        }
        self.days_list[-1].turns_left -= num
        if self.days_list[-1].turns_left == 0: 
            actions['print_all'].append(f"Day {self.days_list[-1].day_number} is ending. You have no more turns left. You have returned to your room and have fallen asleep.")
            self.next_day(player)
            actions['print_all'].append(f"Day {self.days_list[-1].day_number} is beginning. You have {self.days_list[-1].turns_left} turns left. You are currently in {player.loc.name}.")

        return actions


    def calculate_next_activity(self):
        all_groups = [event.meditation_group, event.catharsis_group, event.assert_group, event.opp_action_group, event.pos_attitude_group]
        return all_groups[random.randint(0, len(all_groups) - 1)]
            

class _Day:
    def __init__(self, turns, day) -> None:
        self.day_number = day
        self.turns_left = turns
        self.activity1 = None
        self.activity2 = None

    def __repr__(self) -> str:
        return '(day)'

