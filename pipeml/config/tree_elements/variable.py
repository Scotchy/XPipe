from .node import Node
import os
import string
from .tags import Tags
import yaml

__all__ = ["Variable", "EnvVariable", "Include", "FormatStrVariable", "SingleObjectTag"]

class Variable(Node):

    def __init__(self, name, value):
        super(Variable, self).__init__(name, value)

    def _construct(self, name, value):
        self.name = name
        self.value = value
    
    def _to_yaml(self, n_indents=0):
        return self.value
    
    def _to_dict(self):
        return self.value

    def _check_valid(self, name, value):
        valid_var_name(name)
        return True

    def set_name(self, name):
        self.name = name

    def __call__(self):
        return self.value

    def __repr__(self) -> str:
        return f"{self.name} = {self.value}"

class ListVariable(Variable):

    def __init__(self, name, value):
        super().__init__(name, value)
    
    def __getitem__(self, index):
        value = self.value[index]
        if isinstance(value, Include): 
            return value.load()
        elif isinstance(value, Node):
            return value()
        else: 
            return value
    
    def __len__(self):
        return len(self.value)

    def __call__(self):
        return [el for el in self]

    def __repr__(self) -> str:
        return f"{self.name} = List(len={len(self)})"
        
@Tags.register
class EnvVariable(Variable): 
    yaml_tag = u"!env"
    """This class defines a yaml tag.
    It will load an environment variable.
    """

    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Environment variable name must be a string.")
        if value[0] == "$":
            value = value[1:]
        self.var_name = value
        if value in os.environ:
            value = os.environ[value]
        else:
            raise EnvironmentError(f"Environment variable '{value}' is not defined.")
        self.value = value
        super().__init__("", value)
    
    @classmethod
    def from_yaml(cls, loader, node):
        return EnvVariable(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __repr__(self) -> str:
        return f"EnvVariable(var={self.var_name}, value={self.value})"
    
@Tags.register
class Include(Variable):
    yaml_tag = u"!include"
    """
    This class defines a yaml tag.
    It will include another yaml into the current configuration.
    """
    
    def __init__(self, path):
        self.original_path = path
        try:
            path = string.Template(path).substitute(os.environ)
        except KeyError as e:
            raise EnvironmentError(f"Environment variable '{str(e)}' is not defined in include statement.")
        self.path = path
    
    def load(self):
        with open(self.path, "r") as f:
            return yaml.safe_load(f)
    
    @classmethod
    def from_yaml(cls, loader, node):
        return Include(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)
        
    def __repr__(self) -> str:
        return f"Include(path={self.path})"

@Tags.register
class FormatStrVariable(Variable):
    yaml_tag = u"!f"
    """This class defines a yaml tag. 
    The class will automatically replace substrings $ENV_VAR or ${ENV_VAR} with the corresponding environment variables.
    """

    def __init__(self, value):
        self.original_str = value
        try:
            value = string.Template(value).substitute(os.environ)
        except KeyError as e:
            raise EnvironmentError(f"Environment variable '{str(e)}' is not defined in formatted string.")
        self.str = value
        super().__init__("", value)
    
    @classmethod
    def from_yaml(cls, loader, node):
        return FormatStrVariable(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __repr__(self) -> str:
        return f"FormatStrVariable(original={self.original_str}, output={self.value})"
    
@Tags.register
class SingleObjectTag(Variable):
    yaml_tag = u"!obj"
    """
    This class defines a yaml tag.
    It will include another yaml into the current configuration.
    """
    
    def __init__(self, class_name):
        self.class_name = class_name
    
    def load(self):
        with open(self.path, "r") as f:
            return yaml.safe_load(f)
    
    @classmethod
    def from_yaml(cls, loader, node):
        return SingleObjectTag(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __repr__(self) -> str:
        return f"SingleObjectTag(class_name={self.class_name})"

def valid_var_name(name : str):
    """Raise an error if 'name' is not a valid Variable name.

    Args:
        name (str): Name of the variable

    Raises:
        ValueError: If name contains caracters that are not alphabetical or numerical
        ValueError: If name begin with a number
    """
    if name == "":
        return 
    stripped_name = name.replace("_", "")
    if stripped_name == "":
        raise ValueError(f"Variable '{name}' cannot contain only underscores.")
    if not stripped_name.isalnum():
        raise ValueError(f"Variable '{name}' must contain alphabetical or numerical caracters or underscores.")
    if not name[0].isalpha() or name[0] == "_":
        raise ValueError(f"Variable '{name}' must begin with an alphabetical caracter or an underscore.")