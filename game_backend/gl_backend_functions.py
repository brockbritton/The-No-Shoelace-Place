
# Global Functions for the Game Backend

# Combining dictionaries into one based on each key
def combine_dicts(old, new):
    for key in new:
        if isinstance(new[key], list):
            old[key].extend(new[key])
        elif isinstance(new[key], bool) or isinstance(new[key], tuple):
            old[key] = new[key]
    return old

