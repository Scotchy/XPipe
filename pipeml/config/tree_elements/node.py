
class Node():
    
    def __init__(self, name, config_dict):
        self._name = name 
        self._properties = {}
        self._config_dict = config_dict
        self._check_valid(name, config_dict)
        self._construct(name, config_dict)

    def _construct(self, name, config_dict):
        raise NotImplementedError("This function has to be implemented")

    def _check_valid(self, name, config_dict):
        raise NotImplementedError("This function has to be implemented")
    
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