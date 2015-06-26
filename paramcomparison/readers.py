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

class Reader(object):
    """
    The base class for all readers, which define how to read and process data.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read(self, params):
        """
        :type params: dict
        :param params: A dict which contains the values of parameters.

        :return: The entry corresponding to the parameters.
        :rtype: str
        """
        pass

class UserFunctionReader(Reader):
    """
    A class which relays the reading to a user function.
    """

    def __init__(self, func, data):
        """
        :type func: function
        :param func: A user function which takes two parameters: data and params. The function is
        defined by user and will be called in read().
        """
        self.func = func
        self.data = data

    def read(self, params):
        """
        This function calls the user function. When calling the function, the first parameter is
        params, and the second parameter of the data variable passed in in :func:`__init__`.

        :return: what the func returns.

        .. seealso:: :func:`Reader.read`.
        """

        return self.func(params, self.data)
