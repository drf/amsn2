cdef public class Box(Container) [object PyEtk_Box, type PyEtk_Box_Type]:
    def append(self, Widget child, int group, int fill_policy, int padding):
        etk_box_append(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, <Etk_Box_Group>group, <Etk_Box_Fill_Policy>fill_policy, padding)

    def child_get_at(self, int group, int pos):
        __ret = Object_from_instance(<Etk_Object*>etk_box_child_get_at(<Etk_Box*>self.obj, <Etk_Box_Group>group, pos))
        return (__ret)

    def child_packing_get(self, Widget child):
        cdef Etk_Box_Fill_Policy fill_policy
        cdef int padding
        __ret = bool(<int> etk_box_child_packing_get(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, &fill_policy, &padding))
        return (__ret, fill_policy, padding)

    def child_packing_set(self, Widget child, int fill_policy, int padding):
        etk_box_child_packing_set(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, <Etk_Box_Fill_Policy>fill_policy, padding)

    def child_position_get(self, Widget child):
        cdef Etk_Box_Group group
        cdef int pos
        __ret = bool(<int> etk_box_child_position_get(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, &group, &pos))
        return (__ret, group, pos)

    def child_position_set(self, Widget child, int group, int pos):
        etk_box_child_position_set(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, <Etk_Box_Group>group, pos)

    def homogeneous_get(self):
        __ret = bool(<int> etk_box_homogeneous_get(<Etk_Box*>self.obj))
        return (__ret)

    def homogeneous_set(self, int homogeneous):
        etk_box_homogeneous_set(<Etk_Box*>self.obj, <Etk_Bool>homogeneous)

    def insert(self, Widget child, int group, Widget after, int fill_policy, int padding):
        etk_box_insert(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, <Etk_Box_Group>group, <Etk_Widget*>after.obj, <Etk_Box_Fill_Policy>fill_policy, padding)

    def insert_at(self, Widget child, int group, int pos, int fill_policy, int padding):
        etk_box_insert_at(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, <Etk_Box_Group>group, pos, <Etk_Box_Fill_Policy>fill_policy, padding)

    def prepend(self, Widget child, int group, int fill_policy, int padding):
        etk_box_prepend(<Etk_Box*>self.obj, <Etk_Widget*>child.obj, <Etk_Box_Group>group, <Etk_Box_Fill_Policy>fill_policy, padding)

    def spacing_get(self):
        __ret = etk_box_spacing_get(<Etk_Box*>self.obj)
        return (__ret)

    def spacing_set(self, int spacing):
        etk_box_spacing_set(<Etk_Box*>self.obj, spacing)

    property homogeneous:
        def __get__(self):
            return self.homogeneous_get()

        def __set__(self, arg):
            self.homogeneous_set(arg)

    property spacing:
        def __get__(self):
            return self.spacing_get()

        def __set__(self, arg):
            self.spacing_set(arg)

    def _set_common_params(self, homogeneous=None, spacing=None, **kargs):
        if homogeneous is not None:
            self.homogeneous_set(homogeneous)
        if spacing is not None:
            self.spacing_set(spacing)

        if kargs:
            Container._set_common_params(self, **kargs)

cdef public class HBox(Box) [object PyEtk_HBox, type PyEtk_HBox_Type]:
    def __init__(self, homogeneous=False, spacing=0, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_hbox_new(homogeneous, spacing))
        self._set_common_params(**kargs)


cdef public class VBox(Box) [object PyEtk_VBox, type PyEtk_VBox_Type]:
    def __init__(self, homogeneous=False, spacing=0, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_vbox_new(homogeneous, spacing))
        self._set_common_params(**kargs)

class BoxEnums:
    NONE = ETK_BOX_NONE
    EXPAND = ETK_BOX_EXPAND
    FILL = ETK_BOX_FILL
    EXPAND_FILL = ETK_BOX_EXPAND_FILL
    SHRINK_OPPOSITE = ETK_BOX_SHRINK_OPPOSITE
    START = ETK_BOX_START
    END = ETK_BOX_END
