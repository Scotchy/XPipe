# from .template import Template
import pdb
from .utils import get_statement, is_include, is_object, is_objects_list, is_var
from .objects import SingleObject, ObjectsList, Variable, Include, Parameters
import yaml
from .node import Node
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__all__ = ["Config"]

class Config(Node):

    def __init__(self, config_dict, name=None):
        if name == "root":
            raise ValueError("Forbidden name 'root' in yaml file.")
        if name is None:
            name = "root"
        super(Config, self).__init__(name, config_dict)
        self.config_dict = config_dict

    def _check_valid(self, name, config_dict):
        return True

    @property
    def is_root(self):
        return self.name == "root"

    def _construct(self, name, sub_config):
        for name, sub_config in sub_config.items():
            self.set_node(name, sub_config)

    def set_node(self, name, sub_config):
        if is_var(sub_config):
            setattr(self, name, Variable(name, sub_config))

        elif is_object(sub_config):
            
            setattr(
                self, 
                name, 
                SingleObject(
                    name, 
                    sub_config
                )
            )
        elif is_objects_list(sub_config):
            sub_configs = []
            # for sc in sub_config:
            #     sub_name, sub_sc = list(sc.items())[0]
            #     sub_configs.append(Config(sub_sc, sub_name))
                
            setattr(
                self, 
                name, 
                ObjectsList(
                    name, 
                    sub_config
                )
            )
        elif is_include(sub_config):
            # Load the configuration file
            path = get_statement(sub_config)["argument"]
            with open(path, "r") as f:
                conf = yaml.load(f, Loader=yaml.Loader)
            conf = {name: conf}
            self._construct(name, conf)
            # Note that if some conf keys are present in an included file and in the current file
            # They will overwrite each other (depending their order in the configuration file)  
        elif isinstance(sub_config, dict):

            setattr(self, name, Config(sub_config, name)) # Create an attribute containing the config stored in 'key'
        else: 

            raise ValueError(f"Yaml file format not supported ({name} : {type(sub_config)})")

    def __str__(self):
        raise NotImplementedError()

def load_config(config_file : str, template=None):
    """Load a configuration file and return an ObjectLoader which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
        template (Template): A template containing information of how to load objects defined in the configuration file
    """
    with open(config_file, "r") as stream:
        yaml_dict = yaml.load(stream, Loader=Loader)
    return Config(yaml_dict)
