
import yaml
from .node import Node
import importlib
from .utils import get_statement, is_include, is_object, is_objects_list, is_var
from .variable import Variable
from collections.abc import Mapping

__all__ = ["Config", "SingleObject", "ObjectsList", "Parameters"]

class Config(Node, Mapping):

    def __init__(self, config_dict, name=None):
        if name == "root":
            raise ValueError("Forbidden name 'root' in yaml file.")
        if name is None:
            name = "root"
        self.config_dict = config_dict
        self._properties = {}
        super(Config, self).__init__(name, config_dict)

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
            var = Variable(name, sub_config)
            self._properties[name] = var
            setattr(self, name, var)

        elif is_object(sub_config):
            obj = SingleObject(name, sub_config)
            self._properties[name] = obj
            setattr(self, name, obj)

        elif is_objects_list(sub_config):
            obj_list = ObjectsList(name, sub_config)
            self._properties[name] = obj_list
            setattr(self, name, obj_list)

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
            conf = Config(sub_config, name)
            self._properties[name] = conf
            setattr(self, name, conf) # Create an attribute containing the config stored in 'key'
        else: 

            raise ValueError(f"Yaml file format not supported ({name} : {type(sub_config)})")

    def __len__(self):
        return len(self._properties)

    def __iter__(self):
        for prop in self._properties.keys():
            yield prop

    def __getitem__(self, property):
        return self._properties[property]
    
    def __contains__(self, property):
        return property in self._properties

    def __str__(self):
        raise NotImplementedError()

class Parameters(Node):
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
        self.class_name = class_name
        self._params = {}
        for k, param_dict in params_dict.items():
            if is_var(param_dict):
                var = Variable(k, param_dict)
                self._params[k] = var
                self.__dict__[k] = var
            elif is_object(param_dict):
                so = SingleObject(k, param_dict)
                self._params[k] = so
                self.__dict__[k] = so
            elif is_objects_list(param_dict):
                ol = ObjectsList(class_name, param_dict)
                self._params[k] = ol
                self.__dict__[k] = ol
            elif is_include(param_dict):
                # Parameters are stored in another file
                path = get_statement(param_dict)["argument"]
                with open(path, "r") as f:
                    included_params = yaml.load(f, Loader=yaml.Loader)
                self._construct(class_name, included_params) # Add loaded parameters
                # Note that if some parameters are present in an included file and in the current file
                # They will overwrite each other (depending their order in the configuration file)
            else:
                # Parameter is a dictionary
                conf = Config(param_dict)
                self._params[k] = conf
                self.__dict__[k] = conf

    def _check_valid(self, class_name, param_dict):
        return True

    def __getitem__(self, param):
        return self._params[property]
    
    def __contains__(self, param):
        return param in self._params

    def unwarp(self):
        return {param_name: (param_value() if not isinstance(param_value, Config) else param_value) for param_name, param_value in self._params.items()}

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
        self.name = name
        self.class_name, self.params = list(config_dict.items())[0]
        self.class_name = self.class_name.replace("obj:", "")
        split_index = len(self.class_name) - self.class_name[::-1].index(".") # Get index of the last point
        self.module, self.class_name = self.class_name[:split_index-1], self.class_name[split_index:]
        self.params = Parameters(self.class_name, self.params)

    def __call__(self, **args):
        module = importlib.import_module(self.module)
        class_object = getattr(module, self.class_name)
        params = self.params.unwarp()
        return class_object(**params, **args)

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
        self.name = name
        self.objects = [SingleObject(name, obj_dict) for obj_dict in config_dict]
        
    def __getitem__(self, i):
        return self.objects[i]

    def __call__(self, **args):
        return [obj(**args) for obj in self.objects]

class Include(Node):
    
    def __init__(self, name, config_dict):
        super().__init__(name, config_dict)

    def _check_valid(self, name, config_dict):
        return True
    
    def _construct(self, name, config_dict):
        self.name = name
        include_path = get_statement(config_dict)["argument"]

