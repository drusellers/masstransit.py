An Overview of MassTransit
==========================

:Author: Dru Sellers
:Release: |release|
:Date: |today|

Main Classes of MassTransit
---------------------------

Here is where we type lots of **cool** content add more cool things


neet huh?

.. note::
    this is a note

Bus
"""
.. autoclass:: masstransit.bus.Bus
    :members:

aoeu
How to subscribe to the bus::
    bus.subscribe(MessageType, lambda msg : print msg)
    bus.start()

I can type here
    i can type here too

Methods
"""""""
.. function:: masstransit.bus.Bus.subscribe(kind, callback)

.. function:: publish(msg)

