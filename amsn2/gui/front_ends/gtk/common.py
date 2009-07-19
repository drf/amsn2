
from amsn2.core.views import StringView, MenuItemView

import gobject
import pango
import gtk

GUI_FONT = pango.FontDescription('normal 8')

def stringvToHtml(stringv):
    out = ''
    for x in stringv._elements:
        if x.getType() == StringView.TEXT_ELEMENT:
            out += x.getValue()
        elif x.getType() == StringView.ITALIC_ELEMENT:
            if x.getValue():
                out += '<i>'
            else:
                out += '</i>'
    return out

def escape_pango(str):
    str = gobject.markup_escape_text(str)
    str = str.replace('\n',' ')
    return str

def createMenuItemsFromView(menu, items):
    # TODO: images & radio groups, for now only basic representation
    for item in items:
        if item.type is MenuItemView.COMMAND:
            it = gtk.MenuItem(item.label)
            it.connect("activate", lambda i, item: item.command(), item )
            it.show()
            menu.append(it)
        elif item.type is MenuItemView.CASCADE_MENU:
            men = gtk.Menu()
            it = gtk.MenuItem(item.label)
            createMenuItemsFromView(men, item.items)
            it.set_submenu(men)
            it.show()
            menu.append(it)
        elif item.type is MenuItemView.SEPARATOR:
            it = gtk.SeperatorMenuItem()
            it.show()
            menu.append(it)
        elif item.type is MenuItemView.CHECKBUTTON:
            it = gtk.CheckMenuItem(item.label)
            if item.checkbox:
                it.set_active()
            it.show()
            menu.append(it)
        elif item.type is MenuItemView.RADIOBUTTON:
            it = gtk.RadioMenuItem(item.label)
            it.show()
            menu.append(it)
        elif item.type is MenuItemView.RADIOBUTTONGROUP:
            pass

