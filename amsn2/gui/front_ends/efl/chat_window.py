
from constants import *
import ecore
import ecore.evas
import ecore.x
import etk
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
        self.setTitle("aMSN - Chatwindow")
        self.resize(CW_WIDTH, CW_HEIGHT)

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

   etk_signal_connect_by_code(ETK_WIDGET_KEY_DOWN_SIGNAL, ETK_OBJECT(editor_view), ETK_CALLBACK(_etk_test_im_editor_key_down_cb), message_view);

   etk_widget_show_all(win);
}

/* Called when a key is pressed when the editor text view is focused */
static Etk_Bool _etk_test_im_editor_key_down_cb(Etk_Object *object, Etk_Event_Key_Down *event, void *data)
{
   Etk_Textblock *message_tb, *editor_tb;
   Etk_Textblock_Iter *iter, *cursor;
   Etk_String *message;
   int buddy_id;

   if (!(message_tb = etk_text_view_textblock_get(ETK_TEXT_VIEW(data))))
      return ETK_FALSE;
   if (!(editor_tb = etk_text_view_textblock_get(ETK_TEXT_VIEW(object))))
      return ETK_FALSE;

   message = etk_textblock_text_get(editor_tb, ETK_TRUE);
   if ((strcmp(event->keyname, "Return") == 0 || strcmp(event->keyname, "KP_Enter") == 0))
   {
      iter = etk_textblock_iter_new(message_tb);
      etk_textblock_iter_forward_end(iter);

      if (event->modifiers & ETK_MODIFIER_SHIFT)
      {
         cursor = etk_text_view_cursor_get(ETK_TEXT_VIEW(object));
         etk_textblock_insert(editor_tb, cursor, "\n", -1);
      }
      else
      {
         if (etk_string_length_get(message) > 0)
         {

            buddy_id = _num_messages % _num_im_buddies;
            etk_textblock_insert_markup(message_tb, iter, _im_buddies[buddy_id], -1);
            etk_textblock_insert_markup(message_tb, iter, etk_string_get(message), -1);
            etk_textblock_insert(message_tb, iter, "\n", -1);

            etk_textblock_clear(editor_tb);
            etk_object_destroy(ETK_OBJECT(message));
            _num_messages++;
         }
      }

      etk_textblock_iter_free(iter);
      return ETK_TRUE;
   }

   return ETK_FALSE;
}


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
