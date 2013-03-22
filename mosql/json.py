#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''An alternative of built-in `json`.

It is compatible with :py:mod:`mosql.result` and built-in `datetime`.

.. versionadded :: 0.1.1
'''

__all__ = ['dump', 'dumps', 'load', 'loads', 'ModelJSONEncoder']

import imp

try:
    # it imports module from built-in first, so it skipped this json.py
    json = imp.load_module('json', *imp.find_module('json'))
except ImportError:
    import simplejson as json

from datetime import datetime, date
from functools import partial

from .result import Model, Row, Column

class ModelJSONEncoder(json.JSONEncoder):
    '''It is compatible with :py:mod:`mosql.result` and built-in `datetime`.'''

    def default(self, obj):

        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError, e:
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            elif isinstance(obj, Model):
                return dict(obj)
            elif isinstance(obj, Column):
                return list(obj)
            elif isinstance(obj, Row):
                return dict(obj)
            else:
                raise e

dump = partial(json.dump, cls=ModelJSONEncoder)
'''It uses the :py:class:`ModelJSONEncoder`.'''

dumps = partial(json.dumps, cls=ModelJSONEncoder)
'''It uses the :py:class:`ModelJSONEncoder`.'''

load = json.load
'''It is same as `json.load`.'''

loads = json.loads
'''It is same as `json.loads`.'''
