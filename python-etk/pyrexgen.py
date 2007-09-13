import sys
import os.path
from structobj import *

class Generator(object):
    def __init__(self, out_pxd, out_pyx, out_override, header, enums, functions, objects,
                 structs, overrides, module='', extern_enums=(), extern_objects=()):
        self.out_pxd = out_pxd
        self.out_pyx = out_pyx
        self.out_override = out_override
        self.header = header
        self.functions = functions
        self.objects = objects
        self.structs = structs
        self.overrides = overrides
        self.enums = enums
        self.extern_enums = extern_enums
        self.extern_objects = extern_objects
        self.module = module
        self.properties = {}

    def generate(self):
        self.out_pxd.write("cdef extern from \"%s\":\n" % \
                os.path.basename(self.header))
        self._normalize_names()
        self._build_properties()

        self._gen_enumerations()
        self._gen_structures()
        self._gen_functions()
        self._gen_objects()
        self._gen_properties()

    def _gen_properties(self):
        for o in self.objects:
            if self.properties[o.name]:
                self._gen_object_properties(o)

    def _gen_object_properties(self, obj):
        settable = []
        msettable = []
        for p in self.properties[obj.name]:
            name, has_set, multi_set = p
            self.out_pyx.writelines(
                "    property " + p[0] + ":\n"
                "        def __get__(self):\n"
                "            return self." + p[0] + "_get()\n\n")
            if has_set:
                self.out_pyx.writelines(
                    "        def __set__(self, arg):\n")
                if multi_set:
                    msettable.append(name)
                    self.out_pyx.writelines(
                        "            self." + p[0] + "_set(*arg)\n\n")
                else:
                    settable.append(name)
                    self.out_pyx.writelines(
                        "            self." + p[0] + "_set(arg)\n\n")

        if not settable:
            return

        self.out_pyx.writelines(
            "    def _set_common_params(self, " + \
            ', '.join([s + "=None" for s in settable + msettable]) + "):\n")

        for p in settable:
            self.out_pyx.writelines(
                "        if " + p + " is not None:\n"
                "            self." + p + "_set(" + p + ")\n")

        for p in msettable:
            self.out_pyx.writelines(
                "        if " + p + " is not None:\n"
                "            self." + p + "_set(*" + p + ")\n")

    def _build_properties(self):
        for o in self.objects:
            self._build_object_properties(o)

    def _build_object_properties(self, obj):
        "Identify in method list possible properties"

        self.properties[obj.name] = []

        getters = []
        setters = []
        msetters = []
        for m in obj.methods:
            name = m.name
            if name.endswith('_get'):
                # only accept getters with no arguments, except
                # return ("output") arguments
                args = filter(lambda a: not self._is_type_return(a[0]), m.args)
                if not args:
                    getters.append(name[:-4])

            if name.endswith('_set') and m.args:
                if len(m.args) == 1:
                    setters.append(name[:-4])
                else:
                    msetters.append(name[:-4])

        for p in getters:
            if p in setters:
                self.properties[obj.name].append((p, True, False))
            elif p in msetters:
                self.properties[obj.name].append((p, True, True))
            else:
                self.properties[obj.name].append((p, False, False))

    def _normalize_names(self):
        "Normalize method names to avoid using Python keywords as function names"

        # For now, just dealing with problems we have in Etk
        for o in self.objects:
            for m in o.methods:
                if m.name in ['raise']:
                    m.name = m.name + "_"


    def _output_pxd_section_header(self, section_name):
        self.out_pxd.writelines(
            ("#" + ("#" * 72) + "\n",
             "# %s\n" % section_name))

    def _output_pxd_subsection_header(self, section_name):
        self.out_pxd.writelines(
            ("    #" + ("#" * 67) + "\n",
             "    # %s\n" % section_name))

    ####################################################################
    # Enumerations
    def _output_pxd_enumerate(self, enum):
        self.out_pxd.write("    ctypedef enum %s:\n" % enum.c_name)
        for v in enum.values:
            self.out_pxd.write("        %s\n" % v[1])
        self.out_pxd.write("\n")

    def _output_enumerate(self, enum):
        self._output_pxd_enumerate(enum)

    def _gen_enumerations(self):
        self._output_pxd_subsection_header("Enumerations")
        for e in self.enums:
            self._output_enumerate(e)

    ####################################################################
    # Functions
    def _get_pyrex_pxd_args(self, args):
        lst = []
        for atype, aname in args:
            atype = self._get_canonical_type_pxd_name(atype)
            lst.append("%s %s" % (atype, aname))
        return ", ".join(lst)

    def _get_pyrex_args(self, args):
        lst = []
        for atype, aname in args:
            atype = self._get_canonical_type_name(atype)
            if not self._is_type_return(atype):
                lst.append("%s %s" % (atype, aname))
        return ", ".join(lst)

    def _get_pyrex_use_args(self, args):
        lst = []
        for atype, aname in args:
            if self._is_type_enum(atype):
                lst.append("<%s>%s" % (atype, aname))
            else:
                obj = self._object_from_type(atype)
                if obj:
                    lst.append("<%s>%s.obj" %
                            (self._canonical_object_pxd_name(obj) + "*", aname))
                elif self._is_type_return(atype):
                    lst.append("&" + aname)
                else:
                    lst.append(aname)
        return ", ".join(lst)

    def _get_canonical_type_pxd_name(self, atype):
        atype = atype.replace('const-', '')
        if self._is_type_enum(atype):
            atype = "int"
        else:
            obj = self._object_from_type(atype)
            if obj:
                atype = self._canonical_object_pxd_name(obj) + "*"
        return atype

    def _get_canonical_type_name(self, atype):
        atype = atype.replace('const-', '')
        if self._is_type_enum(atype):
            atype = "int"
        else:
            obj = self._object_from_type(atype)
            if obj:
                atype = self._canonical_object_name(obj)
        return atype

    def _output_pxd_function(self, func, obj=None):
        ret = self._get_canonical_type_pxd_name(func.ret)
        args = self._get_pyrex_pxd_args(func.args)
        if obj:
            itself = self._canonical_object_pxd_name(obj) + "* __self"
            if args:
                args = itself + ", " + args
            else:
                args = itself
        self.out_pxd.write("    %s %s(%s)\n" % (ret, func.c_name, args))

    def _output_function(self, func, obj=None):
        self._output_pxd_function(func, obj)

    def _gen_functions(self):
        self._output_pxd_subsection_header("Functions")
        for f in self.functions:
            self._output_function(f)
        for o in self.objects:
            for f in o.constructors:
                self._output_function(f)
            for f in o.methods:
                self._output_function(f, o)
        self.out_pxd.write("\n")

    ####################################################################
    # Structures
    def _output_structure(self, obj):
        self.out_pxd.write("    ctypedef struct %s\n" % obj.c_name)

    def _gen_structures(self):
        self._output_pxd_subsection_header("Structures")
        for o in self.objects:
            self._output_structure(o)
        for s in self.structs:
            self._output_structure(s)
        self.out_pxd.write("\n")

    ####################################################################
    # Objects
    def _get_object_decl(self, obj):
        if not obj.parent:
            parent = ""
        else:
            parent = obj.parent.split("_", 1)[1] # XXX fix-me
            parent = "(%s)" % parent
        return ("cdef public class %(name)s%(parent)s "
                "[object Py%(c_name)s, type Py%(c_name)s_Type]:\n") % \
                {"name": obj.name, "c_name": obj.c_name,
                 "parent": parent}

    def _output_pxd_object(self, obj, decl):
        self.out_pxd.write(decl)
        self.out_pxd.write("    pass\n")

    def _output_pyx_method_obj(self, meth):
        return "<%s*>self.obj" % meth.object.c_name

    def _output_pyx_method_c_call_pre(self, meth):
        return "%s(%s" % \
               (meth.c_name, self._output_pyx_method_obj(meth))

    def _object_from_type(self, type_name):
        if type_name[-1] != "*":
            return None
        type_name = type_name[:-1]
        for o in self.objects:
            if type_name == o.c_name:
                return o
        for o in self.extern_objects:
            if type_name == o.c_name:
                return o

    def _is_type_object(self, type_name):
        return bool(self._object_from_type(type_name))

    def _is_type_enum(self, type_name):
        for e in self.enums:
            if type_name == e.c_name:
                return True
        for e in self.extern_enums:
            if type_name == e.c_name:
                return True
        return False

    def _canonical_prefix(self, module):
        if self.module == module:
            return ''
        else:
            # XXX: ugly but works for now
            p = module.lower()
            return "%s.c_%s." % (p, p)

    def _canonical_object_name(self, o):
        return self._canonical_prefix(o.module) + o.name

    def _canonical_object_pxd_name(self, o):
        return self._canonical_prefix(o.module) + o.c_name

    simple_types = ("float", "double", "int", "long", "const-char*")
    def _is_type_simple(self, type_name):
        return type_name in self.simple_types

    def _is_type_return(self, type_name):
        return type_name[-1] == "*" and \
            (self._is_type_simple(type_name[:-1]) or \
             self._is_type_enum(type_name[:-1]))

    def _is_simple_args(self, args):
        for atype, aname in args:
            if not self._is_type_simple(atype) and \
               not self._is_type_enum(atype):
                return False
        return True

    def _is_return_args(self, args):
        ret = False
        for atype, aname in args:
            if self._is_type_return(atype):
                ret = True
            elif not self._is_type_simple(atype) and \
                 not self._is_type_enum(atype):
                return False
        return ret

    def _is_complex_args(self, args):
        ret = False
        for atype, aname in args:
            if self._is_type_object(atype):
                ret = True
            elif self._is_type_return(atype):
                pass
            elif not self._is_type_simple(atype) and \
                 not self._is_type_enum(atype):
                return False
        return ret

    def _is_supported_args(self, args):
        ret = True
        for atype, aname in args:
                if self._is_type_object(atype):
                    ret = True
                elif self._is_type_return(atype):
                    pass
                elif not self._is_type_simple(atype) and \
                     not self._is_type_enum(atype):
                    return False
        return ret

    def _output_pyx_method_body__preamble(self, meth):
        ret = []
        for atype, aname in meth.args:
            if self._is_type_return(atype):
                if atype.startswith("const-"):
                    atype = atype[6:]
                self.out_pyx.write("        cdef %s %s\n" %
                                   (atype[:-1], aname))
                ret.append(aname)
            elif self._is_type_object(atype):
                pass
                #self.out_pyx.write("        # XXX: inc %s ref_count?\n" %
                #                   aname)
        return ret

    def _output_pyx_method_body__return(self, meth, ret):
        if ret:
            self.out_pyx.write("        return (%s)\n" % ", ".join(ret))

    def _output_pyx_method_body__call_args(self, meth, prefix='', suffix=''):
        if meth.args:
            self.out_pyx.writelines(
                ("        ", prefix, self._output_pyx_method_c_call_pre(meth),
                ", ", self._get_pyrex_use_args(meth.args), ')', suffix, "\n"))
        else:
            self.out_pyx.writelines(
                ("        ", prefix, self._output_pyx_method_c_call_pre(meth),
                ')', suffix, "\n"))

    def _output_pyx_method_body__call(self, meth, ret):
        if meth.ret == 'void':
            self._output_pyx_method_body__call_args(meth)

        elif meth.ret == 'const-char*':
            self.out_pyx.writelines(
                ("        cdef char *__char_ret\n"
                 "        __ret = None\n"))
            self._output_pyx_method_body__call_args(meth, '__char_ret = ')
            self.out_pyx.writelines(
                ("        if __char_ret != NULL:\n"
                 "            __ret = __char_ret\n"))

        elif meth.ret.endswith('Evas_List*'):
            self.out_pyx.writelines(
                "        cdef Evas_List* __lst\n"
                "        __ret = []\n\n")
            self._output_pyx_method_body__call_args(meth, '__lst = ')
            self.out_pyx.writelines(
                "        while __lst != NULL:\n"
                "            # FIXME: fix this <int> to what you need\n"
                "            __ret.append(<int> __lst.data)\n"
                "            __lst = __lst.next\n\n"
                "        # FIXME: you need to free the Evas_List __lst here\n")

        elif self._is_type_enum(meth.ret):
            if (meth.ret == 'Etk_Bool'):
                self._output_pyx_method_body__call_args(meth, \
                        '__ret = bool(<int> ', ')')
            else:
                self._output_pyx_method_body__call_args(meth, '__ret = <int> ')

        elif self._is_type_simple(meth.ret):
            self._output_pyx_method_body__call_args(meth, '__ret = ')

        elif self._is_type_object(meth.ret):
            # If we are using an object from other module,
            # Object_from_instance has a different way to use
            module = self._object_from_type(meth.ret).module
            mod_prefix = self._canonical_prefix(module)
            if mod_prefix:
                call_prefix = \
                        '__ret = ' + mod_prefix + '_Object_from_instance(<long>'
            else:
                call_prefix = '__ret = Object_from_instance(<' \
                        + module + '_Object*>'
            self._output_pyx_method_body__call_args(meth, call_prefix , ')')

        else:
            sys.stderr.write("Unsupported method return %s.%s: %s\n" %
                             (meth.object.name, meth.name, meth.ret))
            self.out_pyx.write("        # FIXME: unsupported method return\n"
                               "        pass\n")
            return []

        if meth.ret != 'void':
            ret.insert(0, '__ret')

        return ret

    def _output_pyx_method_body(self, meth):
        if meth.args and not self._is_supported_args(meth.args):
            sys.stderr.write("Unsupported method arguments %s.%s: %s\n" %
                    (meth.object.name, meth.name, meth.args))
            self.out_pyx.write("        # FIXME: unsupported method arguments\n"
                               "        pass\n")
            return

        ret = self._output_pyx_method_body__preamble(meth)
        ret = self._output_pyx_method_body__call(meth, ret)

        if ret:
            self._output_pyx_method_body__return(meth, ret)

    def _output_pyx_method(self, meth):
        args = self._get_pyrex_args(meth.args)
        if args:
            args = ", " + args

        if meth.c_name in self.overrides:
            self.out_override.write("    #def %s(self%s):\n" % (meth.name, args))
            self.out_override.write("       #pass\n\n")
        else:
            self.out_pyx.write("    def %s(self%s):\n" % (meth.name, args))
            self._output_pyx_method_body(meth)
            self.out_pyx.write("\n")

    def _output_pyx_object(self, obj, decl):
        self.out_pyx.write(decl)
        self.out_pyx.writelines(
            ("    def _new_obj(self):\n",
             "        if self.obj == NULL:\n",
             "            # FIXME: adjust the constructor here...\n",
             "            self._set_obj(<Etk_Object*>" + obj.constructors[0].c_name + "())\n",
             "\n",
             ))
        for m in obj.methods:
            self._output_pyx_method(m)

    def _output_object(self, obj):
        decl = self._get_object_decl(obj)
        self._output_pxd_object(obj, decl)
        self._output_pyx_object(obj, decl)

    def _gen_objects(self):
        self._output_pxd_section_header("Objects")
        for o in self.objects:
            self._output_object(o)
        self.out_pxd.write("\n")


