An Overview of MassTransit
==========================

:Author: Dru Sellers
:Release: |release|
:Date: |today|

Main Classes of MassTransit
---------------------------

Here is where we type lots of **cool** content add more cool things

some sample C#

.. sourcecode:: csharp

    public class Bob
    {
    
    }

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


I can type here
    i can type here too

Methods
"""""""
.. function:: masstransit.bus.Bus.subscribe(kind, callback)

.. function:: publish(msg)

