cdef public class MenuBar(MenuShell) [object PyEtk_Menu_Bar, type PyEtk_Menu_Bar_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_menu_bar_new())
        self._set_common_params(**kargs)
