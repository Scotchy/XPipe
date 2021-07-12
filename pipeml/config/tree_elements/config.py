# from .template import Template
import pdb
from .utils import get_statement, is_include, is_object, is_objects_list, is_var
from .objects import Config, SingleObject, ObjectsList, Variable, Include, Parameters
import yaml
from .node import Node
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def load_config(config_file : str, template=None):
    """Load a configuration file and return an ObjectLoader which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
        template (Template): A template containing information of how to load objects defined in the configuration file
    """
    with open(config_file, "r") as stream:
        yaml_dict = yaml.load(stream, Loader=Loader)
    return Config(yaml_dict)
