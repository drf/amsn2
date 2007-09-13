#!/usr/bin/env python2

import c_etk
from c_etk import main, main_iterate, main_quit, Object, Widget, signal_stop, \
                  theme_widget_set_from_path

c_etk._object_mapping_register('Etk_Object', Object)
c_etk._object_mapping_register('Etk_Widget', Widget)


class Window(c_etk.Window, c_etk.WindowEnums):
    pass
c_etk._object_mapping_register('Etk_Window', Window)

class Embed(c_etk.Embed, c_etk.EmbedEnums):
    pass
c_etk._object_mapping_register('Etk_Embed', Embed)


class Label(c_etk.Label, c_etk.LabelEnums):
    pass
c_etk._object_mapping_register('Etk_Label', Label)


class Button(c_etk.Button, c_etk.ButtonEnums):
    pass
c_etk._object_mapping_register('Etk_Button', Button)


class Table(c_etk.Table, c_etk.TableEnums):
    pass
c_etk._object_mapping_register('Etk_Table', Table)


class HBox(c_etk.HBox, c_etk.BoxEnums):
    pass
c_etk._object_mapping_register('Etk_HBox', HBox)


class VBox(c_etk.VBox, c_etk.BoxEnums):
    pass
c_etk._object_mapping_register('Etk_VBox', VBox)


class Entry(c_etk.Entry, c_etk.EntryEnums):
    pass
c_etk._object_mapping_register('Etk_Entry', Entry)

class Combobox(c_etk.Combobox, c_etk.ComboboxEnums):
    pass
c_etk._object_mapping_register('Etk_Combobox', Combobox)

class ComboboxItem(c_etk.ComboboxItem):
    pass
c_etk._object_mapping_register('Etk_Combobox_Item', ComboboxItem)

class ComboboxEntry(c_etk.ComboboxEntry, c_etk.ComboboxEntryEnums):
    pass
c_etk._object_mapping_register('Etk_ComboboxEntry', ComboboxEntry)

class ComboboxEntry_Item(c_etk.ComboboxEntry_Item):
    pass
c_etk._object_mapping_register('Etk_Combobox_Entry_Item', ComboboxItem)

class Image(c_etk.Image, c_etk.ImageEnums):
    pass
c_etk._object_mapping_register('Etk_Image', Image)

class ProgressBar(c_etk.ProgressBar, c_etk.ProgressBarEnums):
    pass
c_etk._object_mapping_register('Etk_Progress_Bar', ProgressBar)

class HSlider(c_etk.HSlider, c_etk.SliderEnums):
    pass
c_etk._object_mapping_register('Etk_HSlider', HSlider)

class VSlider(c_etk.VSlider, c_etk.SliderEnums):
    pass
c_etk._object_mapping_register('Etk_VSlider', VSlider)

class Frame(c_etk.Frame, c_etk.FrameEnums):
    pass
c_etk._object_mapping_register('Etk_Frame', Frame)

class Canvas(c_etk.Canvas, c_etk.CanvasEnums):
    pass
c_etk._object_mapping_register('Etk_Canvas', Canvas)

class ToggleButton(c_etk.ToggleButton, c_etk.ToggleButtonEnums):
    pass
c_etk._object_mapping_register('Etk_Toggle_Button', ToggleButton)

c_etk.init()
