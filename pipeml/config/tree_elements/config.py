# from .template import Template
from .objects import Config
import yaml
from .tags import Tags
import yaml

def load_config(config_file : str, template=None):
    """Load a configuration file and return an ObjectLoader which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
        template (Template): A template containing information of how to load objects defined in the configuration file
    """
    Tags.save_tags(yaml) # Set tags constructors and representers
    with open(config_file, "r") as stream:
        yaml_dict = yaml.safe_load(stream)
    return Config("__root__", yaml_dict)
