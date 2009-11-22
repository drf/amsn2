from constants import *
import ecore
import ecore.evas
import ecore.x
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

        #TODO:
        self.autodel_set(True)

    def addChatWidget(self, chat_widget):
        #TODO: use the container
        self.child = chat_widget

#TODO: ChatWidgetContainer
class aMSNChatWidgetContainer:
    pass




class aMSNChatWidget(elementary.Box, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, parent, contacts_uid):
        self._parent = parent
        elementary.Box.__init__(self, parent)
        self.size_hint_weight_set(1.0, 1.0)
        self.size_hint_align_set(-1.0, -1.0)
        self.homogenous_set(False)
        self._parent.resize_object_add(self)
        self.show()
        self._amsn_conversation = amsn_conversation


        self.outsc = elementary.Scroller(parent)
        self.outsc.size_hint_weight_set(1.0, 1.0)
        self.outsc.size_hint_align_set(-1.0, -1.0)
        self.outsc.policy_set(elementary.ELM_SCROLLER_POLICY_ON,
                      elementary.ELM_SCROLLER_POLICY_ON)
        self.outsc.bounce_set(False, True)
        self.pack_end(self.outsc)

        self.outbx = elementary.Box(parent)
        self.outsc.content_set(self.outbx)
        self.outbx.show()
        self.outsc.show()

        self.inbx = elementary.Box(parent)
        self.inbx.horizontal_set(True)
        self.inbx.homogenous_set(False)
        self.pack_end(self.inbx)

        self.insc = elementary.Scroller(parent)
        self.insc.content_min_limit(0, 1)
        self.insc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                             elementary.ELM_SCROLLER_POLICY_OFF);
        self.insc.size_hint_weight_set(1.0, 0.0)
        self.insc.size_hint_align_set(-1.0, -1.0)
        self.ine = elementary.Entry(parent)
        self.ine.size_hint_weight_set(1.0, 1.0)
        self.ine.size_hint_align_set(-1.0, -1.0)
        self.inbx.pack_end(self.ine)
        self.insc.content_set(self.ine)
        self.ine.show()
        self.insc.show()

        self.inb = elementary.Button(parent)
        self.inb.label_set("Send")
        self.inbx.pack_end(self.inb)
        self.inb.show()
        self.inbx.show()


        self.show()

        """
        etk.VPaned.__init__(self)
        self._input = etk.TextView()
        self._input.size_request_set(CW_IN_MIN_WIDTH, CW_IN_MIN_HEIGHT)
        self.__input_tb = self._input.textblock_get()



        self._input_container = etk.HBox()
        self.child2_set(self._input_container, 0)
        self._send_button = etk.Button(label="Send")
        self._send_button.on_clicked(self.__sendButton_cb)
        self._input_container.append(self._input, etk.HBox.START, etk.HBox.EXPAND_FILL, 0)
        self._input_container.append(self._send_button, etk.HBox.START, etk.HBox.NONE, 0)


        self._output = etk.TextView()
        self._output.size_request_set(CW_OUT_MIN_WIDTH, CW_OUT_MIN_HEIGHT)
        self.child1_set(self._output, 1)
        self.__output_tb = self._output.textblock_get()
        self.__iter_out = etk.TextblockIter(self.__output_tb)
        self.__iter_out.forward_end()
        self._output.pass_mouse_events_set(1) #not focusable

        def editor_key_down(obj, event):
            if event.keyname in ("Return", "KP_Enter"):
                if event.modifiers is etk.c_etk.EventEnums.MODIFIER_NONE:
                    self.__sendButton_cb(self._send_button)
                    return False
                elif event.modifiers is etk.c_etk.EventEnums.MODIFIER_SHIFT:
                    iter = etk.TextblockIter(self.__input_tb)
                    iter.forward_end()
                    self.__input_tb.insert(iter, '\n')
                    return False
            return True
        self._input.on_key_down(editor_key_down)
        """

    def __sendButton_cb(self, button):
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

    def onMessageReceived(self, messageview):
        pass
        """
        self.__outputAppendMsg(str(messageview.toStringView()))
        """

    def nudge(self):
        #TODO
        print "Nudge received!!!"
