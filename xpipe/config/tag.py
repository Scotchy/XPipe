
tags = {}


def register(yaml_tag):
    """Register a class such that it can be instantiated from a yaml tag

    Args:
        yaml_tag (str): The corresponding tag to instantiate the registered class
    """        
    def register_aux(tag_class):
        tag_class.yaml_tag = yaml_tag
        tags[yaml_tag] = tag_class
        return tag_class

    return register_aux


def save_tags(yaml):
    """Register all classes that have @tags.register to the given yaml library. 
    Yaml will then be able to load them when needed.

    Args:
        yaml (lib): The yaml library
    """    
    for tag, tag_class in tags.items():
        yaml.SafeLoader.add_constructor(tag, tag_class.from_yaml)
        yaml.SafeDumper.add_multi_representer(tag_class, tag_class.to_yaml)