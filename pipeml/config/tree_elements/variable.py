from .node import Node
import os
import string
from .tags import Tags
import yaml

__all__ = ["Variable"]

class Variable(Node):

    def __init__(self, name, value):
        super(Variable, self).__init__(name, value)

    def _construct(self, name, value):
        self.name = name
        self.value = value
    
    def _check_valid(self, name, value):
        return True

    def set_name(self, name):
        self.name = name

    def __call__(self):
        return self.value

@Tags.register
class EnvVariable(Variable): 
    yaml_tag = u"!env"
    """This class defines a yaml tag.
    It will load an environment variable.
    """

    def __init__(self, value):
        self.var_name = value
        if value in os.environ:
            value = os.environ[value]
        else:
            raise EnvironmentError(f"Environment variable '{value}' is not defined.")
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
            raise EnvironmentError(f"Environment variable '{str(e)}' is not defined in variable '{self.name}'.")
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
class Include(Variable):
    yaml_tag = u"!include"
    """
    This class defines a yaml tag.
    It will include another yaml into the current configuration.
    """

    def __init__(self, path):
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