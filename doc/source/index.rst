.. PipeML documentation master file, created by
   sphinx-quickstart on Sun Dec 27 23:16:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PipeML's documentation !
===================================

PipeML is a library that I started developping in December 2020 for my personal use.
As it might be useful for other people, I decided to publish the code as an open source project on Github.

PipeML focuses on two principal components to make Data Science easier: *configuration files* and *experiment tracking*.

- Configuration files are a big concern in data science field. It can become a true nightmare as you probably want to handle traceability and adopt a clean approach while dealing with a lot of configuration files. But there is no standard today. PipeML facilitates your work by automatically loading python objects from a yaml configuration. You can also easily include other yaml files into another for instance.

- The web interface will enable you to easily organize your experiments into folder, filter them and to plot different kind of graphs. You would particularly appreciate the library if you need to have an overview of a lot of your experiments.

The philosophy behind the project is to be simple and customizable.

As a team, you can run a single PipeML server for everyone. It will promote exchange as everyone can easily share their work with others.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Configuration files
===================

Here is a simple example of how to use yaml configuration file to seamlessly load objects needed to run your experiments.

.. code-block:: yaml

   training:
      gpu: !env CUDA_VISIBLE_DEVICES # Get the value of env variable CUDA_VISIBLE_DEVICES
      epochs: 18
      batch_size: 100

      optimizer: !obj torch.optimSGD : {lr : 0.001}

      scheduler: !obj torch.optim.lr_scheduler.MultiStepLR : {milestones: [2, 6, 10, 14]}

      loss: !obj torch.nn.BCELoss : {}

   model: !include "./models/my_models.yaml"

   transforms:
      !obj transforms.Normalize : {}
      !obj transforms.Noise : {}
      !obj transforms.RandomFlip : {probability: 0.5}

Then you can load the configuration file:

.. code-block:: python

   from pipeml.config import load_config

   conf = load_config("my_config.yaml")
   epochs = conf.training.epochs() # 18

   # Define your model
   # ...

   # Directly instantiate your optimizer and scheduler from configuration
   # Note that you can add argument that are not in the configuration file
   optimizer = params.training.optimizer(params=my_model.parameters()) 
   scheduler = params.training.scheduler(optimizer=optimizer)

Experiment tracking
===================
