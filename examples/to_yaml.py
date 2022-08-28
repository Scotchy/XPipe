import xpipe
from xpipe.config import load_config, to_yaml

file = load_config("./tests/resources/template.yaml")
print(to_yaml(file))