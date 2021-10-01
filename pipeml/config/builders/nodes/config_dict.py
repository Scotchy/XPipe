from typing import Mapping
from .node import Node


class ConfigDict(Node, Mapping):

    def __init__(self, name, config_dict):
        self._config_dict = config_dict
        self._properties = {}
        Node.__init__(self, name, config_dict)
    
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
        return f"ConfigDict(len={len(self)})"
