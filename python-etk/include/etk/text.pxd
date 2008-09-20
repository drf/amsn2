cdef extern from "etk_textblock.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Textblock_Wrap:
        ETK_TEXTBLOCK_WRAP_NONE
        ETK_TEXTBLOCK_WRAP_DEFAULT
        ETK_TEXTBLOCK_WRAP_WORD
        ETK_TEXTBLOCK_WRAP_CHAR

    ctypedef enum Etk_Textblock_Node_Type:
        ETK_TEXTBLOCK_NODE_ROOT
        ETK_TEXTBLOCK_NODE_PARAGRAPH
        ETK_TEXTBLOCK_NODE_LINE
        ETK_TEXTBLOCK_NODE_NORMAL

    ctypedef enum Etk_Textblock_Tag_Type:
        ETK_TEXTBLOCK_TAG_DEFAULT
        ETK_TEXTBLOCK_TAG_BOLD
        ETK_TEXTBLOCK_TAG_ITALIC
        ETK_TEXTBLOCK_TAG_UNDERLINE
        ETK_TEXTBLOCK_TAG_STRIKETHROUGH
        ETK_TEXTBLOCK_TAG_P
        ETK_TEXTBLOCK_TAG_STYLE
        ETK_TEXTBLOCK_TAG_FONT

    ctypedef enum Etk_Textblock_Style_Type:
        ETK_TEXTBLOCK_STYLE_NONE
        ETK_TEXTBLOCK_STYLE_OUTLINE
        ETK_TEXTBLOCK_STYLE_SHADOW
        ETK_TEXTBLOCK_STYLE_SOFT_OUTLINE
        ETK_TEXTBLOCK_STYLE_GLOW
        ETK_TEXTBLOCK_STYLE_OUTLINE_SHADOW
        ETK_TEXTBLOCK_STYLE_FAR_SHADOW
        ETK_TEXTBLOCK_STYLE_OUTLINE_SOFT_SHADOW
        ETK_TEXTBLOCK_STYLE_SOFT_SHADOW
        ETK_TEXTBLOCK_STYLE_FAR_SOFT_SHADOW

    ctypedef enum Etk_Textblock_Underline_Type:
        ETK_TEXTBLOCK_UNDERLINE_NONE
        ETK_TEXTBLOCK_UNDERLINE_SINGLE
        ETK_TEXTBLOCK_UNDERLINE_DOUBLE

    ctypedef enum Etk_Textblock_Gravity:
        ETK_TEXTBLOCK_GRAVITY_RIGHT
        ETK_TEXTBLOCK_GRAVITY_LEFT

    ####################################################################
    # Structures
    ctypedef struct Etk_Textblock
    ctypedef struct Etk_Textblock_Iter

    ####################################################################
    # Functions
    Etk_Textblock *etk_textblock_new()

    void etk_textblock_text_set(Etk_Textblock *tb, char *text, Etk_Bool markup)
    Etk_String *etk_textblock_text_get(Etk_Textblock *tb, Etk_Bool markup)
    Etk_String *etk_textblock_range_text_get(Etk_Textblock *tb, Etk_Textblock_Iter *iter1, Etk_Textblock_Iter *iter2, Etk_Bool markup)

    void etk_textblock_insert(Etk_Textblock *tb, Etk_Textblock_Iter *iter, char *text, int length)

    void etk_textblock_clear(Etk_Textblock *tb)

    Etk_Textblock_Iter   *etk_textblock_iter_new(Etk_Textblock *tb)
    void etk_textblock_iter_free (Etk_Textblock_Iter *__self)
    void     etk_textblock_iter_backward_start(Etk_Textblock_Iter *iter)
    void     etk_textblock_iter_forward_end(Etk_Textblock_Iter *iter)




#########################################################################
# Objects
cdef public class Textblock(Object) [object PyEtk_Textblock, type PyEtk_Textblock_Type]:
    pass
cdef public class TextblockIter [object PyEtk_Textblock_Iter, type PyEtk_Textblock_Iter_Type]:
    cdef Etk_Textblock_Iter * obj
    pass






cdef extern from "etk_text_view.h":

    ####################################################################
    # Structures
    ctypedef struct Etk_Text_View

    ####################################################################
    # Functions
    Etk_Widget * etk_text_view_new ()
    Etk_Textblock * etk_text_view_textblock_get (Etk_Text_View *__self)
    Etk_Textblock_Iter * etk_text_view_cursor_get (Etk_Text_View *__self)
    Etk_Textblock_Iter * etk_text_view_selection_bound_get (Etk_Text_View *__self)


#########################################################################
# Objects
cdef public class TextView(Widget) [object PyEtk_Text_View, type PyEtk_Text_View_Type]:
    pass

