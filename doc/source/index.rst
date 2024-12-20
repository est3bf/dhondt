.. D'hondt Calculation System documentation master file, created by
   sphinx-quickstart on Thu Dec 19 17:27:58 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

D'hondt Calculation System documentation
========================================

Welcome to D'Hondt's documentation page, system used for allocating seats in parliaments
among federal states, or in proportional representation among political parties.
For more information please `read the article`_

.. _`read the article`: https://en.wikipedia.org/wiki/D%27Hondt_method

D'hondt Calculation System is with a API built using Flask framework and Python 
that allows assign candidates according to votes that they received.

Here, you will find guides about how to run D'Hondt web server, how to use his 
API interface, and even documentation of D'Hondt code, should you want to
submit a patch.


.. toctree::
   :maxdepth: 2
   :caption: User's guide:

   getting_started
   utils
   testing

.. toctree::
   :caption: API Reference
   :maxdepth: 1

   api_ref
   

.. toctree::
   :maxdepth: 2
   :caption: Code Reference:

   db_models
   internal_utils
   
   
.. toctree::
   :caption: Changelog
   :maxdepth: 1

   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
