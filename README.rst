ParamComparison
===============

ParamComparison is a Python package which can generate a series of tables to display results of
different parameter combinations. It is useful when trying different parameters to see how good the
results are.

Install
-------

To install, run:
::

    python setup.py install

Or use pip:
::

    pip install ParamComparison

Usage
-----
The basic usage is simple:
::

    import paramcomparison
    from paramcomparison.writers import RstWriter

    def f(a, b, c, d): # or other functions to compute the result
        return a + b + c + d

    param_space = {'a': [1,2], 'b': [3,4], 'c':[5,6], 'd': [7,8]}

    pc = paramcomparison.ParamComparison(param_space, f)
    pc.generate_pages('output', RstWriter(), 'a', 'b')

The directory output will contain some rst files which contains generated tables. You can use
`Sphinx`_, `Nikola`_ or other tools to further convert them into HTML, PDF or other format.

Bug Report
----------

Please submit bug reports to the `issue tracker
<https://github.com/xuhdev/paramcomparison/issues>`_.

License
-------

Copyright (c) 2015 Hong Xu <hong@topbug.net>

ParamComparison is free software: you can redistribute it and/or modify it under the terms of the
GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

ParamComparison is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with ParamComparison.
If not, see <http://www.gnu.org/licenses/>.

You can view the full text of the license in LICENSE.txt. You can also view GNU General Public
License in GPL.txt.

.. _Nikola: http://getnikola.com
.. _Sphinx: http://sphinx-doc.org/
