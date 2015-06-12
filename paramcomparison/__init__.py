from __future__ import print_function
import copy
import itertools
import os
import sys

class ParamComparison:

    def __init__(self, grid, func):
        self.names = tuple(grid.keys())
        self.name_idx = dict() # reverse look up (name --> index)
        for i in range(0, len(self.names)):
            self.name_idx[self.names[i]] = i
        self.grid = dict()
        for i in grid.items():
            v = i[1]
            self.grid[i[0]] = tuple(map(str, v))

        self.results = dict()

        # store all results to a dictionary to be used for further looking up
        for params in itertools.product(*grid.values()):
            func_params = dict(zip(self.names, params))
            result = str(func(**func_params))
            values = tuple(map(str, params))
            self.results[values] = result

    def generate_pages(self, outdir, writer, row_field, col_field):
        """
        Generate a set of pages
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
                                           col_field_idx, self.grid[col_field], values))
            return

        # i is the 3rd field
        for i in range(len(self.names)):

            # i is the index of the 3rd field
            if i == row_field_idx or i == col_field_idx:
                continue

            with open(prefix + writer.get_file_name(self.names[i]), 'w') as f:

                # write title first
                f.write(writer.write_title(self.names[i]))

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
                                                col_field_idx, self.grid[col_field], values))

                    f.write(writer.write_separator())
