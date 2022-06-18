from xpipe.config import load_config, to_dict
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

conf = load_config(os.path.join(base_dir, "conf.yaml"))

my_classes = conf.my_classes() # Instantiate all the objects of the list
my_class1 = conf.my_classes[0]() # Only instantiate the first object
parameters_class1 = conf.my_classes[0]._params # Get the parameters. It is a Parameters object

print(my_class1.__class__.__name__)

# parameters_class1.a is a Variable object. You access its name (parameters_class1.a.name) and value (parameters_class1.a())
print(f"Parameters : {to_dict(parameters_class1)} (One parameter '{parameters_class1.a.name}' with value {parameters_class1.a()})")
