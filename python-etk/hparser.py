#!/usr/bin/env python
# -*- Mode: Python; py-indent-offset: 4 -*-

import re
from structobj import *

import string
trans_enum_name = string.maketrans(string.uppercase + "_",
                                   string.lowercase + "-")
del string

class HeaderParser:
    """Parse a C header (in a buffer) and provides StructObjects that represent
    Etk objects (w/ methods and constructors), enumerations and standalone
    functions."""

    def __init__(self, buf, prefix=None):
        self.orig_buf = buf
        self.buf = strip_comments(buf)
        self.prefix = prefix

        self.objects = {}
        self.enums = {}
        self.functions = {}
        self.structs = {}

        self._objects = []
        self._enums = []
        self._functions = []
        self._structs = []

        self.parse()
        self.build_enumerations()
        self.build_structs()
        self.build_object_tree()
        self.fill_object_tree()  # with methods and constructors

    def parse(self):
        self.parse_objects()

        self._functions = proto_pat.findall(clean_func(self.buf))

        # Parse enumerations
        pos = 0
        while pos < len(self.buf):
            m = enum_pat.search(self.buf, pos)
            if not m:
                break
            name = m.group("name")
            vals = m.group("values")
            isflags = False
            entries = []

            # Enumerations for bitmaps are flags, we identify this by
            # looking for patterns 'like' "1 << 3" in the values
            for e_name, e_value in enum_entries_pat.findall(vals):
                if "<<" in e_value:
                    isflags = True
                entries.append(e_name)
            pos = m.end()

            if entries:
                self._enums.append((name, isflags, entries))

    def parse_objects(self):
        candidates = []
        candidates.extend(obj_struct_pat.findall(self.buf))
        candidates.extend(obj_typedef_struct_pat.findall(self.buf))

        # Use the orig_buf, since we depend on stripped information
        realobjs = realobj_pat.findall(self.orig_buf)

        for o in candidates:
            if typecode(o[0]) in realobjs:
                self._objects.append(o)

        all_structs = struct_pat.findall(self.buf)
        for s in all_structs:
            if not typecode(s) in realobjs:
                self._structs.append(s)


    def build_enumerations(self):
        for e in self._enums:
            name = e[0]
            self.enums[name] = self._make_enum(e)

    def build_structs(self):
        for s in self._structs:
            self.structs[s] = self._make_struct(s)

    def build_object_tree(self):
        for o in self._objects:
            (name, p) = o
            self.objects[name] = self._make_obj(o)

    def fill_object_tree(self):
        for f in self._functions:
            ret, pointer, name, orig_args = f

            if name[0] == '_':
                continue

            args = arg_split_pat.findall(orig_args)
            args = self._adjust_func_args(args)
            is_varargs = orig_args.endswith('...')

            # If has more than one argument and it's type is equal
            # (ignoring case) to the function prefix, it's a method.
            if len(args) >= 1:
                # methods must have at least one argument
                obj = args[0][0][:-1]
                if name[:len(obj)].lower() == obj.lower():
                    self._make_method(obj, name, ret, args, is_varargs)
                    continue

            # Assuming that constructor function name ends with '_new'
            # and returns a pointer
            m = func_new_pat.match(name)
            if m:
                constructor_of = None
                func_name = m.group("name")
                if func_name and pointer_pat.match(ret):
                    components = func_name.split('_')
                    constructor_of = (s.capitalize() for s in components)
                    constructor_of = '_'.join(constructor_of)
                    self._make_constructor(constructor_of, name, ret,
                                           args, is_varargs)
                    continue

            # Otherwise we have a simple function
            self._make_function(name, ret, args, is_varargs)

    def _name_without_prefix(self, s):
        if self.prefix:
            l = len(self.prefix)
            if s[:l] == self.prefix and s[l] == '_':
                return s[l+1:]

        return s

    def _make_function(self, name, ret, args, is_varargs):
        t = Function(name=self._name_without_prefix(name), ret=ret,
                     c_name=name, args=args, is_varargs=is_varargs)
        self.functions[t.c_name] = t

    def _make_constructor(self, constructor_of, name, ret, args, is_varargs):
        t = Constructor(name=self._name_without_prefix(name),
                        c_name=name, args=args, is_varargs=is_varargs,
                        constructor_of=constructor_of, ret=ret)

        # Add constructor into the right object
        try:
            obj = self.objects[constructor_of]
            t.constructor_of = obj
            obj.constructors.append(t)
        except KeyError, e:
            pass

    def _make_method(self, obj, name, ret, args, is_varargs):
        mname = name[len(obj)+1:]
        t = Method(object=obj, name=mname, c_name=name,
                   args=args[1:], ret=ret, is_varargs=is_varargs)

        # Add method into the right object
        try:
            obj = self.objects[obj]
            t.object = obj
            obj.methods.append(t)
        except KeyError, e:
            pass

    def _adjust_func_args(self, args):
        if len(args) == 1 and args[0] == "void":
            args = []
        return args

    def _make_enum(self, e):
        (cname, is_flag, entries) = e

        m = split_prefix_pat.match(cname)
        if not m:
            return

        module = m.group('prefix')
        name = m.group('rest')

        # Look for a common prefix in the enumerations
        prefix = entries[0]
        for ent in entries:
            # shorten prefix til we get a match ...
            while ent[:len(prefix)] != prefix or len(prefix) >= len(ent):
                prefix = prefix[:-1]
        prefix_len = len(prefix)
        values = []

        for ent in entries:
            values.append((ent[prefix_len:].translate(trans_enum_name), ent))

        params = {"name": name,
                  "c_name": cname,
                  "module": module,
                  "values": values}

        if is_flag:
            t = Flags(**params)
        else:
            t = Enum(**params)

        return t

    def _make_struct(self, name):
        m = split_prefix_pat.match(name)
        if not m:
            return None

        cmodule = m.group("prefix")
        cname = name
        name = m.group("rest").replace('_', '', 1)

        t = Struct(name=name, c_name=cname, members=[])
        return t

    def _make_obj(self, o):
        name, parent = o

        cmodule = None

        m = split_prefix_pat.match(name)
        if not m:
            return None

        cmodule = m.group("prefix")
        cname = name
        name = m.group("rest").replace('_', '', 1)

        if parent[-1] == '*':
            parent = None

        t = Object(module = cmodule, name = name, c_name = cname,
                   type_id = typecode(cname), parent = parent,
                   methods = [], constructors = [])

        return t

