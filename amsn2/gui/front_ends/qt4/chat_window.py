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

from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_chatWindow import Ui_ChatWindow
from amsn2.core.views import ContactView, StringView
    
class aMSNChatWindow(QTabWidget, base.aMSNChatWindow):
    def __init__(self, amsn_core, Parent=None):
        QTabWidget.__init__(self, Parent)
        
        self._core = amsn_core
        
    def addChatWidget(self, chat_widget):
        self.addTab(chat_widget, "test")
        
    
class aMSNChatWidget(QWidget, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, Parent=None):
        QWidget.__init__(self, Parent)
        
        self._amsn_conversation = amsn_conversation
        self.ui = Ui_ChatWindow()
        self.ui.setupUi(self)
        self._statusBar = QStatusBar(self)
        self.layout().addWidget(self._statusBar)
        
        self.loadEmoticonList()
        
        QObject.connect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)
        QObject.connect(self.ui.sendButton, SIGNAL("clicked()"), self.__sendMessage)
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
        self._amsn_conversation.sendMessage(strv)
        self.ui.textEdit.append("<b>/me says:</b><br>"+unicode(msg)+"")
        
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
        self.ui.textEdit.append(unicode("<b>"+QString.fromUtf8(contact.name.toString())+" "+self.tr("has joined the conversation")+("</b>")))
        pass

    def onUserLeft(self, contact):
        self.ui.textEdit.append(unicode("<b>"+QString.fromUtf8(contact.name.toString())+" "+self.tr("has left the conversation")+("</b>")))
        pass

    def onUserTyping(self, contact):
        self._statusBar.showMessage(unicode(QString.fromUtf8(contact.name.toString()) + " is typing"), 7000)

    def onMessageReceived(self, sender, message):
        print "Ding!"
        self.ui.textEdit.append(unicode("<b>"+QString.fromUtf8(sender.name.toString())+" "+self.tr("writes:")+("</b>")))
        self.ui.textEdit.append(unicode(message.toHtmlString()))
        pass

    def onNudgeReceived(self, sender):
        self.ui.textEdit.append(unicode("<b>"+sender.name.toString()+" "+self.tr("sent you a nudge!")+("</b>")))
        pass
        
