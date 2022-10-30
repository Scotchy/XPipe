from .node import Node
from .utils import is_objects_list, is_list, is_config, is_var
from . import config as config
from . import variables as variables
from . import tag

import importlib
import yaml
import string
import copy
import os


__all__ = ["Config", "FromIncludes", "List", "SingleObject", "ObjectsList", "construct"]


class Config(Node, dict):
    """
    A configuration is like a dictionary containing elements like SingleObject, Config and so on.
    """

    def _xpipe_check_valid(self, name, config_dict):
        if not isinstance(name, str) or name != "__root__":
            super(Config, self)._xpipe_check_valid(name, config_dict)
        return True


    def _xpipe_construct(self, name, sub_config, path=None):
        object.__setattr__(self, "_xpipe_path", path)

        from_node = None
    
        for name, sub_config in sub_config.items():
            node = construct(name, sub_config, parent=self)
            
            if isinstance(node, FromIncludes):
                if from_node is not None:
                    raise Exception("Only one !from per node is allowed")
                from_node = node
            else:
                dict.__setitem__(self, name, node)
        
        if from_node is not None:
            r = config.merge(from_node.includes, self)
            dict.clear(self)
            dict.update(self, r)


    def _xpipe_to_yaml(self, n_indents=0):
        r = []
        for key, value in self.items():
            el = "  " * n_indents
            el += f"{key}: "
            if not isinstance(value, variables.Variable):
                el += "\n"
            el += f"{value._xpipe_to_yaml(n_indents=n_indents + 1)}"
            r += [el]
        joiner = "\n\n" if self._xpipe_name == "__root__" else "\n"
        return joiner.join(r)


    def _xpipe_to_dict(self):
        return { k: v._xpipe_to_dict() for k, v in self.items() }
    

    def __getattribute__(self, prop: str):
        try:
            return dict.__getitem__(self, prop)
        except KeyError:
            pass

        try: 
            return object.__getattribute__(self, prop)
        except:
            raise AttributeError(f"'{self._xpipe_name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")


    def __setattr__(self, key, value):
        dict.__setitem__(self, key, value)


    def __getitem__(self, prop):
        if dict.__contains__(self, prop):
            return dict.__getitem__(self, prop)
        else:
            raise AttributeError(f"'{self._xpipe_name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")
    

    def __repr__(self) -> str:
        return f"Config(len={len(self)})"
    

    def __deepcopy__(self, memo):
        cls = self.__class__
        copy_instance = cls.__new__(cls)
        memo[id(self)] = copy_instance # Add the object to memo to avoid infinite recursion (the object is referenced by its children)

        dict_values = set(self.keys()) 
        attributes_name = set(self.__dict__.keys()) - dict_values

        # copy attributes
        for name in attributes_name:
            attr_value = object.__getattribute__(self, name)
            attr_value_id = id(attr_value)
            copied_attr_value = memo.get(attr_value_id, None) or copy.deepcopy(attr_value, memo)
            object.__setattr__(copy_instance, name, copied_attr_value)

        # copy dict
        for name in dict_values:
            dict_value = dict.__getitem__(self, name)
            dict_value_id = id(dict_value)
            copied_dict_value = memo.get(dict_value_id, None) or copy.deepcopy(dict_value, memo)
            dict.__setitem__(copy_instance, name, copied_dict_value)

        return copy_instance


    def __hash__(self) -> int:
        return hash(id(self))


