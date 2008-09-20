cdef public class TextblockIter [object PyEtk_Textblock_Iter, type PyEtk_Textblock_Iter_Type]:
    def __init__(self, Textblock tb, **kargs):
        self.obj = <Etk_Textblock_Iter*>etk_textblock_iter_new(<Etk_Textblock*>tb.obj)

    def __dealloc__(self):
        etk_textblock_iter_free(<Etk_Textblock_Iter *>self.obj)

    def backward_start(self):
        etk_textblock_iter_backward_start(<Etk_Textblock_Iter *>self.obj)

    def forward_end(self):
        etk_textblock_iter_forward_end(<Etk_Textblock_Iter *>self.obj)



cdef public class Textblock(Object) [object PyEtk_Textblock, type PyEtk_Textblock_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_textblock_new())
        self._set_common_params(**kargs)

    def text_set(self, char* text, int markup):
        etk_textblock_text_set(<Etk_Textblock*>self.obj, text, <Etk_Bool> markup)

    def insert(self, TextblockIter iter, text):
        length = python.strlen(text)
        etk_textblock_insert (<Etk_Textblock*> self.obj,
                          <Etk_Textblock_Iter*>iter.obj, text, length)

    def clear(self):
        etk_textblock_clear(<Etk_Textblock*>self.obj)

    def text_get(self, int markup):
        __ret = Object_from_instance(<Etk_Object*>
                                 etk_textblock_text_get(<Etk_Textblock*>self.obj, <Etk_Bool> markup))
        return (__ret.string)

    def range_text_get(self, TextblockIter iter1, TextblockIter iter2, int markup):
        __ret = Object_from_instance(<Etk_Object*> etk_textblock_range_text_get(
            <Etk_Textblock*>self.obj, <Etk_Textblock_Iter *>iter1.obj,
            <Etk_Textblock_Iter *>iter2.obj, <Etk_Bool> markup))
        return (__ret.string)


cdef public class TextView(Widget) [object PyEtk_Text_View, type PyEtk_Text_View_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_text_view_new())
        self._set_common_params(**kargs)

    def textblock_get(self):
        __ret = Object_from_instance(<Etk_Object *>
                                     etk_text_view_textblock_get(<Etk_Text_View*>self.obj))
        return (__ret)

    def cursor_get(self):
        __ret = Object_from_instance(<Etk_Object *> etk_text_view_cursor_get(<Etk_Text_View *>self.obj))
        return (__ret)

    def selection_bound_get(self):
        __ret = Object_from_instance(<Etk_Object *> 
                                     etk_text_view_selection_bound_get(<Etk_Text_View *>self.obj))
        return (__ret)
