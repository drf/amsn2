cdef extern from "etk_box.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Box_Fill_Policy:
        ETK_BOX_NONE
        ETK_BOX_EXPAND
        ETK_BOX_FILL
        ETK_BOX_EXPAND_FILL
        ETK_BOX_SHRINK_OPPOSITE

    ctypedef enum Etk_Box_Group:
        ETK_BOX_START
        ETK_BOX_END

    ####################################################################
    # Structures
    ctypedef struct Etk_Box
    ctypedef struct Etk_HBox
    ctypedef struct Etk_VBox
    ctypedef struct Etk_Box_Cell

    ####################################################################
    # Functions
    Etk_Type* etk_box_type_get()
    Etk_Type* etk_hbox_type_get()
    Etk_Type* etk_vbox_type_get()
    void etk_box_append(Etk_Box* __self, Etk_Widget* child, int group, int fill_policy, int padding)
    Etk_Widget* etk_box_child_get_at(Etk_Box* __self, int group, int pos)
    int etk_box_child_packing_get(Etk_Box* __self, Etk_Widget* child, Etk_Box_Fill_Policy* fill_policy, int* padding)
    void etk_box_child_packing_set(Etk_Box* __self, Etk_Widget* child, int fill_policy, int padding)
    int etk_box_child_position_get(Etk_Box* __self, Etk_Widget* child, Etk_Box_Group* group, int* pos)
    void etk_box_child_position_set(Etk_Box* __self, Etk_Widget* child, int group, int pos)
    int etk_box_homogeneous_get(Etk_Box* __self)
    void etk_box_homogeneous_set(Etk_Box* __self, int homogeneous)
    void etk_box_insert(Etk_Box* __self, Etk_Widget* child, int group, Etk_Widget* after, int fill_policy, int padding)
    void etk_box_insert_at(Etk_Box* __self, Etk_Widget* child, int group, int pos, int fill_policy, int padding)
    void etk_box_prepend(Etk_Box* __self, Etk_Widget* child, int group, int fill_policy, int padding)
    int etk_box_spacing_get(Etk_Box* __self)
    void etk_box_spacing_set(Etk_Box* __self, int spacing)
    Etk_Widget* etk_hbox_new(int homogeneous, int spacing)
    Etk_Widget* etk_vbox_new(int homogeneous, int spacing)

#########################################################################
# Objects
cdef public class Box(Container) [object PyEtk_Box, type PyEtk_Box_Type]:
    pass
cdef public class HBox(Box) [object PyEtk_HBox, type PyEtk_HBox_Type]:
    pass
cdef public class VBox(Box) [object PyEtk_VBox, type PyEtk_VBox_Type]:
    pass

