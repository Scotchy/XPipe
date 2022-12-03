List of tags
============

Instantiate an object
*********************

Yaml syntax
-----------


Use the `!obj` tag


.. code-block:: yaml

    array: 
        !obj numpy.array: { object: [1, 2, 3, 4] }

You can also define its parameters in another file:

.. code-block:: yaml

    array: 
        !obj numpy.array: !include "path/to/params.yaml"


params.yaml:

.. code-block:: yaml

    object: [1, 2, 3, 4]


Use it in python
----------------

Use the following code to instantiate the object

.. code-block:: python
    
    my_array = conf.array()


If all arguments are not given in the configuration file or you want to overwrite some of them:

.. code-block:: python

    my_object = conf.object(
        arg1=1,
        arg2="value"
    )


Instantiate a list of objects
*****************************

Yaml syntax
-----------

Use the `!obj` tag in a list.


.. code-block:: yaml

    list_of_arrays:
        - !obj numpy.array: { object: [1, 2, 3, 4] }
        - !obj numpy.array: { object: [2, 3, 4, 5] }


Use it in python
----------------

.. code-block:: python

    first_array = conf.list_of_arrays[0]() # Instantiate only the first object
    first_object = conf.list_of_objects[0](
        arg1=1,
        arg2="value"
    ) # Instantiate only the first object of a list of objects with arguments not defined in conf

    all_instantiated_arrays = conf.list_of_arrays() # Instantiate all objects in a list 
    all_instantiated_objects = conf.list_of_objects(
        args1=1,
        arg2="value"
    ) # Instantiate all objects of a list of objects with arguments not defined in conf



Reference to a class
********************

Yaml syntax
-----------

If you want to store a class without instantiating it, use the `!class` tag

.. code-block:: yaml

    my_class: !class numpy.array


Use it in python
----------------

Use the reference just as the node it refers to.


Include another config file
***************************

Yaml syntax
-----------

Use the `!include` tag

.. code-block:: yaml

    included_conf: !include "path/to/conf.yaml"


The path can be absolute or relative to the **current configuration file**.

Use it in python
----------------

Use the included config just as if you had copy/paste the content of the included config in the node.

For example, assuming `a`=1 is defined in `conf.yaml`:

.. code-block:: python

    a = conf.included_conf.a()


Import another configuration file
*********************************

Yaml syntax
-----------

Use the `!from` tag in association with the `!include` tag.
`!from` will get all includes, merge them and put the result in the current node.

.. code-block:: yaml

    imported_conf:
        !from :
            - !include "path/to/conf1.yaml"
            - !include "path/to/conf2.yaml"
            - !include "path/to/conf3.yaml"
        b: 2

If the variable is defined in multiple files, the highest priority is given to the last included one (here the conf3.yaml file).

If the variable is defined after the `!from` tag (at the same level), it will overwrite the value defined in included file. 

For example, here the value of `b` will be 2 whatever the value of `b` is in conf1.yaml, conf2.yaml or conf3.yaml.

Use it in python
----------------

Assuming:

conf1.yaml:

.. code-block:: yaml

    a: 1

conf2.yaml:

.. code-block:: yaml

    a: 2
    b: 1

conf3.yaml:

.. code-block:: yaml

    c: 2

.. code-block:: python

    a = conf.imported_conf.a() # is equal to 2 because conf2.yaml has the priority on conf1.yaml
    b = conf.imported_conf.b() # is equal to 2 because it is overwritten 
    c = conf.imported_conf.c() # is equal to 2


Get the value of an env variable
********************************

Yaml syntax
-----------

You can recover the value of an environment variable using the `!env` tag.

.. code-block:: yaml

    my_env_var: !env ENV_VARIABLE

Use it in python
----------------

.. code-block:: python

    my_env_var = conf.my_env_var()


Format a string
***************

Yaml syntax
-----------

Use the `!f` tag (such as in python).

.. code-block:: yaml

    string: !f "Hi $USER !"

Where `$USER` is an environment variable.

Use it in python
----------------

.. code-block:: python

    my_string = conf.string() # is equal to "Hi root !" if $USER = "root"


Refer to another variable
************************************

Yaml syntax
-----------

Use the `!ref` tag 

.. code-block:: yaml
    
    experiment:
        training:
            batch_size: 100

        relative_ref_to_batch_size: !ref training/batch_size # 100
        absolute_ref_to_batch_size: !ref /experiment/training/batch_size # 100
        relative_ref_to_cpu: ../resources/cpu # 2

    resources:
        cpu: 2

Use it in python
----------------

.. code-block:: python

    batch_size = conf.experiment.relative_ref_to_batch_size() # is equal to 100 
    batch_size = conf.experiment.absolute_ref_to_batch_size() # is equal to 100 
    batch_size = conf.experiment.relative_ref_to_cpu() # is equal to 2


    

