
from constants import *
import ecore
import ecore.evas
import ecore.x
import etk
import skins
import window
from amsn2.gui import base
from amsn2.core.views import ContactView, StringView

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




class aMSNChatWidget(etk.VPaned, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, parent):
        self._parent = parent
        self._amsn_conversation = amsn_conversation
        etk.VPaned.__init__(self)
        self._input = etk.TextView()
        self._output = etk.TextView()
        self._input_container = etk.HBox()
        self._send_button = etk.Button(label="Send")
        self._send_button.on_clicked(self.__sendButton_cb)
        self._input_container.append(self._input, etk.HBox.START, etk.HBox.EXPAND_FILL, 0)
        self._input_container.append(self._send_button, etk.HBox.END, etk.HBox.FILL, 0)
        self.child2_set(self._input_container, 1)
        self.child1_set(self._output, 1)

        self.__input_tb = self._input.textblock_get()
        self.__output_tb = self._output.textblock_get()
        self.__iter_out = etk.TextblockIter(self.__output_tb)
        self.__iter_out.forward_end()
        self.position = 450 #doesn't work for the moment, maybe a bug in etk

    def __sendButton_cb(self, button):
        msg = self.__input_tb.text_get(0)
        self.__input_tb.clear()
        strv = StringView()
        strv.appendText(msg)
        self._amsn_conversation.sendMessage(strv)

    def __outputAppendMsg(self, msg):
        self.__output_tb.insert(self.__iter_out, msg)


    def onUserJoined(self, contact):
        print "%s joined the conversation" % (contact,)

    def onUserLeft(self, contact):
        print "%s left the conversation" % (contact,)

    def onUserTyping(self, contact):
        print "%s is typing" % (contact,)

    def onMessageReceived(self, messageview):
        self.__outputAppendMsg(messageview.toStringView().toString())

    def nudge(self):
        #TODO
        print "Nudge received!!!"
