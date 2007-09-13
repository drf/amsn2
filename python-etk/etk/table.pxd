cdef extern from "etk_table.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Table_Fill_Policy:
        ETK_TABLE_NONE
        ETK_TABLE_HFILL
        ETK_TABLE_VFILL
        ETK_TABLE_HEXPAND
        ETK_TABLE_VEXPAND
        ETK_TABLE_FILL
        ETK_TABLE_EXPAND
        ETK_TABLE_EXPAND_FILL

    ctypedef enum Etk_Table_Homogeneous:
        ETK_TABLE_NOT_HOMOGENEOUS
        ETK_TABLE_HHOMOGENEOUS
        ETK_TABLE_VHOMOGENEOUS
        ETK_TABLE_HOMOGENEOUS

    ####################################################################
    # Structures
    ctypedef struct Etk_Table
    ctypedef struct Etk_Table_Cell
    ctypedef struct Etk_Table_Col_Row

    ####################################################################
    # Functions
    Etk_Type* etk_table_type_get()
    Etk_Widget* etk_table_new(int num_cols, int num_rows, int homogeneous)
    void etk_table_attach(Etk_Table* __self, Etk_Widget* child, int left_attach, int right_attach, int top_attach, int bottom_attach, int fill_policy, int x_padding, int y_padding)
    void etk_table_attach_default(Etk_Table* __self, Etk_Widget* child, int left_attach, int right_attach, int top_attach, int bottom_attach)
    void etk_table_cell_clear(Etk_Table* __self, int col, int row)
    void etk_table_child_position_get(Etk_Table* __self, Etk_Widget* child, int* left_attach, int* right_attach, int* top_attach, int* bottom_attach)
    int etk_table_homogeneous_get(Etk_Table* __self)
    void etk_table_homogeneous_set(Etk_Table* __self, int homogeneous)
    void etk_table_resize(Etk_Table* __self, int num_cols, int num_rows)

#########################################################################
# Objects
cdef public class Table(Container) [object PyEtk_Table, type PyEtk_Table_Type]:
    pass

