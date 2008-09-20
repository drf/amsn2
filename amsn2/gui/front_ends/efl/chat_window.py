
from constants import *
import ecore
import ecore.evas
import ecore.x
import etk
import skins
import window
from amsn2.gui import base
from amsn2.core.views import MenuView, MenuItemView

class aMSNChatWindow(window.aMSNWindow, base.aMSNChatWindow):
    def __init__(self, conversation_manager):     
        self._conversation_manager = conversation_manager
        window.aMSNWindow.__init__(self, conversation_manager._core)
        self._container = aMSNChatWidgetContainer()
        self.setTitle("aMSN - Chatwindow")

    def addChatWidget(self, chat_widget):
        #TODO: use the container
        self.child = chat_widget

#TODO: ChatWidgetContainer
class aMSNChatWidgetContainer:
    pass




class aMSNChatWidget(etk.Widget, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, parent):
        self._parent = parent
        self._amsn_conversation = amsn_conversation
        #TODO


    def onUserJoined(self, contact):
        print "%s joined the conversation" % (contact,)

    def onUserLeft(self, contact):
        print "%s left the conversation" % (contact,)

    def onUserTyping(self, contact):
        print "%s is typing" % (contact,)

    def onMessageReceived(self, sender, message):
        print "%s says: %s" % (sender.account, message.content)

    def onNudgeReceived(self, sender):
        print "Nudge received from: %s" %(sender,)
