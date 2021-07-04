
import yaml
from .node import Node
import importlib
from .utils import get_statement, is_include, is_object, is_objects_list, is_var
from .variable import Variable

__all__ = ["SingleObject", "ObjectsList", "Parameters"]

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
                self._params[k] = param_dict
                self.__dict__[k] = param_dict

    def _check_valid(self, class_name, param_dict):
        for k, v in param_dict.items():
            if not is_var(v) and not is_object(v) and not is_objects_list(v) and not is_include(v):
                raise ValueError(f"Found bad format for parameter '{k}'' of object '{class_name}' {param_dict}.")
        return True

    def unwarp(self):
        return {param_name: param_value() for param_name, param_value in self._params.items()}

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

