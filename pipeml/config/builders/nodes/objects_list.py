from .node import Node

class ObjectsList(Node):
    """Create a list of SingleObject from a yaml configuration file.

    Args:
        name (str): Name of the list of objects
        config_dict (list<dict>): A list of dictionaries which defines the objects list.
    """

    def __init__(self, name, config_dict):
        super(ObjectsList, self).__init__(name, config_dict)

    def __getitem__(self, i):
        return self._objects[i]

    def __call__(self, **args):
        return [obj(**args) for obj in self._objects]