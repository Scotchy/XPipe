import importlib 


def parse_path(class_path, aliases=None):
    """Get the path of a class from a given path using importlib library. If the path first part is an alias, the path is replaced with the real path.
    exemple:
        class_path = "my_alias.Class"
        aliases = {"my_alias": "package.module"}
        return "package.module.Class"

    Args:
        class_path (str): Class path (e.g. "package.module.Class")
        aliases (dict<str, str>, optional): A dictionary of aliases. The key is the alias and the value is the path. Defaults to None.

    Returns:
        _type_: _description_
    """    
    if aliases is not None:
        for alias, path in aliases.items():
            n = len(alias)
            if class_path[:n] == alias:
                class_path = path + class_path[n:]
    return class_path


def load_class(class_path, aliases=None):
    """Loads a class from a given path using importlib library.

    Args:
        class_path (str): Class path (e.g. "package.module.Class")
        aliases (dict<str, str>, optional): A dictionary of aliases. The key is the alias and the value is the path. Defaults to None.

    Raises:
        ImportError: If the module cannot be imported.
        AttributeError: If the module does not contain the class.

    Returns:
        Object: The class.
    """
    class_path = parse_path(class_path, aliases)
    module_path, class_name = class_path.rsplit('.', 1)
    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        raise ImportError('Could not import module %s: %s' % (module_path, e))
    try:
        return getattr(module, class_name)
    except AttributeError as e:
        raise AttributeError('Module "%s" does not have an element "%s"' % (module_path, class_name))
