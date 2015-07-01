Object on a Slope
=================

This is an example which will show the usage of :class:`paramcomparison.readers.UserFunctionReader`.

Let's say we have a simple physics problem: we have an object which is put on a slope. What is the
time it takes for the object to slide down to the ground, given the following 4 parameters:

- the angle of the slope :math:`\theta`,
- the coefficient of friction :math:`\mu`,
- the initial height of the object :math:`h`,
- the gravitational acceleration :math:`g` (we may not be on the Earth).

This is a rather simple problem, and the time can be computed using the following formula:

.. math::

   t = \sqrt{2h/[g \sin \theta (\sin \theta - \mu \cos \theta)]}

If :math:`t` is an imaginary number (in other words, the result in the square root is negative),
then it means the object would not slide down.

Here, we will use ParamComparison to generate tables to display the relation of the parameters with
the actual time it takes to fall down.

We create a python script to generate the tables using
:class:`paramcomparison.readers.UserFunctionReader`:

.. literalinclude:: gen_tables.py

You can download :download:`the script <gen_tables.py>` and view :doc:`the output of this example
<output/index>`.

Here we generated two pages. Each of the pages lists tables which include all the possible
combinations, but the two pages order the tables in different ways: :doc:`the page g <output/g>`
fixes :math:`h` and compare the effect of changing :math:`g` within each block separated by
horizontal lines, while :doc:`the page h <output/h>` fixes :math:`g` and compare the effect of
changing :math:`h` within each block.

This example may not be very typical though -- paramcomparison is probably more useful when it comes
to experimental data.
