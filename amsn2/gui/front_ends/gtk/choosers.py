
from amsn2.gui import base
import image
import gtk

class aMSNFileChooserWindow(base.aMSNFileChooserWindow, gtk.FileChooserDialog):
    def __init__(self, filters, directory, callback):
        gtk.FileChooserDialog.__init__(self, title='aMSN2 -Choose a file',
                                    action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                    buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        for name in filters.keys():
            filefilter = gtk.FileFilter()
            filefilter.set_name(name)
            for ext in filters[name]:
                filefilter.add_pattern(ext)
            self.add_filter(filefilter)

        toggle = gtk.CheckButton("Show hidden files")
        toggle.show()
        toggle.connect('toggled', lambda toggle: self.set_show_hidden(toggle.get_active()))
        self.set_extra_widget(toggle)

        self.preview = gtk.Image()
        self.set_preview_widget(self.preview)
        self.set_use_preview_label(False)

        self.callback = callback
        #self.set_size_request(500, 400)
        self.set_current_folder_uri(directory)

        self.connect('selection-changed', self.activatePreview)
        self.connect('response', self.onResponse)

        self.run()

    def activatePreview(self, chooser):
        filename = self.get_preview_filename()
        if filename:
            info = gtk.gdk.pixbuf_get_file_info(filename)
            if info:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, -1, 96)
                self.preview.set_from_pixbuf(pixbuf)
                self.set_preview_widget_active(True)
                return

        self.set_preview_widget_active(False)

    def onResponse(self, chooser, id):
        if id ==gtk.RESPONSE_OK:
            self.callback(self.get_filename())
        elif id == gtk.RESPONSE_CANCEL:
            pass
        self.destroy()
        

class aMSNDPChooserWindow(base.aMSNDPChooserWindow, gtk.Window):
    def __init__(self, default_dps, actions, callback):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.showed = False
        self.set_default_size(550, 450)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("aMSN - Choose a Display Picture")
        self.callback = callback
        self.view = None

        self.child = None
        self._setup_boxes(actions)
        self.update_dp_list(default_dps)

        self.show()
        self.show_all()

    def _setup_boxes(self, actions):
        tscroll = gtk.ScrolledWindow()
        tscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        tscroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.iconview = gtk.IconView()
        self._model = gtk.ListStore(gtk.gdk.Pixbuf, object)
        self.iconview.set_model(self._model)
        self.iconview.set_pixbuf_column(0)
        self.iconview.set_selection_mode(gtk.SELECTION_SINGLE)
        self.iconview.connect("item-activated", self.__on_dp_dblclick)
        self.iconview.connect("button-press-event", self.__on_dp_click)
        tscroll.add(self.iconview)
        dpsbox = gtk.VBox()
        dpsbox.pack_start(tscroll)

        buttonbox = gtk.VBox(False)
        buttonbox.set_size_request(100, 450)
        currentdp = gtk.Image()
        buttonbox.pack_start(currentdp, False)
        cancel_button = gtk.Button('Cancel', gtk.STOCK_CANCEL)
        cancel_button.connect('clicked', lambda button: self.destroy())
        ok_button = gtk.Button('Ok', gtk.STOCK_OK)
        ok_button.connect('clicked', self._dp_chosen)
        buttonbox.pack_start(ok_button, False)
        buttonbox.pack_start(cancel_button, False)
        for name, cb in actions:
            button = gtk.Button(name)
            def callback(cb):
                return lambda button: cb()
            button.connect('clicked', callback(cb))
            buttonbox.pack_start(button, False)

        hbox = gtk.HBox()
        hbox.pack_start(dpsbox)
        hbox.pack_start(buttonbox, False)
        self.add(hbox)

    def _dp_chosen(self, button):
        self.callback(self.view)
        self.destroy()

    def __on_dp_dblclick(self, widget, path):
        if path:
            iter = self._model.get_iter(path)
            self.view = self._model.get_value(iter, 1)
            self._dp_chosen(None)
            return True

        else:
            return False

    def __on_dp_click(self, source, event):
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 1:
            treepath = self.iconview.get_path_at_pos(int(event.x), int(event.y))

            if treepath:
                iter = self._model.get_iter(treepath)
                self.view = self._model.get_value(iter, 1)

            # Let the double click callback be called
            return False
        else:
            return False

    def update_dp_list(self, default_dps):
        for dp in default_dps:
            im = image.Image(None, dp)
            self._model.append((im.to_pixbuf(96, 96), dp))


