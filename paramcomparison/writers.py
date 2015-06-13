from __future__ import print_function

import abc

class Writer(object):

    @abc.abstractmethod
    def get_file_name(self, name):
        """
        Parameter
        ---------

        name : str
            Comparison parameter name.

        Return the file name given the comparison parameter name
        """
        return

    @abc.abstractmethod
    def write_title(self, comparison_param):
        """
        Parameter
        ---------

        comparison_param : str
            Comparison parameter name.

        Return the file title given the comparison parameter name
        """
        return

    @abc.abstractmethod
    def write_table(self, names, params, row_idx, row_values, col_idx, col_values, values):
        """
        Parameters
        ----------

        names : sequence of strings
             A sequence of names of fields.
        params : sequence of strings
             A sequence of parameters corresponding to the variable name in the same position of
             names.
        row_idx : int
             The index of the row field.
        row_values : sequence of strings
             A sequence of all possible values of the row fields.
        col_idx : int
             The index of the column field.
        col_values : sequence of strings
             A sequence of all possible values of the column fields.
        values : dict -- key : (str, str), value : str
             A dictionary whose key is an element of the Cartesion product of row_values and
             col_values, and value is the corresponding result in the table entry.

        Return the table string
        """

        return

    @abc.abstractmethod
    def write_separator(self):
        """
        Return the separator between two sets of tables.
        """
        return

import os
try:
    from StringIO import StringIO # python 2
except:
    from io import StringIO

class RstWriter(Writer):
    def __init__(self):
        pass

    def get_file_name(self, name):
        return '{}.rst'.format(name)

    def write_title(self, comparison_param):
        return comparison_param + os.linesep + '=' * len(comparison_param) + os.linesep

    def write_table(self, names, params, row_idx, row_values, col_idx, col_values, values):
        table = StringIO(os.linesep)

        # table title
        if len(names) > 2:
            table_title_list = []
            for i in range(len(names)):
                if i == row_idx or i == col_idx:
                    continue
                if i == len(names) - 1:
                    sep = ''
                table_title_list.append('{} = {}'.format(names[i], params[i]))

            table_title_list.sort()
            print(','.join(table_title_list), file = table)
            print('~' * (len(table.getvalue()) - 1), file = table)
            print('', file = table)

        # max widths of each column
        max_widths = [0 for i in range(len(col_values) + 1)]
        # max heights of each row
        max_heights = [0 for i in range(len(row_values) + 1)]

        # get the max width and column
        max_widths[0] = max(map(len, row_values)) # TODO: incorrect if '\t' is contained
        max_heights[0] = max(map(lambda x : x.count('\n'), col_values))

        for i in range(1, len(col_values) + 1):
            max_widths[i] = max(map(len, [values[(j, col_values[i - 1])] for j in row_values]))

        for i in range(1, len(row_values) + 1):
            max_heights[i] = max(map(lambda x : x.count('\n'),
                                     [values[(row_values[i - 1], j)] for j in col_values]))

        # start writing the table
        for i in range(len(row_values) + 1):
            print('+', file = table, end = '')
            for j in max_widths:
                print('-' * j, file = table, end = '+')
            print('', file = table)
            print('|', file = table, end = '')
            if i == 0: # first row is different: only column titles
                print(' ' * max_widths[0], file = table, end = '|')
                for j in range(len(col_values)):
                    print(col_values[j], file = table, end = '')
                    # fill in the rest of space with whitespaces
                    print(' ' * (max_widths[j + 1] - len(col_values[j])), file = table, end = '|')
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

        print('+', file = table, end = '')
        for j in max_widths:
            print('-' * j, file = table, end = '+')
        print('', file = table)
        print('', file = table)

        ret = table.getvalue()
        table.close()
        return ret

    def write_separator(self):
        return os.linesep + '----' + os.linesep + os.linesep
