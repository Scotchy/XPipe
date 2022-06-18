from xpipe.config import load_config
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

conf = load_config(os.path.join(base_dir, "experiment.yaml"))
epochs = conf.training.epochs() # 18

# Instantiate your model defined in models/my_model.yaml
my_model = conf.model.definition()

# Directly instantiate your optimizer and scheduler from configuration
# Note that you can add argument that are not in the configuration file
optimizer = conf.training.optimizer(params=my_model.parameters())
scheduler = conf.training.scheduler(optimizer=optimizer)

print(f"Epochs: {epochs}")
print(f"Optimizer: {optimizer.__class__.__name__}")
print(f"Scheduler: {scheduler.__class__.__name__}")
print(f"Model: {my_model}")