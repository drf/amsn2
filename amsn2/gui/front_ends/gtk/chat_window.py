# -*- coding: utf-8 -*-
#===================================================
# 
# chat_window.py - This file is part of the amsn2 package
#
# Copyright (C) 2008  Wil Alvarez <wil_alejandro@yahoo.com>
#
# This script is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software 
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This script is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License 
# for more details.
#
# You should have received a copy of the GNU General Public License along with 
# this script (see COPYING); if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#===================================================

import gc
import gtk
import cgi
import time
import pango
from htmltextview import *
from amsn2.gui import base
from amsn2.core.views import ContactView, StringView
import gtk_extras
import papyon
import gobject
import os
from image import Image

class aMSNChatWindow(base.aMSNChatWindow, gtk.Window):
    def __init__(self, amsn_core):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self._amsn_core = amsn_core
        self.child = None
        self.showed = False
        self.set_default_size(550, 450)
        self.set_position(gtk.WIN_POS_CENTER)
        self._theme_manager = amsn_core._core._theme_manager

        #leave

    def addChatWidget(self, chat_widget):
        print 'addedChatWidget'
        #if self.child is not None: self.remove(self.child)
        #if self.child is not None:
        #    self.show_all()
        #    return
        if self.child is None: self.add(chat_widget)
        self.child = chat_widget

        self.show_all()
        self.child.entry.grab_focus()


