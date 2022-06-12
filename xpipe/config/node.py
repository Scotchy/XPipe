from . import utils as utils
import copy


class Node(object):
    
    
    def __init__(self, name, config_dict, parent=None):
        """Initializes a Node object. Every object of a configuration is a Node.

        Args:
            name (str): The name of the node
            config_dict (dict): The configuration of the node
            parent (Node, optional): The parent node. Defaults to None.
        """
        object.__setattr__(self, "_xpipe_name", name)
        object.__setattr__(self, "_xpipe_config_dict", config_dict)
        object.__setattr__(self, "_xpipe_parent", parent)
        self._xpipe_construct(name, config_dict)


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
    

    def __str__(self) -> str:
        return self.__repr__()