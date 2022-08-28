import xpipe
from xpipe.config import load_config, to_dict
from xpipe.client import connect
import numpy as np
from tqdm import tqdm

conf = load_config("./tests/resources/template.yaml")
client = connect("http://localhost:5000")
exp = client.start_run("/test", "exp")

conf_dict = to_dict(conf)
r = exp.log_params(conf_dict)
print(r)

n = 10
losses = 10 * np.exp(-np.arange(n) / (n / 10)) + np.random.rand(n)
for loss in tqdm(losses):
    exp.log_metric("loss", loss)