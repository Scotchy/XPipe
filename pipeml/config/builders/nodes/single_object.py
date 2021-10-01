from .node import Node
import importlib

class SingleObject(Node):
    """Allow the instantiation of an object defined in a yaml configuration file.

    Args:
        name (str): Name of the object
        config_dict (dict): A dictionary defining the object (class name and parameters).
    """

    def __init__(self, name, config_dict):
        super(SingleObject, self).__init__(name, config_dict)
        
    def __call__(self, **args):
        module = importlib.import_module(self._module)
        class_object = getattr(module, self._class_name)
        params = self._params.unwarp()
        return class_object(**params, **args)

    def __repr__(self) -> str:
        return f"SingleObject(name={self._class_name})"