class aMSNChatWidget(base.aMSNChatWidget, gtk.VBox):
    def __init__(self, amsn_conversation, parent, contacts_uid):
        gtk.VBox.__init__(self, False, 0)

        self._parent = parent
        self._amsn_conversation = amsn_conversation
        self._amsn_core = amsn_conversation._core
        self._theme_manager = self._amsn_core._theme_manager
        self._contactlist_manager = self._amsn_core._contactlist_manager
        self.padding = 4
        self.lastmsg = ''
        self.last_sender = ''
        self.nickstyle = "color:#555555; margin-left:2px"
        self.msgstyle = "margin-left:15px"
        self.infostyle = "margin-left:2px; font-style:italic; color:#6d6d6d"

        amsncontacts = [self._contactlist_manager.getContact(uid) for uid in contacts_uid]
        cviews = [ContactView(self._amsn_core, c) for c in amsncontacts]
        self.chatheader = aMSNChatHeader(self._theme_manager, cviews)

        # Titlebar
        parent.set_title("aMSN2 - " + str(cviews[0].name.getTag("nickname")))

        # Middle
        self.textview = HtmlTextView()
        tscroll = gtk.ScrolledWindow()
        tscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        tscroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        tscroll.add(self.textview)

        #self.chat_roster = ChatRoster()

        self.middle_box = gtk.HPaned()
        self.middle_box.pack1(tscroll, True, True)

        # Bottom
        self.entry = MessageTextView()

        # Tags for entry
        tag = self.entry.get_buffer().create_tag("bold")
        tag.set_property("weight", pango.WEIGHT_BOLD)
        tag = self.entry.get_buffer().create_tag("italic")
        tag.set_property("style", pango.STYLE_ITALIC)
        tag = self.entry.get_buffer().create_tag("underline")
        tag.set_property("underline", pango.UNDERLINE_SINGLE)
        tag = self.entry.get_buffer().create_tag("strikethrough")
        tag.set_property("strikethrough", True)
        tag = self.entry.get_buffer().create_tag("foreground")
        tag.set_property("foreground_gdk", gtk.gdk.Color(0,0,0))
        tag = self.entry.get_buffer().create_tag("family")
        tag.set_property("family", "MS Sans Serif")

        escroll = gtk.ScrolledWindow()
        escroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        escroll.set_placement(gtk.CORNER_TOP_LEFT)
        escroll.set_shadow_type(gtk.SHADOW_IN)
        escroll.set_size_request(-1, 40)
        escroll.add(self.entry)

        # Register button icons as stock icons
        iconfactory = gtk.IconFactory()
        icons = ['button_smile', 'button_nudge']
        for key in icons:
            type, path = self._theme_manager.get_button(key)
            pixbuf = gtk.gdk.pixbuf_new_from_file(path)
            iconset = gtk.IconSet(pixbuf)
            iconfactory.add(key, iconset)
            iconfactory.add_default()
            del pixbuf
            gc.collect()

        self.button1 = gtk.ToolButton('button_smile')
        self.button2 = gtk.ToolButton('button_nudge')
        self.button_bold = gtk.ToggleToolButton(gtk.STOCK_BOLD)
        self.button_italic = gtk.ToggleToolButton(gtk.STOCK_ITALIC)
        self.button_underline = gtk.ToggleToolButton(gtk.STOCK_UNDERLINE)
        self.button_strikethrough = gtk.ToggleToolButton(gtk.STOCK_STRIKETHROUGH)
        self.button_color = gtk_extras.ColorToolButton()
        self.button_font = gtk_extras.FontToolButton()
        self.button8 = gtk.ToolButton(gtk.STOCK_CLEAR)

        self.button_font.set_show_size(0)
        self.button_font.set_show_style(0)

        bbox = gtk.Toolbar()
        bbox.set_style(gtk.TOOLBAR_ICONS)
        bbox.insert(self.button1, -1)
        bbox.insert(self.button2, -1)
        bbox.insert(gtk.SeparatorToolItem(), -1)
        bbox.insert(self.button_font, -1)
        bbox.insert(self.button_color, -1)
        bbox.insert(self.button_bold, -1)
        bbox.insert(self.button_italic, -1)
        bbox.insert(self.button_underline, -1)
        bbox.insert(self.button_strikethrough, -1)
        bbox.insert(gtk.SeparatorToolItem(), -1)
        bbox.insert(self.button8, -1)

        bottom_box = gtk.VBox(False, 0)
        bottom_box.pack_start(bbox, False, False, 0)
        bottom_box.pack_start(escroll, True,True, 0)

        self.statusbar = gtk.Statusbar()
        self.statusbar.set_has_resize_grip(False)
        self.statusbar.set_spacing(0)

        self.__set_statusbar_text('Welcome to aMSN2')

        vpaned = gtk.VPaned()
        vpaned.pack1(self.middle_box, True, True)
        vpaned.pack2(bottom_box, False, True)

        self.pack_start(self.chatheader, False, False, self.padding)
        self.pack_start(vpaned, True, True, self.padding)
        self.pack_start(self.statusbar, False, False)

        #Connections
        #========
        '''
        self.entrytextview.connect('focus-in-event', self.chatman.setUrgencyHint, False)
        self.entrytextview.get_buffer().connect("changed",self.__updateTextFormat)
        self.textview.connect("button-press-event", self.__rightClick)

        '''
        '''
        self.textview.connect("url-clicked", self.__on_url_clicked)

        self.button1.connect("clicked", self.__create_smiles_window)
        self.button3.connect("clicked",
            self.__on_changed_text_effect, 'bold')
        self.button4.connect("clicked",
            self.__on_changed_text_effect, 'italic')
        self.button5.connect("clicked",
            self.__on_changed_text_effect, 'underline')
        self.button6.connect("clicked",
            self.__on_changed_text_effect, 'strikethrough')
        self.button7.connect("clicked", self.__on_changed_text_color)
        '''
        self.entry.get_buffer().connect("changed", self.__updateTextFormat)
        self.button_bold.connect("toggled", self.__on_changed_text_effect, "bold")
        self.button_italic.connect("toggled", self.__on_changed_text_effect, "italic")
        self.button_underline.connect("toggled", self.__on_changed_text_effect, "underline")
        self.button_strikethrough.connect("toggled", self.__on_changed_text_effect, "strikethrough")
        self.button_color.connect("color_set", self.__on_changed_text_color)
        self.button_font.connect("font_set", self.__on_changed_text_font)
        self.button2.connect("clicked", self.__on_nudge_send)
        self.button8.connect("clicked", self.__on_clear_textview)
        self.entry.connect('mykeypress', self.__on_chat_send)
        self.entry.connect('key-press-event', self.__on_typing_event)

        # timer to display if a user is typing
        self.typingTimer = None

    def __updateTextFormat(self, textbuffer):
        self.reapply_text_effects()
        self.__on_changed_text_color(self.button_color)
        self.__on_changed_text_font(self.button_font)

    def __on_changed_text_effect(self, button, tag_type):
        buffer = self.entry.get_buffer()
        if button.get_active():
            buffer.apply_tag_by_name(tag_type, buffer.get_start_iter(), buffer.get_end_iter())
        else:
            buffer.remove_tag_by_name(tag_type, buffer.get_start_iter(), buffer.get_end_iter())

    def reapply_text_effects(self):
        self.__on_changed_text_effect(self.button_bold, "bold")
        self.__on_changed_text_effect(self.button_italic, "italic")
        self.__on_changed_text_effect(self.button_underline, "underline")
        self.__on_changed_text_effect(self.button_strikethrough, "strikethrough")

    def __on_changed_text_color(self, button):
        buffer = self.entry.get_buffer()
        tag = buffer.get_tag_table().lookup("foreground")
        tag.set_property("foreground_gdk", button.get_color())
        buffer.apply_tag_by_name("foreground", buffer.get_start_iter(), buffer.get_end_iter())

    def __on_changed_text_font(self, button):
        buffer = self.entry.get_buffer()
        font_name = self.button_font.get_font_name()
        font_family = pango.FontDescription(font_name).get_family()
        tag = buffer.get_tag_table().lookup("family")
        tag.set_property("family", font_family)
        buffer.apply_tag_by_name("family", buffer.get_start_iter(), buffer.get_end_iter())

    def __clean_string(self, str):
        return cgi.escape(str)

    def __on_chat_send(self, entry, event_keyval, event_keymod):
        if (event_keyval == gtk.keysyms.Return):
            buffer = entry.get_buffer()
            start, end = buffer.get_bounds()
            msg = buffer.get_text(start, end)
            entry.clear()
            entry.grab_focus()
            if (msg == ''): return False

            color = self.button_color.get_color()
            hex8 = "%.2x%.2x%.2x" % ((color.red/0x101), (color.green/0x101), (color.blue/0x101))
            style = papyon.TextFormat.NO_EFFECT
            if self.button_bold.get_active(): style |= papyon.TextFormat.BOLD
            if self.button_italic.get_active():  style |= papyon.TextFormat.ITALIC
            if self.button_underline.get_active(): style |= papyon.TextFormat.UNDERLINE
            if self.button_strikethrough.get_active(): style |= papyon.TextFormat.STRIKETHROUGH
            font_name = self.button_font.get_font_name()
            font_family = pango.FontDescription(font_name).get_family()
            format = papyon.TextFormat(font=font_family, color=hex8, style=style)
            strv = StringView()
            strv.appendText(msg)
            self._amsn_conversation.sendMessage(strv, format)

        elif event_keyval == gtk.keysyms.Escape:
            self._parent.destroy()

    def __on_clear_textview(self, widget):
        buffer = self.textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        buffer.delete(start, end)

    def __on_typing_event(self, widget, event):
        self._amsn_conversation.sendTypingNotification()

    def __on_nudge_send(self, widget):
        self.__print_info('Nudge sent')
        self._amsn_conversation.sendNudge()

    def __print_chat(self, nick, msg, sender):
        html = '<div>'
        # TODO: If we have the same nick as our chat buddy, this doesn't work
        if (self.last_sender != sender):
            html += '<span style="%s">%s</span><br/>' % (self.nickstyle,
                nick)
        html += '<span style="%s">[%s] %s</span></div>' % (self.msgstyle,
            time.strftime('%X'), msg)

        self.textview.display_html(html)
        self.textview.scroll_to_bottom()

    def __print_info(self, msg):
        html = '<div><span style="%s">%s</span></div>' % (self.infostyle, msg)
        self.textview.display_html(html)
        self.textview.scroll_to_bottom()

    def __set_statusbar_text(self, msg):
        context = self.statusbar.get_context_id('msg')
        self.statusbar.pop(context)
        self.statusbar.push(context, msg)

    def __typingStopped(self):
        self.__set_statusbar_text("")
        return False # To stop gobject timer

    def onMessageReceived(self, messageview, formatting=None):
        text = messageview.toStringView().toHtmlString()
        text = self.__clean_string(text)
        nick, msg = text.split('\n', 1)
        nick = str(nick.replace('\n', '<br/>'))
        msg = str(msg.replace('\n', '<br/>'))
        sender = str(messageview.sender)

        # peacey: Check formatting of styles and perform the required changes
        if formatting:
            fmsg = '''<span style="'''
            if formatting.font:
                fmsg += "font-family: %s;" % formatting.font
            if formatting.color:
                fmsg += "color: %s;" % ("#"+formatting.color)
            if formatting.style & papyon.TextFormat.BOLD == papyon.TextFormat.BOLD:
                fmsg += "font-weight: bold;"
            if formatting.style & papyon.TextFormat.ITALIC == papyon.TextFormat.ITALIC:
                fmsg += "font-style: italic;"
            if formatting.style & papyon.TextFormat.UNDERLINE == papyon.TextFormat.UNDERLINE:
                fmsg += "text-decoration: underline;"
            if formatting.style & papyon.TextFormat.STRIKETHROUGH == papyon.TextFormat.STRIKETHROUGH:
                fmsg += "text-decoration: line-through;"
            if formatting.right_alignment:
                fmsg += "text-align: right;"
            fmsg = fmsg.rstrip(";")
            fmsg += '''">'''
            fmsg += msg
            fmsg += "</span>"
        else:
            fmsg = msg

        self.__print_chat(nick, fmsg, sender)

        self.last_sender = sender
        self.__typingStopped()

    def onUserJoined(self, contact):
        print "%s joined the conversation" % (contact,)
        self.__print_info("%s joined the conversation" % (contact,))
        self.__set_statusbar_text("%s joined the comversation" % (contact,))

    def onUserLeft(self, contact):
        print "%s left the conversation" % (contact,)
        self.__print_info("%s left the conversation" % (contact,))
        self.__set_statusbar_text("%s left the conversation" % (contact,))
        self.__typingStopped()

    def onUserTyping(self, contact):
        """ Set a timer for 10 sec every time a user types. If the user
        continues typing during these 10 sec, kill the timer and start over with
        10 sec. If the user stops typing; call __typingStopped """

        print "%s is typing" % (contact,)
        self.__set_statusbar_text("%s is typing" % (contact,))
        if self.typingTimer != None:
            gobject.source_remove(self.typingTimer)
            self.typingTimer = None
        self.typingTimer = gobject.timeout_add(10000, self.__typingStopped)

    def nudge(self):
        self.__print_info('Nudge received')


