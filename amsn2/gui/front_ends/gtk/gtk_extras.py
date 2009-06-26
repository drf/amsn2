# Additional helper classes
# ColorToolButton class copied from the sugar project under the GNU LGPL license
# http://sugarlabs.org

import gtk
import gobject

# This not ideal. It would be better to subclass gtk.ToolButton, however
# the python bindings do not seem to be powerfull enough for that.
# (As we need to change a variable in the class structure.)
class ColorToolButton(gtk.ToolItem):
    __gtype_name__ = 'ColorToolButton'
    __gsignals__ = { 'color-set' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,  tuple())}

    def __init__(self, icon_name='color-preview', **kwargs):
        self._accelerator = None
        self._tooltip = None
        #self._palette_invoker = ToolInvoker()
        self._palette = None
        gobject.GObject.__init__(self, **kwargs)
        # The gtk.ToolButton has already added a normal button.
        # Replace it with a ColorButton
        color_button = gtk.ColorButton()
        self.add(color_button)
        # The following is so that the behaviour on the toolbar is correct.
        color_button.set_relief(gtk.RELIEF_NONE)
        color_button.icon_size = gtk.ICON_SIZE_LARGE_TOOLBAR
        #self._palette_invoker.attach_tool(self)
        # This widget just proxies the following properties to the colorbutton
        color_button.connect('notify::color', self.__notify_change)
        color_button.connect('notify::icon-name', self.__notify_change)
        color_button.connect('notify::icon-size', self.__notify_change)
        color_button.connect('notify::title', self.__notify_change)
        color_button.connect('color-set', self.__color_set_cb)
        color_button.connect('can-activate-accel',  self.__button_can_activate_accel_cb)

    def __button_can_activate_accel_cb(self, button, signal_id):
        # Accept activation via accelerators regardless of this widget's state
        return True

    def set_accelerator(self, accelerator):
        self._accelerator = accelerator
        setup_accelerator(self)

    def get_accelerator(self):
        return self._accelerator

    accelerator = gobject.property(type=str, setter=set_accelerator,  getter=get_accelerator)

    def create_palette(self):
        self._palette = self.get_child().create_palette()
        return self._palette

    #def get_palette_invoker(self):
     #   return self._palette_invoker

    #def set_palette_invoker(self, palette_invoker):
      #  self._palette_invoker.detach()
     #   self._palette_invoker = palette_invoker
    #palette_invoker = gobject.property(  type=object, setter=set_palette_invoker, getter=get_palette_invoker)

    def set_color(self, color):
        self.get_child().props.color = color

    def get_color(self):
        return self.get_child().props.color

    color = gobject.property(type=object, getter=get_color, setter=set_color)

    def set_icon_name(self, icon_name):
        self.get_child().props.icon_name = icon_name

    def get_icon_name(self):
        return self.get_child().props.icon_name

    icon_name = gobject.property(type=str,  getter=get_icon_name, setter=set_icon_name)

    def set_icon_size(self, icon_size):
        self.get_child().props.icon_size = icon_size

    def get_icon_size(self):
        return self.get_child().props.icon_size

    icon_size = gobject.property(type=int,  getter=get_icon_size, setter=set_icon_size)

    def set_title(self, title):
        self.get_child().props.title = title

    def get_title(self):
        return self.get_child().props.title

    title = gobject.property(type=str, getter=get_title, setter=set_title)

    def do_expose_event(self, event):
        child = self.get_child()
        allocation = self.get_allocation()
        if self._palette and self._palette.is_up():
            invoker = self._palette.props.invoker
            invoker.draw_rectangle(event, self._palette)
        elif child.state == gtk.STATE_PRELIGHT:
            child.style.paint_box(event.window, gtk.STATE_PRELIGHT,  gtk.SHADOW_NONE, event.area,  child, 'toolbutton-prelight',  allocation.x, allocation.y,  allocation.width, allocation.height)

        gtk.ToolButton.do_expose_event(self, event)

    def __notify_change(self, widget, pspec):
        self.notify(pspec.name)

    def __color_set_cb(self, widget):
        self.emit('color-set')

