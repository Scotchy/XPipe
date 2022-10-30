from .node import Node
from . import tag
from . import config

import os
import string
import yaml
from .loader import load_class

__all__ = [
    "Variable", 
    "SimpleVariable",
    "EnvVariable", 
    "ReferenceVariable", 
    "FormatStrVariable",
    "ClassTag"
]


class Variable(Node):

    def __init__(self, value):
        """Initializes a Variable object.

        Args:
            value (str | int | float): The value of the variable
        """
        object.__setattr__(self, "_xpipe_value", value)
        super(Variable, self).__init__()


    @classmethod
    def _xpipe_instantiate(cls, args):
        return cls(args)


    def _xpipe_construct(self, name, config_dict):
        pass


    @property
    def value(self):
        return object.__getattribute__(self, "_xpipe_value")
    

    @property
    def name(self):
        return object.__getattribute__(self, "_xpipe_name")


    def _xpipe_construct(self, name, value):
        return


    def __call__(self):
        return self.value


    def _xpipe_to_yaml(self, n_indents=0):
        return self.value
    

    def _xpipe_to_dict(self):
        return str(self())


    def __eq__(self, o) -> bool:
        if not isinstance(o, Variable): 
            raise Exception(f"Cannot compare {self} and {o}")
        return self.value == o.value
    

    def __str__(self) -> str:
        return self.__repr__()
        

    def __repr__(self) -> str:
        return f"Variable(name='{self.name}', value={self.value})"
    

    def __hash__(self) -> int:
        return hash(id(self))


class SimpleVariable(Variable):
    """
    A basic variable with no additional functionality.
    """

    def __init__(self):
        super().__init__(None)


    def _xpipe_check_valid(self, name, config_dict):
        return super()._xpipe_check_valid(name, config_dict)


    def _xpipe_construct(self, name, config_dict):
        object.__setattr__(self, "_xpipe_value", config_dict)


@tag.register("!env")
class EnvVariable(Variable): 
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
        super(EnvVariable, self).__init__(value=value)
    

    @classmethod
    def from_yaml(cls, loader, node):
        return EnvVariable(node.value)


    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)


    def __repr__(self) -> str:
        return f"EnvVariable(var={self.var_name}, value={self.value})"
    

@tag.register("!ref")
class ReferenceVariable(Variable):
    """This class defines a yaml tag.
    It is a reference to another node.
    """

    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Reference variable name must be a string.")
        self.var_path = value
        super(ReferenceVariable, self).__init__(value=value)

    @property
    def value(self):
        from .config import get_base, get_node
        if self.var_path.startswith("/"):
            # Absolute path
            base_node = get_base(self)
            path = self.var_path[1:]
        else:
            # Relative path
            base_node = self._xpipe_parent
            path = self.var_path

        node = get_node(base_node, path)
        if isinstance(node, Variable):
            return node()
        return node


    @classmethod
    def from_yaml(cls, loader, node):
        return ReferenceVariable(node.value)


    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)


    def __repr__(self) -> str:
        return f"ReferenceVariable(var={self.var_path}, value={self.value})"
        

@tag.register("!f")
class FormatStrVariable(Variable):
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
        super(FormatStrVariable, self).__init__(value=value)
    
    
    @classmethod
    def from_yaml(cls, loader, node):
        return FormatStrVariable(node.value)


    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)


    def __eq__(self, o) -> bool:
        if not isinstance(o, FormatStrVariable): 
            raise Exception(f"Cannot compare {self} and {o}")
        return self.original_str == o.original_str


    def __repr__(self) -> str:
        return f"FormatStrVariable(original={self.original_str}, output={self.value})"


@tag.register("!class")
class ClassTag(Variable):
    """This class defines a yaml tag
    It store a class (not an instance)"""

    def __init__(self, class_path):
        self.class_path = class_path
        value = load_class(class_path)
        super(ClassTag, self).__init__(value=value)
    

    @classmethod
    def from_yaml(cls, loader, node):
        return ClassTag(node.value)


    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)


    def _xpipe_to_yaml(self, n_indents=0):
        return f"{self.yaml_tag} {self.class_path}"


    def _xpipe_to_dict(self):
        return f"{self.yaml_tag} {self.class_path}"


    def __eq__(self, o) -> bool:
        if not isinstance(o, ClassTag): 
            raise Exception(f"Cannot compare {self} and {o}")
        return self.class_path == o.class_path


    def __repr__(self) -> str:
        return f"ClassTag(class_name={self.class_path})"