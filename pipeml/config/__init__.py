"""
:mod:`pipeml.config` is a package implementing main classes needed to load the yaml tree file and load objects from it.
"""

from .tree_elements import load_config

del tree_elements # pylint: disable=undefined-variable