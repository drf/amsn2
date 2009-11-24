from constants import *
import evas
import ecore
import elementary
import skins
import window
from amsn2.gui import base
from amsn2.core.views import ContactView, StringView
from constants import *

class aMSNChatWindow(window.aMSNWindow, base.aMSNChatWindow):
    def __init__(self, conversation_manager):
        self._conversation_manager = conversation_manager
        window.aMSNWindow.__init__(self, conversation_manager._core)
        self._container = aMSNChatWidgetContainer()
        self.setTitle(TITLE + " - Chatwindow")
        self.resize(CW_WIDTH, CW_HEIGHT)

        self.autodel_set(True)

    def addChatWidget(self, chat_widget):
        self.resize_object_add(chat_widget)
        chat_widget.show()
        print chat_widget.ine.geometry
        print chat_widget.insc.geometry

#TODO: ChatWidgetContainer
class aMSNChatWidgetContainer:
    pass




class aMSNChatWidget(elementary.Box, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, parent, contacts_uid):
        self._parent = parent
        elementary.Box.__init__(self, parent)
        self.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.homogenous_set(False)
        self._parent.resize_object_add(self)
        self.show()
        self._amsn_conversation = amsn_conversation

        self.outsc = elementary.Scroller(parent)
        self.outsc.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                        evas.EVAS_HINT_EXPAND)
        self.outsc.size_hint_align_set(evas.EVAS_HINT_FILL,
                                       evas.EVAS_HINT_FILL)
        self.outsc.policy_set(elementary.ELM_SCROLLER_POLICY_AUTO,
                      elementary.ELM_SCROLLER_POLICY_AUTO)
        self.outsc.bounce_set(False, True)
        self.pack_end(self.outsc)

        self.outbx = elementary.Box(parent)
        self.outsc.content_set(self.outbx)
        self.outbx.show()
        self.outsc.show()

        self.inbx = elementary.Box(parent)
        self.inbx.horizontal_set(True)
        self.inbx.homogenous_set(False)
        self.inbx.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                       0.0)
        self.inbx.size_hint_align_set(evas.EVAS_HINT_FILL,
                                      0.5)
        self.pack_end(self.inbx)

        self.insc = elementary.Scroller(parent)
        self.insc.content_min_limit(0, 1)
        self.insc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                             elementary.ELM_SCROLLER_POLICY_OFF)
        self.insc.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                       evas.EVAS_HINT_EXPAND)
        self.insc.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.inbx.pack_end(self.insc)

        self.ine = elementary.Entry(parent)
        self.ine.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                      evas.EVAS_HINT_EXPAND)
        self.ine.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.insc.content_set(self.ine)
        self.ine.show()
        self.insc.show()

        self.inb = elementary.Button(parent)
        self.inb.label_set("Send")
        self.inb.callback_clicked_add(self.__sendButton_cb, self.ine)
        self.inbx.pack_end(self.inb)
        self.inb.show()
        self.inbx.show()

        self.show()

    def __sendButton_cb(self, button, entry):
        pass
        """
        msg = self.__input_tb.text_get(0)
        self.__input_tb.clear()
        strv = StringView()
        strv.appendText(msg)
        self._amsn_conversation.sendMessage(strv)
        """

    def __outputAppendMsg(self, msg):
        pass
        """
        self.__output_tb.insert(self.__iter_out, msg)
        """


    def onUserJoined(self, contact):
        print "%s joined the conversation" % (contact,)

    def onUserLeft(self, contact):
        print "%s left the conversation" % (contact,)

    def onUserTyping(self, contact):
        print "%s is typing" % (contact,)

    def onMessageReceived(self, messageview, formatting=None):
        pass
        """
        self.__outputAppendMsg(str(messageview.toStringView()))
        """

    def nudge(self):
        #TODO
        print "Nudge received!!!"
