
from numpy import isin


def is_objects_list(name, config_dict):
    """Check if the given configuration is an objects list.

    Args:
        config_dict (any): A configuration

    Returns:
        bool: True if 'config_dict' is a dictionary that defines an objects list
    """
    from . import objects
    
    if not isinstance(config_dict, list) or len(config_dict) == 0:
        return False

    for obj in config_dict:
        
        if not isinstance(obj, dict) or len(obj) <= 0:
            return False
        
        obj, params = list(obj.items())[0]
        if not isinstance(obj, objects.SingleObject):
            return False

    return True


def is_var(name, config_dict):
    """Checks if the given configuration defines a Variable

    Args:
        config_dict (any): A configuration

    Returns:
        bool: True if 'config_dict' defines a Variable
    """  
    return isinstance(config_dict, int) or isinstance(config_dict, float) or isinstance(config_dict, str)


def is_list(name, config_dict):
    """Check if the given configuration is an objects.List.

    Args:
        name (str): Name of the variable
        config_dict (dict): A configuration

    Returns:
        bool: True if 'config_dict' is an objects.List.
    """    
    return not is_objects_list(name, config_dict) and isinstance(config_dict, list)


def is_config(name, config_dict):
    """Check if the given configuration is a objects.Config.

    Args:
        name (str): Name of the variable
        config_dict (dict): A configuration

    Returns:
        bool: True if 'config_dict' is a objects.Config
    """
    return isinstance(config_dict, dict)


def valid_var_name(name : str):
    """Raise an error if 'name' is not a valid Variable name.
    A valid variable name is a string that starts with a letter or an underscore and is followed by letters, numbers, or underscores.

    Args:
        name (str): Name of the variable

    Raises:
        ValueError: If name contains caracters that are not alphabetical or numerical
        ValueError: If name begin with a number
    """
    if name == "":
        return
    stripped_name = name.replace("_", "")
    if stripped_name == "":
        raise ValueError(f"Variable '{name}' cannot contain only underscores.")
    if not stripped_name.isalnum():
        raise ValueError(f"Variable '{name}' must contain alphabetical or numerical caracters or underscores.")
    if not name[0].isalpha() or name[0] == "_":
        raise ValueError(f"Variable '{name}' must begin with an alphabetical caracter or an underscore.")
    
    return True