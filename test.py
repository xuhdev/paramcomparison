import unittest
import os

import paramcomparison
from paramcomparison.writers import RstWriter

def f(a, b, c, d):
    return a + b + c + d

class TestParamComparison(unittest.TestCase):
    """
    Test the class ParamComparison
    """

    def setUp(self):
        self.param_space = {'a': [1,2], 'b': [3,4], 'c':[5,6], 'd': [7,8]}

        self.pc = paramcomparison.ParamComparison(self.param_space, f)
    def test_init(self):
        """
        Test initialization
        """

        pc = self.pc

        # test names
        self.assertEqual(len(pc.names), len(self.param_space))
        self.assertTrue('a' in pc.names and 'b' in pc.names and 'c' in pc.names and 'd' in pc.names)

        # test name_idx
        self.assertTupleEqual(
            (pc.name_idx['a'], pc.name_idx['b'], pc.name_idx['c'], pc.name_idx['d']),
            (pc.names.index('a'), pc.names.index('b'), pc.names.index('c'), pc.names.index('d')))
        self.assertTupleEqual((pc.grid['a'], pc.grid['b'], pc.grid['c'], pc.grid['d']),
                              (('1', '2'), ('3', '4'), ('5', '6'), ('7', '8')))

        # test the results dict
        k = [None, None, None, None]
        k[pc.name_idx['a']] = '1'
        k[pc.name_idx['b']] = '3'
        k[pc.name_idx['c']] = '5'
        k[pc.name_idx['d']] = '8'
        self.assertEqual(pc.results[tuple(k)], '17')
        self.assertEqual(len(pc.results), 16)

    def test_generate_pages(self):
        """
        Test generate_pages function
        """

        self.pc.generate_pages('tmp', RstWriter(), 'a', 'b')

        with open('tmp/c.rst', 'r') as f:
            c = f.read()

            # title string
            title_index = c.find('c' + os.linesep + '=')
            # table string
            t_index = c.find('''
c = 5,d = 7
~~~~~~~~~~~

+-+--+--+
| |3 |4 |
+-+--+--+
|1|16|17|
+-+--+--+
|2|17|18|
+-+--+--+

c = 6,d = 7
~~~~~~~~~~~

+-+--+--+
| |3 |4 |
+-+--+--+
|1|17|18|
+-+--+--+
|2|18|19|
+-+--+--+


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
c = 5,d = 7
~~~~~~~~~~~

+-+--+--+
| |3 |4 |
+-+--+--+
|1|16|17|
+-+--+--+
|2|17|18|
+-+--+--+

c = 5,d = 8
~~~~~~~~~~~

+-+--+--+
| |3 |4 |
+-+--+--+
|1|17|18|
+-+--+--+
|2|18|19|
+-+--+--+


----
'''.strip())

            self.assertNotEqual(title_index, -1)
            self.assertNotEqual(t_index, -1)
            self.assertLess(title_index, t_index)

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
        self.assertNotEqual(table.find('c = c_value'), -1)
        self.assertNotEqual(table.find('''
+--+----+----+
|  |b1  |b2  |
+--+----+----+
|a1|a1b1|a1b2|
+--+----+----+
|a2|a2b1|a2b2|
+--+----+----+
        '''.strip()), -1)


    def test_write_separator(self):
        """
        Test write_separator method
        """

        self.assertNotEqual(self.w.write_separator().find('----'), -1)

if __name__ == '__main__':
    unittest.main()
