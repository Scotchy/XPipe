from os import path
from pipeml import config
from .node import Node
import importlib
from .utils import is_object, is_objects_list, is_var, is_list
from .variable import Include, ListVariable, SingleObjectTag, Variable
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
            self.set_node(name, sub_config)

    def set_node(self, name, sub_config):
        if is_list(sub_config): 
            var = ListVariable(name, sub_config)
            self._pipeml_properties[name] = var
            
        elif is_var(sub_config):
            var = Variable(name, sub_config)
            self._pipeml_properties[name] = var

        elif is_object(sub_config):
            obj = SingleObject(name, sub_config)
            self._pipeml_properties[name] = obj

        elif is_objects_list(sub_config):
            obj_list = ObjectsList(name, sub_config)
            self._pipeml_properties[name] = obj_list
            
        elif isinstance(sub_config, dict):
            conf = Config(name, sub_config)
            self._pipeml_properties[name] = conf

        elif isinstance(sub_config, Include):
            conf = sub_config.load()
            conf = IncludedConfig(conf, name, path=sub_config.path)
            self._pipeml_properties[name] = conf
            # Note that if some conf keys are present in an included file and in the current file
            # They will overwrite each other (depending their order in the configuration file)
        
        elif isinstance(sub_config, Variable):
            sub_config.set_name(name) # Set variable name
            self._pipeml_properties[name] = sub_config

        else: 
            raise ValueError(f"Yaml file format not supported ({name} : {type(sub_config)})")

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
                raise AttributeError(f"'{self._name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")

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

    def __init__(self, config_dict, name, path=None):
        self._path = path
        super(IncludedConfig, self).__init__(name, config_dict)
    
    def __repr__(self) -> str:
        return f"IncludedConfig(len={len(self)}, path={self._path})"

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
        self._class_name = class_name
        for k, param_dict in params_dict.items():
            if is_var(param_dict):
                var = Variable(k, param_dict)
                self._pipeml_properties[k] = var
            elif is_object(param_dict):
                so = SingleObject(k, param_dict)
                self._pipeml_properties[k] = so
            elif is_objects_list(param_dict):
                ol = ObjectsList(class_name, param_dict)
                self._pipeml_properties[k] = ol
            elif isinstance(param_dict, Include):
                included_pipeml_properties = param_dict.load()
                self._pipeml_construct(class_name, included_pipeml_properties) # Add loaded parameters
                # Note that if some conf keys are present in an included file and in the current file
                # They will overwrite each other (depending their order in the configuration file)
            else:
                # Parameter is a dictionary
                conf = Config(class_name, param_dict)
                self._pipeml_properties[k] = conf

    def _pipeml_check_valid(self, class_name, param_dict):
        return True

    def __repr__(self) -> str:
        return f"Parameters({len(self)})"

    def unwarp(self):
        return {param_name: (param_value() if not isinstance(param_value, Config) else param_value) for param_name, param_value in self._pipeml_properties.items()}

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
        self._params = Parameters(self._class_name, self._params)

    def _pipeml_to_yaml(self, n_indents=0):
        r = f"{SingleObjectTag.yaml_tag} {self._module}.{self._class_name}:\n"
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