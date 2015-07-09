# Copyright (c) 2015 Hong Xu <hong@topbug.net>

# This file is part of ParamComparison.

# ParamComparison is free software: you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.

# ParamComparison is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along with
# ParamComparison. If not, see <http://www.gnu.org/licenses/>.

import unittest
import os

import paramcomparison
from paramcomparison.writers import RstWriter
from paramcomparison.readers import UserFunctionReader

def f(params, data):
    return params['a'] + params['b'] + params['c'] + params['d']

class TestParamComparison(unittest.TestCase):
    """
    Test the class ParamComparison
    """

    def setUp(self):
        self.param_space = {'a': [1,2], 'b': [3,4], 'c':[5,6], 'd': [7,8,9]}

        # the main object for testing
        self.pc = paramcomparison.ParamComparison(self.param_space, UserFunctionReader(f, None))

    def test_init(self):
        """
        Test initialization
        """

        # When a non-Reader instance is passed in, make sure TypeError is raised
        self.assertRaises(TypeError, paramcomparison.ParamComparison, self.param_space, None)

        pc = self.pc

        # test names
        self.assertEqual(len(pc.names), len(self.param_space))
        self.assertTrue('a' in pc.names and 'b' in pc.names and 'c' in pc.names and 'd' in pc.names)

        # test name_idx
        self.assertTupleEqual(
            (pc.name_idx['a'], pc.name_idx['b'], pc.name_idx['c'], pc.name_idx['d']),
            (pc.names.index('a'), pc.names.index('b'), pc.names.index('c'), pc.names.index('d')))
        self.assertTupleEqual((pc.grid['a'], pc.grid['b'], pc.grid['c'], pc.grid['d']),
                              (('1', '2'), ('3', '4'), ('5', '6'), ('7', '8', '9')))

        # test the results dict
        k = [None, None, None, None]
        k[pc.name_idx['a']] = '1'
        k[pc.name_idx['b']] = '3'
        k[pc.name_idx['c']] = '5'
        k[pc.name_idx['d']] = '8'
        self.assertEqual(pc.results[tuple(k)], '17')
        self.assertEqual(len(pc.results), 24)

    def test_generate_pages(self):
        """
        Test generate_pages function
        """

        # When a non-Writer instance is passed in, make sure TypeError is raised
        self.assertRaises(TypeError, self.pc.generate_pages, 'tmp', None, 'a', 'b')

        # Make sure when non-existent field is given we raise error
        self.assertRaisesRegexp(ValueError, 'Field "non-existent-field" does not exist',
                               self.pc.generate_pages,
                               'tmp', RstWriter(), 'non-existent-field', 'b')
        self.assertRaisesRegexp(ValueError, 'Field "non-existent-field" does not exist',
                               self.pc.generate_pages,
                               'tmp', RstWriter(), 'a', 'non-existent-field')

        self.pc.generate_pages('tmp', RstWriter(), 'a', 'b')

        with open('tmp/c.rst', 'r') as f:
            c = f.read()

            # title string
            title_index = c.find('c' + os.linesep + '=')
            # table string
            t_index = c.find('''
.. table:: c = 5, d = 7

    +------+--+--+
    |Row: a|3 |4 |
    |Col: b|  |  |
    +------+--+--+
    |1     |16|17|
    +------+--+--+
    |2     |17|18|
    +------+--+--+

.. table:: c = 6, d = 7

    +------+--+--+
    |Row: a|3 |4 |
    |Col: b|  |  |
    +------+--+--+
    |1     |17|18|
    +------+--+--+
    |2     |18|19|
    +------+--+--+


----
            '''.strip())

            self.assertNotEqual(title_index, -1)
            self.assertNotEqual(t_index, -1)
            self.assertLess(title_index, t_index)

        with open('tmp/d.rst', 'r') as f:
            d = f.read()

            # title string
            title_index = d.find('d' + os.linesep + '=')
            # table string
            t_index = d.find('''
.. table:: c = 5, d = 7

    +------+--+--+
    |Row: a|3 |4 |
    |Col: b|  |  |
    +------+--+--+
    |1     |16|17|
    +------+--+--+
    |2     |17|18|
    +------+--+--+

.. table:: c = 5, d = 8

    +------+--+--+
    |Row: a|3 |4 |
    |Col: b|  |  |
    +------+--+--+
    |1     |17|18|
    +------+--+--+
    |2     |18|19|
    +------+--+--+

.. table:: c = 5, d = 9

    +------+--+--+
    |Row: a|3 |4 |
    |Col: b|  |  |
    +------+--+--+
    |1     |18|19|
    +------+--+--+
    |2     |19|20|
    +------+--+--+


----
            '''.strip())

            self.assertNotEqual(title_index, -1)
            self.assertNotEqual(t_index, -1)
            self.assertLess(title_index, t_index)

            # ---- should not end the file
            last_separator_index = d.rfind('----')
            last_plus_index = d.rfind('+')
            self.assertLess(last_separator_index, last_plus_index)

    def test_generate_pages_2_params(self):
        """
        Test generate_pages when there are only2 parameters
        """

        pc = paramcomparison.ParamComparison({'a': ('a1', 'a2'), 'b': ('b1', 'b2')},
                        UserFunctionReader(lambda params, data: params['a'] + params['b'], None))
        pc.generate_pages('tmp2', RstWriter(), 'a', 'b')

        with open('tmp2/main.rst', 'r') as f:
            m = f.read()
            title_index = m.find('''
main
====
            '''.strip())
            t_index = m.find('''
.. table::

    +------+----+----+
    |Row: a|b1  |b2  |
    |Col: b|    |    |
    +------+----+----+
    |a1    |a1b1|a1b2|
    +------+----+----+
    |a2    |a2b1|a2b2|
    +------+----+----+
            '''.strip())

            self.assertNotEqual(title_index, -1)
            self.assertNotEqual(t_index, -1)
            self.assertLess(title_index, t_index)

    def test_generate_pages_3_params(self):
        """
        Test generate_pages when there are 3 parameters
        """

        pc = paramcomparison.ParamComparison(
            {'a': ('a1', 'a2'), 'b': ('b1', 'b2'), 'c': ('c1', 'c2')},
            UserFunctionReader(lambda params, data: params['a'] + params['b'] + params['c'], None))
        pc.generate_pages('tmp3', RstWriter(), 'a', 'b')

        with open('tmp3/c.rst', 'r') as f:
            c = f.read()
            title_index = c.find('''
c
=
            '''.strip())
            t_index = c.find('''
.. table:: c = c1

    +------+------+------+
    |Row: a|b1    |b2    |
    |Col: b|      |      |
    +------+------+------+
    |a1    |a1b1c1|a1b2c1|
    +------+------+------+
    |a2    |a2b1c1|a2b2c1|
    +------+------+------+

.. table:: c = c2

    +------+------+------+
    |Row: a|b1    |b2    |
    |Col: b|      |      |
    +------+------+------+
    |a1    |a1b1c2|a1b2c2|
    +------+------+------+
    |a2    |a2b1c2|a2b2c2|
    +------+------+------+
            '''.strip())

            self.assertNotEqual(title_index, -1)
            self.assertNotEqual(t_index, -1)
            self.assertLess(title_index, t_index)

    def tearDown(self):
        import shutil
        shutil.rmtree('tmp', True)
        shutil.rmtree('tmp2', True)
        shutil.rmtree('tmp3', True)

