Build
==========

Build the web interface
-----------------------

To build the frontend, cd to `xpipe/server/frontend` (from the root folder of the project). 
Then open `src/config.ts` and change the `ENV` var from "dev" to "prod". Then build:  

.. code:: bash

   npm i # If you have not installed the needed dependancies yet
   npm run build # Build

Build the docker image
----------------------

From the root folder of the project: 

.. code:: bash

   sudo docker build -f docker/Dockerfile -t xpipe .

Build the documentation
-----------------------

To build the documentation, cd to `docs` (from the root folder of the project). You can then generate automatically the documentation from code comments:

.. code:: bash

   sh gen_doc.sh

And produce the html files:

.. code:: bash

   make html

All html file will be saved in `<root_folder>/docs/build/html`.