# Regexes
obj_name_pat = "[A-Z][a-z]*_(?:[A-Z][A-Za-z0-9_]*)+"
ign_comment_pat = r"(?:(?:\s*/[*].*[*]/\s*)*)"

struct_pat = re.compile(r"\s*(?:typedef\s+)?struct\s+([A-Za-z_]+)\s*{", re.MULTILINE)

realobj_pat = re.compile(r"#define\s+([A-Za-z0-9_]*_TYPE)", re.MULTILINE)

obj_struct_pat = re.compile(
    (r"\s*struct\s+(?P<name>" + obj_name_pat + r")\s*{\s*" +
     ign_comment_pat +
     r"\s*(?P<parent>" + obj_name_pat + r"(?:\s*\*)?)\s*"),
    re.MULTILINE)

obj_typedef_struct_pat = re.compile(
    (r"\s*typedef\s+struct\s+[_\w]*\s*{\s*" +
     ign_comment_pat +
     r"\s*(?P<parent>" + obj_name_pat + r"(?:\s*\*)?)\s*[^}]*}" +
     r"\s*(?P<name>" + obj_name_pat + r")\s*;"),
    re.MULTILINE)

split_prefix_pat = re.compile(r"""
        (?P<prefix> [A-Z]+ [a-z]* ) _  # !! underscore separate prefix from rest
        (?P<rest> [_A-Za-z0-9]+ )
        """, re.VERBOSE)

enum_pat = re.compile(
    (r"\s*typedef\s+enum\s*{(?P<values>[^}]*)}" +
     r"\s*(?P<name>[A-Z][A-Za-z_0-9]*)\s*;"),
    re.MULTILINE)

enum_entries_pat = re.compile(
    (r"\s*(?P<name>[A-Za-z][_A-Za-z0-9]*)" +
     r"\s*(?:=\s*(?P<value>[^,]*)\s*)?(?:,|)" +
     ign_comment_pat),
    re.MULTILINE)

comment_pat = re.compile(r"/\*([^*]|(\*[^/]))*\*/|#.*$", re.MULTILINE)

proto_pat = re.compile(r"""
(?P<ret>(-|\w|\&|\*)+\s*)  # return type
\s+                        # skip whitespace
(?P<func>\w+)\s*[(]        # match the function name until the opening (
\s*(?P<args>.*?)\s*[)]     # group the function arguments
""", re.IGNORECASE|re.VERBOSE)

id_pat = r"[A-Za-z_][A-Za-z_0-9*]*"
arg_split_pat = re.compile("((?:const-)?" + id_pat + r")\s+(" + id_pat + r")\s*(?:,|)")
get_type_pat = re.compile(r'(const-)?(?P<type>' + id_pat + ')\*?\s+')

pointer_pat = re.compile('.*\*$')
func_new_pat = re.compile('(?P<name>\w+)_new$')

typedef_pat = r"""
    (typedef|struct|enum)[^\{]*?
    \{[^\{]+?\}
    (\s|.|\n)*?;\s*
"""

# Patterns to strip almost all non-function lines
clean_func_pat_list = [re.compile(p, re.MULTILINE|re.VERBOSE) for p in [
        r"\\\n",      # continued lines
        r"^[#].*?$",  # pre-processor directives

        # typedefs, structs and enums,
        # FIXME: two passes to deal with one-level nesting
        typedef_pat, typedef_pat,
        r"^(typedef|struct|enum)(\s|.|\n)*?;\s*", # forward decls

        r"^\s*(extern)\s+\"C\"\s+{",  # extern "C"
        ]]

# Utility functions
def clean_func(buf):
    """Strips almost all non-function lines from a source buffer to make
    parsing of functions easier."""

    for p in clean_func_pat_list:
        buf = p.sub('', buf)

    # multiple whitespace
    pat = re.compile(r"\s+", re.MULTILINE)
    buf = pat.sub(' ', buf)

    # clean up line ends
    pat = re.compile(r";\s*", re.MULTILINE)
    buf = pat.sub('\n', buf)
    buf = buf.lstrip()

    # associate *, &, and [] with type instead of variable
    pat = re.compile(r' \s* ([*|&]+) \s* (\w+)', re.VERBOSE)
    buf = pat.sub(r'\1 \2', buf)
    pat = re.compile(r'\s+ (\w+) \[ \s* \]', re.VERBOSE)
    buf = pat.sub(r'[] \1', buf)

    # make return types that are const work.
    buf = buf.replace('const ', 'const-')

    return buf

def typecode(typename):
    return typename.upper() + "_TYPE"

def strip_comments(buf):
    return comment_pat.sub('', buf)

###

def main(args):
    from pprint import pprint

    for filename in args[1:]:
        buf = open(filename).read()
        h = HeaderParser(buf)

        print "----\nObjects:\n"
        pprint(h.objects.values())

        print "\n\nEnumerations:\n"
        pprint(h.enums.values())

        print "\n\nFunctions:\n"
        pprint(h.functions.values())

        print "\n\nStructs:\n"
        pprint(h.structs.values())

        print "\n--------\n"


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