class aMSNChatHeader(gtk.EventBox):
    def __init__(self, theme_manager, cviews=None):
        gtk.EventBox.__init__(self)

        self.buddy_icon = gtk.Image()
        self.title = gtk.Label()
        self.dp = gtk.Image()
        self.title_color = gtk.gdk.color_parse('#dadada')
        self.psm_color = '#999999'
        self.theme_manager = theme_manager

        self.title.set_use_markup(True)
        self.title.set_justify(gtk.JUSTIFY_LEFT)
        self.title.set_ellipsize(pango.ELLIPSIZE_END)
        self.title.set_alignment(xalign=0, yalign=0.5)
        self.title.set_padding(xpad=2, ypad=2)

        self.dp.set_size_request(50,50)

        hbox = gtk.HBox(False,0)
        hbox.pack_start(self.buddy_icon, False,False,0)
        hbox.pack_start(self.title, True,True,0)
        hbox.pack_start(self.dp, False,False,0)

        self.modify_bg(gtk.STATE_NORMAL, self.title_color)
        self.add(hbox)

        self.update(cviews)

    def update(self, cviews):
        """
        @param cviews: list contacts participating in the conversation.
        @type cviews: list of ContactView's
        """
        #FIXME: Show all users in a multiconversation
        nickname = cviews[0].name.getTag("nickname")
        psm = cviews[0].name.getTag("psm")
        status = cviews[0].name.getTag("status")

        #FIXME: Which user do we show in a multiconversation?
        img = Image(self.theme_manager, cviews[0].dp)
        self.dp.set_from_pixbuf(img.to_pixbuf(50,50))

        title = '<span size="large"><b>%s</b></span>' % (nickname, )
        title += '<span size="medium">  %s</span>' % (status, )

        if(psm != ''):
            title += '\n<span size="small" foreground="%s">%s</span>' % (
            self.psm_color, psm)

        self.title.set_markup(title)

