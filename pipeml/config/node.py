from . import utils as utils

class Node():
    
    def __init__(self, name, config_dict):
        self._pipeml_name = name 
        self._pipeml_config_dict = config_dict
        self._pipeml_check_valid(name, config_dict)
        self._pipeml_construct(name, config_dict)

    def _pipeml_construct(self, name, config_dict):
        raise NotImplementedError("This function has to be implemented")

    def _pipeml_check_valid(self, name, config_dict):
        utils.valid_var_name(name)
        return True
    
    def __str__(self) -> str:
        return self.__repr__()