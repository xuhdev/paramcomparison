#!/bin/env python

import paramcomparison
from paramcomparison.writers import RstWriter
from paramcomparison.readers import UserFunctionReader

# the function which computes the time for the object to fall to the ground
def compute_sliding_time(params, data):
    from math import sqrt, sin, cos

    theta = float(params['theta'])
    mu = float(params['mu'])
    g = float(params['g'])
    h = float(params['h'])

    tmp = 2 * h / (g * sin(theta) * (sin(theta) - mu * cos(theta)))
    if tmp < 0: # the object does not slide
        return 'never'
    # limit the number of digits to 2
    return '{0:.2f}'.format(sqrt(tmp))

param_space = {'theta': ('0.52', '1.05'), 'mu': ('0.1', '0.3', '1.0'),
               'g':('1.6', '3.7', '9.8'), 'h': ('1', '2', '3')}

pc = paramcomparison.ParamComparison(param_space, UserFunctionReader(compute_sliding_time, None))
pc.generate_pages('output', RstWriter(), 'theta', 'mu')
