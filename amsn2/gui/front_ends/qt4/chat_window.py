# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import cgi
import time

import papyon
from amsn2.gui import base
from amsn2.core.views import ContactView, StringView

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *
try:
    from ui_chatWindow import Ui_ChatWindow
except ImportError, e:
    # FIXME: Should do that with logging...
    print "WARNING: To use the QT4 you need to run the generateFiles.sh, check the README"
    raise e

class InputWidget(QTextEdit):
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)

    def keyPressEvent(self, event):
        print "key pressed:" + str(event.key())
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            print "handle!!"
            self.emit(SIGNAL("enterKeyTriggered()"))
        else:
            QTextEdit.keyPressEvent(self, event)

class aMSNChatWindow(QTabWidget, base.aMSNChatWindow):
    def __init__(self, amsn_core, parent=None):
        QTabWidget.__init__(self, parent)

        self._core = amsn_core

    def addChatWidget(self, chat_widget):
        self.addTab(chat_widget, "test")


class aMSNChatWidget(QWidget, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, parent, contacts_uid):
        QWidget.__init__(self, parent)

        self._amsn_conversation = amsn_conversation
        self.ui = Ui_ChatWindow()
        self.ui.setupUi(self)
        self.ui.inputWidget = InputWidget(self)
        self.ui.inputLayout.addWidget(self.ui.inputWidget)
        self._statusBar = QStatusBar(self)
        self.layout().addWidget(self._statusBar)
        self.last_sender = ''
        self.nickstyle = "color:#555555; margin-left:2px"
        self.msgstyle = "margin-left:15px"
        self.infostyle = "margin-left:2px; font-style:italic; color:#6d6d6d"
        self.loadEmoticonList()

        QObject.connect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)
        QObject.connect(self.ui.inputWidget, SIGNAL("enterKeyTriggered()"), self.__sendMessage)
        QObject.connect(self.ui.actionInsert_Emoticon, SIGNAL("triggered()"), self.showEmoticonList)
        self.enterShortcut = QShortcut(QKeySequence("Enter"), self.ui.inputWidget)
        self.nudgeShortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        QObject.connect(self.enterShortcut, SIGNAL("activated()"), self.__sendMessage)
        QObject.connect(self.nudgeShortcut, SIGNAL("activated()"), self.__sendNudge)
        QObject.connect(self.ui.actionNudge, SIGNAL("triggered()"), self.__sendNudge)


    def processInput(self):
        """ Here we process what is inside the widget... so showing emoticon
        and similar stuff"""

        QObject.disconnect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)

        self.text = QString(self.ui.inputWidget.toHtml())

        for emoticon in self.emoticonList:
            if self.text.contains(emoticon) == True:
                print emoticon
                self.text.replace(emoticon, "<img src=\"throbber.gif\" />")

        self.ui.inputWidget.setHtml(self.text)
        self.ui.inputWidget.moveCursor(QTextCursor.End)
        self.__typingNotification()

        QObject.connect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)

    def loadEmoticonList(self):
        self.emoticonList = QStringList()

        """ TODO: Request emoticon list from amsn core, maybe use a QMap to get the image URL? """

        """ TODO: Discuss how to handle custom emoticons. We have to provide an option
        to change the default icon theme, this includes standard emoticons too.
        Maybe qrc? """

        #self.emoticonList << ";)" << ":)" << "EmOtIcOn"
        #We want :) and ;) to work for now :p
        self.emoticonList << "EmOtIcOn"

    def showEmoticonList(self):
        """ Let's popup emoticon selection here """
        print "Guess what? No emoticons. But I'll put in a random one for you"
        self.appendImageAtCursor("throbber.gif")

    def __sendMessage(self):
        # TODO: Switch to this when implemented
        """ msg = self.ui.inputWidget.toHtml()
        self.ui.inputWidget.clear()
        strv = StringView()
        strv.appendElementsFromHtml(msg) """

        msg = self.ui.inputWidget.toPlainText()
        self.ui.inputWidget.clear()
        strv = StringView()
        strv.appendText(unicode(msg))
        ## as we send our msg to the conversation:
        self._amsn_conversation.sendMessage(strv)
        # this one will also notify us of our msg.
        # so no need to do:
        #self.ui.textEdit.append("<b>/me says:</b><br>"+unicode(msg)+"")
        
    def __sendNudge(self):
        self._amsn_conversation.sendNudge()
        self.ui.textEdit.append("<b>/me sent a nudge</b>")

    def __typingNotification(self):
        self._amsn_conversation.sendTypingNotification()

    def appendTextAtCursor(self, text):
        self.ui.inputWidget.textCursor().insertHtml(unicode(text))

    def appendImageAtCursor(self, image):
        self.ui.inputWidget.textCursor().insertHtml(QString("<img src=\"" + str(image) + "\" />"))

    def onUserJoined(self, contact):
        self.ui.textEdit.append(unicode("<b>"+QString.fromUtf8(contact.toHtmlString())+" "+self.tr("has joined the conversation")+("</b>")))
        pass

    def onUserLeft(self, contact):
        self.ui.textEdit.append(unicode("<b>"+QString.fromUtf8(contact.toHtmlString())+" "+self.tr("has left the conversation")+("</b>")))
        pass

    def onUserTyping(self, contact):
        self._statusBar.showMessage(unicode(QString.fromUtf8(contact.toHtmlString()) + " is typing"), 7000)

    def onMessageReceived(self, messageview, formatting=None):
        print "Ding!"

        text = unicode(QString.fromUtf8(messageview.toStringView().toHtmlString()))
        text = cgi.escape(text)
        nick, msg = text.split('\n', 1)
        nick = unicode(QString.fromUtf8(nick.replace('\n', '<br/>')))
        msg = unicode(QString.fromUtf8(msg.replace('\n', '<br/>')))
        sender = unicode(QString.fromUtf8(messageview.sender.toHtmlString()))

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

        html = '<div>'
        if (self.last_sender != sender):
            html += '<span style="%s">%s</span><br/>' % (self.nickstyle, nick)
        html += '<span style="%s">[%s] %s</span></div>' % (self.msgstyle, time.strftime('%X'), msg)

        self.ui.textEdit.append(html)
        self.last_sender = sender

    def onNudgeReceived(self, sender):
        self.ui.textEdit.append(unicode("<b>"+QString.fromUtf8(sender.toHtmlString())+" "+self.tr("sent you a nudge!")+("</b>")))
        pass


