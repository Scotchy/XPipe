
class Node():
    
    def __init__(self, name, config_dict):
        self.__pipeml_name = name
        self.__pipeml_config_dict = config_dict
        self.__pipeml_builder = None
