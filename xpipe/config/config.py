from . import objects
from . import tag
import yaml
import copy

"""
This module exposes the main functions of the xpipe library.
"""

def load_yaml(config_file : str):
    """Loads a configuration file and return a dictionary. This loader is able to load custom tags.

    Args:
        config_file (str): The path of the yaml config file
    
    Returns:
        dict: A dictionary containing a representation of the configuration.
    """
    tag.save_tags(yaml) # Set tags constructors and representers
    with open(config_file, "r") as stream:
        yaml_dict = yaml.safe_load(stream)
    return yaml_dict


def load_config(config_file : str):
    """Loads a configuration file and return a Config Object which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
    
    Returns:
        Config: A Config object
    """
    yaml_dict = load_yaml(config_file)
    return objects.construct("__root__", yaml_dict, parent=None, path=config_file)


def load_config_from_str(conf: str, base_path=None):
    """Loads a configuration from a string and return a Config Object which can instantiate the wanted objects.

    Args:
        conf (str): A configuration
        base_path (str): Simulate that 'conf' comes from this given path. It will be used if your conf contains relative paths. 
    
    Returns:
        Config: A Config object
    """
    tag.save_tags(yaml) # Set tags constructors and representers
    yaml_dict = yaml.safe_load(conf)
    return objects.construct("__root__", yaml_dict, parent=None, path=base_path)


def to_yaml(conf):
    """Converts a Config object to a yaml string

    Args:
        conf (Config): A configuration

    Returns:
        str: The corresponding yaml string
    """
    return conf._xpipe_to_yaml()


def to_dict(conf):
    """Converts a Config object to a dictionary.

    Args:
        conf (Config): A Config object

    Returns:
        dict: A multi-level dictionary containing a representation ogf the configuration.
    """
    return conf._xpipe_to_dict()


def _merge_aux(default_config, overwrite_config, inplace=False):
    """Merges two configurations.

    Args:
        default_config (Config): The default configuration
        overwrite_config (Config): The configuration to overwrite the default configuration with.

    Returns:
        Config: The merged configuration
    """

    if not inplace:
        default_config = copy.deepcopy(default_config)
    
    for key, value in overwrite_config.items():
        if key in default_config and isinstance(default_config[key], objects.Config) and isinstance(value, objects.Config):
            _merge_aux(default_config[key], value, inplace=True)
        else:
            default_config[key] = value

    return default_config


def merge(*confs, inplace=False):
    """Merges multiple configurations.

    Args:
        confs (Config): The configurations to merge

    Returns:
        Config: The merged configuration
    """
    if len(confs) == 0:
        return None
    if len(confs) == 1:
        return confs[0]
    
    if not inplace:
        confs = (objects.Config(),) + confs

    merged_conf = None
    for conf in confs[1:]:
        merged_conf = _merge_aux(confs[0], conf, inplace=True)
    
    return merged_conf


def get_node(config, path, delimiter="/", parent="..", attribute="."):
    """Gets a node from a configuration.

    Args:
        config (Config): The configuration
        path (str): The path of the node to get
        delimiter (str): The delimiter used to separate the path

    Returns:
        Config: The node
    """
    if path == "":
        return config
    split_path = path.split(delimiter)
    node = config

    def get_attr(node, attr_list):
        for attr in attr_list:
            try:
                node = getattr(node, attr)
            except AttributeError:
                raise AttributeError(f"Node does not have an attribute {attr}")
            return node

    for p in split_path:
        
        if p is not None and p[:len(parent) + 1] == parent:
            node = node._xpipe_parent
            p = p[len(parent) + 1:]
            if len(p) > 0:
                attrs = p.split(attribute)
                if len(attrs[0]) > 0:
                    raise ValueError(f"Invalid path {path}") 
                node = get_attr(node, attrs[1:])

        elif p is not None:
            split = p.split(attribute)
            node_name, attrs = split[0], split[1:]

            if node_name in node:
                node = node[node_name]
            else:
                raise ValueError(f"Path not found: {path}")
            if len(attrs) > 0:
                node = get_attr(node, attrs)
        else:
            raise ValueError(f"Path not found: {path}")
    return node


def get_base(node):
    """Return the root node of the given node (highest level node). 
    If the node is in an included configuration, the base node is the root node of the included configuration.

    Errors:
        ValueError: In case there is a circular reference

    Args:
        node (Node): The node to get the base node from
    """
    def aux(node, children=None):
        children = children or set()
        if node in children:
            raise ValueError("Circular reference detected")
        if node._xpipe_parent is None or isinstance(node, objects.IncludedConfig):
            return node
        children.add(node)
        return aux(node._xpipe_parent, children)
    return aux(node)
        

def set_parent(node, parent):
    """Sets the parent of a node.

    Args:
        node (Node): The node to set the parent of
        parent (Node): The parent node
    """
    object.__setattr__(node, "_xpipe_parent", parent)


def set_name(node, name):
    """Sets the name of a node.

    Args:
        node (Node): The node to set the name of
        name (str): The name of the node
    """
    object.__setattr__(node, "_xpipe_name", name)


def set_config_dict(node, config_dict):
    """Sets the node config dict

    Args:
        node (Node): Node
        config_dict (dict): The config dict of the node
    """
    object.__setattr__(node, "_xpipe_config_dict", config_dict)
