#!/bin/env python
#coding=UTF-8
'''
    From http://babel.edgewall.org/browser/trunk/babel/util.py?rev=374#L178
'''

from itertools import izip, imap

class ordered_dict(dict):
    def __init__(self, data=None):
        dict.__init__(self, data or {})
        self._keys = dict.keys(self)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if key not in self._keys:
            self._keys.append(key)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def items(self):
        return zip(self._keys, self.values())

    def iteritems(self):
        return izip(self._keys, self.itervalues())

    def values(self):
        return map(self.get, self._keys)
        
    def itervalues(self):
        return imap(self.get, self._keys)

