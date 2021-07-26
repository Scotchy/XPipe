from os import path
from pipeml import config
from .node import Node
import importlib
from .utils import is_object, is_objects_list, is_var
from .variable import Include, Variable
from collections.abc import Mapping

__all__ = ["Config", "SingleObject", "ObjectsList", "Parameters"]

class Config(Node, Mapping):

    def __init__(self, name, config_dict):
        self._config_dict = config_dict
        self._properties = {}
        Node.__init__(self, name, config_dict)

    def _check_valid(self, name, config_dict):
        return True

    def _construct(self, name, sub_config):
        for name, sub_config in sub_config.items():
            self.set_node(name, sub_config)

    def set_node(self, name, sub_config):
        if is_var(sub_config):
            var = Variable(name, sub_config)
            self._properties[name] = var

        elif is_object(sub_config):
            obj = SingleObject(name, sub_config)
            self._properties[name] = obj

        elif is_objects_list(sub_config):
            obj_list = ObjectsList(name, sub_config)
            self._properties[name] = obj_list
            
        elif isinstance(sub_config, dict):
            conf = Config(name, sub_config)
            self._properties[name] = conf

        elif isinstance(sub_config, Include):
            conf = sub_config.load()
            conf = IncludedConfig(conf, name, path=path)
            self._properties[name] = conf
            # Note that if some conf keys are present in an included file and in the current file
            # They will overwrite each other (depending their order in the configuration file)

        elif isinstance(sub_config, Variable):
            sub_config.set_name(name) # Set variable name
            self._properties[name] = sub_config

        else: 
            raise ValueError(f"Yaml file format not supported ({name} : {type(sub_config)})")

    def __getattribute__(self, prop: str):
        properties = super(Node, self).__getattribute__("_properties")
        if prop in properties:
            return properties[prop]
        else:
            try: 
                return super(Node, self).__getattribute__(prop)
            except:
                raise AttributeError(f"'{self._name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")

    def __getitem__(self, prop):
        if prop in self._properties:
            return self._properties[prop]
        else:
            raise AttributeError(f"'{self._name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")

    def __contains__(self, prop):
        return prop in self._properties
    
    def __len__(self):
        return len(self._properties)

    def __iter__(self):
        for prop in self._properties.keys():
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
        
    def _construct(self, class_name, params_dict):
        self._class_name = class_name
        for k, param_dict in params_dict.items():
            if is_var(param_dict):
                var = Variable(k, param_dict)
                self._properties[k] = var
            elif is_object(param_dict):
                so = SingleObject(k, param_dict)
                self._properties[k] = so
            elif is_objects_list(param_dict):
                ol = ObjectsList(class_name, param_dict)
                self._properties[k] = ol
            elif isinstance(param_dict, Include):
                included_properties = param_dict.load()
                self._construct(class_name, included_properties) # Add loaded parameters
                # Note that if some conf keys are present in an included file and in the current file
                # They will overwrite each other (depending their order in the configuration file)
            else:
                # Parameter is a dictionary
                conf = Config(class_name, param_dict)
                self._properties[k] = conf

    def _check_valid(self, class_name, param_dict):
        return True

    def __repr__(self) -> str:
        return f"Parameters({len(self)})"

    def unwarp(self):
        return {param_name: (param_value() if not isinstance(param_value, Config) else param_value) for param_name, param_value in self._properties.items()}

class SingleObject(Node):
    """Allow the instantiation of an object defined in a yaml configuration file.

        Args:
            name (str): Name of the object
            config_dict (dict): A dictionary defining the object (class name and parameters). Its format is
            {
                'obj:module.class_name': {'param1': value, ...},
            }
    """

    def __init__(self, name, config_dict):
        super(SingleObject, self).__init__(name, config_dict)

    def _check_valid(self, name, config_dict):
        return True

    def _construct(self, name, config_dict):
        self._name = name
        self._class_name, self._params = list(config_dict.items())[0]
        self._class_name = self._class_name.replace("obj:", "")
        split_index = len(self._class_name) - self._class_name[::-1].index(".") # Get index of the last point
        self._module, self._class_name = self._class_name[:split_index-1], self._class_name[split_index:]
        self._params = Parameters(self._class_name, self._params)

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
            config_dict (dict): A list of dictionaries which defines the list. Its format is 
            [
                {'obj:class_name': {'param1': value, ...}}
                ...
            ]
    """
    
    def __init__(self, name, config_dict):
        super(ObjectsList, self).__init__(name, config_dict)

    def _check_valid(self, name, config_dict): 
        return True

    def _construct(self, name, config_dict):
        self._name = name
        self._objects = [SingleObject(name, obj_dict) for obj_dict in config_dict]
        
    def __getitem__(self, i):
        return self._objects[i]

    def __call__(self, **args):
        return [obj(**args) for obj in self._objects]