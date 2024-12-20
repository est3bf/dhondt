DB Models
=========

This section provides the code documentation of the modules that define the D'Hondt
database model, that is, the definition of tables and data stored in the DB.

Table definitions
-----------------
UML Schema
^^^^^^^^^^

.. image:: ../dhondt_db.png
   :scale: 100 %
   :alt: alternate text
   :align: center


Tables models 
^^^^^^^^^^^^^

.. sqla-model:: dhondt.db.tabledefs.ScrutinyTable
.. sqla-model:: dhondt.db.tabledefs.DistrictTable
.. sqla-model:: dhondt.db.tabledefs.PoliticalPartyListTable
.. sqla-model:: dhondt.db.tabledefs.SeatsPoliticalPartiesTable
.. sqla-model:: dhondt.db.tabledefs.DhondtResultTable



Controller
----------
.. automodule:: dhondt.db.controller
   :members:
   :show-inheritance:

Repository
----------
.. automodule:: dhondt.db.dhondt_repository
   :members:
   :show-inheritance:

Exceptions
----------
.. automodule:: dhondt.db.exceptions
   :members:
   :show-inheritance:
