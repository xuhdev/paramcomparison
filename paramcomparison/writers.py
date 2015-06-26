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

from __future__ import print_function

import abc

class Writer(object):
    """
    The base class for all writers, which define how to write output in specific formats.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_file_name(self, name):
        """
        :type name: str
        :param name: Comparison parameter name.

        :return: the file name given the comparison parameter name
        :rtype: str
        """
        pass

    @abc.abstractmethod
    def write_title(self, comparison_param):
        """
        :type comparison_param: str
        :param comparison_param: Comparison parameter name.

        :return: the file title given the comparison parameter name
        :rtype: str
        """
        pass

    @abc.abstractmethod
    def write_table(self, names, params, row_idx, row_values, col_idx, col_values,
                    values):
        """
        :type names: sequence of strings
        :param names: A sequence of names of fields.
        :type params: sequence of strings
        :param params: A sequence of parameters corresponding to the variable name in the same
             position of names.
        :type row_idx: int
        :param row_idx: The index of the row field.
        :type row_values: sequence of strings
        :param row_values: A sequence of all possible values of the row fields.
        :type col_idx: int
        :param col_idx: The index of the column field.
        :type col_values: sequence of strings
        :param col_values: A sequence of all possible values of the column fields.
        :type values: dict: (str, str) -> str
        :param values: A dictionary whose key is an element of the Cartesion product of row_values
             and col_values, and value is the corresponding result in the table entry.

        :return: the table string
        :rtype: str
        """

        pass

    @abc.abstractmethod
    def write_separator(self):
        """
        :return: the separator between two sets of tables.
        :rtype: str
        """
        pass

import os
try:
    from StringIO import StringIO # python 2
except:
    from io import StringIO

class RstWriter(Writer):
    """
    A class to write RST output.
    """

    def __init__(self, indent_size = 4):
        """
        :type indent_size: int
        :param indent_size: The size of indent used in the rst output. Must be greater than 0.
        """
        self.indent_size = indent_size

    def get_file_name(self, name):
        """
        See :func:`Writer.get_file_name`.
        """
        return '{}.rst'.format(name)

    def write_title(self, comparison_param):
        """
        See :func:`Writer.write_title`.
        """
        return comparison_param + os.linesep + '=' * len(comparison_param) + os.linesep

    def write_table(self, names, params, row_idx, row_values, col_idx, col_values,
                    values):
        """
        See :func:`Writer.write_table`.
        """

        table = StringIO(os.linesep)

        # table title
        print ('.. table::', file = table, end = '')
        if len(names) > 2:
            print (' ', file = table, end = '') # need an extra space
            table_title_list = []
            for i in range(len(names)):
                if i == row_idx or i == col_idx:
                    continue
                if i == len(names) - 1:
                    sep = ''
                table_title_list.append('{} = {}'.format(names[i], params[i]))

            table_title_list.sort()
            print(', '.join(table_title_list), file = table)
        else:
            print('', file = table)
        print('', file = table)

        # The first cell shows what are the rows and what are the cols
        first_cell_line_1 = 'Row: ' + names[row_idx]
        first_cell_line_2 = 'Col: ' + names[col_idx]

        # max widths of each column
        max_widths = [0 for i in range(len(col_values) + 1)]
        # max heights of each row
        max_heights = [0 for i in range(len(row_values) + 1)]

        # get the max width and column
        max_widths[0] = max(map(len, row_values)) # TODO: incorrect if '\t' is contained
        max_widths[0] = max(max_widths[0], len(first_cell_line_1), len(first_cell_line_2))
        max_heights[0] = max(map(lambda x : x.count('\n'), col_values))
        if max_heights[0] < 2: # first cell has 2 lines
            max_heights[0] = 2

        for i in range(1, len(col_values) + 1):
            max_widths[i] = max(map(len, [values[(j, col_values[i - 1])] for j in row_values]))

        for i in range(1, len(row_values) + 1):
            max_heights[i] = max(map(lambda x : x.count('\n'),
                                     [values[(row_values[i - 1], j)] for j in col_values]))

        # start writing the table
        for i in range(len(row_values) + 1):
            print(' ' * self.indent_size + '+', file = table, end = '')
            for j in max_widths:
                print('-' * j, file = table, end = '+')
            print('', file = table)
            print(' ' * self.indent_size + '|', file = table, end = '')
            if i == 0: # first row is different: only column titles
                print(first_cell_line_1, file = table, end = '')
                print(' ' * (max_widths[0] - len(first_cell_line_1)), file = table, end = '|')
                for j in range(len(col_values)):
                    print(col_values[j], file = table, end = '')
                    # fill in the rest of space with whitespaces
                    print(' ' * (max_widths[j + 1] - len(col_values[j])), file = table, end = '|')
                print('', file = table)
                # line 2
                print(' ' * self.indent_size + '|', file = table, end = '')
                print(first_cell_line_2, file = table, end = '')
                print(' ' * (max_widths[0] - len(first_cell_line_2)), file = table, end = '|')
                for j in range(1, len(max_widths)): # line 2 only has spaces
                    print(' ' * max_widths[j], file = table, end = '|')
                print('', file = table)
                continue

            # the rest of the row should print row names first
            print(row_values[i - 1], file = table, end = '')
            # fill in the rest of space with whitespaces
            print(' ' * (max_widths[0] - len(row_values[i - 1])), file = table, end = '|')

            for j in range(len(col_values)):
                v = values[(row_values[i - 1], col_values[j])]
                print(v, file = table, end = '')
                # fill in the rest of space with whitespaces
                print(' ' * (max_widths[j + 1] - len(v)), file = table, end = '|')
            print('', file = table)

        print(' ' * self.indent_size + '+', file = table, end = '')
        for j in max_widths:
            print('-' * j, file = table, end = '+')
        print('', file = table)
        print('', file = table)

        ret = table.getvalue()
        table.close()
        return ret

    def write_separator(self):
        """
        See :func:`Writer.write_separator`.
        """

        return os.linesep + '----' + os.linesep + os.linesep
