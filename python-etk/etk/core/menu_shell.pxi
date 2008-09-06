import evas.c_evas

cdef public class MenuShell(Widget) [object PyEtk_Menu_Shell, type PyEtk_Menu_Shell_Type]:
    cdef object _set_obj(self, Etk_Object *obj):
        cdef Etk_Menu_Shell *ms
        Widget._set_obj(self, obj)
        ms = <Etk_Menu_Shell*>obj
        return self

    def prepend(self, MenuItem item):
        etk_menu_shell_prepend(<Etk_Menu_Shell*>self.obj, <Etk_Menu_Item*>item.obj)

    def append(self, MenuItem item):
        etk_menu_shell_append(<Etk_Menu_Shell*>self.obj, <Etk_Menu_Item*>item.obj)

    def prepend_relative(self, MenuItem item, MenuItem relative):
        etk_menu_shell_prepend_relative(<Etk_Menu_Shell*>self.obj, <Etk_Menu_Item*>item.obj, <Etk_Menu_Item*>relative.obj)

    def append_relative(self, MenuItem item, MenuItem relative):
        etk_menu_shell_append_relative(<Etk_Menu_Shell*>self.obj, <Etk_Menu_Item*>item.obj, <Etk_Menu_Item*>relative.obj)

    def insert(self, MenuItem item, int position):
        etk_menu_shell_insert(<Etk_Menu_Shell*>self.obj, <Etk_Menu_Item*>item.obj, position)

    def remove(self, MenuItem item):
        etk_menu_shell_remove(<Etk_Menu_Shell*>self.obj, <Etk_Menu_Item*>item.obj)


    def items_get(self):
        cdef Evas_List* __lst
        cdef Object o
        __ret = []

        __lst = etk_menu_shell_items_get(<Etk_Menu_Shell*>self.obj)
        while __lst != NULL:
            o = Object_from_instance(<Etk_Object*>__lst.data)
            __ret.append(o)
            __lst = __lst.next

        evas.c_evas.evas_list_free(__lst)
        return (__ret)


