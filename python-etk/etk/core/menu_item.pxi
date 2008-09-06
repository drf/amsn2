cdef public class MenuItem(Widget) [object PyEtk_Menu_Item, type PyEtk_Menu_Item_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_menu_item_new())
        self._set_common_params(**kargs)

    def label_set(self, char* label):
        etk_menu_item_label_set(<Etk_Menu_Item*>self.obj, label)

    def label_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_menu_item_label_get(<Etk_Menu_Item*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def set_from_stock(self, int stock_id):
        etk_menu_item_set_from_stock(<Etk_Menu_Item*>self.obj, <Etk_Stock_Id>stock_id)
    
    def submenu_set(self, Menu menu):
        etk_menu_item_submenu_set(<Etk_Menu_Item*>self.obj, <Etk_Menu*>menu.obj)

    def submenu_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_menu_item_submenu_get(<Etk_Menu_Item*>self.obj))
        return (__ret)

    def select(self):
        etk_menu_item_select(<Etk_Menu_Item*>self.obj)

    def unselect(self):
        etk_menu_item_unselect(<Etk_Menu_Item*>self.obj)

    def activate(self):
        etk_menu_item_activate(<Etk_Menu_Item*>self.obj)

    property label:
        def __get__(self):
            return self.label_get()

        def __set__(self, label):
            self.label_set(label)

    property submenu:
        def __get__(self):
            return self.submenu_get()

        def __set__(self, submenu):
            self.submenu_set(submenu)

    def _set_common_params(self, label=None, **kargs):
        if label is not None:
            self.label_set(label)

        if kargs:
            Widget._set_common_params(self, **kargs)

    property SELECTED_SIGNAL:
        def __get__(self):
            return ETK_MENU_ITEM_SELECTED_SIGNAL
    
    def on_selected(self, func, *a, **ka):
        self.connect(self.SELECTED_SIGNAL, func, *a, **ka)

    property UNSELECTED_SIGNAL:
        def __get__(self):
            return ETK_MENU_ITEM_UNSELECTED_SIGNAL
    
    def on_unselected(self, func, *a, **ka):
        self.connect(self.UNSELECTED_SIGNAL, func, *a, **ka)

    property ACTIVATED_SIGNAL:
        def __get__(self):
            return ETK_MENU_ITEM_ACTIVATED_SIGNAL
    
    def on_activated(self, func, *a, **ka):
        self.connect(self.ACTIVATED_SIGNAL, func, *a, **ka)



cdef public class MenuItemSeparator(MenuItem) [object PyEtk_Menu_Item_Separator, type PyEtk_Menu_Item_Separator_Type]:
    def __init__(self):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_menu_item_separator_new())



cdef public class MenuItemImage(MenuItem) [object PyEtk_Menu_Item_Image, type PyEtk_Menu_Item_ImageType]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_menu_item_image_new())
        self._set_common_params(**kargs)

    def image_set(self, Image image):
        etk_menu_item_image_set(<Etk_Menu_Item_Image*>self.obj, <Etk_Image*>image.obj)
    
    property image:
        #TODO: image_get?
        def __set__(self, image):
            self.image_set(image)

    def _set_common_params(self, image=None, **kargs):
        if image is not None:
            self.image_set(image)

        if kargs:
            MenuItem._set_common_params(self, **kargs)



cdef public class MenuItemCheck(MenuItem) [object PyEtk_Menu_Item_Check, type PyEtk_Menu_Item_Check_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_menu_item_check_new())
        self._set_common_params(**kargs)
    
    def active_get(self):
        __ret = bool(<int> etk_menu_item_check_active_get(<Etk_Menu_Item_Check*>self.obj))
        return (__ret)

    def active_set(self, int active):
        etk_menu_item_check_active_set(<Etk_Menu_Item_Check*>self.obj, <Etk_Bool>active)

    property active:
        def __get__(self):
            return self.active_get()

        def __set__(self, active):
            self.active_set(active)

    def _set_common_params(self, active=None, **kargs):
        if active is not None:
            self.active_set(active)

        if kargs:
            MenuItem._set_common_params(self, **kargs)

    property TOGGLED_SIGNAL:
        def __get__(self):
            return ETK_MENU_ITEM_CHECK_TOGGLED_SIGNAL

    def on_toggled(self, func, *a, **ka):
        self.connect(self.TOGGLED_SIGNAL, func, *a, **ka)



cdef public class MenuItemRadio(MenuItemCheck) [object PyEtk_Menu_Item_Radio, type PyEtk_Menu_Item_Radio_Type]:
    def __init__(self, MenuItemRadio fromWidget=None, group=None, **kargs):
        if self.obj == NULL:
            if fromWidget is not None:
                self._set_obj(<Etk_Object*>etk_menu_item_radio_new_from_widget(<Etk_Menu_Item_Radio*>fromWidget.obj))
            else:
                self._set_obj(<Etk_Object*>etk_menu_item_radio_new(NULL))
        if group is not None:
            self.group_set(group)

        if kargs:
            MenuItemCheck._set_common_params(self, **kargs)


    def group_set(self, group):
        pass
        #TODO
        #cdef Evas_List* __lst = NULL
        #cdef Object cobj

        #for elemt in group:
        #    cobj = elemt.obj
        #    if cobj:
        #       __lst = evas.c_evas.evas_list_append(__lst, <Etk_Menu_Item_Radio*>cobj)

        #if __lst != NULL:
        #    etk_menu_item_radio_group_set(<Etk_Menu_Item_Radio*>self.obj, &__lst)


    def group_get(self):
        #TODO
        #cdef Evas_List** __lst_ptr
        #cdef Evas_List* __lst
        #cdef Object o
        __ret = []
        #__lst_ptr = etk_menu_item_radio_group_get(<Etk_Menu_Item_Radio*>self.obj)
        #if __lst_ptr != NULL:
            #__lst = <Evas_List*>*__lst_ptr
            #while __lst != NULL:
                #o = Object_from_instance(<Etk_Object*>__lst.data)
                #__ret.append(o)
                #__lst = __lst.next
        return (__ret)


    property group:
        def __get__(self):
            return self.group_get()

        def __set__(self, group):
            self.group_set(group)

    
    
