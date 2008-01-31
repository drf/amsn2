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

import pymsn.util.string_io as StringIO
try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

import UserDict
import anydbm
import random
from Crypto.Hash import SHA
from Crypto.Cipher import Blowfish

__all__ = ['MemoryStorage', 'DbmStorage', 'DecryptError']

_storage = None

def set_storage(klass):
    global _storage
    _storage = klass

def get_storage(*args):
    global _storage
    if _storage is None:
        _storage = MemoryStorage
    if len(args) > 0:
        return _storage(*args)
    else:
        return _storage


class BlowfishCipher:
    def __init__(self, key):
        self._cipher = Blowfish.new(key)

    def encrypt(self, data):
        return self._cipher.encrypt(self.__add_padding(data))

    def decrypt(self, data):
        return self.__remove_padding(self._cipher.decrypt(data))

    def __add_padding(self, data):
        padding_length = 8 - (len(data) % 8)                                 
        for i in range(padding_length - 1):
            data += chr(random.randrange(0, 256))
        data += chr(padding_length)
        return data

    def __remove_padding(self, data):
        padding_length = ord(data[-1]) % 8
        if padding_length == 0:
            padding_length = 8
        return data[:-padding_length]


class DecryptError(Exception):
    pass


class AbstractStorage(UserDict.DictMixin):
    """Base class for storage objects, storage objects are
    a way to let pymsn and the client agree on how data may
    be stored. This data included security tokens, cached
    display pictures ..."""

    def __init__(self, account, password, identifier):
        """Initializer
        
        @param identifier: the identifier of this storage instance
        @type identifier: string"""
        self.account = account
        self.cipher = BlowfishCipher(SHA.new(password).digest())
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

    # Helper functions
    def _pickle_encrypt(self, value):
        f = StringIO.StringIO()
        pickler = Pickler(f, -1)
        pickler.dump(value)
        data = self.account + f.getvalue() # prepend a known value to check decrypt
        return self.cipher.encrypt(data)

    def _unpickle_decrypt(self, data):
        data = self.cipher.decrypt(data)

        if not data.startswith(self.account):
            raise DecryptError()
        data = data[len(self.account):]
        return Unpickler(StringIO.StringIO(data)).load()


_MemoryStorageDict = {}
class MemoryStorage(AbstractStorage):
    """In memory storage type"""
    
    def __init__(self, account, password, identifier):
        AbstractStorage.__init__(self, account, password, identifier)
        if account + "/" + identifier not in _MemoryStorageDict:
            _MemoryStorageDict[account + "/" + identifier] = {}
        self._dict = _MemoryStorageDict[self.account + "/" + self.storage_id]

    def keys(self):
        return self._dict.keys()

    def __getitem__(self, key):
        return self._unpickle_decrypt(self._dict[key])

    def __setitem__(self, key, value):
        self._dict[key] = self._pickle_encrypt(value)

    def __delitem__(self, key):
        del self._dict[key]

    def __del__(self):
        pass

    def close(self):
        pass


class DbmStorage(AbstractStorage):
    STORAGE_PATH = "~/.pymsn"

    def __init__(self, account, password, identifier):
        import os.path
        AbstractStorage.__init__(self, account, password, identifier)
        
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

    def __getitem__(self, key):
        return self._unpickle_decrypt(self._dict[str(key)]) # some dbm don't support int keys

    def __setitem__(self, key, value):
        self._dict[str(key)] = self._pickle_encrypt(value)
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

