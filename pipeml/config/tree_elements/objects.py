from .node import Node
import importlib
from .utils import is_object, is_objects_list, is_var, is_list, is_config
import pipeml.config.tree_elements.variables as variables
from collections.abc import Mapping

__all__ = ["Config", "SingleObject", "ObjectsList", "Parameters"]

class Config(Node, Mapping):

    def __init__(self, name, config_dict):
        self._pipeml_config_dict = config_dict
        self._pipeml_properties = {}
        Node.__init__(self, name, config_dict)

    def _pipeml_check_valid(self, name, config_dict):
        return True

    def _pipeml_construct(self, name, sub_config):
        for name, sub_config in sub_config.items():
            # self.set_node(name, sub_config)
            node = construct(name, sub_config)
            self._pipeml_properties[name] = node

    def _pipeml_to_yaml(self, n_indents=0):
        r = []
        for key, value in self.items():
            el = "  " * n_indents
            el += f"{key}: "
            if isinstance(value, Config) or isinstance(value, ObjectsList):
                el += "\n"
            el += f"{value._pipeml_to_yaml(n_indents=n_indents + 1)}"
            r += [el]
        joiner = "\n\n" if self._name == "__root__" else "\n"
        return joiner.join(r)

    def _pipeml_to_dict(self):
        return { k: v._pipeml_to_dict() for k, v in self.items() }
    
    def __getattribute__(self, prop: str):
        properties = super(Node, self).__getattribute__("_pipeml_properties")
        if prop in properties:
            return properties[prop]
        else:
            try: 
                return super(Node, self).__getattribute__(prop)
            except:
                raise AttributeError(f"'{self._pipeml_name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")

    def __getitem__(self, prop):
        if prop in self._pipeml_properties:
            return self._pipeml_properties[prop]
        else:
            raise AttributeError(f"'{self._name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")

    def __contains__(self, prop):
        return prop in self._pipeml_properties
    
    def __len__(self):
        return len(self._pipeml_properties)

    def __iter__(self):
        for prop in self._pipeml_properties.keys():
            yield prop

    def __str__(self):
        raise NotImplementedError()
    
    def __repr__(self) -> str:
        return f"Config(len={len(self)})"

class IncludedConfig(Config):

    def __init__(self, name, config_dict):
        conf = config_dict.load()
        self._pipeml_path = config_dict.path
        super(IncludedConfig, self).__init__(name, conf)
    
    def __repr__(self) -> str:
        return f"IncludedConfig(len={len(self)}, path={self._pipeml_path})"

class Parameters(Config):
    """Create parameters of an object from a dict 'param_dict' of format 
    { 
    object_param_name: {class_name: obj_param_dict},
    variable_param_name: value,
    objects_list_param_name: [class_name: obj_param_dict, ...]
    }

    Args:
        param_dict (dict): Dictionary of the parameters
    """

    def __init__(self, class_name, param_dict):
        super(Parameters, self).__init__(class_name, param_dict)
        
    def _pipeml_construct(self, class_name, params_dict):
        super(Parameters, self)._pipeml_construct(class_name, params_dict)

    def _pipeml_check_valid(self, class_name, param_dict):
        return True

    def __repr__(self) -> str:
        return f"Parameters({len(self)})"

    def unwarp(self):
        return {param_name: (param_value() if not isinstance(param_value, Config) else param_value) for param_name, param_value in self._pipeml_properties.items()}

class IncludedParameters(Parameters):

    def __init__(self, class_name, param_dict):
        super().__init__(class_name, param_dict)

    def _pipeml_construct(self, class_name, params_dict):
        conf = params_dict.load()
        self._pipeml_path = params_dict.path
        return super()._pipeml_construct(class_name, conf)

class SingleObject(Node):
    """Allow the instantiation of an object defined in a yaml configuration file.

    Args:
        name (str): Name of the object
        config_dict (dict): A dictionary defining the object (class name and parameters).
    """

    def __init__(self, name, config_dict):
        super(SingleObject, self).__init__(name, config_dict)

    def _pipeml_check_valid(self, name, config_dict):
        return True

    def _pipeml_construct(self, name, config_dict):
        self._name = name
        object, self._params = list(config_dict.items())[0]
        self._class_name = object.class_name
        split_index = len(self._class_name) - self._class_name[::-1].index(".") # Get index of the last point
        self._module, self._class_name = self._class_name[:split_index-1], self._class_name[split_index:]
        if not isinstance(self._params, variables.Include):
            self._params = Parameters(self._class_name, self._params)
        else:
            self._params = IncludedParameters(self._class_name, self._params)

    def _pipeml_to_yaml(self, n_indents=0):
        r = f"{variables.SingleObjectTag.yaml_tag} {self._module}.{self._class_name}:\n"
        r += self._params._pipeml_to_yaml(n_indents=n_indents + 1)
        return r

    def _pipeml_to_dict(self):
        return {
            f"obj:{self._module}.{self._class_name}": self._params._pipeml_to_dict()
        }
        
    def __call__(self, **args):
        module = importlib.import_module(self._module)
        class_object = getattr(module, self._class_name)
        params = self._params.unwarp()
        return class_object(**params, **args)

    def __repr__(self) -> str:
        return f"SingleObject(name={self._class_name})"

class ObjectsList(Node):
    """Create a list of SingleObject from a yaml configuration file.

    Args:
        name (str): Name of the list of objects
        config_dict (list<dict>): A list of dictionaries which defines the objects list.
    """
    
    def __init__(self, name, config_dict):
        super(ObjectsList, self).__init__(name, config_dict)

    def _pipeml_check_valid(self, name, config_dict): 
        return True

    def _pipeml_construct(self, name, config_dict):
        self._name = name
        self._objects = [SingleObject(name, obj_dict) for obj_dict in config_dict]
        
    def _pipeml_to_yaml(self, n_indents=0):
        r = []
        for object in self._objects:
            el = "  " * (n_indents + 1)
            el += f"- {object._pipeml_to_yaml(n_indents=n_indents + 1)}"
            r += [el]
        return "\n".join(r)
    
    def _pipeml_to_dict(self):
        return [ obj._pipeml_to_dict() for obj in self._objects ]

    def __getitem__(self, i):
        return self._objects[i]

    def __call__(self, **args):
        return [obj(**args) for obj in self._objects]


def get_node_type(conf):
    """Detect the object that can build the tree

    Args:
        conf (dict): The configuration dictionary

    Returns:
        Node | Variable: The object type
    """
    if isinstance(conf, variables.Variable):
        # Return the builder class defined by the variable or None if none is needed
        return getattr(conf.__class__, "builder_class", None)

    builder_checkers = [
        (SingleObject, is_object),
        (ObjectsList, is_objects_list),
        (variables.Variable, is_var), 
        (Config, is_config)
    ]
    for node_type, can_build in builder_checkers:
        if can_build(conf):
            return node_type
    raise Exception(f"Configuration cannot be parsed: {conf}")

def construct(name, config_dict):
    """Build a tree from a dictionary

    Args:
        name (str): Name of the node
        config_dict (dict): The dictionary

    Returns:
        Node | Variable: The build tree element
    """
    NodeType = get_node_type(config_dict)

    if NodeType is not None: 
        node = NodeType(name, config_dict)
    else: 
        # Node is already built by a yaml tag
        node = config_dict
        node.set_name(name)
    return node