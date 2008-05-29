
import gtk
import gobject

from amsn2.core.views import StringView
from amsn2.core.views import GroupView
from amsn2.core.views import ContactView
from amsn2.gui import base
import pymsn

class aMSNContactList(base.aMSNContactList, gtk.TreeView):
    '''GTK contactlist'''
    
    def __init__(self, amsn_core):
        '''Constructor'''
        
        gtk.TreeView.__init__(self)
        
        self._amsn_core = amsn_core
        self._main_win = self._amsn_core.getMainWindow()
        
        # the image (None for groups) the object (group or contact) and 
        # the string to display
        self._model = gtk.TreeStore(gtk.gdk.Pixbuf, object, str)
        self.model = self._model.filter_new(root=None)
        #self.model.set_visible_func(self._visible_func)

        self._model.set_sort_func(1, self._sort_method)
        self._model.set_sort_column_id(1, gtk.SORT_ASCENDING)
        self.set_model(self.model)
        
        crt = gtk.CellRendererText()
        column = gtk.TreeViewColumn()
        column.set_expand(True)
        
        exp_column = gtk.TreeViewColumn()
        exp_column.set_max_width(16)       
        
        self.append_column(exp_column)
        self.append_column(column)
        self.set_expander_column(exp_column)
        
        column.pack_start(crt)
        column.add_attribute(crt, 'markup', 2)
        
        self.set_search_column(2)
        self.set_headers_visible(False)
        
        self.view = gtk.VBox()
        self.view.pack_start(self, True, True)
        self.view.show_all()
        
        self._main_win.set_view(self.view)

    def show(self):
        pass #self._edje.show()

    def hide(self):
        pass #self._edje.hide()

    def contactUpdated(self, contact):
        contact_data = (None, contact, contact.name.toString())

        for row in self._model:
            obj = row[1]
            if type(obj) == GroupView:
                for contact_row in row.iterchildren():
                    con = contact_row[1]
                    if con.uid == contact.uid:
                        self._model[contact_row.iter] = contact_data
                        #self.groupUpdated(obj)
            elif type(obj) == ContactView and obj.account == contact.account:
                self._model[row.iter] = contact_data

    def groupUpdated(self, group):
        print 'group updated...'
        raise NotImplementedError
    
    def groupAdded(self, group):
        group_data = (None, group, self.format_group(group))
        iter = self._model.append(None, group_data)
        
        for contact in group.contacts:
            contact_data = (None, contact, contact.name.toString())
            
            self._model.append(iter, contact_data)
            
        path = self._model.get_path(iter)
        self.expand_row(path, False)

    def format_group(self, group):
        return '<b>' + group.name.toString() + '</b>'

    def groupRemoved(self, group):
        pass

    def _sort_method(self, model, iter1, iter2, user_data=None):
        '''callback called to decide the order of the contacts'''

        obj1 = self._model[iter1][1]
        obj2 = self._model[iter2][1]

        return 1
        #if type(obj1) == Group and type(obj2) == Group:
        #    return self.compare_groups(obj1, obj2)
        #elif type(obj1) == Contact and type(obj2) == Contact:
        #    return self.compare_contacts(obj1, obj2)
        #elif type(obj1) == Group and type(obj2) == Contact:
        #    return -1
        #else:
        #    return 1

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass
