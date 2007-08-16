# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2006 Ali Sabil <ali.sabil@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import UserDict
import anydbm

try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

__all__=('MemoryStorage', 'DbmStorage')

_storage = None

def set_storage(klass):
    global _storage
    _storage = klass

def get_storage(*args):
    global _storage
    if _storage is None:
        _storage = MemoryStorage
    if len(args) == 2:
        return _storage(*args)
    else:
        return _storage

class AbstractStorage(UserDict.DictMixin):
    """Base class for storage objects, storage objects are
    a way to let pymsn and the client agree on how data may
    be stored. This data included security tokens, cached
    display pictures ..."""

    def __init__(self, account, identifier):
        """Initializer
        
        @param identifier: the identifier of this storage instance
        @type identifier: string"""
        self.account = account
        self.storage_id = identifier
    
    def keys(self):
        raise NotImplementedError("Abstract method call")
    
    def has_key(self, key):
        return key in self.keys()

    def get(self, key, default=None):
        if self.has_key(key):
            return self[key]
        return default

    def __len__(self):
        return len(self.keys)

    def __contains__(self, key):
        return self.has_key(key)

    def __getitem__(self, key):
        raise NotImplementedError("Abstract method call")

    def __setitem__(self, key, value):
        raise NotImplementedError("Abstract method call")

    def __delitem__(self, key):
        raise NotImplementedError("Abstract method call")

    def __del__(self):
        raise NotImplementedError("Abstract method call")

    def close(self):
        pass


_MemoryStorageDict = {}
class MemoryStorage(AbstractStorage):
    """In memory storage type"""
    
    def __init__(self, account, identifier):
        AbstractStorage.__init__(self, account, identifier)
        if account + "/" + identifier not in _MemoryStorageDict:
            _MemoryStorageDict[account + "/" + identifier] = {}

    def keys(self):
        return _MemoryStorageDict[self.account + "/" + self.storage_id].keys()
    
    def has_key(self, key):
        return key in self.keys()

    def __len__(self):
        return len(self.keys)

    def __contains__(self, key):
        return self.has_key(key)

    def __getitem__(self, key):
        return _MemoryStorageDict[self.account + "/" + self.storage_id][key]

    def __setitem__(self, key, value):
        _MemoryStorageDict[self.account + "/" + self.storage_id][key] = value

    def __delitem__(self, key):
        del _MemoryStorageDict[self.account + "/" + self.storage_id][key]

    def __del__(self):
        pass

    def close(self):
        pass


class DbmStorage(AbstractStorage):

    PICKLING_PROTOCOL = -1 #use the highest possible version
    STORAGE_PATH = "~/.pymsn"

    def __init__(self, account, identifier):
        import os.path
        AbstractStorage.__init__(self, account, identifier)
        
        storage_path = os.path.expanduser(self.STORAGE_PATH)
        
        file_dir = os.path.join(storage_path, self.account)
        file_path = os.path.join(file_dir, self.storage_id)
        try:
            import os
            os.makedirs(file_dir)
        except:
            pass
        self._dict = anydbm.open(file_path, 'c')
    
    def keys(self):
        return self._dict.keys()
    
    def has_key(self, key):
        return self._dict.has_key()

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        return self._dict.has_key()

    def __getitem__(self, key):
        f = StringIO(self._dict[str(key)]) # some dbm don't support int keys
        return Unpickler(f).load()

    def __setitem__(self, key, value):
        f = StringIO()
        pickler = Pickler(f, self.PICKLING_PROTOCOL)
        pickler.dump(value)
        self._dict[str(key)] = f.getvalue()
        if hasattr(self._dict, 'sync'):
            self._dict.sync()

    def __delitem__(self, key):
        del self._dict[str(key)]

    def __del__(self):
        self.close()
    
    def close(self):
        if hasattr(self._dict, 'sync'):
            self._dict.sync()
        self._dict.close()

