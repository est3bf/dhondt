Executing Unit tests
--------------------

This project uses `pytest`_ library to perform unit test

.. _`pytest`: https://docs.pytest.org/en/stable/

There is 2 main test group:

* Database models tests
* Doundt service tests

Database models tests
"""""""""""""""""""""
To persist the data used in this project we use a Postgres data base engine. To access and 
control this database an Object Relational Mapping (ORM) provided by `SqlAlchemy`_ framework.

The goal of this group of test is testing the database schema and the object relationship definitions.

In order to speed up the tests and avoid to use a persistent database, we use a memory based database 
(``sqlite:///:memory:``) that is equivalent to our persistent one.

We also use the `hypothesis`_ library to create the standard and corner cases. This library creates 
random cases and special corner cases automatically.

.. _`hypothesis`: https://hypothesis.readthedocs.io/en/latest/
.. _`SqlAlchemy`: https://www.sqlalchemy.org/

Manual execution
^^^^^^^^^^^^^^^^

Without container
"""""""""""""""""
First we need to install the D'Hondt project. In the root folder of project we need execute in a terminal

.. code-block:: bash
    
    $ pip install -U . 

Then, in the same root folder, we execute the unit tests in a terminal:

.. code-block:: bash
    
    $ pytest -vv

Using containers
""""""""""""""""

To run the test we use the `dhondt-unit_testing` image and use the `unit-test` profile.
The following command built the images and run the unit-test container that executes all unit tests

.. code-block:: bash
   
   $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p msa_dhondt up --build dhondt unit_testing 


Execution with helper command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use simple commands using the container see :ref:`exec_unit_tests` 


Executing CI tests
------------------

To perform continuos integration (CI) test this project uses `schemathesis`_ framework.
This framework analyses the `OpenApi` API definition file `dhondt.yaml`, which provides 
to Schematesis all information about the endpoint (models), types, and how the are linked.

This library work together with `Hipothesis` library to create the standard and corner cases.

Because it's an continuos integration test we need to have both web server and database containers
up before running the test.

.. _`schemathesis`: https://schemathesis.readthedocs.io/en/stable/

Manual execution
^^^^^^^^^^^^^^^^


Without testing container
"""""""""""""""""""""""""

First we need to install the D'Hondt project. In the root folder of project we need execute in a terminal

.. code-block:: bash
    
    $ pip install -U . 


Then, run the web service containers and database containers. Refer to :ref:`run_webservice_container`

Finally iwe execute the unit tests in a terminal:

.. code-block:: bash
    
    $ schemathesis run src/dhondt/web/dhondt.yaml --base-url=http://localhost:5000/dhondt/v1  --hypothesis-database=none --output-truncate=false --validate-schema=true --checks=all


Using testing container
"""""""""""""""""""""""

We launch all containers with following command

.. code-block:: bash

   $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml -p msa_dhondt up --build dhondt ci_testing


Execution with helper command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to use simple commands see :ref:`exec_ci_tests` 

