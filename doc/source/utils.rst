Utils
=====

This section provides the code documentation of auxiliary helper commands
to simplify the operation, specially during the development and testing.

Commands are used as a ``bash alias`` and is founded in ``utils.sh`` file.


Sourcing the helper commands
----------------------------
First we need to include the helpers commands executing in the root folder 

.. code-block:: bash

   $ source utils.sh

Helpers Commands
----------------

Building and running application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Following simple commands perform three operation at the same time:  

* ``stopping`` running containers,  
* ``building`` application and database containers 
* ``running``  application and database containers


For production   
""""""""""""""
.. code-block:: bash

   $ drest

For develepment
"""""""""""""""

.. code-block:: bash

     $ drest_dev


Stopping containers
^^^^^^^^^^^^^^^^^^^

To stop all containers we can use: 

.. code-block:: bash

   $ downd

or also 

.. code-block:: bash

   $ dod


Executing unit and CI tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Following simple commands perform three operation at the same time to execute automatically
the desired tests:  

* ``stopping`` running containers,  
* ``building`` testing container where tests will be executed
* ``running and executing`` tests automatically

We can follow the test execution in the screen and at the end we can see the final report.

.. _exec_unit_tests:

Executing Unit tests
""""""""""""""""""""
.. code-block:: bash

   $ execute_unit_testing


.. _exec_ci_tests:

Execute CI tests
""""""""""""""""
.. code-block:: bash

     $ execute_ci_testing

Build documentation
"""""""""""""""""""

.. code-block:: bash

     $ build_doc


.. _backup_database:

Backup Database
^^^^^^^^^^^^^^^

We can backup and restore the database. A new folder ``db_data`` created to store the the files.
Each time that a new backup is created (executed), a new folder is created (named with the time) to store the information.

.. attention:: Do not remove or delete this folder until execute the restore command. All data will be lost deleting the folder.


Backup
""""""
.. code-block:: bash
   
     $ bkp_data

Restore the database
""""""""""""""""""""

The following command will restore the last backuped database. 

.. code-block:: bash

     $ restore_last_data

Clear database
""""""""""""""
     
If we want to clear all database information (delete the entirely volumen) we can execute the following command:

.. code-block:: bash

      $ clear_db

.. attention:: Don't forget backup the database before execute this command or all information will be lost. 
     
