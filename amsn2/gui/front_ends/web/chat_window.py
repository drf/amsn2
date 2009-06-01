import md5
import random
from amsn2.core.views import ContactView, StringView

class aMSNChatWindow(object):
    """ This interface will represent a chat window of the UI
        It can have many aMSNChatWidgets"""
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self._uid = md5.new(str(random.random())).hexdigest()
        self._main = amsn_core._core._main
        self._main.send("newChatWindow",[self._uid])

    def addChatWidget(self, chat_widget):
        """ add an aMSNChatWidget to the window """
        self._main.send("addChatWidget",[self._uid,chat_widget._uid])

    def show(self):
        self._main.send("showChatWindow",[self._uid])

    def hide(self):
        self._main.send("hideChatWindow",[self._uid])

    def add(self):
        print "aMSNChatWindow.add"
        pass

    def move(self):
        print "aMSNChatWindow.move"
        pass

    def remove(self):
        print "aMSNChatWindow.remove"
        pass

    def attach(self):
        print "aMSNChatWindow.attach"
        pass

    def detach(self):
        print "aMSNChatWindow.detach"
        pass

    def close(self):
        print "aMSNChatWindow.close"
        pass

    def flash(self):
        print "aMSNChatWindow.flash"
        pass
    """TODO: move, remove, detach, attach (shouldn't we use add ?), close,
        flash..."""


class aMSNChatWidget(object):
    """ This interface will present a chat widget of the UI """
    def __init__(self, amsn_conversation, parent):
        """ create the chat widget for the 'parent' window, but don't attach to
        it."""
        self._main=parent._main
        self._uid=md5.new(str(random.random())).hexdigest()
        self._main.send("newChatWidget",[self._uid])
        self._main.addListener("sendMessage",self.sendMessage)
        self._amsn_conversation=amsn_conversation
    
    def sendMessage(self,smL):
        if smL[0]==self._uid:
            stmess = StringView()
            stmess.appendText(smL[1])
            self._amsn_conversation.sendMessage(stmess)
        return True
        
        

    def onMessageReceived(self, messageview):
        """ Called for incoming and outgoing messages
            message: a MessageView of the message"""
        self._main.send("onMessageReceivedChatWidget",[self._uid,messageview.toStringView().toString()])

    def nudge(self):
        self._main.send("nudgeChatWidget",[self._uid])

