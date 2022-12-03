.. image:: https://img.shields.io/badge/python-%3E%3D%203.5-blue
  
Introduction
************

XPipe is a library that I started developping in December 2020 for my personal use.

XPipe facilitates your work by automatically loading python objects from a yaml configuration. 
You can also easily include yaml files into another one.

It is an interesting tool to improve your workflow, make it reproducible and make your configurations more readable.

Getting started
***************

.. code-block:: bash

  pip install xpipe


Documentation: https://x-pipe.readthedocs.io/en/latest/

Configuration files
*******************

XPipe leverages yaml tag power to seamlessly load needed objects and more.
Here is a simple example:

.. code-block:: yaml

  training:
    gpu: !env CUDA_VISIBLE_DEVICES # Get the value of env variable CUDA_VISIBLE_DEVICES
    epochs: 18
    batch_size: 100

    optimizer:
      !obj torch.optim.SGD : {lr : 0.001}

    scheduler:
      !obj torch.optim.lr_scheduler.MultiStepLR : {milestones: [2, 6, 10, 14]}

    loss:
      !obj torch.nn.BCELoss : {}

  model: !include "./models/my_model.yaml"

  transforms:
    - !obj transforms.Normalize : {}
    - !obj transforms.Noise : {}
    - !obj transforms.RandomFlip : {probability: 0.5}


In your `models/my_model.yaml` file, you can define your model and its parameters (assuming that you defined a module 'models' and a class 'Model1' in it).

.. code-block:: yaml

  definition: 
    !obj models.Model1 :
      n_hidden: 100


Then you can load the configuration file:

.. code-block:: yaml

  from xpipe.config import load_config

  conf = load_config("experiment.yaml")
  epochs = conf.training.epochs() # 18

  # Instantiate your model defined in models/my_model.yaml
  my_model = conf.model.definition()

  # Directly instantiate your optimizer and scheduler from configuration
  # Note that you can add argument that are not in the configuration file
  optimizer = conf.training.optimizer(params=my_model.parameters())
  scheduler = conf.training.scheduler(optimizer=optimizer)


See a description of all tags `here <https://x-pipe.readthedocs.io/en/latest/tags.html>`_

Try by yourself the examples in the `examples` folder.
