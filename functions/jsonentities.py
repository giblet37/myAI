"""
Look for Entity values from the NLU json objs


"""


def find_value(json_input, lookup_key):
    global value
    value = None
    if isinstance(json_input, list):
        for item in json_input:
            value = find_entity(item, lookup_key)
            if value is not None:
                break
    else:
        value = find_entity(json_input, lookup_key)
    return value


def find_entity(json_input, lookup_key):
    val = None
    if isinstance(json_input, dict):
        if json_input['entity'] == lookup_key:
            val = json_input['value']
    return val