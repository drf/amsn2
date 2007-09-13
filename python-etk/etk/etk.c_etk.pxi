cdef extern class etk.c_etk.Object:
 cdef Etk_Object (*obj)
 cdef object _data
 cdef object _connections
cdef extern class etk.c_etk.Widget:
 cdef object _virtual_size_request
cdef extern class etk.c_etk.Label:
 pass
cdef extern class etk.c_etk.Container:
 pass
cdef extern class etk.c_etk.Bin:
 pass
cdef extern class etk.c_etk.Toplevel:
 pass
cdef extern class etk.c_etk.Window:
 pass
cdef extern class etk.c_etk.Embed:
 pass
cdef extern class etk.c_etk.Box:
 pass
cdef extern class etk.c_etk.HBox:
 pass
cdef extern class etk.c_etk.VBox:
 pass
cdef extern class etk.c_etk.Image:
 pass
cdef extern class etk.c_etk.Button:
 pass
cdef extern class etk.c_etk.Table:
 pass
cdef extern class etk.c_etk.Entry:
 pass
cdef extern class etk.c_etk.ComboboxItem:
 pass
cdef extern class etk.c_etk.Combobox:
 pass
cdef extern class etk.c_etk.ComboboxEntry_Item:
 pass
cdef extern class etk.c_etk.ComboboxEntry:
 pass
cdef extern class etk.c_etk.ProgressBar:
 pass
cdef extern class etk.c_etk.Range:
 pass
cdef extern class etk.c_etk.Slider:
 pass
cdef extern class etk.c_etk.HSlider:
 pass
cdef extern class etk.c_etk.VSlider:
 pass
cdef extern class etk.c_etk.Frame:
 pass
cdef extern class etk.c_etk.Canvas:
 pass
cdef extern class etk.c_etk.ToggleButton:
 pass
