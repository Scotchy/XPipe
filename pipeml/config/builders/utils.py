
from .config_dict_builder import ConfigDictBuilder
from .objects_list_builder import ObjectsListBuilder
from .single_object_builder import SingleObjectBuilder
    
def is_objects_list(conf):
    """Check if the given configuration is an objects list.

    Args:
        conf (any): A configuration

    Returns:
        bool: True if 'conf' is a dictionary that defines an objects list
    """
    if not isinstance(conf, list) or len(conf) == 0:
        return False
    for obj in conf:
        if not is_single_object(obj):
            return False
    return True

def is_single_object(conf):
    """Checks if the given configuration defines an object.

    Args:
        conf (any): A configuration

    Returns:
        bool: True if 'conf' is a dictionary that defines an object
    """
    if not isinstance(conf, dict):
        return False
    keys = list(conf.keys())
    return len(keys) == 1 and isinstance(keys[0], SingleObjectTag)

def is_var(conf):
    """Checks if the given configuration defines a variable

    Args:
        conf (any): A configuration

    Returns:
        bool: True if 'conf' defines a variable
    """
    # A variable can be a list of int, float, str, but not objects instances
    if isinstance(conf, list):
        for el in conf:
            if is_single_object(el):
                return False
        return True
        
    return isinstance(conf, int) or isinstance(conf, float) or isinstance(conf, str) or isinstance(conf, list)

def is_list(conf):
    return is_var(conf) and isinstance(conf, list)

def get_builder(conf):
    
    # Note that the order of the checks is important
    builder_checkers = [
        (SingleObjectBuilder, is_single_object),
        (ObjectsListBuilder, is_objects_list),
        (ConfigDictBuilder, is_dict)
    ]
    for builder, can_build in builder_checkers:
        if can_build(conf):
            return builder
    raise Exception(f"Configuration cannot be parsed: {conf}")