class TestRstWriter(unittest.TestCase):
    """
    Test the class writers.RstWriter
    """

    def setUp(self):
        self.w = RstWriter()

    def test_get_file_name(self):
        """
        Test get_file_name
        """

        self.assertEqual(self.w.get_file_name('test'), 'test.rst')

    def test_write_title(self):
        """
        Test write_title method
        """

        title = 'Test'
        self.assertNotEqual(self.w.write_title(title).find(title), -1)
        self.assertNotEqual(self.w.write_title(title).find('==='), -1)

    def test_write_table(self):
        """
        Test write_table method
        """

        names = ('a', 'b', 'c')
        params = (None, None, 'c_value')
        row_idx = 0
        col_idx = 1

        table = self.w.write_table(('a', 'b', 'c'), (None, None, 'c_value'),
                                   0, ('a1', 'a2'), 1, ('b1', 'b2'),
                                   {('a1', 'b1'): 'a1b1',
                                    ('a1', 'b2'): 'a1b2',
                                    ('a2', 'b1'): 'a2b1',
                                    ('a2', 'b2'): 'a2b2'})
        self.assertNotEqual(table.find('.. table:: c = c_value'), -1)
        self.assertNotEqual(table.find('''
    +------+----+----+
    |Row: a|b1  |b2  |
    |Col: b|    |    |
    +------+----+----+
    |a1    |a1b1|a1b2|
    +------+----+----+
    |a2    |a2b1|a2b2|
    +------+----+----+
        '''.strip()), -1)

        # Test empty entry case
        table = self.w.write_table(('a', 'b', 'c'), (None, None, 'c_value'),
                                   0, ('a1', 'a2'), 1, ('b1', 'b2'),
                                   {('a1', 'b1'): '',
                                    ('a1', 'b2'): 'a1b2',
                                    ('a2', 'b1'): '',
                                    ('a2', 'b2'): 'a2b2'})
        self.assertNotEqual(table.find('.. table:: c = c_value'), -1)
        self.assertNotEqual(table.find('''
    +------+--+----+
    |Row: a|b1|b2  |
    |Col: b|  |    |
    +------+--+----+
    |a1    |  |a1b2|
    +------+--+----+
    |a2    |  |a2b2|
    +------+--+----+
        '''.strip()), -1)


    def test_write_separator(self):
        """
        Test write_separator method
        """

        self.assertNotEqual(self.w.write_separator().find('----'), -1)

class TestReader(unittest.TestCase):
    def test_abstract(self):
        from paramcomparison.readers import Reader
        self.assertRaises(TypeError, Reader)

class TestWriter(unittest.TestCase):
    def test_abstract(self):
        from paramcomparison.writers import Writer
        self.assertRaises(TypeError, Writer)

if __name__ == '__main__':
    unittest.main()
