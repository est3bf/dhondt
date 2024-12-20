Getting started
===============

Obtaining D'Hondt
-----------------

D'Hondt system is distributed as a Python module, and it can be installed using ``pip``
directly from the internal GitHub. It is also distributed inside a dedicated
Docker image.

Finally, to install manually D'Hondt by running (this command will install all required python
modules):

.. code-block:: bash
    
    $ git clone git@github.com:est3bf/dhondt.git
    $ pip install -U . 


We can use dedicated ``Docker images`` to run the web server using ``docker compose``
as orchestrator.

.. attention:: Do not forget to add your user to docker group

.. code-block:: bash
    
    $ sudo adduser youruser docker


Building Images
---------------

First we need to built the images.
The following is for build and run manually using docker commands.

Production
^^^^^^^^^^

.. code-block:: bash

    $ docker compose -f .gci/docker-compose.yml  -p [project name] build dhondt


[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml  -p msa_dhondt build dhondt

Development
^^^^^^^^^^^

.. code-block:: bash

    $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p [project name] build dhondt


[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p msa_dhondt build dhondt

Unit Testing
^^^^^^^^^^^^

.. code-block:: bash

     $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p [project name] build dhondt unit_testing 


[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p msa_dhondt build dhondt unit_testing

Continuos Integration (CI) Testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p [project name] build dhondt ci_testing 

[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p [project name] build dhondt ci_testing 

Creating Database Volume
------------------------

To use Postgres database we need to create a ``docker volume`` with the name ``data_postgres``
The command to create is:

.. code-block:: bash
    
    $ docker volume create data_postgres

Running containers
------------------

.. _run_webservice_container:

Production
^^^^^^^^^^

.. code-block:: bash

    $ docker compose -f .gci/docker-compose.yml  -p [project name] up -d 


[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml  -p msa_dhondt up -d 

Development
^^^^^^^^^^^

.. code-block:: bash

   $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p [project name] build dhondt


[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
   $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p msa_dhondt up -d

Unit Testing
^^^^^^^^^^^^

.. code-block:: bash

    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p [project name] up

[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p msa_dhondt up

Continuos Integration (CI) Testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To execute the documentation execute the following command:

.. code-block:: bash

    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p [project name] up

[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p msa_dhondt up


Building This Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build this documentation execute the following command:

.. code-block:: bash

    $ docker compose -f .gci/docker-compose-doc.yml -p [project name] up --build doc



Stopping containers
-------------------

.. code-block:: bash

    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml -p [project name] down 

[project name] is the project name which the image and container will have.

Example:

.. code-block:: bash
    
    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml  -p msa_dhondt down

