from . import objects as objects
import yaml
from .tags import Tags
import yaml
import copy

def load_config(config_file : str, template=None):
    """Loads a configuration file and return a Config Object which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
    
    Returns:
        Config: A Config object
    """
    Tags.save_tags(yaml) # Set tags constructors and representers
    with open(config_file, "r") as stream:
        yaml_dict = yaml.safe_load(stream)
    return objects.Config("__root__", yaml_dict)

def load_yaml(config_file : str):
    """Loads a configuration file and return a Config Object which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
    
    Returns:
        Config: A Config object
    """
    Tags.save_tags(yaml) # Set tags constructors and representers
    with open(config_file, "r") as stream:
        yaml_dict = yaml.safe_load(stream)
    return yaml_dict

def load_config_from_str(conf: str):
    """Loads a configuration from a string and return a Config Object which can instantiate the wanted objects.

    Args:
        conf (str): A configuration
    
    Returns:
        Config: A Config object
    """
    Tags.save_tags(yaml) # Set tags constructors and representers
    yaml_dict = yaml.safe_load(conf)
    return objects.Config("__root__", yaml_dict)

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

def merge(default_config, overwrite_config, inplace=False):
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
            default_config[key] = merge(default_config[key], value, inplace=inplace)
        else:
            default_config[key] = value

    return default_config

def multi_merge(*confs, inplace=False):
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
    
    merged_conf = None
    for conf in confs[1:]:
        merged_conf = merge(confs[0], conf, inplace=inplace)
    
    return merged_conf

def get_node(config, path, delimiter="."):
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
    path = path.split(delimiter)
    node = config
    for p in path:
        if node is None:
            import pdb; pdb.set_trace()
        if p in node:
            node = node[p]
        else:
            raise ValueError("Path not found: {}".format(path))
    return node

def get_base(node):

    def aux(node, children=None):
        children = children or set()
        if node in children:
            raise ValueError("Circular reference detected")
        if node._xpipe_parent is None or isinstance(node, objects.IncludedConfig):
            return node
        children.add(node)
        return aux(node._xpipe_parent, children)
    return aux(node)
        