@tag.register("!include")
class IncludedConfig(Config):
    
    @classmethod
    def _xpipe_instantiate(cls, path):
        included_config = IncludedConfig()
        object.__setattr__(included_config, "_xpipe_path", path)
        return included_config


    def _xpipe_construct(self, name, sub_config):
        
        path = object.__getattribute__(self, "_xpipe_path")
        path = self.__compute_full_path(path)
        conf = self.__load(path)
        object.__setattr__(self, "_xpipe_path", path)
        super(IncludedConfig, self)._xpipe_construct(name, conf, path=path)


    def __compute_full_path(self, path):
        try:
            path = string.Template(path).substitute(os.environ)
        except KeyError as e:
            raise EnvironmentError(f"Environment variable '{str(e)}' is not defined in include statement.")

        parent = object.__getattribute__(self, "_xpipe_parent")
        base_path = config.get_base(parent)._xpipe_path or "" if parent is not None else ""

        base_path = os.path.dirname(base_path)

        path = os.path.expanduser(path)
        base_path = os.path.expanduser(base_path)

        if not os.path.isabs(path):
            path = os.path.join(base_path, path)
        
        return path 


    def __load(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)


    def __eq__(self, o: object) -> bool:
        if not isinstance(o, IncludedConfig): 
            raise Exception(f"Cannot compare {self} and {o}")
        return self._xpipe_path == o._xpipe_path


    def __hash__(self) -> int:
        return hash(id(self))


    def __repr__(self) -> str:
        return f"IncludedConfig(len={len(self)}, path={self._xpipe_path})"


@tag.register("!from")
class FromIncludes(Node):
    
    @classmethod
    def _xpipe_instantiate(cls, arg):
        from_includes = FromIncludes()
        return from_includes


    def _xpipe_check_valid(self, name, config_dict):
        
        if not isinstance(config_dict, list):
            raise Exception(f"{name} must be a list")
        
        for include in config_dict:
            if not isinstance(include, variables.Include):
                raise Exception(f"{name} must be a list of includes")
        
        return True


    def _xpipe_construct(self, name, config_dict):
        self.includes = config.merge(*[construct("", sub_config_dict, parent=self) for sub_config_dict in config_dict], inplace=True)


class List(Node, list):
    
    def __init__(self):
        Node.__init__(self)
        list.__init__(self)


    def _xpipe_construct(self, name, config_dict):
        for i, element in enumerate(config_dict):
            var_name = f"{name}[{i}]"
            constructed_el = construct(var_name, element, parent=self)
            self.append(constructed_el)


    def _xpipe_check_valid(self, name, config_dict):
        return True


    def _xpipe_to_dict(self):
        return [el._xpipe_to_dict() if isinstance(el, Node) else el for el in self]


    def _xpipe_to_yaml(self, n_indents=0):
        r = ""
        
        for el in self:
            indents = "  " * (n_indents + 1)
            yaml_el = el._xpipe_to_yaml(n_indents = n_indents + 2) if isinstance(el, Node) else el
            if isinstance(el, Config) or isinstance(el, ObjectsList) or isinstance(el, List):
                yaml_el = f"\n{yaml_el}"
            if isinstance(el, SingleObject):
                yaml_el = yaml_el.lstrip()
            r += f"{indents}- {yaml_el}\n"
        return r


    def __getitem__(self, index):
        from .variables import Variable
        element = list.__getitem__(self, index)
        if isinstance(element, Variable):
            return element()
        else:
            return element


    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


    def __hash__(self) -> int:
        return hash(id(self))
        

    def __call__(self):
        return [el for el in self]


    def __repr__(self) -> str:
        return f"[{', '.join(map(lambda x: str(x), self))}]"
    

    def __deepcopy__(self, memo):
        cls = self.__class__
        copy_instance = cls.__new__(cls)
        memo[id(self)] = copy_instance # Add the object to memo to avoid infinite recursion (the object is referenced by its children)
        
        for i in range(len(self)):
            el = list.__getitem__(self, i)
            el_id = id(el)
            copied_el = copy.deepcopy(el, memo)
            copy_instance.append(copied_el)

        return copy_instance


