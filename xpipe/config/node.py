from . import utils as utils
import copy


class Node(object):
    
    
    def __init__(self):
        """
        Initializes a Node object. Every object of a configuration is a Node.
        """
        object.__setattr__(self, "_xpipe_name", None) # The name of the node
        object.__setattr__(self, "_xpipe_config_dict", None) # The configuration of the node
        object.__setattr__(self, "_xpipe_parent", None) # The parent node


    def _xpipe_construct(self, name, config_dict):
        """This function constructs the node. 
        It is called by the constructor.
        It must be overridden by the child class.

        Args:
            name (str): The name of the node
            config_dict (_type_): The configuration of the node

        Raises:
            NotImplementedError: If the function is not overridden by the child class.
        """
        raise NotImplementedError("This function has to be implemented")


    def _xpipe_check_valid(self, name, config_dict):
        """This function checks if the configuration is valid.

        Args:
            name (str): The name of the node
            config_dict (dict): The configuration of the node

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        if isinstance(name, str):
            utils.valid_var_name(name)
        return True
    

    @classmethod
    def _xpipe_instantiate(cls, arg):
        """Function that returns an instance of the current object with minimal configuration. 
        It is called when the object is loaded from a yaml tag to instantiate an 'empty shell' of the object before it is fully loaded thanks to _xpipe_construct.

        Args:
            arg (Any): Argument coming from yaml (example: !tag arg)

        Raises:
            NotImplementedError: This function must be implemented by the child class

        Returns:
            Node: Instance of the current object
        """
        raise NotImplementedError("This function has to be implemented. It must return an instance of the node with proper configuration.")


    @classmethod
    def from_yaml(cls, loader, node):
        return cls._xpipe_instantiate(node.value)


    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)


    def __str__(self) -> str:
        return self.__repr__()