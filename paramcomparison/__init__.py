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
import copy
import itertools
import os
import sys

__version__ = '0.1.2'

class ParamComparison:
    """
    A class to initiate the generation of pages

    :type grid: dict: str -> (val0, val1, ...)
    :param grid: A dictionary whose keys are strings of variable names and values are sequences of
         values to be tried for the corresponding variable.
    :type reader: readers.Reader
    :param reader: The Reader class to load and process data.
    :type readable_names: dict: str -> str
    :param readable_names: A dictionary which maps names in grid keys to human readable names
    """

    def __init__(self, grid, reader, readable_names = dict()):

        self.names = tuple(grid.keys())
        self.name_idx = dict() # reverse look up (name --> index)
        for i in range(0, len(self.names)):
            self.name_idx[self.names[i]] = i
        self.grid = dict()
        for i in grid.items():
            v = i[1]
            self.grid[i[0]] = tuple(map(str, v))

        self.results = dict()

        self.readable_names = copy.deepcopy(readable_names)

        # For all names which don't have a human readable name, create a dummy one for them
        for name in self.names:
            if not name in self.readable_names:
                self.readable_names[name] = name

        # store all results to a dictionary to be used for further looking up
        for params in itertools.product(*grid.values()):
            func_params = dict(zip(self.names, params))
            result = str(reader.read(func_params))
            values = tuple(map(str, params))
            self.results[values] = result

    def generate_pages(self, outdir, writer, row_field, col_field):
        """
        Generate a set of pages

        :type outdir: str
        :param outdir: The directory to write files to.
        :type writer: writers.Writer
        :param writer: The writer to be used.
        :type row_field: str
        :param row_field: The field to be used in rows.
        :type col_field: str
        :param col_field: The field to be used in columns.
        """

        # make sure writer is valid
        from .writers import Writer
        if not isinstance(writer, Writer):
            raise Exception('Invalid writer. Must be an instance of paramcomparison.writers.Writer')

        try:
            os.mkdir(outdir)
        except:
            pass

        prefix = outdir
        if prefix[-1] != os.path.sep:
            prefix += os.path.sep

        # the index of the row and column field
        row_field_idx = self.names.index(row_field)
        col_field_idx = self.names.index(col_field)

        # make sure both row_field and col_field exist
        if row_field_idx == -1:
            raise Exception('Field "{}" does not exist'.format(row_field))
        if col_field_idx == -1:
            raise Exception('Field "{}" does not exist'.format(col_field))

        if len(self.names) == 2: # we only have 2 fields, just generate a table
            values = dict()
            params = [None, None]
            for r in self.grid[row_field]:
                params[row_field_idx] = r
                for c in self.grid[col_field]:
                    params[col_field_idx] = c
                    values[(r, c)] = self.results[tuple(params)]
            with open(prefix + writer.get_file_name('main'), 'w') as f:
                f.write(writer.write_title('main'))
                f.write(writer.write_table(self.names, (None, None),
                                           row_field_idx, self.grid[row_field],
                                           col_field_idx, self.grid[col_field], values,
                                           self.readable_names))
            return

        # i is the 3rd field
        for i in range(len(self.names)):

            # i is the index of the 3rd field
            if i == row_field_idx or i == col_field_idx:
                continue

            with open(prefix + writer.get_file_name(self.names[i]), 'w') as f:

                # write title first
                f.write(writer.write_title(self.readable_names[self.names[i]]))

                # subgrid with i, row_field_idx and col_field_idx removed
                subgrid = copy.deepcopy(self.grid)
                for j in (i, row_field_idx, col_field_idx):
                    subgrid.pop(self.names[j])

                # Iterate all fields except row_field and col_field. Field i is always iterated in
                # the last level. List the tables of the row field and column field for them.
                for x in itertools.product(*subgrid.values()):
                    params = [None for j in range(len(self.names))]
                    subgrid_keys = tuple(subgrid.keys())
                    for j in range(len(subgrid_keys)):
                        params[self.name_idx[subgrid_keys[j]]] = x[j]
                    for v in self.grid[self.names[i]]:
                        params[i] = v
                        # a dictionary for only row and column fields
                        values = dict()
                        for r in self.grid[row_field]:
                            params[row_field_idx] = r
                            for c in self.grid[col_field]:
                                params[col_field_idx] = c
                                values[(r, c)] = self.results[tuple(params)]

                        params[row_field_idx] = None
                        params[col_field_idx] = None
                        f.write(writer.write_table(self.names, tuple(params),
                                                   row_field_idx, self.grid[row_field],
                                                   col_field_idx, self.grid[col_field],
                                                   values, self.readable_names))

                    f.write(writer.write_separator())
