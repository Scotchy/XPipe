
from pipeml.config.tree_elements import config
import pipeml.config.tree_elements.variables as variables


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
    return len(keys) == 1 and isinstance(keys[0], variables.SingleObjectTag)


def is_var(config_dict):
    """Checks if the given configuration defines a variable

    Args:
        config_dict (any): A configuration

    Returns:
        bool: True if 'config_dict' defines a variable
    """
    # A variable can be a list of int, float, str, but not objects instances
    if isinstance(config_dict, list):
        for el in config_dict:
            if is_object(el):
                return False
        return True
        
    return isinstance(config_dict, int) or isinstance(config_dict, float) or isinstance(config_dict, str) or isinstance(config_dict, list)


def is_list(config_dict):
    return is_var(config_dict) and isinstance(config_dict, list)

def is_config(config_dict):
    return isinstance(config_dict, dict)