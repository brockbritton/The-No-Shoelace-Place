
# Global Functions for the Game Backend

# Combining dictionaries into one based on each key
def combine_dicts(old, new):
    for key in new:
        if isinstance(new[key], list):
            old[key].extend(new[key])
        elif isinstance(new[key], bool) or isinstance(new[key], tuple):
            old[key] = new[key]
        elif isinstance(new[key], dict):
            old[key] = _combine_update_value_dicts(old[key], new[key])
    return old

def _combine_update_value_dicts(old_dict, new_dict):
    for key, value in new_dict:
        old_dict[key] = value
    return old_dict

def parse_tuples(tuple_list, old_action_dict):
    dest, helper = tuple_list[0], tuple_list[1]
    new_action_dict = combine_dicts(old_action_dict, tuple_list[2])
    return dest, helper, new_action_dict

