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
        # TODO: Init chat window code from amsn core here
        
        self._amsn_conversation = amsn_conversation
        self.ui = Ui_ChatWindow()
        self.ui.setupUi(self)
        
        self.loadEmoticonList()
        
        QObject.connect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)
        QObject.connect(self.ui.sendButton, SIGNAL("clicked()"), self.__sendMessage)
        QObject.connect(self.ui.actionInsert_Emoticon, SIGNAL("triggered()"), self.showEmoticonList)
        self.enterShortcut = QShortcut("Enter", self.ui.inputWidget)
        QObject.connect(self.enterShortcut, SIGNAL("activated()"), self.__sendMessage)
        
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
        
        QObject.connect(self.ui.inputWidget, SIGNAL("textChanged()"), self.processInput)
        
    def loadEmoticonList(self):
        self.emoticonList = QStringList()
        
        """ TODO: Request emoticon list from amsn core, maybe use a QMap to get the image URL? """
        
        """ TODO: Discuss how to handle custom emoticons. We have to provide an option
        to change the default icon theme, this includes standard emoticons too.
        Maybe qrc? """
        
        self.emoticonList << ";)" << ":)" << "EmOtIcOn"
        
    def showEmoticonList(self):
        """ Let's popup emoticon selection here """
        print "Guess what? No emoticons. But I'll put in a random one for you"
        self.appendImageAtCursor("throbber.gif")
        
    def __sendMessage(self):
        msg = self.ui.inputWidget.toPlainText()
        self.ui.inputWidget.clear()
        strv = StringView()
        strv.appendText(str(msg))
        self._amsn_conversation.sendMessage(strv)
        self.ui.textEdit.append("<b>/me says:</b><br>"+msg+"")
        
    def __sendNudge(self):
        self._amsn_conversation.sendNudge()
        self.ui.textEdit.append("<b>/me sent a nudge</b>")
        
    def appendTextAtCursor(self, text):
        self.ui.inputWidget.textCursor().insertHtml(str(text))
        
    def appendImageAtCursor(self, image):
        self.ui.inputWidget.textCursor().insertHtml(QString("<img src=\"" + str(image) + "\" />"))
        
    def onUserJoined(self, contact):
        self.ui.textEdit.append("<b>"+contact.name.toString()+" "+self.tr("has joined the conversation")+("</b>"))
        pass

    def onUserLeft(self, contact):
        self.ui.textEdit.append("<b>"+contact.name.toString()+" "+self.tr("has left the conversation")+("</b>"))
        pass

    def onUserTyping(self, contact):
        self.ui.statusText.setText(QString(contact.name.toString() + " is typing"))

    def onMessageReceived(self, sender, message):
        print "Ding!"
        self.ui.textEdit.append("<b>"+sender.name.toString()+" "+self.tr("writes:")+("</b>"))
        self.ui.textEdit.append(message.toString())
        pass

    def onNudgeReceived(self, sender):
        self.ui.textEdit.append("<b>"+sender.name.toString()+" "+self.tr("sent you a nudge!")+("</b>"))
        pass
        
