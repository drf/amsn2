
cdef extern from "etk_paned.h":
    ####################################################################
    # Structures
    ctypedef struct Etk_Paned
    ctypedef struct Etk_HPaned
    ctypedef struct Etk_VPaned

    ####################################################################
    # Functions
    Etk_Widget * etk_hpaned_new()
    Etk_Widget * etk_vpaned_new()
    void etk_paned_child1_set(Etk_Paned *__self, Etk_Widget *child, int expand)
    void etk_paned_child2_set (Etk_Paned *__self, Etk_Widget *child, int expand)
    Etk_Widget * etk_paned_child1_get (Etk_Paned *__self)
    Etk_Widget * etk_paned_child2_get (Etk_Paned *__self)
    void etk_paned_child1_expand_set (Etk_Paned *__self, int expand)
    void etk_paned_child2_expand_set (Etk_Paned *__self, int expand)
    int etk_paned_child1_expand_get (Etk_Paned *__self)
    int etk_paned_child2_expand_get (Etk_Paned *__self)
    void etk_paned_position_set (Etk_Paned *__self, int position)
    int etk_paned_position_get (Etk_Paned *__self)



#########################################################################
# Objects
cdef public class Paned(Container) [object PyEtk_Paned, type PyEtk_Paned_Type]:
    pass
cdef public class HPaned(Paned) [object PyEtk_HPaned, type PyEtk_HPaned_Type]:
    pass
cdef public class VPaned(Paned) [object PyEtk_VPaned, type PyEtk_VPaned_Type]:
    pass

