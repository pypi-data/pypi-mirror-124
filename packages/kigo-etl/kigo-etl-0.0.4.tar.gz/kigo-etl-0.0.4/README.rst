Kigo ETL framework
==============================================

.. image:: https://travis-ci.com/AsyncMicroStack/kigo-etl.svg?branch=master
   :target: http://travis-ci.com/AsyncMicroStack/kigo-etl

.. pull-quote ::
   Declarative ETL engine.

Example of usege
------------------
Let's assume that we have a file named input_1

::

   aaaaaaaaaaaaaaaaaaaaaabbbbbbbbbsome data 11      some data 2Y
   aaaaaaaaaaaaaaaaaaaaaabbbbbbbbbsome data 12      some data 2Y
   aaaaaaaaaaaaaaaaaaaaaabbbbbbbbbsome data 13      some data 2N

.. code-block:: python

   # helloworld.py

   from kigo.etl.mapper.mapping import mapping
   from kigo.etl.extractors.fabric import Extract


   @mapping
   class SomeClass:
       data_1 = Extract.TextSlice[31:43]
       data_2 = Extract.TextSlice[49:61]

What we expect is to have 3 instances of classes SomeClass where data_1 and data_2 will have proper ranges of data. For example first instance will look like:

::

   data_1 -> 'some data 11'
   data_2 -> 'some data 2Y'



Documentation
-------------

Documentation and links to additional resources are available at
https://www.asyncstack.org/kigo-etl


License
-------

Apache 2.0. See LICENSE for details.