#!/usr/bin/env python

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

from distutils.core import setup

setup(name='ParamComparison',
      version='0.1',
      description='Parameter Comparison Table Generator',
      long_description=open('README.rst').read(),
      author='Hong Xu',
      author_email='hong@topbug.net',
      url='paramcomparison.topbug.net',
      packages=['paramcomparison'],
      license='COPYING.txt'
     )