def main(args):
    import hparser
    from pprint import pprint

    f = args[1]
    buf = open(f).read()

    h = hparser.HeaderParser(buf)

    extern_enums = (
        Enum(module="Etk", name="Stock_Size", c_name="Etk_Stock_Size",
             values=None),
        Enum(module="Etk", name="Stock_Id", c_name="Etk_Stock_Id",
             values=None),
        Enum(module="Etk", name="Bool", c_name="Etk_Bool",
             values=None),
        )
    extern_objects = (
        Object(module="Etk", name="Image", c_name="Etk_Image",
               type_id="ETK_IMAGE_TYPE", parent=None, methods=None,
               constructors=None),
        Object(module="Etk", name="Widget", c_name="Etk_Widget",
               type_id="ETK_WIDGET_TYPE", parent=None, methods=None,
               constructors=None),
        Object(module="Evas", name="Object", c_name="Evas_Object",
               type_id='', parent=None, methods=None, constructors=None),
        Object(module="Evas", name="Evas", c_name="Evas",
               type_id='', parent=None, methods=None, constructors=None),
        Object(module="Evas", name="List", c_name="Evas_List",
               type_id='', parent=None, methods=None, constructors=None),
        )

    functions = h.functions.values()
    enums = h.enums.values()
    objects = h.objects.values()
    structs = h.structs.values()

    functions.sort()
    enums.sort()
    objects.sort()
    structs.sort()
    for o in objects:
        o.constructors.sort()
        o.methods.sort()

    out_pyx = open("out.pyx", "wb")
    out_pxd = open("out.pxd", "wb")
    out_override = open("out_over.pxi", "wb")
    gen = Generator(out_pxd=out_pxd, out_pyx=out_pyx,
                    out_override=out_override,
                    header=args[1],
                    enums=enums,
                    functions=functions,
                    objects=objects,
                    structs=structs,
                    overrides=args[2:],
                    module='Etk',
                    extern_enums=extern_enums,
                    extern_objects=extern_objects)
    gen.generate()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
