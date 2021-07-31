
from pipeml.config.tree_elements.variable import SingleObjectTag


def get_statement(config_dict):
    """Chekcs if 'config_dict' is a statement. A statement is a key in the configuration in the following format:
    {
        object:np.array: { "object": [1,2,3,4] }
    }
    Here 'object' is the statement and 'np.array' the argument. Both values are returned

    Args:
        config_dict (any): A configuration

    Returns:
        dict: {
            "statement": The statement found (None if no statement found),
            "Argument": The argument found (None if no statement found)
        }
    """
    r = {
        "statement": None,
        "argument": None
    }

    if not isinstance(config_dict, dict): 
        return r
    if len(config_dict) != 1:
        return r
    key = list(config_dict.keys())[0]
    if not isinstance(key, str):
        return r
    split_key = key.split(":")
    if len(split_key) != 2:
        return r
    r = {
        "statement": split_key[0],
        "argument": split_key[1]
    }
    return r
    
def is_objects_list(config_dict):
    """Check if the given configuration is an objects list.

    Args:
        config_dict (any): A configuration

    Returns:
        bool: True if 'config_dict' is a dictionary that defines an objects list
    """
    if not isinstance(config_dict, list) or len(config_dict) == 0:
        return False
    for obj in config_dict:
        if not is_object(obj):
            return False
    return True

def is_object(config_dict):
    """Checks if the given configuration defines an object.

    Args:
        config_dict (any): A configuration

    Returns:
        bool: True if 'config_dict' is a dictionary that defines an object
    """
    if not isinstance(config_dict, dict):
        return False
    keys = list(config_dict.keys())
    return len(keys) == 1 and isinstance(keys[0], SingleObjectTag)

def is_var(config_dict):
    """Checks if the given configuration defines a variable

    Args:
        config_dict (any): A configuration

    Returns:
        bool: True if 'config_dict' defines a variable
    """
    # A variable can be a list of int, float, str, but not objects instances
    if is_objects_list(config_dict):
        return False
    return isinstance(config_dict, int) or isinstance(config_dict, float) or isinstance(config_dict, str) or isinstance(config_dict, list)
    
types_detectors = {
    "object": is_object,
    "objects_list": is_objects_list,
    "var": is_var
}

def get_type(config_dict):
    for object_name, detect_object in types_detectors.items():
        if detect_object(config_dict):
            return object_name
    return "config"