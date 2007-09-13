#!/usr/bin/env python
# -*- Mode: Python; py-indent-offset: 4 -*-

import pprint

class StructObject(object):
    @classmethod
    def _get_attrs_names(cls):
        name = "__%s_attr_cache" % cls.__name__
        try:
            return getattr(cls, name)
        except AttributeError:
            pass

        if cls is not StructObject:
            attrs = list(cls.__slots__)
        else:
            attrs = []
        for subcls in cls.__mro__:
            if subcls is not cls and issubclass(subcls, StructObject):
                for n in subcls._get_attrs_names():
                    attrs.append(n)

        cache = tuple(attrs)
        setattr(cls, name, cache)
        return cache

    def __init__(self, **ka):
        for n in self._get_attrs_names():
            setattr(self, n, ka[n])

    def __str__(self):
        attrs = []
        for name in self._get_attrs_names():
            attrs.append("%s=%r" % (name, getattr(self, name)))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(attrs))

    __repr__ = __str__


class Enum(StructObject):
    __slots__ = ("module", "name", "c_name", "values")

    def __cmp__(self, other):
        return cmp(self.c_name, other.c_name)


class Flags(Enum): pass


class Object(StructObject):
    __slots__ = ("module", "name", "c_name", "type_id", "parent", "methods",
                 "constructors")

    def __str__(self):
        return ("%s(module=%r, name=%r, c_name=%r, type_id=%r, parent=%r,\n"
                "constructors=\n%s,\n\t"
                "methods=\n%s)") % \
                (self.__class__.__name__, self.module, self.name, self.c_name,
                 self.type_id, self.parent,
                 pprint.pformat(self.constructors, 16),
                 pprint.pformat(self.methods, 16))

    __repr__ = __str__

class Struct(StructObject):
    __slots__ = ("name", "c_name", "members")

    def __cmp__(self, other):
        return cmp(self.c_name, other.c_name)


class Function(StructObject):
    __slots__ = ("name", "c_name", "args", "ret", "is_varargs")

    def __cmp__(self, other):
        return cmp(self.c_name, other.c_name)


class Method(Function):
    __slots__ = ("object",)

    def __str__(self):
        return ("%s(object=%r, name=%r, c_name=%r, ret=%r, args=%s, "
                "is_varargs=%s)") % \
                (self.__class__.__name__, self.object.c_name, self.name,
                 self.c_name, self.ret, self.args, self.is_varargs)

    __repr__ = __str__


class Constructor(Function):
    __slots__ = ("constructor_of",)

    def __str__(self):
        return ("%s(constructor_of=%r, name=%r, c_name=%r, ret=%r, args=%s, "
                "is_varargs=%s)") % \
                (self.__class__.__name__, self.constructor_of.c_name,
                 self.name, self.c_name, self.ret, self.args, self.is_varargs)

    __repr__ = __str__

