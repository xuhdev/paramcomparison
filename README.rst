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
    from paramcomparison.readers import UserFunctionReader

    # f can be any custom function. It can be a function which reads a data file, or computes on the
    # fly.
    def f(params, data):
        return params['a'] + params['b'] + params['c'] + params['d']

    param_space = {'a': [1,2], 'b': [3,4], 'c':[5,6], 'd': [7,8]}

    pc = paramcomparison.ParamComparison(param_space, UserFunctionReader(f, None))
    pc.generate_pages('output', RstWriter(), 'a', 'b')

The directory output will contain some rst files which contains generated tables. You can use
`Sphinx`_, `Nikola`_ or other tools to further convert them into HTML, PDF and other formats.

Source Code
-----------

The source code is available on `GitHub <https://github.com/xuhdev/paramcomparison>`__.

Bug Report and Contribution
---------------------------

Please submit bug reports to the `issue tracker
<https://github.com/xuhdev/paramcomparison/issues>`_. To contribute, please make a pull request on
`GitHub <https://github.com/xuhdev/paramcomparison/pulls>`__.

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
License version 3 in GPL.txt.

.. _Nikola: http://getnikola.com
.. _Sphinx: http://sphinx-doc.org/