@tag.register("!obj")
class SingleObject(Node):
    """
    Allow the instantiation of an object defined in a yaml configuration file.
    """

    @classmethod
    def _xpipe_instantiate(cls, class_path):
        single_object = SingleObject()
        single_object._class_path = class_path
        split_index = len(class_path) - class_path[::-1].index(".") # Get index of the last point
        single_object._module, single_object._class_name = class_path[:split_index-1], class_path[split_index:]
        return single_object


    def _xpipe_check_valid(self, name, config_dict):
        return True


    def _xpipe_construct(self, name, params_dict):
        
        self._params = construct(name, params_dict, parent=self)

        config.set_name(self._params, self._class_name)
        config.set_parent(self._params, self)
        self._params._xpipe_construct(self._class_name, params_dict)
        

    def _xpipe_to_yaml(self, n_indents=0):
        indents = "  " * (n_indents)
        r = f"{indents}{self.yaml_tag} {self._module}.{self._class_name}:\n"
        r += self._params._xpipe_to_yaml(n_indents=n_indents + 1)
        return r


    def _xpipe_to_dict(self):
        return {
            f"{self.yaml_tag} {self._module}.{self._class_name}": self._params._xpipe_to_dict()
        }
        

    def __call__(self, **args):
        module = importlib.import_module(self._module)
        class_object = getattr(module, self._class_name)
        return class_object(
            **config.to_dict(self._params), 
            **args
        )


    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SingleObject): 
            raise Exception(f"Cannot compare {self} and {o}")
        return self._class_name == o._class_name and self._params == o._params


    def __hash__(self) -> int:
        return hash(id(self))


    def __repr__(self) -> str:
        return f"SingleObject(name={self._class_name})"


class ObjectsList(List):
    """
    Create a list of SingleObject from a yaml configuration file.
    """


    def _xpipe_check_valid(self, name, config_dict): 
        super(ObjectsList, self)._xpipe_check_valid(name, config_dict)


    def __call__(self, **args):
        return [obj(**args) for obj in self]


def get_node_type(name, conf):
    """Detects the object that can build the tree

    Args:
        conf (dict): The configuration dictionary

    Returns:
        Node | Variable | None : The object type
    """

    builder_checkers = [
        (ObjectsList, is_objects_list),
        (List, is_list), 
        (Config, is_config),
        (variables.SimpleVariable, is_var)
    ]
    for node_type, can_build in builder_checkers:
        if can_build(name, conf):
            return node_type
        
    return None


def construct(name, config_dict, parent=None, **kwargs):
    """Build a tree from a dictionary

    Args:
        name (str): Name of the node
        config_dict (dict): The dictionary
        parent (Node): Parent node
        **kwargs: Complementary arguments to pass to _xpipe_construct method of the node being built.

    Returns:
        Node | Variable: The build tree element
    """
    if isinstance(config_dict, Node):
        # It's something already loaded which has no parameters (like IncludedConfig)
        node = config_dict
        config.set_name(node, name)
        config.set_parent(node, parent)
        config.set_config_dict(node, {})
        node._xpipe_construct(name, config_dict, **kwargs)
        return node 

    if isinstance(name, Node):
        # It's something already loaded (like a FromIncludes)
        node = name
        config.set_name(node, "")
        config.set_parent(node, parent)
        config.set_config_dict(node, config_dict)
        node._xpipe_construct(name, config_dict, **kwargs)
        return node 

    if not isinstance(config_dict, Node) and isinstance(config_dict, dict) and len(config_dict) == 1:
        # It's something already loaded which has parameters (like a SingleObject)
        node_dict, sub_config_dict = list(config_dict.items())[0]
        if isinstance(node_dict, Node):
            config.set_name(node_dict, name)
            config.set_parent(node_dict, parent)
            config.set_config_dict(node_dict, sub_config_dict)
            node_dict._xpipe_construct(name, sub_config_dict, **kwargs)
            return node_dict
    
    # It is something that has not been loaded by a yaml tag
    NodeType = get_node_type(name, config_dict)
    if NodeType is not None: 
        node = NodeType()
        config.set_name(node, name)
        config.set_parent(node, parent)
        config.set_config_dict(node, config_dict)
        node._xpipe_construct(name, config_dict, **kwargs)
        return node

    # No case works, node cannot be built
    raise Exception(f"Cannot build node {name}")
