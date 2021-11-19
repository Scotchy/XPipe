Welcome to XPipe's documentation !
##################################

.. image:: https://img.shields.io/badge/python-%3E%3D%203.5-blue
  
Introduction
************

XPipe is a library that I started developping in December 2020 for my personal use.
As it might be useful for other people, I decided to publish the code as an open source project.

XPipe focuses on two principal components to make Data Science easier:

- **Configuration files** are a big concern in data science field and there is no standard today. XPipe facilitates your work by automatically loading python objects from a yaml configuration. You can also easily include other yaml files into another.

- **Experiment tracking**: The web interface enables you to easily organize your experiments into folders, to filter them and to plot different kind of graphs. You will particularly appreciate the library if you deal with a lot of experiments.

The philosophy behind the project is to be simple and customizable.

As a team, you can run a single XPipe server for everyone. It will promote exchange as everyone can easily share their work with others.

Getting started
***************

.. code-block:: bash

  pip install xpipe


Documentation (work in progress): https://x-pipe.readthedocs.io/en/latest/#

Configuration files
*******************

Here is a simple example of how to use yaml configuration files to seamlessly load needed objects to run your experiments.
  
.. code-block:: yaml

  training:
    gpu: !env CUDA_VISIBLE_DEVICES # Get the value of env variable CUDA_VISIBLE_DEVICES
    epochs: 18
    batch_size: 100

    optimizer: !obj torch.optimSGD : {lr : 0.001}

    scheduler: !obj torch.optim.lr_scheduler.MultiStepLR : {milestones: [2, 6, 10, 14]}

    loss: !obj torch.nnBCELoss : {}

  model: !include "./models/my_model.yaml"

  transforms:
    !obj transforms.Normalize : {}
    !obj transforms.Noise : {}
    !obj transforms.RandomFlip : {probability: 0.5}


Then you can load the configuration file:

.. code-block:: yaml

  from xpipe.config import load_config

  conf = load_config("my_config.yaml")
  epochs = conf.training.epochs() # 18

  # Instantiate your model defined in models/my_model.yaml
  my_model = params.model()

  # Directly instantiate your optimizer and scheduler from configuration
  # Note that you can add argument that are not in the configuration file
  optimizer = params.training.optimizer(params=my_model.parameters()) 
  scheduler = params.training.scheduler(optimizer=optimizer)

Experiment tracking
*******************

This feature is still experimental.

You have two options to start the server:

1. Run the server from the commandline. You must host a MongoDB server instance.

.. code-block:: bash

  xpipe --db_host <db_ip_address> --db_port <db_port> --port <server_port> --artifacts-dir <artifacts_dir>

2. Run directly the docker image (no other dependancies needed)

.. code-block:: bash

  docker pull drosos/xpipe:0.1.2
  docker run -v <data_dir>:/data -p <server_port>:80 drosos/xpipe:0.1.2

The `<data_dir>` directory will contain the mongodb database and artifacts.

Then you can connect to http://127.0.0.1:<server_port> to access the web interface.

.. image:: https://raw.githubusercontent.com/Scotchy/XPipe/main/docs/images/gui1.png

If you open an experiment, you can get some details and results:

.. image:: https://raw.githubusercontent.com/Scotchy/XPipe/main/docs/images/gui2.png
