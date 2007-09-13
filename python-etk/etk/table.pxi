cdef public class Table(Container) [object PyEtk_Table, type PyEtk_Table_Type]:
    def __init__(self, cols=1, rows=1, homogeneous=0, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_table_new(cols, rows, homogeneous))
        self._set_common_params(**kargs)

    def attach(self, Widget child, int left_attach, int right_attach, int top_attach, int bottom_attach, int fill_policy, int x_padding, int y_padding):
        etk_table_attach(<Etk_Table*>self.obj, <Etk_Widget*>child.obj, left_attach, right_attach, top_attach, bottom_attach, <Etk_Table_Fill_Policy>fill_policy, x_padding, y_padding)

    def attach_default(self, Widget child, int left_attach, int right_attach, int top_attach, int bottom_attach):
        etk_table_attach_default(<Etk_Table*>self.obj, <Etk_Widget*>child.obj, left_attach, right_attach, top_attach, bottom_attach)

    def cell_clear(self, int col, int row):
        etk_table_cell_clear(<Etk_Table*>self.obj, col, row)

    def child_position_get(self, Widget child):
        cdef int left_attach
        cdef int right_attach
        cdef int top_attach
        cdef int bottom_attach
        etk_table_child_position_get(<Etk_Table*>self.obj, <Etk_Widget*>child.obj, &left_attach, &right_attach, &top_attach, &bottom_attach)
        return (left_attach, right_attach, top_attach, bottom_attach)

    def homogeneous_get(self):
        __ret = <int> etk_table_homogeneous_get(<Etk_Table*>self.obj)
        return (__ret)

    def homogeneous_set(self, int homogeneous):
        etk_table_homogeneous_set(<Etk_Table*>self.obj, <Etk_Table_Homogeneous>homogeneous)

    def resize(self, int num_cols, int num_rows):
        etk_table_resize(<Etk_Table*>self.obj, num_cols, num_rows)

    property homogeneous:
        def __get__(self):
            return self.homogeneous_get()

        def __set__(self, arg):
            self.homogeneous_set(arg)

    def _set_common_params(self, homogeneous=None, **kargs):
        if homogeneous is not None:
            self.homogeneous_set(homogeneous)

        if kargs:
            Container._set_common_params(self, **kargs)

class TableEnums:
    NONE = ETK_TABLE_NONE
    HFILL = ETK_TABLE_HFILL
    VFILL = ETK_TABLE_VFILL
    HEXPAND = ETK_TABLE_HEXPAND
    VEXPAND = ETK_TABLE_VEXPAND
    FILL = ETK_TABLE_FILL
    EXPAND = ETK_TABLE_EXPAND
    EXPAND_FILL = ETK_TABLE_EXPAND_FILL
    NOT_HOMOGENEOUS = ETK_TABLE_NOT_HOMOGENEOUS
    HHOMOGENEOUS = ETK_TABLE_HHOMOGENEOUS
    VHOMOGENEOUS = ETK_TABLE_VHOMOGENEOUS
    HOMOGENEOUS = ETK_TABLE_HOMOGENEOUS