class FontToolButton(gtk.ToolItem):
    __gtype_name__ = 'FontToolButton'
    __gsignals__ = { 'font-set' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,  tuple())}

    def __init__(self, icon_name='font-preview', **kwargs):
        self._accelerator = None
        self._tooltip = None
        #self._palette_invoker = ToolInvoker()
        self._palette = None
        gobject.GObject.__init__(self, **kwargs)
        # The gtk.ToolButton has already added a normal button.
        # Replace it with a ColorButton
        font_button = gtk.FontButton()
        self.add(font_button)
        # The following is so that the behaviour on the toolbar is correct.
        font_button.set_relief(gtk.RELIEF_NONE)
        font_button.icon_size = gtk.ICON_SIZE_LARGE_TOOLBAR
        #self._palette_invoker.attach_tool(self)
        # This widget just proxies the following properties to the colorbutton
        font_button.connect('notify::font-name', self.__notify_change)
        font_button.connect('notify::show-style', self.__notify_change)
        font_button.connect('notify::show-size', self.__notify_change)
        font_button.connect('notify::icon-name', self.__notify_change)
        font_button.connect('notify::icon-size', self.__notify_change)
        font_button.connect('notify::title', self.__notify_change)
        font_button.connect('font-set', self.__font_set_cb)
        font_button.connect('can-activate-accel',  self.__button_can_activate_accel_cb)

    def __button_can_activate_accel_cb(self, button, signal_id):
        # Accept activation via accelerators regardless of this widget's state
        return True

    def set_accelerator(self, accelerator):
        self._accelerator = accelerator
        setup_accelerator(self)

    def get_accelerator(self):
        return self._accelerator

    accelerator = gobject.property(type=str, setter=set_accelerator,  getter=get_accelerator)

    def create_palette(self):
        self._palette = self.get_child().create_palette()
        return self._palette

    def set_font_name(self, font_name):
        self.get_child().props.font_name = font_name

    def get_font_name(self):
        return self.get_child().props.font_name

    font_name = gobject.property(type=object, getter=get_font_name, setter=set_font_name)

    def set_show_size(self, show_size):
        self.get_child().props.show_size = show_size

    def get_show_size(self):
        return self.get_child().props.show_size

    show_size = gobject.property(type=object, getter=get_show_size, setter=set_show_size)

    def set_show_style(self, show_style):
        self.get_child().props.show_style = show_style

    def get_show_style(self):
        return self.get_child().props.show_style

    show_style = gobject.property(type=object, getter=get_show_style, setter=set_show_style)


    def set_icon_name(self, icon_name):
        self.get_child().props.icon_name = icon_name

    def get_icon_name(self):
        return self.get_child().props.icon_name

    icon_name = gobject.property(type=str,  getter=get_icon_name, setter=set_icon_name)

    def set_icon_size(self, icon_size):
        self.get_child().props.icon_size = icon_size

    def get_icon_size(self):
        return self.get_child().props.icon_size

    icon_size = gobject.property(type=int,  getter=get_icon_size, setter=set_icon_size)

    def set_title(self, title):
        self.get_child().props.title = title

    def get_title(self):
        return self.get_child().props.title

    title = gobject.property(type=str, getter=get_title, setter=set_title)

    def do_expose_event(self, event):
        child = self.get_child()
        allocation = self.get_allocation()
        if self._palette and self._palette.is_up():
            invoker = self._palette.props.invoker
            invoker.draw_rectangle(event, self._palette)
        elif child.state == gtk.STATE_PRELIGHT:
            child.style.paint_box(event.window, gtk.STATE_PRELIGHT,  gtk.SHADOW_NONE, event.area,  child, 'toolbutton-prelight',  allocation.x, allocation.y,  allocation.width, allocation.height)

        gtk.ToolButton.do_expose_event(self, event)

    def __notify_change(self, widget, pspec):
        self.notify(pspec.name)

    def __font_set_cb(self, widget):
        self.emit('font-set')

